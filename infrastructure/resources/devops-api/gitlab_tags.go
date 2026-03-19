package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/Masterminds/semver/v3"
)

var tagBlacklist = []string{
	"develop-",
	"test",
	"rc-",
	"nac",
	"releasetest",
	"snapshot-",
	"remove_",
}

type GitLabTag struct {
	Name   string `json:"name"`
	Commit struct {
		CreatedAt time.Time `json:"created_at"`
	} `json:"commit"`
}

type Tag struct {
	Name      string
	CreatedAt time.Time
}

func isBlacklisted(tag string) bool {

	tag = strings.ToLower(tag)

	for _, prefix := range tagBlacklist {

		if strings.HasPrefix(tag, prefix) {
			return true
		}
	}

	return false
}

func filterBlacklisted(tags []Tag) []Tag {

	var result []Tag

	for _, t := range tags {

		if !isBlacklisted(t.Name) {
			result = append(result, t)
		}
	}

	return result
}

func extractVersion(tag string) string {

	tag = strings.TrimPrefix(tag, "version/")
	tag = strings.TrimPrefix(tag, "v")

	parts := strings.Split(tag, "-")

	return parts[0]
}

func sortByDate(tags []Tag) {

	sort.Slice(tags, func(i, j int) bool {
		return tags[i].CreatedAt.After(tags[j].CreatedAt)
	})
}

func sortByVersion(tags []Tag) {

	sort.Slice(tags, func(i, j int) bool {

		vi, err1 := semver.NewVersion(extractVersion(tags[i].Name))
		vj, err2 := semver.NewVersion(extractVersion(tags[j].Name))

		if err1 == nil && err2 == nil {
			return vi.GreaterThan(vj)
		}

		return tags[i].Name > tags[j].Name
	})
}

func uniqueVersions(tags []Tag) []Tag {

	seen := map[string]bool{}
	var result []Tag

	for _, t := range tags {

		base := extractVersion(t.Name)

		if !seen[base] {
			seen[base] = true
			result = append(result, t)
		}
	}

	return result
}

func limitTags(tags []Tag, limit int) []Tag {

	if limit <= 0 || limit >= len(tags) {
		return tags
	}

	return tags[:limit]
}

func fetchTags(repo string, perPage int) ([]Tag, error) {

	repo = normalizeRepo(repo)

	project := url.PathEscape(repo)

	page := 1
	var tags []Tag

	client := &http.Client{}

	for {

		endpoint := fmt.Sprintf(
			"%s/api/v4/projects/%s/repository/tags?per_page=%d&page=%d",
			gitlabURL,
			project,
			perPage,
			page,
		)

		req, err := http.NewRequest("GET", endpoint, nil)
		if err != nil {
			return nil, err
		}

		req.Header.Set("PRIVATE-TOKEN", gitlabToken)

		resp, err := client.Do(req)
		if err != nil {
			return nil, err
		}

		if resp.StatusCode != http.StatusOK {

			body, _ := io.ReadAll(resp.Body)
			resp.Body.Close()

			return nil, fmt.Errorf(
				"gitlab api error: %s\nendpoint: %s\nresponse: %s",
				resp.Status,
				endpoint,
				string(body),
			)
		}

		var gitlabTags []GitLabTag

		err = json.NewDecoder(resp.Body).Decode(&gitlabTags)
		resp.Body.Close()

		if err != nil {
			return nil, err
		}

		if len(gitlabTags) == 0 {
			break
		}

		for _, t := range gitlabTags {

			tags = append(tags, Tag{
				Name:      t.Name,
				CreatedAt: t.Commit.CreatedAt,
			})
		}

		page++
	}

	return tags, nil
}

// @Summary Get repository tags
// @Description Get semver tags from a GitLab repository
// @Tags tags
// @Produce json
// @Param repo query string true "Repository path (e.g. services/reporting)"
// @Param sort query string false "Sort order (date|version)"
// @Param limit query int false "Limit number of results"
// @Success 200 {array} string
// @Failure 400 {string} string "Invalid parameters"
// @Failure 500 {string} string "Internal error"
// @Router /tags [get]
func tagsHandler(w http.ResponseWriter, r *http.Request) {

	repo := r.URL.Query().Get("repo")
	sortType := r.URL.Query().Get("sort")
	unique := r.URL.Query().Get("unique")
	limitParam := r.URL.Query().Get("limit")
	perPageParam := r.URL.Query().Get("per_page")

	perPage := 100

	if perPageParam != "" {

		v, err := strconv.Atoi(perPageParam)

		if err == nil && v > 0 && v <= 100 {
			perPage = v
		}
	}

	if repo == "" {
		http.Error(w, "repo parameter is required", http.StatusBadRequest)
		return
	}

	tags, err := fetchTags(repo, perPage)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	tags = filterBlacklisted(tags)

	switch sortType {

	case "version":
		sortByVersion(tags)

	case "date":
		sortByDate(tags)

	default:
		sortByDate(tags)
	}

	if unique == "true" {
		tags = uniqueVersions(tags)
	}

	if limitParam != "" {

		limit, err := strconv.Atoi(limitParam)

		if err == nil {
			tags = limitTags(tags, limit)
		}
	}

	var result []string

	for _, t := range tags {
		result = append(result, t.Name)
	}

	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(result)
}

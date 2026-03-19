package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"sort"
	"strings"
	"time"
)

func gitlabTree(blueprint string, path string) ([]GitLabItem, error) {

	project := url.PathEscape(
		fmt.Sprintf("seaallocation/infrastructure/blueprints/%s", blueprint),
	)

	endpoint := fmt.Sprintf(
		"%s/api/v4/projects/%s/repository/tree?path=%s&per_page=100",
		gitlabURL,
		project,
		path,
	)

	req, err := http.NewRequest("GET", endpoint, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("PRIVATE-TOKEN", gitlabToken)

	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {

		body, _ := io.ReadAll(resp.Body)

		return nil, fmt.Errorf(
			"gitlab api error: %s\nresponse: %s",
			resp.Status,
			string(body),
		)
	}

	var items []GitLabItem

	err = json.NewDecoder(resp.Body).Decode(&items)

	return items, err
}

// @Summary Get platforms
// @Tags blueprints
// @Produce json
// @Success 200 {array} string
// @Router /blueprints/platforms [get]
func platformsHandler(w http.ResponseWriter, r *http.Request) {

	blueprint := r.URL.Query().Get("blueprint")

	items, err := gitlabTree(blueprint, "")
	if err != nil {
		respondError(w, err)
		return
	}

	var list []string

	for _, i := range items {

		if i.Type == "tree" {
			list = append(list, i.Name)
		}
	}

	sort.Strings(list)
	respondJSON(w, APIResponse{
		Status: "ok",
		Data:   list,
	})
}

// @Summary Get environments
// @Tags blueprints
// @Produce json
// @Success 200 {array} string
// @Router /blueprints/environments [get]
func environmentsHandler(w http.ResponseWriter, r *http.Request) {

	blueprint := r.URL.Query().Get("blueprint")
	platform := r.URL.Query().Get("platform")

	path := platform
	items, err := gitlabTree(blueprint, path)
	if err != nil {
		respondError(w, err)
		return
	}

	var list []string

	for _, i := range items {

		if i.Type == "tree" {
			list = append(list, i.Name)
		}
	}

	sort.Strings(list)
	respondJSON(w, APIResponse{
		Status: "ok",
		Data:   list,
	})
}

// @Summary Get services
// @Tags blueprints
// @Produce json
// @Success 200 {array} string
// @Router /blueprints/services [get]
func servicesHandler(w http.ResponseWriter, r *http.Request) {

	blueprint := r.URL.Query().Get("blueprint")
	platform := r.URL.Query().Get("platform")
	env := r.URL.Query().Get("env")

	path := fmt.Sprintf("%s/%s", platform, env)
	items, err := gitlabTree(blueprint, path)

	if err != nil {
		respondError(w, err)
		return
	}

	var list []string

	for _, i := range items {

		if i.Type == "blob" && strings.HasSuffix(i.Name, ".yaml") {

			name := strings.TrimSuffix(i.Name, ".yaml")

			list = append(list, name)
		}
	}

	sort.Strings(list)
	respondJSON(w, APIResponse{
		Status: "ok",
		Data:   list,
	})
}

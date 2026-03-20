package main

import (
	"encoding/json"
	"net/http"
	"net/url"
	"os"
	"strings"
)

var gitlabURL = strings.TrimRight(os.Getenv("GITLAB_URL"), "/")
var gitlabToken = os.Getenv("GITLAB_TOKEN")
var pghost = os.Getenv("PG_HOST")
var user = os.Getenv("POSTGRES_USER")
var password = os.Getenv("POSTGRES_PASSWORD")
var maxTags = os.Getenv("gitlab_max_tags")

type APIResponse struct {
	Status string   `json:"status"`
	Data   []string `json:"data,omitempty"`
	Error  string   `json:"error,omitempty"`
}

type VersionResponse struct {
	Version string   `json:"version"`
	Data    []string `json:"data,omitempty"`
	Error   string   `json:"error,omitempty"`
}

type GitLabItem struct {
	Name string `json:"name"`
	Type string `json:"type"`
}

func respondJSON(w http.ResponseWriter, payload interface{}) {

	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(payload)
}

func respondError(w http.ResponseWriter, err error) {

	respondJSON(w, APIResponse{
		Status: "error",
		Error:  err.Error(),
	})
}

func normalizeRepo(repo string) string {

	repo = strings.TrimSpace(repo)

	if strings.HasPrefix(repo, "http") {

		u, err := url.Parse(repo)
		if err == nil {
			repo = strings.TrimPrefix(u.Path, "/")
		}
	}

	if strings.HasSuffix(repo, ".git") {
		repo = strings.TrimSuffix(repo, ".git")
	}

	if strings.HasPrefix(repo, "git@") {

		parts := strings.Split(repo, ":")

		if len(parts) == 2 {
			repo = parts[1]
		}
	}

	return repo
}

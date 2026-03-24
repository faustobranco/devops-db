package main

import (
	"encoding/json"
	"net/http"
	"os"
)

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

type IPResponse struct {
	Query   string `json:"query"`
	Country string `json:"country"`
	City    string `json:"city"`
}

func getLocation(ip string) (*IPResponse, error) {
	resp, err := http.Get("http://ip-api.com/json/" + ip)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var data IPResponse
	err = json.NewDecoder(resp.Body).Decode(&data)
	return &data, err
}

func respondJSON(w http.ResponseWriter, payload interface{}) {

	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(payload)
}

// @Summary Health check
// @Description Check if API is running
// @Tags health
// @Produce json
// @Success 200 {object} map[string]string
// @Router /health [get]
func healthHandler(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")

	respondJSON(w, APIResponse{Status: "ok"})
}

// @Summary Version check
// @Description Show APIs version (semver)
// @Tags version
// @Produce json
// @Success 200 {object} map[string]string
// @Router /version [get]
func versionHandler(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")

	respondJSON(w, VersionResponse{Version: os.Getenv("IPLOCATOR_VERSION")})
}

func main() {
	http.HandleFunc("/location", func(w http.ResponseWriter, r *http.Request) {
		ip := r.URL.Query().Get("ip")

		// fallback: usa IP do request
		if ip == "" {
			ip = r.RemoteAddr
		}

		location, err := getLocation(ip)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		json.NewEncoder(w).Encode(location)
	})
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/version", versionHandler)

	http.ListenAndServe(":8080", nil)
}

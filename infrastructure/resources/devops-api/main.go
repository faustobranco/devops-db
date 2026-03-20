package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"

	_ "github.com/lib/pq"

	_ "devops-api/docs"

	httpSwagger "github.com/swaggo/http-swagger"
)

var db *sql.DB

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

	respondJSON(w, VersionResponse{Version: os.Getenv("DEVOPSAPI_VERSION")})
}

func main() {

	http.HandleFunc("/health", healthHandler)

	http.HandleFunc("/databases", databasesHandler)
	http.HandleFunc("/schemas", schemasHandler)

	http.HandleFunc("/blueprints/platforms", platformsHandler)
	http.HandleFunc("/blueprints/environments", environmentsHandler)
	http.HandleFunc("/blueprints/services", servicesHandler)

	http.HandleFunc("/tags", tagsHandler)
	http.HandleFunc("/version", versionHandler)

	http.Handle("/swagger/", httpSwagger.WrapHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	fmt.Println("devops-api listening on :" + port)

	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		panic(err)
	}
}

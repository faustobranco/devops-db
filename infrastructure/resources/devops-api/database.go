package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"strings"
)

func openDB(host, database string) (*sql.DB, error) {

	connStr := fmt.Sprintf(
		"host=%s user=%s password=%s dbname=%s sslmode=require connect_timeout=5",
		host,
		user,
		password,
		database,
	)

	return sql.Open("postgres", connStr)
}

func resolveDBHost(service, env string) string {

	service = strings.ToLower(service)
	env = strings.ToLower(env)

	key := service + "_" + env
	fmt.Println("env key:", key)

	return os.Getenv(key)
}

// @Summary Get databases
// @Description List databases for a service and environment
// @Tags databases
// @Produce json
// @Param service query string true "Service name"
// @Param env query string true "Environment"
// @Success 200 {object} map[string]interface{}
// @Router /databases [get]
func databasesHandler(w http.ResponseWriter, r *http.Request) {

	service := r.URL.Query().Get("service")
	env := r.URL.Query().Get("env")

	fmt.Println("service:", service)
	fmt.Println("env:", env)

	if service == "" || env == "" {
		respondJSON(w, APIResponse{
			Status: "error",
			Error:  "missing service or env parameter",
		})
		return
	}

	host := resolveDBHost(service, env)

	if host == "" {
		respondJSON(w, APIResponse{
			Status: "error",
			Error:  "database host not configured",
		})
		return
	}

	conn, err := openDB(host, "postgres")
	if err != nil {
		respondError(w, err)
		return
	}
	defer conn.Close()

	rows, err := conn.Query(`
		SELECT datname
		FROM pg_database
		WHERE datistemplate = false
	`)
	if err != nil {
		respondError(w, err)
		return
	}

	defer rows.Close()

	var list []string

	for rows.Next() {

		var name string

		err := rows.Scan(&name)
		if err != nil {
			continue
		}

		list = append(list, name)
	}
	if err := rows.Err(); err != nil {
		respondError(w, err)
		return
	}

	respondJSON(w, APIResponse{
		Status: "ok",
		Data:   list,
	})
}

// @Summary Get schemas
// @Description List schemas for a database
// @Tags schemas
// @Produce json
// @Param service query string true "Service name"
// @Param env query string true "Environment"
// @Param db query string true "Database name"
// @Success 200 {object} map[string]interface{}
// @Router /schemas [get]
func schemasHandler(w http.ResponseWriter, r *http.Request) {

	database := r.URL.Query().Get("db")

	if database == "" {
		respondJSON(w, APIResponse{
			Status: "error",
			Error:  "missing db parameter",
		})
		return
	}

	service := r.URL.Query().Get("service")
	env := r.URL.Query().Get("env")

	host := resolveDBHost(service, env)

	conn, err := openDB(host, database)
	if err != nil {
		respondError(w, err)
		return
	}

	defer conn.Close()

	rows, err := conn.Query(`
		SELECT nspname
		FROM pg_namespace
		WHERE nspname NOT LIKE 'pg_%'
		AND nspname != 'information_schema'
		ORDER BY nspname;
	`)
	if err != nil {
		respondError(w, err)
		return
	}

	defer rows.Close()

	var list []string

	for rows.Next() {

		var name string

		err := rows.Scan(&name)
		if err != nil {
			continue
		}

		list = append(list, name)
	}
	if err := rows.Err(); err != nil {
		respondError(w, err)
		return
	}

	respondJSON(w, APIResponse{
		Status: "ok",
		Data:   list,
	})
}

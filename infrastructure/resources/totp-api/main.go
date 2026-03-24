package main

import (
	"crypto/hmac"
	"crypto/sha1"
	"encoding/base32"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
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

type TotPResponse struct {
	Totp  string   `json:"totp"`
	Data  []string `json:"data,omitempty"`
	Error string   `json:"error,omitempty"`
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

	respondJSON(w, VersionResponse{Version: os.Getenv("TOTPVALIDATOR_VERSION")})
}

func totphHandler(w http.ResponseWriter, r *http.Request) {

	secret := r.URL.Query().Get("secret")

	w.Header().Set("Content-Type", "application/json")

	code, err := generateTOTP(secret)
	if err != nil {
		panic(err)
	}

	respondJSON(w, TotPResponse{Totp: code})
}

func generateTOTP(secret string) (string, error) {

	secret = strings.ToUpper(secret)

	key, err := base32.StdEncoding.WithPadding(base32.NoPadding).DecodeString(secret)
	if err != nil {
		return "", err
	}

	timestep := time.Now().Unix() / 30

	var buf [8]byte
	binary.BigEndian.PutUint64(buf[:], uint64(timestep))

	h := hmac.New(sha1.New, key)
	h.Write(buf[:])
	hash := h.Sum(nil)

	offset := hash[len(hash)-1] & 0x0F

	truncated := binary.BigEndian.Uint32(hash[offset : offset+4])
	truncated &= 0x7fffffff

	code := truncated % 1000000

	return fmt.Sprintf("%06d", code), nil
}

func main() {

	http.HandleFunc("/totp", totphHandler)
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/version", versionHandler)

	http.ListenAndServe(":8080", nil)

}

# build stage
FROM golang:1.26-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o devops-api
#RUN CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o devops-api

# runtime stage
FROM nexus.devops-db.internal/base_images/base_go:1.0.4

WORKDIR /app

COPY --from=builder /app/devops-api .

EXPOSE 8080

CMD ["./devops-api"]


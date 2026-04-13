FROM alpine:3.20

RUN apk add --no-cache \
    ca-certificates \
 && addgroup -g 10001 app \
 && adduser -D -u 10001 -G app app

WORKDIR /app

USER app
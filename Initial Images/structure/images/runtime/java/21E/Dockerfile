# ---- builder ----
FROM eclipse-temurin:21 AS builder

RUN jlink \
    --add-modules java.base,java.logging \
    --strip-debug \
    --no-man-pages \
    --no-header-files \
    --output /jre

# ---- runtime ----
FROM nexus.devops-db.internal/docker-base-images-public/tooling-extended-debian:1.0.0

COPY --from=builder /jre /jre

ENV JAVA_HOME=/jre
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

USER app

ENTRYPOINT ["java"]
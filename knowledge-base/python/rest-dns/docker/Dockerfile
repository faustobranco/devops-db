FROM nexus.devops-db.internal/docker-base-images-public/ubuntu_python:3.10.6

WORKDIR /app

# Install CA certificates
RUN curl -sk -O https://nexus.devops-db.internal/repository/certificate-internal/pki/root/devops-db-root-ca.crt && \
    curl -sk -O https://nexus.devops-db.internal/repository/certificate-internal/pki/intermediate/devops-db-intermediate.crt && \
    cat devops-db-root-ca.crt devops-db-intermediate.crt > devops-db-chain.crt && \
    cp devops-db-root-ca.crt        /usr/local/share/ca-certificates/devops-db-root-ca.crt && \
    cp devops-db-intermediate.crt   /usr/local/share/ca-certificates/devops-db-intermediate.crt && \
    cp devops-db-chain.crt          /usr/local/share/ca-certificates/devops-db-chain.crt && \
    update-ca-certificates && \
    rm devops-db-root-ca.crt devops-db-intermediate.crt devops-db-chain.crt

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY *.py .

EXPOSE 8080

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

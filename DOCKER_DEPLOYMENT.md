# Docker Deployment Guide for TECHNOSHIELD

This guide provides instructions for deploying the TECHNOSHIELD application using Docker and Docker Compose.

## Prerequisites

- Docker Engine (version 20.10.0 or higher)
- Docker Compose (version 2.0.0 or higher)
- Git

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/technoshield.git
cd technoshield
```

### 2. Configure Environment Variables

1. Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

2. Edit the `.env` file and set the required environment variables:

```
# PostgreSQL Configuration
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=technoshield

# JWT Authentication
SECRET_KEY=your_generated_secret_key

# Grafana Credentials
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=your_secure_grafana_password

# SSL/TLS Configuration
SSL_CERT_PATH=/path/to/ssl/certificate
SSL_KEY_PATH=/path/to/ssl/key
```

### 3. Generate Security Credentials

#### Generate JWT Secret Key

For Linux/macOS:
```bash
./scripts/generate_jwt_secret.sh
```

For Windows:
```powershell
.\scripts\generate_jwt_secret.ps1
```

#### Generate SSL Certificates (for HTTPS)

For Linux/macOS:
```bash
./scripts/generate_ssl_certs.sh
```

For Windows:
```powershell
.\scripts\generate_ssl_certs.ps1
```

### 4. Build and Start the Containers

```bash
docker-compose up -d --build
```

This command will:
- Build the Docker images for all services
- Create and start the containers in detached mode

### 5. Verify Deployment

After the containers are up and running, you can access the following services:

- Frontend: https://localhost
- Backend API: https://localhost/api
- API Documentation: https://localhost/api/docs
- Grafana Dashboards: https://localhost:3000 (default credentials: admin/your_secure_grafana_password)

### 6. Container Management

#### View Running Containers

```bash
docker-compose ps
```

#### View Container Logs

```bash
# View logs for all containers
docker-compose logs

# View logs for a specific service
docker-compose logs backend
```

#### Stop Containers

```bash
docker-compose down
```

#### Stop and Remove Volumes

```bash
docker-compose down -v
```

## Production Deployment Considerations

### Security

- Ensure all passwords in the `.env` file are strong and unique
- Use proper SSL certificates from a trusted certificate authority for production
- Consider using Docker secrets for sensitive information
- Implement network segmentation using Docker networks

### Performance

- Configure resource limits for containers based on your server capacity
- Implement container health checks
- Set up container restart policies

### High Availability

- Consider using Docker Swarm or Kubernetes for orchestration in production
- Implement load balancing for the frontend and backend services
- Set up database replication for PostgreSQL

### Monitoring

- The deployment includes Prometheus and Grafana for monitoring
- Configure alerting in Grafana for critical metrics
- Set up log aggregation using a tool like ELK stack or Loki

## Troubleshooting

### Common Issues

1. **Container fails to start**
   - Check container logs: `docker-compose logs [service_name]`
   - Verify environment variables are set correctly
   - Ensure ports are not already in use

2. **Database connection issues**
   - Verify PostgreSQL container is running
   - Check database credentials in the `.env` file
   - Ensure the database has been initialized properly

3. **SSL/TLS certificate problems**
   - Verify certificate paths in the `.env` file
   - Check that certificates are valid and not expired
   - Ensure the Nginx configuration is correctly referencing the certificates

## Updating the Application

```bash
# Pull the latest changes
git pull

# Rebuild and restart the containers
docker-compose up -d --build
```

## Backup and Restore

### Backup PostgreSQL Data

```bash
docker-compose exec postgres pg_dump -U your_postgres_user technoshield > backup.sql
```

### Restore PostgreSQL Data

```bash
cat backup.sql | docker-compose exec -T postgres psql -U your_postgres_user technoshield
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image Documentation](https://hub.docker.com/_/postgres)
- [Nginx Docker Image Documentation](https://hub.docker.com/_/nginx)
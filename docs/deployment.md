# Deployment Guide

## Publishing to PyPI

The DEGIRO Portfolio package is automatically published to PyPI using GitHub Actions when you create a release tag.

## Automated Publishing Process

### Prerequisites

1. **Set up PyPI Trusted Publishing** (Recommended):
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new publisher:
     - **PyPI Project Name**: `degiro-portfolio`
     - **Owner**: Your GitHub username
     - **Repository**: `degiro-portfolio`
     - **Workflow name**: `publish.yml`
     - **Environment name**: `pypi`

2. **Alternative: API Token**:
   - Create token at https://pypi.org/manage/account/token/
   - Add to GitHub Secrets as `PYPI_API_TOKEN`

### Release Process

1. **Update Version**:
   ```bash
   # Edit pyproject.toml
   version = "0.2.1"
   ```

2. **Run Tests**:
   ```bash
   uv run pytest
   ```

3. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Release v0.2.1"
   ```

4. **Create and Push Tag**:
   ```bash
   git tag v0.2.1
   git push origin main
   git push origin v0.2.1
   ```

5. **GitHub Actions Will**:
   - Run full test suite
   - Build the package
   - Publish to PyPI
   - Create GitHub Release with artifacts

## Manual Publishing

If you need to publish manually:

```bash
# Build the package
uv build

# Publish to PyPI (requires PyPI credentials)
uv publish

# Or use twine
uv run pip install twine
uv run twine upload dist/*
```

## Installation from PyPI

Once published, users can install via:

```bash
pip install degiro-portfolio

# Or with uv
uv pip install degiro-portfolio
```

## Local Deployment

### Development Deployment

```bash
# Clone repository
git clone <repository-url>
cd degiro-portfolio

# Install dependencies
uv sync

# Setup data
uv run invoke demo-setup

# Start server
./degiro-portfolio start
```

### Production Deployment

For production use, consider:

1. **Use a process manager**:
   ```bash
   # systemd service
   sudo systemctl start degiro-portfolio

   # Or PM2
   pm2 start ./degiro-portfolio
   ```

2. **Set up reverse proxy** (nginx example):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Configure SSL/TLS**:
   ```bash
   # Using certbot
   sudo certbot --nginx -d your-domain.com
   ```

4. **Environment Variables**:
   ```bash
   # Create .env file
   DATABASE_URL=sqlite:///path/to/degiro-portfolio.db
   HOST=0.0.0.0
   PORT=8000
   ```

## Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 8000

# Start server
CMD ["./degiro-portfolio", "start"]
```

Build and run:

```bash
# Build image
docker build -t degiro-portfolio .

# Run container
docker run -p 8000:8000 -v $(pwd)/data:/app/data degiro-portfolio
```

## Cloud Deployment

### Heroku

```bash
# Create Procfile
echo "web: uvicorn src.degiro_portfolio.main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
heroku create degiro-portfolio
git push heroku main
```

### Railway

1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically on push

### AWS/GCP/Azure

Deploy as a containerized application or serverless function.

## Database Considerations

### SQLite (Default)

- Suitable for personal use
- Single file database
- No setup required
- Backup: just copy `degiro-portfolio.db`

### PostgreSQL (Production)

For multi-user deployments:

```python
# Update database.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/degiro"
)
```

## Monitoring

### Health Check Endpoint

Add to `main.py`:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Logging

Configure logging for production:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Backup Strategy

### Database Backups

```bash
# Backup SQLite database
cp degiro-portfolio.db degiro-portfolio-backup-$(date +%Y%m%d).db

# Automated daily backup
0 2 * * * cp /path/to/degiro-portfolio.db /backups/degiro-$(date +\%Y\%m\%d).db
```

### Transaction Data

Keep original Excel files as backup:
- Store securely
- Version control transaction imports
- Export database periodically

## Security Considerations

1. **Authentication**: Add authentication for production use
2. **HTTPS**: Always use HTTPS in production
3. **Secrets**: Use environment variables for sensitive data
4. **Updates**: Keep dependencies updated
5. **Firewall**: Restrict access to necessary ports

## Performance Optimization

### Database Indexes

Add indexes for frequently queried fields in `database.py`.

### Caching

Consider caching for:
- Stock prices (update periodically)
- Market indices
- Chart data

### CDN

Serve static assets from CDN in production.

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Locked

```bash
# Stop server
./degiro-portfolio stop

# Check for stale connections
fuser degiro-portfolio.db

# Restart
./degiro-portfolio start
```

### Memory Issues

Monitor memory usage:
```bash
# Check memory
top -p $(pgrep -f degiro-portfolio)

# Restart periodically
crontab -e
0 3 * * * /path/to/degiro-portfolio restart
```

## Support

For deployment issues:
- Check [GitHub Issues](https://github.com/your-username/degiro-portfolio/issues)
- Review application logs
- Verify configuration
- Test in development first

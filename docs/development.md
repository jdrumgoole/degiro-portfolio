# Development Guide

## Development Environment

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd degiro-portfolio

# Install dependencies including dev dependencies
uv sync

# Install Playwright browsers for testing
uv run playwright install chromium
```

## Project Structure

```
degiro-portfolio/
├── src/degiro_portfolio/      # Main application code
│   ├── __init__.py
│   ├── database.py           # Database models and configuration
│   ├── import_data.py        # Transaction import logic
│   ├── fetch_prices.py       # Price fetching logic
│   ├── fetch_indices.py      # Index data fetching
│   ├── main.py               # FastAPI application
│   └── static/
│       └── index.html        # Frontend interface
├── tests/                    # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_*.py            # Test files
│   └── README.md
├── docs/                    # Sphinx documentation
├── .github/                 # GitHub Actions workflows
├── tasks.py                 # Invoke tasks
├── degiro-portfolio         # CLI script
└── pyproject.toml          # Project configuration
```

## Development Workflow

### Starting Development Server

The development server includes auto-reload for rapid iteration:

```bash
uv run invoke dev
```

This starts uvicorn with `--reload` flag, which automatically restarts when code changes.

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

3. **Run tests**:
   ```bash
   uv run invoke test
   ```

4. **Format code**:
   ```bash
   uv run invoke format-code
   ```

5. **Run linting**:
   ```bash
   uv run invoke lint
   ```

6. **Commit changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

### Invoke Tasks

Common development tasks:

```bash
# Start/stop/restart server
uv run invoke start
uv run invoke stop
uv run invoke restart
uv run invoke status

# Development server with auto-reload
uv run invoke dev

# Testing
uv run invoke test

# Code quality
uv run invoke lint
uv run invoke format-code

# Database operations
uv run invoke db-info
uv run invoke purge-data
uv run invoke clean

# Data management
uv run invoke import-data
uv run invoke load-demo
uv run invoke fetch-prices
uv run invoke fetch-indices

# View logs
uv run invoke logs
```

## Code Style

### Python

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Use Ruff for linting and formatting

### JavaScript

- Use modern ES6+ syntax
- Keep vanilla JavaScript (no frameworks)
- Comment complex logic
- Use meaningful variable names

## Database Development

### Models

Database models are defined in `src/degiro_portfolio/database.py` using SQLAlchemy ORM.

Key models:
- `Stock`: Stock metadata
- `Transaction`: Transaction history
- `StockPrice`: Historical OHLCV data
- `Index`: Market index metadata
- `IndexPrice`: Index historical prices

### Making Schema Changes

1. Modify models in `database.py`
2. Delete existing database: `uv run invoke clean`
3. Restart server to recreate schema
4. Re-import data: `uv run invoke setup`

**Note**: For production, implement proper database migrations using Alembic.

## Testing

See [Testing Guide](testing.md) for comprehensive testing documentation.

Quick test commands:

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_portfolio_overview.py

# Run with verbose output
uv run pytest -v

# Run with print statements visible
uv run pytest -v -s
```

## Adding New Features

### Backend (FastAPI)

1. Add new route in `main.py`:
   ```python
   @app.get("/api/new-endpoint")
   async def new_endpoint():
       # Implementation
       return {"data": "value"}
   ```

2. Add database queries if needed
3. Write tests in `tests/test_api_endpoints.py`

### Frontend

1. Modify `static/index.html`
2. Add JavaScript functions for new features
3. Update UI elements
4. Write Playwright tests in `tests/`

## Debugging

### Server Logs

```bash
# View logs
uv run invoke logs

# Follow logs in real-time
tail -f degiro-portfolio.log
```

### Database Inspection

```bash
# Show database info
uv run invoke db-info

# SQLite command line
sqlite3 degiro-portfolio.db
```

### Development Mode

Run with debug logging:

```python
# In main.py, set debug mode
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

## Release Process

When making a release:

1. Update version in `pyproject.toml`
2. Update documentation
3. Run full test suite
4. Build package: `uv build`
5. Create git tag: `git tag v0.x.x`
6. Push tag: `git push origin v0.x.x`
7. GitHub Actions will automatically publish to PyPI

See [Deployment](deployment.md) for more details.

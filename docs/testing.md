# Testing Guide

## Test Suite Overview

The DEGIRO Portfolio application includes a comprehensive test suite using Pytest and Playwright for end-to-end testing.

## Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── test_portfolio_overview.py    # Portfolio UI tests (17 tests)
├── test_stock_charts.py          # Chart visualization tests (15 tests)
├── test_api_endpoints.py         # API endpoint tests (14 tests)
├── test_interactive_features.py  # User interaction tests (19 tests)
└── README.md                     # Testing documentation
```

## Running Tests

### All Tests

```bash
# Run complete test suite
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with visible output (print statements)
uv run pytest -v -s
```

### Specific Test Files

```bash
# Portfolio overview tests
uv run pytest tests/test_portfolio_overview.py -v

# Stock chart tests
uv run pytest tests/test_stock_charts.py -v

# API endpoint tests
uv run pytest tests/test_api_endpoints.py -v

# Interactive feature tests
uv run pytest tests/test_interactive_features.py -v
```

### Specific Tests

```bash
# Run a specific test by name
uv run pytest tests/test_portfolio_overview.py::test_portfolio_displays_holdings -v

# Run tests matching a pattern
uv run pytest -k "test_stock" -v
```

## Test Categories

### Portfolio Overview Tests (17 tests)

Tests for the main portfolio dashboard:
- Holdings display
- Stock cards
- Price information
- Daily change indicators
- Market data status
- Overall layout and UI

**Example:**
```python
def test_portfolio_displays_holdings(page, test_app):
    """Test that portfolio displays all holdings"""
    page.goto("http://localhost:8001")
    # Verify stock cards are displayed
    assert page.locator(".stock-card").count() > 0
```

### Stock Chart Tests (15 tests)

Tests for chart visualizations:
- Candlestick charts
- Transaction markers
- Position percentage charts
- Investment tranche tracking
- Market index comparison
- Chart interactivity

**Example:**
```python
def test_chart_displays_candlestick_data(page, test_app):
    """Test that clicking a stock displays its chart"""
    page.goto("http://localhost:8001")
    page.locator(".stock-card").first.click()
    # Verify chart is displayed
    assert page.locator("#priceChart").is_visible()
```

### API Endpoint Tests (14 tests)

Tests for all API endpoints:
- Holdings endpoint
- Stock prices endpoint
- Transaction history endpoint
- Chart data endpoint
- Market data endpoints
- Upload functionality
- Error handling

**Example:**
```python
def test_get_holdings(client):
    """Test GET /api/holdings endpoint"""
    response = client.get("/api/holdings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Interactive Feature Tests (19 tests)

Tests for user interactions:
- Chart navigation
- Tab switching
- Market data updates
- File uploads
- Button clicks
- Responsive behavior
- Error handling

**Example:**
```python
def test_update_market_data_button(page, test_app):
    """Test market data update functionality"""
    page.goto("http://localhost:8001")
    page.locator("#update-market-data-btn").click()
    # Verify update feedback
    assert page.locator(".update-status").is_visible()
```

## Test Fixtures

### Application Fixtures

Defined in `conftest.py`:

#### `test_app`
Starts an isolated test server on port 8001 with a separate test database.

```python
@pytest.fixture
def test_app():
    """Start test server with isolated database"""
    # Setup and teardown handled automatically
```

#### `test_db`
Creates and seeds a test database with example data.

```python
@pytest.fixture
def test_db():
    """Create test database with sample data"""
    # Returns database session
```

### Playwright Fixtures

#### `page`
Provides a Playwright page instance for browser automation.

```python
def test_example(page, test_app):
    page.goto("http://localhost:8001")
    # Interact with page
```

#### `client`
Provides an httpx test client for API testing.

```python
def test_api_example(client):
    response = client.get("/api/holdings")
    assert response.status_code == 200
```

## Test Database

Tests use an isolated test database to avoid affecting production data:

- **Test DB**: `test-degiro-portfolio.db`
- **Test Port**: 8001 (production uses 8000)
- **Automatic Cleanup**: Database is deleted after tests

The test database is seeded with example data including:
- Multiple stocks (NVDA, MSFT, META, etc.)
- Transaction history
- Historical prices
- Market indices

## Writing New Tests

### Portfolio UI Test

```python
def test_new_ui_feature(page, test_app):
    """Test description"""
    # Navigate to page
    page.goto("http://localhost:8001")

    # Perform actions
    page.locator("#some-button").click()

    # Assert expectations
    assert page.locator("#result").is_visible()
    assert page.locator("#result").text_content() == "Expected"
```

### API Test

```python
def test_new_api_endpoint(client):
    """Test API endpoint"""
    # Make request
    response = client.get("/api/new-endpoint")

    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

### Interactive Test

```python
def test_user_interaction(page, test_app):
    """Test user interaction"""
    page.goto("http://localhost:8001")

    # Fill form
    page.fill("#input-field", "test value")

    # Submit
    page.click("#submit-button")

    # Wait for result
    page.wait_for_selector("#result", state="visible")

    # Verify
    assert "success" in page.locator("#result").text_content().lower()
```

## Test Best Practices

### 1. Isolation
- Each test should be independent
- Don't rely on test execution order
- Use fixtures for setup and teardown

### 2. Clear Naming
```python
# Good
def test_portfolio_displays_stock_cards():
    pass

# Bad
def test_stuff():
    pass
```

### 3. Arrange-Act-Assert
```python
def test_example(page, test_app):
    # Arrange - setup
    page.goto("http://localhost:8001")

    # Act - perform action
    page.click("#button")

    # Assert - verify result
    assert page.locator("#result").is_visible()
```

### 4. Wait for Elements
```python
# Wait for element to be visible
page.wait_for_selector("#element", state="visible")

# Or use locator assertions
expect(page.locator("#element")).to_be_visible()
```

### 5. Meaningful Assertions
```python
# Good - specific assertion
assert page.locator(".stock-card").count() == 10

# Bad - vague assertion
assert page.locator(".stock-card").count() > 0
```

## Continuous Integration

Tests run automatically on GitHub Actions:
- On every push to main
- On every pull request
- Before publishing releases

See `.github/workflows/ci.yml` for CI configuration.

## Debugging Tests

### Run Single Test with Output
```bash
uv run pytest tests/test_file.py::test_name -v -s
```

### Playwright Inspector
```bash
PWDEBUG=1 uv run pytest tests/test_file.py::test_name
```

### Screenshots on Failure
Playwright automatically captures screenshots on test failures in `test-results/` directory.

### Server Logs
Test server logs are available in `test-degiro-portfolio.log` during test execution.

## Test Coverage

Current test coverage:
- **Portfolio Overview**: 17 tests
- **Stock Charts**: 15 tests
- **API Endpoints**: 14 tests
- **Interactive Features**: 19 tests
- **Total**: 65+ tests

Coverage areas:
- UI rendering and layout
- Data display accuracy
- Chart functionality
- API endpoints
- User interactions
- Error handling
- Edge cases

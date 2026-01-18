"""Unit tests for FastAPI endpoints in main.py."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import os
from pathlib import Path


@pytest.fixture
def client(test_database):
    """Create a test client for the FastAPI app."""
    # Import after test_database fixture to ensure correct DB
    from degiro_portfolio.main import app
    return TestClient(app)


def test_root_endpoint_returns_html(client):
    """Test that root endpoint returns HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert b"DEGIRO Portfolio" in response.content


def test_ping_endpoint(client):
    """Test ping health check endpoint."""
    response = client.get("/api/ping")
    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert data["status"] == "ok"
    assert data["server"] == "DEGIRO Portfolio"
    assert "version" in data
    assert "started" in data
    assert "uptime_seconds" in data
    assert "uptime" in data

    # Check uptime is a positive number
    assert data["uptime_seconds"] >= 0


def test_holdings_endpoint(client):
    """Test holdings API endpoint."""
    response = client.get("/api/holdings")
    assert response.status_code == 200
    data = response.json()
    assert "holdings" in data
    assert isinstance(data["holdings"], list)
    assert len(data["holdings"]) > 0


def test_holdings_structure(client):
    """Test that holdings have correct structure."""
    response = client.get("/api/holdings")
    data = response.json()

    if data["holdings"]:
        holding = data["holdings"][0]
        assert "id" in holding
        assert "name" in holding
        assert "symbol" in holding
        assert "shares" in holding
        assert "transactions_count" in holding


def test_stock_prices_endpoint(client):
    """Test stock prices API endpoint."""
    response = client.get("/api/stock/1/prices")
    assert response.status_code == 200
    data = response.json()
    assert "prices" in data
    assert isinstance(data["prices"], list)


def test_stock_transactions_endpoint(client):
    """Test stock transactions API endpoint."""
    response = client.get("/api/stock/1/transactions")
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)


def test_stock_chart_data_endpoint(client):
    """Test stock chart data API endpoint."""
    response = client.get("/api/stock/1/chart-data")
    assert response.status_code == 200
    data = response.json()

    assert "stock" in data
    assert "prices" in data
    assert "transactions" in data
    assert "indices" in data
    assert "stock_normalized" in data
    assert "position_percentage" in data


def test_stock_chart_data_has_indices(client):
    """Test that chart data includes market indices."""
    response = client.get("/api/stock/1/chart-data")
    data = response.json()

    # Should have indices data
    assert isinstance(data["indices"], list)
    # Indices should be S&P 500 and Euro Stoxx 50
    if data["indices"]:
        index_names = [idx["name"] for idx in data["indices"]]
        assert any("S&P" in name or "500" in name for name in index_names)


def test_invalid_stock_id_returns_404(client):
    """Test that invalid stock ID returns 404."""
    response = client.get("/api/stock/999999/chart-data")
    assert response.status_code == 404


def test_market_data_status_endpoint(client):
    """Test market data status endpoint."""
    response = client.get("/api/market-data-status")
    assert response.status_code == 200
    data = response.json()
    assert "has_data" in data


def test_portfolio_performance_endpoint(client):
    """Test portfolio performance endpoint."""
    response = client.get("/api/portfolio-performance")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    assert isinstance(data["stocks"], list)


def test_portfolio_valuation_history_endpoint(client):
    """Test portfolio valuation history endpoint."""
    response = client.get("/api/portfolio-valuation-history")
    assert response.status_code == 200
    data = response.json()
    assert "dates" in data
    assert "values" in data
    assert "invested" in data
    assert isinstance(data["dates"], list)
    assert isinstance(data["values"], list)
    assert isinstance(data["invested"], list)


def test_update_market_data_endpoint(client):
    """Test update market data endpoint (POST)."""
    response = client.post("/api/update-market-data")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "message" in data


def test_refresh_live_prices_endpoint(client):
    """Test refresh live prices endpoint."""
    response = client.post("/api/refresh-live-prices")
    assert response.status_code == 200
    data = response.json()
    # May not have quotes if no tickers configured, but should return valid JSON
    assert isinstance(data, dict)


def test_ensure_indices_exist_function(mocker):
    """Test the ensure_indices_exist helper function."""
    from degiro_portfolio.main import ensure_indices_exist, INDICES
    from degiro_portfolio.database import SessionLocal, Index, IndexPrice
    import pandas as pd
    from datetime import datetime, timedelta

    # Create mock price data
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    mock_history = pd.DataFrame({
        'Open': [100.0] * 100,
        'High': [101.0] * 100,
        'Low': [99.0] * 100,
        'Close': [100.5] * 100,
        'Volume': [1000000] * 100
    }, index=dates)

    # Mock yfinance Ticker to avoid real API calls
    mock_ticker = mocker.MagicMock()
    mock_ticker.history.return_value = mock_history
    mocker.patch('yfinance.Ticker', return_value=mock_ticker)

    db = SessionLocal()
    try:
        # Clear existing indices for clean test
        db.query(IndexPrice).delete()
        db.query(Index).delete()
        db.commit()

        # Call function
        indices_created, prices_fetched = ensure_indices_exist(db)

        # Should have created indices
        assert indices_created == len(INDICES)

        # Should have fetched prices
        assert prices_fetched > 0

        # Verify indices exist in database
        indices = db.query(Index).all()
        assert len(indices) == len(INDICES)

    finally:
        db.close()


def test_api_cors_headers(client):
    """Test that API responses have proper headers."""
    response = client.get("/api/holdings")
    # Should return JSON
    assert "application/json" in response.headers["content-type"]


def test_static_files_served(client):
    """Test that static files are accessible."""
    # This might fail if static files don't exist, but endpoint should be registered
    response = client.get("/static/favicon.svg")
    # 200 if file exists, 404 if not, but shouldn't be 500
    assert response.status_code in [200, 404]

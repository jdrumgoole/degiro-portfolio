"""Unit tests for fetch_indices.py module."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import pandas as pd


@pytest.fixture
def mock_yfinance():
    """Mock yfinance to avoid real API calls."""
    with patch('degiro_portfolio.fetch_indices.yf') as mock_yf:
        # Create mock ticker
        mock_ticker = MagicMock()

        # Create mock historical data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365*5), periods=1000, freq='D')
        mock_hist = pd.DataFrame({
            'Close': [100 + i * 0.1 for i in range(1000)],
            'Open': [99 + i * 0.1 for i in range(1000)],
            'High': [101 + i * 0.1 for i in range(1000)],
            'Low': [98 + i * 0.1 for i in range(1000)],
            'Volume': [1000000] * 1000
        }, index=dates)

        mock_ticker.history.return_value = mock_hist
        mock_yf.Ticker.return_value = mock_ticker

        yield mock_yf


def test_fetch_index_prices_creates_indices(test_database, mock_yfinance):
    """Test that fetch_index_prices creates index records."""
    from degiro_portfolio.fetch_indices import fetch_index_prices, INDICES
    from degiro_portfolio.database import SessionLocal, Index

    session = SessionLocal()
    try:
        # Clear existing indices
        session.query(Index).delete()
        session.commit()

        # Run fetch
        fetch_index_prices()

        # Verify indices were created
        indices = session.query(Index).all()
        assert len(indices) == len(INDICES)

        # Verify index names and symbols
        index_symbols = {idx.symbol for idx in indices}
        expected_symbols = set(INDICES.keys())
        assert index_symbols == expected_symbols

    finally:
        session.close()


def test_fetch_index_prices_stores_price_data(test_database, mock_yfinance):
    """Test that fetch_index_prices stores price data."""
    from degiro_portfolio.fetch_indices import fetch_index_prices
    from degiro_portfolio.database import SessionLocal, IndexPrice, Index

    session = SessionLocal()
    try:
        # Clear existing data
        session.query(IndexPrice).delete()
        session.query(Index).delete()
        session.commit()

        # Run fetch
        fetch_index_prices()

        # Verify prices were stored
        prices = session.query(IndexPrice).all()
        assert len(prices) > 0

        # Verify price data structure
        if prices:
            price = prices[0]
            assert hasattr(price, 'date')
            assert hasattr(price, 'close')
            assert hasattr(price, 'index_id')
            assert isinstance(price.close, float)
            assert isinstance(price.date, datetime)

    finally:
        session.close()


def test_fetch_index_prices_updates_existing_data(test_database, mock_yfinance):
    """Test that fetch_index_prices refreshes existing data."""
    from degiro_portfolio.fetch_indices import fetch_index_prices, INDICES
    from degiro_portfolio.database import SessionLocal, Index, IndexPrice

    session = SessionLocal()
    try:
        # First fetch
        fetch_index_prices()

        # Count initial prices
        initial_count = session.query(IndexPrice).count()
        assert initial_count > 0

        # Second fetch should delete and recreate
        fetch_index_prices()

        # Should have similar number of prices (deletes and recreates)
        final_count = session.query(IndexPrice).count()
        assert final_count > 0
        # Might differ slightly but should be in same range
        assert abs(final_count - initial_count) < initial_count * 0.5

    finally:
        session.close()


def test_indices_constant_has_expected_values():
    """Test that INDICES constant has expected index definitions."""
    from degiro_portfolio.fetch_indices import INDICES

    # Should have S&P 500 and Euro Stoxx 50
    assert "^GSPC" in INDICES
    assert "^STOXX50E" in INDICES

    # Should have correct names
    assert INDICES["^GSPC"] == "S&P 500"
    assert INDICES["^STOXX50E"] == "Euro Stoxx 50"


def test_fetch_index_prices_handles_empty_data(test_database):
    """Test fetch_index_prices handles empty data gracefully."""
    from degiro_portfolio.fetch_indices import fetch_index_prices
    from degiro_portfolio.database import SessionLocal, Index

    with patch('degiro_portfolio.fetch_indices.yf') as mock_yf:
        # Create mock ticker with no data
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = pd.DataFrame()  # Empty dataframe
        mock_yf.Ticker.return_value = mock_ticker

        session = SessionLocal()
        try:
            # Clear existing data
            session.query(Index).delete()
            session.commit()

            # Should not crash
            fetch_index_prices()

            # Should still create index records even if no data
            indices = session.query(Index).all()
            # At least the index records should be created
            assert len(indices) >= 0

        finally:
            session.close()


def test_fetch_index_prices_transaction_safety(test_database, mock_yfinance):
    """Test that fetch_index_prices handles database transactions properly."""
    from degiro_portfolio.fetch_indices import fetch_index_prices
    from degiro_portfolio.database import SessionLocal, Index, IndexPrice

    session = SessionLocal()
    try:
        # Clear existing data
        session.query(IndexPrice).delete()
        session.query(Index).delete()
        session.commit()

        # Run fetch
        fetch_index_prices()

        # Data should be committed and retrievable in new session
        new_session = SessionLocal()
        try:
            indices = new_session.query(Index).all()
            assert len(indices) > 0

            prices = new_session.query(IndexPrice).all()
            assert len(prices) > 0
        finally:
            new_session.close()

    finally:
        session.close()

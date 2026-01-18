"""Test for database purge functionality.

IMPORTANT: This file is named with 'zzz' prefix to ensure it runs LAST alphabetically.
The purge test is destructive and must run after all other tests that depend on the
test database having data.
"""

import pytest
from playwright.sync_api import Page, BrowserContext


@pytest.fixture
def purge_page(context: BrowserContext, server_process):
    """Page fixture for purge tests - doesn't wait for stock cards.

    After purging, there are no stock cards, so we can't use the standard
    page fixture which waits for .stock-card to appear.
    """
    page = context.new_page()
    page.goto(server_process, timeout=10000)
    # Just wait for the page to be interactive, not for specific content
    page.wait_for_load_state("domcontentloaded", timeout=10000)
    yield page
    page.close()


def test_purge_database_deletes_all_data(purge_page: Page, base_url):
    """Test that the purge database endpoint deletes all data."""
    # First, verify we have data in the database
    holdings_response = purge_page.request.get(f"{base_url}/api/holdings")
    assert holdings_response.ok
    initial_holdings = holdings_response.json()["holdings"]
    initial_stock_count = len(initial_holdings)

    # We should have stocks from the test data
    assert initial_stock_count > 0, "Test database should have stocks before purge"

    # Count initial transactions (sum across all stocks)
    initial_transaction_count = sum(h["transactions_count"] for h in initial_holdings)
    assert initial_transaction_count > 0, "Test database should have transactions before purge"

    # Call the purge endpoint
    purge_response = purge_page.request.post(f"{base_url}/api/purge-database")
    assert purge_response.ok, f"Purge API returned {purge_response.status}"

    purge_result = purge_response.json()

    # Verify the purge was successful
    assert purge_result["success"] is True, "Purge should report success"
    assert "deleted" in purge_result, "Response should include deleted counts"

    deleted = purge_result["deleted"]

    # Verify counts are reported
    assert deleted["stocks"] == initial_stock_count, \
        f"Should report {initial_stock_count} stocks deleted, got {deleted['stocks']}"
    assert deleted["transactions"] == initial_transaction_count, \
        f"Should report {initial_transaction_count} transactions deleted, got {deleted['transactions']}"
    assert deleted["stock_prices"] >= 0, "Should report stock_prices count"
    assert deleted["indices"] >= 0, "Should report indices count"
    assert deleted["index_prices"] >= 0, "Should report index_prices count"

    # Verify all data is actually gone - check holdings endpoint returns empty
    holdings_after_purge = purge_page.request.get(f"{base_url}/api/holdings")
    assert holdings_after_purge.ok
    final_holdings = holdings_after_purge.json()["holdings"]

    assert len(final_holdings) == 0, \
        f"After purge, should have 0 holdings, but got {len(final_holdings)}"


def test_purge_database_handles_already_empty_database(purge_page: Page, base_url):
    """Test that purging an already empty database works without error."""
    # First, purge to ensure the database is empty (works with parallel testing)
    first_purge = purge_page.request.post(f"{base_url}/api/purge-database")
    assert first_purge.ok, "First purge should succeed"

    # Now purge again - this tests the empty database case
    purge_response = purge_page.request.post(f"{base_url}/api/purge-database")
    assert purge_response.ok

    purge_result = purge_response.json()
    assert purge_result["success"] is True

    # All counts should be 0 since database was already empty
    deleted = purge_result["deleted"]
    assert deleted["stocks"] == 0
    assert deleted["transactions"] == 0
    assert deleted["stock_prices"] == 0

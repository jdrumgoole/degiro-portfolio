"""Pytest configuration and fixtures for DEGIRO Portfolio tests.

Supports parallel test execution with pytest-xdist:
- A master test database is created once with all example data and mock market data
- Each worker copies this master database to get isolated, pre-populated data
- Each worker gets its own server port (8001 + worker_num)
- No API calls during parallel tests - all data is pre-loaded
"""

import os
import shutil
import subprocess
import time
import signal
import filelock
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page


# Test configuration - isolated from production
TEST_PORT_BASE = 8001  # Base port, workers use 8001 + worker_num
TEST_HOST = "127.0.0.1"
TEST_DB_DIR = Path(__file__).parent / ".test_data"
MASTER_DB_PATH = TEST_DB_DIR / "master_test_portfolio.db"
MASTER_DB_LOCK = TEST_DB_DIR / "master_test_portfolio.lock"
EXAMPLE_DATA = "example_data.xlsx"


def get_worker_id(config_or_request):
    """Get xdist worker ID or 'main' for single-process runs."""
    # Handle both config and request objects
    if hasattr(config_or_request, 'workerinput'):
        return config_or_request.workerinput.get("workerid", "main")
    if hasattr(config_or_request, 'config') and hasattr(config_or_request.config, 'workerinput'):
        return config_or_request.config.workerinput.get("workerid", "main")
    return "main"


def get_worker_port(worker_id):
    """Get unique port for worker. main=8001, gw0=8001, gw1=8002, etc."""
    if worker_id == "main":
        return TEST_PORT_BASE
    try:
        worker_num = int(worker_id.replace("gw", ""))
        return TEST_PORT_BASE + worker_num
    except ValueError:
        return TEST_PORT_BASE


def get_worker_db_path(worker_id):
    """Get unique database path for worker."""
    if worker_id == "main":
        return TEST_DB_DIR / "test_portfolio.db"
    return TEST_DB_DIR / f"test_portfolio_{worker_id}.db"


def create_master_test_database():
    """Create the master test database with example data and mock market data.

    This is called once before any workers start. The database is then copied
    for each worker to provide isolated, pre-populated test data.
    """
    # Set up environment for master database
    os.environ["DATABASE_URL"] = f"sqlite:///{MASTER_DB_PATH.absolute()}"

    # Reinitialize database engine
    from degiro_portfolio.database import reinitialize_engine
    reinitialize_engine()

    print(f"\n📦 Creating master test database: {MASTER_DB_PATH}")

    # Import the example data
    from degiro_portfolio.import_data import import_transactions
    import_transactions(EXAMPLE_DATA)

    # Add mock price data for tests (avoid API calls during testing)
    from degiro_portfolio.database import Stock, StockPrice, Index, IndexPrice, SessionLocal
    from datetime import datetime, timedelta

    db = SessionLocal()
    try:
        # Get all stocks
        stocks = db.query(Stock).all()

        # Generate mock price data for the last 180 days
        base_date = datetime.now() - timedelta(days=180)

        for stock in stocks:
            # Create mock prices with some variation
            base_price = 100.0  # Starting price
            for day in range(180):
                current_date = base_date + timedelta(days=day)
                # Add some variation to make realistic-looking data
                variation = (day % 10) - 5  # -5 to +5
                price = base_price + variation

                price_record = StockPrice(
                    stock_id=stock.id,
                    date=current_date,
                    open=price - 0.5,
                    high=price + 1.0,
                    low=price - 1.0,
                    close=price,
                    volume=1000000,
                    currency=stock.currency
                )
                db.add(price_record)

        # Add mock index data
        indices_data = [
            Index(symbol="^GSPC", name="S&P 500"),
            Index(symbol="^STOXX50E", name="Euro Stoxx 50")
        ]
        for index in indices_data:
            existing = db.query(Index).filter_by(symbol=index.symbol).first()
            if not existing:
                db.add(index)

        db.commit()

        # Add mock index prices
        for index in db.query(Index).all():
            base_index_price = 4000.0
            for day in range(180):
                current_date = base_date + timedelta(days=day)
                variation = (day % 10) - 5
                price = base_index_price + variation * 10

                index_price = IndexPrice(
                    index_id=index.id,
                    date=current_date,
                    close=price
                )
                db.add(index_price)

        db.commit()
        print(f"✅ Master test database created with mock price data")
    finally:
        db.close()


def pytest_configure(config):
    """Set up test database path before any tests run.

    This hook runs early in pytest startup, before test collection.
    For parallel runs, uses a file lock to ensure only one process creates
    the master database, then each worker copies it.
    """
    # Create test data directory
    TEST_DB_DIR.mkdir(exist_ok=True)

    # Get worker ID for xdist parallel runs
    worker_id = get_worker_id(config)
    test_db_path = get_worker_db_path(worker_id)

    # Use a file lock to ensure only one process creates the master database
    with filelock.FileLock(str(MASTER_DB_LOCK), timeout=120):
        if not MASTER_DB_PATH.exists():
            # First process creates the master database
            create_master_test_database()

    # Copy master database to worker-specific path
    if test_db_path.exists():
        test_db_path.unlink()
    shutil.copy(MASTER_DB_PATH, test_db_path)
    print(f"📋 Copied master database to {test_db_path} (worker: {worker_id})")

    # Set the DATABASE_URL environment variable for this worker
    test_db_absolute = str(test_db_path.absolute())
    os.environ["DATABASE_URL"] = f"sqlite:///{test_db_absolute}"

    # Store the path for later use
    config._test_db_path = test_db_path
    config._test_worker_id = worker_id


@pytest.fixture(scope="session", autouse=True)
def test_environment(request):
    """Set up isolated test environment before any tests run.

    The database is already created and copied in pytest_configure.
    This fixture just handles cleanup.
    """
    worker_id = get_worker_id(request)
    test_db_path = get_worker_db_path(worker_id)

    # Save original environment variables
    original_env = {
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "PORT": os.environ.get("PORT"),
    }

    yield

    # Restore original environment variables
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    # Clean up test database for this worker
    if test_db_path.exists():
        test_db_path.unlink()

    # Remove test data directory if empty (ignore errors)
    try:
        # Only try to remove master DB and lock if we're the last worker
        # This is a best-effort cleanup
        for f in [MASTER_DB_PATH, MASTER_DB_LOCK]:
            if f.exists():
                f.unlink()
        TEST_DB_DIR.rmdir()
    except OSError:
        pass  # Directory not empty or doesn't exist


@pytest.fixture(scope="session")
def test_database(request):
    """Provide the test database path.

    The database is already created and copied in pytest_configure.
    This fixture just reinitializes the engine and returns the path.
    """
    worker_id = get_worker_id(request)
    test_db_path = get_worker_db_path(worker_id)
    test_db_absolute = str(test_db_path.absolute())

    # Ensure DATABASE_URL is set correctly for this worker
    os.environ["DATABASE_URL"] = f"sqlite:///{test_db_absolute}"

    # Reinitialize database engine to use the copied test database
    from degiro_portfolio.database import reinitialize_engine
    reinitialize_engine()

    print(f"\n✅ Using test database: {test_db_absolute} (worker: {worker_id})")

    yield test_db_absolute


@pytest.fixture(scope="session")
def server_process(test_database, request):
    """Start dedicated FastAPI test server on isolated port."""
    worker_id = get_worker_id(request)
    test_port = get_worker_port(worker_id)

    # Ensure test server uses test database
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{test_database}"
    env["PORT"] = str(test_port)

    # Check if port is already in use
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((TEST_HOST, test_port))
    sock.close()

    if result == 0:
        raise Exception(
            f"Port {test_port} is already in use. Please stop any services using this port.\n"
            f"Run: lsof -ti:{test_port} | xargs kill -9"
        )

    print(f"\n🚀 Starting test server on {TEST_HOST}:{test_port} (worker: {worker_id})")

    # Start the server in a subprocess
    process = subprocess.Popen(
        [
            "uv", "run", "uvicorn",
            "degiro_portfolio.main:app",
            "--host", TEST_HOST,
            "--port", str(test_port),
            "--log-level", "warning"  # Reduce log noise during tests
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid  # Create new process group for clean shutdown
    )

    # Wait for server to be ready (reduced wait time)
    import httpx
    test_url = f"http://{TEST_HOST}:{test_port}"
    max_retries = 20  # Reduced from 30

    for i in range(max_retries):
        try:
            response = httpx.get(f"{test_url}/api/ping", timeout=0.5)  # Use ping endpoint, shorter timeout
            if response.status_code == 200:
                print(f"✅ Test server ready at {test_url}")
                break
        except (httpx.ConnectError, httpx.ReadTimeout):
            if i == max_retries - 1:
                # Kill the process group
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                raise Exception(f"Test server failed to start on port {test_port}")
            time.sleep(0.25)  # Reduced from 0.5

    yield test_url

    # Cleanup: Kill the process group to ensure all subprocesses are terminated
    print(f"\n🛑 Shutting down test server")
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        # Force kill if graceful shutdown fails
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass

    # Ensure port is freed
    time.sleep(0.5)


@pytest.fixture(scope="session")
def browser(playwright):
    """Create a browser instance for the test session."""
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="module")
def context(browser: Browser):
    """Create a browser context shared across tests in a module."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US"
    )
    yield context
    context.close()


@pytest.fixture(scope="session")
def base_url(server_process):
    """Provide the base URL for API calls."""
    return server_process


@pytest.fixture(scope="module")
def shared_page(context: BrowserContext, server_process):
    """Create a page shared across tests in a module (for read-only tests)."""
    page = context.new_page()
    page.goto(server_process, timeout=10000)  # 10 seconds
    yield page
    page.close()


@pytest.fixture
def page(shared_page, server_process):
    """Provide page for each test, navigating back to home to reset state."""
    # Navigate back to home page to reset state between tests
    shared_page.goto(server_process, timeout=10000)  # 10 seconds
    # Wait for page to be fully loaded (holdings to appear)
    shared_page.wait_for_selector(".stock-card", timeout=8000)  # 8 seconds
    yield shared_page


@pytest.fixture
def expected_stocks():
    """Expected stock data from example_data.xlsx."""
    return {
        "NVIDIA CORP": {
            "shares": 129,
            "transactions": 4,
            "currency": "USD",
            "ticker": "NVDA"
        },
        "MICROSOFT CORP": {
            "shares": 30,
            "transactions": 3,
            "currency": "USD",
            "ticker": "MSFT"
        },
        "META PLATFORMS INC": {
            "shares": 68,
            "transactions": 2,
            "currency": "USD",
            "ticker": "META"
        },
        "ALPHABET INC-CL A": {
            "shares": 57,
            "transactions": 2,
            "currency": "USD",
            "ticker": "GOOGL"
        },
        "ADVANCED MICRO DEVICES": {
            "shares": 97,
            "transactions": 3,
            "currency": "USD",
            "ticker": "AMD"
        },
        "ASML HOLDING NV": {
            "shares": 33,
            "transactions": 3,
            "currency": "EUR",
            "ticker": "ASML.AS"
        },
        "SAP SE": {
            "shares": 75,
            "transactions": 2,
            "currency": "EUR",
            "ticker": "SAP.DE"
        },
        "INFINEON TECHNOLOGIES AG": {
            "shares": 400,
            "transactions": 3,
            "currency": "EUR",
            "ticker": "IFX.DE"
        },
        "NOKIA OYJ": {
            "shares": 900,
            "transactions": 2,
            "currency": "EUR",
            "ticker": "NOKIA.HE"
        },
        "TELEFONAKTIEBOLAGET LM ERICSSON-B": {
            "shares": 1400,
            "transactions": 2,
            "currency": "SEK",
            "ticker": "ERIC-B.ST"
        },
        "STMICROELECTRONICS NV": {
            "shares": 240,
            "transactions": 2,
            "currency": "EUR",
            "ticker": "STM.PA"
        }
    }

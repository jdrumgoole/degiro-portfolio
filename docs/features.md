# Features

## Portfolio Management

### Transaction Import

- **Excel Import**: Import DEGIRO transaction exports directly from Excel
- **Web Upload**: Upload new transaction files through the web interface
- **Multi-currency Support**: Handles EUR, USD, and SEK with automatic conversion
- **Automatic Processing**: Automatically creates stock records and links transactions

### Price Data Management

- **Historical Prices**: Fetches complete historical OHLCV data from Yahoo Finance
- **One-click Updates**: Update all stock prices with a single button click
- **Market Indices**: Track S&P 500 and Euro Stoxx 50 for performance comparison
- **Efficient Storage**: SQLite database for fast data retrieval

## Portfolio Overview

The main dashboard provides:

### Stock Cards

Each stock displays:
- Company name and ticker symbol
- Current share count
- Latest closing price
- Daily percentage change (▲ increase / ▼ decrease)
- Exchange information
- Transaction count

### Market Data Status

- Shows the most recent price update date
- Helps you know when data was last refreshed

### Interactive Elements

- **Clickable Tickers**: Links to Google Finance for quick reference
- **Company Names**: Links to Google search for investor relations
- **Compact Design**: Space-efficient layout showing all key information

## Interactive Charts

### Price Charts

**Candlestick Charts**:
- Open, High, Low, Close data visualization
- Transaction markers showing buy/sell points
- Zoom and pan capabilities
- Hover for detailed information

### Position Value Charts

**Position Percentage View**:
- Shows position value as percentage (100% = break-even)
- Helps visualize profit/loss over time
- Transaction markers indicate purchase points

### Investment Tranche Tracking

**Individual Purchase Performance**:
- Tracks each purchase separately
- Shows performance of individual tranches
- Helps understand which purchases are profitable

### Market Comparison

**Index Comparison Charts**:
- Compare stock performance to S&P 500
- Compare to Euro Stoxx 50
- Normalized charts for fair comparison

## Data Management

### Database Operations

```bash
# Show database information
uv run invoke db-info

# View server logs
uv run invoke logs

# Purge all data
uv run invoke purge-data

# Clean generated files
uv run invoke clean
```

### Update Operations

- **Fetch Prices**: Update historical price data
- **Fetch Indices**: Update market index data
- **Re-import**: Re-import transactions from updated Excel files

## Multi-Currency Support

The application handles multiple currencies:

- **EUR**: Euro
- **USD**: US Dollar
- **SEK**: Swedish Krona

Price charts automatically display in the transaction currency, ensuring accurate visualization.

## API Features

The application exposes a RESTful API for:

- Fetching portfolio holdings
- Retrieving stock prices and transactions
- Getting chart data
- Uploading transaction files
- Updating market data

See [API Reference](api-reference.md) for complete endpoint documentation.

## Performance Metrics

Track key portfolio metrics:

- Total portfolio value
- Total gain/loss
- Individual stock performance
- Position-level profit/loss
- Market-relative performance

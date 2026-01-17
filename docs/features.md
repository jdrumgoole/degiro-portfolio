# Features

This page explains everything the application can do for you.

## Managing Your Portfolio

### Importing Your Transactions

**What it does**: Takes your DEGIRO transaction history and imports it into the application.

✅ **Drag and Drop Upload** - Click the upload button, select your Excel file from DEGIRO, done!
✅ **Automatic Stock Detection** - The app automatically recognizes all your stocks
✅ **Multi-Currency Support** - Works with EUR, USD, SEK, GBP and automatically converts to EUR
✅ **Smart Processing** - Links all your buy/sell transactions together for each stock

**How to use**: Click "📤 Upload Transactions" in the web interface, select your DEGIRO Excel export.

### Getting Price Data

**What it does**: Downloads historical stock prices so you can see charts and track performance.

✅ **Automatic Download** - Prices download automatically when you upload transactions
✅ **One-Click Updates** - Click "📈 Update Market Data" to refresh all prices
✅ **Market Benchmarks** - Also downloads S&P 500 and Euro Stoxx 50 for comparison
✅ **Fast Access** - All data stored on your computer for instant viewing

**How to use**: Prices update automatically on upload. Click "Update Market Data" anytime to refresh.

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

## Understanding the Charts

When you click on any stock card, you'll see four interactive charts:

### 1. Price Chart (Candlestick Chart)

**What it shows**: Historical stock price movements.

**What you see**:
- Green/red bars (candlesticks) show daily price ranges
- Green = price went up that day
- Red = price went down that day
- Green markers = when you bought shares
- Red markers = when you sold shares

**What you can do**:
- Zoom in/out with mouse wheel or pinch
- Pan left/right by dragging
- Hover over any point to see exact prices and dates

**Why it's useful**: See how the stock price has moved over time and when you made your purchases.

### 2. Position Value % Chart

**What it shows**: Whether you're making money or losing money on this stock.

**How to read it**:
- Line above 100% = You're profitable (making money)
- Line below 100% = You're at a loss (losing money)
- Line at exactly 100% = Break-even (no profit, no loss)

**Example**: If the line is at 120%, your position is worth 20% more than what you paid for it.

**Why it's useful**: Instantly see if you're up or down on your investment.

### 3. Investment Tranches Chart

**What it shows**: Performance of each individual purchase separately.

**What it does**:
- If you bought a stock multiple times at different prices, this tracks each purchase separately
- Shows which purchases are profitable and which aren't
- Helps you understand your average cost

**Why it's useful**: Some of your purchases might be profitable while others are at a loss - this chart shows you which is which.

### 4. Market Comparison Chart

**What it shows**: How your stock compares to the overall market.

**What you see**:
- Your stock's performance (line)
- S&P 500 performance (US market index)
- Euro Stoxx 50 performance (European market index)

**How to read it**:
- If your stock line is higher = Beating the market (doing better)
- If your stock line is lower = Underperforming the market (doing worse)

**Why it's useful**: Helps you understand if your stock is actually performing well or if the whole market is just going up/down.

## Managing Your Data

### Clearing All Data

**What it does**: Removes all your transactions and price data if you want to start fresh.

**How to use**:
1. Scroll to the bottom of the dashboard
2. Click the red "⚠️ Delete All Data" button
3. Confirm the deletion

**Warning**: This permanently deletes everything! You'll need to re-upload your transactions.

**When to use it**:
- You want to start over from scratch
- You uploaded the wrong file and want to clean up
- You're testing the application with demo data

### Viewing Information

**Command-line tools** (optional, for advanced users):

```bash
# See how many stocks and transactions you have
uv run invoke db-info

# View what the server is doing (useful for troubleshooting)
uv run invoke logs
```

## Multi-Currency Support

**What it does**: The app works with stocks in different currencies and converts everything to EUR for easy comparison.

**Supported currencies**:
- 🇪🇺 EUR (Euro)
- 🇺🇸 USD (US Dollar)
- 🇸🇪 SEK (Swedish Krona)
- 🇬🇧 GBP (British Pound)

**How it works**:
- Stock prices display in their original currency
- Position values automatically convert to EUR
- Exchange rates update daily
- Charts show prices in the currency you bought/sold in

**Example**: If you own US stocks (priced in USD) and European stocks (priced in EUR), the app shows your total portfolio value in EUR so you can easily compare them.

## What You Can Track

The application shows you:

### Portfolio Level
✅ **Total Portfolio Value** - Sum of all your investments in EUR
✅ **Overall Gain/Loss** - How much money you've made or lost overall
✅ **Number of Holdings** - How many different stocks you own

### Individual Stock Level
✅ **Current Value** - What your shares are worth now
✅ **Purchase Price** - What you originally paid
✅ **Profit/Loss** - Difference between current value and what you paid
✅ **Percentage Return** - Your profit/loss as a percentage
✅ **Daily Change** - How much the stock moved today
✅ **Share Count** - Number of shares you own

### Performance Tracking
✅ **Historical Performance** - How your stocks have performed over time
✅ **Market Comparison** - How you're doing vs S&P 500 and Euro Stoxx 50
✅ **Transaction History** - All your buy/sell transactions with dates and prices
✅ **Tranche Performance** - Performance of each individual purchase

## Additional Features

### Quick Links
- Click any **company name** to search Google for investor relations info
- Click any **ticker symbol** to view the stock on Google Finance
- Click "Update Market Data" to refresh all prices instantly

### Data Privacy
- All data stored locally on your computer
- No account required
- No data sent to external servers (except to download stock prices)

### Technical Features (for developers)
- RESTful API for programmatic access
- SQLite database for data storage
- Complete API documentation available in [API Reference](api-reference.md)

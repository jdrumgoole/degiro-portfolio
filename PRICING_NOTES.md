# Pricing Data Notes

## Why Portfolio Values May Differ from DEGIRO

You may notice that the portfolio value shown in this application differs from what DEGIRO shows. This is **normal and expected** for the following reasons:

### 1. **Timing Difference**
- **DEGIRO**: Shows real-time intraday prices (current market price)
- **This App**: Shows end-of-day closing prices (previous trading day)
- **Impact**: 1-3 day delay in price updates

**Example:**
- DEGIRO (Jan 12, 10:00 AM): EUR 168,692 (live prices)
- This App (Jan 12, 10:00 AM): EUR 217,626 (using Jan 9 closing prices)

### 2. **Price Volatility**
Your portfolio contains volatile defense/aerospace stocks:
- Rheinmetall AG
- SAAB AB
- Leonardo SPA
- Airbus Group

These stocks can move 5-10% in a single day, causing large swings in portfolio value.

### 3. **Price Type Differences**
- **DEGIRO**: May show mid-price (between bid/ask)
- **Yahoo Finance**: Shows closing price (last trade of the day)
- **Impact**: Small differences even on the same date

### 4. **Currency Conversion**
For USD-denominated stocks (AERCAP):
- **DEGIRO**: Uses real-time EUR/USD exchange rate
- **This App**: Uses historical rates from your transactions (avg: 1.0781 USD/EUR)
- **Impact**: Can cause differences in EUR-equivalent values

## What's Normal?

**Normal differences:**
- ✅ 1-3 day lag in prices (we show yesterday's close)
- ✅ Small differences (1-5%) due to timing and price type
- ✅ Different values between updates

**Concerning differences:**
- ❌ More than 10% difference for the same date
- ❌ Wrong stock quantities
- ❌ Missing stocks or transactions

## How to Minimize Differences

### Option 1: Update Prices Regularly (Recommended)

Click the **"📈 Update Market Data"** button daily to get the latest closing prices:

```bash
# Or via CLI
uv run invoke fetch-prices
```

### Option 2: Accept End-of-Day Prices

For long-term portfolio tracking, end-of-day prices are perfectly adequate. You don't need real-time data to track your portfolio performance over weeks and months.

### Option 3: Upgrade to Paid API (Not Recommended)

Paid APIs (Alpha Vantage, Twelve Data Pro, etc.) offer real-time or near-real-time data, but:
- ❌ Cost $9-50/month
- ❌ May still not match DEGIRO exactly (different data sources)
- ❌ Overkill for portfolio tracking

## Data Provider: Yahoo Finance

This application uses **Yahoo Finance** as the default data provider because:

✅ **Best for European stocks**
- Full coverage of Stockholm, Frankfurt, Milan, Paris, Amsterdam exchanges
- All your defense/aerospace stocks available
- No API key required

✅ **Free and reliable**
- No rate limits
- Good historical data
- Widely used and tested

⚠️ **Limitations**
- End-of-day prices only (no intraday)
- Unofficial API (web scraping)
- Occasional missing data or errors

### Alternative: Twelve Data

The application also supports **Twelve Data API**, but:
- ❌ Free tier has limited European stock coverage
- ❌ Your stocks (SAAB, Rheinmetall, Leonardo) not available
- ✅ Excellent for US stocks
- ✅ Real-time data (paid tiers)

To use Twelve Data (if you upgrade to paid tier):
```bash
export PRICE_DATA_PROVIDER=twelvedata
export TWELVEDATA_API_KEY=your_key
```

See **TWELVEDATA_SETUP.md** for details.

## Expected Behavior

### Scenario: Fresh Upload

1. **Upload transactions** - Prices fetched automatically
2. **View portfolio** - Shows values using latest available closing prices
3. **Compare to DEGIRO** - May differ due to timing (see above)
4. **Next day** - Click "Update Market Data" to refresh

### Scenario: Daily Tracking

1. **Morning** - Your portfolio shows yesterday's closing prices
2. **DEGIRO** - Shows real-time prices (different values)
3. **Evening** - Click "Update Market Data"
4. **Result** - Portfolio updates to today's closing prices
5. **Tomorrow morning** - Values closer to DEGIRO's current prices

## Understanding Your Portfolio

### What This App Shows

✅ **Long-term performance** - How your investments have grown over time
✅ **Gains/losses** - Realized and unrealized returns
✅ **Holdings tracking** - Current positions and quantities
✅ **Transaction history** - Complete audit trail
✅ **Market comparison** - Performance vs S&P 500, Euro Stoxx 50

### What DEGIRO Shows

✅ **Real-time value** - Current market value right now
✅ **Intraday movements** - Live price changes
✅ **Trading capabilities** - Buy/sell with current quotes

## Recommendation

**Use this app for:**
- Tracking long-term performance
- Analyzing historical returns
- Comparing to market indices
- Portfolio visualization

**Use DEGIRO for:**
- Real-time values
- Trading decisions
- Current day's performance

**Both together:** Get the complete picture of your investment performance!

## Still Concerned?

If you see persistent large discrepancies (>10% for the same date), please check:

1. **Stock quantities match** - Compare holdings in app vs DEGIRO
2. **All stocks imported** - Some stocks may be missing
3. **Price dates** - Check when prices were last updated
4. **Currency settings** - Ensure stocks have correct native currency

If issues persist, create a GitHub issue with:
- Screenshots from both app and DEGIRO
- Date of comparison
- List of expected vs actual holdings

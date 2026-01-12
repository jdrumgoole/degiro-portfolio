# Twelve Data Setup Guide

## Why Twelve Data?

Twelve Data provides **more accurate and up-to-date** pricing for European stocks compared to Yahoo Finance.

**Benefits:**
- ✅ **Real-time data** for European exchanges (Amsterdam, Paris, Frankfurt, Milan, Stockholm)
- ✅ **Better accuracy** - Direct exchange feeds
- ✅ **More reliable** - Official API, not web scraping
- ✅ **Free tier** - 8 API calls/minute, 800/day (enough for daily portfolio updates)
- ✅ **Better for your portfolio** - European defense/aerospace stocks covered

## Getting Your Free API Key

### Step 1: Sign Up

1. Go to https://twelvedata.com/
2. Click **"Get Free API Key"** or **"Sign Up"**
3. Fill in your email and create an account
4. **Verify your email** (check your inbox)

### Step 2: Get Your API Key

1. Log in to your Twelve Data dashboard
2. Go to **"API Key"** section (usually in the left sidebar)
3. **Copy your API key** (it looks like: `abcd1234efgh5678ijkl9012mnop3456`)

### Step 3: Configure DEGIRO Portfolio

You have two options:

#### Option A: Environment Variable (Recommended)

```bash
# Linux/Mac - Add to ~/.bashrc or ~/.zshrc
export TWELVEDATA_API_KEY="your_api_key_here"

# Or set it temporarily for this session
export TWELVEDATA_API_KEY="your_api_key_here"
export PRICE_DATA_PROVIDER="twelvedata"
```

```cmd
REM Windows CMD
set TWELVEDATA_API_KEY=your_api_key_here
set PRICE_DATA_PROVIDER=twelvedata
```

```powershell
# Windows PowerShell
$env:TWELVEDATA_API_KEY="your_api_key_here"
$env:PRICE_DATA_PROVIDER="twelvedata"
```

#### Option B: Create .env File

Create a file named `.env` in your project root:

```bash
# .env file
TWELVEDATA_API_KEY=your_api_key_here
PRICE_DATA_PROVIDER=twelvedata
```

## Using Twelve Data

### Test Your Setup

```bash
# Test that it works
uv run python -c "
from src.degiro_portfolio.config import Config
from src.degiro_portfolio.price_fetchers import get_price_fetcher

print(f'Provider: {Config.PRICE_DATA_PROVIDER}')
print(f'API Key configured: {\"Yes\" if Config.TWELVEDATA_API_KEY else \"No\"}')

if Config.PRICE_DATA_PROVIDER == 'twelvedata':
    fetcher = get_price_fetcher()
    print('✅ Twelve Data fetcher created successfully!')
"
```

### Fetch Prices

Once configured, all price fetching will automatically use Twelve Data:

```bash
# Purge old Yahoo Finance data
uv run invoke purge-data

# Upload your transactions (will fetch with Twelve Data)
# Or use CLI:
uv run invoke import-data

# Fetch prices (will use Twelve Data)
uv run invoke fetch-prices

# Start server
uv run invoke start
```

## Free Tier Limits

**Twelve Data Free Tier:**
- ✅ 8 API calls per minute
- ✅ 800 API calls per day
- ✅ No credit card required

**Typical usage:**
- 6 stocks in your portfolio = 6 API calls
- Daily update = 6 calls
- Well within free limits!

**If you exceed limits:**
- You'll get an error message
- Wait a minute and try again
- Or upgrade to paid plan ($9/month for 30 calls/min)

## Switching Between Providers

### Use Twelve Data

```bash
export PRICE_DATA_PROVIDER="twelvedata"
uv run invoke restart
```

### Switch Back to Yahoo Finance

```bash
export PRICE_DATA_PROVIDER="yahoo"
uv run invoke restart
```

## Troubleshooting

### "API key required"

**Problem:** You see an error about missing API key.

**Solution:**
1. Make sure you set `TWELVEDATA_API_KEY` environment variable
2. Restart your terminal/shell
3. Verify with: `echo $TWELVEDATA_API_KEY` (Linux/Mac) or `echo %TWELVEDATA_API_KEY%` (Windows)

### "No data available"

**Problem:** Twelve Data returns no data for a stock.

**Solution:**
1. Check the ticker symbol is correct for Twelve Data
2. Some European stocks need exchange suffix (e.g., `SAAB-B.ST` for Stockholm)
3. Verify the stock is available on Twelve Data website

### "Rate limit exceeded"

**Problem:** Too many API calls in a short time.

**Solution:**
1. Wait 1 minute and try again
2. Fetch prices less frequently (once per day is usually enough)
3. Consider upgrading to paid plan if you need more calls

## Ticker Symbols for Twelve Data

Most European stocks work with the same symbols:

- **Stockholm**: `SAAB-B.ST`
- **Milan**: `LDO.MI`
- **Paris**: `AIR.PA`
- **Frankfurt**: `RHM.DE`
- **Amsterdam**: `ASML.AS` or `ASML`
- **NYSE**: `AER`

The application already has these configured in `ticker_resolver.py`.

## Comparison

| Feature | Yahoo Finance | Twelve Data |
|---------|--------------|-------------|
| **Cost** | Free | Free (800/day) |
| **European stocks** | Fair | Excellent |
| **Real-time** | No | Yes |
| **Accuracy** | Good | Excellent |
| **Reliability** | Fair (web scraping) | Excellent (official API) |
| **Your portfolio** | 29% off | **Accurate** |
| **Setup** | None needed | API key required |

## Recommendation

**For your European defense/aerospace portfolio, use Twelve Data.** The free tier is more than enough for daily updates, and the accuracy is significantly better than Yahoo Finance.

## Support

- Twelve Data documentation: https://twelvedata.com/docs
- Get help: https://twelvedata.com/support
- DEGIRO Portfolio issues: Create issue on GitHub

# API Reference

## Overview

The DEGIRO Portfolio application provides a RESTful API built with FastAPI. All endpoints return JSON data unless otherwise specified.

Base URL: `http://localhost:8000`

## Endpoints

### Portfolio Endpoints

#### GET /api/holdings

Get all current stock holdings with latest prices.

**Response:**
```json
[
  {
    "id": 1,
    "name": "NVIDIA Corporation",
    "symbol": "NVDA",
    "isin": "US67066G1040",
    "currency": "USD",
    "total_quantity": 129.0,
    "latest_price": 140.15,
    "daily_change_percent": 2.34,
    "transaction_count": 4
  }
]
```

#### GET /api/portfolio-performance

Get portfolio-wide performance metrics.

**Response:**
```json
{
  "total_value": 125000.50,
  "total_cost": 100000.00,
  "total_gain_loss": 25000.50,
  "gain_loss_percent": 25.0
}
```

### Stock Endpoints

#### GET /api/stock/{stock_id}/prices

Get historical price data for a specific stock.

**Parameters:**
- `stock_id` (path): Stock ID

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "open": 138.50,
    "high": 141.20,
    "low": 137.80,
    "close": 140.15,
    "volume": 45234567
  }
]
```

#### GET /api/stock/{stock_id}/transactions

Get transaction history for a specific stock.

**Parameters:**
- `stock_id` (path): Stock ID

**Response:**
```json
[
  {
    "id": 1,
    "date": "2024-01-15",
    "quantity": 50.0,
    "price": 135.00,
    "fees": 2.50,
    "transaction_type": "Buy",
    "currency": "USD"
  }
]
```

#### GET /api/stock/{stock_id}/chart-data

Get combined data for chart visualization.

**Parameters:**
- `stock_id` (path): Stock ID

**Response:**
```json
{
  "prices": [...],
  "transactions": [...],
  "position_percentage": [...],
  "tranches": [...]
}
```

### Market Data Endpoints

#### GET /api/market-data-status

Get the most recent market data update timestamp.

**Response:**
```json
{
  "last_update": "2024-01-15T16:00:00",
  "status": "up_to_date"
}
```

#### POST /api/update-market-data

Fetch latest market data for all stocks and indices.

**Request:** No body required

**Response:**
```json
{
  "status": "success",
  "stocks_updated": 10,
  "indices_updated": 2
}
```

### Upload Endpoints

#### POST /api/upload-transactions

Upload a new transaction Excel file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with file field

**Response:**
```json
{
  "status": "success",
  "stocks_imported": 5,
  "transactions_imported": 23
}
```

### Index Endpoints

#### GET /api/indices

Get all market indices.

**Response:**
```json
[
  {
    "id": 1,
    "symbol": "^GSPC",
    "name": "S&P 500"
  },
  {
    "id": 2,
    "symbol": "^STOXX50E",
    "name": "Euro Stoxx 50"
  }
]
```

#### GET /api/index/{index_id}/prices

Get historical price data for a market index.

**Parameters:**
- `index_id` (path): Index ID

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "close": 4850.25
  }
]
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200 OK`: Success
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Python Client Example

```python
import httpx

# Get all holdings
response = httpx.get("http://localhost:8000/api/holdings")
holdings = response.json()

# Get stock prices
stock_id = 1
response = httpx.get(f"http://localhost:8000/api/stock/{stock_id}/prices")
prices = response.json()

# Update market data
response = httpx.post("http://localhost:8000/api/update-market-data")
result = response.json()
```

## Rate Limiting

Currently, there are no rate limits on the API. However, be mindful of:

- Yahoo Finance rate limits when fetching prices
- Database performance with large datasets
- Concurrent request handling

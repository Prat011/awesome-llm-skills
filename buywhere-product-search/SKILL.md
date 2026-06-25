---
name: buywhere-product-search
description: Search and compare products across 11M+ items in Shopee, Lazada, Amazon, Walmart, and 20+ retailers in Singapore, SEA, and US. Use when the user asks about product prices, availability, comparisons, deals, or wants to find the best price for a specific item.
---

# BuyWhere Product Search

Real-time product search and price comparison across Southeast Asia and the US. Use the BuyWhere MCP server to query 11M+ products with structured filters, get normalized prices, compare across merchants, and find the cheapest in-stock listing.

## When to Use This Skill

- User asks "What's the best price for X?" or "Find me a MacBook Air M4 under S$2000"
- User wants to compare products across retailers
- User asks about current deals or discounts
- User wants product details (specs, brand, availability)
- User wants alternatives or similar products
- Cross-border shopping between Singapore, SEA, and the US

## What This Skill Does

1. **search_products**: Full-text search across 11M+ products with merchant/region/price-range/in-stock filters
2. **get_product**: Fetch canonical product details (title, brand, specs, current price, stock, merchant, URL)
3. **compare_products**: Side-by-side comparison of multiple products across merchants
4. **find_best_price**: Return the cheapest in-stock merchant listing for a product
5. **get_deals**: Current active deals and discounts by merchant or category
6. **list_categories**: Enumerate the category tree and merchant coverage
7. **find_similar**: Discover alternative/similar products by category and attributes

## How to Use

### Setup (one-time)

The BuyWhere MCP server is available via streamable-HTTP at `https://api.buywhere.ai/mcp`. Get a free API key in 3 seconds (no signup flow):

```bash
curl -X POST https://api.buywhere.ai/v1/auth/register
```

Then connect via Claude Desktop / Cursor / Codex CLI:

```json
{
  "mcpServers": {
    "buywhere": {
      "url": "https://api.buywhere.ai/mcp",
      "headers": { "Authorization": "Bearer YOUR_KEY" }
    }
  }
}
```

Or stdio for local: `npx @buywhere/mcp-server` (auth via `BUYWHERE_API_KEY` env var).

### Basic Usage

Ask naturally — the skill auto-invokes:

> "Find me the cheapest Sony WH-1000XM5 in Singapore right now"

The skill calls `search_products` then `find_best_price`, returns merchant, price, and stock.

### Advanced Usage

Filter by region, merchant, price range, or in-stock only:

> "Show me Shopee SG listings for the iPhone 17 Pro 256GB under S$1800, in stock only"

The skill calls `search_products({ query, merchant: "shopee_sg", region: "SG", price_max: 1800, in_stock_only: true })`.

### Compare Across Borders

> "Compare MacBook Air M4 13" prices between Amazon US and Shopee SG"

The skill calls `compare_products` with regional merchant filters and returns normalized specs side-by-side.

## Example

**User**: "What's the current price of the Dyson V12 in Singapore and is there a deal?"

**Skill invocation**:
```
1. search_products({ query: "Dyson V12", region: "SG", limit: 5 })
2. get_deals({ query: "dyson", region: "SG" })
3. Compose response with best price + active deal
```

**Output**:
> The Dyson V12 Detect Slim is currently S$899 at Harvey Norman SG (was S$1099, 18% off). In stock with free delivery. Two other listings: S$949 at Shopee SG (no deal), S$999 at Lazada SG. BuyWhere tracks 3 active Dyson deals in SG right now.

## Notes

- Data refreshes hourly; cache results per-query-hash for short windows
- API rate limit: 100 req/min per key (free tier)
- Coverage: Singapore (full), Malaysia, Indonesia, Philippines, Thailand, Vietnam, US
- Merchant coverage: Shopee, Lazada, Amazon, Walmart, Harvey Norman, Best Denki, Challenger, and 13 others
- MCP-native: also exposed via LangChain, LlamaIndex, n8n companion packages
- Source: https://github.com/BuyWhere/buywhere-mcp

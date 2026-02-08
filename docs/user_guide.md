# NSE Analytics - User Guide

**For:** End-users (traders, analysts)  
**Level:** No programming required

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Daily Usage](#daily-usage)
3. [Understanding the Data](#understanding-the-data)
4. [Reading the Charts](#reading-the-charts)
5. [Tips & Best Practices](#tips--best-practices)
6. [Common Questions](#common-questions)

---

## Getting Started

### What You'll Use

- **Google Sheets** - Your interface (no code needed)
- **Python service** - Runs in background (IT/admin starts this)

### Prerequisites

✅ Google Sheet shared with you  
✅ Python service running (ask IT/admin)  
✅ Internet connection

---

## Daily Usage

### Step 1: Open Google Sheet

1. Open the shared Google Sheet
2. You'll see 5 tabs at bottom:
   - `CUSTOM_VIEW` ← **Start here**
   - `RAW_DATA` ← Complete data
   - `CUSTOM_DATA` ← Filtered view
   - `DELIVERY_CHARTS` ← Graphs
   - `SYSTEM_STATUS` ← System health

---

### Step 2: Enter Stock Details

Go to **CUSTOM_VIEW** tab.

**Fill in these cells:**

| Cell | Field | Example | Notes |
|------|-------|---------|-------|
| **C4** | Symbol | `RELIANCE` | NSE stock symbol (all capitals) |
| **C5** | From Date | `01-01-2025` | Format: DD-MM-YYYY |
| **C6** | To Date | `31-01-2025` | Format: DD-MM-YYYY |
| **C7** | Trigger | `TRUE` | Type TRUE or check checkbox |

**Example:**
```
Symbol:          RELIANCE
From Date:       01-01-2025
To Date:         31-01-2025
Update Trigger:  TRUE
```

---

### Step 3: Wait for Data

**What happens:**
1. Python service detects your input (checks every 5 seconds)
2. Downloads data from NSE (takes 5-10 seconds)
3. Updates all sheets automatically
4. Resets trigger to FALSE

**Time:** 10-30 seconds total

**You'll know it's done when:**
- Cell C7 changes back to `FALSE`
- `RAW_DATA` tab fills with data
- Charts appear in `DELIVERY_CHARTS`
- `SYSTEM_STATUS` shows "SUCCESS"

---

### Step 4: View Results

#### Tab 1: CUSTOM_VIEW

**Summary Metrics:**
- Average Delivery %
- Maximum Delivery %
- Minimum Delivery %
- Total Records

**What this tells you:**
- High avg delivery % (>60%) = Genuine buying/selling
- Low avg delivery % (<30%) = Speculative trading

---

#### Tab 2: RAW_DATA

**Complete NSE data dump**

Columns include:
- Symbol, Series, Date
- Open, High, Low, Close prices
- Total Traded Quantity
- Deliverable Quantity
- **Delivery %** (key metric)

**Use:** Reference for detailed analysis

---

#### Tab 3: CUSTOM_DATA

**Filtered view with essential columns:**

| Column | Description |
|--------|-------------|
| SYMBOL | Stock symbol |
| Date | Trading date |
| Traded Volume | Total shares traded |
| Delivery Volume | Shares actually delivered |
| Delivery % | Percentage delivered |

**Use:** Easy-to-read daily breakdown

---

#### Tab 4: DELIVERY_CHARTS

**Visual trend analysis**

**Line graph:**
- X-axis: Date
- Y-axis: Delivery %

**What to look for:**
- **Rising trend** = Accumulation (bullish)
- **Falling trend** = Distribution (bearish)
- **Spikes** = Unusual activity (investigate)
- **Stable high %** = Strong conviction

---

#### Tab 5: SYSTEM_STATUS

**System health monitoring**

Shows:
- Last update time
- Current symbol processed
- Status (SUCCESS / ERROR)
- Data metrics
- Any errors

**Use:** Verify data freshness

---

## Understanding the Data

### Key Metrics Explained

#### Delivery Percentage

**Formula:** (Deliverable Qty ÷ Total Traded Qty) × 100

**What it means:**
- **High (60-100%):** Actual buying/selling with intent to hold
- **Medium (40-60%):** Mix of trading and investing
- **Low (0-40%):** Mostly intraday speculation

**Example:**
```
Total Traded: 1,000,000 shares
Delivered: 600,000 shares
Delivery %: 60%
```

60% were actual deliveries (taken to demat accounts)  
40% were intraday trades (squared off same day)

---

#### Average Delivery %

**What it is:** Mean delivery % across date range

**How to interpret:**
- **>70%** = Very strong delivery-based activity
- **50-70%** = Healthy mix
- **30-50%** = Moderate speculation
- **<30%** = Heavy speculation

---

#### Volume vs Delivery Volume

**Traded Volume:** All shares traded (including intraday)  
**Delivery Volume:** Shares actually transferred to buyers

**Why it matters:**
- High delivery on high volume = Strong conviction
- Low delivery on high volume = Speculation/manipulation risk

---

## Reading the Charts

### Delivery % Trend Chart

#### Patterns to Watch

**1. Rising Delivery %**
```
         ╱
        ╱
       ╱
      ╱
─────╱
```
**Signal:** Accumulation phase  
**Action:** Bullish indicator

---

**2. Falling Delivery %**
```
╲
 ╲
  ╲
   ╲
    ────
```
**Signal:** Distribution phase  
**Action:** Bearish indicator

---

**3. Delivery Spike**
```
    │
────┴────
```
**Signal:** Unusual event (news, results, etc.)  
**Action:** Investigate cause

---

**4. Stable High Delivery**
```
──────────
    (>60%)
```
**Signal:** Sustained investor interest  
**Action:** Strong stock

---

## Tips & Best Practices

### Date Range Selection

✅ **For trend analysis:** 3-6 months  
✅ **For recent activity:** 1-2 weeks  
✅ **For quarterly review:** 3 months  
❌ **Avoid:** More than 1 year (NSE limit)

### Symbol Entry

✅ **Use exact NSE symbol:** `RELIANCE` not `Reliance`  
✅ **Check NSE website** if unsure  
✅ **Common symbols:**
- RELIANCE, TCS, INFY, HDFCBANK
- ICICIBANK, SBIN, BAJFINANCE
- See `data/nse_equity_list.CSV` for full list

### Date Format

✅ **Correct:** `01-01-2025` (DD-MM-YYYY)  
❌ **Wrong:** `2025-01-01`, `1/1/2025`, `Jan 1 2025`

### Multiple Requests

✅ Wait for current request to complete  
✅ Check SYSTEM_STATUS shows SUCCESS  
✅ Then enter next symbol

### Data Freshness

✅ NSE updates delivery data **next day**  
✅ Today's data won't be available until tomorrow  
✅ Weekend/holiday data unavailable until next trading day

---

## Common Questions

### Q: Why is the trigger automatically resetting to FALSE?

**A:** This is normal. The system:
1. Detects TRUE
2. Fetches data
3. Resets to FALSE (ready for next request)

---

### Q: How do I fetch data for a different stock?

**A:** Simple:
1. Change symbol in C4
2. Set C7 to TRUE
3. Wait for update

---

### Q: Can I fetch multiple stocks at once?

**A:** No, one at a time. But you can:
1. Fetch stock A
2. Wait for completion
3. Fetch stock B
4. Repeat

---

### Q: What if data doesn't appear?

**A:** Check:
1. Is Python service running? (ask IT)
2. Is symbol correct? (check NSE website)
3. Is date range valid? (not future dates, max 1 year)
4. Check SYSTEM_STATUS tab for errors

---

### Q: Why does delivery % vary so much day-to-day?

**A:** Normal. Factors:
- News/announcements
- Expiry days (F&O)
- Market volatility
- Institutional activity

**Solution:** Look at trends, not single days

---

### Q: What's a "good" delivery percentage?

**A:**
- **>70%:** Very high (strong hands)
- **50-70%:** Healthy (normal investment activity)
- **30-50%:** Moderate (mix of trading/investing)
- **<30%:** Low (heavy speculation)

**Context matters:** Compare to stock's historical average

---

### Q: Can I export this data?

**A:** Yes, Google Sheets built-in:
- File → Download → Excel (.xlsx)
- File → Download → CSV
- File → Download → PDF

---

### Q: How far back can I go?

**A:**
- NSE allows max **1 year** per request
- For older data, make multiple requests:
  - 01-01-2024 to 31-12-2024
  - 01-01-2023 to 31-12-2023
  - etc.

---

### Q: What if I get "Symbol not found" error?

**A:**
1. Verify symbol on [NSE website](https://www.nseindia.com)
2. Check you're using equity symbol (not F&O)
3. Some stocks delisted/suspended
4. Use exact spelling/caps

---

### Q: Charts not updating?

**A:**
1. Check CUSTOM_DATA has data
2. Refresh sheet (Ctrl+R / Cmd+R)
3. If still broken, recreate chart:
   - Insert → Chart
   - Range: `CUSTOM_DATA!B:E`
   - Type: Line chart

---

## Interpreting Real Examples

### Example 1: Strong Stock

```
Symbol: RELIANCE
Date Range: Jan 2025
Avg Delivery %: 68%
Trend: Stable high
```

**Interpretation:**
- High consistent delivery
- Strong investor confidence
- Not heavily traded speculatively
- **Signal:** Fundamentally driven

---

### Example 2: Speculative Stock

```
Symbol: XYZ
Date Range: Jan 2025
Avg Delivery %: 22%
Trend: Volatile, low
```

**Interpretation:**
- Low delivery percentage
- High intraday trading
- Speculative activity
- **Caution:** Risky, momentum-driven

---

### Example 3: Event-Driven Spike

```
Date: 15-01-2025
Delivery %: 85% (vs 50% average)
Volume: 3x normal
```

**Interpretation:**
- Unusual activity on specific day
- Check for: Results, news, announcements
- **Action:** Research the event

---

## Getting Help

**Data Issues:**
- Check SYSTEM_STATUS tab
- Verify Python service running (ask IT/admin)

**Sheet Issues:**
- Refresh page
- Check formulas in CUSTOM_DATA
- Verify chart data range

**Symbol Questions:**
- Use NSE website to verify
- See `data/nse_equity_list.CSV`

---

## Best Practices Summary

✅ **Always verify symbols** on NSE website first  
✅ **Start with 1-month ranges** for testing  
✅ **Look at trends**, not single days  
✅ **Compare to historical average** for context  
✅ **Check news/events** for delivery spikes  
✅ **Export data regularly** for offline analysis  
✅ **Monitor SYSTEM_STATUS** for errors

---

**Happy Analyzing! 📊**

For setup or technical issues, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

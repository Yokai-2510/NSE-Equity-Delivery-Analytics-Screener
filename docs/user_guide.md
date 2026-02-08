# NSE Equity Delivery Analytics System
## User Guide

**Version:** 1.0  
**Date:** February 8, 2026  
**For:** End Users (Non-Technical)

---

## Welcome! 👋

This guide will help you use the NSE Equity Delivery Analytics System to analyze historical delivery data for any NSE equity symbol.

**What You Can Do:**
- ✅ Get historical delivery data for any NSE stock
- ✅ Analyze delivery trends over custom date ranges
- ✅ Visualize patterns with automatic charts
- ✅ Track volume vs delivery relationships
- ✅ Export data for further analysis

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Understanding the Interface](#2-understanding-the-interface)
3. [Fetching Data](#3-fetching-data)
4. [Interpreting Results](#4-interpreting-results)
5. [Working with Charts](#5-working-with-charts)
6. [Common Use Cases](#6-common-use-cases)
7. [Tips & Best Practices](#7-tips-best-practices)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Quick Start

### Your First Analysis (5 Minutes)

**Step 1:** Open your Google Sheet

Go to: https://sheets.google.com and open your "NSE Delivery Analytics" spreadsheet

**Step 2:** Navigate to CUSTOM_VIEW Tab

Click on the **CUSTOM_VIEW** tab at the bottom of the sheet

**Step 3:** Enter Your Query

| Field | What to Enter | Example |
|-------|---------------|---------|
| Symbol | NSE stock symbol (uppercase) | `INFY` |
| From Date | Start date (DD-MM-YYYY) | `01-01-2026` |
| To Date | End date (DD-MM-YYYY) | `31-01-2026` |
| Update Trigger | Check the box | ☑ |

**Step 4:** Wait for Results

- The checkbox will automatically uncheck
- Data appears in 10-30 seconds
- Check SYSTEM_STATUS for confirmation

**Step 5:** View Your Data

- **RAW_DATA:** Complete dataset
- **CUSTOM_VIEW:** Filtered view with summary metrics
- **DELIVERY_CHARTS:** Visual trends
- **SYSTEM_STATUS:** Operation status

**Done!** You've completed your first analysis.

---

## 2. Understanding the Interface

### 2.1 Sheet Structure

Your Google Spreadsheet has **4 tabs** (sheets):

#### 📊 RAW_DATA
**Purpose:** Complete data storage

**What's Here:**
- All downloaded data from NSE
- Date-wise records
- Price, volume, delivery information
- Complete history for the requested symbol

**User Action:** **View Only** (don't edit this sheet)

---

#### 🎯 CUSTOM_VIEW
**Purpose:** Your control panel and analysis view

**What's Here:**

**Input Section (Top):**
- Symbol input field
- Date range selectors
- Update trigger button
- Summary metrics (Avg, Max, Min delivery %)

**Data Section (Below):**
- Filtered data based on your inputs
- Same data as RAW_DATA but formatted for viewing
- Updates automatically when you trigger new data

**User Action:** **Input & View** (this is your main workspace)

---

#### 📈 DELIVERY_CHARTS
**Purpose:** Visual analytics

**What's Here:**
- Line chart: Delivery % over time
- Combo chart: Volume vs Delivery %
- Trend visualization
- Pattern recognition

**User Action:** **View Only** (charts update automatically)

---

#### 🟢 SYSTEM_STATUS
**Purpose:** System health and operation status

**What's Here:**
- Last update timestamp
- Current symbol being monitored
- Pipeline status (Success/Error)
- Total records fetched
- Summary statistics
- Error messages (if any)

**User Action:** **View Only** (diagnostic information)

---

### 2.2 Input Fields Explained

#### Symbol (Cell B1)
**What it is:** The NSE stock ticker symbol

**Valid Examples:**
- `INFY` (Infosys)
- `RELIANCE` (Reliance Industries)
- `TCS` (Tata Consultancy Services)
- `HDFCBANK` (HDFC Bank)
- `WIPRO` (Wipro Limited)

**Rules:**
- Must be UPPERCASE
- Use exact NSE symbol
- No prefixes (use `INFY`, not `NSE:INFY`)
- No spaces

**Where to Find Symbols:**
Visit https://www.nseindia.com/market-data/live-equity-market

---

#### From Date (Cell B2)
**What it is:** Start date of your analysis period

**Format:** `DD-MM-YYYY`

**Valid Examples:**
- `01-01-2026`
- `15-06-2025`
- `31-12-2025`

**Rules:**
- Must be a trading day (not weekend/holiday)
- Cannot be more than 1 year before "To Date"
- Use DD-MM-YYYY format (not MM-DD-YYYY)

---

#### To Date (Cell B3)
**What it is:** End date of your analysis period

**Format:** `DD-MM-YYYY`

**Valid Examples:**
- `31-01-2026`
- `30-06-2025`
- `31-12-2025`

**Rules:**
- Must be after "From Date"
- Cannot be more than 1 year after "From Date"
- Use DD-MM-YYYY format

---

#### Update Trigger (Cell B4)
**What it is:** The "Go" button

**How it Works:**
- **Unchecked (FALSE):** Idle, no action
- **Checked (TRUE):** Fetch new data
- Auto-unchecks after processing

**How to Use:**
- Click the checkbox to check it
- Or type `TRUE` and press Enter
- System automatically resets to FALSE when done

---

## 3. Fetching Data

### 3.1 Step-by-Step Process

**Step 1: Choose Your Stock**

Think about which stock you want to analyze. Examples:
- Large cap: `RELIANCE`, `TCS`, `HDFCBANK`
- Mid cap: `PERSISTENT`, `MPHASIS`
- Any NSE-listed equity

**Step 2: Decide Your Date Range**

Consider what period you want to analyze:
- Last month: `01-01-2026` to `31-01-2026`
- Last quarter: `01-10-2025` to `31-12-2025`
- Custom period: Any range up to 1 year

**Step 3: Enter in CUSTOM_VIEW**

| Cell | Enter |
|------|-------|
| B1 | Your symbol (e.g., `INFY`) |
| B2 | From date (e.g., `01-01-2026`) |
| B3 | To date (e.g., `31-01-2026`) |

**Step 4: Trigger the Update**

Check the box in B4 or type `TRUE`

**Step 5: Monitor Progress**

Watch the SYSTEM_STATUS sheet:
- "Pipeline Status" will show "Running"
- Wait 10-30 seconds
- Status changes to "Success" when done

**Step 6: Review Results**

Check all sheets:
- ✅ RAW_DATA has new data
- ✅ CUSTOM_VIEW shows filtered view
- ✅ DELIVERY_CHARTS updated
- ✅ SYSTEM_STATUS shows metrics

---

### 3.2 What Happens Behind the Scenes

When you click trigger:

1. **Python service detects** the trigger (within 5 seconds)
2. **Validates your inputs** (symbol format, date range)
3. **Connects to NSE** and downloads historical data
4. **Processes the data** (calculates delivery %, validates)
5. **Updates all sheets** with fresh data
6. **Resets trigger** back to FALSE
7. **Logs success** in SYSTEM_STATUS

**You don't need to do anything except wait!**

---

### 3.3 Response Times

**Expected Wait Times:**

| Date Range | Typical Time |
|------------|-------------|
| 1 week | 5-10 seconds |
| 1 month | 10-15 seconds |
| 3 months | 15-25 seconds |
| 1 year | 20-30 seconds |

**Factors Affecting Speed:**
- NSE server response time
- Internet connection speed
- Number of trading days in range

---

## 4. Interpreting Results

### 4.1 Understanding the Data Columns

#### Symbol
The NSE stock ticker (e.g., INFY, RELIANCE)

#### Date
Trading date in DD-MM-YYYY format

#### Open
Stock price at market open (9:15 AM)

#### High
Highest price during the trading day

#### Low
Lowest price during the trading day

#### Close
Final price at market close (3:30 PM)

#### Total Qty
Total number of shares traded during the day

#### Deliverable Qty
Number of shares actually delivered (transferred to demat accounts)

#### Delivery %
**Most Important Metric!**
- Formula: (Deliverable Qty / Total Qty) × 100
- **High % (>50%):** Indicates investment-based buying
- **Low % (<30%):** Indicates intraday/speculative trading
- **Medium % (30-50%):** Mixed trading activity

#### Turnover
Total value traded (in INR)

#### Trades
Number of individual trades executed

---

### 4.2 Summary Metrics Explained

**Located in CUSTOM_VIEW (Cells D1-D3)**

#### Average Delivery %
**What it is:** Mean delivery percentage over your selected date range

**How to Interpret:**
- **>60%:** Strong investor interest, accumulation phase
- **40-60%:** Balanced trading, neutral sentiment
- **<40%:** High speculation, short-term trading

**Example:**
If Avg Delivery % = 55%, it means on average, 55% of traded shares were delivered (not squared off intraday).

---

#### Max Delivery %
**What it is:** Highest single-day delivery percentage

**How to Interpret:**
- Identifies days with maximum investor conviction
- Often occurs on:
  - Result announcements
  - Major news events
  - Strong buying interest

**Example:**
Max Delivery % = 85% on a specific date → Check news for that date

---

#### Min Delivery %
**What it is:** Lowest single-day delivery percentage

**How to Interpret:**
- Identifies days with maximum speculation
- Often occurs on:
  - High volatility days
  - Expiry days (if related to F&O activity)
  - Market panic/euphoria

**Example:**
Min Delivery % = 15% → Likely a highly speculative trading day

---

### 4.3 Reading the Charts

#### Chart 1: Delivery % Over Time (Line Chart)

**What it Shows:**
- X-axis: Date
- Y-axis: Delivery %
- Trend line showing delivery pattern

**How to Read:**

**Rising Trend:**
- Increasing investor participation
- Accumulation phase
- Positive sentiment

**Falling Trend:**
- Decreasing investor interest
- Profit booking
- Shift to speculative trading

**Stable/Flat:**
- Consistent trading pattern
- Mature stock behavior
- No major sentiment change

---

#### Chart 2: Volume vs Delivery (Combo Chart)

**What it Shows:**
- X-axis: Date
- Left Y-axis: Volume (bars)
- Right Y-axis: Delivery % (line)

**How to Read:**

**High Volume + High Delivery:**
- Strong buying with conviction
- Bullish signal
- Institutional interest

**High Volume + Low Delivery:**
- Speculative activity
- Intraday trading spike
- Caution advised

**Low Volume + High Delivery:**
- Quiet accumulation
- Smart money buying
- Potentially bullish

**Low Volume + Low Delivery:**
- Lack of interest
- Sideways movement expected

---

## 5. Working with Charts

### 5.1 Customizing Charts

**Change Chart Type:**
1. Click on the chart
2. Click three dots (⋮) in top-right
3. Select "Edit chart"
4. Choose different chart type
5. Click "Update"

**Adjust Date Range:**
Charts automatically adjust based on RAW_DATA. To show specific period:
1. Filter RAW_DATA by dates
2. Or use CUSTOM_VIEW filters

**Add More Charts:**
1. Go to DELIVERY_CHARTS sheet
2. Click Insert → Chart
3. Select data range from RAW_DATA
4. Customize as needed

---

### 5.2 Exporting Charts

**As Image:**
1. Click on chart
2. Click three dots (⋮)
3. Select "Download" → "PNG" or "SVG"
4. Save to your computer

**In Presentations:**
1. Click on chart
2. Click three dots (⋮)
3. Select "Copy chart"
4. Paste in Google Slides or PowerPoint

---

## 6. Common Use Cases

### 6.1 Pre-Investment Analysis

**Goal:** Evaluate delivery trends before investing

**Steps:**
1. Enter the stock symbol you're considering
2. Set date range: Last 3-6 months
3. Trigger data fetch
4. Analyze:
   - Is Avg Delivery % > 50%? (Good sign)
   - Is delivery % trending upward? (Accumulation)
   - Check volume on high delivery days (Institutional buying?)

**Decision:**
- High & rising delivery % → Positive for investment
- Low & falling delivery % → High speculation, be cautious

---

### 6.2 Post-Result Tracking

**Goal:** See how the market reacted to quarterly results

**Steps:**
1. Note the result announcement date
2. Set date range: 1 week before to 2 weeks after result date
3. Trigger data fetch
4. Observe:
   - Delivery % spike on result day? (Strong reaction)
   - Volume increase? (Participation level)
   - Sustained high delivery post-results? (Conviction)

**Interpretation:**
- High delivery % post-results → Positive market response
- Low delivery % despite volume → Speculative, short-term move

---

### 6.3 Comparing Investment vs Speculation

**Goal:** Understand if a stock is investor-driven or trader-driven

**Steps:**
1. Fetch 6-month data for the stock
2. Calculate average delivery %
3. Compare with benchmark:

**Investor-Driven Stocks:**
- Avg Delivery % > 60%
- Stable delivery pattern
- Low volatility in delivery %

**Trader-Driven Stocks:**
- Avg Delivery % < 40%
- Volatile delivery pattern
- Wild swings in delivery %

---

### 6.4 Identifying Accumulation Phases

**Goal:** Spot when smart money is accumulating

**Steps:**
1. Fetch 3-month data
2. Look for pattern:
   - Rising delivery % despite flat/falling price
   - Increasing volume + increasing delivery %
   - Consistent high delivery (>60%) for 10+ days

**Signal:**
This indicates accumulation → Potential future rally

---

### 6.5 Monitoring Your Holdings

**Goal:** Track delivery trends in stocks you own

**Steps:**
1. Create a list of your holdings
2. Fetch data for each symbol (one at a time)
3. Track weekly/monthly:
   - Is delivery % increasing? (Others accumulating)
   - Is delivery % decreasing? (Distribution phase?)
   - Compare with historical average

**Action:**
- Rising delivery → Hold/Add
- Falling delivery → Review fundamentals, consider exit

---

## 7. Tips & Best Practices

### 7.1 Date Range Selection

**For Short-Term Trading:**
- Use: 1-2 weeks
- Focus: Daily delivery % changes
- Look for: Spikes and drops

**For Long-Term Investing:**
- Use: 3-6 months
- Focus: Average delivery % and trend
- Look for: Consistent patterns

**For Special Events:**
- Result announcements: ±2 weeks around date
- Corporate actions: ±1 month
- News events: ±1 week

---

### 7.2 Symbol Selection Tips

**Check Symbol on NSE Website:**
1. Go to: https://www.nseindia.com
2. Search for company name
3. Copy the exact symbol shown

**Common Symbol Patterns:**
- Most company names: `TCS`, `WIPRO`, `INFY`
- Banks: Often include "BANK" - `HDFCBANK`, `ICICIBANK`
- Multiple series stocks: Use main symbol (usually without suffix)

---

### 7.3 Data Quality Checks

**Always Verify:**

1. **Date Range Coverage:**
   - Check SYSTEM_STATUS → "Total Records"
   - Trading days only (expect ~20-22 days per month)
   - Weekends and holidays excluded

2. **Data Completeness:**
   - Scroll through RAW_DATA
   - No major gaps in dates
   - All columns populated

3. **Delivery % Range:**
   - Should be between 0-100%
   - If all zeros → Data issue, re-fetch
   - If >100% → Report as bug

---

### 7.4 Performance Tips

**Optimize Your Queries:**

**DO:**
- ✅ Fetch data once, analyze multiple times
- ✅ Use reasonable date ranges (1-3 months typical)
- ✅ Wait for previous query to complete before new one
- ✅ Download sheet as Excel for offline analysis

**DON'T:**
- ❌ Trigger multiple times rapidly (causes errors)
- ❌ Fetch full 1-year data unless really needed
- ❌ Keep triggering if system shows error (check logs first)

---

### 7.5 Exporting Data

**To Excel:**
1. File → Download → Microsoft Excel (.xlsx)
2. All sheets and formatting preserved
3. Charts export as images

**To CSV:**
1. Go to RAW_DATA sheet
2. File → Download → Comma-separated values (.csv)
3. Import into any analysis tool

**To PDF:**
1. File → Download → PDF
2. Choose sheets to include
3. Adjust layout settings

---

## 8. Troubleshooting

### 8.1 User-Side Issues

#### Issue: "Trigger doesn't work"

**Symptoms:**
- Checkbox doesn't uncheck
- No data appears
- SYSTEM_STATUS doesn't update

**Solutions:**
1. **Wait longer:** Sometimes takes up to 30 seconds
2. **Check SYSTEM_STATUS:** Look for error messages
3. **Verify inputs:**
   - Symbol is uppercase and valid
   - Dates are in DD-MM-YYYY format
   - Date range is ≤ 1 year
4. **Try manual trigger:** Type `TRUE` in B4 instead of checkbox

---

#### Issue: "Invalid symbol" error

**Symptoms:**
- SYSTEM_STATUS shows "Invalid symbol format"
- No data fetched

**Solutions:**
1. **Verify symbol spelling:**
   - Go to NSE website
   - Search for company
   - Copy exact symbol
2. **Check for spaces:** Remove any spaces before/after symbol
3. **Ensure uppercase:** Type in CAPS

---

#### Issue: "No data for date range"

**Symptoms:**
- SYSTEM_STATUS shows success
- RAW_DATA is empty or has very few rows

**Possible Causes:**
1. **Weekends/Holidays:** No trading = no data
2. **Future dates:** Cannot fetch data for dates in future
3. **Symbol suspended:** Stock not traded during that period

**Solutions:**
- Adjust date range to recent trading days
- Verify symbol was trading during that period

---

#### Issue: "Old data still showing"

**Symptoms:**
- Triggered new query
- RAW_DATA shows previous symbol's data

**Solution:**
1. **Hard refresh browser:** Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. **Check SYSTEM_STATUS:** Verify "Symbol" field shows new symbol
3. **Wait for processing:** May take 20-30 seconds for large datasets

---

### 8.2 Understanding Error Messages

**In SYSTEM_STATUS sheet, "Last Error" field:**

| Error Message | Meaning | Action |
|---------------|---------|--------|
| "Invalid symbol format" | Symbol validation failed | Check spelling, use uppercase |
| "Invalid date range" | Date format wrong or range > 1 year | Fix date format or reduce range |
| "NSE API error: 403" | NSE blocked request temporarily | Wait 5-10 minutes, retry |
| "No data found" | Symbol had no trading in date range | Check if symbol was suspended |
| "Connection timeout" | Network issue or NSE down | Check internet, retry later |

---

### 8.3 When to Contact Support

**Contact support if:**
- Error persists after 3 retry attempts
- SYSTEM_STATUS shows error you don't understand
- Data appears corrupted (wrong values, missing columns)
- Charts don't update despite successful data fetch
- Application stops responding for >5 minutes

**Before Contacting:**
1. Screenshot of SYSTEM_STATUS
2. Note what you entered (symbol, dates)
3. Describe what you expected vs what happened
4. Check if internet connection is stable

---

## 9. Advanced Usage

### 9.1 Creating Custom Formulas

**In CUSTOM_VIEW, you can add your own analysis columns.**

**Example: High Delivery Days Counter**

In a new column (e.g., F1):
```
=COUNTIF(RAW_DATA!I:I, ">60")
```
This counts days with delivery % > 60%

**Example: Average Volume**
```
=AVERAGE(FILTER(RAW_DATA!G:G, RAW_DATA!G:G>0))
```

**Example: Max Price in Range**
```
=MAX(RAW_DATA!D:D)
```

---

### 9.2 Conditional Formatting

**Highlight High Delivery Days:**

1. Select the Delivery % column in CUSTOM_VIEW
2. Format → Conditional formatting
3. Format cells if: "Greater than" → `60`
4. Choose green background
5. Add another rule: "Less than" → `30`
6. Choose red background

Now high delivery days are green, low are red!

---

### 9.3 Creating Comparison Sheets

**Compare Multiple Stocks:**

1. Fetch data for Stock A (e.g., INFY)
2. **Copy RAW_DATA to new sheet** named "INFY_Data"
3. Fetch data for Stock B (e.g., TCS)
4. **Copy RAW_DATA to new sheet** named "TCS_Data"
5. Create comparison formulas:
   - Avg Delivery INFY: `=AVERAGE(INFY_Data!I:I)`
   - Avg Delivery TCS: `=AVERAGE(TCS_Data!I:I)`

**Note:** RAW_DATA gets overwritten each query, so copy if you want to keep!

---

## 10. Keyboard Shortcuts

**Google Sheets Shortcuts:**

| Action | Windows | Mac |
|--------|---------|-----|
| Refresh page | Ctrl+R | Cmd+R |
| Hard refresh | Ctrl+Shift+R | Cmd+Shift+R |
| Find | Ctrl+F | Cmd+F |
| Download | Ctrl+D | Cmd+D |
| New tab | Ctrl+T | Cmd+T |
| Jump to cell | Ctrl+G | Cmd+G |

---

## 11. Best Practices Summary

### ✅ DO:
- Use valid NSE symbols (check nseindia.com)
- Use DD-MM-YYYY date format
- Wait for completion before new query
- Check SYSTEM_STATUS for errors
- Download data for offline analysis if needed
- Keep date ranges reasonable (1-3 months typical)

### ❌ DON'T:
- Trigger multiple queries simultaneously
- Use symbols from other exchanges (only NSE)
- Fetch more than 1 year data in single query
- Edit RAW_DATA sheet manually (it gets overwritten)
- Share your Google Sheet credentials publicly
- Expect real-time or intraday data (historical only)

---

## 12. Glossary

**Delivery Percentage:** Percentage of traded quantity that was delivered to demat accounts (not squared off intraday)

**Trading Day:** Days when stock exchange is open (excludes weekends, holidays)

**NSE Symbol:** Official ticker code for a stock on National Stock Exchange

**VWAP:** Volume Weighted Average Price

**Turnover:** Total value of shares traded (quantity × price)

**Accumulation:** Phase where investors are buying and holding (high delivery %)

**Distribution:** Phase where investors are selling (falling delivery %)

---

## 13. Quick Reference Card

### Minimum Requirements
- ✅ Valid NSE symbol
- ✅ Date range ≤ 1 year
- ✅ DD-MM-YYYY date format
- ✅ Internet connection

### What to Enter
| Field | Format | Example |
|-------|--------|---------|
| Symbol | UPPERCASE | `RELIANCE` |
| From Date | DD-MM-YYYY | `01-01-2026` |
| To Date | DD-MM-YYYY | `31-01-2026` |
| Trigger | Check box | ☑ |

### Expected Results
- ⏱️ Wait time: 10-30 seconds
- 📊 Data in: RAW_DATA, CUSTOM_VIEW
- 📈 Charts in: DELIVERY_CHARTS
- ✅ Status in: SYSTEM_STATUS

### Common Symbols
- `RELIANCE` - Reliance Industries
- `TCS` - Tata Consultancy Services
- `INFY` - Infosys
- `HDFCBANK` - HDFC Bank
- `WIPRO` - Wipro
- `SBIN` - State Bank of India
- `ITC` - ITC Limited

---

## 14. Getting Help

**Self-Help Resources:**
1. Check this User Guide
2. Review SYSTEM_STATUS for error messages
3. Verify inputs against requirements
4. Try with a different symbol/date range

**Support Channels:**
- Email: support@yourcompany.com
- GitHub: (link if available)
- Documentation: (link to full docs)

**When Reporting Issues:**
Include:
- Symbol and date range you entered
- Screenshot of SYSTEM_STATUS
- Error message (if any)
- What you expected vs what happened

---

**Happy Analyzing! 📊**

Your feedback helps us improve. If you have suggestions, please share them!

---

**End of User Guide**
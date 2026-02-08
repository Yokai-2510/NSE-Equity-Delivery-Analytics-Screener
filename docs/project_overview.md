# NSE Equity Delivery Analytics System
## Project Overview Document

**Version:** 1.0  
**Date:** February 8, 2026  
**Project Type:** Data Analytics Pipeline with Google Sheets Interface

---

## 1. Executive Summary

The NSE Equity Delivery Analytics System is a Python-based data pipeline that automatically fetches historical equity delivery data from the National Stock Exchange of India (NSE) and presents it in an interactive Google Sheets dashboard.

**Core Value Proposition:**
- Eliminate manual data download and formatting
- Instant historical delivery analysis for any NSE equity
- Visual trend analysis without technical knowledge
- Self-service analytics for traders and analysts

---

## 2. Problem Statement

### Current Pain Points
- NSE historical data requires manual download via browser
- Data comes in raw CSV format requiring cleanup
- Analysis requires Excel expertise and formula knowledge
- Repetitive work for each symbol and date range
- No automated refresh mechanism
- Charts and metrics must be manually recreated

### Solution
A monitoring service that:
1. Watches a Google Sheet for user input
2. Automatically downloads NSE data when requested
3. Processes and structures the data
4. Updates all analysis sheets automatically
5. Maintains system health monitoring

---

## 3. Scope & Boundaries

### In Scope
- **Exchange:** NSE (National Stock Exchange of India)
- **Segment:** Equity (EQ series only)
- **Symbols:** Any NSE-listed equity symbol
- **Date Range:** Any historical range (max 1 year per request)
- **Metrics:** Price, volume, delivery quantity, delivery percentage
- **Interface:** Google Sheets only
- **Automation:** Trigger-based pipeline execution

### Out of Scope
- Intraday or real-time data
- Futures and Options (F&O) segment
- Corporate actions adjustments
- Predictive analytics or trading signals
- Multiple symbols in single request
- Data export to other formats
- Mobile or web interface

---

## 4. System Capabilities

### 4.1 Data Acquisition
- Fetch historical data from NSE public API
- Handle NSE's cookie-based authentication
- Retry mechanism for network failures
- Download data in CSV format
- Store raw data temporarily

### 4.2 Data Processing
- Parse NSE CSV format
- Validate data completeness
- Calculate delivery percentage
- Standardize date formats
- Handle missing or malformed data

### 4.3 Google Sheets Integration
- Monitor user input cells for changes
- Detect update trigger (button click)
- Write data to multiple sheets atomically
- Preserve formulas and chart references
- Update system health metrics

### 4.4 System Monitoring
- Track last successful data fetch
- Log pipeline execution status
- Record API response times
- Monitor error conditions
- Maintain operational metrics

---

## 5. User Workflow

### Step-by-Step Process

**Step 1: User Input**
- Open the Google Sheet
- Navigate to "CUSTOM_VIEW" sheet
- Enter NSE symbol (e.g., "RELIANCE", "INFY", "TCS")
- Select From Date (DD-MM-YYYY)
- Select To Date (DD-MM-YYYY)
- Click "Update Data" button or check the trigger box

**Step 2: System Processing** (Automated)
- Python service detects the trigger
- Validates symbol and date range
- Downloads data from NSE
- Processes CSV file
- Updates all sheets

**Step 3: View Results**
- "RAW_DATA" sheet contains complete dataset
- "CUSTOM_VIEW" sheet shows filtered, user-friendly view
- "DELIVERY_CHARTS" displays visual trends
- "SYSTEM_STATUS" shows health and last update time

**Step 4: Analysis**
- Review delivery percentage trends
- Identify high/low delivery days
- Compare volume vs delivery patterns
- Export or share the sheet as needed

---

## 6. Google Sheets Structure

The system maintains a single Google Spreadsheet with 4 sheets:

### Sheet 1: RAW_DATA
**Purpose:** Complete data dump (source of truth)

**Contents:**
- All NSE CSV columns as-is
- Symbol, Date, Open, High, Low, Close
- VWAP, Total Traded Quantity, Turnover
- Deliverable Quantity, Delivery Percentage
- Number of Trades

**User Interaction:** None (read-only for users)

**Technical Note:** Other sheets reference this via formulas

---

### Sheet 2: CUSTOM_VIEW
**Purpose:** User-friendly filtered view and input interface

**Contains:**
- Input fields: Symbol, From Date, To Date, Update Trigger
- Filtered data based on user selection
- Summary metrics (Average, Max, Min delivery %)
- Conditional formatting for quick insights

**User Interaction:** Primary interface for inputs and viewing results

**Technical Note:** Uses QUERY or FILTER formulas to subset RAW_DATA

---

### Sheet 3: DELIVERY_CHARTS
**Purpose:** Visual analytics

**Contains:**
- Line chart: Delivery % over time
- Bar chart: Daily volume comparison
- Combo chart: Price vs Delivery %
- Trend indicators

**User Interaction:** View-only, auto-updates

**Technical Note:** Chart data ranges dynamically reference RAW_DATA

---

### Sheet 4: SYSTEM_STATUS
**Purpose:** Operational health monitoring

**Displays:**
- Last CSV Download Time
- Last Successful Update Time
- Current Symbol Being Monitored
- Date Range Being Monitored
- Pipeline Status (Idle / Running / Error)
- Total Records Fetched
- API Response Time (seconds)
- Error Log (last 5 errors)

**User Interaction:** View-only, diagnostic information

**Technical Note:** Updated by Python service on each pipeline run

---

## 7. Key Metrics Provided

### Price Metrics
- **Open Price:** Day's opening price
- **High Price:** Day's highest price
- **Low Price:** Day's lowest price
- **Close Price:** Day's closing price
- **VWAP:** Volume Weighted Average Price

### Volume Metrics
- **Total Traded Quantity:** Total shares traded
- **Turnover:** Total value traded (in currency)
- **Number of Trades:** Count of executed trades

### Delivery Metrics
- **Deliverable Quantity:** Shares transferred to demat accounts
- **Delivery Percentage:** (Deliverable Qty / Total Qty) × 100

### Derived Analytics
- **Average Delivery %:** Mean across date range
- **Maximum Delivery %:** Highest single-day delivery
- **Minimum Delivery %:** Lowest single-day delivery
- **Delivery Trend:** Visual pattern over time

---

## 8. Technical Architecture (High-Level)

### Components
1. **Python Monitoring Service:** Polls Google Sheets for triggers
2. **NSE Data Fetcher:** Downloads historical CSV from NSE API
3. **Data Processor:** Parses and validates CSV data
4. **Google Sheets Writer:** Updates all sheets atomically
5. **Logging System:** Tracks operations and errors

### Data Flow
```
User Input (Google Sheets)
    ↓
Trigger Detection (Python polls every 5 sec)
    ↓
Input Validation (Symbol, dates)
    ↓
NSE API Call (Download CSV)
    ↓
Data Processing (Parse, validate, calculate)
    ↓
Google Sheets Update (Write to all sheets)
    ↓
System Status Update (Log success/failure)
    ↓
CSV Cleanup (Delete local file)
```

### Deployment
- Runs as a background Python service
- Can be deployed on local machine, cloud VM, or serverless
- Requires continuous operation to monitor triggers

---

## 9. System Requirements

### For Python Service
- **Python Version:** 3.9 or higher
- **Libraries:** requests, pandas, gspread, pyyaml
- **Storage:** 100 MB for logs and temporary CSVs
- **Network:** Stable internet connection
- **Runtime:** Continuous (24/7 for best experience)

### For Google Sheets
- **Google Account:** Required
- **Sheet Permissions:** Service account must have Editor access
- **Browser:** Any modern browser
- **Internet:** Required for viewing and editing

---

## 10. Limitations & Constraints

### Data Limitations
- Maximum 1 year of data per request (NSE limitation)
- Historical data only (no real-time)
- Equity segment only (no F&O, commodities, etc.)
- Data accuracy depends on NSE API uptime

### Technical Constraints
- Requires Python service to be running
- Google Sheets API has rate limits (300 requests/minute)
- NSE API may throttle excessive requests
- Large date ranges may take 10-30 seconds to process

### Operational Constraints
- Service must restart if server reboots
- Google Sheets must be shared with service account
- Network interruptions will delay updates
- Manual intervention needed if NSE changes API format

---

## 11. Success Criteria

### Functional Success
- ✅ User can fetch data for any NSE equity symbol
- ✅ Data appears in Google Sheets within 30 seconds
- ✅ All metrics calculate correctly
- ✅ Charts update automatically
- ✅ System status reflects accurate state

### Performance Success
- ✅ 95% uptime for monitoring service
- ✅ < 30 second end-to-end pipeline execution
- ✅ < 5% data fetch failure rate
- ✅ Handles 100+ daily update requests

### User Experience Success
- ✅ No technical knowledge required
- ✅ Clear error messages when issues occur
- ✅ Intuitive sheet layout
- ✅ Reliable and predictable behavior

---

## 12. Future Enhancements (Not in Current Scope)

### Potential Additions
- Multi-symbol comparison in single view
- Email/Slack alerts on delivery spikes
- Historical comparison (this year vs last year)
- Automatic weekly/monthly data refresh
- Export to PDF reports
- Integration with portfolio tracking systems
- Real-time data streaming (when available from NSE)

### Scalability Considerations
- Could support multiple users with separate sheets
- Could be extended to other exchanges (BSE, etc.)
- Could add database layer for faster historical queries
- Could build web UI as alternative to Google Sheets

---

## 13. Stakeholders

### Primary Users
- **Retail Traders:** Analyze delivery trends before trading decisions
- **Analysts:** Research delivery patterns for reports
- **Portfolio Managers:** Monitor delivery activity in holdings

### System Administrators
- **DevOps/IT Team:** Deploy and maintain Python service
- **Data Team:** Troubleshoot data quality issues

### Service Providers
- **NSE:** Data source (public API)
- **Google Cloud:** Sheets API and potential hosting
- **Python Ecosystem:** Core libraries and tools

---

## 14. Risk Assessment

### Technical Risks
- **NSE API Changes:** Medium probability, high impact
  - *Mitigation:* Monitoring alerts, version-locked API endpoints
  
- **Google Sheets API Limits:** Low probability, medium impact
  - *Mitigation:* Rate limiting, batch operations
  
- **Service Downtime:** Medium probability, medium impact
  - *Mitigation:* Health checks, auto-restart, logging

### Operational Risks
- **User Error (Invalid Symbol):** High probability, low impact
  - *Mitigation:* Input validation, clear error messages
  
- **Network Failures:** Medium probability, low impact
  - *Mitigation:* Retry logic, timeout handling

### Data Risks
- **Incomplete Data from NSE:** Low probability, medium impact
  - *Mitigation:* Data validation, fill missing values
  
- **Timezone/Date Format Issues:** Low probability, low impact
  - *Mitigation:* Consistent date parsing, UTC timestamps

---

## 15. Compliance & Legal

### Data Usage
- Uses publicly available NSE data
- No redistribution or commercial resale of data
- For personal/internal analysis only
- Subject to NSE terms of service

### Privacy
- No user personal data collected
- Google service account credentials secured
- Logs contain only operational data (no PII)

### Licensing
- Python code: MIT License (or client's choice)
- NSE data: Subject to NSE usage terms
- Google Sheets: Subject to Google's terms of service

---

## 16. Glossary

**NSE:** National Stock Exchange of India

**Equity:** Stock or share of a company

**Delivery Percentage:** Proportion of traded shares that were actually delivered (vs intraday speculation)

**VWAP:** Volume Weighted Average Price - average price weighted by volume

**Service Account:** Google account used by applications (not humans)

**Pipeline:** Automated sequence of data processing steps

**Trigger:** User action that initiates the data fetch process

**Raw Data:** Unprocessed data directly from NSE

---

## 17. Document Control

**Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-08 | System Architect | Initial document |

**Approvals:**

- [ ] Project Sponsor
- [ ] Technical Lead
- [ ] End User Representative

**Next Review Date:** 2026-05-08

---

**End of Project Overview Document**
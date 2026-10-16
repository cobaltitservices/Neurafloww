# FLOW TESTER PRO / NEURAFLOWW: DEVELOPMENT DIARY

**Project Codename**: Neurafloww / Flow Tester Pro Quantitative Terminal  
**Primary Repository**: [cobaltitservices/Neurafloww](https://github.com/cobaltitservices/Neurafloww.git)  
**Hosting & Deployment**: Vercel Serverless Edge CDN  
**Database & Telemetry**: Supabase / Serverless Architecture  
**Document Classification**: Engineering Log & Project Development Diary  
**Date of Record**: October 15, 2026  

---

## 1. Executive Summary & Mission

Flow Tester Pro (Neurafloww) is an institutional-grade algorithmic cryptocurrency training platform, backtesting matrix, and web terminal. The system orchestrates over 1,824 to 2,400 discrete deep learning models across 18 major trading pairs and 16 timeframe resolutions, executing predictive inference using 6 specialized neural network architectures.

This development diary records the chronological evolution of the platform: from initial model training and distributed compute orchestration on Google Cloud Platform, through the strategic migration to a serverless GitHub and Vercel pipeline, to the latest user experience and telemetry enhancements.

---

## 2. Infrastructure Evolution: GCP to Serverless Vercel

```
[Phase 1: Legacy Monolith]
GCP Compute Instance (34.170.186.204)
├── Nginx Web Server (/var/www/html)
├── FastAPI Daemon (Port 8000 via Systemd)
└── Local File Storage & SQLite DB

            │
            ▼ [Strategic Architecture Migration]

[Phase 2: Modern Serverless Stack]
GitHub Repository (cobaltitservices/Neurafloww)
├── Continuous Deployment: Vercel Edge CDN (Automatic GitHub Webhook Deploy)
├── High-Performance Static Web Application (HTML5 / Vanilla CSS / ES6 JavaScript)
├── Database & Identity: Supabase Integration
└── Local Automated Sync Utility (deploy_to_github.sh)
```

### Strategic Rationale
- **Cost Reduction**: Replaced recurring cloud virtual machine compute costs with free-tier Vercel CDN hosting and Supabase database services.
- **Reliability & Uptime**: Eliminated single-point-of-failure VM crashes, memory leaks, and port 22/80 timeout risks.
- **Instant Global Edge Delivery**: Static assets and dashboard components are served with sub-50ms latency across global edge locations.
- **Automated CI/CD**: Every push to the `main` branch of `cobaltitservices/Neurafloww` triggers instant automated building and deployment.

---

## 3. Chronological Development Log

### Phase 1: Deep Learning Engine & Pipeline Architecture
- **ClickHouse Ingestion**: Built streaming data collectors ingesting tick-level and multi-timeframe OHLCV data across 18 cryptocurrency pairs (BTC, ETH, SOL, XRP, DOGE, ADA, AVAX, LINK, BNB, NEAR, MATIC, DOT, LTC, ATOM, UNI, SHIB, ZEC, TRX).
- **Timeframe Matrix**: Configured 16 discrete timeframe resolutions (1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w).
- **Model Architecture Suite**:
  1. *Architecture 1 (LSTM)*: Deep Long Short-Term Memory recurrent networks for sequential trend persistence.
  2. *Architecture 2 (GRU)*: Gated Recurrent Units optimized for lower latency and volatile market regimes.
  3. *Architecture 3 (TCN)*: Temporal Convolutional Networks with dilated causal convolutions for large receptive fields.
  4. *Architecture 4 (Transformer)*: Multi-head self-attention models capturing cross-temporal correlations.
  5. *Architecture 5 (CNN-LSTM)*: Hybrid spatial feature extraction paired with temporal sequential forecasting.
  6. *Architecture 6 (MLP-Mixer)*: Token-mixing and channel-mixing multi-layer perceptrons for linear complexity inference.
- **Leak-Free Scaling**: Designed chronological data splitters and fit-only-on-train standard scalers (`scaler.pkl`).
- **Resource-Aware Orchestrator**: Developed multi-process workers with automatic checkpoint recovery and state tracking in `jobs.db`.

---

### Phase 2: Quantitative Backtesting & Paper Trading Engine
- **Vectorized Backtesting Engine**: Developed high-speed evaluators computing institutional metrics:
  - Cumulative Return Percentage
  - Sharpe Ratio and Sortino Ratio (downside volatility risk-adjusted metric)
  - Maximum Drawdown (MDD)
  - Win Rate Percentage and Profit Factor
- **Simulated Paper Trading Engine**: Constructed an order book execution simulation with configurable slippage, maker/taker exchange fee deduction, and dynamic position sizing.
- **Automated Reporting Suite**: Generated multi-format exports (CSV, JSON, HTML, PDF) via `storage/export_engine.py` for audit compliance.

---

### Phase 3: Dashboard Interface & Bloomberg Terminal Aesthetic
- **Visual Design System**: Created a dark-mode first, glassmorphic quantitative terminal aesthetic with tailored HSL color tokens (`#030712`, `#0b1329`, `#38bdf8`, `#10b981`, `#f59e0b`, `#ef4444`).
- **Live Market Feeds**: Embedded responsive TradingView/Binance candlestick charting alongside custom SVG equity curve projections.
- **Model Leaderboard**: Built real-time sorting and filtering across all 1,824+ models with quick tier filters:
  - Top 1% Institutional Best Performers
  - Top 10% High-Accuracy Decile
  - Top 24 Benchmark Models
- **Theme Engine**: Integrated dual light/dark mode with smooth CSS transition tokens and local storage persistence.

---

### Phase 4: Migration to GitHub, Vercel & Supabase
- **GCP Decommissioning**: Fully retired the legacy Google Cloud Platform compute instance (`34.170.186.204`).
- **Repository Setup**: Initialized and configured the public repository at `https://github.com/cobaltitservices/Neurafloww.git`.
- **Pure Static Optimization**: Streamlined application bundle for Vercel static hosting:
  - Removed heavy server-side Python dependencies from the deployment tree.
  - Configured `vercel.json` with `framework: null`, static route rewrites, and immutable asset cache headers.
- **Automated Deployment Script**: Created `deploy_to_github.sh` in the workspace to synchronize dashboard updates and push to GitHub via authenticated token in a single command.

---

### Phase 5: Branding, Communication & Mobile Optimization
- **Interactive Branding**: Linked the Flow Tester header logo directly to the primary matrix view with smooth top-scrolling.
- **Clickable Telephone Support**: Added support hotline link (`+1 (800) 555-0199`) in the navigation toolbar with one-click clipboard copying and automatic system dialer triggering.
- **Operations Support Email**: Connected the operations email (`security@quantlabs.cloud`) with pre-populated subject lines and clipboard copy feedback.
- **Comprehensive Mobile Optimization**:
  - Re-engineered viewport metadata and CSS media queries (`max-width: 768px` and `max-width: 480px`).
  - Implemented collapsible hamburger sidebar with touch-friendly backdrop overlay.
  - Converted rigid data grids into horizontally swipeable cards.
  - Adapted modal dialogs to responsive viewports (`width: 94%`, `max-height: 90vh`).

---

### Phase 6: Interface Refinements & Quick-Menu Architecture
- **Navigation Label Standardization**: Renamed primary sidebar links to clean, modern terminology:
  - `Model Matrix / Jobs`
  - `Model Leaderboard`
  - `Paper Trading`
  - `Activity Logs`
  - `Admin`
  - `API`
- **Header Simplification**: Removed legacy 100% CPU boost button from the navigation toolbar.
- **Global Search Placeholders**: Added standardized `placeholder="Search bar..."` across search inputs.
- **Footer Quick-Menu Pop-Up Boxes**: Re-architected footer category headings into interactive toggle buttons with scrollable pop-up menus (`max-height: 175px; overflow-y: auto;`):
  - *Terminal Modules*: Direct jumps to Jobs, Leaderboard, Paper Trading, Logs, Admin, and API.
  - *Cloud Clusters*: Quick navigation to GCP compute, cluster metrics, and storage exports.
  - *Developer & APIs*: Links to OpenAPI specs, Python SDK, and export utilities.
  - *Governance & Legal*: Compliance notices, Privacy Policy, Terms of Service, and documentation.
- **Dismissal Handlers**: Added outside-click detection and Escape key listeners to close open footer menus.

---

### Phase 7: Usability, Telemetry & Universal Search Suite
- **Password Visibility Toggle**:
  - Enhanced the Admin Login modal with an eye/eye-slash visibility toggle button (`admin-pw-toggle-btn`).
  - Built a dedicated Change Password modal (`change-pw-modal-overlay`) with visibility toggles for Current Password, New Password, and Confirm Password fields.
  - Implemented the reusable JavaScript helper `togglePasswordVisibility(inputId, iconId, btnEl)`.
- **UTM Tracking & Campaign Attribution**:
  - Automated URL query parameter parsing (`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `ref`).
  - Configured multi-session persistence across `sessionStorage` and `localStorage`.
  - Added a live attribution pill (`utm-tracking-pill`) in the header toolbar.
  - Added an attribution telemetry card inside the Admin Visits tab.
  - Created an interactive Campaign URL Builder modal (`utm-modal-overlay`) with a one-click copy button.
- **Scroll Progress Bar**:
  - Implemented a 3px glowing accent bar (`scroll-progress-bar`) fixed at the top of the viewport.
  - Calculates page scroll depth from 0% to 100% using passive scroll listeners.
- **Universal Site Search & Command Palette**:
  - Added header search trigger (`site-search-trigger`) with `⌘K` keyboard badge.
  - Configured global keyboard shortcuts (`/` or `Cmd+K` / `Ctrl+K`) to open the Command Palette.
  - Built search indexing covering Trading Pairs, Neural Architectures, Terminal Views, Actions, and Legal Docs.
  - Added arrow key navigation (`Up` / `Down`), `Enter` execution, and `Escape` dismissal.
- **Sticky Headers**:
  - Elevated top navigation bar (`.top-header`) with `position: sticky; top: 0; z-index: 100; backdrop-filter: blur(16px);`.
  - Added dynamic scroll shadow (`.header-scrolled`) when scrolling down the page.
  - Configured data table headers (`.table th`) with `position: sticky; top: 0; z-index: 15; backdrop-filter: blur(8px);`.
  - Set all `.table-wrap` containers to `overflow-y: auto; max-height: 640px;` so headers stay pinned when scrolling data rows.

### Phase 8: Uniform Platform Rebranding to NEURAFLOWW
- **Sidebar Brand Component**: Updated the prominent sidebar brand header to `NEURAFLOWW` with version badge `v3.0 PRO` and `• QUANT TERMINAL` status indicator.
- **Page Titles & Meta Suite**: Synchronized document titles, meta descriptions, Open Graph cards, Twitter Cards, and web app manifest identifiers from legacy "Flow Tester" to **Neurafloww**.
- **Navigation & Universal Search**: Rebranded the quick search modal index to `Neurafloww Universal Index` and updated all view docTitle dynamic switchers.
- **Footer & 404 Routing**: Rebranded footer brand title to `NEURAFLOWW PRO`, copyright notice to `Neurafloww Quantitative Systems`, and 404 error template headers.

### Phase 9: Master Handover Documentation & Institutional Architecture Transfer
- **Comprehensive Handover Manual**: Created `HANDOVER_DOCUMENTATION.md` following the institutional "leaving the company" knowledge transfer standard.
- **Binance Ingestion Engine**: Fully documented REST kline ingestion, 1.0-second cached batch price queries, WebSocket streams, 18-asset universe, 16 timeframe resolutions, and 13-feature engineering vector.
- **ClickHouse Analytics Architecture**: Documented native columnar time-series queries on `crypto_data.ohlcv_data` at host `34.132.233.162:8123`, partitioned by `toYYYYMM(timestamp)`, with sub-millisecond query latency and Geometric Brownian Motion (GBM) offline synthetic fallback.
- **Backblaze B2 & Cold Storage**: Documented S3-compatible API integration (`s3.us-west-004.backblazeb2.com`), Snappy Parquet tick archival, model checkpoint backup, and 78% storage cost savings over standard cloud providers.
- **Multi-Cloud Compute Infrastructure**: Detailed AWS EC2 instance profiles (`c5.9xlarge`, `c7i.16xlarge`, `g5.xlarge`, `t3.medium`), DynamoDB tables, GCP compute/GCS buckets, and Salad Cloud decentralized GPU training on RTX 3090/4090 hardware.
- **Admin Development Diary UI Revamp**: Elevated the Development Diary in `dashboard/index.html` with glassmorphic cards, glowing cyan accents, phase chip filters, copy-to-clipboard buttons, and raw markdown inspectors.

---

## 4. Key Repository Files & Architecture Map

| File Path | Description | Target Environment |
|---|---|---|
| `HANDOVER_DOCUMENTATION.md` | Master institutional handover manual & complete technical audit | Project Root & Docs |
| `DEVELOPMENT_DIARY.md` | Complete engineering changelog and development diary | Project Root & Docs |
| `dashboard/index.html` | Primary Single Page Application (UI, CSS, and JS) | Vercel Static CDN |
| `dashboard/404.html` | Custom branded 404 error page | Vercel Static CDN |
| `dashboard/DEVELOPMENT_DIARY.md` | In-app readable development diary | Vercel Static CDN |
| `dashboard/assets/` | Optimized WebP/PNG logos, icons, and web manifest | Vercel Static CDN |
| `vercel.json` | Vercel deployment configuration, clean URLs, and rewrites | Vercel Infrastructure |
| `deploy_to_github.sh` | Automated sync and push script to GitHub remote | Local Workspace |
| `export_website_package.py` | Bundling tool generating `website_production_package.zip` | Local Workspace |
| `storage/export_engine.py` | Reporting engine exporting CSV, JSON, and PDF reports | Local Analytics |
| `data/clickhouse_client.py` | ClickHouse time-series data client & GBM mock engine | Core Engine |
| `data/dynamodb_data_client.py` | AWS DynamoDB time-series and trade storage client | Core Engine |
| `paper_trading/engine.py` | Real-time Top 15/24 Paper Trading execution engine | Core Engine |
| `config.yaml` | System configuration, pairs, timeframes, and training hyperparams | Core Engine |

---

## 5. Live Deployment Verification

- **Remote Git Repository**: `https://github.com/cobaltitservices/Neurafloww.git`
- **Default Branch**: `main`
- **Build Status**: Automated Vercel Edge build and deployment triggered on push.
- **GCP Status**: All SSH and deployment scripts to `34.170.186.204` are permanently decommissioned.


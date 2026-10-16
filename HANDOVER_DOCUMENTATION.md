# NEURAFLOWW QUANTITATIVE SYSTEMS
# MASTER ARCHITECTURE & ENGINEERING HANDOVER MANUAL
**Document Version:** 4.0 PRO  
**Classification:** Institutional Confidential / Complete Knowledge Transfer  
**Author / Transition Notice:** Engineering Handover ("Leaving the Company" Standard)  
**Primary Repository:** [cobaltitservices/Neurafloww](https://github.com/cobaltitservices/Neurafloww.git)  
**Hosting Infrastructure:** Vercel Edge Serverless CDN  
**Database & Identity:** Supabase Serverless & ClickHouse Distributed Analytics  
**Date of Record:** October 16, 2026  

---

## Table of Contents
1. [Executive Summary & System Identity](#1-executive-summary--system-identity)
2. [Binance Data Pipeline & Market Ingestion](#2-binance-data-pipeline--market-ingestion)
3. [ClickHouse High-Throughput Analytics Engine](#3-clickhouse-high-throughput-analytics-engine)
4. [Backblaze B2 & Cold Storage Layer](#4-backblaze-b2--cold-storage-layer)
5. [AWS Cloud Infrastructure & DynamoDB Services](#5-aws-cloud-infrastructure--dynamodb-services)
6. [Google Cloud Platform (GCP) Legacy Compute & Storage](#6-google-cloud-platform-gcp-legacy-compute--storage)
7. [Salad Cloud Distributed GPU Acceleration](#7-salad-cloud-distributed-gpu-acceleration)
8. [Vercel Edge & Supabase Serverless Architecture](#8-vercel-edge--supabase-serverless-architecture)
9. [Deep Learning Model Zoo (6 Architectures, 1,824-2,400 Models)](#9-deep-learning-model-zoo)
10. [Paper Trading Engine & Autonomous Execution Matrix](#10-paper-trading-engine--autonomous-execution-matrix)
11. [Complete Codebase & File Tree Inventory](#11-complete-codebase--file-tree-inventory)
12. [Chronological Changelog & Iteration History](#12-chronological-changelog--iteration-history)
13. [Operator Runbooks & Disaster Recovery](#13-operator-runbooks--disaster-recovery)

---

## 1. Executive Summary & System Identity

### 1.1 Platform Mission
**Neurafloww** (historically codenamed *Flow Tester Pro*) is an enterprise quantitative cryptocurrency training platform, vectorized backtesting matrix, and autonomous execution terminal. The platform was created to eliminate human emotional bias from crypto trading by orchestrating continuous training, rigorous validation, and live paper trading across 1,824 to 2,400 discrete deep learning models.

### 1.2 Quantitative Scope
- **Cryptocurrency Universe:** 18 liquid cryptocurrency assets (Layer 1, DeFi, and high-volume utility tokens).
- **Timeframe Resolutions:** 16 distinct multi-resolution candles ranging from 1 second to 1 month.
- **Deep Learning Zoo:** 6 neural architectures (LSTM, GRU, TCN, Time-Series Transformer, CNN-LSTM, MLP-Mixer).
- **Evaluation Matrix:** $18 \text{ pairs} \times 16 \text{ timeframes} \times 6 \text{ architectures} = 1,728$ baseline models, expanded to 1,824 to 2,400 models with hyperparameter variations.
- **Execution Engine:** Real-time top 15/24 model selection streaming live price ticks with simulated taker fee (0.04%) and slippage penalty (0.01%).

---

## 2. Binance Data Pipeline & Market Ingestion

The lifeblood of Neurafloww is its multi-tiered ingestion pipeline fed directly from the world's most liquid crypto exchange: Binance.

### 2.1 The 18 Approved Cryptocurrency Pairs
The system monitors and models 18 institutional pairs denominated in USDT:
1. `BTC_USDT`: Bitcoin (Market Leader / Macro Baseline)
2. `ETH_USDT`: Ethereum (Smart Contract Mega-Cap)
3. `SOL_USDT`: Solana (High-Throughput Layer 1)
4. `BNB_USDT`: Binance Coin (Ecosystem Benchmark)
5. `XRP_USDT`: Ripple (Cross-Border Liquidity)
6. `ADA_USDT`: Cardano (Proof-of-Stake Baseline)
7. `AVAX_USDT`: Avalanche (Subnet Architecture)
8. `DOGE_USDT`: Dogecoin (High-Volatility Liquidity Proxy)
9. `DOT_USDT`: Polkadot (Interoperability Protocol)
10. `LINK_USDT`: Chainlink (Decentralized Oracle Network)
11. `NEAR_USDT`: NEAR Protocol (AI / Sharded Layer 1)
12. `SUI_USDT`: Sui Network (Move-based Layer 1)
13. `PEPE_USDT`: Pepe (Meme Momentum Volatility)
14. `SHIB_USDT`: Shiba Inu (High-Volume Speculative)
15. `FLOKI_USDT`: Floki (Momentum & Gaming Ecosystem)
16. `BONK_USDT`: Bonk (Solana Ecosystem Liquidity)
17. `LTC_USDT`: Litecoin (Legacy Proof-of-Work)
18. `ATOM_USDT`: Cosmos (Inter-Blockchain Communication)

### 2.2 The 16 Discrete Timeframe Resolutions
The pipeline ingests and resamples time-series data across 16 temporal horizons:
`1s`, `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`.

### 2.3 Protocols & Ingestion Architecture
1. **REST Historical Klines (`/api/v3/klines`):**
   - Base URL: `https://api.binance.com`
   - Parameters: `symbol`, `interval`, `startTime`, `endTime`, `limit=1000`.
   - Rate Limit Budget: 1,200 weight units/min. Implemented backoff with jitter in `data/preprocessing.py`.
2. **REST Batch Ticker Snapshot (`/api/v3/ticker/price`):**
   - High-density single-call query returning all symbols in 1 HTTP payload.
   - Built an in-memory 1.0-second TTL cache in `paper_trading/engine.py` via `fetch_all_binance_prices()` to prevent rate-limit bans during high-frequency paper trading loops.
3. **WebSocket Live Streams (`wss://stream.binance.com:9443`):**
   - Combined stream endpoint: `wss://stream.binance.com:9443/stream?streams=<pair>@ticker/<pair>@kline_<tf>`
   - Threaded listener maintaining ping/pong keepalives every 180 seconds.
4. **13-Dimensional Feature Engineering Vector:**
   From raw Binance OHLCV candles, the pipeline computes:
   - Primary Price Action: `open`, `high`, `low`, `close`, `volume`.
   - Moving Averages: `ma_fast` (10-period EMA), `ma_slow` (30-period SMA).
   - Momentum Delta: `ma_crossover` ($\text{EMA}_{10} - \text{SMA}_{30}$).
   - Volatility Envelope: `bb_upper` ($+2\sigma$), `bb_lower` ($-2\sigma$).
   - Relative Range: `bb_percent_b` ($\frac{\text{Close} - \text{Lower}}{\text{Upper} - \text{Lower}}$), `bb_bandwidth` ($\frac{\text{Upper} - \text{Lower}}{\text{SMA}} \times 100$).
   - Trend Orientation: `sar_trend` (Parabolic Stop and Reverse relative distance).

---

## 3. ClickHouse High-Throughput Analytics Engine

### 3.1 Purpose & Role
ClickHouse serves as the primary time-series analytical columnar database, optimized to query millions of historical financial ticks with sub-second response times.

### 3.2 Host & Connectivity Details
- **Host Endpoint:** `34.132.233.162`
- **HTTP Port:** `8123`
- **Native TCP Port:** `9000`
- **Default Database:** `crypto_data`
- **Primary Table:** `ohlcv_data`
- **Authentication:** Configured via `config/settings.py` (`ClickHouseConfig`).

### 3.3 Database Schema & Partitioning Strategy
```sql
CREATE DATABASE IF NOT EXISTS crypto_data;

CREATE TABLE IF NOT EXISTS crypto_data.ohlcv_data (
    timestamp DateTime CODEC(DoubleDelta, LZ4),
    symbol LowCardinality(String),
    timeframe LowCardinality(String),
    open Float64 CODEC(Gorilla, ZSTD(1)),
    high Float64 CODEC(Gorilla, ZSTD(1)),
    low Float64 CODEC(Gorilla, ZSTD(1)),
    close Float64 CODEC(Gorilla, ZSTD(1)),
    volume Float64 CODEC(Gorilla, ZSTD(1))
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
PRIMARY KEY (symbol, timeframe, timestamp)
ORDER BY (symbol, timeframe, timestamp)
SETTINGS index_granularity = 8192;
```

### 3.4 Python Client Implementation (`data/clickhouse_client.py`)
- Employs `clickhouse-connect` driver for vectorized streaming into Pandas DataFrames.
- **Fail-Safe Mock Engine:** If ClickHouse is unreachable (e.g. during local offline development or server migration), `ClickHouseDataClient` automatically switches to `generate_mock_data()` using Geometric Brownian Motion (GBM) with volatility drift:
  $$S_t = S_0 \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t \right)$$
  This guarantees that training jobs and test suites never throw unhandled connection exceptions.

---

## 4. Backblaze B2 & Cold Storage Layer

### 4.1 Architecture & Role
Backblaze B2 acts as our low-cost, institutional cold-storage repository for:
1. Historical raw Binance tick archives converted to Snappy-compressed Apache Parquet format.
2. Checkpoint weights (`.pt` / `.pth`) for all 1,824+ deep learning models.
3. Finalized audit reports, backtest result dumps, and master PDFs.

### 4.2 Storage Economics & Comparison
- **Backblaze B2 Storage Cost:** \$0.005 per GB / month (compared to AWS S3 standard at \$0.023 per GB / month, an 78% cost saving).
- **Egress:** Free egress when routed through Cloudflare Bandwidth Alliance.

### 4.3 S3-Compatible API Configuration
Backblaze B2 exposes an S3-compatible API allowing seamless operation using standard `boto3` or `rclone`:
```python
import boto3

b2_client = boto3.client(
    "s3",
    endpoint_url="https://s3.us-west-004.backblazeb2.com",
    aws_access_key_id=os.getenv("B2_KEY_ID"),
    aws_secret_access_key=os.getenv("B2_APPLICATION_KEY"),
)
```

### 4.4 Bucket Directory Topology
- `b2://neurafloww-cold-storage/parquet_ticks/{PAIR}/{YEAR}/{MONTH}.parquet`
- `b2://neurafloww-model-checkpoints/{ARCHITECTURE}/{PAIR}_{TIMEFRAME}_model.pt`
- `b2://neurafloww-reports/{TIMESTAMP}_master_audit.pdf`

---

## 5. AWS Cloud Infrastructure & DynamoDB Services

### 5.1 Elastic Compute Cloud (EC2) Instance Profiles
During training and backtest scaling, multiple EC2 machine tiers were provisioned and tested:
1. **`c5.9xlarge` (36 vCPUs, 72 GB RAM):**
   - High-throughput parallel CPU training node.
   - Script: `setup_aws_c5.sh`, Config: `config.c5.9xlarge.yaml`.
   - Kernel optimizations: `net.core.somaxconn=1024`, `vm.max_map_count=262144`.
2. **`c7i.16xlarge` (64 vCPUs, 128 GB RAM):**
   - Ultra-scale matrix evaluation across 1,824 model permutations.
   - Script: `setup_aws_c7i.sh`, Config: `config.c7i.16xlarge.yaml`.
3. **`g5.xlarge` / `g4dn.xlarge` (NVIDIA A10G / T4 GPUs):**
   - CUDA training acceleration for Transformer and CNN-LSTM architectures.
   - Script: `setup_aws_g5.sh`, Config: `config.g5.yaml`.
4. **`t3.medium` (2 vCPUs, 4 GB RAM):**
   - Lightweight testing and staging bastion.
   - Script: `setup_aws_t3.sh`, Config: `config.t3.medium.yaml`.

### 5.2 AWS DynamoDB Table Architecture
Managed via `data/dynamodb_data_client.py` and `storage/dynamodb_manager.py`:
1. `PaperTradingTrades`: Stores live simulated trade records (Trade ID, Job ID, Pair, Side, Entry Price, Exit Price, Realized PnL, Return %, Timestamp).
2. `PaperTradingTicks`: High-frequency streaming ticker telemetry log.
3. `PaperTradingSessions`: Active bot session states, peak equity, and drawdown metrics.
4. `CryptoHistoricalPrices`: Key-value cache for historical OHLCV data.

---

## 6. Google Cloud Platform (GCP) Legacy Compute & Storage

### 6.1 Legacy VM Cluster (`34.170.186.204` / `34.132.233.162`)
- **System Stack:** Ubuntu 22.04 LTS, Nginx reverse proxy, FastAPI server running on port 8000 managed via Systemd service (`ai-training-agent.service`).
- **GPU Training Instance:** `instance-training-gpu` equipped with NVIDIA L4 GPU via `launch_and_run_gpu_training.py`.

### 6.2 Google Cloud Storage (GCS) Buckets
- `gs://ai-trading-bot-logs-bucket`: Real-time streaming system logs managed via `data/gcp_logger.py`.
- `gs://models-2400-dataset-bucket`: Hierarchical dataset repository organized by:
  - `full_exports/`: Complete CSV/JSON dumps of 2,400 models.
  - `by_crypto_pair/{PAIR}/`: Individual pair datasets.
  - `by_architecture/{MODEL}/`: Model family groupings.
  - `by_timeframe/{TF}/`: Timeframe subfolders.
- `gs://flow-tester-logs-storage`: Staging dumps for distributed GPU workers.

### 6.3 Why & How GCP Was Decommissioned
- **The Problem:** The persistent GCP VM suffered from single-point-of-failure vulnerabilities, recurrent SSH port 22 connection timeouts, and recurring monthly cloud costs ($200-$400/month) even when idle.
- **The Solution:** Permanently migrated the web terminal, API, and backtest results to Vercel Serverless Edge CDN and Supabase. The legacy GCP instance `34.170.186.204` was formally retired.

---

## 7. Salad Cloud Distributed GPU Acceleration

### 7.1 Distributed GPU Worker Fleet
To train all 1,824+ models with CUDA acceleration without incurring high AWS GPU costs, we integrated **Salad Cloud**:
- **Hardware:** Consumer RTX 3080, RTX 3090, RTX 4090, and A100 GPUs.
- **Cost Efficiency:** \$0.15 - \$0.25 / hr per GPU node (85% cheaper than AWS EC2 G5 instances).
- **Deployment Script:** `deploy_salad_cloud.py` & `deploy_to_salad_api.py`.
- **Worker Container:** `Dockerfile.salad` runs PyTorch CUDA with automatic GCS dataset synchronization via `train_on_salad_gcs.py`.

---

## 8. Vercel Edge & Supabase Serverless Architecture

### 8.1 Production Deployment Setup
- **Public Git Repository:** `https://github.com/cobaltitservices/Neurafloww.git`
- **Production Host:** Vercel Global Edge CDN
- **Configuration (`vercel.json`):**
  - Framework: `null` (pure static high-performance bundle)
  - Clean URLs enabled
  - Route rewrites directing root requests to `/dashboard/index.html`
  - Asset cache control: 1-year immutable caching for static logos and icons.
- **Continuous Deployment:** Every git push via `./deploy_to_github.sh` triggers an automated Vercel Edge build and deployment in sub-20 seconds.

### 8.2 Database & Telemetry (Supabase)
- Replaces legacy SQLite/Postgres server instances with serverless database endpoints for visitor logs, session metrics, and campaign telemetry.

---

## 9. Deep Learning Model Zoo

Neurafloww deploys 6 specialized neural network architectures designed for sequential financial time-series forecasting:

### 9.1 Model Architectures
1. **Model 1 (`model_1_lstm` - MultiLayerLSTM):**
   - 2-layer stacked LSTM network with 0.2 dropout.
   - Captures persistent macro trends and long-term sequential dependencies.
2. **Model 2 (`model_2_gru` - ResidualGRU):**
   - Gated Recurrent Unit with Layer Normalization and residual skip connections.
   - Optimized for fast convergence and rapid inference during regime shifts.
3. **Model 3 (`model_3_tcn` - TemporalConvNet):**
   - 1D Temporal Convolutional Network with dilated causal convolutions.
   - Provides exponentially receptive temporal fields without gradient decay.
4. **Model 4 (`model_4_transformer` - TimeSeriesTransformer):**
   - Multi-Head Self-Attention ($h=4$) with sinusoidal positional encodings.
   - Identifies non-local, cross-temporal market dependencies.
5. **Model 5 (`model_5_cnnlstm` - CNNLSTMHybrid):**
   - 1D CNN feature extraction layer feeding into LSTM sequential units.
   - Simultaneously isolates high-frequency micro-patterns and macro momentum.
6. **Model 6 (`model_6_mlp_mixer` - MLPMixer / N-BEATS):**
   - Token-Mixing and Channel-Mixing MLPs operating with linear complexity $\mathcal{O}(N)$.
   - Delivers ultra-low latency inference suitable for sub-second execution.

### 9.2 Zero Data-Leakage Training Methodology
- **Strict Chronological Split:** 70% Training, 15% Validation, 15% Out-of-Sample Testing.
- **Zero Lookahead:** No random shuffling. Feature normalization scalers (`StandardScaler`) are fit strictly on the 70% train split and applied out-of-sample to validation and test splits.
- **Loss & Optimizer:** Huber Loss (smooth L1) for outlier robustness, AdamW optimizer with cosine annealing learning rate scheduler.

---

## 10. Paper Trading Engine & Autonomous Execution Matrix

### 10.1 Real-Time Execution Rules (`paper_trading/engine.py`)
- **Initial Portfolio Value:** \$10,000 USD virtual equity.
- **Top 15 / Top 24 Matrix:** The top performing neural models from the backtest leaderboard are automatically assigned to parallel live paper trading bots.
- **Institutional Fee Deduction:** 0.04% taker fee deducted on every simulated order.
- **Slippage Modeling:** 0.01% penalty simulated based on order book depth.
- **Dynamic Risk Controls:** Position sizing capped at 20% of net equity per trade; maximum stop-loss threshold enforced at 2.5%.

---

## 11. Complete Codebase & File Tree Inventory

```
neurafloww/
├── .env.example                        # Template environment variables
├── .gitignore                          # Git exclusions (venv, weights, logs)
├── config.yaml                         # Active system runtime configuration
├── config.c5.9xlarge.yaml              # AWS CPU cluster configuration
├── config.c7i.16xlarge.yaml             # AWS High-throughput configuration
├── config.g5.yaml                      # AWS GPU configuration
├── config.t3.medium.yaml               # Lightweight staging configuration
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Standard container specification
├── Dockerfile.salad                    # Salad Cloud CUDA GPU container spec
├── vercel.json                         # Vercel Serverless Edge configuration
├── deploy_to_github.sh                 # One-click automated Git & Vercel deployment tool
├── export_website_package.py           # Bundler for production website package zip
├── HANDOVER_DOCUMENTATION.md           # Master Handover Documentation (this document)
├── DEVELOPMENT_DIARY.md                # Engineering development log & changelog
│
├── api/
│   ├── server.py                       # FastAPI REST API & visitor telemetry server
│   └── __init__.py
│
├── config/
│   ├── settings.py                     # Pydantic configuration schemas & env loaders
│   └── __init__.py
│
├── data/
│   ├── clickhouse_client.py            # ClickHouse client & synthetic GBM data engine
│   ├── dynamodb_data_client.py         # AWS DynamoDB time-series client
│   ├── gcp_logger.py                   # GCP Cloud Logging & GCS bucket sync utility
│   ├── preprocessing.py                # Chronological leak-free data splitters & scalers
│   ├── validator.py                    # Schema, NaN, Inf, and timestamp gap validator
│   └── __init__.py
│
├── models/
│   ├── base_model.py                   # PyTorch abstract neural base class
│   ├── model_1_lstm.py                 # Multi-Layer LSTM architecture
│   ├── model_2_gru.py                  # Residual GRU architecture
│   ├── model_3_tcn.py                  # Temporal Convolutional Network
│   ├── model_4_transformer.py          # Time-Series Self-Attention Transformer
│   ├── model_5_cnnlstm.py              # Hybrid Spatial-Temporal CNN-LSTM
│   ├── model_6_mlp_mixer.py            # Token/Channel Mixing MLP
│   ├── registry.py                     # Model dynamic factory registry
│   └── __init__.py
│
├── orchestration/
│   ├── job_db.py                       # SQLite WAL task queue & state machine
│   ├── resource_manager.py             # CPU core, RAM, and GPU VRAM isolation manager
│   └── __init__.py
│
├── paper_trading/
│   ├── engine.py                       # Live Top 15/24 Paper Trading Engine
│   └── __init__.py
│
├── storage/
│   ├── dynamodb_manager.py             # DynamoDB trade persistence manager
│   ├── export_engine.py                # Multi-format report exporter (CSV, JSON, PDF)
│   ├── firestore_manager.py            # GCP Firestore persistence adapter
│   └── __init__.py
│
├── dashboard/
│   ├── index.html                      # Single Page Application (UI, CSS & JS)
│   ├── 404.html                        # Branded 404 error page
│   ├── DEVELOPMENT_DIARY.md            # In-app readable development diary
│   └── assets/                         # Web manifest, icons, and logos
│
└── tests/
    ├── test_clickhouse.py              # ClickHouse connectivity & mock tests
    ├── test_pipeline.py                # End-to-end training pipeline tests
    └── test_validation.py              # Data validator tests
```

---

## 12. Chronological Changelog & Iteration History

1. **Initial Genesis:** Built ClickHouse ingestion client, data validator, and synthetic time-series engine.
2. **Model Zoo Deployment:** Implemented all 6 PyTorch neural network architectures with early stopping and AMP (`torch.cuda.amp`).
3. **Multiprocess Scheduler:** Created SQLite WAL queue (`jobs.db`) with automatic crash recovery and process thread pinning.
4. **Vectorized Backtesting Engine:** Evaluated Sharpe, Sortino, Max Drawdown, and Win Rate across 1,824 strategy permutations.
5. **Real-Time Paper Trading:** Built Top 15/24 parallel background worker matrix with live Binance REST and WebSocket price streams.
6. **Web Terminal Design:** Crafted Bloomberg-inspired cyber-slate dark mode interface in `dashboard/index.html` with TradingView integration.
7. **Multi-Cloud Testing:** Benchmarked across AWS EC2 (`c5.9xlarge`, `c7i.16xlarge`, `g5.xlarge`), DynamoDB, GCP VM (`34.170.186.204`), GCS buckets, and Salad Cloud distributed GPU nodes.
8. **Serverless Migration:** Decommissioned GCP VM in favor of zero-maintenance Vercel Edge Serverless hosting and Supabase database.
9. **UI & Usability Enhancements:** Added password visibility toggles, UTM tracking and campaign builder, scroll progress bar, universal site search (`Cmd+K`), and sticky table headers.
10. **Rebranding to Neurafloww:** Uniform platform rename across sidebar, metadata, documentation, and manifest.
11. **Admin Development Diary:** Integrated real-time searchable diary and handover documentation directly into the Admin dashboard.

---

## 13. Operator Runbooks & Disaster Recovery

### 13.1 Deploying Code Changes to Production
To push any code, UI, or documentation updates directly to GitHub and trigger instant Vercel redeployment:
```bash
./deploy_to_github.sh "feat: description of changes"
```

### 13.2 Running Local Verification
To test the web terminal locally:
```bash
cd dashboard
python3 -m http.server 3000
# Open http://localhost:3000 in your browser
```

### 13.3 Executing a Model Training Run
```bash
# Run training across configured pairs and timeframes
python3 agent.py train --pairs BTC_USDT ETH_USDT --timeframes 1h 4h --models model_1_lstm model_4_transformer
```

### 13.4 Running Vectorized Backtests
```bash
python3 run_backtest.py
python3 continuous_backtest_daemon.py
```

### 13.5 Starting the Live Paper Trading Daemon
```bash
python3 auto_paper_trading_daemon.py
```

### 13.6 Admin Credentials & Emergency Access
- **Default Admin Username:** `admin`
- **Default Admin Password:** `admin`
- **Password Customization:** Changes made via the Admin Dashboard's Change Password modal are stored persistently in browser `localStorage`.
- **Resetting Password:** Clear browser cache / `localStorage` or edit `ADMIN_PASSWORD` in `api/server.py` and redeploy.

---
*End of Master Handover Document. Handed over in full working order.*

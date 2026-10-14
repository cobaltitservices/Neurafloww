# AI Training Agent for Financial Time-Series Data

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-DBMS-FFCC00?style=for-the-badge&logo=clickhouse&logoColor=black)](https://clickhouse.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

A production-grade, distributed-ready AI training agent system that automatically ingests financial time-series data from **ClickHouse**, generates and orchestrates **1,824+ independent training jobs** (19 trading pairs × 16 timeframes × 6 neural network models), and trains them in parallel with resource-aware scheduling, zero data leakage protection, fault-tolerant crash recovery, real-time web dashboard monitoring, and REST API controls.

---

## 📐 System Architecture Diagram

```
                               +-----------------------------+
                               |    ClickHouse Database      |
                               +--------------+--------------+
                                              |
                                              v
+-----------------------------------------------------------------------------------+
|                            DATA DISCOVERY & VALIDATOR                             |
|  - Schema Inspection (Pairs, Timeframes, Target, OHLCV)                           |
|  - Quality Checks (Missing Data, Time Gaps, NaNs, Infs, Insufficient Rows)        |
+-------------------------------------+---------------------------------------------+
                                      | Validated Data Stream
                                      v
+-----------------------------------------------------------------------------------+
|                                   JOB GENERATOR                                   |
|  - Creates 1,824+ Unique Job Specs (PAIR_TF_MODEL_HASH)                           |
|  - Persists specs to SQLite Job DB (State: PENDING)                               |
+-------------------------------------+---------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------------+
|                        RESOURCE-AWARE ORCHESTRATOR / SCHEDULER                    |
|  - Resumability Engine (Recovers interrupted/failed jobs on startup)              |
|  - Resource Telemetry (CPU Cores, RAM GB, GPU VRAM, GPU Util)                     |
|  - Queue Dispatcher (Dispatches job iff resources permit)                         |
+---------------+---------------------+-----------------------------+---------------+
                |                     |                             |
                v                     v                             v
     +-------------------+   +-------------------+       +-------------------+
     | Worker Process 1  |   | Worker Process 2  |  ...  | Worker Process N  |
     | (CPU Thread Limit |   | (CPU Thread Limit |       | (CPU Thread Limit |
     |  & VRAM Isolation)|   |  & VRAM Isolation)|       |  & VRAM Isolation)|
     +---------+---------+   +---------+---------+       +---------+---------+
               |                       |                           |
               +-----------------------+---------------------------+
                                       | Job Pipelines
                                       v
+-----------------------------------------------------------------------------------+
|                                TRAINING PIPELINE                                  |
|  1. ClickHouse Batch Load    5. PyTorch Model Instance (6 Architectures)          |
|  2. Chronological Split      6. Training Loop (AMP, Early Stop, Checkpointing)    |
|  3. Data Scaler (No Leak)    7. Evaluation (ML Metrics & Financial Metrics)        |
|  4. Sliding Windowing        8. Save Artifacts & Update SQLite Status              |
+-------------------------------------+---------------------------------------------+
                                      |
        +-----------------------------+-----------------------------+
        |                                                           |
        v                                                           v
+-------------------------------+                       +-------------------------------+
|      ARTIFACT & METRICS       |                       |        CONTROL SYSTEM         |
|  - Checkpoints & Models       |                       |  - CLI Interface (agent.py)   |
|  - Evaluation JSON Metrics    |                       |  - FastAPI Backend Server     |
|  - Structured Job Logs        |                       |  - Web Monitoring Dashboard   |
+-------------------------------+                       +-------------------------------+
```

---

## ✨ Key Features & Capabilities

- **Massive Scalability (1,824+ Jobs)**: Automatically generates and manages training combinations for 19 trading pairs across 16 timeframes and 6 neural network models.
- **ClickHouse Native Ingestion & Mock Engine**: Native SQL query engine (`clickhouse-connect`) with parameterized batching + embedded synthetic financial data generator for offline execution and testing without a live database.
- **Zero Data Leakage Pipeline**: Strict time-ordered chronological splitting (70% train / 15% val / 15% test) without shuffling. Normalization scalers are fit **exclusively** on the training set.
- **6 Deep Neural Network Architectures**:
  1. `model_1_lstm`: Multi-Layer LSTM Network
  2. `model_2_gru`: LayerNorm Residual GRU Architecture
  3. `model_3_tcn`: 1D Temporal Convolutional Network (TCN) with Dilated Causal Convolutions
  4. `model_4_transformer`: Time-Series Transformer with Positional Encoding & Multi-Head Self-Attention
  5. `model_5_cnnlstm`: Spatial-Temporal CNN-LSTM Hybrid Architecture
  6. `model_6_mlp_mixer`: N-BEATS / MLP-Mixer Deep Linear Forecasting Architecture
- **Resource-Aware Scheduler**: Hardware telemetry monitor (`psutil` & CUDA/NVML) preventing CPU oversubscription and GPU VRAM exhaustion. Enforces per-job thread limits (`torch.set_num_threads`).
- **Resumability & Crash Recovery**: SQLite WAL-backed metadata queue tracks job state transitions. Interrupted or crashed jobs automatically resume upon system restart.
- **Comprehensive Financial Evaluation**: Calculates standard ML loss metrics (MSE, MAE, RMSE, R²) and financial trading metrics (Directional Accuracy, Cumulative Return, Sharpe Ratio, Max Drawdown, Win Rate, Profit Factor).
- **Cyber-Slate Web Dashboard & API**: Real-time glassmorphism web UI (`http://localhost:8000`) and interactive Swagger OpenAPI docs (`http://localhost:8000/docs`).
- **Docker & GPU Support**: Production container setup with NVIDIA GPU pass-through capability.

---

## 📁 Directory Structure

```
ai-training-agent/
├── agent.py                        # Master CLI control interface
├── config.yaml                     # Central system configuration
├── .env.example                    # Secrets & connection environment template
├── requirements.txt                # Production Python dependencies
├── Dockerfile                      # Container specification
├── docker-compose.yml              # Docker stack orchestration
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Pydantic & YAML config loader
│
├── data/
│   ├── __init__.py
│   ├── clickhouse_client.py        # ClickHouse client & mock data generator
│   ├── validator.py                # Data quality & schema discovery validator
│   └── preprocessing.py            # Chronological splitter & feature scaler
│
├── models/
│   ├── __init__.py
│   ├── base_model.py               # Abstract Base Class for neural models
│   ├── model_1_lstm.py             # Multi-layer LSTM model
│   ├── model_2_gru.py              # Residual GRU network
│   ├── model_3_tcn.py              # 1D Temporal Convolutional Network
│   ├── model_4_transformer.py      # Time-Series Transformer
│   ├── model_5_cnnlstm.py          # CNN-LSTM Hybrid
│   ├── model_6_mlp_mixer.py        # N-BEATS / MLP-Mixer
│   └── registry.py                 # Dynamic model registry mapping
│
├── training/
│   ├── __init__.py
│   ├── trainer.py                  # PyTorch training loop (AMP, early stop, LR sched)
│   ├── evaluator.py                # ML loss & financial trading evaluator
│   ├── checkpoint.py               # Checkpoint & artifact saving manager
│   └── pipeline.py                 # Single job execution pipeline
│
├── orchestration/
│   ├── __init__.py
│   ├── job_db.py                   # SQLite WAL queue & resumability engine
│   ├── resource_manager.py         # Hardware telemetry gatekeeper
│   ├── scheduler.py                # Multi-process parallel job scheduler
│   └── worker.py                   # Worker process wrapper with retry backoff
│
├── tracking/
│   ├── __init__.py
│   └── experiment_tracker.py       # Metrics logger & optional MLflow integration
│
├── storage/
│   ├── __init__.py
│   └── artifact_manager.py         # Local & cloud artifact storage manager
│
├── api/
│   ├── __init__.py
│   └── server.py                   # FastAPI REST backend server
│
├── dashboard/
│   └── index.html                  # Single-page Glassmorphism Web UI
│
└── tests/                          # Automated PyTest test suite
    ├── test_clickhouse.py
    ├── test_validation.py
    ├── test_models.py
    ├── test_pipeline.py
    ├── test_orchestration.py
    └── test_api.py
```

---

## ⚡ Quickstart Guide

### 1. Installation & Environment Setup

Clone the repository and create a Python 3.10+ virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run Automated Test Suite

Verify that all unit and integration tests pass:

```bash
pytest -v
```

### 3. Run MVP Mode (Single Job Verification)

Executes 1 single training job end-to-end to verify data extraction, feature scaling, model training, evaluation, and artifact saving:

```bash
python agent.py start --mvp
```

### 4. Launch Full Production Parallel System

Generates the **1,824 training job matrix** and launches the resource-aware worker process pool:

```bash
python agent.py start
```

### 5. Launch Web Dashboard & REST API

Start the FastAPI server at `http://localhost:8000`:

```bash
python agent.py dashboard --port 8000
```

- **Web Dashboard**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Configuration & Credentials

All infrastructure and hyperparameter settings are controlled via `config.yaml` and `.env`.

### `config.yaml` Overview

```yaml
clickhouse:
  host: "localhost"
  port: 8123
  user: "default"
  password: ""
  database: "crypto_data"
  table: "ohlcv_data"
  secure: false
  use_mock: true  # Set to false for live ClickHouse DB connection

pairs:
  - "BTC_USDT"
  - "ETH_USDT"
  - "SOL_USDT"
  - "BNB_USDT"
  - "XRP_USDT"
  - "ADA_USDT"
  - "DOGE_USDT"
  - "AVAX_USDT"
  - "DOT_USDT"
  - "LINK_USDT"
  - "MATIC_USDT"
  - "NEAR_USDT"
  - "LTC_USDT"
  - "ATOM_USDT"
  - "UNI_USDT"
  - "APT_USDT"
  - "OP_USDT"
  - "ARB_USDT"
  - "SUI_USDT"

timeframes:
  - "1s"
  - "1m"
  - "3m"
  - "5m"
  - "15m"
  - "30m"
  - "1h"
  - "2h"
  - "4h"
  - "6h"
  - "8h"
  - "12h"
  - "1d"
  - "3d"
  - "1w"
  - "1M"

models:
  - "model_1_lstm"
  - "model_2_gru"
  - "model_3_tcn"
  - "model_4_transformer"
  - "model_5_cnnlstm"
  - "model_6_mlp_mixer"

training:
  max_concurrent_jobs: 4
  epochs: 10
  batch_size: 128
  learning_rate: 0.001
  lookback_window: 60
  prediction_horizon: 1
  train_ratio: 0.70
  validation_ratio: 0.15
  test_ratio: 0.15
  early_stopping_patience: 3
  use_amp: true

resources:
  cpu_limit_per_job: 2
  ram_limit_per_job_gb: 4.0
  gpu_limit_per_job: 1.0
  max_cpu_percent: 85.0
  max_ram_percent: 85.0
  max_gpu_vram_percent: 85.0

retry:
  max_retries: 3
  backoff_factor: 2.0
  initial_delay_seconds: 5.0
```

### Environment Secrets (`.env`)

Copy `.env.example` to `.env` to configure sensitive production credentials:

```bash
cp .env.example .env
```

```env
CLICKHOUSE_HOST=your-clickhouse-host.domain
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=your_user
CLICKHOUSE_PASSWORD=your_secure_password
CLICKHOUSE_DATABASE=crypto_data
CLICKHOUSE_TABLE=ohlcv_data

ARTIFACT_STORAGE_PATH=./artifacts
DATABASE_URL=sqlite:///./jobs.db
```

---

## 🛠️ CLI Command Reference

The master CLI agent (`agent.py`) provides commands for controlling and inspecting the training system:

```bash
# Check queue status, completed counts, and hardware telemetry
python agent.py status

# Generate performance ranking report across completed models and pairs
python agent.py report

# Reset all failed jobs back to PENDING state for auto-retry
python agent.py retry-failed

# Start FastAPI Web Dashboard server
python agent.py dashboard --host 0.0.0.0 --port 8000
```

---

## 🔌 Connecting to a Live ClickHouse Database

1. Set `use_mock: false` in `config.yaml` or set environment variable `CLICKHOUSE_USE_MOCK=false`.
2. Provide connection parameters in `.env`:
   ```env
   CLICKHOUSE_HOST=192.168.1.100
   CLICKHOUSE_PORT=8123
   CLICKHOUSE_USER=analytics_reader
   CLICKHOUSE_PASSWORD=supersecretpassword
   CLICKHOUSE_DATABASE=market_data
   CLICKHOUSE_TABLE=crypto_ohlcv
   ```
3. Ensure your ClickHouse table contains the following columns:
   - `timestamp` (DateTime / DateTime64)
   - `symbol` / `pair` (String)
   - `timeframe` (String)
   - `open`, `high`, `low`, `close`, `volume` (Float32 / Float64)

---

## 🧩 Adding New Neural Network Models

To add a new neural network architecture without rewriting the orchestration pipeline:

1. Create `model_7_custom.py` in `models/` inheriting from `BaseModel`:

   ```python
   import torch
   import torch.nn as nn
   from .base_model import BaseModel

   class Model7Custom(BaseModel):
       def __init__(self, input_dim: int, lookback_window: int, prediction_horizon: int = 1, **kwargs):
           super().__init__(input_dim, lookback_window, prediction_horizon, **kwargs)
           self.build_model()

       def build_model(self) -> None:
           self.network = nn.Sequential(
               nn.Linear(self.input_dim * self.lookback_window, 128),
               nn.ReLU(),
               nn.Linear(128, self.prediction_horizon)
           )

       def forward(self, x: torch.Tensor) -> torch.Tensor:
           flattened = x.reshape(x.size(0), -1)
           return self.network(flattened)
   ```

2. Register the new model in `models/registry.py`:

   ```python
   from .model_7_custom import Model7Custom
   register_model("model_7_custom", Model7Custom)
   ```

3. Add `"model_7_custom"` to the `models` list in `config.yaml`.

---

## 🐳 Docker Deployment

### Run Container Stack with Docker Compose

```bash
docker compose up -d
```

This starts:
- **`agent-dashboard`**: FastAPI server on port `8000`.
- **`agent-worker`**: Parallel worker scheduler process with GPU pass-through enabled.

---

## ☁️ Deploying on AWS EC2 `c5.9xlarge`

The AWS EC2 **`c5.9xlarge`** instance type provides **36 vCPUs** and **72 GB RAM** compute-optimized resources.

### Hardware Allocation for `c5.9xlarge`:
- **Worker Process Concurrency**: `max_concurrent_jobs: 16`
- **CPU Threads per Worker**: `cpu_limit_per_job: 2` (16 workers × 2 threads = 32 vCPUs, leaving 4 vCPUs for OS & API)
- **RAM Allocation**: `ram_limit_per_job_gb: 3.5` (16 workers × 3.5 GB = 56 GB RAM out of 72 GB)

### Deployment Steps on AWS:

1. Launch an EC2 Instance on AWS:
   - **Instance Type**: `c5.9xlarge`
   - **AMI**: Ubuntu 22.04 LTS (x86_64)
   - **Storage**: 100+ GB EBS GP3 volume
   - **Security Group**: Allow TCP port `8000` (Web Dashboard & API) and SSH port `22`.

2. SSH into your instance and clone repository:
   ```bash
   ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
   git clone <your-repo-url> ai-agent-for-training
   cd ai-agent-for-training
   ```

3. Run the automated AWS installer script:
   ```bash
   chmod +x setup_aws_c5.sh
   ./setup_aws_c5.sh
   ```

4. Start background systemd services:
   ```bash
   sudo systemctl start ai-training-agent
   sudo systemctl start ai-training-dashboard
   ```

5. Monitor execution & telemetry:
   ```bash
   # View system service status
   sudo systemctl status ai-training-agent

   # Stream live application logs
   journalctl -u ai-training-agent -f
   ```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

# QuantTrader - Reinforcement Learning Trading Agent

QuantTrader is a deep reinforcement learning agent that autonomously learns to trade stocks for maximum profit using historical and real-time market data. It leverages custom Gym environments and RLlib (Ray) to train, simulate, and optionally paper trade in real-time.

## 🌐 Features
- PPO-based stock trading agent
- Alpha Vantage integration for **historical and real-time data**
- Real-time data streaming support for paper/live trading
- Custom OpenAI Gym trading environment
- Reward shaping with transaction cost and portfolio tracking
- Modular codebase for training, inference, and evaluation
- Jupyter notebooks for EDA and visualization
- Config-driven setup for reproducibility

## 🛠 Tech Stack
- Python, PyTorch
- Ray + RLlib
- OpenAI Gym
- Alpha Vantage API
- Pandas, NumPy, Matplotlib
- YAML for config management
- Dotenv for API key security

## 📁 Project Structure
```
QuantTrader/
├── config/
│   ├── env.yaml              # Trading environment parameters (window size, cost)
│   ├── train.yaml            # RL training hyperparameters
│   └── logging.yaml          # Logging and output settings
├── data/
│   ├── historical/           # Pre-downloaded CSV data (for training)
│   └── raw/                  # Raw downloaded data files (if any)
├── notebooks/
│   ├── analysis.ipynb        # EDA and feature exploration
│   └── results_visualization.ipynb   # Visuals of training metrics
├── src/
│   ├── env/
│   │   ├── stock_trading_env.py   # Custom Gym-compatible environment
│   │   └── utils.py               # Performance metrics and helpers
│   ├── data/
│   │   └── data_pipeline.py       # Historical + real-time data loading
│   ├── agent/
│   │   └── model.py               # (Optional) custom neural network
│   ├── train.py                   # RLlib training script
│   └── run.py                     # Paper/live trading runner
├── tests/
│   └── test_environment.py       # Unit tests for env and data
├── .env                          # API keys and environment variables
├── requirements.txt              # Dependencies
└── README.md
```

## 🚀 Setup Instructions

### 1. Clone and Install
```bash
git clone https://github.com/pyourusername/QuantTrader.git
cd QuantTrader
pip install -r requirements.txt
```

### 2. Set your Alpha Vantage API key
Create a `.env` file in the root directory:
```
ALPHA_VANTAGE_API_KEY=your_key_here
CHECKPOINT_PATH=checkpoints/PPO/checkpoint_000020/checkpoint-20
```

### 3. Fetch Historical Stock Data
```bash
python src/data/data_pipeline.py
```

### 4. Run Real-Time Streaming (optional)
```bash
# Streams live prices (prints price every 60 seconds for 5 minutes)
python src/data/data_pipeline.py --stream
```

### 5. Train the Agent
```bash
python src/train.py
```

### 6. Evaluate or Paper Trade
```bash
python src/run.py
```

## 🧠 Agent Algorithm

- Uses **Proximal Policy Optimization (PPO)** from Ray RLlib.
- Custom Gym environment receives state of shape `[window_size, features]` including OHLCV and technical indicators.
- Action space: **Buy, Hold, Sell**.
- Reward includes: **Portfolio return - transaction cost**.

Hyperparameters and trading environment are easily adjustable in `config/train.yaml` and `config/env.yaml`.

## 📉 Visualization
Use the following notebook:
```bash
notebooks/results_visualization.ipynb
```
To visualize:
- Portfolio value over time
- Reward trends across episodes
- Action distribution (buy/sell/hold)

## 🧪 Testing
Run unit tests using:
```bash
pytest tests/
```
## 📦 Deployment
### Docker Support (Optional)
To containerize the project:

1. Build the Docker image:
```bash
docker build -t quanttrader .
```

2. Run a container:
```bash
docker run --env-file .env quanttrader
```

3. (Optional) Mount local data/ directory:
```bash
docker run -v $(pwd)/data:/app/data --env-file .env quanttrader
```

> Make sure to include your `.env` and downloaded data if required for the container to function correctly.

## 📄 License
MIT License

---

Made with ❤️ using PyTorch + Ray RLlib
```

# 🌙 nof1-agents - Autonomous Crypto Trading Bot

> **AI-powered autonomous trading inspired by [Nof1.ai](https://nof1.ai/) Alpha Arena**  
> Pure LLM decision-making + HyperLiquid perpetuals = Fully autonomous crypto trading

This project is a clone/implementation inspired by [Nof1.ai](https://nof1.ai/)'s Alpha Arena approach, where AI models make autonomous trading decisions based purely on technical analysis and market data.

---

## 🎯 What is This?

**nof1-agents** is an autonomous cryptocurrency trading system that uses Large Language Models (LLMs) to:
- Analyze real-time market data from HyperLiquid perpetuals exchange
- Make independent trading decisions (LONG/SHORT/CLOSE/HOLD)
- Execute trades automatically with risk management
- Track performance and log all reasoning

### How It Works

Every **5 minutes** (configurable), the AI:

1. **📊 Collects Data** - Account balance, positions, market data (OHLCV, indicators, funding rates)
2. **🤖 Analyzes** - Sends data to DeepSeek LLM with technical context
3. **🎯 Decides** - AI responds with trading decision + confidence + reasoning
4. **⚡ Executes** - If confidence ≥ 65%, executes trade on HyperLiquid
5. **📝 Logs** - Saves reasoning traces, trades, and performance

**Example AI Decision:**
```json
{
  "decision": "OPEN_LONG",
  "symbol": "BTC",
  "confidence": 0.88,
  "reasoning": "Strong uptrend, RSI recovering from oversold, MACD bullish crossover...",
  "position_size_usd": 9000,
  "leverage": 20,
  "stop_loss": 105000,
  "take_profit": 115000
}
```

---

## ⭐ Key Features

- **🤖 Pure LLM Trading** - No hard-coded rules, AI decides everything
- **📈 Multi-Asset** - Trade BTC, ETH, SOL, BNB, DOGE, XRP
- **⚡ High Leverage** - Up to 50x leverage on HyperLiquid (configurable)
- **🛡️ Risk Management** - Stop loss, take profit, position sizing, confidence thresholds
- **📊 Technical Analysis** - EMA, RSI, MACD, ATR, Bollinger Bands, Funding Rates
- **🔄 Modular Design** - Swap AI models easily (DeepSeek, Claude, GPT-4, Gemini)
- **📝 Complete Logging** - All reasoning, trades, and performance tracked
- **🎨 Nof1-Style Prompts** - Inspired by Alpha Arena's technical approach

---

## 🚀 Quick Start

### Prerequisites

**Python 3.10 Required** (due to dependency compatibility)

Check your Python version:
```bash
python3.10 --version
```

If you don't have Python 3.10, install it:

**macOS (Homebrew):**
```bash
brew install python@3.10
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev
```

**Windows:**  
Download from [python.org](https://www.python.org/downloads/release/python-3100/)

---

### 1. Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd nof1-agents

# Create virtual environment with Python 3.10
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Configure API Keys

```bash
# Copy environment template
cp env.example .env

# Edit .env with your actual keys
nano .env  # or use your preferred editor
```

**Required API Keys in `.env`:**

```bash
# Get DeepSeek API key from: https://platform.deepseek.com
DEEPSEEK_KEY=your_deepseek_api_key_here

# Your HyperLiquid Ethereum private key (NEVER SHARE THIS!)
HYPER_LIQUID_ETH_PRIVATE_KEY=0xyour_private_key_here

# Your HyperLiquid wallet address
HYPER_LIQUID_MASTER_ADDRESS=0xyour_wallet_address_here
```

**Where to Get Keys:**
- **DeepSeek API**: Sign up at [platform.deepseek.com](https://platform.deepseek.com)
- **HyperLiquid**: Use your existing Ethereum wallet's private key and address

⚠️ **SECURITY WARNING**: Never commit your `.env` file to Git! It's already in `.gitignore`.

---

### 3. Configure Trading Settings

Edit `agents/agent_configs.py` to customize your trading parameters:

```python
CONFIG = {
    'STARTING_CAPITAL_USD': 500,         # Your starting capital
    'SYMBOLS': ['BTC', 'ETH', 'SOL'],    # Coins to trade
    'MAX_LEVERAGE': 20,                   # Maximum leverage (1-50x)
    'MAX_POSITION_PERCENT': 90,          # Use 90% of capital per position
    'CHECK_INTERVAL_MINUTES': 3,          # How often to check (minutes)
    'MIN_CONFIDENCE_TO_TRADE': 0.65,      # Only trade if AI ≥65% confident
    'STOP_LOSS_PERCENT': 5.0,             # Auto-exit at -5% loss
    'TAKE_PROFIT_PERCENT': 10.0,          # Auto-exit at +10% gain
    'MODEL_NAME': 'deepseek-chat',        # AI model to use
    'TEMPERATURE': 0.7,                   # LLM creativity (0-1)
}
```

**💡 Recommended Starting Settings:**
```python
# For beginners - start with these safer settings:
CONFIG = {
    'STARTING_CAPITAL_USD': 100,         # Start small
    'SYMBOLS': ['BTC', 'ETH'],           # Just 2 coins
    'MAX_LEVERAGE': 5,                    # Low leverage!
    'CHECK_INTERVAL_MINUTES': 5,          # Less frequent
    'MIN_CONFIDENCE_TO_TRADE': 0.75,      # Higher confidence
}
```

**🎯 Quick Presets Available:**

You can use pre-configured presets in `agent_configs.py`:

- **`CONSERVATIVE_CONFIG`** - Lower risk
  - 10x leverage (vs 20x default)
  - 50% position size (vs 90%)
  - 75% confidence required (vs 65%)
  - 3% stop loss (tighter)

- **`AGGRESSIVE_CONFIG`** - Higher risk
  - 30x leverage (vs 20x default)
  - 95% position size (vs 90%)
  - 60% confidence required (vs 65%)
  - 7% stop loss (wider)

- **`MULTI_SYMBOL_CONFIG`** - Diversified
  - Trade 3 symbols simultaneously
  - 30% per symbol (90% total)
  - 5 minute intervals

---

### 4. Run the Trading Bot

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the trader
python agents/deepseek_trader.py

# Or use the standalone runner
python run.py
```

**You should see:**
```
🌙 DeepSeek Nof1 Trader - Alpha Arena Style
✅ DeepSeek ready: deepseek-chat
📋 DeepSeek Trader Configuration loaded
🚀 Starting Nof1 Trading Agent...
```

**Stop the bot:** Press `Ctrl+C`

---

## 📁 Project Structure

```
nof1-agents/
├── agents/                     # 🤖 Trading agent logic
│   ├── deepseek_trader.py      # Main trading bot (RUN THIS)
│   ├── base_pure_agent.py      # Base agent class
│   └── agent_configs.py        # ⚙️ Configuration (EDIT THIS)
│
├── models/                     # 🧠 LLM implementations
│   ├── model_factory.py        # Model selector
│   ├── deepseek_model.py       # DeepSeek integration
│   ├── claude_model.py         # Claude integration
│   ├── openai_model.py         # GPT integration
│   └── ...                     # Other models
│
├── exchange/                   # 💱 Exchange integrations
│   └── nice_funcs_hyperliquid.py  # HyperLiquid API wrapper
│
├── data_formatters/            # 📊 Data formatting
│   ├── market_data_formatter.py   # Market data + indicators
│   ├── position_formatter.py      # Position tracking
│   └── account_formatter.py       # Account metrics
│
├── prompts/                    # 💬 LLM prompts
│   └── nof1_style_prompt.py    # Nof1-inspired prompt format
│
├── requirements.txt            # 📦 Dependencies
├── env.example                 # 🔑 Environment template
├── run.py                      # 🚀 Standalone runner
└── README.md                   # 📖 This file
```

---

## ⚙️ Configuration Options

All settings in `agents/agent_configs.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `STARTING_CAPITAL_USD` | 500 | Your starting capital ($) |
| `SYMBOLS` | BTC, ETH, SOL, BNB, DOGE, XRP | Coins to trade |
| `MAX_LEVERAGE` | 20 | Maximum leverage (1-50x) |
| `MAX_POSITION_PERCENT` | 90 | % of capital per position |
| `CHECK_INTERVAL_MINUTES` | 3 | Check every N minutes |
| `MIN_CONFIDENCE_TO_TRADE` | 0.65 | Only trade when AI ≥65% confident |
| `STOP_LOSS_PERCENT` | 5.0 | Auto-exit at -5% loss |
| `TAKE_PROFIT_PERCENT` | 10.0 | Auto-exit at +10% gain |
| `MODEL_NAME` | deepseek-chat | LLM model to use |
| `TEMPERATURE` | 0.7 | LLM creativity (0-1) |

### Example: Conservative Trading

```python
from agents.deepseek_trader import DeepSeekTrader

trader = DeepSeekTrader(
    symbols=['BTC', 'ETH'],
    starting_capital_usd=100,
    max_leverage=10,           # Lower leverage
    min_confidence=0.75,       # Higher confidence required
    stop_loss_percent=3.0,     # Tighter stop loss
    check_interval_minutes=5   # Check less frequently
)

trader.run()
```

---

## 📊 Logs & Performance Tracking

All data saved to `src/data/nof1_agents/`:

### 📝 Reasoning Traces
```
src/data/nof1_agents/reasoning/deepseek_2025-10-27.txt
```
Contains full AI reasoning for every decision:
```
[2025-10-27 14:32:15] DEEPSEEK REASONING TRACE
DECISION: OPEN_LONG BTC
CONFIDENCE: 88%

REASONING:
Strong bullish momentum observed:
1. Price broke above 20-EMA with conviction
2. RSI at 45, recovering from oversold
3. MACD showing bullish crossover
4. Funding rate slightly negative (long opportunity)
5. Volume increasing on upward moves

TRADE PARAMETERS:
- Entry: $111,113.50
- Position: $9,000 (20x leverage)
- Stop Loss: $105,000
- Take Profit: $115,000
- Risk/Reward: 3.5
```

### 💰 Trade Logs
```
src/data/nof1_agents/trades/2025-10-27_trades.json
```
JSON log of all executed trades.

### 📈 Performance Metrics
```
src/data/nof1_agents/performance/
```
P&L tracking, Sharpe ratio, win rate, drawdown.

---

## 🛡️ Risk Management

### Built-in Protections

- ✅ **Confidence Thresholds** - Only trade when AI is confident enough
- ✅ **Position Sizing** - Limits per-trade exposure
- ✅ **Stop Loss** - Automatic exit on adverse moves
- ✅ **Take Profit** - Lock in gains automatically
- ✅ **Leverage Caps** - Prevent over-leveraging
- ✅ **Max Drawdown** - Stop trading if down X%
- ✅ **Min Balance** - Preserve minimum account balance

### ⚠️ Important Warnings

- ⚠️ **You can lose all your capital** - High leverage = high risk
- ⚠️ **AI can make mistakes** - No system is perfect
- ⚠️ **Start small** - Test with $10-50 first
- ⚠️ **Monitor closely** - Watch the first few hours
- ⚠️ **Lower leverage** - Start with 5x, not 20x
- ⚠️ **Paper trade first** - Test thoroughly before real money

**This software comes with NO WARRANTY. Use at your own risk.**

---

## 🤖 Supported AI Models

### Current: DeepSeek (Default)
- **Model**: `deepseek-chat` or `deepseek-reasoner`
- **Cost**: ~$0.14 per 1M input tokens (very cheap!)
- **Speed**: Fast responses (~1-2 seconds)

### Also Available:
- **Claude** (Anthropic) - `claude-3-5-haiku-latest`
- **GPT-4** (OpenAI) - `gpt-4o`
- **Gemini** (Google) - `gemini-2.5-flash`
- **Groq** (Fast inference) - `mixtral-8x7b-32768`
- **Ollama** (Local) - `llama3.2`

To switch models, edit `agent_configs.py`:
```python
CONFIG = {
    'MODEL_NAME': 'deepseek-chat',  # Change this
    # or 'claude-3-5-haiku-latest'
    # or 'gpt-4o'
}
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure you're using Python 3.10
python --version  # Should show 3.10.x

# Recreate virtual environment
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "DEEPSEEK_KEY not found"
```bash
# Check .env file exists
ls -la .env

# Make sure keys are set correctly
cat .env

# Reload environment
source venv/bin/activate
```

### "Can't connect to HyperLiquid"
```bash
# Verify wallet address and private key in .env
# Make sure HYPER_LIQUID_ETH_PRIVATE_KEY starts with 0x
# Test connection manually
python -c "from exchange.nice_funcs_hyperliquid import get_current_price; print(get_current_price('BTC'))"
```

### "Dependencies fail to install"
```bash
# Ensure Python 3.10 is active
python --version

# Update pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

---

## 🎨 Inspiration: Nof1.ai Alpha Arena

This project is inspired by [Nof1.ai](https://nof1.ai/)'s **Alpha Arena** approach:

- **Pure LLM decision-making** - No hard-coded rules, AI analyzes technical data
- **Technical analysis focus** - Price action, indicators, volume, momentum
- **Autonomous execution** - AI makes decisions and executes trades
- **Perpetuals trading** - Leverage, funding rates, long/short positions
- **Continuous learning** - AI adapts to market conditions

**Key Differences:**
- Nof1.ai is a competitive platform with multiple AI agents competing
- This is a standalone implementation you can run yourself
- Full control over configuration, models, and risk parameters

Learn more about Nof1.ai: [https://nof1.ai/](https://nof1.ai/)

---

## 📚 Additional Resources

### Learn More
- **HyperLiquid Docs**: [docs.hyperliquid.xyz](https://docs.hyperliquid.xyz)
- **DeepSeek API**: [platform.deepseek.com/docs](https://platform.deepseek.com/docs)
- **Nof1.ai**: [nof1.ai](https://nof1.ai/)

### Technical Indicators
- **EMA (Exponential Moving Average)** - Trend following
- **RSI (Relative Strength Index)** - Overbought/oversold
- **MACD (Moving Average Convergence Divergence)** - Momentum
- **ATR (Average True Range)** - Volatility
- **Bollinger Bands** - Price channels

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional exchange integrations (Binance, Bybit, etc.)
- More LLM providers (Grok, Llama, etc.)
- Advanced risk management strategies
- Backtesting framework
- Web dashboard for monitoring
- Multi-agent coordination

---

## 📄 License

MIT License - See LICENSE file for details

---

## ⚠️ Disclaimer

**THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY.**

- **No Financial Advice**: This is not financial advice. Do your own research.
- **High Risk**: Cryptocurrency trading, especially with leverage, is extremely risky.
- **No Warranty**: This software comes with absolutely no warranty.
- **Your Responsibility**: You are solely responsible for any losses incurred.
- **Test First**: Always test thoroughly with small amounts before scaling up.

**You can lose all your capital. Never risk more than you can afford to lose.**

---

## 📞 Support

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Security**: Report security issues privately

---

**Ready to start?**

```bash
# 1. Setup environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure keys
cp env.example .env
nano .env  # Add your API keys

# 3. Run the bot
python agents/deepseek_trader.py
```

**Trade responsibly. Start small. Monitor closely. Good luck! 🚀**

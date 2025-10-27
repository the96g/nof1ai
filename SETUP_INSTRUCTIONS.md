# 🚀 Setup Instructions for nof1-agents

## 📋 Complete Setup Checklist

Follow these steps to get your autonomous trading bot running:

---

## ✅ Step 1: Prerequisites

### Install Python 3.10

**Check if installed:**
```bash
python3.10 --version
```

**If not installed:**

**macOS:**
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

## ✅ Step 2: Clone Repository

```bash
git clone <your-repository-url>
cd nof1-agents
```

---

## ✅ Step 3: Setup Virtual Environment

```bash
# Create virtual environment with Python 3.10
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify activation (should show Python 3.10)
python --version
```

---

## ✅ Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
python -c "import pandas, pandas_ta, hyperliquid; print('✅ All dependencies installed')"
```

---

## ✅ Step 5: Get Your API Keys

### 1. DeepSeek API Key

1. Go to [https://platform.deepseek.com](https://platform.deepseek.com)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

**Cost:** Very cheap! ~$0.14 per 1M tokens

### 2. HyperLiquid Credentials

You need two things:

**a) Your Wallet Address** (public)
- This is your Ethereum wallet address
- Example: `0x1234...5678`
- Copy from MetaMask or your wallet

**b) Your Private Key** (KEEP SECRET!)
- Export from MetaMask: Settings → Security → Export Private Key
- Starts with `0x`
- ⚠️ **NEVER SHARE THIS WITH ANYONE!**

---

## ✅ Step 6: Configure Environment

```bash
# Copy template
cp env.example .env

# Edit with your keys
nano .env  # or use: code .env, vim .env, etc.
```

**Fill in your keys in `.env`:**

```bash
# Get from https://platform.deepseek.com
DEEPSEEK_KEY=sk-your-actual-deepseek-key-here

# Your Ethereum private key (from MetaMask)
HYPER_LIQUID_ETH_PRIVATE_KEY=0xyour-private-key-here

# Your wallet address
HYPER_LIQUID_MASTER_ADDRESS=0xyour-wallet-address-here
```

**Save and exit.**

---

## ✅ Step 7: Configure Trading Settings

Edit `agents/agent_configs.py`:

```bash
nano agents/agent_configs.py  # or your preferred editor
```

**Recommended settings for beginners:**

```python
CONFIG = {
    'STARTING_CAPITAL_USD': 100,         # Start small!
    'SYMBOLS': ['BTC', 'ETH'],           # Trade just 2 coins
    'MAX_LEVERAGE': 5,                    # Lower leverage = safer
    'MAX_POSITION_PERCENT': 50,          # Use 50% of capital
    'CHECK_INTERVAL_MINUTES': 5,         # Check every 5 minutes
    'MIN_CONFIDENCE_TO_TRADE': 0.75,     # Higher confidence = fewer trades
    'STOP_LOSS_PERCENT': 3.0,            # Tighter stop loss
    'TAKE_PROFIT_PERCENT': 10.0,         # 10% profit target
}
```

**Save and exit.**

---

## ✅ Step 8: Test Configuration

```bash
# Make sure venv is activated
source venv/bin/activate

# Test imports
python -c "from agents.agent_configs import CONFIG; print('✅ Config loaded successfully')"

# Test API connection
python -c "from exchange.nice_funcs_hyperliquid import get_current_price; print(f'BTC Price: ${get_current_price(\"BTC\"):,.2f}')"
```

If both commands succeed, you're ready!

---

## ✅ Step 9: Run the Bot

```bash
# Make sure venv is activated
source venv/bin/activate

# Run the trading bot
python agents/deepseek_trader.py
```

**Expected output:**
```
🌙 DeepSeek Pure LLM Trader - Nof1 Style
================================================================
✅ DeepSeek ready: deepseek-chat
📋 DeepSeek Trader Configuration:
   Exchange: hyperliquid
   Symbols: ['BTC', 'ETH']
   Starting Capital: $100.00
   Max Leverage: 5x
   Min Confidence: 75.0%

🚀 Starting Pure LLM Trading Agent...
Press Ctrl+C to stop

📊 Collecting real-time data from HyperLiquid...
```

---

## ✅ Step 10: Monitor & Stop

### Monitor
- Watch console for AI decisions
- Check logs in `src/data/nof1-agents/`
- Monitor your HyperLiquid account

### Stop the Bot
Press `Ctrl+C` to stop gracefully

### Check Logs
```bash
# View reasoning traces
cat src/data/nof1-agents/reasoning/deepseek_*.txt

# View trade logs
cat src/data/nof1-agents/trades/*.json
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "DEEPSEEK_KEY not found"
```bash
# Check .env file exists
ls -la .env

# Verify keys are set
cat .env

# Make sure no spaces around = sign
# WRONG: DEEPSEEK_KEY = sk-...
# RIGHT: DEEPSEEK_KEY=sk-...
```

### Issue: "Can't connect to HyperLiquid"
```bash
# Verify private key format
# Should start with 0x
# Example: 0x1234567890abcdef...

# Test connection manually
python -c "from exchange.nice_funcs_hyperliquid import get_current_price; print(get_current_price('BTC'))"
```

### Issue: Bot keeps saying "DO_NOTHING"
This is normal! The AI is being cautious. You can:
- Lower `MIN_CONFIDENCE_TO_TRADE` to 0.65
- Wait for better market conditions
- Check that data is being collected properly

---

## 📚 Next Steps

1. **Monitor First Hour** - Watch how AI makes decisions
2. **Review Logs** - Check `src/data/nof1-agents/reasoning/`
3. **Adjust Settings** - Tune based on performance
4. **Scale Gradually** - Increase capital slowly
5. **Read Full README** - [README.md](README.md) for advanced features

---

## ⚠️ Safety Reminders

- ✅ Start with $50-100 maximum
- ✅ Use low leverage (5x, not 20x!)
- ✅ Monitor closely for first few hours
- ✅ Understand you can lose all your capital
- ✅ Never risk more than you can afford to lose

---

## 🆘 Need Help?

1. Check [QUICKSTART.md](QUICKSTART.md) for quick answers
2. Read [README.md](README.md) for detailed info
3. Review [SECURITY.md](SECURITY.md) for key management
4. Open GitHub issue for bugs
5. Check logs in `src/data/nof1-agents/`

---

## ✅ Quick Command Reference

```bash
# Activate environment
source venv/bin/activate

# Run bot
python agents/deepseek_trader.py

# Stop bot
Ctrl+C

# View logs
cat src/data/nof1-agents/reasoning/deepseek_*.txt

# Test connection
python -c "from exchange.nice_funcs_hyperliquid import get_current_price; print(get_current_price('BTC'))"

# Check config
python -c "from agents.agent_configs import CONFIG; print(CONFIG)"
```

---

**You're all set! Happy trading! 🚀**

Remember: Start small, monitor closely, trade responsibly.


# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 🎯 Prerequisites

- Python 3.10 installed
- HyperLiquid wallet with some funds
- DeepSeek API key

## 📝 Step-by-Step Setup

### 1️⃣ Install Python 3.10

**Check if you have it:**
```bash
python3.10 --version
```

**Don't have it? Install:**

macOS:
```bash
brew install python@3.10
```

Ubuntu:
```bash
sudo apt update && sudo apt install python3.10 python3.10-venv python3.10-dev
```

Windows: Download from [python.org](https://www.python.org/downloads/release/python-3100/)

---

### 2️⃣ Setup Project

```bash
# Navigate to project directory
cd nof1-agents

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3️⃣ Configure API Keys

```bash
# Copy environment template
cp env.example .env

# Edit with your keys
nano .env  # or use any text editor
```

**Fill in your keys:**

```bash
# Get from https://platform.deepseek.com
DEEPSEEK_KEY=sk-your-actual-deepseek-key-here

# Your Ethereum private key (starts with 0x)
HYPER_LIQUID_ETH_PRIVATE_KEY=0xyour-private-key-here

# Your wallet address (starts with 0x)
HYPER_LIQUID_MASTER_ADDRESS=0xyour-wallet-address-here
```

**Where to get these:**
- **DeepSeek API Key**: Sign up at [platform.deepseek.com](https://platform.deepseek.com)
- **Private Key**: Export from MetaMask or your wallet
- **Wallet Address**: Copy from MetaMask or your wallet

---

### 4️⃣ Configure Trading Settings (Optional)

Edit `agents/agent_configs.py`:

```python
CONFIG = {
    'STARTING_CAPITAL_USD': 500,         # Change to your capital
    'SYMBOLS': ['BTC', 'ETH'],           # Coins to trade
    'MAX_LEVERAGE': 20,                  # Lower for safer trading
    'CHECK_INTERVAL_MINUTES': 3,         # Check frequency
    'MIN_CONFIDENCE_TO_TRADE': 0.65,     # Higher = safer but fewer trades
}
```

**Recommended for beginners:**
- Start with $50-100 capital
- Use 5-10x leverage (not 20x!)
- Increase confidence to 0.75
- Trade only BTC and ETH

---

### 5️⃣ Run the Bot

```bash
# Make sure venv is activated
source venv/bin/activate

# Run!
python agents/deepseek_trader.py
```

**Expected Output:**
```
🌙 DeepSeek Pure LLM Trader - Nof1 Style
✅ DeepSeek ready: deepseek-chat
📋 Configuration loaded
🚀 Starting Pure LLM Trading Agent...

📊 Collecting real-time data from HyperLiquid...
   💰 Fetching account data...
      Account Value: $500.00
      Available Cash: $500.00
```

---

### 6️⃣ Monitor & Stop

**Watch the logs** - The bot will:
- Print decisions every 3 minutes
- Show reasoning and confidence
- Log all trades

**Stop the bot:**
- Press `Ctrl+C` to stop gracefully

**Check logs:**
```bash
# Reasoning traces
cat src/data/nof1-agents/reasoning/deepseek_2025-10-27.txt

# Trade logs
cat src/data/nof1-agents/trades/2025-10-27_trades.json
```

---

## 🛡️ Safety Checklist

Before running with real money:

- [ ] I have backed up my private keys securely
- [ ] I'm only using funds I can afford to lose
- [ ] I've tested with small amounts first ($10-50)
- [ ] I understand leverage increases both gains AND losses
- [ ] I've set appropriate stop loss percentages
- [ ] I'm monitoring the bot during the first few hours
- [ ] I've read the risk warnings in README.md

---

## 🔧 Common Issues

### "ModuleNotFoundError: No module named 'pandas_ta'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "DEEPSEEK_KEY not found"
```bash
# Make sure .env file exists
ls -la .env

# Check contents (keys should not be empty)
cat .env
```

### "Can't connect to HyperLiquid"
- Verify your private key starts with `0x`
- Ensure wallet has some funds
- Check internet connection

### Bot keeps saying "DO_NOTHING"
- This is normal - AI is being cautious
- Lower `MIN_CONFIDENCE_TO_TRADE` to 0.60
- Market conditions might not be favorable

---

## 📚 Next Steps

Once you're running:

1. **Monitor for first hour** - Watch how AI makes decisions
2. **Review logs** - Check reasoning traces to understand AI logic
3. **Adjust settings** - Tune confidence, leverage, stop loss
4. **Scale gradually** - Start small, increase capital slowly
5. **Track performance** - Monitor P&L and win rate

---

## 🆘 Need Help?

- Read full [README.md](README.md) for detailed info
- Check [SECURITY.md](SECURITY.md) for key management
- Open GitHub issue for bugs
- Review logs in `src/data/nof1-agents/`

---

**Happy trading! Start small, trade safe, monitor closely. 🚀**


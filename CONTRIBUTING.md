# 🤝 Contributing to nof1-agents

Thank you for your interest in contributing! This project welcomes contributions from the community.

## 🎯 Ways to Contribute

### 1. Bug Reports
- Open a GitHub issue
- Include steps to reproduce
- Provide error messages and logs
- Mention your Python version and OS

### 2. Feature Requests
- Describe the feature clearly
- Explain the use case
- Discuss potential implementation

### 3. Code Contributions
- Fix bugs
- Add new features
- Improve documentation
- Add tests
- Optimize performance

### 4. Documentation
- Improve README
- Add tutorials
- Fix typos
- Translate to other languages

## 🚀 Getting Started

### Setup Development Environment

```bash
# Clone and setup
git clone <repo-url>
cd nof1-agents

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp env.example .env
# Add your test API keys
```

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic

4. **Test thoroughly**
   ```bash
   # Test with small capital first
   python agents/deepseek_trader.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub

## 📝 Code Style

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

### Example:
```python
def calculate_position_size(
    account_balance: float,
    max_position_percent: float,
    leverage: int
) -> float:
    """
    Calculate position size based on account balance and leverage
    
    Args:
        account_balance: Available account balance in USD
        max_position_percent: Maximum % of balance to use (0-100)
        leverage: Leverage multiplier (1-50)
    
    Returns:
        Notional position size in USD
    """
    margin = account_balance * (max_position_percent / 100)
    notional_size = margin * leverage
    return notional_size
```

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### 1. Exchange Integrations
- **Binance Futures** integration
- **Bybit** integration
- **OKX** integration
- Abstract exchange interface

### 2. AI Model Providers
- **Grok (xAI)** integration
- **Local Llama** via Ollama
- **Claude Opus** support
- Model ensemble/voting system

### 3. Risk Management
- Dynamic position sizing
- Portfolio-level risk management
- Drawdown protection algorithms
- Kelly Criterion implementation

### 4. Features
- Backtesting framework
- Paper trading mode
- Web dashboard (Flask/Streamlit)
- Telegram notifications
- Multi-agent coordination
- Market regime detection

### 5. Infrastructure
- Unit tests (pytest)
- Integration tests
- CI/CD pipeline (GitHub Actions)
- Docker support
- Logging improvements

## 🧪 Testing

### Manual Testing Checklist

Before submitting PR, test:
- [ ] Bot starts without errors
- [ ] Data collection works for all symbols
- [ ] LLM responds correctly
- [ ] Trades execute successfully (paper trade first!)
- [ ] Logs are created properly
- [ ] Configuration changes work
- [ ] Error handling works

### Test with Small Capital
Always test with small amounts ($10-50) first!

## 📋 Pull Request Guidelines

### PR Title Format
```
feat: Add Binance integration
fix: Correct position sizing calculation
docs: Update installation instructions
refactor: Improve data formatter structure
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tested manually with small capital
- [ ] All existing features still work
- [ ] Added new tests (if applicable)

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No sensitive data in commit
- [ ] Ready for review
```

## 🔒 Security

### Never Commit Secrets!
- Check `.gitignore` includes `.env`
- Never force-add sensitive files
- Don't commit API keys or private keys
- Review changes before committing

### Security Checklist
```bash
# Before committing
git diff  # Review all changes
git status  # Check staged files
```

## 🐛 Reporting Security Issues

If you find a security vulnerability:
1. **Do NOT open a public issue**
2. Email maintainers privately
3. Provide details and reproduction steps
4. Allow time for fix before disclosure

## 💬 Communication

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - Questions, ideas, showcase
- **Pull Requests** - Code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution helps make this project better. Whether it's:
- A one-line typo fix
- A major feature addition
- Documentation improvements
- Bug reports
- Feature suggestions

**All contributions are valued and appreciated!**

---

**Questions?** Open a GitHub Discussion or Issue. We're here to help! 🚀


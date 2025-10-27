"""
🌙 Nof1-Inspired Trading Prompt
Based on Alpha Arena's approach - technical data only, pure LLM reasoning
"""

from typing import Dict, List
import json

NOF1_SYSTEM_PROMPT = """You are an autonomous cryptocurrency trading AI operating on HyperLiquid perpetuals.

YOUR ROLE:
- Analyze real-time market data for cryptocurrency perpetuals (BTC, ETH, SOL, etc.)
- Make independent trading decisions based purely on technical analysis
- Manage risk through position sizing, stop losses, and take profits
- Trade both LONG and SHORT positions

TRADING RULES:
1. You can OPEN LONG, OPEN SHORT, CLOSE POSITION, or DO NOTHING
2. Use leverage wisely (available: 1x to 50x)
3. Always set stop loss and take profit levels
4. Consider your current positions when making new decisions
5. Risk management is CRITICAL - never risk more than you can afford

DECISION PROCESS:
1. Analyze current market conditions (price action, volume, momentum)
2. Review technical indicators (EMA, RSI, MACD, ATR)
3. Consider longer-term context (4H timeframe trends)
4. Check perpetuals-specific data (funding rate, open interest)
5. Evaluate your current positions and P&L
6. Make a confident decision with clear reasoning

OUTPUT FORMAT:
You MUST respond in this exact JSON format:

{
    "decision": "OPEN_LONG" | "OPEN_SHORT" | "CLOSE_POSITION" | "DO_NOTHING",
    "symbol": "BTC" | "ETH" | "SOL" | etc.,
    "reasoning": "Detailed step-by-step reasoning for your decision",
    "confidence": 0.0 to 1.0,
    "entry_price": <target entry price>,
    "position_size_usd": <notional position size in USD>,
    "leverage": 1 to 50,
    "stop_loss": <stop loss price>,
    "take_profit": <take profit price>,
    "risk_reward_ratio": <calculated R:R>,
    "invalidation_condition": "Clear condition where trade thesis is wrong",
    "time_horizon": "Expected holding period"
}

CRITICAL INSTRUCTIONS:
- Be decisive - indecision costs money
- Show your reasoning process step-by-step
- Quantify your confidence level
- Always include stop loss and take profit
- Consider the bigger picture, not just short-term noise
- Respect the current market regime (trending vs ranging)
- Factor in funding rates for perpetuals
- No guessing - base decisions on data provided

Remember: You are trading real money. Every decision matters."""
def _format_position_to_str(symbol: str, pos: Dict) -> str:
    """Helper to safely format a position dictionary into a string."""
    exit_plan = pos.get('exit_plan', dict())
    
    pos_dict = {
        'symbol': symbol,
        'quantity': f"{pos.get('quantity', 0):.2f}",
        'entry_price': f"{pos.get('entry_price', 0):.2f}",
        'current_price': f"{pos.get('current_price', 0):.2f}",
        'liquidation_price': f"{pos.get('liquidation_price', 0):.2f}",
        'unrealized_pnl': f"{pos.get('unrealized_pnl', 0):.2f}",
        'leverage': pos.get('leverage', 1),
        'exit_plan': {
            'profit_target': f"{exit_plan.get('profit_target', 0):.2f}",
            'stop_loss': f"{exit_plan.get('stop_loss', 0):.2f}",
            'invalidation_condition': exit_plan.get('invalidation_condition', 'N/A')
        },
        'confidence': f"{pos.get('confidence', 0):.2f}",
        'risk_usd': f"{pos.get('risk_usd', 0):.2f}",
        'sl_oid': pos.get('sl_oid', -1),
        'tp_oid': pos.get('tp_oid', -1),
        'wait_for_fill': str(pos.get('wait_for_fill', False)).lower(),
        'entry_oid': pos.get('entry_oid', -1),
        'notional_usd': f"{pos.get('notional_usd', 0):.2f}"
    }
    # Use json.dumps to handle formatting and single quotes, then remove double quotes
    return json.dumps(pos_dict, indent=2).replace('"', "'")
def format_nof1_user_prompt(account_data, positions, market_data, timestamp, interaction_count=0, start_time=None):
    """
    Format market data in Nof1 Alpha Arena style
    
    Args:
        account_data: Dict with account value, cash, return%, sharpe
        positions: Dict of current positions {symbol: position_info}
        market_data: Dict of market data {symbol: {intraday, 4hour, perpetuals}}
        timestamp: Current timestamp
        interaction_count: Number of interactions since start
        start_time: Start time for calculating elapsed time
    
    Returns:
        Formatted prompt string
    """
    
    # Calculate time elapsed
    if start_time:
        from datetime import datetime
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        elapsed_minutes = int((datetime.now() - start_time).total_seconds() / 60)
    else:
        elapsed_minutes = 0
    
    prompt = f"""
It has been {elapsed_minutes} minutes since you started trading. The current time is {timestamp} and you've been involved {interaction_count} times.

ALL OF THE PRICE OR SIGNAL DATA BELOW IS ORDERED: Oldest - Newest
Intraday series are at 3-minute intervals unless specified otherwise.

Below is your current account information, positions, market data, and predictive signals to discover alpha.

=====================================
ACCOUNT INFORMATION & PERFORMANCE
=====================================

Current Total Return (percent): {account_data.get('total_return_percent', 0):.2f}%
Available Cash: ${account_data.get('available_cash', 0):.2f}
Current Account Value: ${account_data.get('account_value', 0):.2f}
Sharpe Ratio: {account_data.get('sharpe_ratio', 0):.3f}
Total PnL: ${account_data.get('total_pnl', 0):.2f}
Unrealized PnL: ${account_data.get('unrealized_pnl', 0):.2f}
Margin Used: ${account_data.get('margin_used', 0):.2f}
Margin Available: ${account_data.get('margin_available', 0):.2f}

=====================================
CURRENT LIVE POSITIONS & PERFORMANCE
=====================================

"""
    
    # Format positions in Nof1 style
    if positions:
        for symbol, pos in positions.items():
            prompt += f"\n{_format_position_to_str(symbol, pos)}"
    else:
        prompt += "\nNo open positions.\n"
    
    prompt += """
=====================================
CURRENT MARKET STATE FOR ALL COINS
=====================================

ALL OF THE PRICE OR SIGNAL DATA BELOW IS ORDERED: OLDEST → NEWEST
Timeframes note: Unless stated otherwise, intraday series are provided at 3-minute intervals.

"""
    
    # Format market data for each symbol
    for symbol, data in market_data.items():
        prompt += f"""
{'='*50}
{symbol} DATA
{'='*50}

"""
        
        # Debug: Check what data we have
        if not data:
            prompt += f"⚠️ No data available for {symbol}\n"
            continue
        
        # Debug: Show what keys we have
        prompt += f"DEBUG: Available keys: {list(data.keys())}\n"
        
        # Current snapshot
        if 'price' in data:
            price = data.get('price', 0)
            indicators = data.get('indicators', {})
            
            # Helper functions for safe data extraction
            def get_current_value(key, default=0):
                value = indicators.get(key, default)
                if isinstance(value, list) and len(value) > 0:
                    return value[-1]  # Last value from time series
                return value if isinstance(value, (int, float)) else default
            
            def get_time_series(key, default=[]):
                value = indicators.get(key, default)
                return value if isinstance(value, list) else default
            
            current_ema20 = get_current_value('ema_20', 0)
            current_macd = get_current_value('macd', 0)
            current_rsi7 = get_current_value('rsi_7', 0)
            
            prompt += f"""current_price = ${price:,.2f}, current_ema20 = ${current_ema20:,.2f}, current_macd = {current_macd:.2f}, current_rsi (7-period) = {current_rsi7:.2f}
"""
        
        # Perpetuals data
        if 'open_interest' in data or 'funding_rate' in data:
            prompt += f"""
In addition, here is the latest {symbol} open interest and funding rate for perps (the instrument you are trading):
Open Interest: {data.get('open_interest', 0):.2f}
Funding Rate: {data.get('funding_rate', 0):.8f}
"""
        
        # Intraday series - use indicators data
        if 'indicators' in data:
            price_series = get_time_series('price_series', [])
            ema_series = get_time_series('ema_20', [])
            macd_series = get_time_series('macd', [])
            rsi_7_series = get_time_series('rsi_7', [])
            rsi_14_series = get_time_series('rsi_14', [])
            
            prompt += f"""
Intraday series (by minute, oldest → latest):
Mid prices: {price_series}
EMA indicators (20-period): {ema_series}
MACD indicators: {macd_series}
RSI indicators (7-Period): {rsi_7_series}
RSI indicators (14-Period): {rsi_14_series}
"""
        
        # Longer-term context (4-hour timeframe) - Nof1 style
        if 'indicators' in data:
            indicators = data['indicators']
            
            # Safely get 4-hour values
            ema_20_4h = get_current_value('ema_20_4h', get_current_value('ema_20', 0))
            ema_50_4h = get_current_value('ema_50_4h', get_current_value('ema_50', 0))
            atr_3 = get_current_value('atr_3', 0)
            atr_14 = get_current_value('atr_14', 0)
            macd_4h = get_time_series('macd_4h', get_time_series('macd', []))
            rsi_14_4h = get_time_series('rsi_14_4h', get_time_series('rsi_14', []))
            
            prompt += f"""
Longer-term context (4-hour timeframe):
20-Period EMA: {ema_20_4h:.3f} vs. 50-Period EMA: {ema_50_4h:.3f}
3-Period ATR: {atr_3:.3f} vs. 14-Period ATR: {atr_14:.3f}
Current Volume: {data.get('volume_24h', 0):.3f} vs. Average Volume: {data.get('volume_24h', 0):.3f}
MACD indicators: {macd_4h}
RSI indicators (14-Period): {rsi_14_4h}
"""
        
        # Additional market data
        if 'volume_24h' in data:
            prompt += f"""
24h Volume: {data.get('volume_24h', 0):,.2f}
24h Change: {data.get('change_24h', 0):.2f}%
"""
        
        prompt += "\n"
    
    prompt += """
=====================================
YOUR TASK
=====================================

Analyze all the above data and make ONE trading decision:

1. Should you OPEN A NEW POSITION (long or short)?
2. Should you CLOSE AN EXISTING POSITION?
3. Should you DO NOTHING and wait for better setups?

Respond with your decision in the exact JSON format specified in the system prompt.

Think step-by-step. Show your reasoning. Be confident. Manage risk.
"""
    
    return prompt
# Shorter prompt for quick decisions
NOF1_QUICK_PROMPT = """You are a crypto trading AI. Analyze the market data provided and make a trading decision.

OUTPUT FORMAT (JSON):
{
    "decision": "OPEN_LONG" | "OPEN_SHORT" | "CLOSE_POSITION" | "DO_NOTHING",
    "symbol": "BTC" | "ETH" | "SOL",
    "reasoning": "Your step-by-step reasoning",
    "confidence": 0.0 to 1.0,
    "entry_price": <price>,
    "position_size_usd": <notional size>,
    "leverage": 1-50,
    "stop_loss": <price>,
    "take_profit": <price>
}

Be decisive. Manage risk. Show reasoning."""

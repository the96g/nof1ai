"""
🌙 Aster DEX Stub
Aster support has been removed from standalone nof1-agents.
This is a stub file to prevent import errors.

If you need Aster support, use the full moon-dev-ai-agents project.
For HyperLiquid trading, you don't need this file.
"""

# Stub - Aster not supported in standalone nof1-agents
ASTER_AVAILABLE = False

def __getattr__(name):
    """Return None for any function call"""
    return lambda *args, **kwargs: None

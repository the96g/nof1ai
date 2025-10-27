#!/usr/bin/env python3
"""
🌙 Nof1-Agents Runner
Independent runner for the nof1-agents module

Usage:
    python run.py
"""

import sys
from pathlib import Path

# Add current directory to path for independent operation
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Add project root for model_factory access
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

if __name__ == "__main__":
    from agents.deepseek_trader import main
    main()

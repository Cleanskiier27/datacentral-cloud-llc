#!/usr/bin/env python3
"""
BUSTER.BOT Entry Point.
Direct alias to moonbase_bot.py for seamless interoperability.
"""

import sys
import os

repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from moonbase_bot import main

if __name__ == "__main__":
    main()

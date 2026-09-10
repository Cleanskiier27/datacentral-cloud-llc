#!/usr/bin/env python3
"""
BUSTER.BOT Entry Point.
Direct alias to moonbase_bot.py for seamless interoperability.
"""

import sys
import os
import importlib.util

repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Load main from top-level moonbase_bot.py
spec = importlib.util.spec_from_file_location("moonbase_bot_main", os.path.join(repo_root, "moonbase_bot.py"))
moonbase_bot_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(moonbase_bot_main)
main = moonbase_bot_main.main

repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)



if __name__ == "__main__":
    main()

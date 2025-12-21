#!/usr/bin/env python3
"""
🚀 START.py — ENTRY POINT
This script manages project creation through AI Agent.

WORKFLOW:
1. Loads the "Constitution" (manifesto.md) and shows it to the Agent.
2. Runs the "Builder" (builder.py) to create files.
"""

import os
import sys
from pathlib import Path

# Get the path where the scripts are located (your tools folder)
TOOLKIT_DIR = Path(__file__).parent.resolve()
MANIFESTO_PATH = TOOLKIT_DIR / "manifesto.md"
BUILDER_PATH = TOOLKIT_DIR / "builder.py"

def main():
    # 1. Check for required tools
    if not MANIFESTO_PATH.exists() or not BUILDER_PATH.exists():
        print("❌ ERROR: manifesto.md or builder.py not found")
        print(f"Make sure they are in: {TOOLKIT_DIR}")
        return

    # 2. Read and output the Manifesto for AI
    print("\n" + "="*60)
    print("🧠 LOADING KNOWLEDGE BASE (File #1)...")
    print("="*60)
    print(MANIFESTO_PATH.read_text(encoding='utf-8'))
    print("\n" + "="*60)
    print("🤖 INSTRUCTIONS FOR CURSOR AGENT:")
    print("1. You just read the Manifesto above. This is LAW.")
    print("2. Now I will run the structure generator.")
    print("3. Your task — verify the result and create _AI_INCLUDE files based on the Manifesto.")
    print("="*60 + "\n")

    # 3. Ask for name and run Builder
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = input("Enter new project name: ").strip()

    if not project_name:
        return

    # Import and run builder.py as module
    sys.path.append(str(TOOLKIT_DIR))
    import builder
    builder.run(project_name)

    print(f"\n✨ Project {project_name} initialized.")
    print(f"📂 Now go to folder: cd {project_name}")
    print("💡 And tell Cursor: 'Configure details according to the Manifesto'.")

if __name__ == "__main__":
    main()

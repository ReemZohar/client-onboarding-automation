#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Orchestrator import get_orchestrator

def main():
    urls = sys.argv[1:]
    
    orchestrator = get_orchestrator()
    client = orchestrator.run(urls)
    
    if "error" in client:
        print(f"Error: {client['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()

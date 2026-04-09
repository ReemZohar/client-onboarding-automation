#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Orchestrator import get_orchestrator

def main():
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python run.py <url> [url2] [url3] ...")
        sys.exit(1)
    
    print(f"Processing {len(urls)} URL(s)...")
    
    orchestrator = get_orchestrator()
    client = orchestrator.run(urls)
    
    if "error" in client:
        print(f"Error: {client['error']}")
        sys.exit(1)
    
    print(f"\n✓ Client saved: {client['name']}")
    print(f"\nOpen src/ui.html in browser to view.")

if __name__ == "__main__":
    main()

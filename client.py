#!/usr/bin/env python3
"""
Heavenet Agora Client v0.1
Law VI: Users > Investors. The interface is the product.

No signup. No cloud. No tracking.
Reads from localhost:1776. Works offline.
Your.heavenet/oath.json is your login.
"""

import requests
import json
import sys
import os
from datetime import datetime
from pathlib import Path

AGORA_URL = "http://localhost:1776"
HEAVENET_ROOT = Path(__file__).parent
OATH = "I will uphold Law I-VII or I will fork. I seek Rep, not equity."

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_identity():
    try:
        r = requests.get(f"{AGORA_URL}/identity", timeout=1)
        return r.json()
    except:
        return None

def get_posts():
    try:
        r = requests.get(f"{AGORA_URL}/posts", timeout=2)
        return r.json().get("posts", [])
    except:
        return []

def post_content(content):
    try:
        r = requests.post(f"{AGORA_URL}/post", json={"content": content}, timeout=2)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

def render_post(post):
    ts = datetime.fromtimestamp(post['timestamp']).strftime('%Y-%m-%d %H:%M')
    rep_stars = "★" * min(post['rep'] // 100, 5) # Law II: Rep is visible
    return f"""
{rep_stars} {post['author_id']}... | Rep: {post['rep']} | {ts}
{'-' * 60}
{post['content']}
{'=' * 60}
"""

def main():
    identity = get_identity()
    if not identity:
        print("❌ Law II violation: Agora daemon not running.")
        print(" Run: python daemon/server.py")
        print(f"\n {OATH}")
        sys.exit(1)

    while True:
        clear()
        print("=== HEAVENET AGORA v0.1 ===")
        print(f"Identity: {identity['short_id']}... | Rep: {identity['rep']}")
        print(f"Law VI: Users > Investors. No ads. No cloud.")
        print("=" * 60)

        posts = get_posts()
        if not posts:
            print("\n No posts yet. Law V: Ship Daily. Be the first.\n")
        else:
            for post in reversed(posts[-10:]): # Show last 10, newest first
                print(render_post(post))

        print("\nCommands: [p]ost | [r]efresh | [q]uit")
        cmd = input("> ").strip().lower()

        if cmd == 'p':
            print("\nWrite post. Law II: Your Rep will be attached.")
            print("Press Enter twice to submit. Ctrl+C to cancel.")
            lines = []
            try:
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
                content = "\n".join(lines[:-1]).strip()
                if content:
                    status, resp = post_content(content)
                    if status == 201:
                        print("✅ Posted. Law III: It's now in /vault/agora/")
                    else:
                        print(f"❌ Failed: {resp.get('error', 'Unknown error')}")
                    input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                pass

        elif cmd == 'r':
            continue

        elif cmd == 'q':
            print(f"\n{OATH}\n")
            break

if __name__ == "__main__":
    main()
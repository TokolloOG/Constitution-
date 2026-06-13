#!/usr/bin/env python3
"""
Heavenet Agora Client v0.2
Law VI: Users > Investors. Encrypted by default.

Decrypts posts using your.heavenet/id_ed25519 key.
Shows [ENCRYPTED] if you don't have the key.
"""

import requests
import json
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

AGORA_URL = "http://localhost:1776"
HEAVENET_ROOT = Path(__file__).parent
CRYPTO_PATH = HEAVENET_ROOT / "daemon" / "crypto.js"
OATH = "I will uphold Law I-VII or I will fork. I seek Rep, not equity."

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def decrypt_content(encrypted_text):
    """Law VI: Try to decrypt. If fail, return None."""
    try:
        result = subprocess.run(
            ["node", str(CRYPTO_PATH), "decrypt"],
            input=encrypted_text.encode(),
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.decode().strip()
    except:
        pass
    return None

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

def post_content(content, recipients=None):
    try:
        payload = {"content": content}
        if recipients:
            payload["recipients"] = recipients
        r = requests.post(f"{AGORA_URL}/post", json=payload, timeout=2)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

def render_post(post):
    ts = datetime.fromtimestamp(post['timestamp']).strftime('%Y-%m-%d %H:%M')
    rep_stars = "★" * min(post['rep'] // 100, 5)

    # Law VI: Decrypt if possible
    if post.get('encrypted'):
        decrypted = decrypt_content(post['content'])
        if decrypted:
            content = decrypted
            lock = "🔓"
        else:
            content = "[ENCRYPTED - You are not a recipient]"
            lock = "🔒"
    else:
        content = post['content']
        lock = "📢" # plaintext

    return f"""
{rep_stars} {post['author_id']}... | Rep: {post['rep']} | {ts} {lock}
{'-' * 60}
{content}
{'=' * 60}
"""

def main():
    identity = get_identity()
    if not identity:
        print("❌ Law II violation: Agora daemon not running.")
        print(" Run: python daemon/server.py")
        sys.exit(1)

    while True:
        clear()
        print("=== HEAVENET AGORA v0.2 ===")
        print(f"Identity: {identity['short_id']}... | Rep: {identity['rep']}")
        print(f"Law VI: Users > Investors. 🔓=yours, 🔒=encrypted, 📢=public")
        print("=" * 60)

        posts = get_posts()
        if not posts:
            print("\n No posts yet. Law V: Ship Daily.\n")
        else:
            for post in reversed(posts[-10:]):
                print(render_post(post))

        print("\nCommands: [p]ost | [g]roup post | [r]efresh | [q]uit")
        cmd = input("> ").strip().lower()

        if cmd == 'p':
            print("\nWrite public post. Encrypted to self only.")
            content = input("Post: ").strip()
            if content:
                status, resp = post_content(content)
                print("✅ Posted" if status == 201 else f"❌ {resp.get('error')}")
                input("Enter...")

        elif cmd == 'g':
            print("\nWrite group post. Enter recipient pubkeys, comma separated:")
            print("Get pubkeys: node daemon/crypto.js pubkey")
            recips = input("Recipients: ").strip().split(',')
            recips = [r.strip() for r in recips if r.strip()]
            if recips:
                content = input("Post: ").strip()
                if content:
                    status, resp = post_content(content, recips)
                    print("✅ Posted to group" if status == 201 else f"❌ {resp.get('error')}")
                    input("Enter...")

        elif cmd == 'r':
            continue
        elif cmd == 'q':
            print(f"\n{OATH}\n")
            break

if __name__ == "__main__":
    main()
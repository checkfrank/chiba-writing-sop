#!/usr/bin/env python3
"""
content-repurposer/scripts/threads-post.py — Generate a Meta Threads post (Windows-compatible)

Usage:
    echo 'content' | python threads-post.py --stdin
    python threads-post.py <source_file>
"""

import sys
import os
import json
from pathlib import Path
from pathlib import Path


def load_config():
    config_dir = Path.home() / '.config' / 'content-repurposer'
    config_file = config_dir / 'config.json'
    if not os.path.exists(config_file):
        print("❌ Config not found. Run setup.py first.", file=sys.stderr)
        sys.exit(1)
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_content():
    if '--stdin' in sys.argv:
        return sys.stdin.read()
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        print("Usage: python threads-post.py <source_file> or echo 'content' | python threads-post.py --stdin", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        return f.read()


def build_prompt(content, config):
    voice = config.get('voice', {})
    threads = config.get('platforms', {}).get('threads', {})
    user = config.get('user', {})

    prompt = f"""**Source Content:**
---
{content}
---

**Your Task:**
Transform the Source Content into a single, casual post for Meta Threads.

**Constraints:**
1. **Platform:** Meta Threads Post
2. **Voice & Tone:**
   - Tone: {voice.get('tone', 'professional-casual')}
   - Personality: {', '.join(voice.get('personality', ['direct', 'insightful', 'practical']))}
   - Style: Must be '{threads.get('style', 'casual')}' and conversational.
3. **Post Structure:**
   - Single post, not a thread.
   - Get straight to the point.
   - End with an open-ended question to encourage replies.
4. **Length:** Under {threads.get('max_length', 500)} characters.
5. **Hashtags:** {'Include 1-2 relevant hashtags.' if threads.get('include_hashtags', False) else 'Do not include any hashtags.'}
6. **Output Format:**
   - Single block of text. No commentary.

**User Info:**
- Name: {user.get('name', '')}

Begin."""

    return prompt


if __name__ == '__main__':
    content = read_content()
    config = load_config()
    prompt = build_prompt(content, config)
    print(prompt)

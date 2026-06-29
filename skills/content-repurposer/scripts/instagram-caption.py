#!/usr/bin/env python3
"""
content-repurposer/scripts/instagram-caption.py — Generate an Instagram caption (Windows-compatible)

Usage:
    echo 'content' | python instagram-caption.py --stdin
    python instagram-caption.py <source_file>
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
        print("Usage: python instagram-caption.py <source_file> or echo 'content' | python instagram-caption.py --stdin", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        return f.read()


def build_prompt(content, config):
    voice = config.get('voice', {})
    instagram = config.get('platforms', {}).get('instagram', {})
    user = config.get('user', {})

    prompt = f"""**Source Content:**
---
{content}
---

**Your Task:**
Transform the Source Content into a short, punchy Instagram caption for a visual (carousel or reel).

**Constraints:**
1. **Platform:** Instagram Caption
2. **Voice & Tone:**
   - Tone: {voice.get('tone', 'professional-casual')}
   - Personality: {', '.join(voice.get('personality', ['direct', 'insightful', 'practical']))}
   - Avoid: {', '.join(voice.get('avoid', ['corporate jargon']))}
   - Emoji Density: {instagram.get('emoji_density', 'high')}
3. **Caption Structure:**
   - Hook: First line must be a strong hook, no more than {instagram.get('hook_length', 50)} characters.
   - Body: Summarize the core message. Use line breaks for readability.
   - Call to Action: End with an engagement question (e.g., 'What's your take? 👇').
4. **Length:**
   - Main caption (excluding hashtags): 150-{instagram.get('target_length', 200)} characters.
   - Total (including hashtags): Max {instagram.get('max_length', 300)} characters.
5. **Hashtags:**
   - After main caption, add separator '---'.
   - Then provide {instagram.get('min_hashtags', 5)}-{instagram.get('max_hashtags', 10)} hashtags.
6. **Output Format:**
   - Single block of text. No commentary.

**User Info:**
- Name: {user.get('name', '')}
- Primary CTA: Link in bio.

Begin."""

    return prompt


if __name__ == '__main__':
    content = read_content()
    config = load_config()
    prompt = build_prompt(content, config)
    print(prompt)

#!/usr/bin/env python3
"""
content-repurposer/scripts/newsletter.py — Generate a newsletter section (Windows-compatible)

Usage:
    echo 'content' | python newsletter.py --stdin
    python newsletter.py <source_file>
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
        print("Usage: python newsletter.py <source_file> or echo 'content' | python newsletter.py --stdin", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        return f.read()


def build_prompt(content, config):
    voice = config.get('voice', {})
    newsletter = config.get('platforms', {}).get('newsletter', {})
    user = config.get('user', {})

    prompt = f"""**Source Content:**
---
{content}
---

**Your Task:**
Transform the Source Content into a compelling email newsletter section.

**Constraints:**
1. **Platform:** Email Newsletter Section
2. **Voice & Tone:**
   - Tone: {voice.get('tone', 'professional-casual')}
   - Personality: {', '.join(voice.get('personality', ['direct', 'insightful', 'practical']))}
   - Avoid: {', '.join(voice.get('avoid', ['corporate jargon']))}
   - Emoji Level: {voice.get('emoji_level', 'moderate')}
3. **Newsletter Structure:**
   - Subject Lines: Begin with {newsletter.get('subject_line_count', 3)} compelling subject line options, each prefixed with 'Subject:'.
   - Separator: After subject lines, add a '---' separator.
   - Body: A '{newsletter.get('section_style', 'scannable')}' newsletter section using markdown.
   - Length: Approximately {newsletter.get('target_length', 400)} words.
   - CTA: {'Include a clear Call to Action at the ' + newsletter.get('cta_placement', 'end') + '.' if newsletter.get('include_cta', True) else 'Do not include a Call to Action.'}
4. **Output Format:**
   - Format the body as {newsletter.get('format', 'markdown')}.
   - Single block of text. No commentary.

**User Info:**
- Name: {user.get('name', '')}
- Brand: {user.get('brand', '')}
- Primary CTA: {user.get('primary_cta', '')}

Begin."""

    return prompt


if __name__ == '__main__':
    content = read_content()
    config = load_config()
    prompt = build_prompt(content, config)
    print(prompt)

#!/usr/bin/env python3
"""
content-repurposer/scripts/linkedin-post.py — Generate a LinkedIn post (Windows-compatible)

Usage:
    echo 'content' | python linkedin-post.py --stdin
    python linkedin-post.py <source_file>
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
        print("Usage: python linkedin-post.py <source_file> or echo 'content' | python linkedin-post.py --stdin", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        return f.read()


def build_prompt(content, config):
    voice = config.get('voice', {})
    linkedin = config.get('platforms', {}).get('linkedin', {})
    user = config.get('user', {})

    prompt = f"""**Source Content:**
---
{content}
---

**Your Task:**
Transform the Source Content into a high-engagement LinkedIn post.

**Constraints:**
1. **Platform:** LinkedIn Post
2. **Voice & Tone:**
   - Tone: {voice.get('tone', 'professional-casual')}
   - Personality: {', '.join(voice.get('personality', ['direct', 'insightful', 'practical']))}
   - Avoid: {', '.join(voice.get('avoid', ['corporate jargon']))}
   - Emoji Level: {voice.get('emoji_level', 'moderate')}
3. **Post Structure:**
   - Hook: Start with a compelling '{linkedin.get('hook_style', 'personal_insight')}' to encourage clicks on '...see more'.
   - Body: Elaborate on key points. Use short paragraphs and bullet points. {'Include a personal story or professional insight.' if linkedin.get('include_story', True) else ''}
   - Focus: {'Strong B2B/professional focus.' if linkedin.get('b2b_focus', True) else 'General audience focus.'}
   - Conclusion: End with a clear Call to Action or an engaging question.
4. **Length:** Between {linkedin.get('min_length', 1300)} and {linkedin.get('max_length', 2000)} characters.
5. **Formatting:**
   - Do NOT include any links in the main body.
   - Use whitespace and line breaks effectively.
6. **Hashtags:** Include a block of {linkedin.get('max_hashtags', 5)} relevant hashtags at the end.
7. **Output Format:**
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

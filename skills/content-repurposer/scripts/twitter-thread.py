#!/usr/bin/env python3
"""
content-repurposer/scripts/twitter-thread.py — Generate a Twitter thread (Windows-compatible)

Usage:
    echo 'content' | python twitter-thread.py --stdin
    python twitter-thread.py <source_file>
"""

import sys
import os
import json
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
        print("Usage: python twitter-thread.py <source_file> or echo 'content' | python twitter-thread.py --stdin", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        return f.read()


def build_prompt(content, config):
    voice = config.get('voice', {})
    twitter = config.get('platforms', {}).get('twitter', {})
    user = config.get('user', {})

    prompt = f"""**Source Content:**
---
{content}
---

**Your Task:**
Transform the Source Content into a high-engagement Twitter thread.

**Constraints:**
1. **Platform:** Twitter Thread
2. **Voice & Tone:**
   - Tone: {voice.get('tone', 'professional-casual')}
   - Personality: {', '.join(voice.get('personality', ['direct', 'insightful', 'practical']))}
   - Avoid: {', '.join(voice.get('avoid', ['corporate jargon']))}
   - Emoji Level: {voice.get('emoji_level', 'moderate')}
3. **Thread Structure:**
   - Total Tweets: Between {twitter.get('thread_length_min', 3)} and {twitter.get('thread_length_max', 10)}.
   - Hook (First Tweet): Must be a compelling '{twitter.get('hook_style', 'bold_claim')}' to grab attention. Must NOT contain any hashtags.
   - Body Tweets: Each tweet should cover a single, clear point.
   - Formatting: {'Numbered (e.g., 1/, 2/, etc.)' if twitter.get('numbered', True) else 'Flow naturally without numbering.'}
   - Conclusion (Last Tweet): Include a Call to Action in the style of a '{twitter.get('cta_style', 'question')}'.
4. **Character Limits:** Each tweet MUST be under 280 characters.
5. **Hashtags:** Only in the final tweet. Maximum {twitter.get('max_hashtags', 2)} relevant hashtags.
6. **Output Format:**
   - Separate each tweet with '---'.
   - Do not include any commentary or explanation.

**User Info:**
- Name: {user.get('name', '')}
- Brand: {user.get('brand', '')}
- Primary CTA: {user.get('primary_cta', '')}

Begin."""

    return prompt


def call_llm(prompt):
    """
    Use WorkBuddy's llm tool to generate the thread.
    In an automated environment, this would call an LLM API.
    For now, output the prompt so the agent can execute it.
    """
    # This function is called by the agent (us) via the LLM tool
    # When running manually, we print the prompt
    print(prompt)


if __name__ == '__main__':
    content = read_content()
    config = load_config()
    prompt = build_prompt(content, config)
    call_llm(prompt)

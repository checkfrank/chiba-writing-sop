#!/usr/bin/env python3
"""
content-repurposer/scripts/setup.py — Initialize config and output directories (Windows-compatible)

Usage:
    python setup.py
"""

import os
import json
from pathlib import Path


def main():
    skill_dir = Path(__file__).parent.parent
    config_dir = Path.home() / '.config' / 'content-repurposer'
    output_dir = Path.home() / 'content-repurposer-output'

    print("♻️  Content Repurposer Setup")
    print("━" * 40)

    # Create config directory
    config_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created {config_dir}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created {output_dir}")

    # Copy example config
    config_file = config_dir / 'config.json'
    example_config = skill_dir / 'config.example.json'
    if not config_file.exists() and example_config.exists():
        config_file.write_text(example_config.read_text(encoding='utf-8'), encoding='utf-8')
        print(f"✓ Created config.json (edit with your voice and platform preferences)")
    else:
        print("• config.json already exists (skipped)")

    # Create example content file
    example_file = output_dir / 'examples' / 'sample-post.md'
    example_file.parent.mkdir(parents=True, exist_ok=True)
    if not example_file.exists():
        example_content = """# The Power of Small Wins

We obsess over big launches and major milestones. But here's what I've learned after 10 years of building: momentum comes from small wins.

## Why Small Wins Matter

1. **Psychological fuel**: Each small win releases dopamine, keeping you motivated
2. **Compounding progress**: 1% better each day = 37x better in a year
3. **Reduced perfectionism**: Ship fast, learn fast, improve fast

## My Framework

Instead of waiting for the "perfect" launch:
- Ship the MVP version today
- Get one user's feedback
- Iterate tomorrow
- Repeat

## Real Example

Last month I built a simple automation tool in 2 hours. Not perfect. Not pretty. But it saved me 30 minutes every day. That's 15 hours/month. That's real progress.

## Your Turn

What's one small win you can ship TODAY? Not this week. Not "when it's ready." Today.

The big wins take care of themselves when you stack enough small ones.
"""
        example_file.write_text(example_content, encoding='utf-8')
        print(f"✓ Created sample-post.md (test with: python repurpose.py examples/sample-post.md)")
    else:
        print("• sample-post.md already exists (skipped)")

    # Create log file
    log_file = config_dir / 'repurpose-log.json'
    if not log_file.exists():
        log_file.write_text('{"repurposings":[]}', encoding='utf-8')
        print(f"✓ Created repurpose-log.json")
    else:
        print("• repurpose-log.json already exists (skipped)")

    print("")
    print("Next steps:")
    print(f"  1. Edit {config_file} with your voice settings")
    print(f"  2. Test with sample: python repurpose.py {example_file}")
    print(f"  3. Check output in: {output_dir}/")
    print("")
    print("Pro tip: Set your voice.tone, personality, and user.primary_cta first.")
    print("")
    print("♻️  Ready to repurpose content!")


if __name__ == '__main__':
    main()

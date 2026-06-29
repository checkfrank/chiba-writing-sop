#!/usr/bin/env python3
"""
content-repurposer/scripts/repurpose.py — Main repurposing script (Windows-compatible)

Takes one long-form content source and generates platform-optimized snippets.
Usage:
    python repurpose.py <source_file_or_url> [--platforms twitter,linkedin] [--output-dir path] [--dry-run]
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime


def slugify(text, max_length=50):
    """Convert text to URL-friendly slug."""
    slug = text.lower().strip()
    # Keep alphanumeric, hyphens, underscores, Chinese chars
    slug = ''.join(c if c.isalnum() or c in '-_ ' or ord(c) > 127 else '-' for c in slug)
    slug = slug.replace(' ', '-').replace('__', '_')
    slug = slug.strip('-')
    return slug[:max_length]


def load_config(config_path):
    """Load config from JSON file."""
    if not os.path.exists(config_path):
        print(f"❌ Error: Config file not found at {config_path}")
        print("Run 'python setup.py' first.")
        sys.exit(1)
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_source(source_input):
    """Read content from file or URL."""
    content = ""
    is_url = source_input.startswith('http://') or source_input.startswith('https://')

    if is_url:
        print(f"🌐 Fetching content from URL: {source_input}")
        # Use web_fetch or read from stdin
        try:
            import urllib.request
            with urllib.request.urlopen(source_input, timeout=10) as response:
                raw = response.read()
                # Try to decode, strip HTML tags
                try:
                    content = raw.decode('utf-8')
                except UnicodeDecodeError:
                    content = raw.decode('gbk', errors='ignore')
        except Exception as e:
            print(f"⚠️  Failed to fetch URL: {e}")
            print("Try using a local file instead.")
            sys.exit(1)
    else:
        if not os.path.isfile(source_input):
            print(f"❌ Error: Source file not found at {source_input}")
            sys.exit(1)
        print(f"📄 Reading content from file: {source_input}")
        with open(source_input, 'r', encoding='utf-8') as f:
            content = f.read()

    if not content.strip():
        print("❌ Error: Could not read content from source.")
        sys.exit(1)

    return content


def main():
    parser = argparse.ArgumentParser(
        description="Transform long-form content into platform-optimized snippets."
    )
    parser.add_argument('source', help='Source file path or URL')
    parser.add_argument('--platforms', help='Comma-separated platforms (e.g., twitter,linkedin)')
    parser.add_argument('--output-dir', help='Override output directory')
    parser.add_argument('--dry-run', action='store_true', help='Print prompts instead of executing')
    args = parser.parse_args()

    # Determine paths
    skill_dir = Path(__file__).parent.parent
    config_dir = Path.home() / '.config' / 'content-repurposer'
    config_file = config_dir / 'config.json'

    # Load config
    config = load_config(str(config_file))

    # Read source
    content = read_source(args.source)

    # Prepare output directory
    output_dir = args.output_dir or config.get('output', {}).get('directory', str(Path.home() / 'content-repurposer-output'))
    output_dir = output_dir.replace('~', str(Path.home()))

    date_slug = datetime.now().strftime('%Y-%m-%d')
    source_slug = slugify(Path(args.source).stem if not args.source.startswith('http') else args.source)
    final_dir = os.path.join(output_dir, f"{date_slug}-{source_slug}")
    os.makedirs(final_dir, exist_ok=True)

    print(f"♻️  Starting content repurposing...")
    print(f"Source: {args.source}")
    print(f"Outputting to: {final_dir}")
    print("━" * 40)

    # Determine platforms
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(',')]
    else:
        platforms = []
        for name, platform_config in config.get('platforms', {}).items():
            if platform_config.get('enabled', False):
                platforms.append(name)

    # Remap platform names to script names
    script_map = {
        'twitter': 'twitter-thread',
        'linkedin': 'linkedin-post',
        'newsletter': 'newsletter',
        'instagram': 'instagram-caption',
        'threads': 'threads-post',
    }

    # Run each platform script
    for platform in platforms:
        script_name = script_map.get(platform)
        if not script_name:
            print(f"⚠️  Unknown platform: {platform}")
            continue

        script_path = skill_dir / 'scripts' / f'{script_name}.py'
        if not script_path.exists():
            print(f"⚠️  Script for platform '{platform}' not found. Skipping.")
            continue

        print(f"➡️  Processing for: {platform}")

        if args.dry_run:
            print(f"DRY RUN: Would execute python {script_path} --stdin")
            continue

        # Call the platform-specific script
        import subprocess
        result = subprocess.run(
            [sys.executable, str(script_path), '--stdin'],
            input=content,
            capture_output=True,
            text=True,
            timeout=300,
        )

        output_file = None
        if platform == 'newsletter':
            output_file = os.path.join(final_dir, f'{platform}.md')
        else:
            output_file = os.path.join(final_dir, f'{platform}.txt')

        if result.returncode == 0 and result.stdout.strip():
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"✓ Saved to {os.path.basename(output_file)}")
        else:
            print(f"❌ Failed to generate content for {platform}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")

    print("")
    print(f"✅ Repurposing complete!")
    print(f"Find your content in: {final_dir}")

    # Copy best platform to clipboard if configured
    copy_behavior = config.get('output', {}).get('copy_to_clipboard', 'none')
    if copy_behavior != 'none' and not args.dry_run:
        # Find highest priority platform that was generated
        platform_configs = config.get('platforms', {})
        best_platform = None
        best_priority = 999
        for p in platforms:
            if p in platform_configs and platform_configs[p].get('priority', 999) < best_priority:
                best_priority = platform_configs[p]['priority']
                best_platform = p

        if best_platform:
            best_file = None
            if best_platform == 'newsletter':
                best_file = os.path.join(final_dir, f'{best_platform}.md')
            else:
                best_file = os.path.join(final_dir, f'{best_platform}.txt')

            if best_file and os.path.exists(best_file):
                try:
                    with open(best_file, 'r', encoding='utf-8') as f:
                        import pyperclip
                        pyperclip.copy(f.read())
                    print(f"📋 Copied '{best_platform}' content to clipboard.")
                except ImportError:
                    print(f"⚠️  Install 'pyperclip' to enable clipboard copy: pip install pyperclip")
                except Exception as e:
                    print(f"⚠️  Clipboard copy failed: {e}")


if __name__ == '__main__':
    main()

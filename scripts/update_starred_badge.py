#!/usr/bin/env python3
"""Update SVG badge using the GitHub REST endpoint for starred repos.

This counts repositories the profile owner has STARRED, not stars RECEIVED.
It never overwrites the badge when the API fails.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import urllib.error
import urllib.request

USER = "hisokaBK"
OUT = Path(__file__).resolve().parents[1] / "assets" / "badges" / "starred.svg"


def count_starred(user: str) -> int:
    token = os.environ.get("GITHUB_TOKEN", "")
    result = 0
    page = 1
    while True:
        url = f"https://api.github.com/users/{user}/starred?per_page=100&page={page}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Hisoka-GitHub-profile-starred-badge",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                import json
                repos = json.load(response)
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            raise RuntimeError(f"GitHub API unavailable: {exc}") from exc
        if not isinstance(repos, list):
            raise RuntimeError("GitHub API did not return a list; badge remains unchanged")
        result += len(repos)
        if len(repos) < 100:
            break
        page += 1
        if page > 100:
            raise RuntimeError("Pagination limit exceeded; badge remains unchanged")
    return result


def svg_badge(n: int) -> str:
    value = str(n)
    width = max(180, 155 + 15 * len(value))
    value_x = 142 + (width-142)/2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" role="img" aria-label="Starred Repos: {value}">
  <title>Repositories starred by {USER}: {value}</title>
  <rect width="{width}" height="28" rx="6" fill="#190E2C"/>
  <path d="M135 0 H{width-6} Q{width} 0 {width} 6 V22 Q{width} 28 {width-6} 28 H135 Z" fill="#DF369F"/>
  <g fill="#FFF" font-family="DejaVu Sans, Verdana, sans-serif" font-weight="600" font-size="11">
    <text x="12" y="18">★ STARRED REPOS</text>
    <text x="{value_x:.1f}" y="18" text-anchor="middle">{value}</text>
  </g>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=None, help="Manual initial seed only (GitHub Action omits this)")
    args = parser.parse_args()
    number = args.count if args.count is not None else count_starred(USER)
    if number < 0:
        raise ValueError("Invalid negative count")
    new = svg_badge(number)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and OUT.read_text(encoding="utf-8") == new:
        print(f"Unchanged: starred repositories = {number}")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"Updated: starred repositories = {number}")


if __name__ == "__main__":
    main()

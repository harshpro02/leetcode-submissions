"""Pulls your accepted LeetCode submissions into this repo and commits them.

This is the LeetHub replacement. LeetCode serves your submitted code only to an
authenticated session, so it needs two cookies from your own browser. Put them
in a .env file next to this script (.env is gitignored and must stay that way):

    LEETCODE_SESSION=eyJ...
    CSRF_TOKEN=abc...

Get them from your browser while logged in to leetcode.com:
    DevTools (F12) -> Application -> Storage -> Cookies -> https://leetcode.com
    copy the values of LEETCODE_SESSION and csrftoken

LEETCODE_SESSION expires roughly monthly, and whenever you log in elsewhere.
When it does, this script says so plainly rather than failing silently.

    python pull_submissions.py                 fetch, write, commit
    python pull_submissions.py --push          ...and push
    python pull_submissions.py --dry-run       show what it would write
    python pull_submissions.py --limit 100     how many submissions to scan
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
ENV = ROOT / ".env"
API = "https://leetcode.com/api/submissions/"
GRAPHQL = "https://leetcode.com/graphql"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

EXT = {
    "python": "py", "python3": "py", "java": "java", "cpp": "cpp", "c": "c",
    "csharp": "cs", "javascript": "js", "typescript": "ts", "golang": "go",
    "rust": "rs", "kotlin": "kt", "swift": "swift", "ruby": "rb", "php": "php",
    "scala": "scala", "elixir": "ex", "dart": "dart", "racket": "rkt",
    "erlang": "erl", "mysql": "sql", "mssql": "sql", "oraclesql": "sql",
    "postgresql": "sql", "pythondata": "py", "bash": "sh",
}

COMMENT = {
    "py": "#", "java": "//", "cpp": "//", "c": "//", "cs": "//", "js": "//",
    "ts": "//", "go": "//", "rs": "//", "kt": "//", "swift": "//", "rb": "#",
    "php": "//", "scala": "//", "ex": "#", "dart": "//", "sql": "--", "sh": "#",
}


def load_env():
    if not ENV.exists():
        sys.exit(
            "No .env file. Create one next to this script containing:\n"
            "  LEETCODE_SESSION=...\n"
            "  CSRF_TOKEN=...\n"
            "See the docstring at the top of this file for where to find them."
        )
    values = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    session = values.get("LEETCODE_SESSION")
    csrf = values.get("CSRF_TOKEN", "")
    if not session or session == "paste_here":
        sys.exit("LEETCODE_SESSION missing from .env")
    return session, csrf


def request(url, session, csrf, data=None):
    # Cloudflare rejects requests that do not look like a browser, with a 403
    # that is easily mistaken for an expired cookie. Send the full header set.
    headers = {
        "Cookie": "LEETCODE_SESSION=" + session + "; csrftoken=" + csrf,
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://leetcode.com/submissions/",
        "Origin": "https://leetcode.com",
        "x-csrftoken": csrf,
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()

    # LeetCode throttles this endpoint and answers 403, which looks exactly like
    # a rejected cookie. Retry with backoff before concluding the session died.
    delay = 2.0
    for attempt in range(5):
        req = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429) and attempt < 4:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def fetch_submissions(session, csrf, limit):
    """Accepted submissions, newest first, deduped to one per problem."""
    seen, offset, page = {}, 0, 20
    while offset < limit:
        try:
            body = request(API + "?offset=" + str(offset) + "&limit=" + str(page),
                           session, csrf)
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                sys.exit(
                    "LeetCode rejected the request (HTTP " + str(exc.code)
                    + ") after retrying.\nEither LEETCODE_SESSION has expired, "
                    "in which case copy a fresh one into .env, or you are being\n"
                    "rate limited, in which case wait a few minutes and re-run."
                )
            raise
        dump = body.get("submissions_dump", [])
        if not dump:
            break
        for sub in dump:
            if sub.get("status_display") != "Accepted":
                continue
            seen.setdefault(sub["title_slug"], sub)
        if not body.get("has_next"):
            break
        offset += page
        time.sleep(1.5)
    return seen


def fetch_code(submission_id, session, csrf):
    """Fallback for when the list endpoint omits the code field."""
    query = (
        "query detail($id: Int!) { submissionDetails(submissionId: $id) "
        "{ code lang { name } } }"
    )
    data = request(GRAPHQL, session, csrf,
                   {"query": query, "variables": {"id": int(submission_id)}})
    details = (data.get("data") or {}).get("submissionDetails")
    return details.get("code") if details else None


_QUESTION_CACHE = {}


def describe(slug):
    if slug in _QUESTION_CACHE:
        return _QUESTION_CACHE[slug]
    query = (
        "query q($titleSlug: String!) { question(titleSlug: $titleSlug) "
        "{ questionFrontendId title difficulty } }"
    )
    payload = json.dumps({"query": query, "variables": {"titleSlug": slug}}).encode()
    req = urllib.request.Request(
        GRAPHQL, data=payload,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT,
                 "Referer": "https://leetcode.com"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        question = json.load(response)["data"]["question"]
    result = (int(question["questionFrontendId"]), question["title"],
              question["difficulty"])
    _QUESTION_CACHE[slug] = result
    return result


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit("git " + " ".join(args) + " failed:\n" + result.stderr.strip())
    return result.stdout.strip()


def build_file(number, title, difficulty, slug, sub, ext):
    marker = COMMENT.get(ext, "#")
    solved = time.strftime("%Y-%m-%d", time.localtime(int(sub["timestamp"])))
    header = (
        marker + " " + str(number) + ". " + title + " [" + difficulty + "]\n"
        + marker + " https://leetcode.com/problems/" + slug + "/\n"
        + marker + " Accepted " + solved
        + "  runtime " + str(sub.get("runtime", "n/a"))
        + "  memory " + str(sub.get("memory", "n/a")) + "\n\n"
    )
    return header


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    session, csrf = load_env()
    print("Scanning up to " + str(args.limit) + " submissions...")
    accepted = fetch_submissions(session, csrf, args.limit)
    print(str(len(accepted)) + " distinct problems accepted.\n")

    written = []
    for slug, sub in sorted(accepted.items()):
        number, title, difficulty = describe(slug)
        ext = EXT.get(sub.get("lang", ""), "txt")
        folder = ROOT / ("%04d-%s" % (number, slug))
        target = folder / ("solution." + ext)

        code = sub.get("code") or fetch_code(sub["id"], session, csrf)
        if not code:
            print("  ! no code returned for " + str(number) + ". " + title)
            continue

        body = build_file(number, title, difficulty, slug, sub, ext) + code.rstrip() + "\n"

        if target.exists() and target.read_text(encoding="utf-8") == body:
            continue

        if args.dry_run:
            print("  would write " + str(target.relative_to(ROOT)))
            written.append(target)
            continue

        folder.mkdir(exist_ok=True)
        target.write_text(body, encoding="utf-8")
        print("  wrote " + str(target.relative_to(ROOT)))
        written.append(target)

    if not written:
        print("Nothing new. Repository already matches your submissions.")
        return 0
    if args.dry_run:
        print("\nWould write " + str(len(written)) + " file(s).")
        return 0

    git("add", "-A")
    if len(written) == 1:
        subject = "Add " + written[0].parent.name
    else:
        subject = "Sync " + str(len(written)) + " accepted submissions"
    git("commit", "-m", subject)
    print("\nCommitted: " + subject)
    if args.push:
        git("push")
        print("Pushed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

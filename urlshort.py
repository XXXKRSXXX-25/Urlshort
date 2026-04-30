#!/usr/bin/env python3

import sys
import argparse
import re
from urllib.parse import urlparse
from collections import defaultdict

# 🎨 Colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    return f"""
{Colors.BOLD}{Colors.CYAN}
  urlshort - clean recon grouper 🚀
{Colors.END}
"""


# 🔥 Parse ALL formats
def parse_line(line):
    line = line.strip()
    if not line:
        return None

    match = re.search(r'https?://[^\s]+', line)
    if not match:
        return None

    url = match.group(0)
    parts = line.split()

    status = None
    length = None
    title = ""
    server = ""

    # 🔥 DIRSEARCH
    if parts and parts[0].isdigit():
        status = int(parts[0])
        size_raw = parts[1]

        if size_raw.endswith("KB"):
            length = int(float(size_raw.replace("KB", "")) * 1024)
        elif size_raw.endswith("MB"):
            length = int(float(size_raw.replace("MB", "")) * 1024 * 1024)
        elif size_raw.endswith("B"):
            length = int(size_raw.replace("B", ""))

    # 🔥 HTTPX
    matches = re.findall(r'\[(.*?)\]', line)

    if matches:
        if len(matches) > 0 and not status:
            status = matches[0]

        if len(matches) > 1 and matches[1].isdigit():
            length = int(matches[1])

        if len(matches) > 2:
            title = matches[2]

        if len(matches) > 3:
            server = matches[3]

    return {
        "url": url,
        "status": status,
        "length": length,
        "title": title,
        "server": server
    }


def read_inputs(files):
    if not files and not sys.stdin.isatty():
        for line in sys.stdin:
            yield line
    else:
        for file in files:
            try:
                with open(file, "r", errors="ignore") as f:
                    for line in f:
                        yield line
            except:
                pass


def main():
    parser = argparse.ArgumentParser(description="Clean URL grouping tool")

    parser.add_argument("-l", "--list", nargs="*", help="Input files")
    parser.add_argument("-o", "--output", help="Save output")

    # 🔥 Filters
    parser.add_argument("-ml", help="Match title")
    parser.add_argument("-ms", help="Match server")
    parser.add_argument("-mc", help="Match content length")
    parser.add_argument("-msz", help="Match size")
    parser.add_argument("-sc", help="Match status")
    parser.add_argument("-ext", help="Filter extension")

    # 🔥 NEW GROUP MODE
    parser.add_argument(
        "--group-mode",
        choices=["root", "server", "file", "path"],
        default="root",
        help="Grouping mode"
    )

    parser.add_argument("--no-color", action="store_true")

    args = parser.parse_args()

    if (not args.list) and sys.stdin.isatty():
        print(banner())
        parser.print_help()
        sys.exit(0)

    print(banner())

    groups = defaultdict(set)
    parsed_data = []

    for line in read_inputs(args.list):
        data = parse_line(line)
        if not data:
            continue

        # 🔥 Filters
        if args.sc and str(data["status"]) not in args.sc.split(","):
            continue

        if args.ml and args.ml.lower() not in data["title"].lower():
            continue

        if args.ms and args.ms.lower() not in data["server"].lower():
            continue

        if args.mc:
            if data["length"] not in set(map(int, args.mc.split(","))):
                continue

        if args.msz:
            if data["length"] not in set(map(int, args.msz.split(","))):
                continue

        if args.ext:
            if not any(data["url"].endswith("." + e.strip()) for e in args.ext.split(",")):
                continue

        parsed_data.append(data)

    # 🔥 GROUPING
    for d in parsed_data:
        url = d["url"]
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        filename = url.split("/")[-1]

        # 🔥 ROOT MODE
        if args.group_mode == "root":
            key = "root"

        # 🔥 SERVER MODE
        elif args.group_mode == "server":
            key = d["server"].lower() if d["server"] else "unknown"

        # 🔥 FILE MODE (dirsearch best)
        elif args.group_mode == "file":
            if d["length"]:
                key = f"{filename} - {d['length']}B"
            else:
                key = filename

        # 🔥 PATH MODE
        elif args.group_mode == "path":
            if path:
                parts = [p for p in path.split("/") if p]
                key = parts[-1]
            else:
                key = "root"

        groups[key].add(url)

    out = open(args.output, "w") if args.output else sys.stdout

    # 🔥 SORT by count
    keys = sorted(groups.keys(), key=lambda k: len(groups[k]), reverse=True)

    for key in keys:
        header = f"\n### {key} ({len(groups[key])})\n"

        if not args.no_color:
            header = f"\n{Colors.BOLD}{Colors.CYAN}### {key}{Colors.YELLOW} ({len(groups[key])}){Colors.END}\n"

        out.write(header)

        for url in sorted(groups[key]):
            line = url

            if not args.no_color:
                line = f"{Colors.GREEN}{line}{Colors.END}"

            out.write(line + "\n")

    if args.output:
        out.close()
        print(f"{Colors.GREEN}[+] Saved to {args.output}{Colors.END}")


if __name__ == "__main__":
    main()
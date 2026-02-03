"""Fetch xkcd comics and write chunked JSONL files.

Usage:
  python fetch_xkcd.py --start 1 --end 2600 --chunk-size 100 --outdir training --download-images

Defaults:
  - If --end is omitted, the script will query the latest comic automatically.
  - Each record contains: num, title, alt, transcript, img, day/month/year, license, attribution
"""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from tqdm import tqdm
except Exception:
    tqdm = lambda x, **kwargs: x  # type: ignore

LICENSE = "CC BY-NC 2.5"
ATTRIBUTION = "xkcd — Randall Munroe"


def session_with_retries(backoff_factor: float = 0.3, total_retries: int = 5) -> requests.Session:
    s = requests.Session()
    retries = Retry(total=total_retries, backoff_factor=backoff_factor, status_forcelist=(500, 502, 503, 504))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


def get_latest_num(session: requests.Session) -> int:
    resp = session.get("https://xkcd.com/info.0.json", timeout=10)
    resp.raise_for_status()
    return int(resp.json()["num"])


def fetch_comic(session: requests.Session, num: int) -> Optional[Dict]:
    url = f"https://xkcd.com/{num}/info.0.json"
    try:
        r = session.get(url, timeout=10)
        if r.status_code == 404:
            # some numbers may not exist
            return None
        r.raise_for_status()
        data = r.json()
        record = {
            "num": data.get("num"),
            "title": data.get("title"),
            "alt": data.get("alt"),
            "transcript": data.get("transcript"),
            "img": data.get("img"),
            "year": data.get("year"),
            "month": data.get("month"),
            "day": data.get("day"),
            "license": LICENSE,
            "attribution": ATTRIBUTION,
            "source_url": f"https://xkcd.com/{num}/",
        }
        return record
    except Exception:
        return None


def download_image(session: requests.Session, url: str, dest_path: str) -> bool:
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        r = session.get(url, stream=True, timeout=20)
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(1024 * 8):
                if chunk:
                    f.write(chunk)
        return True
    except Exception:
        return False


def write_jsonl_chunk(records: List[Dict], out_dir: str, prefix: str, index: int) -> str:
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{prefix}-{index:04d}.jsonl"
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return path


def parse_args():
    p = argparse.ArgumentParser(description="Fetch xkcd comics into chunked JSONL files")
    p.add_argument("--start", type=int, default=1, help="Start comic number (inclusive)")
    p.add_argument("--end", type=int, default=None, help="End comic number (inclusive). If omitted, uses latest.")
    p.add_argument("--chunk-size", type=int, default=100, help="Number of records per JSONL chunk")
    p.add_argument("--outdir", type=str, default="training", help="Output directory for JSONL files")
    p.add_argument("--prefix", type=str, default="xkcd-archive", help="Prefix for output files")
    p.add_argument("--download-images", action="store_true", help="Also download comic images into outdir/images")
    p.add_argument("--sample", type=int, default=None, help="Fetch only the first N comics starting from --start (for quick test)")
    p.add_argument("--delay", type=float, default=0.5, help="Delay (seconds) between requests")
    return p.parse_args()


def main():
    args = parse_args()
    s = session_with_retries()

    end = args.end
    if end is None:
        end = get_latest_num(s)

    if args.sample:
        end = args.start + args.sample - 1

    records = []
    chunk_index = 1
    saved_files = []
    image_dir = os.path.join(args.outdir, "images") if args.download_images else None

    for num in tqdm(range(args.start, end + 1)):
        rec = fetch_comic(s, num)
        if rec is None:
            # skip missing or error
            continue
        if args.download_images and rec.get("img"):
            img_url = rec["img"]
            img_name = f"{rec['num']}-{os.path.basename(img_url.split('?')[0])}"
            img_path = os.path.join(image_dir, img_name)
            success = download_image(s, img_url, img_path)
            if success:
                rec["local_img"] = img_path
        records.append(rec)
        if len(records) >= args.chunk_size:
            path = write_jsonl_chunk(records, args.outdir, args.prefix, chunk_index)
            saved_files.append(path)
            chunk_index += 1
            records = []
        time.sleep(args.delay)

    if records:
        path = write_jsonl_chunk(records, args.outdir, args.prefix, chunk_index)
        saved_files.append(path)

    print("Saved:")
    for p in saved_files:
        print(" -", p)


if __name__ == "__main__":
    main()

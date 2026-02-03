# xkcd archive importer 🔧

This folder contains a small utility to fetch the xkcd archive and store it as chunked JSONL files.

Scripts:
- `fetch_xkcd.py` — CLI tool to download metadata (and optionally images) and write chunked JSONL files.

Usage example:

```bash
python fetch_xkcd.py --start 401 --chunk-size 100 --outdir training --sample 50
```

Notes:
- Each record contains `num`, `title`, `alt`, `transcript`, `img`, `year/month/day`, `license`, and `attribution`.
- Default license: `CC BY-NC 2.5` and attribution `xkcd — Randall Munroe`.
- Images are not downloaded by default; use `--download-images` to enable.

Testing:
- The `--sample` flag is useful to do a quick sanity run before a full fetch.

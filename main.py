import argparse, time, csv, requests
from datetime import datetime
def main():
    p = argparse.ArgumentParser(description="URL uptime & latency logger")
    p.add_argument("--urls", required=True, help="file with one URL per line")
    p.add_argument("--out", default="uptime.csv")
    args = p.parse_args()
    with open(args.urls) as f: urls=[u.strip() for u in f if u.strip()]
    with open(args.out, "a", newline="") as fp:
        w = csv.writer(fp); w.writerow(["ts","url","status","ms"])
        for url in urls:
            t0=time.time()
            try:
                r=requests.get(url, timeout=10)
                ms=int((time.time()-t0)*1000)
                w.writerow([datetime.utcnow().isoformat(), url, r.status_code, ms])
            except Exception:
                ms=int((time.time()-t0)*1000)
                w.writerow([datetime.utcnow().isoformat(), url, "ERR", ms])
    print(f"Wrote {args.out}")
if __name__ == "__main__":
    main()

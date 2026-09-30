"""Critic: pull independent external data (run 2026-09-30 ~04:45 UTC). Saves to external/.
 1. SEC EDGAR submissions JSON for MU -> all 8-K filings with acceptance timestamps (earnings-date + timing check).
 2. Nasdaq.com historical daily bars for MU (second price vendor, ~10y) -> external/nasdaq_mu_daily.csv
 3. For a peer/high-attention panel: SEC 8-K item 2.02 filings + Yahoo chart daily bars (cross-sectional test
    of 'short day-1 open after an after-close print').
Nothing here is used for trading. Read-only public endpoints.
"""
import json, os, sys, time, urllib.request, pandas as pd

OUT = "external"; os.makedirs(OUT, exist_ok=True)
UA_SEC = {"User-Agent": "independent research critic contact@example.com", "Accept-Encoding": "gzip, deflate"}
UA_WEB = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

def get(url, headers, retries=3, sleep=1.0):
    for k in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    import gzip; data = gzip.decompress(data)
                return data
        except Exception as ex:
            err = ex; time.sleep(sleep * (k + 1))
    raise err

def sec_filings(cik):
    """All filings for a CIK (recent + older index files) as a DataFrame."""
    cik10 = f"{int(cik):010d}"
    j = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik10}.json", UA_SEC))
    frames = []
    rec = j["filings"]["recent"]
    frames.append(pd.DataFrame({k: rec[k] for k in ["accessionNumber", "filingDate", "reportDate", "acceptanceDateTime", "form", "items"]}))
    for f in j["filings"].get("files", []):
        time.sleep(0.3)
        jj = json.loads(get("https://data.sec.gov/submissions/" + f["name"], UA_SEC))
        frames.append(pd.DataFrame({k: jj[k] for k in ["accessionNumber", "filingDate", "reportDate", "acceptanceDateTime", "form", "items"]}))
    df = pd.concat(frames, ignore_index=True)
    df["name"] = j["name"]
    return df

def yahoo_daily(sym, p1=1000000000, p2=1800000000):
    j = None
    for host in ["query2", "query1"]:   # query1 rate-limits (429) from this host; query2 does not
        url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d&events=div,splits"
        try:
            j = json.loads(get(url, {"User-Agent": "Mozilla/5.0"}, retries=2))["chart"]["result"][0]; break
        except Exception as ex:
            err = ex
    if j is None: raise err
    q = j["indicators"]["quote"][0]
    df = pd.DataFrame({"Open": q["open"], "High": q["high"], "Low": q["low"], "Close": q["close"], "Volume": q["volume"]},
                      index=pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York").normalize().tz_localize(None))
    df.index.name = "Date"
    splits = j.get("events", {}).get("splits", {})
    sp = pd.Series({pd.to_datetime(v["date"], unit="s", utc=True).tz_convert("America/New_York").normalize().tz_localize(None): v["numerator"] / v["denominator"] for v in splits.values()}, dtype=float)
    return df.dropna(subset=["Open", "Close"]), sp

def nasdaq_daily(sym):
    url = f"https://api.nasdaq.com/api/quote/{sym}/historical?assetclass=stocks&fromdate=2001-01-01&todate=2026-09-30&limit=10000"
    h = dict(UA_WEB); h.update({"Accept": "application/json", "Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"})
    rows = json.loads(get(url, h))["data"]["tradesTable"]["rows"]
    df = pd.DataFrame(rows)
    for c in ["close", "open", "high", "low"]:
        df[c] = df[c].str.replace("$", "", regex=False).str.replace(",", "").astype(float)
    df["volume"] = df["volume"].str.replace(",", "").astype(float)
    df["Date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    return df.set_index("Date").sort_index()[["open", "high", "low", "close", "volume"]].rename(columns=str.capitalize)

def cboe_chain(sym):
    """CBOE delayed quotes (all expiries) -> parsed CSV with bid/ask/iv/oi/volume per contract."""
    import re
    j = json.loads(get(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json", UA_WEB))
    rows = []
    for o in j["data"]["options"]:
        m = re.match(rf"{sym}(\d{{6}})([CP])(\d{{8}})", o["option"])
        if m: rows.append(dict(exp="20" + m.group(1), cp=m.group(2), K=int(m.group(3)) / 1000, bid=o["bid"], ask=o["ask"], iv=o.get("iv"), oi=o.get("open_interest"), vol=o.get("volume"), delta=o.get("delta"), last=o.get("last_trade_price")))
    df = pd.DataFrame(rows); df["spr"] = df.ask - df.bid
    return j.get("timestamp"), j["data"].get("current_price"), df

if __name__ == "__main__":
    what = sys.argv[1:] or ["mu", "panel", "chain"]
    if "chain" in what:
        ts, spot, ch = cboe_chain("MU"); ch.to_csv(f"{OUT}/cboe_mu_chain_2026-09-29_close.csv", index=False)
        print("CBOE MU chain:", ts, "spot", spot, len(ch), "contracts")
    if "mu" in what:
        f = sec_filings(723125); f.to_csv(f"{OUT}/sec_filings_MU.csv", index=False)
        print("MU SEC filings:", len(f), f.filingDate.min(), f.filingDate.max(), "8-Ks:", (f.form.str.startswith("8-K")).sum())
        n = nasdaq_daily("MU"); n.to_csv(f"{OUT}/nasdaq_mu_daily.csv")
        print("Nasdaq MU daily:", len(n), n.index.min().date(), n.index.max().date())
    if "panel" in what:
        panel = {"NVDA": 1045810, "AMD": 2488, "INTC": 50863, "WDC": 106040, "STX": 1137789, "LRCX": 707549, "AMAT": 6951,
                 "TXN": 97476, "QCOM": 804328, "AAPL": 320193, "NFLX": 1065280, "TSLA": 1318605, "META": 1326801, "AMZN": 1018724,
                 "MSFT": 789019, "KLAC": 319201, "ON": 1097864, "MRVL": 1835632, "SWKS": 4127, "MCHP": 827054}
        for sym, cik in panel.items():
            try:
                fp = f"{OUT}/sec_filings_{sym}.csv"
                if os.path.exists(fp): f = pd.read_csv(fp)
                else: f = sec_filings(cik); f.to_csv(fp, index=False)
                d, sp = yahoo_daily(sym); d.to_csv(f"{OUT}/yahoo_{sym}_daily.csv"); sp.to_csv(f"{OUT}/yahoo_{sym}_splits.csv", header=["ratio"])
                print(sym, "filings", len(f), "8-K 2.02:", f["items"].fillna("").str.contains("2.02").sum(), "| daily", len(d), d.index.min().date(), d.index.max().date(), "| splits", len(sp))
            except Exception as ex:
                print(sym, "FAILED", repr(ex)[:200])
            time.sleep(1.0)

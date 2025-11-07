import requests
from bs4 import BeautifulSoup
import pandas as pd
import time, random

BASE = "https://www.ebi.ac.uk/merops/cgi-bin/substrates?id={merops_id}"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; biomarker-scraper/1.0)"}

proteases = {
    "Neutrophil elastase (ELANE)": "S01.131",
    "Proteinase 3 (PRTN3)": "S01.132",
    "Cathepsin G (CTSG)": "S01.133",
    "MMP8 (Collagenase-2)": "M10.002",
    "MMP9 (Gelatinase B)": "M10.004",
    "Thrombin (F2, coagulation factor IIa)": "S01.217",
    "Plasmin": "S01.233",
    "Caspase-1": "C14.001",
    "NSP1": "S01.134",
    "NSP2": "S01.135",
    "Granzyme B": "S01.021",
    "Kallikrein 1": "S01.070",
    "Kallikrein 2": "S01.071",
    "MMP1 (Collagenase-1)": "M10.001",
    "MMP2 (Gelatinase A)": "M10.003",
    "MMP7 (Matrilysin)": "M10.005",
    "MMP12 (Macrophage metalloelastase)": "M10.006",
    "Factor VIIa": "S01.220",
    "Factor IXa": "S01.221",
    "Factor Xa": "S01.222",
    "tPA": "S01.234",
    "Urokinase": "S01.235",
    "Caspase-3": "C14.002",
    "Caspase-6": "C14.003",
    "Caspase-7": "C14.004",
    "Caspase-8": "C14.005",
    "Caspase-9": "C14.006",
}

def make_negatives(seq, n=2):
    negatives = []
    for _ in range(n):
        s = list(seq)
        random.shuffle(s)
        negatives.append("".join(s))
    return negatives

all_rows = []

for name, merops_id in proteases.items():
    url = BASE.format(merops_id=merops_id)
    print(f"Fetching substrates for {name} ({merops_id}) from {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  [WARN] Failed to fetch {name}: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"  [WARN] No substrate table found for {name}")
        continue

    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    rows_parsed = 0
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if not cells:
            continue

        row = dict(zip(headers[:len(cells)], cells))
        seq = row.get("Substrate", None)
        if not seq:
            continue


        row["Protease_Name"] = name
        row["MEROPS_ID"] = merops_id
        row["Label"] = 1
        all_rows.append(row)


        for neg_seq in make_negatives(seq, n=2):
            neg_row = row.copy()
            neg_row["Substrate"] = neg_seq
            neg_row["Label"] = 0
            all_rows.append(neg_row)

        rows_parsed += 1

    print(f"  -> Parsed {rows_parsed} positives (+ {rows_parsed*2} negatives).")
    time.sleep(0.5)


df = pd.DataFrame(all_rows)
import os

# Define a writable path for the output CSV file
output_dir = os.path.expanduser("~/Documents/AET Senior Research")  # Change this to your desired directory
out_csv = os.path.join(output_dir, "MEROPS_sepsis_expanded_dataset.csv")

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the DataFrame to the writable path
df.to_csv(out_csv, index=False)
print(f"Data saved to {out_csv}")


"""
SigWatcher: анализ SIGHASH-флагов и типов подписей в Bitcoin-транзакциях.
"""

import requests
import argparse

SIGHASH_TYPES = {
    0x01: "ALL",
    0x02: "NONE",
    0x03: "SINGLE",
    0x81: "ALL|ANYONECANPAY",
    0x82: "NONE|ANYONECANPAY",
    0x83: "SINGLE|ANYONECANPAY"
}

def get_transaction(txid):
    url = f"https://api.blockchair.com/bitcoin/raw/transaction/{txid}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Ошибка получения транзакции.")
    return r.json()["data"][txid]["decoded_raw_transaction"]

def analyze_signatures(tx):
    results = []
    for vin in tx.get("vin", []):
        scriptsig = vin.get("script_sig", {}).get("asm", "")
        witness = vin.get("txinwitness", [])
        sigs = []

        # Legacy подписи
        if scriptsig:
            parts = scriptsig.split()
            for part in parts:
                if part.endswith("01") or part.endswith("02") or part.endswith("03") or part.endswith("81") or part.endswith("82") or part.endswith("83"):
                    try:
                        sighash_flag = int(part[-2:], 16)
                        sigs.append(sighash_flag)
                    except:
                        continue

        # SegWit подписи
        for w in witness:
            if isinstance(w, str) and len(w) > 2:
                try:
                    sighash_flag = int(w[-2:], 16)
                    sigs.append(sighash_flag)
                except:
                    continue

        for sig in sigs:
            decoded = SIGHASH_TYPES.get(sig, f"Неизвестен ({sig})")
            results.append(decoded)
    return results

def sigwatch(txid):
    print(f"🔍 Анализ сигнатур в транзакции: {txid}")
    tx = get_transaction(txid)
    flags = analyze_signatures(tx)
    if not flags:
        print("✅ Подписей не найдено или они нестандартны.")
        return
    for i, flag in enumerate(flags):
        print(f"🖋️ Подпись #{i+1}: {flag}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SigWatcher — анализ флагов SIGHASH в подписях.")
    parser.add_argument("txid", help="TXID транзакции")
    args = parser.parse_args()
    sigwatch(args.txid)

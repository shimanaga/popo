#!/usr/bin/env python3
"""suggest_rate_fixed.py - corrected full version

Produces proposals for increasing B2 based on an ODS file containing song scores.
This is a standalone script. Edit DEFAULT_FILE_PATH at the top if needed.
"""

from typing import Optional, List, Dict, Any, Tuple
import argparse, csv, sys
import pandas as pd

# -------------------- Configuration constants (editable) --------------------
DEFAULT_FILE_PATH = "data.ods"   # <-- default input file path
DEFAULT_MAX_SUGGESTIONS = 3                # <-- default number of suggestions to output
# ---------------------------------------------------------------------------

DIFFICULTY_RANGES = {
    "14+": (14.5, 14.9),
    "15": (15.0, 15.4),
    "15+": (15.5, 15.9),
    "16": (16.0, 16.9),
}


def read_ods(path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, engine="odf")
    except Exception as e:
        raise RuntimeError(f"Failed to read ODS '{path}': {e}")
    return df


def pick_columns(df: pd.DataFrame):
    cols = list(df.columns)
    lower = {c.strip().lower(): c for c in cols}
    def find(cands):
        for c in cands:
            if c.lower() in lower:
                return lower[c.lower()]
        return None
    #song_col = find(["song", "title", "曲名", "name"]) or (cols[0] if len(cols)>0 else None)
    song_col = cols[1]
    diff_col = cols[2]
    d_col = cols[3]
    score_col = cols[4]
    return song_col, diff_col, d_col, score_col


def calc_G(score: int) -> float:
    E = int(score)
    if E <= 800000:
        return 0.0
    if E <= 970000:
        return (E - 800000) / 170000.0
    if E <= 990000:
        return (E - 970000) / 20000.0
    if E <= 995000:
        return (E - 990000) / 10000.0 + 1.0
    if E <= 999000:
        return (E - 995000) / 8000.0 + 1.5
    if E <= 1000000:
        return (E - 999000) / 10000.0 + 2.0
    return (E - 999000) / 10000.0 + 2.0


def calc_single_rate(D: float, score: int) -> float:
    E = int(score)
    if E <= 800000:
        return 0.0
    if E <= 970000:
        return (E - 800000) / 170000.0
    if E <= 990000:
        return (E - 970000) / 20000.0
    if E <= 995000:
        return (E - 990000) / 10000.0 + 1.0
    # E > 995000: top branch
    G = calc_G(E)
    return (D + G) / 34.0 * 40.0


def compute_table(df_raw: pd.DataFrame) -> pd.DataFrame:
    song_col, diff_col, d_col, score_col = pick_columns(df_raw)
    if song_col is None:
        raise RuntimeError("Could not detect song/title column.")
    df = pd.DataFrame()
    df["song"] = df_raw[song_col].astype(str)
    df["difficulty"] = df_raw[diff_col] if diff_col is not None and diff_col in df_raw.columns else pd.NA
    df["D"] = pd.to_numeric(df_raw[d_col], errors="coerce") if d_col is not None and d_col in df_raw.columns else pd.NA
    if score_col is not None and score_col in df_raw.columns:
        df["score"] = pd.to_numeric(df_raw[score_col], errors="coerce").fillna(0).astype(int)
    else:
        df["score"] = 0
    df["G"] = df["score"].apply(calc_G)
    df["F"] = df.apply(lambda r: calc_single_rate(float(r["D"]) if not pd.isna(r["D"]) else 0.0, int(r["score"])), axis=1)
    return df


def compute_B2_from_Fs(Fs: List[float]) -> float:
    top = sorted(Fs, reverse=True)[:40]
    if len(top) == 0:
        return 0.0
    return float(sum(top) / len(top))


def recompute_B2_with_updated_row(df: pd.DataFrame, idx: int, new_score: int) -> float:
    Fs = df["F"].tolist()
    D = float(df.loc[idx, "D"]) if not pd.isna(df.loc[idx, "D"]) else 0.0
    newF = calc_single_rate(D, new_score)
    Fs[idx] = newF
    return compute_B2_from_Fs(Fs)


def find_min_score_to_reach_target(df: pd.DataFrame, idx: int, target_B2: float, max_score: int = 1000000) -> Optional[int]:
    current_B2 = compute_B2_from_Fs(df["F"].tolist())
    if current_B2 >= target_B2 - 1e-12:
        return int(df.loc[idx, "score"])
    b2_at_max = recompute_B2_with_updated_row(df, idx, max_score)
    if b2_at_max < target_B2 - 1e-9:
        return None
    lo = int(df.loc[idx, "score"])
    hi = max_score
    while lo < hi:
        mid = (lo + hi) // 2
        b2 = recompute_B2_with_updated_row(df, idx, mid)
        if b2 >= target_B2 - 1e-12:
            hi = mid
        else:
            lo = mid + 1
    return lo


def difficulty_filter_indices(df: pd.DataFrame, label: str) -> List[int]:
    rng = DIFFICULTY_RANGES.get(label)
    if rng is None:
        return []
    lo, hi = rng
    idxs = [i for i, v in df["D"].iteritems() if (not pd.isna(v) and lo <= float(v) <= hi)]
    return idxs


def dcfmt(v):
    return "" if pd.isna(v) else v


def propose(df: pd.DataFrame, difficulty: Optional[str], target: Optional[float], max_suggestions: int = DEFAULT_MAX_SUGGESTIONS):
    dfc = df.copy().reset_index(drop=True)
    current_B2 = compute_B2_from_Fs(dfc["F"].tolist())

    if difficulty is not None:
        candidates = difficulty_filter_indices(dfc, difficulty)
    else:
        candidates = list(range(len(dfc)))

    proposals = []

    if target is not None:
        for i in candidates:
            cur_score = int(dfc.loc[i, "score"])
            if cur_score >= 1000000:
                continue
            min_score = find_min_score_to_reach_target(dfc, i, target, max_score=1000000)
            if min_score is None:
                continue
            newF = calc_single_rate(float(dfc.loc[i, "D"]) if not pd.isna(dfc.loc[i, "D"]) else 0.0, min_score)
            newB2 = recompute_B2_with_updated_row(dfc, i, min_score)
            proposals.append({
                "index": i,
                "song": str(dfc.loc[i, "song"]),
                "difficulty": dcfmt(dfc.loc[i, "difficulty"]),
                "D": float(dfc.loc[i, "D"]) if not pd.isna(dfc.loc[i, "D"]) else None,
                "current_score": int(dfc.loc[i, "score"]),
                "target_score": int(min_score),
                "current_F": float(dfc.loc[i, "F"]),
                "new_F": float(newF),
                "new_B2": float(newB2),
            })
        proposals = sorted(proposals, key=lambda x: (x["target_score"], -x["new_B2"]))[:max_suggestions]
    else:
        # Default proposals: find underperforming songs among peers (D +/- 0.4)
        n = len(dfc)
        peers_window = 0.4
        for i in range(n):
            if pd.isna(dfc.loc[i, "D"]):
                continue
            Dv = float(dfc.loc[i, "D"])
            peers = [j for j in range(n) if (not pd.isna(dfc.loc[j, "D"]) and abs(float(dfc.loc[j, "D"]) - Dv) <= peers_window)]
            if len(peers) < 4:
                continue
            Fs_peers = [float(dfc.loc[j, "F"]) for j in peers]
            Fs_sorted = sorted(Fs_peers)
            curF = float(dfc.loc[i, "F"])
            worse_or_equal = sum(1 for v in Fs_peers if v <= curF)
            percentile = worse_or_equal / len(Fs_peers)
            if percentile > 0.35:
                continue
            idx_75 = max(0, int(0.75 * len(Fs_sorted)) - 1)
            targetF = Fs_sorted[idx_75]
            cur_score = int(dfc.loc[i, "score"])
            lo = cur_score
            hi = 1000000
            achievable = None
            while lo <= hi:
                mid = (lo + hi) // 2
                newF = calc_single_rate(float(dfc.loc[i, "D"]), mid)
                if newF >= targetF - 1e-12:
                    achievable = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            if achievable is None:
                if recompute_B2_with_updated_row(dfc, i, 999000) > current_B2:
                    achievable = 999000
                else:
                    continue
            newF = calc_single_rate(float(dfc.loc[i, "D"]), achievable)
            newB2 = recompute_B2_with_updated_row(dfc, i, achievable)
            deltaB2 = newB2 - current_B2
            if deltaB2 <= 1e-9:
                continue
            proposals.append({
                "index": i,
                "song": str(dfc.loc[i, "song"]),
                "difficulty": dcfmt(dfc.loc[i, "difficulty"]),
                "D": float(dfc.loc[i, "D"]),
                "current_score": int(dfc.loc[i, "score"]),
                "target_score": int(achievable),
                "current_F": float(dfc.loc[i, "F"]),
                "new_F": float(newF),
                "new_B2": float(newB2),
                "deltaB2": float(deltaB2),
                "peer_percentile": float(percentile),
            })
        proposals = sorted(proposals, key=lambda x: (-x["deltaB2"], x["target_score"]))[:max_suggestions]

    summary = {"current_B2": current_B2, "num_songs": len(dfc)}
    return summary, proposals


def print_proposals(summary: Dict[str, Any], proposals: List[Dict[str, Any]]):
    print(f"Current B2 (top-40 average): {summary['current_B2']:.5f} (based on {summary['num_songs']} songs)")
    if not proposals:
        print("No candidate proposals found under the given constraints.")
        return
    for i, p in enumerate(proposals, start=1):
        print(f"Proposal #{i}:")
        print(f"  楽曲名: {p['song']}")
        print(f"  難易度: {p.get('difficulty', '')} 譜面定数: {p.get('D', '')}")
        print(f"  現在のスコア: {p['current_score']}   現在の単レ: {p['current_F']:.5f}")
        print(f"  このスコア出せ: {p['target_score']}   予想単レ: {p['new_F']:.5f}")
        print(f"  総合レート上昇: {p['new_B2']:.5f}")
        if 'deltaB2' in p:
            print(f"  Expected delta B2: {p['deltaB2']:.5f}")
        if 'peer_percentile' in p:
            print(f"  Peer-percentile (lower => underperforming): {p['peer_percentile']:.3f}")

def write_csv(path: str, proposals: List[Dict[str, Any]]):
    if not proposals:
        return
    keys = list(proposals[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for p in proposals:
            writer.writerow(p)

def parse_args():
    parser = argparse.ArgumentParser(description="Suggest songs & target scores to raise B2.")
    parser.add_argument('--file', required=False, default=DEFAULT_FILE_PATH, help='Path to ODS file')
    parser.add_argument('--difficulty', required=False, help='Difficulty filter: 14+, 15, 15+, 16')
    parser.add_argument('--target', type=float, required=False, help='Target B2 (e.g. 1.200)')
    parser.add_argument('--max', type=int, default=DEFAULT_MAX_SUGGESTIONS, help='Max number of suggestions')
    parser.add_argument('--out', required=False, help='CSV output path for suggestions')
    return parser.parse_args()

def main():
    t = ""
    args = parse_args()
    df_raw = read_ods(args.file)
    df = compute_table(df_raw)
    summary, proposals = propose(df, args.difficulty, args.target, args.max)
    t += "現在の総合レート: {:.5f} (14+以上{}曲)\n".format(summary['current_B2'],summary['num_songs'])
    if not proposals:
        t += "おすすめ楽曲の代わりにボブが出現しました。"
        return t
    else:
        for i, p in enumerate(proposals, start=1):
            t += "提案#{}:\n".format(i)
            t += "  楽曲名: {}\n".format(p['song'])
            t += "  難易度: {} 譜面定数: {}\n".format(p.get('difficulty',''), p.get('D',''))
            t += "  現在のスコア: {}   現在の単曲レート: {:.5f}\n".format(p['current_score'], p['current_F'])
            t += "  このスコア出せ: {}   予想単曲レート: {:.5f}\n".format(p['target_score'], p['new_F'])
            t += "  予想総合レート: {:.5f}\n".format(p['new_B2'])
            if 'deltaB2' in p:
                t += "  レート上昇: {:.5f}\n".format(p['deltaB2'])
            if 'peer_percentile' in p:
                t += "  P値: {:.3f}\n".format(p['peer_percentile'])
        return t

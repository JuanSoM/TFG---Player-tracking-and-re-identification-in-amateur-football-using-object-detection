#!/usr/bin/env python3
"""
eval_reid.py

Evaluación de ReID con:
  - Split consulta/galería con distancia temporal (--step)
  - Múltiples consultas por ID (--nq)
  - Cálculo de CMC (Rank-1/5/10) y mAP en streaming
  - Impresión de ejemplos de top-5 por consulta (--show-examples)
"""
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
from tqdm import tqdm
from collections import defaultdict

def split_q_g_by_step(ids, step, nq):
    """
    Selecciona como consultas los índices [0, step, 2*step, ...], hasta nq por bloque,
    y el resto como galería. Garantiza que cada consulta tenga al menos otra muestra
    de la misma ID en la galería.
    """
    N = len(ids)
    q_idxs = []
    for start in range(0, N, step):
        block = list(range(start, min(start+step, N)))
        # agrupa block por ID
        by_id = defaultdict(list)
        for i in block:
            by_id[ids[i]].append(i)
        for pid, idxs in by_id.items():
            # toma hasta nq consultas por ID en este bloque
            if len(idxs) < 2:
                continue
            q_for_pid = idxs[:nq]
            # filtrar aquellas que tengan al menos otro idx fuera de q_for_pid
            for qi in q_for_pid:
                if any(j!=qi and ids[j]==pid for j in range(N) if j not in q_for_pid):
                    q_idxs.append(qi)
    q_idxs = sorted(set(q_idxs))
    g_mask = np.ones(N, dtype=bool)
    g_mask[q_idxs] = False
    g_idxs = np.nonzero(g_mask)[0]
    return np.array(q_idxs), g_idxs

def evaluate(feats, ids, topk=(1,5,10), batch_size=200, step=500, nq=1, show_examples=0):
    # 1) split Q/G
    q_idxs, g_idxs = split_q_g_by_step(ids, step, nq)
    fq, iq = feats[q_idxs], ids[q_idxs]
    fg, ig = feats[g_idxs], ids[g_idxs]

    Q, G = len(iq), len(ig)
    print(f">>> Consultas Q={Q}, Galería G={G}")

    firsts, aps = [], []
    examples = []

    # 2) streaming
    for st in tqdm(range(0, Q, batch_size), desc="Eval ReID"):
        en = min(st + batch_size, Q)
        dmat = np.linalg.norm(fq[st:en, None, :] - fg[None, :, :], axis=2)  # (B, G)
        for i in range(en - st):
            dr = dmat[i]
            order = np.argsort(dr)
            matches = (ig[order] == iq[st + i])
            # CMC
            if matches.any():
                firsts.append(np.argmax(matches))
            # mAP
            aps.append(average_precision_score(matches.astype(int), -dr))
            # ejemplos
            if show_examples > 0 and len(examples) < show_examples:
                top5 = order[:5]
                examples.append({
                    "q_idx": int(q_idxs[st+i]),
                    "q_id": int(iq[st+i]),
                    "top5_idxs": top5.tolist(),
                    "top5_ids": ig[top5].tolist(),
                    "top5_dist": dr[top5].tolist()
                })

    # 3) CMC→Rank-k
    maxr = max(topk)
    cnt = np.zeros(maxr, dtype=int)
    for fpos in firsts:
        if fpos < maxr:
            cnt[fpos] += 1
    cmc = np.cumsum(cnt) / len(firsts)
    rankk = {f"Rank-{k}": cmc[k-1] for k in topk}

    # 4) mAP
    mAP = float(np.mean(aps))

    # 5) report
    print("\n--- ReID Results ---")
    for k, v in rankk.items():
        print(f"{k}: {v:.2%}")
    print(f"mAP: {mAP:.2%}\n")

    # 6) ejemplos
    if examples:
        print(f"--- Top-{5} ejemplos de consulta vs galerías ---")
        for ex in examples:
            print(f"q_idx={ex['q_idx']} (ID={ex['q_id']}):")
            for rank,(gi,gid,dist) in enumerate(zip(ex["top5_idxs"], ex["top5_ids"], ex["top5_dist"]),1):
                print(f"  {rank:>2d}. gal_idx={gi} (ID={gid}), dist={dist:.4f}")
        print()

    return rankk, mAP

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="Evalúa ReID con split temporal, multi-consulta y muestra ejemplos."
    )
    p.add_argument("--feats", required=True, help="ruta a feats.npy")
    p.add_argument("--ids",   required=True, help="ruta a ids.npy")
    p.add_argument("--out_csv", default="reid_report.csv")
    p.add_argument("--batch-size", type=int, default=200)
    p.add_argument("--step",       type=int, default=500,
                   help="intervalo temporal para separar bloques de consultas")
    p.add_argument("--nq",         type=int, default=1,
                   help="número de queries por ID en cada bloque")
    p.add_argument("--show-examples", type=int, default=0,
                   help="cuántos ejemplos de top-5 imprimir")
    args = p.parse_args()

    feats = np.load(args.feats)
    ids   = np.load(args.ids)
    rankk, mAP = evaluate(
        feats, ids,
        batch_size=args.batch_size,
        step=args.step,
        nq=args.nq,
        show_examples=args.show_examples
    )
    row = {**rankk, "mAP": mAP}
    pd.DataFrame([row]).to_csv(args.out_csv, index=False, float_format="%.4f")
    print(f"Reporte guardado en {args.out_csv}")

#python eval_reid.py  --feats feats.npy  --ids   ids.npy  --step 500 --nq 2 --show-examples 3 --out_csv realistic_reid.csv
#!/usr/bin/env python3
"""
Script mejorado para extraer embeddings con torchreid y evaluar ReID (Rank-k y mAP).
Incluye barra de progreso y mensajes de estado cada N frames.
"""
import os
import argparse
import cv2
import numpy as np
import torch
from torchreid.reid.utils import FeatureExtractor
from sklearn.metrics import average_precision_score
from tqdm import tqdm

# ---------- Utilidades ----------
def find_frame_path(frames_dir, fnum):
    """
    Busca recursivamente el archivo JPG con nombre fnum (000001.jpg) en frames_dir.
    """
    target = f"{fnum:06d}.jpg"
    for root, _, files in os.walk(frames_dir):
        if target in files:
            return os.path.join(root, target)
    return None

# ---------- Extracción de embeddings ----------
def extract_embeddings(frames_dir, mot_corr_txt, extractor, out_feats, out_ids, log_interval=100):
    """
    Extrae embeddings de cada detección en mot_corr_txt.
    Muestra progreso y guarda feats (N,D) e ids (N,) como .npy.
    """
    # Leer MOT corregido
    mot = {}
    with open(mot_corr_txt, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            fnum = int(float(parts[0])); tid = int(float(parts[1]))
            x, y, w, h = map(float, parts[2:6])
            mot.setdefault(fnum, []).append((tid, (x, y, w, h)))

    feats_list = []
    ids_list   = []
    frame_nums = sorted(mot.keys())

    print(f"Extrayendo embeddings de {len(frame_nums)} frames...")
    for idx, fnum in enumerate(tqdm(frame_nums, desc="Frames")):
        if idx and idx % log_interval == 0:
            print(f" Procesados {idx}/{len(frame_nums)} frames")

        img_path = find_frame_path(frames_dir, fnum)
        if img_path is None:
            print(f"[WARN] Frame no encontrado: {fnum:06d}.jpg")
            continue
        img = cv2.imread(img_path)
        if img is None:
            print(f"[WARN] Error leyendo imagen: {img_path}")
            continue

        crops, tids = [], []
        for tid, (x,y,w,h) in mot[fnum]:
            x1, y1, x2, y2 = int(x), int(y), int(x+w), int(y+h)
            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue
            crop = cv2.resize(crop, (128,256))
            crops.append(crop)
            tids.append(tid)

        if not crops:
            continue
        # Extraer embeddings
        embs = extractor(crops)  # tensor (B,D)
        embs = embs.numpy()
        # Normalizar L2
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        embs = embs / np.clip(norms, 1e-12, None)

        feats_list.append(embs)
        ids_list.extend(tids)

    if not feats_list:
        raise RuntimeError("No se extrajeron embeddings: revisa rutas y MOT corregido.")

    feats = np.vstack(feats_list)
    ids   = np.array(ids_list)
    np.save(out_feats, feats)
    np.save(out_ids, ids)
    print(f"Embeddings: {out_feats} ({feats.shape}), IDs: {out_ids} ({ids.shape})")
    return feats, ids

# ---------- Evaluación ReID ----------
def evaluate_reid(feats, ids, topk=(1,5,10)):
    dist = np.linalg.norm(feats[:,None,:] - feats[None,:,:], axis=2)
    idx_sort = np.argsort(dist, axis=1)

    cmc = np.zeros(len(ids))
    for i, qid in enumerate(ids):
        matches = (ids[idx_sort[i]] == qid)
        if matches.any():
            first = np.argmax(matches)
            cmc[first:] += 1
    cmc = cmc.cumsum() / len(ids)
    rankk = {f"Rank-{k}": cmc[k-1] for k in topk if k-1 < len(cmc)}

    y_true  = (ids[None,:] == ids[:,None]).astype(int).ravel()
    y_score = (-dist).ravel()
    mAP     = average_precision_score(y_true, y_score)

    print("\n--- ReID Metrics ---")
    for k,v in rankk.items(): print(f"{k}: {v:.2%}")
    print(f"mAP: {mAP:.2%}\n")
    return rankk, mAP

# ---------- Main ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames-dir", required=True,
                        help="Directorio raíz con subcarpetas de frames")
    parser.add_argument("--mot-corr", required=True,
                        help="Ruta a mot_corr30_c.txt corregido")
    parser.add_argument("--model-path", required=True,
                        help="Checkpoint torchreid (.pth.tar) para extractor")
    parser.add_argument("--out-csv", default="reid_report.csv",
                        help="CSV de salida con métricas ReID")
    args = parser.parse_args()

    # Inicializar extractor
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    extractor = FeatureExtractor(
        model_name='osnet_x1_0',
        model_path=args.model_path,
        device=device
    )
    print(f"Extractor en dispositivo: {device}")

    # Extraer
    feats, ids = extract_embeddings(
        args.frames_dir, args.mot_corr, extractor,
        out_feats="feats.npy", out_ids="ids.npy"
    )

    # Evaluar
    rankk, mAP = evaluate_reid(feats, ids)

    # Guardar CSV
    import pandas as pd
    row = {**rankk, 'mAP': mAP}
    pd.DataFrame([row]).to_csv(args.out_csv, index=False, float_format="%.4f")
    print(f"Reporte guardado en {args.out_csv}")

import os
import cv2
import argparse
import tkinter as tk
from tkinter import simpledialog
from collections import Counter

# Interactive MOT correction with flexible ID modification and distinct duplicate coloring

def parse_mot_file(mot_path):
    entries = []
    with open(mot_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            entries.append({
                'frame': int(float(parts[0])), 
                'id': int(float(parts[1])), 
                'bbox': tuple(map(float, parts[2:6])),
                'raw': line.strip()
            })
    return entries


def draw_annotations(img, detections, global_highlight=None, raw_color_map=None):
    out = img.copy()
    global_h = set(global_highlight or [])
    for det in detections:
        x,y,w,h = map(int, det['bbox'])
        tid = det['id']
        raw = det['raw']
        if raw_color_map and raw in raw_color_map:
            color = raw_color_map[raw]
        elif tid in global_h:
            color = (0,0,255)
        else:
            color = (0,255,0)
        cv2.rectangle(out, (x,y), (x+w, y+h), color, 2)
        cv2.putText(out, str(tid), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return out


def pause_loop(by_frame, frames, id_map, raw_map, removed, frames_dir,
               new_ids, duplicate_entries, approved_dup_ids, start_i):
    i = start_i
    orig_frame = frames[i]
    palette = [(255,0,0),(255,255,0),(255,0,255),(0,255,255),(128,0,255)]
    raw_color_map = {d['raw']: palette[idx % len(palette)]
                     for idx,d in enumerate(duplicate_entries)}
    color_names = ["azul", "amarillo", "magenta", "cian", "violeta"]
    if duplicate_entries:
        dup_msgs = []
        dup_ids = []
        for idx_det, det in enumerate(duplicate_entries, 1):
            det_id = raw_map.get(det['raw'], id_map.get(det['id'], det['id']))
            name = color_names[(idx_det - 1) % len(color_names)]
            dup_msgs.append(f"{idx_det} ({name}) id {det_id}")
            dup_ids.append(det_id)
        print("Duplicados: " + ", ".join(dup_msgs) + f" en frame {orig_frame}")
    elif new_ids:
        print(f"Nuevos IDs detectados: {new_ids} en frame {orig_frame}")
    print(f"Pausa en frame {orig_frame}")
    print("Opciones: [n]ext, [p]revious, [m]odificar ID, [d]elete detección, [c]ontinue")

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key==ord('n') and i < len(frames)-1:
            i+=1
        elif key==ord('p') and i>0:
            i-=1
        elif key in (ord('m'), ord('d')):
            root = tk.Tk(); root.withdraw()
            prompt = "Introduzca 'i'<indice> para instancia o ID para global:"
            sel = simpledialog.askstring("Seleccionar detección", prompt)
            root.destroy()
            if not sel: continue
            if sel.startswith('i'):
                try:
                    idx = int(sel[1:]) - 1
                    chosen = duplicate_entries[idx]
                except:
                    print("Selección inválida")
                    continue
                if key==ord('m'):
                    new_id = simpledialog.askinteger("Nuevo ID", "Nuevo ID para la instancia seleccionada:")
                    if new_id is not None:
                        raw_map[chosen['raw']] = new_id
                        print(f"Instancia bbox {chosen['bbox']} mapeada a {new_id}")
                else:
                    removed.add(chosen['raw'])
                    print(f"Instancia bbox {chosen['bbox']} eliminada")
            else:
                try:
                    orig = int(sel)
                except:
                    print("ID inválido.")
                    continue
                if key==ord('m'):
                    new = simpledialog.askinteger("Nuevo ID", f"Nuevo ID para todas detecciones {orig}:")
                    if new is not None:
                        id_map[orig] = new
                        print(f"Mapeado global ID {orig} -> {new}")
                else:
                    for d in by_frame[orig_frame]:
                        cur = raw_map.get(d['raw'], id_map.get(d['id'], d['id']))
                        if cur==orig:
                            removed.add(d['raw'])
                    print(f"Todas detecciones ID {orig} eliminadas en frame {orig_frame}")
        elif key==ord('c'):
            # approve these duplicate IDs so they don't re-pause
            if duplicate_entries:
                approved_dup_ids.update(dup_ids)
            break
        else:
            continue
        # redraw
        f2 = frames[i]
        dets2 = [d for d in by_frame[f2] if d['raw'] not in removed]
        mapped2 = [{'bbox':d['bbox'],'id':raw_map.get(d['raw'],id_map.get(d['id'],d['id'])),'raw':d['raw']} for d in dets2]
        highlights = []
        if f2==orig_frame:
            highlights = [raw_map.get(d['raw'],id_map.get(d['id'],d['id'])) for d in duplicate_entries]
        img2 = cv2.imread(os.path.join(frames_dir, f"{f2:06d}.jpg"))
        cv2.imshow('Annotations', draw_annotations(img2, mapped2, new_ids, raw_color_map if f2==orig_frame else None))
    cv2.waitKey(1)
    return i


def process_all(entries, frames_dir, output_path, no_pause=False):
    id_map, raw_map, removed = {},{},set()
    approved_dup_ids = set()
    seen_ids, out_lines = set(),[]
    by_frame={}
    for e in entries:
        by_frame.setdefault(e['frame'],[]).append(e)
    frames = sorted(by_frame)
    cv2.namedWindow('Annotations',cv2.WINDOW_NORMAL)
    i=0
    while i<len(frames):
        frame=frames[i]
        img=cv2.imread(os.path.join(frames_dir,f"{frame:06d}.jpg"))
        if img is None:
            print(f"Cannot read {frame}")
            i+=1
            continue
        dets=[d for d in by_frame[frame] if d['raw'] not in removed]
        mapped=[{'bbox':d['bbox'],'id':raw_map.get(d['raw'],id_map.get(d['id'],d['id'])),'raw':d['raw']} for d in dets]
        ids=[m['id'] for m in mapped]
        # detect duplicates excluding approved
        dup_ids=[u for u,c in Counter(ids).items() if c>1 and u not in approved_dup_ids]
        duplicate_entries=[]
        for uid in dup_ids:
            es=[m for m in mapped if m['id']==uid]
            if len({tuple(m['bbox']) for m in es})>1:
                duplicate_entries.extend(es)
        new_ids=[u for u in set(ids) if u not in seen_ids]
        highlights=new_ids+[m['id'] for m in duplicate_entries]
        cv2.imshow('Annotations',draw_annotations(img,mapped,highlights))
        key=cv2.waitKey(1)&0xFF
        if ((new_ids or duplicate_entries) and not no_pause) or key==ord('p'):
            i = pause_loop(by_frame, frames, id_map, raw_map, removed, frames_dir, new_ids, duplicate_entries, approved_dup_ids, i)
            dets=[d for d in by_frame[frame] if d['raw'] not in removed]
            mapped=[{'bbox':d['bbox'],'id':raw_map.get(d['raw'],id_map.get(d['id'],d['id'])),'raw':d['raw']} for d in dets]
        # write out
        for m in mapped:
            if m['raw'] in removed: continue
            parts=m['raw'].split(','); parts[1]=str(m['id'])
            out_lines.append(','.join(parts)); seen_ids.add(m['id'])
        i+=1
    cv2.destroyAllWindows()
    with open(output_path,'w') as f: f.write("\n".join(out_lines)+"\n")
    print(f"Saved corrected MOT to {output_path}")

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frames_dir',required=True)
    parser.add_argument('--mot_file',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--no-pause',action='store_true')
    args = parser.parse_args()
    entries=parse_mot_file(args.mot_file)
    process_all(entries,args.frames_dir,args.output,args.no_pause)



#python annotate_review.py --frames_dir "C:/Users/jismbs/Documents/gta-link/tracked_output_DeepEIoU_trackerVideo2_HiperparametersOptimized" --mot_file "C:/Users/jismbs/Documents/gta-link/DeepEIoU_trackerVideo2_Split+Connect_eps0.8_minSamples10_K4_mergeDist0.7_spatial1.0/video2.txt" --output "C:/Users/jismbs/Documents/gta-link/DeepEIoU_trackerVideo2_Split+Connect_eps0.8_minSamples10_K4_mergeDist0.7_spatial1.0/mot_corr.txt"
import os
import cv2
import argparse
import tkinter as tk
from tkinter import simpledialog
from collections import Counter

# Interactive MOT correction with manual frame control, per-frame ID modifications, approval colors, and undo

def parse_mot_file(mot_path):
    entries = []
    with open(mot_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            entries.append({
                'frame': int(float(parts[0])),  # frame number
                'id':    int(float(parts[1])),  # original ID
                'bbox':  tuple(map(float, parts[2:6])),  # bbox
                'raw':   line.strip()  # raw line
            })
    return entries


def draw_annotations(img, detections,
                     new_ids, approved_new_ids,
                     duplicate_entries, approved_dup_ids,
                     raw_color_map=None, raw_index_map=None):
    out = img.copy()
    for det in detections:
        x, y, w, h = map(int, det['bbox'])
        tid = det['id']
        raw = det['raw']
        # determine color
        if raw_color_map and raw in raw_color_map:
            color = raw_color_map[raw]
        elif tid in approved_new_ids or tid in approved_dup_ids:
            color = (0, 255, 0)  # green approved
        elif tid in new_ids or any(d['id'] == tid for d in duplicate_entries):
            color = (0, 0, 255)  # red pending
        else:
            color = (0, 255, 0)
        # draw rectangle
        cv2.rectangle(out, (x, y), (x + w, y + h), color, 2)
        # prepare label
        label = str(tid)
        if raw_index_map and raw in raw_index_map:
            label += f"(i{raw_index_map[raw] + 1})"
        # put text
        cv2.putText(out, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return out


def get_mapped_id(frame, det,
                  id_map, raw_map,
                  frame_id_map, frame_raw_map):
    # per-frame raw map
    if frame in frame_raw_map and det['raw'] in frame_raw_map[frame]:
        return frame_raw_map[frame][det['raw']]
    # per-frame id map
    if frame in frame_id_map and det['id'] in frame_id_map[frame]:
        return frame_id_map[frame][det['id']]
    # fallback global maps
    return raw_map.get(det['raw'], id_map.get(det['id'], det['id']))


def pause_loop(by_frame, frames,
               id_map, raw_map,
               frame_id_map, frame_raw_map,
               removed, frames_dir,
               new_ids, duplicate_entries,
               approved_new_ids, approved_dup_ids,
               start_i):
    i = start_i
    orig_frame = frames[i]
    # color palette for duplicates
    palette = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 255)]
    raw_color_map = {d['raw']: palette[idx % len(palette)] for idx, d in enumerate(duplicate_entries)}
    raw_index_map = {d['raw']: idx for idx, d in enumerate(duplicate_entries)}

    # display duplicate info with indices
    if duplicate_entries:
        dup_info = ', '.join(f"i{idx+1}:{d['id']}" for idx, d in enumerate(duplicate_entries))
        print(f"Duplicados en frame {orig_frame}: {dup_info}")
    elif new_ids:
        print(f"Nuevos IDs en frame {orig_frame}: {new_ids}")
    print("Navegación: [n]/[c]=next, [p]=prev, [u]=undo, [m]=modificar, [d]=delete, [q]=quit")

    while True:
        f2 = frames[i]
        dets2 = [d for d in by_frame[f2] if d['raw'] not in removed]
        mapped2 = []
        for d in dets2:
            mid = get_mapped_id(f2, d, id_map, raw_map, frame_id_map, frame_raw_map)
            mapped2.append({'bbox': d['bbox'], 'id': mid, 'raw': d['raw']})
        img2 = cv2.imread(os.path.join(frames_dir, f"{f2:06d}.jpg"))
        cv2.imshow('Annotations', draw_annotations(
            img2, mapped2,
            new_ids, approved_new_ids,
            duplicate_entries, approved_dup_ids,
            raw_color_map if f2 == orig_frame else None,
            raw_index_map if f2 == orig_frame else None
        ))

        key = cv2.waitKey(0) & 0xFF
        if key in (ord('n'), ord('c')):
            approved_new_ids.update(new_ids)
            approved_dup_ids.update(d['id'] for d in duplicate_entries)
            return min(i + 1, len(frames) - 1), False
        elif key == ord('p'):
            return max(i - 1, 0), False
        elif key == ord('u'):
            return max(i - 1, 0), True
        elif key in (ord('m'), ord('d')):
            root = tk.Tk(); root.withdraw()
            sel = simpledialog.askstring("Seleccionar detección", "'i'<número> o ID:")
            root.destroy()
            if not sel: continue
            # instance-level
            if sel.startswith('i'):
                try:
                    idx = int(sel[1:]) - 1
                    chosen = duplicate_entries[idx]
                except:
                    print("Selección inválida"); continue
                if key == ord('m'):
                    new_id = simpledialog.askinteger("Nuevo ID", "ID para esta instancia:")
                    if new_id is not None:
                        frame_raw_map.setdefault(orig_frame, {})[chosen['raw']] = new_id
                        print(f"Instancia raw={chosen['raw']} -> {new_id} en frame {orig_frame}")
                else:
                    removed.add(chosen['raw'])
                    print("Instancia eliminada")
            # global-level
            else:
                try:
                    orig = int(sel)
                except:
                    print("ID inválido"); continue
                if key == ord('m'):
                    new = simpledialog.askinteger("Nuevo ID", f"ID {orig} -> ? en frame {orig_frame}:")
                    if new is not None:
                        frame_id_map.setdefault(orig_frame, {})[orig] = new
                        print(f"ID {orig} -> {new} en frame {orig_frame}")
                else:
                    for d in by_frame[orig_frame]:
                        cur = get_mapped_id(orig_frame, d, id_map, raw_map, frame_id_map, frame_raw_map)
                        if cur == orig:
                            removed.add(d['raw'])
                    print(f"Instancias ID {orig} eliminadas en frame {orig_frame}")
            continue
        elif key == ord('q'):
            return len(frames), False
        else:
            continue


def process_all(entries, frames_dir, output_path):
    id_map, raw_map = {}, {}
    frame_id_map, frame_raw_map = {}, {}
    removed = set()
    approved_dup_ids = set()
    approved_new_ids = set()
    seen_ids = set()
    out_lines = []
    by_frame = {}
    for e in entries:
        by_frame.setdefault(e['frame'], []).append(e)
    frames = sorted(by_frame)

    cv2.namedWindow('Annotations', cv2.WINDOW_NORMAL)
    i = 0
    while 0 <= i < len(frames):
        frame = frames[i]
        img = cv2.imread(os.path.join(frames_dir, f"{frame:06d}.jpg"))
        if img is None:
            print(f"No puedo leer frame {frame}")
            i += 1
            continue
        dets = [d for d in by_frame[frame] if d['raw'] not in removed]
        mapped = []
        for d in dets:
            mid = get_mapped_id(frame, d, id_map, raw_map, frame_id_map, frame_raw_map)
            mapped.append({'bbox': d['bbox'], 'id': mid, 'raw': d['raw']})
        ids = [m['id'] for m in mapped]
        dup_ids = [u for u, c in Counter(ids).items() if c > 1 and u not in approved_dup_ids]
        duplicate_entries = []
        for uid in dup_ids:
            es = [m for m in mapped if m['id'] == uid]
            if len({tuple(m['bbox']) for m in es}) > 1:
                duplicate_entries.extend(es)
        new_ids = [u for u in set(ids) if u not in seen_ids and u not in approved_new_ids]
        cv2.imshow('Annotations', draw_annotations(
            img, mapped,
            new_ids, approved_new_ids,
            duplicate_entries, approved_dup_ids
        ))
        i, undo = pause_loop(
            by_frame, frames,
            id_map, raw_map,
            frame_id_map, frame_raw_map,
            removed, frames_dir,
            new_ids, duplicate_entries,
            approved_new_ids, approved_dup_ids,
            i
        )
        if i >= len(frames): break
        if not undo:
            dets2 = [d for d in by_frame[frame] if d['raw'] not in removed]
            for d in dets2:
                mid = get_mapped_id(frame, d, id_map, raw_map, frame_id_map, frame_raw_map)
                parts = d['raw'].split(',')
                parts[1] = str(mid)
                out_lines.append(','.join(parts))
                seen_ids.add(mid)
    cv2.destroyAllWindows()
    with open(output_path, 'w') as f:
        f.write("\n".join(out_lines) + "\n")
    print(f"Guardado MOT corregido en {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frames_dir', required=True)
    parser.add_argument('--mot_file', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    entries = parse_mot_file(args.mot_file)
    process_all(entries, args.frames_dir, args.output)

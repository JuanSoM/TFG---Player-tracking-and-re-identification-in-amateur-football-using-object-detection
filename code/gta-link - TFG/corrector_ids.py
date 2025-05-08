import os
import cv2
import shutil
import json
from tkinter import *
from PIL import Image, ImageTk
from collections import defaultdict

class MOTCorrector:
    def __init__(self, mot_path, players_folder, output_folder):
        self.root = Tk()
        self.root.title("Corrector de IDs - Balonmano")
        
        # Configuración de rutas
        self.mot_path = mot_path
        self.players_folder = players_folder
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Datos
        self.mot_data = self.load_mot_data()
        self.current_index = 0
        self.corrections = {}
        self.approved_ids = {}  # {id: last_approved_image}
        
        # Interfaz principal
        self.setup_main_ui()
        self.setup_preview_ui()
        self.load_current_detection()
        
        self.root.mainloop()
    
    def load_mot_data(self):
        """Carga y organiza los datos del MOT por frame"""
        data = []
        with open(self.mot_path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                frame_id = int(float(parts[0]))
                track_id = int(float(parts[1]))
                bbox = list(map(float, parts[2:6]))
                data.append({
                    'frame': frame_id,
                    'id': track_id,
                    'bbox': bbox,
                    'original_line': line.strip()
                })
        return data
    
    def setup_main_ui(self):
        """Interfaz para la corrección actual"""
        self.main_frame = Frame(self.root)
        self.main_frame.pack(side=LEFT, padx=20, pady=20)
        
        # Panel de imagen actual
        self.current_img_label = Label(self.main_frame)
        self.current_img_label.pack()
        
        # Información
        self.info_label = Label(self.main_frame, text="", font=('Arial', 12))
        self.info_label.pack(pady=10)
        
        # Corrección de ID
        control_frame = Frame(self.main_frame)
        control_frame.pack(pady=10)
        
        Label(control_frame, text="Nuevo ID:").pack()
        self.new_id_entry = Entry(control_frame)
        self.new_id_entry.pack()
        self.new_id_entry.bind('<Return>', self.confirm_correction)  # <- MODIFICADO
        
        Button(control_frame, text="Confirmar", command=self.confirm_correction).pack(pady=5)
        
        # Navegación
        nav_frame = Frame(self.main_frame)
        nav_frame.pack(pady=20)
        
        Button(nav_frame, text="<< Anterior", command=self.prev_detection).pack(side=LEFT)
        Button(nav_frame, text="Siguiente >>", command=self.next_detection).pack(side=LEFT)
    
    def setup_preview_ui(self):
        """Interfaz para mostrar IDs aprobados con scrollbar funcional"""
        self.preview_frame = Frame(self.root)
        self.preview_frame.pack(side=RIGHT, padx=20, pady=20, fill=Y)
        
        Label(self.preview_frame, text="IDs Aprobados", font=('Arial', 14)).pack()

        # Canvas y scrollbar
        self.preview_canvas = Canvas(self.preview_frame, width=400, height=600)
        self.scrollbar = Scrollbar(self.preview_frame, orient=VERTICAL, command=self.preview_canvas.yview)
        self.preview_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.preview_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.preview_content = Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_content, anchor="nw")
        
        # Ajuste automático del scroll
        def on_frame_configure(event):
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))

        self.preview_content.bind("<Configure>", on_frame_configure)

        # Scroll con la rueda del ratón
        def _on_mousewheel(event):
            self.preview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.preview_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    
    def load_current_detection(self):
        """Carga la detección actual"""
        if self.current_index >= len(self.mot_data):
            self.info_label.config(text="¡Proceso completado!")
            return
        
        detection = self.mot_data[self.current_index]
        frame_id = detection['frame']
        track_id = detection['id']
        
        # Buscar imagen correspondiente
        img_path = self.find_player_image(track_id, frame_id)
        
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path)
            img.thumbnail((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            
            self.current_img_label.config(image=img_tk)
            self.current_img_label.image = img_tk
            self.info_label.config(text=f"Frame: {frame_id}\nID Actual: {track_id}")
        else:
            self.info_label.config(text=f"Frame: {frame_id}\nID: {track_id}\nImagen no encontrada!")
        
        # Mostrar IDs aprobados
        self.update_preview()
    
    def find_player_image(self, track_id, frame_id):
        """Busca la imagen del jugador en el formato frame_id_track_id.jpg"""
        player_folder = f"player_{track_id:03d}"
        player_path = os.path.join(self.players_folder, player_folder)
        
        if not os.path.exists(player_path):
            return None
        
        # Buscar imagen con el formato correcto
        expected_name = f"{frame_id:06d}_{track_id:03d}.jpg"
        for f in os.listdir(player_path):
            if f.startswith(f"{frame_id:06d}_"):
                return os.path.join(player_path, f)
        
        return None
    
    def update_preview(self):
        """Actualiza el panel de IDs aprobados"""
        # Limpiar contenido anterior
        for widget in self.preview_content.winfo_children():
            widget.destroy()
        
        # Mostrar cada ID aprobado con su última imagen
        for id_num, img_path in sorted(self.approved_ids.items()):
            frame = Frame(self.preview_content)
            frame.pack(pady=5, fill=X)
            
            # Mostrar imagen
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img.thumbnail((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                
                img_label = Label(frame, image=img_tk)
                img_label.image = img_tk
                img_label.pack(side=LEFT)
            
            # Mostrar ID
            Label(frame, text=f"ID: {id_num}", font=('Arial', 11)).pack(side=LEFT, padx=10)
    
    def confirm_correction(self, event=None):  # <- MODIFICADO
        """Confirma la corrección del ID actual o aprueba el existente"""
        new_id_text = self.new_id_entry.get()
        current_detection = self.mot_data[self.current_index]
        original_id = current_detection['id']
        
        if new_id_text == "":
            new_id = original_id  # ID aprobado sin cambios
        elif new_id_text.isdigit():
            new_id = int(new_id_text)
        else:
            return  # entrada inválida
        
        # Registrar corrección si cambia
        self.corrections[self.current_index] = new_id

        # Actualizar IDs aprobados
        img_path = self.find_player_image(original_id, current_detection['frame'])
        if img_path:
            self.approved_ids[new_id] = img_path

        self.new_id_entry.delete(0, END)  # Limpiar entrada
        self.next_detection()
    
    def prev_detection(self):
        """Retrocede a la detección anterior"""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_detection()
    
    def next_detection(self):
        """Avanza a la siguiente detección"""
        if self.current_index < len(self.mot_data) - 1:
            self.current_index += 1
            self.load_current_detection()
        else:
            self.save_results()
    
    def save_results(self):
        """Guarda los resultados en un nuevo archivo MOT"""
        output_path = os.path.join(self.output_folder, "mot_corregido.txt")
        
        with open(output_path, 'w') as f:
            for i, detection in enumerate(self.mot_data):
                original_line = detection['original_line']
                parts = original_line.split(',')
                
                # Aplicar corrección si existe
                if i in self.corrections:
                    parts[1] = str(self.corrections[i])
                
                f.write(','.join(parts) + '\n')
        
        # Guardar mapeo de correcciones
        with open(os.path.join(self.output_folder, 'corrections.json'), 'w') as f:
            json.dump({
                'corrections': self.corrections,
                'approved_ids': {k: v for k, v in self.approved_ids.items()}
            }, f, indent=2)
        
        print(f"Proceso completado. Resultados guardados en: {self.output_folder}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Herramienta de corrección de IDs para tracking')
    parser.add_argument('--mot', required=True, help='Ruta al archivo MOT original')
    parser.add_argument('--players', required=True, help='Ruta a la carpeta de jugadores (player_*)')
    parser.add_argument('--output', required=True, help='Carpeta de salida para los resultados')
    
    args = parser.parse_args()
    
    # Ejecutar la aplicación
    app = MOTCorrector(
        mot_path=args.mot,
        players_folder=args.players,
        output_folder=args.output
    )

#python corrector_ids.py --mot "C:\Users\jismbs\Documents\gta-link\DeepEIoU_trackerVideo2_Split+Connect_eps0.6_minSamples10_K3_mergeDist0.4_spatial1.0\video2.txt" --players "C:\Users\jismbs\Documents\gta-link\player_crops" --output "C:\Users\jismbs\Documents\gta-link\corregido"
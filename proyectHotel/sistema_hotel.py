import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class SistemaHotel:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Hotelera")
        self.root.geometry("600x660")
        
        # Estructuras de datos
        self.habitaciones = self.cargar_datos('habitaciones.json')
        self.huespedes = self.cargar_datos('huespedes.json')
        
        self.crear_interfaz()
    
    def cargar_datos(self, archivo):
        try:
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read().strip()
                    if not contenido:
                        print(f"El archivo {archivo} está vacío. Se creará una lista vacía.")
                        return []
                    return json.loads(contenido)
            else:
                # Si el archivo no existe, crearlo con lista vacía
                print(f"El archivo {archivo} no existe. Creándolo...")
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=2)
                return []
        except json.JSONDecodeError as e:
            print(f"Error en formato JSON en {archivo}: {e}")
            # Crear un archivo nuevo si está corrupto
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
            return []
        except Exception as e:
            print(f"Error al cargar {archivo}: {e}")
            return []
    
    def guardar_datos(self, archivo, datos):
        with open(archivo, 'w') as f:
            json.dump(datos, f, indent=4)
    
    def crear_interfaz(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[10, 5])
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        style.configure('Treeview', font=('Arial', 10), rowheight=26)
        style.configure('TLabel', font=('Arial', 10))
        # Colores personalizados para Treeview
        style.map('Treeview', background=[('selected', '#b3d9ff')])
        style.configure('Disponible.Treeview', background='#e6ffe6', foreground='black')
        style.configure('Ocupada.Treeview', background='#ffe6e6', foreground='black')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        # Pestañas
        self.crear_pestaña_inicio()
        self.crear_pestaña_habitaciones()
        self.crear_pestaña_huespedes()
    
    def crear_pestaña_inicio(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Inicio")
        
        # Título centrado
        label = ttk.Label(frame, text="SISTEMA DE GESTIÓN HOTELERA", font=("Arial", 16, "bold"), anchor="center", justify="center")
        label.pack(pady=(20, 10), anchor="center")

        try:
            from PIL import Image, ImageTk
            img = Image.open("images.jpg")
            img = img.resize((460, 280))
            self.logo_img = ImageTk.PhotoImage(img)
            label_img = ttk.Label(frame, image=self.logo_img, anchor="center", justify="center")
            label_img.pack(pady=10, anchor="center")
        except Exception:
            pass
        # Estadísticas centradas
        info_text = f"""
Habitaciones totales: {len(self.habitaciones)}\nHuéspedes registrados: {len(self.huespedes)}"""
        info_label = ttk.Label(frame, text=info_text, font=("Arial", 12), anchor="center", justify="center")
        info_label.pack(pady=10, anchor="center")

    def crear_pestaña_habitaciones(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Habitaciones")
        # Treeview para mostrar habitaciones
        columns = ('numero', 'tipo', 'estado', 'precio')
        self.tree_hab = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        self.tree_hab.heading('numero', text='Número')
        self.tree_hab.heading('tipo', text='Tipo')
        self.tree_hab.heading('estado', text='Estado')
        self.tree_hab.heading('precio', text='Precio')
        self.tree_hab.column('numero', width=100)
        self.tree_hab.column('tipo', width=150)
        self.tree_hab.column('estado', width=150)
        self.tree_hab.column('precio', width=100)
        self.actualizar_lista_habitaciones()
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_hab.yview)
        self.tree_hab.configure(yscrollcommand=scrollbar.set)
        self.tree_hab.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def actualizar_lista_habitaciones(self):
        for item in self.tree_hab.get_children():
            self.tree_hab.delete(item)
        for hab in self.habitaciones:
            tag = 'disponible' if hab['estado'].lower() == 'disponible' else 'ocupada'
            self.tree_hab.insert('', 'end', values=(
                hab['numero'],
                hab['tipo'],
                hab['estado'].capitalize(),
                f"${hab['precio']}"
            ), tags=(tag,))
        # Colorear filas según estado
        self.tree_hab.tag_configure('disponible', background='#e6ffe6', foreground='black')
        self.tree_hab.tag_configure('ocupada', background='#ffe6e6', foreground='black')

    def crear_pestaña_huespedes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Huéspedes")
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="➕ Agregar Huésped", 
              command=self.agregar_huesped).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✔️ Check Out", 
              command=self.check_out_huesped).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar huéspedes
        columns = ('id', 'nombre', 'email', 'telefono')
        self.tree_hues = ttk.Treeview(frame, columns=columns + ('habitacion',), show='headings', height=15)
        
        self.tree_hues.heading('id', text='ID')
        self.tree_hues.heading('nombre', text='Nombre')
        self.tree_hues.heading('email', text='Email')
        self.tree_hues.heading('telefono', text='Teléfono')
        self.tree_hues.heading('habitacion', text='Habitación')
        
        self.tree_hues.column('id', width=50)
        self.tree_hues.column('nombre', width=180)
        self.tree_hues.column('email', width=150)
        self.tree_hues.column('telefono', width=100)
        self.tree_hues.column('habitacion', width=90)
        
        self.actualizar_lista_huespedes()
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_hues.yview)
        self.tree_hues.configure(yscrollcommand=scrollbar.set)
        
        self.tree_hues.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def check_out_huesped(self):
        item = self.tree_hues.selection()
        if not item:
            messagebox.showwarning("Selecciona un huésped", "Debes seleccionar un huésped para hacer check out.")
            return
        huesped_values = self.tree_hues.item(item[0], 'values')
        huesped_id = int(huesped_values[0])
        habitacion_num = huesped_values[4]
        # Confirmar acción
        if not messagebox.askyesno("Confirmar", f"¿Seguro que deseas hacer check out del huésped {huesped_values[1]}?"):
            return
        # Eliminar huésped
        self.huespedes = [h for h in self.huespedes if h['id'] != huesped_id]
        # Liberar habitación
        for hab in self.habitaciones:
            if str(hab['numero']) == str(habitacion_num):
                hab['estado'] = 'disponible'
        self.guardar_datos('huespedes.json', self.huespedes)
        self.guardar_datos('habitaciones.json', self.habitaciones)
        self.actualizar_lista_huespedes()
        self.actualizar_lista_habitaciones()
        messagebox.showinfo("Check Out", "Check out realizado y habitación liberada.")
    
    def actualizar_lista_huespedes(self):
        for item in self.tree_hues.get_children():
            self.tree_hues.delete(item)
        
        for huesped in self.huespedes:
                self.tree_hues.insert('', 'end', values=(
                    huesped['id'],
                    f"{huesped.get('nombre', '')} {huesped.get('apellido', '')}",
                    huesped.get('email', ''),
                    huesped.get('telefono', ''),
                    huesped.get('habitacion', '-')
                ))
    
    def agregar_huesped(self):
        # Buscar habitaciones disponibles
        habitaciones_disponibles = [h for h in self.habitaciones if h['estado'].lower() == 'disponible']
        if not habitaciones_disponibles:
            messagebox.showwarning("Sin habitaciones", "No hay habitaciones disponibles para asignar.")
            return
        popup = tk.Toplevel(self.root)
        popup.title("Agregar Huésped")
        popup.geometry("400x350")
        popup.grab_set()
        campos = [
            ("Nombre:", 0),
            ("Apellido:", 1),
            ("Email:", 2),
            ("Teléfono:", 3),
            ("Documento:", 4)
        ]
        entries = {}
        for label, row in campos:
            ttk.Label(popup, text=label).grid(row=row, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(popup, width=30)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')
            entries[label.lower().replace(':', '')] = entry
        # Combo para seleccionar habitación
        ttk.Label(popup, text="Habitación:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        hab_combo = ttk.Combobox(popup, width=27, state="readonly")
        hab_combo['values'] = [f"{h['numero']} - {h['tipo']} (${h['precio']})" for h in habitaciones_disponibles]
        hab_combo.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        def guardar():
            idx = hab_combo.current()
            if idx == -1:
                messagebox.showerror("Error", "Debe seleccionar una habitación disponible.")
                return
            habitacion = habitaciones_disponibles[idx]
            nuevo_huesped = {
                'id': len(self.huespedes) + 1,
                'nombre': entries['nombre'].get(),
                'apellido': entries['apellido'].get(),
                'email': entries['email'].get(),
                'telefono': entries['teléfono'].get(),
                'documento': entries['documento'].get(),
                'habitacion': habitacion['numero']
            }
            self.huespedes.append(nuevo_huesped)
            # Marcar habitación como ocupada
            for h in self.habitaciones:
                if h['numero'] == habitacion['numero']:
                    h['estado'] = 'ocupada'
            self.guardar_datos('huespedes.json', self.huespedes)
            self.guardar_datos('habitaciones.json', self.habitaciones)
            self.actualizar_lista_huespedes()
            self.actualizar_lista_habitaciones()
            popup.destroy()
            messagebox.showinfo("Éxito", "Huésped agregado y habitación asignada correctamente")
        ttk.Button(popup, text="Guardar", command=guardar).grid(
            row=6, column=0, columnspan=2, pady=10)
        ttk.Button(popup, text="Cancelar", command=popup.destroy).grid(
            row=7, column=0, columnspan=2, pady=5)
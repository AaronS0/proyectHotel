import tkinter as tk
from tkinter import ttk, messagebox

# Datos iniciales
habitaciones = [
    {"numero": "101", "tipo": "Sencilla", "precio": 50, "estado": "disponible"},
    {"numero": "102", "tipo": "Sencilla", "precio": 50, "estado": "disponible"},
    {"numero": "201", "tipo": "Doble", "precio": 120, "estado": "disponible"},
    {"numero": "202", "tipo": "Doble", "precio": 120, "estado": "ocupada"},
    {"numero": "301", "tipo": "Familiar", "precio": 180, "estado": "disponible"},
    {"numero": "302", "tipo": "Familiar", "precio": 180, "estado": "disponible"},
    {"numero": "401", "tipo": "Suite", "precio": 250, "estado": "ocupada"},
    {"numero": "402", "tipo": "Suite", "precio": 250, "estado": "disponible"},
]

huespedes = [
    {"id": 1, "nombre": "Aaron", "apellido": "Sanchez", "email": "asanche@gmail.com", "telefono": "3000000000", "documento": "1111111111", "habitacion": "401"},
    {"id": 2, "nombre": "Amir", "apellido": "Amaya", "email": "amiram@gmail.com", "telefono": "3111111111", "documento": "1100110011", "habitacion": "202"},
]

# Funciones principales
def actualizar_lista_habitaciones():
    for item in tree_hab.get_children():
        tree_hab.delete(item)
    for hab in habitaciones:
        tag = 'disponible' if hab['estado'].lower() == 'disponible' else 'ocupada'
        tree_hab.insert('', 'end', values=(hab['numero'], hab['tipo'], hab['estado'], f"${hab['precio']}"), tags=(tag,))
    tree_hab.tag_configure('disponible', background='#e6ffe6')
    tree_hab.tag_configure('ocupada', background='#ffe6e6')

def actualizar_lista_huespedes():
    for item in tree_hues.get_children():
        tree_hues.delete(item)
    for huesped in huespedes:
        tree_hues.insert('', 'end', values=(huesped["id"], f"{huesped['nombre']} {huesped['apellido']}", huesped["email"], huesped["telefono"], huesped["habitacion"]))

def agregar_huesped():
    disponibles = [h for h in habitaciones if h["estado"].lower() == "disponible"]
    if not disponibles:
        messagebox.showwarning("Sin habitaciones", "No hay habitaciones disponibles.")
        return
    
    popup = tk.Toplevel(root)
    popup.title("Agregar Huésped")
    popup.geometry("350x300")
    popup.grab_set()

    labels = ["Nombre", "Apellido", "Email", "Teléfono", "Documento"]
    entries = {}
    for i, campo in enumerate(labels):
        ttk.Label(popup, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        e = ttk.Entry(popup, width=25)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[campo.lower()] = e

    ttk.Label(popup, text="Habitación").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    combo = ttk.Combobox(popup, width=23, state="readonly")
    combo["values"] = [f"{h['numero']} - {h['tipo']} (${h['precio']})" for h in disponibles]
    combo.grid(row=5, column=1, padx=5, pady=5)

    def guardar():
        if combo.current() == -1:
            messagebox.showerror("Error", "Seleccione una habitación.")
            return
        habitacion = disponibles[combo.current()]
        nuevo = {
            "id": len(huespedes) + 1,
            "nombre": entries["nombre"].get(),
            "apellido": entries["apellido"].get(),
            "email": entries["email"].get(),
            "telefono": entries["teléfono"].get(),
            "documento": entries["documento"].get(),
            "habitacion": habitacion["numero"]
        }
        huespedes.append(nuevo)
        habitacion["estado"] = "ocupada"
        actualizar_lista_habitaciones()
        actualizar_lista_huespedes()
        popup.destroy()
        messagebox.showinfo("Éxito", "Huésped agregado.")

    ttk.Button(popup, text="Guardar", command=guardar).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(popup, text="Cancelar", command=popup.destroy).grid(row=7, column=0, columnspan=2, pady=5)

def check_out_huesped():
    sel = tree_hues.selection()
    if not sel:
        messagebox.showwarning("Atención", "Seleccione un huésped.")
        return
    values = tree_hues.item(sel[0], "values")
    huesped_id = int(values[0])
    habitacion_num = values[4]

    if not messagebox.askyesno("Confirmar", f"¿Desea hacer check-out de {values[1]}?"):
        return
    
    # Quitar huésped
    global huespedes
    huespedes = [h for h in huespedes if h["id"] != huesped_id]

    # Liberar habitación
    for h in habitaciones:
        if h["numero"] == habitacion_num:
            h["estado"] = "disponible"

    actualizar_lista_habitaciones()
    actualizar_lista_huespedes()
    messagebox.showinfo("Listo", "Check-out realizado.")

# Interfaz gráfica
root = tk.Tk()
root.title("Sistema Hotelero")
root.geometry("600x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# --- Inicio
frame_inicio = ttk.Frame(notebook)
notebook.add(frame_inicio, text="Inicio")
ttk.Label(frame_inicio, text="SISTEMA DE GESTIÓN HOTELERA", font=("Times New Roman", 16, "bold")).pack(pady=10)

try:
    from PIL import Image, ImageTk
    img = Image.open("images.png")
    img = img.resize((250, 400))
    logo = ImageTk.PhotoImage(img)
    ttk.Label(frame_inicio, image=logo).pack(pady=10)
except:
    pass

info = f"Habitaciones totales: {len(habitaciones)}\nHuéspedes registrados: {len(huespedes)}"
ttk.Label(frame_inicio, text=info, font=("Arial", 12)).pack(pady=10)

# --- Habitaciones
frame_hab = ttk.Frame(notebook)
notebook.add(frame_hab, text="Habitaciones")
cols = ("numero", "tipo", "estado", "precio")
tree_hab = ttk.Treeview(frame_hab, columns=cols, show="headings", height=15)
for col in cols:
    tree_hab.heading(col, text=col.capitalize())
tree_hab.pack(fill="both", expand=True)
actualizar_lista_habitaciones()

# --- Huéspedes
frame_hues = ttk.Frame(notebook)
notebook.add(frame_hues, text="Huéspedes")

btn_frame = ttk.Frame(frame_hues)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="➕ Agregar Huésped", command=agregar_huesped).pack(side="left", padx=5)
ttk.Button(btn_frame, text="✔️ Check Out", command=check_out_huesped).pack(side="left", padx=5)

cols2 = ("id", "nombre", "email", "telefono", "habitacion")
tree_hues = ttk.Treeview(frame_hues, columns=cols2, show="headings", height=15)
for col in cols2:
    tree_hues.heading(col, text=col.capitalize())
tree_hues.pack(fill="both", expand=True)
actualizar_lista_huespedes()

root.mainloop()

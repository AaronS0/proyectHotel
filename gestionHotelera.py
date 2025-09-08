import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# --- Datos iniciales
habitaciones = [
    {"numero": "101", "tipo": "Sencilla", "precio": 50, "estado": "Ocupada"},
    {"numero": "102", "tipo": "Sencilla", "precio": 50, "estado": "Ocupada"},
    {"numero": "201", "tipo": "Doble", "precio": 120, "estado": "Disponible"},
    {"numero": "202", "tipo": "Doble", "precio": 120, "estado": "Ocupada"},
    {"numero": "301", "tipo": "Familiar", "precio": 180, "estado": "Disponible"},
    {"numero": "302", "tipo": "Familiar", "precio": 180, "estado": "Disponible"},
    {"numero": "401", "tipo": "Suite", "precio": 250, "estado": "Ocupada"},
    {"numero": "402", "tipo": "Suite", "precio": 250, "estado": "Disponible"},
]

huespedes = [
    {"id": 1, "nombre": "Aaron", "apellido": "Sanchez", "email": "asanche@gmail.com", "telefono": "3000000000", "documento": "1111111111", "habitacion": "401"},
    {"id": 2, "nombre": "Amir", "apellido": "Amaya", "email": "amiram@gmail.com", "telefono": "3111111111", "documento": "1100110011", "habitacion": "202"},
    {"id": 3, "nombre": "David", "apellido": "Revelo", "email": "drevelo@email.com", "telefono": "3123456789", "documento": "2222222222", "habitacion": "101"},
    {"id": 4, "nombre": "Juan", "apellido": "Escobar", "email": "jescobar@email.com", "telefono": "3134567890", "documento": "3333333333", "habitacion": "102"},
]

# --- Variables Globales ---
usuario_logeado = None
label_huespedes_valor = None
label_habitaciones_valor = None

# --- Funciones de Actualización de UI ---

def actualizar_lista_habitaciones():
    for item in tree_hab.get_children():
        tree_hab.delete(item)
    for hab in habitaciones:
        tag = 'Disponible' if hab['estado'] == 'Disponible' else 'Ocupada'
        tree_hab.insert('', 'end', values=(hab['numero'], hab['tipo'], hab['estado'], f"${hab['precio']}"), tags=(tag,))
    
    # El color de fondo es el mismo del tema, solo cambia el color del texto de la fila.
    style.configure('Treeview', background='#5d4037', foreground='white', fieldbackground='#5d4037', rowheight=25)
    tree_hab.tag_configure('Disponible', foreground='#a5d6a7') # Verde claro para el texto
    tree_hab.tag_configure('Ocupada', foreground='#ef9a9a') # Rojo claro para el texto

def actualizar_lista_huespedes():
    for item in tree_hues.get_children():
        tree_hues.delete(item)
    for huesped in huespedes:
        tree_hues.insert('', 'end', values=(huesped["id"], f"{huesped['nombre']} {huesped['apellido']}", huesped["email"], huesped["telefono"], huesped["habitacion"]))

def actualizar_estadisticas_inicio():
    if label_huespedes_valor and label_habitaciones_valor:
        num_huespedes = len(huespedes)
        num_disp = len([h for h in habitaciones if h['estado'] == 'Disponible'])
        label_huespedes_valor.config(text=f"{num_huespedes}")
        label_habitaciones_valor.config(text=f"{num_disp}")

# --- Funciones de Lógica de la Aplicación ---

def agregar_huesped():
    Disponibles = [h for h in habitaciones if h["estado"] == "Disponible"]
    if not Disponibles:
        messagebox.showwarning("Sin habitaciones", "No hay habitaciones disponibles.")
        return
    
    popup = tk.Toplevel(root)
    popup.title("Agregar Huésped")
    popup.geometry("350x300")
    popup.grab_set()
    popup.configure(bg='#3e2723')

    labels = ["Nombre", "Apellido", "Email", "Teléfono", "Documento"]
    entries = {}
    for i, campo in enumerate(labels):
        ttk.Label(popup, text=campo, background='#3e2723', foreground='white').grid(row=i, column=0, padx=5, pady=5, sticky="e")
        e = ttk.Entry(popup, width=25, style='TEntry')
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[campo.lower()] = e

    ttk.Label(popup, text="Habitación", background='#3e2723', foreground='white').grid(row=5, column=0, padx=5, pady=5, sticky="e")
    combo = ttk.Combobox(popup, width=23, state="readonly", style='TCombobox')
    combo["values"] = [f"{h['numero']} - {h['tipo']} (${h['precio']})" for h in Disponibles]
    combo.grid(row=5, column=1, padx=5, pady=5)

    def guardar():
        if combo.current() == -1:
            messagebox.showerror("Error", "Seleccione una habitación.")
            return
        habitacion = Disponibles[combo.current()]
        nuevo = {
            "id": len(huespedes) + 1, "nombre": entries["nombre"].get(), "apellido": entries["apellido"].get(),
            "email": entries["email"].get(), "telefono": entries["teléfono"].get(),
            "documento": entries["documento"].get(), "habitacion": habitacion["numero"]
        }
        huespedes.append(nuevo)
        habitacion["estado"] = "Ocupada"
        actualizar_lista_habitaciones()
        actualizar_lista_huespedes()
        actualizar_estadisticas_inicio()
        popup.destroy()
        messagebox.showinfo("Éxito", "Huésped agregado.")

    ttk.Button(popup, text="Guardar", command=guardar, style='TButton').grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Button(popup, text="Cancelar", command=popup.destroy, style='TButton').grid(row=7, column=0, columnspan=2, pady=5)

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
    
    global huespedes
    huespedes = [h for h in huespedes if h["id"] != huesped_id]
    for h in habitaciones:
        if h["numero"] == habitacion_num:
            h["estado"] = "Disponible"

    actualizar_lista_habitaciones()
    actualizar_lista_huespedes()
    actualizar_estadisticas_inicio()
    messagebox.showinfo("Listo", "Check-out realizado.")

def check_login():
    global usuario_logeado
    nombre, clave = entry_nombre.get(), entry_clave.get()
    if clave == "1234":
        for huesped in huespedes:
            if huesped['nombre'].lower() == nombre.lower():
                usuario_logeado = f"{huesped['nombre']} {huesped['apellido']}"
                root_login.destroy()
                main_app()
                return
        messagebox.showerror("Error de Autenticación", "Nombre de usuario.")
    else:
        messagebox.showerror("Error de Autenticación", "Clave incorrecta.")

# --- Ventana de inicio de sesión ---
def run_login():
    global root_login, entry_nombre, entry_clave
    root_login = tk.Tk()
    root_login.title("Iniciar Sesión")
    root_login.geometry("300x200")
    root_login.configure(bg='#3e2723')
    root_login.resizable(False, False)

    try:
        root_login.iconphoto(True, tk.PhotoImage(file='icono.png'))
    except Exception: pass

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#3e2723')
    style.configure('TLabel', background='#3e2723', foreground='white')
    style.configure('TEntry', fieldbackground='#5d4037', foreground='white', insertcolor='white')
    style.configure('TButton', background='#5d4037', foreground='white', font=('Arial', 10, 'bold'))
    style.map('TButton', background=[('active', '#8d6e63')])

    login_frame = ttk.Frame(root_login, padding=20)
    login_frame.pack(expand=True)
    ttk.Label(login_frame, text="Nombre:", style='TLabel').grid(row=0, column=0, pady=5, sticky="e")
    entry_nombre = ttk.Entry(login_frame, style='TEntry')
    entry_nombre.grid(row=0, column=1, pady=5)
    ttk.Label(login_frame, text="Clave:", style='TLabel').grid(row=2, column=0, pady=5, sticky="e")
    entry_clave = ttk.Entry(login_frame, show="*", style='TEntry')
    entry_clave.grid(row=2, column=1, pady=5)
    ttk.Button(login_frame, text="Entrar", command=check_login, style='TButton').grid(row=3, column=0, columnspan=2, pady=10)
    entry_clave.bind("<Return>", lambda event: check_login())
    root_login.mainloop()

def main_app():
    global root, notebook, tree_hab, tree_hues, label_huespedes_valor, label_habitaciones_valor, style
    root = tk.Tk()
    root.title("Sistema de gestión hotelera")
    root.geometry("780x680")
    root.configure(bg='#3e2723')

    try:
        root.iconphoto(True, tk.PhotoImage(file='icono.png'))
    except Exception: pass

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#3e2723')
    style.configure('TNotebook', background='#3e2723', borderwidth=0)
    
    # Para cambiar el tamaño de las pestañas, modifica el 'padding' aquí.
    style.configure('TNotebook.Tab', padding=[10, 5], foreground='#cccccc')
    
    # Para eliminar el marco punteado al seleccionar.
    style.map('TNotebook.Tab', 
              background=[('selected', '#5d4037'), ('!selected', '#3e2723')],
              foreground=[('selected', 'white'), ('!selected', '#cccccc')])
    
    style.configure('TLabel', background='#3e2723', foreground='white')
    style.configure('Treeview.Heading', background='#8d6e63', foreground='white', font=('Arial', 10, 'bold'))
    style.configure('TButton', background='#5d4037', foreground='white', font=('Arial', 10, 'bold'))
    style.map('TButton', background=[('active', '#8d6e63')])
    style.configure('TEntry', fieldbackground='#5d4037', foreground='white', insertcolor='white')
    style.configure('TCombobox', fieldbackground='#5d4037', foreground='white')

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Pestaña Inicio ---
    frame_inicio = ttk.Frame(notebook); notebook.add(frame_inicio, text="Inicio")
    titulo_principal = f"BIENVENIDO {usuario_logeado.upper()}"
    ttk.Label(frame_inicio, text=titulo_principal, font=("Georgia", 18, "bold"), background='#3e2723', foreground='white').pack(pady=20)
    try:
        original_img = Image.open("logo.png")
        logo = ImageTk.PhotoImage(original_img.resize((250, 400), Image.Resampling.LANCZOS))
        img_label = ttk.Label(frame_inicio, image=logo, background='#3e2723'); img_label.image = logo
        img_label.pack(pady=10)
    except Exception: pass
    info_frame = ttk.Frame(frame_inicio, padding=10); info_frame.pack(pady=20, padx=20)
    ttk.Label(info_frame, text="Habitaciones Disponibles:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    label_habitaciones_valor = ttk.Label(info_frame, font=("Arial", 14, "bold"), foreground='#a1887f')
    label_habitaciones_valor.grid(row=0, column=1, padx=10, pady=5, sticky='w')
    ttk.Label(info_frame, text="Huéspedes Registrados:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
    label_huespedes_valor = ttk.Label(info_frame, font=("Arial", 14, "bold"), foreground='#a1887f')
    label_huespedes_valor.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    # --- Pestaña Habitaciones ---
    frame_hab = ttk.Frame(notebook); notebook.add(frame_hab, text="Habitaciones")
    cols = ("numero", "tipo", "estado", "precio")
    tree_hab = ttk.Treeview(frame_hab, columns=cols, show="headings", style='Treeview')
    # Para centrar la información, se añade anchor='center' en cada columna.
    tree_hab.column("numero", width=100, anchor='center')
    tree_hab.column("tipo", width=200, anchor='center')
    tree_hab.column("estado", width=150, anchor='center')
    tree_hab.column("precio", width=100, anchor='center')
    for col in cols: tree_hab.heading(col, text=col.capitalize())
    tree_hab.pack(fill="both", expand=True, padx=5, pady=5)
    
    # --- Pestaña Huéspedes ---
    frame_hues = ttk.Frame(notebook); notebook.add(frame_hues, text="Huéspedes")
    btn_frame = ttk.Frame(frame_hues); btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="➕ Agregar Huésped", command=agregar_huesped, style='TButton').pack(side='left', padx=10)
    ttk.Button(btn_frame, text="✔️ Check Out", command=check_out_huesped, style='TButton').pack(side='left', padx=10)
    cols2 = ("id", "nombre", "email", "telefono", "habitacion")
    tree_hues = ttk.Treeview(frame_hues, columns=cols2, show="headings", style='Treeview')
    # Para centrar la información, se añade anchor='center' en cada columna.
    tree_hues.column("id", width=50, anchor='center')
    tree_hues.column("nombre", width=200, anchor='center')
    tree_hues.column("email", width=220, anchor='center')
    tree_hues.column("telefono", width=120, anchor='center')
    tree_hues.column("habitacion", width=100, anchor='center')
    for col in cols2: tree_hues.heading(col, text=col.capitalize())
    tree_hues.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Carga inicial de datos
    actualizar_lista_habitaciones()
    actualizar_lista_huespedes()
    actualizar_estadisticas_inicio()

    root.mainloop()

# --- Punto de entrada del programa ---
if __name__ == "__main__":
    run_login()

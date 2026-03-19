"""
╔══════════════════════════════════════════════════════╗
║   TALLER: Lista de Tareas con Lista Simple Enlazada  ║
║   Estructura de Datos — Python + Tkinter (Desktop)   ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


# ══════════════════════════════════════════════
#  ESTRUCTURA DE DATOS: NODO
# ══════════════════════════════════════════════
class Nodo:
    """
    Cada nodo contiene una tarea y una referencia
    al siguiente nodo en la lista.
    """
    def __init__(self, tarea: str, prioridad: str = "Media"):
        self.tarea = tarea
        self.prioridad = prioridad
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.siguiente = None   # referencia al siguiente nodo


# ══════════════════════════════════════════════
#  ESTRUCTURA DE DATOS: LISTA SIMPLE
# ══════════════════════════════════════════════
class ListaSimple:
    """
    Lista enlazada simple para gestionar tareas pendientes.
    La cabeza apunta al primer nodo; el último nodo apunta a None.
    """

    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def agregar_inicio(self, tarea, prioridad="Media"):
        if self._existe(tarea):
            return "⚠ La tarea ya existe en la lista."
        nuevo = Nodo(tarea, prioridad)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamanio += 1
        return "✓ Tarea agregada al inicio."

    def agregar_final(self, tarea, prioridad="Media"):
        if self._existe(tarea):
            return "⚠ La tarea ya existe en la lista."
        nuevo = Nodo(tarea, prioridad)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1
        return "✓ Tarea agregada al final."

    def eliminar(self, tarea):
        if self.cabeza is None:
            return "⚠ La lista está vacía."
        if self.cabeza.tarea == tarea:
            self.cabeza = self.cabeza.siguiente
            self.tamanio -= 1
            return "✓ Tarea eliminada."
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.tarea == tarea:
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio -= 1
                return "✓ Tarea eliminada."
            actual = actual.siguiente
        return "⚠ Tarea no encontrada."

    def buscar(self, tarea):
        actual = self.cabeza
        pos = 1
        while actual:
            if actual.tarea == tarea:
                return pos
            actual = actual.siguiente
            pos += 1
        return -1

    def obtener_todas(self):
        resultado = []
        actual = self.cabeza
        pos = 1
        while actual:
            resultado.append({
                "pos": pos,
                "tarea": actual.tarea,
                "prioridad": actual.prioridad,
                "fecha": actual.fecha,
            })
            actual = actual.siguiente
            pos += 1
        return resultado

    def limpiar(self):
        self.cabeza = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def _existe(self, tarea):
        return self.buscar(tarea) != -1

    def cadena_texto(self):
        if self.esta_vacia():
            return "CABEZA → NULL"
        partes = []
        actual = self.cabeza
        while actual:
            nombre = actual.tarea[:16] + "…" if len(actual.tarea) > 16 else actual.tarea
            partes.append(f"[{nombre}]")
            actual = actual.siguiente
        return "CABEZA → " + " → ".join(partes) + " → NULL"


# ══════════════════════════════════════════════
#  PALETA Y FUENTES
# ══════════════════════════════════════════════
BG      = "#0f0f1a"
SURFACE = "#16162a"
CARD    = "#1e1e35"
BORDER  = "#2e2e50"
ACCENT  = "#ff6b35"
PURPLE  = "#7c3aed"
GREEN   = "#06d6a0"
YELLOW  = "#f59e0b"
RED     = "#ef4444"
TEXT    = "#e8e8f8"
MUTED   = "#7070a0"

FONT_TITLE = ("Courier New", 22, "bold")
FONT_HEAD  = ("Courier New", 12, "bold")
FONT_BODY  = ("Courier New", 11)
FONT_SMALL = ("Courier New", 9)
FONT_MONO  = ("Courier New", 10)


# ══════════════════════════════════════════════
#  APLICACIÓN TKINTER
# ══════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lista = ListaSimple()
        self._cargar_ejemplo()
        self._setup_window()
        self._build_ui()
        self._refrescar()

    def _cargar_ejemplo(self):
        self.lista.agregar_final("Estudiar algoritmos de ordenamiento", "Alta")
        self.lista.agregar_final("Implementar árbol binario", "Media")
        self.lista.agregar_final("Revisar apuntes de pilas y colas", "Baja")

    def _setup_window(self):
        self.title("Taller · Lista Simple Enlazada")
        self.configure(bg=BG)
        self.geometry("920x700")
        self.minsize(800, 580)

    # ────────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ──────────────────────────────
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=30, pady=(24, 0))

        tk.Label(hdr, text="ESTRUCTURA DE DATOS  //  TALLER",
                 font=("Courier New", 8, "bold"), bg=BG, fg=ACCENT).pack(anchor="w")
        tk.Label(hdr, text="Lista de Tareas Pendientes",
                 font=("Courier New", 26, "bold"), bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(hdr, text="Implementación con Nodos enlazados en Python puro",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(anchor="w", pady=(2, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=30, pady=14)

        # ── Cuerpo ───────────────────────────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=30)
        body.columnconfigure(0, weight=0, minsize=270)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_panel_izq(body)
        self._build_panel_der(body)

        # ── Status bar ───────────────────────────
        self.status_var = tk.StringVar(value="Listo.")
        self._status_lbl = tk.Label(self, textvariable=self.status_var,
                                    font=FONT_SMALL, bg=SURFACE, fg=GREEN,
                                    anchor="w", padx=16, pady=7)
        self._status_lbl.pack(fill="x", side="bottom", pady=(10, 0))

    # ── Panel izquierdo ──────────────────────────
    def _build_panel_izq(self, parent):
        col = tk.Frame(parent, bg=BG)
        col.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        # Stats
        stats = self._frame_borde(col)
        stats.pack(fill="x", pady=(0, 12))
        tk.Label(stats, text="ESTADÍSTICAS", font=FONT_SMALL, bg=SURFACE,
                 fg=MUTED, padx=12, pady=8, anchor="w").pack(fill="x")
        self.sv = {k: tk.StringVar(value="0")
                   for k in ("Total", "Alta", "Media", "Baja")}
        colores = {"Total": TEXT, "Alta": RED, "Media": YELLOW, "Baja": GREEN}
        for k, var in self.sv.items():
            r = tk.Frame(stats, bg=SURFACE)
            r.pack(fill="x", padx=12, pady=3)
            tk.Label(r, text=k, font=FONT_SMALL, bg=SURFACE,
                     fg=MUTED, width=7, anchor="w").pack(side="left")
            tk.Label(r, textvariable=var, font=FONT_HEAD, bg=SURFACE,
                     fg=colores[k]).pack(side="right")
        tk.Frame(stats, bg=SURFACE, height=6).pack()

        # Agregar
        self._seccion(col, "AGREGAR TAREA")

        tk.Label(col, text="Descripción de la tarea", font=FONT_SMALL,
                 bg=BG, fg=MUTED, anchor="w").pack(fill="x", pady=(6, 2))
        self.e_tarea = self._entry(col)

        tk.Label(col, text="Prioridad", font=FONT_SMALL,
                 bg=BG, fg=MUTED, anchor="w").pack(fill="x", pady=(10, 2))

        self._style_ttk()
        self.combo = ttk.Combobox(col, values=["Alta", "Media", "Baja"],
                                   state="readonly", font=FONT_BODY)
        self.combo.set("Media")
        self.combo.pack(fill="x")

        self._btn(col, "⬇  Agregar al Final", ACCENT, self._agregar_final).pack(fill="x", pady=(10, 4))
        self._btn(col, "⬆  Agregar al Inicio", PURPLE, self._agregar_inicio).pack(fill="x")

        # Buscar / Eliminar
        self._seccion(col, "BUSCAR / ELIMINAR")

        tk.Label(col, text="Nombre exacto (o doble clic en fila)", font=FONT_SMALL,
                 bg=BG, fg=MUTED, anchor="w").pack(fill="x", pady=(6, 2))
        self.e_buscar = self._entry(col)

        self._btn(col, "🔍  Buscar en la Lista", SURFACE, self._buscar,
                  fg=GREEN, borde=GREEN).pack(fill="x", pady=(8, 4))
        self._btn(col, "✕  Eliminar Tarea", SURFACE, self._eliminar,
                  fg=RED, borde=RED).pack(fill="x")
        self._btn(col, "🗑  Vaciar Lista Completa", SURFACE, self._limpiar,
                  fg=MUTED, borde=BORDER).pack(fill="x", pady=(14, 0))

        self.e_tarea.bind("<Return>", lambda e: self._agregar_final())
        self.e_buscar.bind("<Return>", lambda e: self._buscar())

    # ── Panel derecho ────────────────────────────
    def _build_panel_der(self, parent):
        col = tk.Frame(parent, bg=BG)
        col.grid(row=0, column=1, sticky="nsew")
        col.rowconfigure(1, weight=1)
        col.columnconfigure(0, weight=1)

        # Diagrama
        diag_outer = self._frame_borde(col)
        diag_outer.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        tk.Label(diag_outer, text="DIAGRAMA DE ENLACE",
                 font=FONT_SMALL, bg=SURFACE, fg=MUTED,
                 padx=12, pady=8, anchor="w").pack(fill="x")

        self.lbl_diag = tk.Label(diag_outer, text="", font=("Courier New", 10),
                                  bg=SURFACE, fg=GREEN, padx=12, pady=10,
                                  anchor="w", wraplength=560, justify="left")
        self.lbl_diag.pack(fill="x")
        tk.Frame(diag_outer, bg=SURFACE, height=4).pack()

        # Lista (Treeview)
        tk.Label(col, text="NODOS DE LA LISTA",
                 font=FONT_SMALL, bg=BG, fg=MUTED,
                 anchor="w").grid(row=1, column=0, sticky="nw", pady=(0, 6))

        tree_frame = tk.Frame(col, bg=BG)
        tree_frame.grid(row=1, column=0, sticky="nsew", pady=(22, 0))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        cols = ("#", "Tarea", "Prioridad", "Fecha")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                  style="App.Treeview")

        for c, w, anchor in [("#", 38, "center"), ("Tarea", 260, "w"),
                               ("Prioridad", 90, "center"), ("Fecha", 135, "center")]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, stretch=(c == "Tarea"), anchor=anchor)

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        self.tree.tag_configure("Alta",  foreground=RED)
        self.tree.tag_configure("Media", foreground=YELLOW)
        self.tree.tag_configure("Baja",  foreground=GREEN)

        self.tree.bind("<Double-1>", self._clic_fila)

    # ────────────────────────────────────────────
    #  ACCIONES
    # ────────────────────────────────────────────
    def _agregar_final(self):
        tarea = self.e_tarea.get().strip()
        prio  = self.combo.get()
        if not tarea:
            return self._set_status("⚠ Escribe el nombre de la tarea.", YELLOW)
        msg = self.lista.agregar_final(tarea, prio)
        self.e_tarea.delete(0, "end")
        self._set_status(msg, GREEN if "✓" in msg else YELLOW)
        self._refrescar()

    def _agregar_inicio(self):
        tarea = self.e_tarea.get().strip()
        prio  = self.combo.get()
        if not tarea:
            return self._set_status("⚠ Escribe el nombre de la tarea.", YELLOW)
        msg = self.lista.agregar_inicio(tarea, prio)
        self.e_tarea.delete(0, "end")
        self._set_status(msg, GREEN if "✓" in msg else YELLOW)
        self._refrescar()

    def _eliminar(self):
        tarea = self.e_buscar.get().strip()
        if not tarea:
            sel = self.tree.selection()
            if sel:
                tarea = self.tree.item(sel[0], "values")[1]
            else:
                return self._set_status("⚠ Escribe o selecciona una tarea.", YELLOW)
        if not messagebox.askyesno("Confirmar eliminación",
                                   f"¿Eliminar la tarea?\n\n\"{tarea}\""):
            return
        msg = self.lista.eliminar(tarea)
        self.e_buscar.delete(0, "end")
        self._set_status(msg, GREEN if "✓" in msg else RED)
        self._refrescar()

    def _buscar(self):
        tarea = self.e_buscar.get().strip()
        if not tarea:
            return self._set_status("⚠ Escribe el nombre a buscar.", YELLOW)
        pos = self.lista.buscar(tarea)
        if pos != -1:
            self._set_status(f"✓ '{tarea}' encontrada en la posición {pos}.", GREEN)
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[1] == tarea:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    break
        else:
            self._set_status("✗ Tarea no encontrada en la lista.", RED)

    def _limpiar(self):
        if self.lista.esta_vacia():
            return self._set_status("⚠ La lista ya está vacía.", YELLOW)
        if messagebox.askyesno("Confirmar", "¿Vaciar toda la lista de tareas?"):
            self.lista.limpiar()
            self._set_status("✓ Lista vaciada.", GREEN)
            self._refrescar()

    def _clic_fila(self, event):
        sel = self.tree.selection()
        if sel:
            tarea = self.tree.item(sel[0], "values")[1]
            self.e_buscar.delete(0, "end")
            self.e_buscar.insert(0, tarea)

    # ────────────────────────────────────────────
    #  REFRESCO DE VISTA
    # ────────────────────────────────────────────
    def _refrescar(self):
        tareas = self.lista.obtener_todas()

        self.sv["Total"].set(str(len(tareas)))
        self.sv["Alta"].set(str(sum(1 for t in tareas if t["prioridad"] == "Alta")))
        self.sv["Media"].set(str(sum(1 for t in tareas if t["prioridad"] == "Media")))
        self.sv["Baja"].set(str(sum(1 for t in tareas if t["prioridad"] == "Baja")))

        self.lbl_diag.config(text=self.lista.cadena_texto())

        for item in self.tree.get_children():
            self.tree.delete(item)
        for t in tareas:
            self.tree.insert("", "end",
                             values=(t["pos"], t["tarea"], t["prioridad"], t["fecha"]),
                             tags=(t["prioridad"],))

    def _set_status(self, msg, color=TEXT):
        self.status_var.set(msg)
        self._status_lbl.config(fg=color)

    # ────────────────────────────────────────────
    #  HELPERS DE WIDGET
    # ────────────────────────────────────────────
    def _frame_borde(self, parent):
        return tk.Frame(parent, bg=SURFACE, highlightthickness=1,
                        highlightbackground=BORDER)

    def _seccion(self, parent, titulo):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", pady=(16, 0))
        tk.Frame(f, bg=ACCENT, width=3, height=13).pack(side="left")
        tk.Label(f, text=f"  {titulo}", font=("Courier New", 9, "bold"),
                 bg=BG, fg=MUTED).pack(side="left")

    def _entry(self, parent):
        e = tk.Entry(parent, font=FONT_BODY, bg=SURFACE, fg=TEXT,
                     insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=PURPLE)
        e.pack(fill="x", ipady=8, ipadx=6)
        return e

    def _btn(self, parent, text, bg, cmd, fg=TEXT, borde=None):
        b = tk.Button(parent, text=text, font=FONT_MONO, bg=bg, fg=fg,
                      activebackground=BORDER, activeforeground=TEXT,
                      relief="flat", cursor="hand2", command=cmd, pady=9,
                      highlightthickness=1,
                      highlightbackground=borde if borde else bg)
        return b

    def _style_ttk(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("App.Treeview",
                     background=CARD, foreground=TEXT,
                     fieldbackground=CARD, borderwidth=0,
                     rowheight=40, font=FONT_BODY)
        s.configure("App.Treeview.Heading",
                     background=SURFACE, foreground=MUTED,
                     borderwidth=0, font=("Courier New", 9, "bold"))
        s.map("App.Treeview",
              background=[("selected", PURPLE)],
              foreground=[("selected", TEXT)])
        s.configure("TCombobox",
                     fieldbackground=SURFACE, background=SURFACE,
                     foreground=TEXT, selectbackground=PURPLE,
                     selectforeground=TEXT)


# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
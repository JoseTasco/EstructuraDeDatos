import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid

# ════════════════════════════════════════════════════
#   DOUBLY LINKED LIST
# ════════════════════════════════════════════════════

class Node:
    def __init__(self, order: dict):
        self.order = order
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head   = None
        self.tail   = None
        self.cursor = None
        self.size   = 0

    # ── Add order at the end ─────────────────────
    def add(self, data: dict):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        if self.cursor is None:
            self.cursor = new_node
        return data

    # ── Cancel order by ID ───────────────────────
    def cancel(self, order_id: str) -> bool:
        node = self._find(order_id)
        if node is None:
            return False
        if self.cursor == node:
            self.cursor = node.next or node.prev
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.size -= 1
        return True

    # ── Change order status ──────────────────────
    def change_status(self, order_id: str, new_status: str) -> bool:
        node = self._find(order_id)
        if node:
            node.order["estado"] = new_status
            return True
        return False

    # ── Move cursor forward ──────────────────────
    def cursor_next(self):
        if self.cursor and self.cursor.next:
            self.cursor = self.cursor.next
            return self.cursor.order
        return None

    # ── Move cursor backward ─────────────────────
    def cursor_prev(self):
        if self.cursor and self.cursor.prev:
            self.cursor = self.cursor.prev
            return self.cursor.order
        return None

    # ── Get current cursor order ─────────────────
    def current_order(self):
        return self.cursor.order if self.cursor else None

    # ── Return all orders as list ─────────────────
    def get_all(self) -> list:
        result = []
        current = self.head
        while current:
            result.append({
                **current.order,
                "is_cursor": (current == self.cursor)
            })
            current = current.next
        return result

    # ── Find node by ID ──────────────────────────
    def _find(self, order_id: str):
        current = self.head
        while current:
            if current.order["id"] == order_id:
                return current
            current = current.next
        return None


# ════════════════════════════════════════════════════
#   TKINTER APPLICATION
# ════════════════════════════════════════════════════

STATUSES = ["pendiente", "preparando", "listo", "entregado"]

STATUS_COLOR = {
    "pendiente":  "#f59e0b",
    "preparando": "#60a5fa",
    "listo":      "#3ecf8e",
    "entregado":  "#888680",
}

BG        = "#0f0f11"
SURFACE   = "#18181c"
SURFACE2  = "#222228"
BORDER    = "#2a2a30"
TEXT      = "#f0ede8"
MUTED     = "#888680"
ACCENT    = "#ff6b35"
GREEN     = "#3ecf8e"
FONT_MAIN = ("Consolas", 10)
FONT_BIG  = ("Consolas", 13, "bold")
FONT_SM   = ("Consolas", 9)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.list = DoublyLinkedList()
        self.title("Gestión de Pedidos — Lista Doble")
        self.configure(bg=BG)
        self.geometry("980x680")
        self.resizable(True, True)
        self._build_ui()
        self._refresh()

    # ─────────────────────────────────────────────
    #  BUILD INTERFACE
    # ─────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self, bg=SURFACE, pady=12, padx=20)
        header.pack(fill="x")
        tk.Label(header, text="🍽  Gestión de Pedidos", bg=SURFACE,
                 fg=TEXT, font=("Consolas", 16, "bold")).pack(side="left")
        tk.Label(header, text="[ LISTA DOBLEMENTE ENLAZADA ]", bg=SURFACE,
                 fg=ACCENT, font=FONT_SM).pack(side="right", padx=10)

        # ── Main body ──
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # Left column
        left = tk.Frame(body, bg=BG, width=310)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        self._build_form(left)
        self._build_viz(left)

        # Right column
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_stats(right)
        self._build_nav(right)
        self._build_list(right)

    # ── Form panel ───────────────────────────────
    def _build_form(self, parent):
        frame = tk.LabelFrame(parent, text=" ➕ Nuevo Pedido ", bg=SURFACE,
                              fg=ACCENT, font=FONT_MAIN,
                              bd=1, relief="solid", padx=12, pady=10)
        frame.pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Cliente:", bg=SURFACE, fg=MUTED,
                 font=FONT_SM).pack(anchor="w")
        self.inp_client = tk.Entry(frame, bg=SURFACE2, fg=TEXT,
                                   insertbackground=TEXT, font=FONT_MAIN,
                                   relief="flat", bd=4)
        self.inp_client.pack(fill="x", pady=(2, 8))

        tk.Label(frame, text="Mesa:", bg=SURFACE, fg=MUTED,
                 font=FONT_SM).pack(anchor="w")
        self.inp_table = ttk.Combobox(frame, values=[
            "Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4", "Mesa 5", "Para llevar"
        ], font=FONT_MAIN, state="readonly")
        self.inp_table.pack(fill="x", pady=(2, 8))

        tk.Label(frame, text="Items del pedido:", bg=SURFACE, fg=MUTED,
                 font=FONT_SM).pack(anchor="w")
        self.inp_items = tk.Text(frame, bg=SURFACE2, fg=TEXT,
                                 insertbackground=TEXT, font=FONT_MAIN,
                                 relief="flat", bd=4, height=4)
        self.inp_items.pack(fill="x", pady=(2, 10))

        btn = tk.Button(frame, text="  +  AGREGAR PEDIDO  ",
                        bg=ACCENT, fg="white", font=("Consolas", 11, "bold"),
                        relief="flat", cursor="hand2",
                        command=self._add_order)
        btn.pack(fill="x", ipady=6)

    # ── List structure visualization ─────────────
    def _build_viz(self, parent):
        frame = tk.LabelFrame(parent, text=" ESTRUCTURA DE LA LISTA ",
                              bg=SURFACE, fg=MUTED, font=FONT_SM,
                              bd=1, relief="solid", padx=8, pady=8)
        frame.pack(fill="x")

        self.viz_canvas = tk.Canvas(frame, bg=SURFACE, height=70,
                                    highlightthickness=0)
        self.viz_canvas.pack(fill="x")

    # ── Stats row ────────────────────────────────
    def _build_stats(self, parent):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 10))

        self.lbl_total   = self._stat_card(row, "0", "TOTAL",      ACCENT)
        self.lbl_pending = self._stat_card(row, "0", "PENDIENTES", "#f59e0b")
        self.lbl_ready   = self._stat_card(row, "0", "LISTOS",     GREEN)

    def _stat_card(self, parent, value, label, color):
        f = tk.Frame(parent, bg=SURFACE, bd=0, padx=14, pady=10)
        f.pack(side="left", padx=(0, 8))
        lbl_num = tk.Label(f, text=value, bg=SURFACE, fg=color,
                           font=("Consolas", 22, "bold"))
        lbl_num.pack()
        tk.Label(f, text=label, bg=SURFACE, fg=MUTED,
                 font=FONT_SM).pack()
        return lbl_num

    # ── Cursor navigation bar ────────────────────
    def _build_nav(self, parent):
        nav = tk.Frame(parent, bg=SURFACE, pady=10, padx=14)
        nav.pack(fill="x", pady=(0, 10))

        self.btn_prev = tk.Button(nav, text="◀  Anterior",
                                  bg=SURFACE2, fg=TEXT, font=FONT_MAIN,
                                  relief="flat", bd=0, padx=10, pady=6,
                                  cursor="hand2", command=self._nav_prev)
        self.btn_prev.pack(side="left")

        self.lbl_cursor = tk.Label(nav, text="— Sin pedidos —",
                                   bg=SURFACE, fg=TEXT,
                                   font=("Consolas", 11, "bold"))
        self.lbl_cursor.pack(side="left", expand=True)

        self.btn_next = tk.Button(nav, text="Siguiente  ▶",
                                  bg=SURFACE2, fg=TEXT, font=FONT_MAIN,
                                  relief="flat", bd=0, padx=10, pady=6,
                                  cursor="hand2", command=self._nav_next)
        self.btn_next.pack(side="right")

    # ── Scrollable orders list ───────────────────
    def _build_list(self, parent):
        tk.Label(parent, text="── NODOS EN LA LISTA ──",
                 bg=BG, fg=MUTED, font=FONT_SM).pack(anchor="w")

        wrapper = tk.Frame(parent, bg=BG)
        wrapper.pack(fill="both", expand=True, pady=(4, 0))

        scrollbar = tk.Scrollbar(wrapper, bg=SURFACE2, troughcolor=BG)
        scrollbar.pack(side="right", fill="y")

        self.canvas_list = tk.Canvas(wrapper, bg=BG,
                                     yscrollcommand=scrollbar.set,
                                     highlightthickness=0)
        self.canvas_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.canvas_list.yview)

        self.frame_list = tk.Frame(self.canvas_list, bg=BG)
        self.canvas_list.create_window((0, 0), window=self.frame_list,
                                       anchor="nw")
        self.frame_list.bind("<Configure>",
            lambda e: self.canvas_list.configure(
                scrollregion=self.canvas_list.bbox("all")))

    # ─────────────────────────────────────────────
    #  ACTION HANDLERS
    # ─────────────────────────────────────────────

    def _add_order(self):
        client = self.inp_client.get().strip()
        items  = self.inp_items.get("1.0", "end").strip()
        table  = self.inp_table.get()

        if not client or not items:
            messagebox.showwarning("Campos vacíos",
                                   "Debes ingresar cliente e items del pedido.")
            return

        order = {
            "id":      str(uuid.uuid4())[:6].upper(),
            "cliente": client,
            "items":   items,
            "mesa":    table or "—",
            "estado":  "pendiente",
            "hora":    datetime.now().strftime("%H:%M"),
        }
        self.list.add(order)

        # Clear form
        self.inp_client.delete(0, "end")
        self.inp_items.delete("1.0", "end")
        self.inp_table.set("")
        self._refresh()

    def _cancel_order(self, order_id):
        if messagebox.askyesno("Cancelar pedido",
                               f"¿Cancelar el pedido #{order_id}?"):
            self.list.cancel(order_id)
            self._refresh()

    def _advance_status(self, order_id, current_status):
        idx        = STATUSES.index(current_status)
        new_status = STATUSES[(idx + 1) % len(STATUSES)]
        self.list.change_status(order_id, new_status)
        self._refresh()

    def _nav_next(self):
        result = self.list.cursor_next()
        if result is None:
            messagebox.showinfo("Navegación", "Ya estás en el último pedido.")
        self._refresh()

    def _nav_prev(self):
        result = self.list.cursor_prev()
        if result is None:
            messagebox.showinfo("Navegación", "Ya estás en el primer pedido.")
        self._refresh()

    # ─────────────────────────────────────────────
    #  UI REFRESH
    # ─────────────────────────────────────────────

    def _refresh(self):
        orders = self.list.get_all()

        # Update stats
        total   = len(orders)
        pending = sum(1 for o in orders if o["estado"] == "pendiente")
        ready   = sum(1 for o in orders if o["estado"] == "listo")
        self.lbl_total.config(text=str(total))
        self.lbl_pending.config(text=str(pending))
        self.lbl_ready.config(text=str(ready))

        # Update cursor label
        current = self.list.current_order()
        if current:
            self.lbl_cursor.config(
                text=f"[ CURSOR ]  #{current['id']} — {current['cliente']}")
        else:
            self.lbl_cursor.config(text="— Sin pedidos —")

        # Redraw structure visualization
        self._draw_viz(orders)

        # Clear and repopulate order cards
        for widget in self.frame_list.winfo_children():
            widget.destroy()

        if not orders:
            tk.Label(self.frame_list,
                     text="\n  No hay pedidos.\n  Agrega uno con el formulario.\n",
                     bg=BG, fg=MUTED, font=FONT_MAIN).pack(padx=8)
            return

        for order in orders:
            self._order_card(order)

    def _order_card(self, order):
        is_cursor    = order.get("is_cursor", False)
        border_color = ACCENT if is_cursor else BORDER
        bg_card      = "#1e1a16" if is_cursor else SURFACE

        card = tk.Frame(self.frame_list, bg=bg_card,
                        highlightbackground=border_color,
                        highlightthickness=2, pady=8, padx=12)
        card.pack(fill="x", pady=4, padx=4)

        # Top row: ID + cursor badge + time
        top = tk.Frame(card, bg=bg_card)
        top.pack(fill="x")

        tk.Label(top, text=f"#{order['id']}", bg=bg_card,
                 fg=ACCENT if is_cursor else MUTED, font=FONT_SM).pack(side="left")

        if is_cursor:
            tk.Label(top, text=" ◀ CURSOR ", bg=ACCENT, fg="white",
                     font=("Consolas", 8, "bold"), padx=4).pack(side="left", padx=6)

        tk.Label(top, text=order["hora"], bg=bg_card,
                 fg=MUTED, font=FONT_SM).pack(side="right")

        # Client name
        tk.Label(card, text=order["cliente"], bg=bg_card, fg=TEXT,
                 font=("Consolas", 12, "bold"), anchor="w").pack(fill="x", pady=(2, 0))

        # Table
        tk.Label(card, text=f"Mesa: {order['mesa']}", bg=bg_card,
                 fg=MUTED, font=FONT_SM, anchor="w").pack(fill="x")

        # Items
        tk.Label(card, text=order["items"], bg=bg_card,
                 fg="#b0ada8", font=FONT_MAIN, anchor="w",
                 wraplength=480, justify="left").pack(fill="x", pady=(2, 6))

        # Bottom row: status + action buttons
        bottom = tk.Frame(card, bg=bg_card)
        bottom.pack(fill="x")

        status_color = STATUS_COLOR.get(order["estado"], MUTED)
        tk.Label(bottom, text=f"● {order['estado'].upper()}",
                 bg=bg_card, fg=status_color,
                 font=("Consolas", 9, "bold")).pack(side="left")

        # Cancel button
        tk.Button(bottom, text="✕ Cancelar",
                  bg="#2a1a1a", fg="#f87171", font=FONT_SM,
                  relief="flat", bd=0, padx=8, pady=3,
                  cursor="hand2",
                  command=lambda oid=order["id"]: self._cancel_order(oid)
                  ).pack(side="right", padx=(6, 0))

        # Advance status button
        tk.Button(bottom, text="→ Avanzar estado",
                  bg=SURFACE2, fg=TEXT, font=FONT_SM,
                  relief="flat", bd=0, padx=8, pady=3,
                  cursor="hand2",
                  command=lambda oid=order["id"], st=order["estado"]:
                      self._advance_status(oid, st)
                  ).pack(side="right")

    # ── Draw doubly linked list visualization ─────
    def _draw_viz(self, orders):
        c = self.viz_canvas
        c.delete("all")
        w = c.winfo_width() or 290

        if not orders:
            c.create_text(w // 2, 35, text="NULL ←  vacía  → NULL",
                          fill=MUTED, font=FONT_SM)
            return

        n       = len(orders)
        box_w   = 54
        arrow_w = 22
        total_w = n * box_w + (n + 1) * arrow_w + 40
        x = (w - total_w) // 2 + 20
        y = 35

        # Left NULL
        c.create_text(x, y, text="NULL", fill=MUTED, font=FONT_SM)
        x += 28

        for order in orders:
            # Left arrow
            c.create_text(x, y, text="←", fill=BORDER, font=FONT_MAIN)
            x += arrow_w

            # Node box
            box_color  = ACCENT  if order["is_cursor"] else SURFACE2
            text_color = "white" if order["is_cursor"] else TEXT
            c.create_rectangle(x, y - 16, x + box_w, y + 16,
                                fill=box_color,
                                outline=ACCENT if order["is_cursor"] else BORDER)
            c.create_text(x + box_w // 2, y - 4,
                          text=f"#{order['id']}", fill=text_color, font=FONT_SM)
            c.create_text(x + box_w // 2, y + 8,
                          text=order["estado"][:4], fill=text_color,
                          font=("Consolas", 7))
            x += box_w

            # Right arrow
            c.create_text(x, y, text="→", fill=BORDER, font=FONT_MAIN)
            x += arrow_w

        # Right NULL
        c.create_text(x, y, text="NULL", fill=MUTED, font=FONT_SM)


# ════════════════════════════════════════════════════
#   ENTRY POINT
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.mainloop()
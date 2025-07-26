import tkinter as tk 
from tkinter import messagebox, ttk
from struk_generator import buat_struk_pdf

# Harga layanan
layanan_dict = {
    "Fotocopy": 500,
    "Print A4": 1000,
    "Print F4": 2000,
    "Undangan 600": 600,
    "Undangan 500": 500,
    "Undangan 800": 800,
    "Undangan 1500": 1500,
    "Foto Ukuran 10 Inci": 15000,
    "Phas Foto 2x3": 1000,
    "Phas Foto 3x4": 2500,
    "Phas Foto 4x6": 3000,
    "Phas Foto 6x8": 5000,
    "Laminating": 5000,
}

items = []
total = 0
bayar = 0
dp = 0
kembalian = 0

def format_ribuan(entry):
    try:
        value = entry.get().replace(",", "")
        if value == "":
            return
        int_value = int(value)
        entry.delete(0, tk.END)
        entry.insert(0, f"{int_value:,}")
    except ValueError:
        pass

def tambah_item():
    layanan = layanan_var.get()
    try:
        qty = int(jumlah_entry.get())
    except:
        messagebox.showerror("Error", "Jumlah harus berupa angka.")
        return

    harga = layanan_dict[layanan]
    subtotal = harga * qty
    items.append((layanan, qty, harga, subtotal))

    tree.insert("", "end", values=(len(items), layanan, qty, f"Rp{subtotal:,}"))
    update_total()
    jumlah_entry.delete(0, tk.END)

def update_total():
    global total
    total = sum(item[3] for item in items)
    total_label.config(text=f"Total: Rp{total:,}")

def proses_pembayaran():
    global bayar, dp, kembalian
    try:
        dp = int(dp_entry.get().replace(",", "")) if dp_entry.get() else 0
        bayar = int(bayar_entry.get().replace(",", ""))
    except:
        messagebox.showerror("Error", "Masukkan angka yang valid untuk Panjar dan Bayar.")
        return

    total_setelah_dp = total - dp

    if bayar < total_setelah_dp:
        output_label.config(
            text=f"Uang bayar kurang!\nSisa setelah Panjar: Rp{total_setelah_dp:,}",
            fg="red"
        )
    else:
        kembalian = bayar - total_setelah_dp
        output_label.config(
            text=f"Transaksi berhasil!\nKembalian: Rp{kembalian:,}",
            fg="green"
        )

def cetak_struk():
    if not items:
        messagebox.showwarning("Kosong", "Belum ada item untuk dicetak.")
        return

    if total == 0 or bayar == 0:
        messagebox.showwarning("Belum Dibayar", "Silakan proses pembayaran dulu.")
        return

    buat_struk_pdf(items, total, bayar, kembalian, dp)
    reset_semua()

def cek_sisa_dp():
    try:
        dp = int(dp_entry.get().replace(",", "")) if dp_entry.get() else 0
        sisa = total - dp
        if sisa <= 0:
            output_label.config(
                text=f"Tidak ada sisa pembayaran.\nTotal sudah ditutup DP.",
                fg="blue"
            )
        else:
            output_label.config(
                text=f"Sisa yang harus dibayar: Rp{sisa:,}",
                fg="orange"
            )
    except:
        messagebox.showerror("Error", "Masukkan angka yang valid untuk Panjar.")

def reset_semua():
    global total, bayar, dp, kembalian
    items.clear()
    for row in tree.get_children():
        tree.delete(row)
    bayar_entry.delete(0, tk.END)
    dp_entry.delete(0, tk.END)
    jumlah_entry.delete(0, tk.END)
    update_total()
    total = bayar = dp = kembalian = 0
    output_label.config(text="")

# GUI
root = tk.Tk()
root.title("Arjuna Fotocopy")
root.geometry("800x720")

judul_label = tk.Label(root, text="ARJUNA FOTOCOPY", font=("Arial", 16, "bold"))
judul_label.pack(pady=10)

layanan_var = tk.StringVar(value="Print A4")

tk.Label(root, text="Layanan:").pack()
tk.OptionMenu(root, layanan_var, *layanan_dict.keys()).pack()

tk.Label(root, text="Jumlah:").pack()
jumlah_entry = tk.Entry(root)
jumlah_entry.pack()

tk.Button(root, text="Tambah", command=tambah_item, width=15, height=1, cursor="hand2").pack(pady=5)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

tabel_frame = tk.Frame(main_frame)
tabel_frame.pack(side="left", padx=10, pady=10)

style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

columns = ("No", "Jenis Layanan", "Jumlah", "Harga")
tree = ttk.Treeview(tabel_frame, columns=columns, show="headings", style="Treeview")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

tree.column("No", width=40)
tree.column("Jenis Layanan", width=200)
tree.column("Jumlah", width=80)
tree.column("Harga", width=100)
tree.pack()

pembayaran_frame = tk.Frame(main_frame)
pembayaran_frame.pack(side="right", padx=20, pady=10, fill="both", expand=True)

total_label = tk.Label(pembayaran_frame, text="Total: Rp0", font=("Arial", 12, "bold"))
total_label.pack(pady=5)

tk.Label(pembayaran_frame, text="Panjar (DP):").pack()
dp_entry = tk.Entry(pembayaran_frame)
dp_entry.pack()

tk.Label(pembayaran_frame, text="Bayar (Rp):").pack()
bayar_entry = tk.Entry(pembayaran_frame)
bayar_entry.pack()

# Format angka otomatis
dp_entry.bind("<KeyRelease>", lambda event: format_ribuan(dp_entry))
bayar_entry.bind("<KeyRelease>", lambda event: format_ribuan(bayar_entry))

output_label = tk.Label(pembayaran_frame, text="", font=("Arial", 12), fg="green", justify="center")
output_label.pack(pady=10)

btn_cek_sisa = tk.Button(
    pembayaran_frame,
    text="Cek Sisa DP",
    bg="#ffd700",
    command=cek_sisa_dp,
    width=20,
    height=1,
    cursor="hand2"
)
btn_cek_sisa.pack(pady=3)

btn_proses = tk.Button(
    pembayaran_frame,
    text="Proses Pembayaran",
    bg="#8fbc8f",
    command=proses_pembayaran,
    width=20,
    height=2,
    cursor="hand2"
)
btn_proses.pack(pady=3)

btn_struk = tk.Button(
    pembayaran_frame,
    text="Cetak Struk",
    bg="#add8e6",
    command=cetak_struk,
    width=20,
    height=2,
    cursor="hand2"
)
btn_struk.pack(pady=3)

tk.Button(
    root,
    text="Reset",
    bg="#f08080",
    command=reset_semua,
    width=20,
    height=2,
    cursor="hand2"
).pack(pady=10)

root.mainloop()

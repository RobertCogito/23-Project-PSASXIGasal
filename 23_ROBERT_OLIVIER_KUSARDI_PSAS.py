import tkinter as tk
from tkinter import ttk
from natsort import natsorted

# ----------------- DATA -----------------
data_siswa = [  
    {"username": "admin", 
     "password": "admin123", 
     "nama": "Admin", 
     "kelas": "XI-12", 
     "nilai_mapil": [], 
     "nilai_mapel": [], 
     "mean_nilai": 0}
]

list_mapel = [
    "PKN", "Sejarah", "Bahasa Jawa", "Bahasa Inggris", "Bahasa Indonesia",
    "PAK", "Academic English", "PJOK", "TP", "Matematika Wajib"
]

current_user = 0
list_entry_nilai = []

# ----------------- FUNCTIONS -----------------
def switch_frame(frame):
    if frame == halaman_dashboard:
        populate_welcome()
    frame.tkraise()
    
def cek_login():
    global current_user
    username = user_var.get().strip()
    password = pass_var.get().strip()


    for i, s in enumerate(data_siswa):
        if s.get("username") == username and s.get("password") == password:
            current_user = i
            label_status_login.config(text="Login berhasil!", foreground="#00ff0d")
            populate_welcome()
            switch_frame(halaman_dashboard)
            return

    label_status_login.config(text="Username atau password salah!", foreground="#c62828")


def signup():
    username = signup_user_var.get().strip()
    password = signup_pass_var.get().strip()
    konfirmasi = signup_confirm_var.get().strip()

    if not username or not password or not konfirmasi:
        label_status_signup.config(text="Semua kolom harus diisi!", foreground="#c62828")
        return

    if password != konfirmasi:
        label_status_signup.config(text="Password tidak sama!", foreground="#c62828")
        return

    if any(u.get("username") == username for u in data_siswa):
        label_status_signup.config(text="Username sudah dipakai!", foreground="#c62828")
        return

    data_siswa.append({
        "username": username,
        "password": password,
        "nama": "",
        "kelas": "",
        "nilai_mapil": [],
        "nilai_mapel": [],
        "mean_nilai": 0
    })
    label_status_signup.config(text="Akun berhasil dibuat! Silahkan login", foreground="#00ff0d")
    entry_usn_baru.delete(0, tk.END)
    entry_pass_baru.delete(0, tk.END)
    entry_confirm_pass_baru.delete(0, tk.END)


def populate_welcome():
    s = data_siswa[current_user]
    nama = s.get("nama") or ""
    klas = s.get("kelas") or ""
    label_welcome.config(text=f"Halo, {nama} — {klas}")


def update_mapil():
    nama = entry_nama.get().strip()
    kelas = combobox_kelas.get().strip()

    if not nama or not kelas:
        label_di_hal_input_nama.config(text="Semua kolom harus diisi!", foreground="#c62828")
        return

    label_di_hal_input_nama.config(text="")
    data_siswa[current_user]["nama"] = nama
    data_siswa[current_user]["kelas"] = kelas

    # Pilih label mapil sesuai kelas
    mapil_khusus = {
        ("XI-1", "XI-2", "XI-3"): ["Fisika", "Matematika Lanjut", "Biologi", "Kimia"],
        ("XI-4", "XI-5"): ["Fisika", "Matematika Lanjut", "TIK", "Kimia"],
        ("XI-6", "XI-7", "XI-8"): ["Fisika", "Matematika Lanjut", "Ekonomi", "Geografi"],
        ("XI-9", "XI-10", "XI-11"): ["Sosiologi", "Ekonomi", "Geografi", "Antropologi"],
        ("XI-12",): ["Mapil 1", "Mapil 2", "Mapil 3", "Mapil 4"],
    }

    judul_mapil = ["Mapil 1", "Mapil 2", "Mapil 3", "Mapil 4"]
    for k, v in mapil_khusus.items():
        if kelas in k:
            judul_mapil = v
            break

    nilai_mapil1.config(text=f"Nilai {judul_mapil[0]}")
    nilai_mapil2.config(text=f"Nilai {judul_mapil[1]}")
    nilai_mapil3.config(text=f"Nilai {judul_mapil[2]}")
    nilai_mapil4.config(text=f"Nilai {judul_mapil[3]}")

    # Bersihkan nilai mapel sebelumnya
    for e in list_entry_nilai:
        e.delete(0, tk.END)

    switch_frame(halaman_input_data_nilai)


def simpan_data():
    # Validasi mapil
    try:
        nilai1 = float(entry_nilai_mapil1.get().strip())
        nilai2 = float(entry_nilai_mapil2.get().strip())
        nilai3 = float(entry_nilai_mapil3.get().strip())
        nilai4 = float(entry_nilai_mapil4.get().strip())
    except ValueError:
        label_status.config(text="Isi semua nilai mapil dengan angka!", foreground="#c62828")
        return

    # Ambil nilai mapel wajib
    nilai_mapel_lain = []
    for i in list_entry_nilai:
        v = i.get().strip()
        try:
            nilai_mapel_lain.append(float(v))
        except ValueError:
            label_status.config(text="Semua nilai mapel harus angka!", foreground="#c62828")
            return

    data_siswa[current_user]["nilai_mapil"] = [nilai1, nilai2, nilai3, nilai4]
    data_siswa[current_user]["nilai_mapel"] = nilai_mapel_lain

    total_mapel = 4 + len(nilai_mapel_lain)
    total_nilai = sum([nilai1, nilai2, nilai3, nilai4]) + sum(nilai_mapel_lain)
    mean = round(total_nilai / total_mapel, 2) if total_mapel > 0 else 0
    data_siswa[current_user]["mean_nilai"] = mean

    label_status.config(text="Data berhasil disimpan!", foreground="#2e7d32")


def tampilkan_data():
    tree.delete(*tree.get_children())
    for i, s in enumerate(data_siswa, start=1):
        nama = s.get("nama") or "-"
        kelas = s.get("kelas") or "-"
        mean = s.get("mean_nilai") if s.get("mean_nilai") is not None else "-"
        tree.insert("", tk.END, values=(i, nama, kelas, mean))
    switch_frame(halaman_nampilin_data)


def cari_data():
    keyword = entry_cari.get().strip().lower()
    tree_cari.delete(*tree_cari.get_children())
    if not keyword:
        return

    found = False
    for s in data_siswa:
        nama = (s.get("nama") or "").lower()
        if keyword in nama:
            tree_cari.insert("", tk.END, values=(s.get("nama") or "-", s.get("kelas") or "-", s.get("mean_nilai") or "-"))
            found = True
    if not found:
        tree_cari.insert("", tk.END, values=("Tidak ditemukan", "-", "-"))


def logout():
    global current_user
    current_user = 0
    entry_user.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    label_status_login.config(text="")
    label_status_signup.config(text="")
    switch_frame(halaman_login)

def sort_treeview(tree, col, reverse):
    # Ambil semua data dari TreeView
    data = [(tree.set(item, col), item) for item in tree.get_children('')]

    # Sorting pakai natsort
    sorted_data = natsorted(data, key=lambda x: x[0], reverse=reverse)

    # Masukkan kembali ke TreeView
    for index, (val, item) in enumerate(sorted_data):
        tree.move(item, '', index)

    # Toggle sorting arah berikutnya
    tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))

# ----------------- UI -----------------
root = tk.Tk()
root.title("Aplikasi Data Peserta Didik A1")
root.geometry("980x620")
root.configure(bg="#f6f8fb")

style = ttk.Style()
style.configure('Card.TFrame', background="#5b82cb")
style.configure('Search.TLabel', background="#8236d3")
style.theme_use('clam')
style.configure('TFrame', background='#5b82cb')
style.configure('TLabel', background='#5b82cb', font=('Segoe UI', 11))
style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=6)
style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
style.configure('Colorful.TCheckbutton', background='#5b82cb', foreground='white', font=('Segoe UI', 12, 'bold'))

# ----------------- TKINTER VARIABLES -----------------
user_var = tk.StringVar()
pass_var = tk.StringVar()

signup_user_var = tk.StringVar()
signup_pass_var = tk.StringVar()
signup_confirm_var = tk.StringVar()

show_login_pass = tk.BooleanVar(value=False)
show_signup_pass = tk.BooleanVar(value=False)
show_signup_confirm = tk.BooleanVar(value=False)

# frames
halaman_login = ttk.Frame(root)
halaman_signup = ttk.Frame(root)
halaman_dashboard = ttk.Frame(root)
halaman_input_nama = ttk.Frame(root)
halaman_input_data_nilai = ttk.Frame(root)
halaman_cari_data = ttk.Frame(root)
halaman_nampilin_data = ttk.Frame(root)

for frame in (halaman_login, halaman_signup, halaman_dashboard, halaman_input_nama, halaman_input_data_nilai, halaman_cari_data, halaman_nampilin_data):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# ---------- LOGIN ----------
frm_login_card = ttk.Frame(halaman_login)
frm_login_card.place(relx=0.5, rely=0.45, anchor='center')

ttk.Label(frm_login_card, text='Aplikasi Data Peserta Didik A1', style='Header.TLabel').pack(pady=(0,10))

entry_user = ttk.Entry(frm_login_card, width=36, textvariable=user_var)
entry_password = ttk.Entry(frm_login_card, width=36, show="*", textvariable=pass_var)

ttk.Label(frm_login_card, text='Username').pack(anchor='w')
entry_user.pack(pady=4)
ttk.Label(frm_login_card, text='Password').pack(anchor='w')
entry_password.pack(pady=4)

# Checkbox show/hide password login
def toggle_login_password():
    if show_login_pass.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

cb_login_show = tk.Checkbutton(
    frm_login_card,
    text="Show Password",
    bg='#5b82cb',
    fg='white',
    activebackground='#4c6aa3',
    variable=show_login_pass,
    command=toggle_login_password
)
cb_login_show.pack(pady=(0, 6))

button_login = ttk.Button(frm_login_card, text='Login', command=cek_login)
button_login.pack(pady=8)

label_status_login = ttk.Label(frm_login_card, text='', foreground='#c62828')
label_status_login.pack()

link_signup = ttk.Button(frm_login_card, text='Belum punya akun? Daftar', command=lambda: switch_frame(halaman_signup))
link_signup.pack(pady=(8,0))

# ---------- SIGNUP ----------
frm_signup_card = ttk.Frame(halaman_signup)
frm_signup_card.place(relx=0.5, rely=0.45, anchor='center')

ttk.Label(frm_signup_card, text='Buat Akun Baru', style='Header.TLabel').pack(pady=(0,10))
entry_usn_baru = ttk.Entry(frm_signup_card, width=36, textvariable=signup_user_var)
entry_pass_baru = ttk.Entry(frm_signup_card, width=36, show="*", textvariable=signup_pass_var)
entry_confirm_pass_baru = ttk.Entry(frm_signup_card, width=36, show="*", textvariable=signup_confirm_var)

ttk.Label(frm_signup_card, text='Username').pack(anchor='w')
entry_usn_baru.pack(pady=4)
ttk.Label(frm_signup_card, text='Password').pack(anchor='w')
entry_pass_baru.pack(pady=4)

# Checkbox control
def toggle_signup_password():
    entry_pass_baru.config(show="" if show_signup_pass.get() else "*")
def toggle_signup_confirm():
    entry_confirm_pass_baru.config(show="" if show_signup_confirm.get() else "*")

cb_signup_pass = tk.Checkbutton(
    frm_signup_card,
    text="Show Password",
    bg='#5b82cb',
    fg='white',
    activebackground='#4c6aa3',
    variable=show_signup_pass,
    command=toggle_signup_password,
)

cb_signup_confirm = tk.Checkbutton(
    frm_signup_card,
    text="Show Confirm Password",
    bg='#5b82cb',
    fg='white',
    activebackground='#4c6aa3',
    variable=show_signup_confirm,
    command=toggle_signup_confirm
)

cb_signup_pass.pack()
ttk.Label(frm_signup_card, text='Konfirmasi Password').pack(anchor='w')
entry_confirm_pass_baru.pack(pady=4)
cb_signup_confirm.pack()

btn_signup_submit = ttk.Button(frm_signup_card, text='Daftar', command=signup)
btn_signup_submit.pack(pady=8)

label_status_signup = ttk.Label(frm_signup_card, text='')
label_status_signup.pack()

btn_back_login = ttk.Button(frm_signup_card, text='Kembali', command=lambda: switch_frame(halaman_login))
btn_back_login.pack(pady=(6,0))

# ---------- DASHBOARD ----------
header = ttk.Frame(halaman_dashboard)
header.pack(fill='x', padx=20, pady=10)

label_welcome = ttk.Label(header, text='Halo, (belum login)', style='Header.TLabel')
label_welcome.pack(side='left')

btn_logout = ttk.Button(header, text='Logout', command=logout)
btn_logout.pack(side='right')

# menu cards
menu_frame = ttk.Frame(halaman_dashboard)
menu_frame.pack(pady=30)

btn_input_data = ttk.Button(menu_frame, text='Input Data Peserta Didik', width=30, command=lambda: switch_frame(halaman_input_nama))
btn_view_data = ttk.Button(menu_frame, text='Lihat Semua Data', width=30, command=tampilkan_data)
btn_search = ttk.Button(menu_frame, text='Cari Data', width=30, command=lambda: switch_frame(halaman_cari_data))

btn_input_data.grid(row=0, column=0, padx=10, pady=8)
btn_view_data.grid(row=1, column=0, padx=10, pady=8)
btn_search.grid(row=2, column=0, padx=10, pady=8)

# ---------- INPUT NAMA & KELAS ----------
card_nama = ttk.Frame(halaman_input_nama)
card_nama.place(relx=0.5, rely=0.4, anchor='center')

ttk.Label(card_nama, text='Masukkan Nama & Kelas', style='Header.TLabel').pack(pady=(0,10))
ttk.Label(card_nama, text='Nama', style='Header.TLabel').pack(pady=(0,10))
entry_nama = ttk.Entry(card_nama, width=40)
entry_nama.pack(pady=4)

ttk.Label(card_nama, text='Kelas', style='Header.TLabel').pack(pady=(0,10))
combobox_kelas = ttk.Combobox(card_nama, values=("XI-1","XI-2","XI-3","XI-4","XI-5","XI-6","XI-7","XI-8","XI-9","XI-10","XI-11","XI-12"), width=38)
combobox_kelas.pack(pady=4)

label_di_hal_input_nama = ttk.Label(card_nama, text='')
label_di_hal_input_nama.pack(pady=6)

btn_next_mapil = ttk.Button(card_nama, text='Next', command=update_mapil)
btn_next_mapil.pack(pady=6)

btn_back_dashboard = ttk.Button(card_nama, text='Kembali', command=lambda: switch_frame(halaman_dashboard))
btn_back_dashboard.pack()

# ---------- INPUT NILAI ----------
canvas_frame = ttk.Frame(halaman_input_data_nilai)
canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)

left_col = ttk.Frame(canvas_frame)
left_col.pack(side='left', fill='y', padx=10)

right_col = ttk.Frame(canvas_frame)
right_col.pack(side='right', fill='both', expand=True, padx=10)

# Mapil labels
nilai_mapil1 = ttk.Label(left_col, text='')
nilai_mapil1.pack(anchor='w', pady=6)
entry_nilai_mapil1 = ttk.Entry(left_col, width=18)
entry_nilai_mapil1.pack(pady=2)

nilai_mapil2 = ttk.Label(left_col, text='')
nilai_mapil2.pack(anchor='w', pady=6)
entry_nilai_mapil2 = ttk.Entry(left_col, width=18)
entry_nilai_mapil2.pack(pady=2)

nilai_mapil3 = ttk.Label(left_col, text='')
nilai_mapil3.pack(anchor='w', pady=6)
entry_nilai_mapil3 = ttk.Entry(left_col, width=18)
entry_nilai_mapil3.pack(pady=2)

nilai_mapil4 = ttk.Label(left_col, text='')
nilai_mapil4.pack(anchor='w', pady=6)
entry_nilai_mapil4 = ttk.Entry(left_col, width=18)
entry_nilai_mapil4.pack(pady=2)

# Mapel wajib (scrollable)
scroll_container = ttk.Frame(right_col)
scroll_container.pack(side="right", fill='both', expand=True)

canvas_inside = tk.Canvas(scroll_container, borderwidth=0, highlightthickness=0, background='#5b82cb')
frame_inside = ttk.Frame(canvas_inside)
vsb = ttk.Scrollbar(scroll_container, orient='vertical', command=canvas_inside.yview)
canvas_inside.configure(yscrollcommand=vsb.set)

vsb.pack(side='right', fill='y')
canvas_inside.pack(side='left', fill='both', expand=True)
canvas_inside.create_window((0,0), window=frame_inside, anchor='nw')

frame_inside.bind('<Configure>', lambda e: canvas_inside.configure(scrollregion=canvas_inside.bbox('all')))

list_entry_nilai.clear()
for mapel in list_mapel:
    ttk.Label(frame_inside, text=f"Nilai {mapel}").pack(anchor='w', pady=(6,0))
    ent = ttk.Entry(frame_inside, width=30)
    ent.pack(pady=2)
    list_entry_nilai.append(ent)

label_status = ttk.Label(halaman_input_data_nilai, text='')
label_status.pack(pady=8)

btn_simpan_data = ttk.Button(halaman_input_data_nilai, text='Simpan Data', command=simpan_data)
btn_simpan_data.pack(pady=(0,6))

btn_back_to_dash = ttk.Button(halaman_input_data_nilai, text='Kembali ke Dashboard', command=lambda: switch_frame(halaman_dashboard))
btn_back_to_dash.pack()

# ---------- CARI DATA ----------
card_cari = ttk.Frame(halaman_cari_data, style='Card.TFrame')
card_cari.place(relx=0.5, rely=0.06, anchor='n')

ttk.Label(card_cari, text='Cari Data Peserta', style='Header.TLabel').pack(pady=(6,8))
entry_cari = ttk.Entry(card_cari, width=40)
entry_cari.pack(pady=4)
btn_cari_exec = ttk.Button(card_cari, text='Cari', command=cari_data)
btn_cari_exec.pack(pady=6)

cols = ("Nama", "Kelas", "Mean")

tree_cari = ttk.Treeview(halaman_cari_data, columns=cols, show='headings', height=15)
for c in cols:
    tree_cari.heading(c, text=c)
    tree_cari.column(c, width=200, anchor='center')

tree_cari.place(relx=0.5, rely=0.28, anchor='n')

btn_back_from_cari = ttk.Button(halaman_cari_data, text='Kembali', command=lambda: switch_frame(halaman_dashboard))
btn_back_from_cari.place(relx=0.5, rely=0.88, anchor='s')

# ---------- LIHAT DATA ----------
cols_all = ("No", "Nama", "Kelas", "Mean")

tree = ttk.Treeview(halaman_nampilin_data, columns=cols_all, show='headings', height=18)
for c in cols_all:
    tree.heading(c, text=c, command=lambda col=c: sort_treeview(tree, col, False))
    tree.column(c, width=220, anchor='center')

tree.pack(fill='both', expand=True, padx=20, pady=10)

btn_back_view = ttk.Button(halaman_nampilin_data, text='Kembali', command=lambda: switch_frame(halaman_dashboard))
btn_back_view.pack(pady=6)

# start
switch_frame(halaman_login)
root.mainloop()
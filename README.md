# Aplikasi Data Peserta Didik A1

**Deskripsi Singkat**
Aplikasi desktop berbasis **Python** dengan **Tkinter** untuk mengelola data peserta didik. Aplikasi ini memungkinkan pengguna untuk **login**, **membuat akun baru**, **menginput nama, kelas, dan nilai mapel**, serta **melihat dan mencari data peserta didik** dengan mudah.

**Fitur Utama**

* Sistem **Login dan Signup** dengan validasi username dan password.
* **Dashboard interaktif** dengan akses ke fitur utama: input data, lihat semua data, dan cari data.
* Input **nama, kelas, nilai mapel wajib, dan nilai mapil** dengan tampilan yang rapi dan scrollable.
* **Perhitungan rata-rata nilai (mean)** secara otomatis berdasarkan data yang diinput.
* **Fitur pencarian** data peserta berdasarkan nama dengan tampilan hasil yang jelas.
* **Sortir data** berdasarkan kolom di tampilan semua data menggunakan **natural sorting**.
* Navigasi mudah antara halaman menggunakan tombol dan **frame switching**.

**Teknologi**

* **Python 3**
* **Tkinter** untuk GUI
* **ttk** untuk komponen interface modern
* **natsort** untuk sorting data secara alami

**Struktur Repo**

* `main.py` – File utama berisi seluruh kode aplikasi.

**Cara Menjalankan**

1. Pastikan Python 3.x sudah terinstall.
2. Install library yang dibutuhkan:

   ```bash
   pip install natsort
   ```
3. Jalankan aplikasi:

   ```bash
   python main.py
   ```

# ⏱️ Time Studio

Aplikasi **Timer** dan **Stopwatch** sederhana dengan tampilan gelap (dark mode) modern, dibuat menggunakan Python dan [Kivy](https://kivy.org/). Antarmuka berbahasa Indonesia, dengan tombol-tombol rounded berwarna dan transisi geser antar layar.

## ✨ Fitur

### Menu Utama
- Navigasi ke mode **Timer** atau **Stopwatch**
- Transisi slide antar layar

### Timer (Hitung Mundur)
- Input waktu dalam format **Jam : Menit : Detik** (JJ / MM / DD)
- Tombol **MULAI**, **JEDA**, dan **RESET**
- Tampilan sisa waktu `HH:MM:SS` yang diperbarui setiap detik
- Pesan status (berjalan, dijeda, waktu habis, validasi input kosong)
- Timer otomatis dijeda saat kembali ke menu

### Stopwatch
- Tampilan waktu dengan ketelitian 0,1 detik (`HH:MM:SS.d`)
- Tombol **MULAI**, **LAP**, dan **RESET**
- **Riwayat Lap** yang dapat di-scroll
- Stopwatch otomatis dihentikan saat kembali ke menu

## 📸 Tampilan

Tema warna yang digunakan:

| Elemen | Warna |
|---|---|
| Background | Biru gelap `#121724` |
| Kartu | Biru keabuan `#1F2638` |
| Aksen | Cyan, Ungu, Pink, Hijau |

> Tambahkan screenshot aplikasi di sini, misalnya `docs/screenshot-menu.png`.

## 🧰 Kebutuhan

- Python 3.8 atau lebih baru
- [Kivy](https://pypi.org/project/Kivy/)

## 🚀 Instalasi

1. Clone atau unduh proyek ini.
2. (Opsional) Buat virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

3. Pasang dependensi:

   ```bash
   pip install kivy
   ```

## ▶️ Menjalankan Aplikasi

```bash
python main.py
```

> Ganti `main.py` dengan nama file script Anda.

## 🕹️ Cara Penggunaan

### Timer
1. Dari menu utama, tekan **TIMER**.
2. Isi kolom **JJ** (jam), **MM** (menit), dan **DD** (detik). Kolom yang dikosongkan dianggap `0`.
3. Tekan **MULAI** untuk memulai hitung mundur.
4. Tekan **JEDA** untuk menghentikan sementara, lalu **MULAI** lagi untuk melanjutkan.
5. Tekan **RESET** untuk mengosongkan input dan mengembalikan timer ke `00:00:00`.
6. Tekan tombol **X** untuk kembali ke menu.

### Stopwatch
1. Dari menu utama, tekan **STOPWATCH**.
2. Tekan **MULAI** untuk menjalankan stopwatch.
3. Tekan **LAP** saat berjalan untuk mencatat waktu lap.
4. Tekan **RESET** untuk menghentikan stopwatch dan menghapus semua riwayat lap.
5. Tekan tombol **X** untuk kembali ke menu.

## 🗂️ Struktur Kode

| Komponen | Deskripsi |
|---|---|
| `RoundedButton` (KV) | Template tombol rounded dengan warna normal dan saat ditekan |
| `ColoredCard` | `BoxLayout` dengan background rounded rectangle berwarna |
| `make_button()` | Helper untuk membuat tombol dengan warna kustom |
| `MenuScreen` | Layar menu utama |
| `TimerScreen` | Layar timer hitung mundur (update tiap 1 detik) |
| `StopwatchScreen` | Layar stopwatch dengan fitur lap (update tiap 0,1 detik) |
| `TimeStudioApp` | Kelas utama aplikasi dan pengatur `ScreenManager` |

## 🎨 Kustomisasi

Warna tema dapat diubah dengan mudah pada konstanta di bagian atas file:

```python
BG_DARK       = (0.07, 0.09, 0.14, 1)
CARD_BG       = (0.12, 0.15, 0.22, 1)
ACCENT_CYAN   = (0.15, 0.85, 0.85, 1)
ACCENT_PURPLE = (0.55, 0.35, 0.95, 1)
ACCENT_PINK   = (0.95, 0.30, 0.55, 1)
ACCENT_GREEN  = (0.25, 0.85, 0.45, 1)
```

## 📝 Catatan & Batasan Saat Ini

- Stopwatch belum memiliki tombol **jeda** terpisah (hanya Mulai, Lap, Reset).
- Timer belum memiliki notifikasi suara atau getar saat waktu habis; hanya pesan teks "Waktu habis!".
- Stopwatch menghitung waktu dengan menjumlahkan interval `Clock`, sehingga bisa terjadi sedikit selisih (drift) pada pemakaian yang sangat lama.

## 💡 Ide Pengembangan

- Tombol jeda/lanjut pada stopwatch
- Alarm suara saat timer selesai
- Preset timer (misalnya 5, 10, 25 menit untuk Pomodoro)
- Ekspor riwayat lap
- Build ke Android dengan [Buildozer](https://buildozer.readthedocs.io/)

## 📄 Lisensi

Tentukan lisensi proyek Anda di sini (misalnya MIT).

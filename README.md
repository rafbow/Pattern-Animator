# 🎨 Pattern Animator

**Tugas Ujian Mid Semester – Python Interactive Animation**

Program **Pattern Animator** adalah aplikasi terminal berbasis Python yang menampilkan animasi berbagai pola (pattern) bergerak secara horizontal. Pengguna dapat mengontrol kecepatan, mengganti pola, mengatur jarak gerakan, menampilkan statistik, serta melakukan pause/resume secara real-time.

---

## ✨ Fitur Utama

* 10 jenis pattern animasi (Simple, Wave, Pulse, Random, Alternate, Arrow, Box Rotate, Fibonacci, Fractal)
* Pergerakan bolak-balik dengan jarak dinamis
* Kecepatan animasi dapat diatur
* Statistik real-time: waktu berjalan, jumlah bouncing, kecepatan, range, dan nama pattern
* Preview pattern sebelum animasi
* Sistem input non-blocking (real-time)
* Menu interaktif + help screen

---

## 🎮 Kontrol Keyboard

| Tombol    | Fungsi                          |
| --------- | ------------------------------- |
| **W / ↑** | Percepat animasi                |
| **S / ↓** | Perlambat animasi               |
| **D / →** | Pattern berikutnya              |
| **A / ←** | Pattern sebelumnya              |
| **R**     | Random pattern                  |
| **+ / =** | Tambah jarak gerakan            |
| **- / _** | Kurangi jarak gerakan           |
| **Space** | Pause / Resume                  |
| **I**     | Tampilkan/sembunyikan statistik |
| **H / ?** | Help Menu                       |
| **Q**     | Keluar                          |

---

## 🚀 Cara Menjalankan Program

Pastikan Python 3.8+ sudah terinstall.

```bash
python pattern_animator.py
```

---

## 📂 Struktur Program

* `PatternGenerator` → menghasilkan berbagai jenis pattern
* `AnimationController` → logika utama animasi
* `input_thread()` → membaca input keyboard tanpa mengganggu animasi
* Menu interaktif → preview, petunjuk, dan start animasi

---

## 📝 Deskripsi Singkat

Program Pattern Animator menampilkan animasi pola bergerak secara interaktif di terminal. Pengguna dapat mengubah pattern, kecepatan, jarak gerakan, pause/resume, dan melihat statistik real-time. Termasuk menu, preview pattern, dan kontrol penuh. **Tugas ujian mid semester.**

---

## 📜 Lisensi

Proyek ini dibuat untuk **tugas ujian mid semester** dan bebas dimodifikasi sesuai kebutuhan pembelajaran.


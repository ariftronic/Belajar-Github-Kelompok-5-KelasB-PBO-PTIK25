# Kebun Binatang — Refactoring dengan Prinsip SOLID

> **Mata Kuliah :** Pemrograman Berorientasi Objek  
> **Tugas       :** Latihan Analisis & Implementasi Prinsip SOLID  
> **Bahasa      :** Python 3  

---

## 👥 Anggota Kelompok

| No | Nama | Role | File Tanggung Jawab | Branch |
|----|------|------|---------------------|--------|
| 1 | **Danang** | Core Architect | `base_hewan.py` | `feature/base-hewan` |
| 2 | **Awang** | Implementator | `hewan.py` | `feature/hewan` |
| 3 | **Dika** | Environment Manager | `manajemen.py` | `feature/manajemen` |
| 4 | **Arif** | Git Master | `main.py` | `feature/main` |
| 5 | **Afrizal** | System Analyst | `README.md` | `feature/readme` |

---

## 📋 Deskripsi Proyek

Proyek ini merupakan implementasi refactoring sistem manajemen kebun binatang sederhana menggunakan Python. Kode awal yang diberikan melanggar 4 dari 5 prinsip SOLID — kemudian dianalisis dan diperbaiki oleh kelompok secara kolaboratif melalui GitHub.

Setiap anggota bertanggung jawab atas **satu file terpisah** sehingga tidak terjadi merge conflict selama proses kolaborasi.

---

## 📁 Struktur Proyek
kebun-binatang-solid/

base_hewan.py ← Danang : ABC Hewan, interface BisaMakan & BisaTerbang (ISP + LSP)

hewan.py ← Awang : Kelas konkret Burung, Kucing, Ikan (OCP + LSP)

manajemen.py ← Dika : Kelas Kandang & KebunBinatang (DIP + OCP)

main.py ← Arif : Entry point & integrasi semua modul

README.md ← Afrizal : Dokumentasi proyek


## 🚀 Cara Menjalankan

**Persyaratan:** Python 3.7 atau lebih baru (tidak ada library tambahan)

```bash
# 1. Clone repository ini
git clone https://github.com/<username>/kebun-binatang-solid.git

# 2. Masuk ke folder project
cd kebun-binatang-solid

# 3. Jalankan simulasi
python main.py
```
---

## 🔴 Analisis Kode Awal — Masalah yang Ditemukan

Kode awal terdiri dari tiga kelas: `Hewan`, `Kandang`, dan `KebunBinatang`. Setelah dianalisis, ditemukan **4 pelanggaran** prinsip SOLID:

### ❌ O — Open/Closed Principle

```python
# KODE LAMA — harus diubah setiap ada hewan baru
class KebunBinatang:
    def rawat_semua_hewan(self):
        for hewan in self.kandang.hewan_list:
            hewan.makan()
            hewan.terbang()  # ← hardcode, apa jadinya jika ada ikan?
```

`rawat_semua_hewan()` memanggil `terbang()` secara hardcode untuk **semua** hewan. Setiap kali ada jenis hewan baru, method ini **harus dimodifikasi** — melanggar prinsip "tertutup untuk modifikasi".

---

### ❌ L — Liskov Substitution Principle

```python
# KODE LAMA — kontrak superclass tidak bisa dipenuhi subclass
class Hewan:
    def terbang(self):
        print(f"{self.nama} sedang terbang.")

# Kucing mewarisi terbang() padahal kucing tidak bisa terbang
# → melanggar LSP
```

Jika `Kucing` mewarisi `Hewan`, ia "mewarisi" kemampuan terbang yang tidak dimilikinya. Ini melanggar kontrak superclass dan merusak logika program saat substitusi dilakukan.

---

### ❌ I — Interface Segregation Principle

```python
# KODE LAMA — interface gemuk, memaksa semua hewan punya terbang()
class Hewan:
    def makan(self): ...
    def terbang(self): ...  # ← dipaksakan ke semua subclass
```

`Hewan` bertindak sebagai satu interface besar. Subkelas seperti `Kucing` atau `Ikan` terpaksa mewarisi `terbang()` meski tidak relevan sama sekali.

---

### ❌ D — Dependency Inversion Principle

```python
# KODE LAMA — hard dependency pada kelas konkret
class KebunBinatang:
    def __init__(self):
        self.kandang = Kandang()  # ← membuat sendiri, tidak bisa diganti
```

`KebunBinatang` membuat objek `Kandang` secara langsung di dalam konstruktornya. Ini menyebabkan *tight coupling* — sulit diuji secara terisolasi dan sulit diganti implementasinya.

---

### ✅ S — Single Responsibility Principle (Sudah Terpenuhi)

Kelas `Hewan`, `Kandang`, dan `KebunBinatang` di kode awal sudah memiliki tanggung jawab yang terpisah — masing-masing berfokus pada satu domain. Prinsip ini **tidak dilanggar**.

---

## 🟢 Solusi — Struktur Multi-File yang Memenuhi SOLID

### `base_hewan.py` → Memperbaiki ISP & LSP *(Afrizal)*

Interface dipecah menjadi tiga bagian terpisah:

```python
class Hewan(ABC):       # kontrak identitas dasar
class BisaMakan(ABC):   # interface terisolasi: kemampuan makan
class BisaTerbang(ABC): # interface terisolasi: kemampuan terbang
```

- **ISP ✅** — Kelas hanya wajib mengimplementasikan interface yang benar-benar dimilikinya.  
- **LSP ✅** — Tidak ada kontrak yang dilanggar karena setiap subkelas hanya berjanji atas kemampuan nyatanya.

---

### `hewan.py` → Memperkuat OCP & LSP *(Awang)*

```python
class Burung(Hewan, BisaMakan, BisaTerbang): ...  # bisa makan & terbang
class Kucing(Hewan, BisaMakan): ...               # hanya bisa makan
class Ikan(Hewan, BisaMakan): ...                 # ditambah TANPA ubah file lain
```

- **OCP ✅** — Tambah hewan baru = buat kelas baru di file ini. `manajemen.py` dan `main.py` tidak perlu disentuh.  
- **LSP ✅** — `Kucing` tidak punya method `terbang()` sama sekali — bukan kosong, tapi memang tidak ada.

---

### `manajemen.py` → Memperbaiki DIP & OCP *(Dika)*

```python
class KebunBinatang:
    def __init__(self, kandang: Kandang) -> None:
        self.kandang = kandang  # ← Dependency Injection, tidak buat sendiri

    def rawat_semua_hewan(self):
        for hewan in self.kandang.hewan_list:
            if isinstance(hewan, BisaMakan):   # polimorfisme
                hewan.makan()
            if isinstance(hewan, BisaTerbang): # dipanggil hanya jika relevan
                hewan.terbang()
```

- **DIP ✅** — `KebunBinatang` menerima `Kandang` dari luar (Dependency Injection), bukan membuatnya sendiri.  
- **OCP ✅** — `rawat_semua_hewan()` tidak perlu diubah saat ada hewan baru dengan kemampuan baru.

---

### `main.py` → Integrasi & Demo *(Arif)*

Menyatukan semua modul dan membuktikan bahwa sistem berjalan dengan benar, termasuk **demo OCP** (menambah `Elang` tanpa mengubah `manajemen.py`).

---

## 📊 Ringkasan Pemenuhan Prinsip SOLID

| Prinsip | Kode Awal | Kode Refactor | File Kunci |
|---------|:---------:|:-------------:|------------|
| **S** — Single Responsibility | ✅ | ✅ | Semua file |
| **O** — Open/Closed | ❌ | ✅ | `hewan.py`, `manajemen.py` |
| **L** — Liskov Substitution | ❌ | ✅ | `base_hewan.py`, `hewan.py` |
| **I** — Interface Segregation | ❌ | ✅ | `base_hewan.py` |
| **D** — Dependency Inversion | ❌ | ✅ | `manajemen.py` |

---

## 🌿 Alur Kerja Git Tim

Setiap anggota bekerja pada **file yang berbeda** di branch terpisah, sehingga tidak terjadi merge conflict.

**Langkah kolaborasi:**

```bash
# Tiap anggota clone repo dan buat branch sendiri
git clone https://github.com/<username>/kebun-binatang-solid.git
cd kebun-binatang-solid
git checkout -b feature/nama-branch

# Kerjakan file masing-masing, lalu commit dan push
git add nama_file.py
git commit -m "Tambah implementasi [nama prinsip]"
git push origin feature/nama-branch

# Buat Pull Request di GitHub → review → merge ke main
```

---

## 📐 Diagram Dependensi Modul

main.py
didalamnya : 
hewan.py
base_hewan.py
manajemen.py
base_hewan.py

`base_hewan.py` adalah fondasi sistem — semua modul bergantung padanya. Tidak ada dependensi melingkar (circular dependency).

---

*Dibuat sebagai bagian dari tugas kolaborasi tim — Mata Kuliah Pemrograman Berorientasi Objek.*


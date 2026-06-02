# 🦁 Refactor Kebun Binatang — Analisis Prinsip SOLID

> **Tugas   :** Danang — System Analyst  
> **Proyek  :** Latihan Kolaborasi Tim & Analisis Prinsip SOLID  
> **Kursus  :** Pemrograman Berorientasi Objek

---

## 📁 Struktur File Proyek

```
kebun_binatang/
├── base_hewan.py   ← Afrizal  (Core Architect)
├── hewan.py        ← Awang    (Implementator)
├── manajemen.py    ← Dika     (Environment Manager)
├── main.py         ← Arif     (Git Master)
└── README.md       ← Danang   (System Analyst)
```

---

## 🔴 Bagian 1 — Analisis Kode Awal yang Bermasalah

Kode awal yang terdiri dari tiga kelas (`Hewan`, `Kandang`, `KebunBinatang`) melanggar **empat dari lima** prinsip SOLID. Berikut analisis per prinsip.

---

### 1. OCP — Open/Closed Principle ❌

> *"Kelas harus terbuka untuk ekstensi, tetapi tertutup untuk modifikasi."*

**Kode awal bermasalah:**

```python
class KebunBinatang:
    def rawat_semua_hewan(self):
        for hewan in self.kandang.hewan_list:
            hewan.makan()
            hewan.terbang()   # ← dipanggil keras di sini
```

**Mengapa melanggar OCP?**  
Method `rawat_semua_hewan()` memanggil `makan()` dan `terbang()` secara **hardcode** untuk setiap hewan. Jika di masa depan kita ingin menambahkan hewan yang bisa berenang (`berenang()`), kita **harus mengubah** method ini. Artinya kelas tidak "tertutup untuk modifikasi."

---

### 2. LSP — Liskov Substitution Principle ❌

> *"Objek subkelas harus bisa menggantikan objek superclass-nya tanpa mengubah kebenaran program."*

**Kode awal bermasalah:**

```python
class Hewan:
    def terbang(self):
        print(f"{self.nama} sedang terbang.")
```

**Mengapa melanggar LSP?**  
Kelas `Hewan` mendefinisikan `terbang()` seolah-olah **semua** hewan bisa terbang. Padahal seekor `Kucing` yang mewarisi `Hewan` **tidak bisa terbang** secara logis. Jika `Kucing` dipaksa mewarisi method ini, ada dua kemungkinan buruk: (a) method terbang() berjalan namun outputnya tidak masuk akal, atau (b) subkelas harus meng-override dengan `raise NotImplementedError`, yang justru merusak substitusi. Kontrak superclass tidak dapat dipenuhi oleh subkelas secara jujur.

---

### 3. ISP — Interface Segregation Principle ❌

> *"Kelas tidak boleh dipaksa bergantung pada interface yang tidak digunakannya."*

**Kode awal bermasalah:**

```python
class Hewan:
    def makan(self):  ...
    def terbang(self): ...   # ← satu "interface" gemuk
```

**Mengapa melanggar ISP?**  
`Hewan` bertindak sebagai satu interface besar yang menggabungkan kemampuan `makan` dan `terbang` sekaligus. Subkelas seperti `Kucing` atau `Ikan` terpaksa mewarisi `terbang()` meski tidak relevan. Interface seharusnya dipecah berdasarkan kapabilitas spesifik agar setiap kelas hanya mengimplementasikan apa yang memang dimilikinya.

---

### 4. DIP — Dependency Inversion Principle ❌

> *"Modul tingkat tinggi tidak boleh bergantung pada modul tingkat rendah. Keduanya harus bergantung pada abstraksi."*

**Kode awal bermasalah:**

```python
class KebunBinatang:
    def __init__(self):
        self.kandang = Kandang()   # ← instansiasi langsung di dalam!
```

**Mengapa melanggar DIP?**  
`KebunBinatang` (modul tingkat tinggi) secara **langsung membuat** objek `Kandang` (modul tingkat rendah) di dalam konstruktornya. Ini membuat keduanya tightly coupled. Jika kita ingin mengganti `Kandang` dengan `KandangPremium` atau menguji `KebunBinatang` secara terisolasi (unit test), kita tidak bisa melakukannya tanpa mengubah kode `KebunBinatang`.

---

### ✅ Prinsip yang Sudah Terpenuhi di Kode Awal

| Prinsip | Status | Keterangan |
|---------|--------|------------|
| **SRP** (Single Responsibility) | ✅ Terpenuhi | `Hewan`, `Kandang`, dan `KebunBinatang` masing-masing memiliki tanggung jawab yang berbeda dan terpisah. |

---

## 🟢 Bagian 2 — Solusi: Struktur Multi-File yang Memenuhi SOLID

Berikut penjelasan bagaimana setiap file baru menyelesaikan pelanggaran di atas.

---

### `base_hewan.py` → Memperbaiki ISP & LSP

```python
class Hewan(ABC): ...       # Kontrak identitas dasar
class BisaMakan(ABC): ...   # Interface terisolasi: hanya kemampuan makan
class BisaTerbang(ABC): ... # Interface terisolasi: hanya kemampuan terbang
```

- **ISP ✅** — Interface dipecah menjadi `BisaMakan` dan `BisaTerbang`. Setiap kelas hanya mewarisi interface yang relevan dengan kemampuan nyatanya.  
- **LSP ✅** — `Kucing` yang mewarisi `BisaMakan` tidak pernah "tahu" tentang `terbang()`. Tidak ada kontrak yang dilanggar. Setiap subkelas dapat menggantikan superclass-nya dengan aman.

---

### `hewan.py` → Memperkuat LSP & OCP

```python
class Burung(Hewan, BisaMakan, BisaTerbang): ...  # Bisa makan & terbang
class Kucing(Hewan, BisaMakan): ...               # Hanya bisa makan
class Ikan(Hewan, BisaMakan): ...                 # Tambahan baru, tanpa ubah file lain
```

- **LSP ✅** — `Kucing` tidak memiliki method `terbang()` sama sekali, bukan method kosong. Tidak ada kebohongan pada kontrak.  
- **OCP ✅** — Menambah `Ikan` atau hewan baru lainnya cukup dilakukan di file ini. File `manajemen.py` dan `main.py` **tidak perlu diubah**.

---

### `manajemen.py` → Memperbaiki DIP & OCP

```python
class KebunBinatang:
    def __init__(self, kandang: Kandang) -> None:  # ← Dependency Injection
        self.kandang = kandang

    def rawat_semua_hewan(self):
        for hewan in self.kandang.hewan_list:
            if isinstance(hewan, BisaMakan):    # ← Polimorfisme
                hewan.makan()
            if isinstance(hewan, BisaTerbang):  # ← OCP
                hewan.terbang()
```

- **DIP ✅** — `KebunBinatang` tidak lagi membuat `Kandang` sendiri. Objek `Kandang` diinjeksikan dari luar (Dependency Injection), membuat keduanya loosely coupled dan mudah diuji secara terisolasi.  
- **OCP ✅** — `rawat_semua_hewan()` menggunakan `isinstance()` untuk memanggil aksi hanya jika hewan memiliki kemampuan tersebut. Menambah hewan baru dengan kemampuan baru tidak memerlukan perubahan pada method ini.

---

### `main.py` → Integrasi Bersih

```python
kandang = Kandang(nama_kandang="Kandang Utama")
# ... tambah hewan ...
kebun = KebunBinatang(kandang=kandang)   # Injeksi dari luar
kebun.rawat_semua_hewan()
```

File ini membuktikan bahwa semua komponen dapat dirakit dengan rapi tanpa ada ketergantungan tersembunyi.

---

## 📊 Ringkasan Pemenuhan Prinsip SOLID

| Prinsip | Kode Awal | Kode Baru | File Kunci |
|---------|:---------:|:---------:|------------|
| **S** — Single Responsibility | ✅ | ✅ | Semua file |
| **O** — Open/Closed | ❌ | ✅ | `manajemen.py`, `hewan.py` |
| **L** — Liskov Substitution | ❌ | ✅ | `base_hewan.py`, `hewan.py` |
| **I** — Interface Segregation | ❌ | ✅ | `base_hewan.py` |
| **D** — Dependency Inversion | ❌ | ✅ | `manajemen.py` |

---

## 🚀 Cara Menjalankan

```bash
# Clone repository
git clone https://github.com/<username>/kebun-binatang-solid.git
cd kebun-binatang-solid

# Jalankan simulasi (tidak perlu install library tambahan)
python main.py
```

---

## 🌿 Alur Kerja Git Tim

```
main
├── feature/base-hewan   → Afrizal  → base_hewan.py
├── feature/hewan        → Awang    → hewan.py
├── feature/manajemen    → Dika     → manajemen.py
├── feature/main         → Arif     → main.py
└── feature/readme       → Danang   → README.md
```

Karena setiap anggota tim bekerja pada **file yang berbeda**, tidak akan terjadi **merge conflict** saat semua branch digabungkan ke `main`.

---

*Dokumen ini dibuat sebagai bagian dari tugas kolaborasi tim — Mata Kuliah Pemrograman Berorientasi Objek.*


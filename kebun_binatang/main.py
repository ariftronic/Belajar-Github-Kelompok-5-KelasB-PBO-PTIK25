"""
main.py
=======
Tugas  : Arif — Git Master
Deskripsi: Skrip utama yang mengimpor semua modul dan menjalankan
           simulasi kebun binatang dari awal hingga akhir.

Cara menjalankan:
    $ python main.py

Catatan untuk Git Master (Arif):
    - Pastikan semua branch sudah di-merge ke 'main' sebelum menjalankan.
    - Struktur direktori yang diharapkan:
        kebun_binatang/
        ├── base_hewan.py    ← branch: feature/base-hewan   (Afrizal)
        ├── hewan.py         ← branch: feature/hewan        (Awang)
        ├── manajemen.py     ← branch: feature/manajemen    (Dika)
        ├── main.py          ← branch: feature/main         (Arif)
        └── README.md        ← branch: feature/readme       (Danang)
"""

# ---------------------------------------------------------------------------
# Import modul dari anggota tim
# ---------------------------------------------------------------------------
from hewan import Burung, Ikan, Kucing           # Modul Awang
from manajemen import KebunBinatang, Kandang     # Modul Dika


# ---------------------------------------------------------------------------
# Fungsi utama
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 50)
    print("  SIMULASI KEBUN BINATANG — Refactor SOLID")
    print("=" * 50)

    # -----------------------------------------------------------------------
    # 1. Buat kandang (objek mandiri — siap diinjeksikan)
    # -----------------------------------------------------------------------
    kandang_utama = Kandang(nama_kandang="Kandang Utama")

    # -----------------------------------------------------------------------
    # 2. Buat hewan-hewan
    # -----------------------------------------------------------------------
    burung_1 = Burung(nama="Cici")
    burung_2 = Burung(nama="Rio")
    kucing_1 = Kucing(nama="Mochi")
    ikan_1   = Ikan(nama="Nemo")

    # -----------------------------------------------------------------------
    # 3. Masukkan hewan ke kandang
    # -----------------------------------------------------------------------
    print("\n--- Mengisi Kandang ---")
    kandang_utama.tambah_hewan(burung_1)
    kandang_utama.tambah_hewan(burung_2)
    kandang_utama.tambah_hewan(kucing_1)
    kandang_utama.tambah_hewan(ikan_1)

    # -----------------------------------------------------------------------
    # 4. Buat KebunBinatang dengan Dependency Injection
    #    (kandang diinjeksikan dari luar — DIP)
    # -----------------------------------------------------------------------
    kebun = KebunBinatang(kandang=kandang_utama)

    # -----------------------------------------------------------------------
    # 5. Jalankan simulasi perawatan
    # -----------------------------------------------------------------------
    kebun.rawat_semua_hewan()

    # -----------------------------------------------------------------------
    # 6. Bersihkan kandang
    # -----------------------------------------------------------------------
    print("--- Membersihkan Kandang ---")
    kebun.bersihkan_semua_kandang()

    # -----------------------------------------------------------------------
    # 7. Demo OCP: tambah hewan baru TANPA ubah kode manajemen.py
    # -----------------------------------------------------------------------
    print("\n--- Demo OCP: Menambah Elang Tanpa Mengubah manajemen.py ---")

    # Impor Burung lagi sebagai pengganti Elang untuk demo sederhana
    elang = Burung(nama="Elang Jawa")
    kandang_utama.tambah_hewan(elang)
    kebun.rawat_semua_hewan()

    print("Simulasi selesai. ✅")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()

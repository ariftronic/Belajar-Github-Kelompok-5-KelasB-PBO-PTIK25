"""
manajemen.py
============
Tugas  : Dika — Environment Manager
Prinsip: DIP (Dependency Inversion Principle) & OCP (Open/Closed Principle)

Modul ini mendefinisikan kelas Kandang dan KebunBinatang.

DIP  → KebunBinatang tidak lagi membuat instansi Kandang secara langsung
       di dalam __init__().  Objek Kandang diinjeksikan dari luar (Dependency
       Injection) sehingga KebunBinatang bergantung pada abstraksi,
       bukan pada implementasi konkret.

OCP  → rawat_semua_hewan() menggunakan polimorfisme: ia hanya memanggil
       makan() pada setiap hewan, dan terbang() hanya jika hewan
       mengimplementasikan BisaTerbang.  Menambah jenis hewan baru tidak
       memerlukan perubahan pada method ini.
"""

from typing import List

from base_hewan import BisaMakan, BisaTerbang, Hewan


# ---------------------------------------------------------------------------
# Kandang
# ---------------------------------------------------------------------------
class Kandang:
    """
    Manajemen kumpulan hewan dalam satu kandang.

    Bertanggung jawab menyimpan daftar hewan dan operasi kandang
    (bersihkan, tambah hewan, dsb.).
    """

    def __init__(self, nama_kandang: str = "Kandang Utama") -> None:
        self.nama_kandang = nama_kandang
        self._hewan_list: List[Hewan] = []

    # -- Akses read-only ke daftar hewan ------------------------------------
    @property
    def hewan_list(self) -> List[Hewan]:
        """Kembalikan salinan list hewan agar tidak bisa dimodifikasi langsung."""
        return list(self._hewan_list)

    # -- Operasi kandang ----------------------------------------------------
    def tambah_hewan(self, hewan: Hewan) -> None:
        """Tambahkan satu hewan ke kandang."""
        if not isinstance(hewan, Hewan):
            raise TypeError(f"Objek '{hewan}' bukan turunan dari Hewan.")
        self._hewan_list.append(hewan)
        print(f"[KANDANG] {hewan} berhasil dimasukkan ke {self.nama_kandang}.")

    def bersihkan_kandang(self) -> None:
        """Simulasikan pembersihan kandang."""
        print(f"[KANDANG] {self.nama_kandang} sedang dibersihkan oleh petugas. 🧹")

    def jumlah_hewan(self) -> int:
        """Kembalikan jumlah hewan yang ada di kandang."""
        return len(self._hewan_list)

    def __str__(self) -> str:
        return f"{self.nama_kandang} ({self.jumlah_hewan()} hewan)"


# ---------------------------------------------------------------------------
# KebunBinatang  ←  Dependency Injection diterapkan di sini
# ---------------------------------------------------------------------------
class KebunBinatang:
    """
    Manajemen kebun binatang secara keseluruhan.

    Perubahan utama dari kode awal:
    - Kandang DIINJEKSIKAN lewat parameter __init__, bukan dibuat di dalam.
      Ini adalah penerapan Dependency Injection (DIP).
    - rawat_semua_hewan() menggunakan isinstance() untuk memanggil terbang()
      hanya pada hewan yang benar-benar bisa terbang (OCP + polimorfisme).
    """

    def __init__(self, kandang: Kandang) -> None:
        # Menerima kandang dari luar — bukan membuat sendiri (DIP)
        if not isinstance(kandang, Kandang):
            raise TypeError("Parameter 'kandang' harus merupakan instansi Kandang.")
        self.kandang = kandang

    def rawat_semua_hewan(self) -> None:
        """
        Iterasi semua hewan di kandang dan jalankan aksi yang sesuai.

        OCP  → Method ini tidak perlu diubah saat hewan baru ditambahkan.
        Polimorfisme → makan() dipanggil via interface BisaMakan;
                       terbang() hanya dipanggil jika hewan mengimplementasikan
                       BisaTerbang.
        """
        print(f"\n{'='*50}")
        print(f"  Merawat semua hewan di {self.kandang}")
        print(f"{'='*50}")

        if self.kandang.jumlah_hewan() == 0:
            print("  (Belum ada hewan di kandang.)")
            return

        for hewan in self.kandang.hewan_list:
            print(f"\n  >> {hewan}")

            # Panggil makan() hanya jika hewan mengimplementasikan BisaMakan
            if isinstance(hewan, BisaMakan):
                hewan.makan()

            # Panggil terbang() hanya jika hewan mengimplementasikan BisaTerbang
            if isinstance(hewan, BisaTerbang):
                hewan.terbang()

        print(f"\n{'='*50}\n")

    def bersihkan_semua_kandang(self) -> None:
        """Perintahkan pembersihan kandang."""
        self.kandang.bersihkan_kandang()

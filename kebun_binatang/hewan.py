"""
hewan.py
========
Tugas  : Awang — Implementator
Prinsip: LSP (Liskov Substitution Principle) & OCP (Open/Closed Principle)

Modul ini mengimplementasikan kelas-kelas hewan konkret dengan mengimpor
kontrak dari base_hewan.py.

LSP → Burung dan Kucing dapat digunakan di mana pun objek Hewan dibutuhkan
      tanpa merusak logika program.  Kucing TIDAK mewarisi BisaTerbang
      sehingga tidak pernah dipaksa mengimplementasikan terbang().

OCP → Menambah hewan baru (misal: Ikan, Elang) cukup dengan membuat kelas
      baru di modul ini tanpa mengubah kode yang sudah ada di manajemen.py
      atau main.py.
"""

from base_hewan import BisaMakan, BisaTerbang, Hewan


# ---------------------------------------------------------------------------
# Burung — bisa makan DAN terbang
# ---------------------------------------------------------------------------
class Burung(Hewan, BisaMakan, BisaTerbang):
    """
    Representasi burung di kebun binatang.

    Mewarisi Hewan (identitas), BisaMakan, dan BisaTerbang karena burung
    memang memiliki kedua kemampuan tersebut.
    """

    def __init__(self, nama: str) -> None:
        super().__init__(nama=nama, jenis="Burung")

    def makan(self) -> None:
        print(f"[MAKAN]   {self} memakan biji-bijian dengan paruhnya. 🐦")

    def terbang(self) -> None:
        print(f"[TERBANG] {self} mengepakkan sayap dan terbang tinggi. 🕊️")


# ---------------------------------------------------------------------------
# Kucing — hanya bisa makan (tidak mewarisi BisaTerbang)
# ---------------------------------------------------------------------------
class Kucing(Hewan, BisaMakan):
    """
    Representasi kucing di kebun binatang.

    Hanya mewarisi BisaMakan karena kucing tidak bisa terbang.
    Tidak ada method terbang() di sini, sehingga tidak ada implementasi
    kosong / raise NotImplementedError yang melanggar LSP.
    """

    def __init__(self, nama: str) -> None:
        super().__init__(nama=nama, jenis="Kucing")

    def makan(self) -> None:
        print(f"[MAKAN]   {self} memakan ikan dengan lahap. 🐱")


# ---------------------------------------------------------------------------
# Ikan — hanya bisa makan (contoh extensibility / OCP)
# ---------------------------------------------------------------------------
class Ikan(Hewan, BisaMakan):
    """
    Representasi ikan di kebun binatang.

    Kelas ini ditambahkan TANPA menyentuh kode lain (OCP).
    Ikan hanya bisa makan — tidak bisa terbang.
    """

    def __init__(self, nama: str) -> None:
        super().__init__(nama=nama, jenis="Ikan")

    def makan(self) -> None:
        print(f"[MAKAN]   {self} melahap pelet ikan di akuarium. 🐟")


from hewan import Burung, Ikan, Kucing
from manajemen import KebunBinatang, Kandang

def main() -> None:
    print("=" * 50)
    print("  SIMULASI KEBUN BINATANG — Refactor SOLID")
    print("=" * 50)
    
    kandang_utama = Kandang(nama_kandang="Kandang Utama")
    
    burung_1 = Burung(nama="Cici")
    burung_2 = Burung(nama="Rio")
    kucing_1 = Kucing(nama="Mochi")
    ikan_1   = Ikan(nama="Nemo")
    
    print("\n--- Mengisi Kandang ---")
    kandang_utama.tambah_hewan(burung_1)
    kandang_utama.tambah_hewan(burung_2)
    kandang_utama.tambah_hewan(kucing_1)
    kandang_utama.tambah_hewan(ikan_1)
    
    kebun = KebunBinatang(kandang=kandang_utama)
    
    kebun.rawat_semua_hewan()
    
    print("--- Membersihkan Kandang ---")
    kebun.bersihkan_semua_kandang()
    
    print("\n--- Demo OCP: Menambah Elang Tanpa Mengubah manajemen.py ---")
    elang = Burung(nama="Elang Jawa")
    kandang_utama.tambah_hewan(elang)
    kebun.rawat_semua_hewan()
    
    print("Simulasi selesai. ✅")

if __name__ == "__main__":
    main()
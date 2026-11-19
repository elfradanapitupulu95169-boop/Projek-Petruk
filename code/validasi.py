"""Modul validasi input LaporRT."""

KATEGORI = ["Jalan Rusak", "Lampu Jalan", "Saluran Air", "Sampah", "Fasilitas Umum Lain"]
JENIS = ["Laporan", "Aspirasi"]
STATUS = ["Menunggu", "Diproses", "Selesai"]


def validasi_laporan(judul, kategori, lokasi, deskripsi):
    for nama, nilai in (("Judul", judul), ("Kategori", kategori),
                        ("Lokasi", lokasi), ("Deskripsi", deskripsi)):
        if not str(nilai).strip():
            raise ValueError(f"{nama} wajib diisi.")
    if kategori not in KATEGORI:
        raise ValueError("Kategori tidak valid.")
    if len(str(judul)) > 100:
        raise ValueError("Judul maksimal 100 karakter.")


def validasi_akun(username, password):
    if not username.strip() or " " in username:
        raise ValueError("Username wajib diisi dan tanpa spasi.")
    assert len(password) >= 4, "Password minimal 4 karakter."

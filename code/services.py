from datetime import date

from . import Datastorage, validasi
from .modelLaporan import Laporan


def urutkan(data, key=lambda x: x, balik=False):
    if len(data) <= 1:
        return list(data)
    tengah = len(data) // 2
    kiri = urutkan(data[:tengah], key, balik)
    kanan = urutkan(data[tengah:], key, balik)
    hasil, i, j = [], 0, 0
    while i < len(kiri) and j < len(kanan):
        a, b = key(kiri[i]), key(kanan[j])
        ambil_kiri = a >= b if balik else a <= b
        if ambil_kiri:
            hasil.append(kiri[i]); i += 1
        else:
            hasil.append(kanan[j]); j += 1
    return hasil + kiri[i:] + kanan[j:]


def hitung_total(*args):
    return sum(args)


class LaporanService:

    def __init__(self, path_laporan=Datastorage.FILE_LAPORAN, path_user=Datastorage.FILE_USER):
        self.path_laporan = path_laporan
        self.path_user = path_user
        self.laporan = Datastorage.muat_laporan(path_laporan)
        self.users = Datastorage.muat_user(path_user)

    def registrasi(self, username, password):
        validasi.validasi_akun(username, password)
        if any(u["username"] == username for u in self.users):
            raise ValueError("Username sudah dipakai.")
        self.users.append({"username": username, "password": password, "role": "warga"})
        Datastorage.simpan_user(self.users, self.path_user)

    def login(self, username, password):
        for u in self.users:
            if u["username"] == username and u["password"] == password:
                return u["role"]
        raise ValueError("Username atau password salah.")

    def _id_baru(self):
        angka = [int(l.id.split("-")[1]) for l in self.laporan if l.id.startswith("LP-")]
        return f"LP-{(max(angka) if angka else 0) + 1:03d}"

    def kirim(self, pelapor, jenis, judul, kategori, lokasi, deskripsi):
        """Memvalidasi lalu menyimpan laporan baru dengan status 'Menunggu'."""
        validasi.validasi_laporan(judul, kategori, lokasi, deskripsi)
        lap = Laporan(self._id_baru(), pelapor, jenis, judul.strip(), kategori,
                      lokasi.strip(), deskripsi.strip(), date.today().isoformat())
        self.laporan.append(lap)
        Datastorage.tambah_baris(lap, self.path_laporan)
        return lap

    def ubah_status(self, id_laporan, status, catatan=""):
        if status not in validasi.STATUS:
            raise ValueError("Status tidak valid.")
        lap = self.cari_id(id_laporan)
        lap.status, lap.catatan = status, catatan.strip()
        Datastorage.simpan_laporan(self.laporan, self.path_laporan)

    def cari_id(self, id_laporan):
        for l in self.laporan:
            if l.id == id_laporan:
                return l
        raise ValueError(f"Laporan {id_laporan} tidak ditemukan.")

    def cari(self, kata="", data=None, **filter):
        kata = kata.lower().strip()
        hasil = []
        for l in (self.laporan if data is None else data):
            teks = f"{l.id} {l.judul} {l.lokasi} {l.deskripsi}".lower()
            if kata in teks and all(getattr(l, k) == v for k, v in filter.items() if v):
                hasil.append(l)
        return hasil

    def ringkasan(self, data=None):
        data = self.laporan if data is None else data
        return {s: hitung_total(*[1 for l in data if l.status == s]) for s in validasi.STATUS}

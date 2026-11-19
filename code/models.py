from dataclasses import dataclass


@dataclass
class Laporan:
    """Satu baris data laporan/aspirasi warga."""
    id: str
    pelapor: str
    jenis: str
    judul: str
    kategori: str
    lokasi: str
    deskripsi: str
    tanggal: str
    status: str = "Menunggu"
    catatan: str = ""

    FIELD = ["id", "pelapor", "jenis", "judul", "kategori", "lokasi",
             "deskripsi", "tanggal", "status", "catatan"]

    def to_dict(self):
        """Mengubah objek menjadi dict (untuk disimpan ke CSV)."""
        return {f: getattr(self, f) for f in self.FIELD}

    @classmethod
    def from_dict(cls, d):
        """Membuat objek dari dict hasil baca CSV."""
        return cls(**{f: d[f] for f in cls.FIELD})

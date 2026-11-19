import csv
import os

from .modelLaporan import Laporan

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FILE_LAPORAN = os.path.join(DATA_DIR, "laporan.csv")
FILE_USER = os.path.join(DATA_DIR, "users.csv")
FIELD_USER = ["username", "password", "role"]


def muat_laporan(path=FILE_LAPORAN):
    hasil = []
    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            for baris in csv.DictReader(f):
                try:
                    hasil.append(Laporan.from_dict(baris))
                except (KeyError, TypeError, ValueError):
                    continue  
    except FileNotFoundError:
        pass
    return hasil


def simpan_laporan(daftar, path=FILE_LAPORAN):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=Laporan.FIELD)
        w.writeheader()
        w.writerows(l.to_dict() for l in daftar)


def muat_user(path=FILE_USER):
    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        awal = [{"username": "admin", "password": "admin", "role": "pengurus"}]
        simpan_user(awal, path)
        return awal


def simpan_user(daftar, path=FILE_USER):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELD_USER)
        w.writeheader()
        w.writerows(daftar)


def tambah_baris(laporan, path=FILE_LAPORAN):
    baru = not os.path.exists(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=Laporan.FIELD)
        if baru:
            w.writeheader()
        w.writerow(laporan.to_dict())

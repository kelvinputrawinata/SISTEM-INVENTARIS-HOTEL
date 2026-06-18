from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional
import json

class NotifikasiStok:
    @abstractmethod
    def kirim_peringatan_stok(self, pesan: str):
        pass

class User(ABC):
    def __init__(self, user_id: str, nama: str, email: str, password: str):
        self.user_id = user_id
        self.nama = nama
        self.email = email
        self.password = password
        self.login_status = False
    
    @abstractmethod
    def get_role(self) -> str:
        pass
    
    def login(self, password: str) -> bool:
        if self.password == password:
            self.login_status = True
            return True
        return False
    
    def logout(self):
        self.login_status = False

class AdminGudang(User):
    def __init__(self, user_id: str, nama: str, email: str, password: str, 
                 gudang_lokasi: str):
        super().__init__(user_id, nama, email, password)
        self.gudang_lokasi = gudang_lokasi
        
    def get_role(self) -> str:
        return "Admin Gudang"
    
    def kelola_barang(self, barang, aksi: str):
        return f"Admin {self.nama} melakukan {aksi} pada barang {barang.nama}"

class ManajerLogistik(User):
    def __init__(self, user_id: str, nama: str, email: str, password: str, 
                 wilayah: str):
        super().__init__(user_id, nama, email, password)
        self.wilayah = wilayah
        
    def get_role(self) -> str:
        return "Manajer Logistik"
    
    def setujui_pemesanan(self, pemesanan_id: str) -> str:
        return f"Manajer {self.nama} menyetujui pemesanan {pemesanan_id}"


class Barang:
    def __init__(self, id_barang: str, nama: str, kategori: str, 
                 stok: int, harga: float, berat: float, 
                 min_stok: int = 10):
        self.id_barang = id_barang
        self.nama = nama
        self.kategori = kategori
        self.stok = stok
        self.harga = harga
        self.berat = berat
        self.min_stok = min_stok
        self.lokasi_rak = None
        
    def update_stok(self, jumlah: int) -> bool:
        if self.stok + jumlah < 0:
            return False
        self.stok += jumlah
        return True
    
    def cek_stok_menipis(self) -> bool:
        return self.stok <= self.min_stok
    
    def hitungBiayaPenyimpanan(self) -> float:
        # Biaya dasar per unit per hari
        return self.berat * 0.5 * (self.stok / 100)
    
    def to_dict(self):
        return {
            "id_barang": self.id_barang,
            "nama": self.nama,
            "kategori": self.kategori,
            "stok": self.stok,
            "harga": self.harga,
            "berat": self.berat,
            "min_stok": self.min_stok,
            "lokasi_rak": self.lokasi_rak
        }

class BarangPerishable(Barang):
    def __init__(self, id_barang: str, nama: str, kategori: str, 
                 stok: int, harga: float, berat: float, 
                 tanggal_kadaluarsa: str, min_stok: int = 10):
        super().__init__(id_barang, nama, kategori, stok, harga, berat, min_stok)
        self.tanggal_kadaluarsa = datetime.strptime(tanggal_kadaluarsa, "%Y-%m-%d")
        self.suhu_penyimpanan = -2  # Celcius
        
    def hitungBiayaPenyimpanan(self) -> float:

        biaya_dasar = super().hitungBiayaPenyimpanan()
        biaya_pendingin = self.berat * 0.3 * (self.stok / 100)
        return biaya_dasar + biaya_pendingin
    
    def cek_kadaluarsa(self) -> bool:
        return datetime.now() > self.tanggal_kadaluarsa
    
    def sisa_hari_kadaluarsa(self) -> int:
        selisih = self.tanggal_kadaluarsa - datetime.now()
        return selisih.days
    
    def to_dict(self):
        data = super().to_dict()
        data["tanggal_kadaluarsa"] = self.tanggal_kadaluarsa.strftime("%Y-%m-%d")
        data["suhu_penyimpanan"] = self.suhu_penyimpanan
        return data

class BarangFragile(Barang):
    def __init__(self, id_barang: str, nama: str, kategori: str, 
                 stok: int, harga: float, berat: float, 
                 instruksi_proteksi: str, min_stok: int = 10):
        super().__init__(id_barang, nama, kategori, stok, harga, berat, min_stok)
        self.instruksi_proteksi = instruksi_proteksi
        self.butuh_packing_khusus = True
        
    def hitungBiayaPenyimpanan(self) -> float:
    
        biaya_dasar = super().hitungBiayaPenyimpanan()
        biaya_proteksi = self.berat * 0.4 * (self.stok / 100)
        return biaya_dasar + biaya_proteksi
    
    def to_dict(self):
        data = super().to_dict()
        data["instruksi_proteksi"] = self.instruksi_proteksi
        data["butuh_packing_khusus"] = self.butuh_packing_khusus
        return data


class Supplier:
    def __init__(self, id_supplier: str, nama: str, alamat: str, 
                 telepon: str, email: str):
        self.id_supplier = id_supplier
        self.nama = nama
        self.alamat = alamat
        self.telepon = telepon
        self.email = email
        self.daftar_barang = []
        
    def tambah_barang_supplier(self, barang_id: str):
        self.daftar_barang.append(barang_id)
        
    def to_dict(self):
        return {
            "id_supplier": self.id_supplier,
            "nama": self.nama,
            "alamat": self.alamat,
            "telepon": self.telepon,
            "email": self.email,
            "daftar_barang": self.daftar_barang
        }


class TransaksiMasuk:
    def __init__(self, id_transaksi: str, barang_id: str, supplier_id: str,
                 jumlah: int, tanggal: str, admin_id: str):
        self.id_transaksi = id_transaksi
        self.barang_id = barang_id
        self.supplier_id = supplier_id
        self.jumlah = jumlah
        self.tanggal = datetime.strptime(tanggal, "%Y-%m-%d")
        self.admin_id = admin_id
        self.status = "Diterima"
        
    def to_dict(self):
        return {
            "id_transaksi": self.id_transaksi,
            "barang_id": self.barang_id,
            "supplier_id": self.supplier_id,
            "jumlah": self.jumlah,
            "tanggal": self.tanggal.strftime("%Y-%m-%d"),
            "admin_id": self.admin_id,
            "status": self.status
        }

class TransaksiKeluar:
    def __init__(self, id_transaksi: str, barang_id: str, jumlah: int,
                 tanggal: str, admin_id: str, tujuan: str):
        self.id_transaksi = id_transaksi
        self.barang_id = barang_id
        self.jumlah = jumlah
        self.tanggal = datetime.strptime(tanggal, "%Y-%m-%d")
        self.admin_id = admin_id
        self.tujuan = tujuan
        self.status = "Dikirim"
        
    def to_dict(self):
        return {
            "id_transaksi": self.id_transaksi,
            "barang_id": self.barang_id,
            "jumlah": self.jumlah,
            "tanggal": self.tanggal.strftime("%Y-%m-%d"),
            "admin_id": self.admin_id,
            "tujuan": self.tujuan,
            "status": self.status
        }

class SistemManajemenGudang(NotifikasiStok):
    def __init__(self):
        self.daftar_user = {}
        self.daftar_barang = {}
        self.daftar_supplier = {}
        self.daftar_transaksi_masuk = {}
        self.daftar_transaksi_keluar = {}
        self.log_notifikasi = []
        
    def kirim_peringatan_stok(self, pesan: str):
        """Implementasi dari interface NotifikasiStok"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "pesan": pesan,
            "dibaca": False
        }
        self.log_notifikasi.append(log_entry)
        return log_entry
    
    def tambah_user(self, user: User):
        self.daftar_user[user.user_id] = user
        
    def tambah_barang(self, barang: Barang):
        self.daftar_barang[barang.id_barang] = barang
        
    def tambah_supplier(self, supplier: Supplier):
        self.daftar_supplier[supplier.id_supplier] = supplier
        
    def transaksi_masuk(self, transaksi: TransaksiMasuk):
        self.daftar_transaksi_masuk[transaksi.id_transaksi] = transaksi
        
        if transaksi.barang_id in self.daftar_barang:
            barang = self.daftar_barang[transaksi.barang_id]
            barang.update_stok(transaksi.jumlah)
            
            if barang.cek_stok_menipis():
                pesan = f"PERINGATAN: Stok {barang.nama} (ID: {barang.id_barang}) menipis! Stok saat ini: {barang.stok}"
                self.kirim_peringatan_stok(pesan)
                
    def transaksi_keluar(self, transaksi: TransaksiKeluar):
        self.daftar_transaksi_keluar[transaksi.id_transaksi] = transaksi
        
        if transaksi.barang_id in self.daftar_barang:
            barang = self.daftar_barang[transaksi.barang_id]
            if barang.update_stok(-transaksi.jumlah):
                
                if barang.cek_stok_menipis():
                    pesan = f"PERINGATAN: Stok {barang.nama} (ID: {barang.id_barang}) menipis! Stok saat ini: {barang.stok}"
                    self.kirim_peringatan_stok(pesan)
                    
    def get_barang_dengan_stok_menipis(self) -> List[Barang]:
        return [b for b in self.daftar_barang.values() if b.cek_stok_menipis()]
    
    def hitung_total_biaya_penyimpanan(self) -> float:
        total = 0
        for barang in self.daftar_barang.values():
            total += barang.hitungBiayaPenyimpanan()
        return total
    
    def get_user_by_id(self, user_id: str):
        return self.daftar_user.get(user_id)
    
    def get_barang_by_id(self, barang_id: str):
        return self.daftar_barang.get(barang_id)
    
    def get_supplier_by_id(self, supplier_id: str):
        return self.daftar_supplier.get(supplier_id)
    
    def get_all_data(self):
        return {
            "users": {uid: {"nama": u.nama, "role": u.get_role()} for uid, u in self.daftar_user.items()},
            "barang": {bid: b.to_dict() for bid, b in self.daftar_barang.items()},
            "supplier": {sid: s.to_dict() for sid, s in self.daftar_supplier.items()},
            "transaksi_masuk": {tid: t.to_dict() for tid, t in self.daftar_transaksi_masuk.items()},
            "transaksi_keluar": {tid: t.to_dict() for tid, t in self.daftar_transaksi_keluar.items()},
            "notifikasi": self.log_notifikasi,
            "total_biaya_penyimpanan": self.hitung_total_biaya_penyimpanan()
        }
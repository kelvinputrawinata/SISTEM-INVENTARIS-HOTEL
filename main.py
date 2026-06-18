from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import uuid
from models import *

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

sistem = SistemManajemenGudang()

def init_demo_data():

    admin1 = AdminGudang("ADM001", "Kelvin Winata Putra", "budi@logistik.com", "admin123", "Gudang Utara")
    admin2 = AdminGudang("ADM002", "Graceisya", "siti@logistik.com", "admin123", "Gudang Selatan")
    manajer1 = ManajerLogistik("MGR001", "Ahmad Hidayat", "ahmad@logistik.com", "manager123", "Jawa Barat")
    
    sistem.tambah_user(admin1)
    sistem.tambah_user(admin2)
    sistem.tambah_user(manajer1)
    

    barang1 = Barang("BRG001", "Kursi Kantor", "Furniture", 50, 450000, 5.0, 20)
    barang2 = BarangPerishable("BRG002", "Susu UHT", "Makanan", 30, 15000, 1.0, "2026-12-31", 15)
    barang3 = BarangFragile("BRG003", "Kaca Cermin", "Dekorasi", 25, 350000, 8.0, "Handle dengan hati-hati, jangan jatuh", 10)
    barang4 = Barang("BRG004", "Laptop", "Elektronik", 15, 12000000, 2.5, 5)
    

    barang1.lokasi_rak = "Rak A-01"
    barang2.lokasi_rak = "Rak C-03 (Pendingin)"
    barang3.lokasi_rak = "Rak B-02 (Khusus)"
    barang4.lokasi_rak = "Rak A-05"
    
    sistem.tambah_barang(barang1)
    sistem.tambah_barang(barang2)
    sistem.tambah_barang(barang3)
    sistem.tambah_barang(barang4)
    
    
    supplier1 = Supplier("SUP001", "PT Maju Jaya", "Jl. Industri No. 10, Jakarta", "021-555-1234", "info@majujaya.com")
    supplier2 = Supplier("SUP002", "CV Sumber Makmur", "Jl. Raya Bandung No. 45", "022-555-5678", "sumbermakmur@email.com")
    
    supplier1.tambah_barang_supplier("BRG001")
    supplier1.tambah_barang_supplier("BRG004")
    supplier2.tambah_barang_supplier("BRG002")
    supplier2.tambah_barang_supplier("BRG003")
    
    sistem.tambah_supplier(supplier1)
    sistem.tambah_supplier(supplier2)
    
    transaksi1 = TransaksiMasuk("TRX001", "BRG001", "SUP001", 20, "2026-06-15", "ADM001")
    transaksi2 = TransaksiMasuk("TRX002", "BRG002", "SUP002", 15, "2026-06-16", "ADM002")
    
    sistem.transaksi_masuk(transaksi1)
    sistem.transaksi_masuk(transaksi2)


init_demo_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    data = sistem.get_all_data()
    stok_menipis = sistem.get_barang_dengan_stok_menipis()
    return render_template('dashboard.html', 
                         data=data, 
                         stok_menipis=stok_menipis,
                         total_biaya=data['total_biaya_penyimpanan'])

@app.route('/barang')
def daftar_barang():
    barang_list = sistem.daftar_barang
    return render_template('barang.html', barang_list=barang_list)

@app.route('/barang/tambah', methods=['GET', 'POST'])
def tambah_barang():
    if request.method == 'POST':
        try:
            id_barang = f"BRG{str(uuid.uuid4())[:8].upper()}"
            nama = request.form['nama']
            kategori = request.form['kategori']
            stok = int(request.form['stok'])
            harga = float(request.form['harga'])
            berat = float(request.form['berat'])
            min_stok = int(request.form.get('min_stok', 10))
            jenis = request.form['jenis']
            
            if jenis == 'biasa':
                barang = Barang(id_barang, nama, kategori, stok, harga, berat, min_stok)
            elif jenis == 'perishable':
                tanggal_kadaluarsa = request.form['tanggal_kadaluarsa']
                barang = BarangPerishable(id_barang, nama, kategori, stok, harga, berat, 
                                         tanggal_kadaluarsa, min_stok)
            elif jenis == 'fragile':
                instruksi = request.form['instruksi_proteksi']
                barang = BarangFragile(id_barang, nama, kategori, stok, harga, berat, 
                                      instruksi, min_stok)
            else:
                flash('Jenis barang tidak valid', 'error')
                return redirect(url_for('tambah_barang'))
            
            barang.lokasi_rak = request.form.get('lokasi_rak', '')
            sistem.tambah_barang(barang)
            flash('Barang berhasil ditambahkan!', 'success')
            return redirect(url_for('daftar_barang'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('tambah_barang'))
    
    return render_template('tambah_barang.html')

@app.route('/barang/<barang_id>/edit', methods=['GET', 'POST'])
def edit_barang(barang_id):
    barang = sistem.get_barang_by_id(barang_id)
    if not barang:
        flash('Barang tidak ditemukan', 'error')
        return redirect(url_for('daftar_barang'))
    
    if request.method == 'POST':
        try:
            barang.nama = request.form['nama']
            barang.kategori = request.form['kategori']
            barang.stok = int(request.form['stok'])
            barang.harga = float(request.form['harga'])
            barang.berat = float(request.form['berat'])
            barang.min_stok = int(request.form.get('min_stok', 10))
            barang.lokasi_rak = request.form.get('lokasi_rak', '')
            
            flash('Barang berhasil diupdate!', 'success')
            return redirect(url_for('daftar_barang'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('edit_barang.html', barang=barang)

@app.route('/api/barang')
def api_barang():
    return jsonify({bid: b.to_dict() for bid, b in sistem.daftar_barang.items()})

@app.route('/api/barang/<barang_id>')
def api_barang_detail(barang_id):
    barang = sistem.get_barang_by_id(barang_id)
    if barang:
        return jsonify(barang.to_dict())
    return jsonify({"error": "Barang tidak ditemukan"}), 404

@app.route('/api/notifikasi')
def api_notifikasi():
    return jsonify(sistem.log_notifikasi)

@app.route('/api/stok-menipis')
def api_stok_menipis():
    stok_menipis = sistem.get_barang_dengan_stok_menipis()
    return jsonify([b.to_dict() for b in stok_menipis])

@app.route('/api/biaya-penyimpanan')
def api_biaya_penyimpanan():
    return jsonify({
        "total": sistem.hitung_total_biaya_penyimpanan(),
        "detail": {bid: b.hitungBiayaPenyimpanan() for bid, b in sistem.daftar_barang.items()}
    })

if __name__ == '__main__':
    app.run(debug=True)
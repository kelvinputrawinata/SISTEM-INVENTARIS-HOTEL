# SISTEM-INVENTARIS-HOTEL
Sistem ini di buat sebagai syarat memenuhi nilai uas yang ada. 

Sistem Manajemen Inventaris dan Rantai Pasok Gudang adalah aplikasi berbasis web yang dibangun menggunakan Python (Flask) dan Bootstrap untuk membantu perusahaan mengelola operasional gudang secara digital dan otomatis. Sistem ini dirancang untuk mengatasi masalah pengelolaan stok manual, seperti ketidakakuratan data, keterlambatan pemesanan ulang, barang kadaluarsa yang tidak terpantau, serta kesulitan menghitung biaya penyimpanan.

Sistem memiliki dua jenis pengguna, yaitu Admin Gudang yang mengelola data barang dan transaksi, serta Manajer Logistik yang memantau operasional melalui dashboard dan menerima notifikasi stok menipis. Program mendukung tiga jenis barang, yaitu Barang Biasa, Barang Perishable (memiliki tanggal kadaluarsa), dan Barang Fragile (mudah pecah), masing-masing dengan perhitungan biaya penyimpanan yang berbeda.

Fitur utama sistem meliputi pengelolaan data barang, transaksi masuk dan keluar, pemantauan stok secara real-time, perhitungan biaya penyimpanan, dashboard monitoring, serta notifikasi otomatis ketika stok berada di bawah batas minimum. Sistem juga menyediakan REST API yang memungkinkan integrasi dengan aplikasi lain.

Dalam pengembangannya, sistem menerapkan lima konsep utama Object-Oriented Programming (OOP), yaitu Abstract Class, Inheritance, Polymorphism, Interface, dan Encapsulation, sehingga kode lebih terstruktur, fleksibel, dan mudah dikembangkan.

Secara keseluruhan, sistem ini mampu meningkatkan efisiensi pengelolaan gudang, menjaga akurasi data stok, mengurangi risiko kehabisan barang, serta membantu pengambilan keputusan melalui informasi yang tersaji secara cepat dan akurat.



Sistem ini dilengkapi dengan berbagai fitur yang mendukung pengelolaan gudang secara digital dan terotomatisasi. Berikut adalah fitur-fitur utama yang tersedia dalam sistem.

**Manajemen User**

Sistem menyediakan pengelolaan akun pengguna dengan dua peran berbeda yaitu Admin Gudang yang memiliki hak akses penuh untuk mengelola barang dan transaksi, serta Manajer Logistik yang bertugas memonitor operasional melalui dashboard dan menerima notifikasi. Setiap user harus melakukan login menggunakan email dan password sebelum dapat mengakses sistem untuk menjaga keamanan data.

**Manajemen Barang**

Sistem mampu mengelola tiga jenis barang dengan karakteristik berbeda. Barang Biasa adalah barang standar tanpa perlakuan khusus. Barang Perishable adalah barang yang memiliki tanggal kadaluarsa dan membutuhkan suhu penyimpanan khusus. Barang Fragile adalah barang yang mudah pecah dan membutuhkan instruksi proteksi serta packing khusus. Setiap barang memiliki atribut lengkap seperti ID, nama, kategori, stok, harga, berat, batas minimum stok, dan lokasi rak. Admin dapat menambah, mengedit, dan melihat daftar semua barang.

**Manajemen Supplier**

Sistem mencatat dan mengelola data pemasok barang dengan informasi lengkap seperti ID supplier, nama, alamat, telepon, email, dan daftar barang yang disuplai. Fitur ini memudahkan admin dalam melacak asal barang dan melakukan pemesanan ulang ke supplier yang tepat.

**Manajemen Transaksi**

Sistem mencatat dua jenis transaksi secara detail dan otomatis mengupdate stok. Transaksi Masuk mencatat penerimaan barang dari supplier dan otomatis menambah stok. Transaksi Keluar mencatat pengiriman barang ke customer dan otomatis mengurangi stok. Sistem juga mencegah transaksi keluar jika stok tidak mencukupi untuk menjaga integritas data.

**Notifikasi Stok Menipis**

Sistem secara otomatis mengirim peringatan kepada Manajer Logistik ketika stok barang berada di bawah batas minimum. Notifikasi tercatat dalam log dengan timestamp, isi pesan peringatan, dan status dibaca. Fitur ini memungkinkan manajer segera melakukan pemesanan ulang sebelum barang habis.

**Perhitungan Biaya Penyimpanan**

Sistem menghitung biaya penyimpanan secara otomatis dengan formula berbeda sesuai jenis barang. Barang Biasa menggunakan biaya dasar. Barang Perishable menambahkan biaya pendingin. Barang Fragile menambahkan biaya proteksi. Sistem menampilkan biaya per barang dan total biaya seluruh barang di dashboard.

**Dashboard Monitoring**

Sistem menampilkan informasi penting tentang kondisi gudang secara real-time dalam satu tampilan terintegrasi. Dashboard menampilkan statistik total barang, total supplier, jumlah user, jumlah stok menipis, total biaya penyimpanan, daftar barang dengan stok menipis, log notifikasi terbaru, dan riwayat transaksi masuk dan keluar.

**REST API**

Sistem menyediakan endpoint API untuk integrasi dengan aplikasi lain. Endpoint yang tersedia meliputi API untuk mendapatkan seluruh data barang, detail barang berdasarkan ID, daftar stok menipis, total biaya penyimpanan, dan log notifikasi. Semua API mengembalikan data dalam format JSON.

**Tampilan Web Responsif**

Sistem dibangun dengan antarmuka yang responsif sehingga dapat diakses dari berbagai perangkat seperti komputer, laptop, tablet, dan smartphone. Navigasi antar halaman jelas dan konsisten untuk memudahkan penggunaan.



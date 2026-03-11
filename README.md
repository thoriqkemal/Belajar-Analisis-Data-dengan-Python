# Proyek Analisis Data: Bike Sharing Dashboard

Dashboard interaktif ini dibangun menggunakan **Streamlit** untuk menganalisis tren penggunaan sepeda berdasarkan dataset *Bike-sharing*. Proyek ini bertujuan untuk mengidentifikasi pola penyewaan musiman, pengaruh kondisi lingkungan, dan memberikan rekomendasi strategis bagi manajemen operasional.

## 📊 Ringkasan Analisis & Insight

Berdasarkan visualisasi dan perhitungan pada dashboard, berikut adalah temuan utamanya:

* **Pertumbuhan YoY (Year-over-Year)**: Jumlah peminjaman pada Desember 2012 mengalami pertumbuhan sebesar **31,17%** dibandingkan dengan Desember 2011.
* **Korelasi Utama**: Pengguna terdaftar memiliki korelasi tertinggi (**97%**) terhadap total jumlah peminjaman.
* **Pola Waktu Sibuk**: Permintaan tertinggi terjadi pada jam pulang kerja, khususnya antara pukul **16.00 hingga 19.00**.
* **Segmentasi Lingkungan**: Cluster **"Kondisi Ideal"** (Cerah & Hangat) menunjukkan rata-rata penyewaan tertinggi, sementara kondisi ekstrem menyebabkan penurunan drastis.
* **Analisis Musiman**: **Musim Panas (Summer)** merupakan periode puncak permintaan, sedangkan **Musim Dingin (Winter)** mencatatkan angka terendah.

## 💡 Rekomendasi Bisnis

* **Program Loyalitas**: Memperkuat program membership bagi pengguna terdaftar karena kelompok ini adalah kontributor pendapatan paling stabil.
* **Manajemen Armada**: Melakukan *rebalancing* armada secara proaktif menuju area perkantoran atau hub transportasi sebelum pukul 16.00 untuk memenuhi lonjakan permintaan jam sibuk.
* **Rolling Maintenance**: Alokasikan 100% ketersediaan unit pada musim panas untuk memaksimalkan pendapatan, dan jadwalkan pemeliharaan besar (*overhaul*) pada musim dingin.
* **Strategi Promosi**: Memberikan insentif berupa 'Voucher Khusus Musim Dingin' pada kuartal keempat untuk menjaga stabilitas jumlah penyewaan di luar jam sibuk.

## 🌐 Live Project

Anda dapat mengakses dashboard yang sudah berjalan secara langsung melalui tautan berikut:

* **[Bike Sharing Analysis Dashboard](https://dashboardpy-4c8xrdpnav7jnhd8xjwnpf.streamlit.app/)**

## 🛠️ Fitur Dashboard

* **Filter Eksplorasi**: Filter rentang waktu dan pemilihan musim secara dinamis di sidebar.
* **Distribusi Kategori**: Visualisasi interaktif menggunakan histogram dan pie chart untuk variabel cuaca, hari kerja, dan jam.
* **Environmental Clustering**: Analisis lanjutan yang mengelompokkan penggunaan berdasarkan suhu, kelembapan, dan kondisi cuaca.

## 📂 Struktur Proyek

```text
.
├── data/
│   └── hour.csv             # Dataset utama (per jam)
├── dashboard/
│   └── dashboard.py         # Script utama Streamlit
├── requirements.txt         # Daftar library Python
└── README.md                # Dokumentasi proyek

```

## 🚀 Cara Menjalankan secara Lokal

1. **Persiapkan Environment**:
```bash
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt

```


2. **Jalankan Aplikasi**:
```bash
streamlit run dashboard/dashboard.py

```



## 📜 Lisensi

Proyek ini bersifat **Open Source** dan dilisensikan di bawah **MIT License**. Anda bebas untuk menggunakan, memodifikasi, dan mendistribusikan kode ini untuk tujuan apa pun selama menyertakan atribusi kepada penulis.

## 👨‍💻 Identitas Pengembang

* **Nama**: Thoriq Kemal
* **Email**: thoriqekemal@gmail.com
* **ID Dicoding**: thoriqkemal

---
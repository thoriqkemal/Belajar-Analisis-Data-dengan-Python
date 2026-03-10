import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import os

# --- 1. DATA WRANGLING ---
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "../data/hour.csv") 
    
    if not os.path.exists(path):
        st.error(f"File not found at {path}. Please check your file structure!")
        st.stop()
        
    df = pd.read_csv(path)
    
    df['dteday'] = pd.to_datetime(df['dteday'])
    df.rename(columns={
        'yr': 'year',
        'mnth': 'month',
        'hr': 'hour',
        'weathersit': 'weather_condition',
        'hum': 'humidity',
        'cnt': 'total_count'
    }, inplace=True)
    
    q1 = df['total_count'].quantile(0.25)
    q3 = df['total_count'].quantile(0.75)

    df['total_count'] = np.where(df['total_count'] > q3, q3, df['total_count'])
    df['total_count'] = np.where(df['total_count'] < q1, q1, df['total_count'])
    
    return df

hour_df = load_data()

# --- 2. SIDEBAR / HEADER ---
st.title('Proyek Analisis Data: Bike-sharing-dataset')
st.sidebar.header("User Info")
st.sidebar.markdown("""
- **Nama:** Thoriq Kemal
- **Email:** thoriqekemal@gmail.com
- **ID Dicoding:** thoriqkemal
""")

# --- SIDEBAR FILTER ---
st.sidebar.header("Filter Eksplorasi")

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

try:
    # Mengambil input rentang waktu
    date_range = st.sidebar.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Validasi: Cek apakah pengguna sudah memilih kedua tanggal (start & end)
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Silakan pilih rentang waktu yang lengkap (Tanggal Mulai dan Tanggal Selesai).")
        st.stop() # Menghentikan eksekusi sementara sampai input lengkap

except Exception as e:
    st.error(f"Terjadi kesalahan pada input tanggal: {e}")
    st.stop()

season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
selected_season = st.sidebar.multiselect(
    "Pilih Musim:",
    options=list(season_map.keys()),
    default=list(season_map.keys()),
    format_func=lambda x: season_map[x]
)

filter_df = hour_df[
    (hour_df["dteday"] >= pd.to_datetime(start_date)) & 
    (hour_df["dteday"] <= pd.to_datetime(end_date)) &
    (hour_df["season"].isin(selected_season))
]

# --- 3. HELPER PLOTTING FUNCTION ---
def plot_monthly_trend(data, title, color='skyblue'):
    monthly = data.groupby(pd.Grouper(key='dteday', freq='M'))['total_count'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly['dteday'], monthly['total_count'], marker='o', linestyle='-', color=color)
    
    ax.set_facecolor('#00172B')
    fig.patch.set_facecolor('#00172B')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.grid(True, alpha=0.3)
    plt.title(title, color='white')
    
    st.pyplot(fig)

# --- 4. VISUALIZATIONS ---
st.subheader("Distribution of Bike Rentals per Month (2011 - 2012)")
plot_monthly_trend(hour_df, "Trend Overview")

st.subheader('Distribution based on Categories')
tab1, tab2 = st.tabs(["Histograms", "Pie Charts"])

with tab1:
    features_hist = ['month', 'hour', 'weekday', 'temp', 'humidity', 'windspeed']
    for feat in features_hist:
        fig = px.histogram(filter_df, x=feat, y='total_count', title=f'Distribution of {feat.capitalize()}', color_discrete_sequence=['#636EFA'], template="plotly_dark")
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    features_pie = ['season', 'year', 'holiday', 'workingday', 'weather_condition']
    for feat in features_pie:
        fig = px.pie(filter_df, names=feat, values='total_count', title=f'Share by {feat.replace("_", " ").capitalize()}')
        st.plotly_chart(fig, use_container_width=True)

# --- 5. CORRELATION ---
st.subheader('Correlation Matrix')
correlation = filter_df.select_dtypes(include=['number']).corr()
fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', ax=ax_corr)
st.pyplot(fig_corr)

# --- 6. ADVANCED ANALYSIS: CLUSTERING ---
st.header("Analisis Lanjutan: Environmental Clustering")

def classify_usage_segment(row):
    if row['temp'] > 0.6 and row['weather_condition'] == 1:
        return 'Kondisi Ideal (Cerah & Hangat)'
    elif row['weather_condition'] >= 3 or row['windspeed'] > 0.5:
        return 'Kondisi Kurang Ideal (Ekstrem)'
    elif row['humidity'] > 0.7:
        return 'Kondisi Menengah (Lembap)'
    else:
        return 'Kondisi Standar'

filter_df['usage_cluster'] = filter_df.apply(classify_usage_segment, axis=1)

cluster_summary = filter_df.groupby('usage_cluster')['total_count'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    x='usage_cluster', 
    y='total_count', 
    data=cluster_summary, 
    color='#4682B4',
    ax=ax
)

plt.xticks(rotation=15, ha='right')

ax.set_title('Average Rentals by Environmental Cluster', fontsize=14, fontweight='bold')
ax.set_xlabel('Usage Segment Cluster')
ax.set_ylabel('Average Total Count')
sns.despine()

st.pyplot(fig)

st.info("""
**Insight Analisis Clustering:**
* Cluster ini dibentuk dengan menggabungkan variabel **temp**, **humidity**, **windspeed**, dan **weather_condition** untuk memberikan gambaran kondisi lingkungan yang komprehensif.
* **Kondisi Ideal (Cerah dan Hangat)** menunjukkan rata-rata peminjaman yang jauh lebih tinggi dibandingkan segmen lainnya.
* Sebaliknya pada **Kondisi Kurang Ideal (Hujan/Salju atau Ekstrem)**, terjadi penurunan permintaan yang signifikan akibat faktor cuaca buruk atau kecepatan angin tinggi.
""")

# --- 7. BUSINESS QUESTIONS ---
st.header('Pertanyaan Bisnis')

col1, col2 = st.columns(2)

with col1:
    st.subheader("YoY growth in Desember")
    st.info("""
        Apakah total peminjaman sepeda pada bulan Desember 2012 mengalami pertumbuhan dibandingkan dengan Desember 2011, dan faktor apa yang paling memengaruhinya?
    """)
    dec_2011 = hour_df[(hour_df['dteday'].dt.year == 2011) & (hour_df['dteday'].dt.month == 12)]['total_count'].sum()
    dec_2012 = hour_df[(hour_df['dteday'].dt.year == 2012) & (hour_df['dteday'].dt.month == 12)]['total_count'].sum()

    growth = dec_2012 - dec_2011
    growth_percentage = (growth / dec_2011) * 100
    
    labels = ['Desember 2011', 'Desember 2012']
    values = [dec_2011, dec_2012]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(labels, values, color='#4682B4',width=0.6)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (max(values)*0.02), 
                f'{int(yval):,}', ha='center', va='bottom', 
                fontsize=12, fontweight='bold')

    ax.text(0.5, max(values) * 0.5, f"Growth: +{growth_percentage:.2f}%", 
            ha='center', fontsize=13, color='darkblue', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="darkblue", lw=1.5))

    ax.set_title('Growth of Total Rental\nDesember 2011 vs Desember 2012', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('Total Rental Count', fontsize=12)
    ax.set_ylim(0, max(values) * 1.2)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig)

    st.metric(
        label="Pertumbuhan Desember (YoY)", 
        value=f"{dec_2012:,} unit", 
        delta=f"{growth_percentage:.2f}% (20212 vs 2011)"
    )

with col2:
    st.subheader("Seasonality Analysis")
    st.info("""
        Bagaimana perbedaan signifikan jumlah rata-rata peminjaman sepeda antar musim di tahun 2012 untuk menentukan alokasi stok sepeda dan jadwal pemeliharaan armada?
    """)
    seasonal_mean = hour_df.groupby('season')['total_count'].mean().reset_index()
    season_map = {
        1: 'Musim Dingin (Winter)',
        2: 'Musim Semi (Spring)',
        3: 'Musim Panas (Summer)',
        4: 'Musim Gugur (Autumn/Fall)'
    }
    seasonal_mean['season_name'] = seasonal_mean['season'].map(season_map)

    peak_season = seasonal_mean.loc[seasonal_mean['total_count'].idxmax()]
    low_season = seasonal_mean.loc[seasonal_mean['total_count'].idxmin()]

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        x='season_name', 
        y='total_count', 
        data=seasonal_mean, 
        color='#4682B4',
        legend=False
    )

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, 9), 
            textcoords = 'offset points',
            fontsize=11, fontweight='bold')

    ax.set_title('Mean of Total Count Each Season', fontsize=15, pad=20, fontweight='bold')
    ax.set_xlabel('Season', fontsize=12)
    ax.set_ylabel('Mean of Total Count', fontsize=12)
    plt.xticks(rotation=15)
    ax.set_ylim(0, peak_season['total_count'] * 1.15) 

    plt.tight_layout()

    st.pyplot(fig)

    st.write(f"✅ Paling Ramai: {peak_season['season_name']} dengan rata-rata {peak_season['total_count']:,.2f} total penyewaan.")
    st.write(f"❌ Paling Sepi: {low_season['season_name']} dengan rata-rata {low_season['total_count']:,.2f} total penyewaan.")


st.subheader("YoY Trends")
st.info("""
Bagaimana tren fluktuasi bulanan peminjaman sepeda dari tahun 2011 ke 2012 guna mengidentifikasi bulan-bulan dengan penurunan tajam yang memerlukan strategi promosi khusus?
""")

monthly_trend = hour_df.groupby(['year', 'month'])['total_count'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x='month', y='total_count', hue='year', marker='o', ax=ax)

ax.set_title('Monthly Bike Rentals: 2011 vs 2012', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Total Rental Count')
ax.set_xticks(range(1, 13))
ax.legend(title='Year', labels=['2011', '2012'])
ax.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig)

with st.expander("Lihat Detail Angka Pertumbuhan YoY"):
    monthly_yoy = hour_df.groupby(['month', 'year'])['total_count'].sum().unstack()
    monthly_yoy.columns = ['2011', '2012']
    monthly_yoy['Growth_Pct'] = ((monthly_yoy['2012'] - monthly_yoy['2011']) / monthly_yoy['2011']) * 100
    st.dataframe(monthly_yoy.style.format("{:.2f}"))

st.header("Conclusion")
st.info("""
1. Iya, terjadi pertumbuhan yang signifikan di bulan Desember 2012. Berdasarkan data, jumlah peminjaman meningkat pesat dengan angka YoY Growth sebesar 31,17% dibandingkan Desember 2011. Faktor faktor yang mempengaruhi antara lain adalah kategori **pengguna terdaftar (97%)** dan **jam peminjaman (42%)** seperti yang ditampilkan pada matriks korelasi diatas.

2. Pada **musim panas** merupakan periode dengan permintaan tertinggi, sehingga diperlukan pemeliharaan ketersediaan unit sebesar 100% di seluruh stasiun. Sebaliknya, **musim dingin** mencatatkan rata-rata peminjaman terendah, yang dapat dimanfaatkan sebagai periode optimal untuk melakukan pemeliharaan armada secara besar-besaran tanpa mengganggu stabilitas layanan.

3. Kinerja tahun 2012 tumbuh melampaui 2011 secara konsisten tanpa ada penurunan performa YoY. Meski demikian, terdapat tren penurunan pasca-Juli hingga akhir tahun yang sejalan dengan transisi musim dingin. Mengingat faktor suhu sangat memengaruhi minat pengguna, pemberian 'Voucher khusus Cuaca Dingin' pada kuartal keempat menjadi strategi krusial untuk menjaga stabilitas jumlah penyewaan di luar jam sibuk. 

- Berdasarkan matriks korelasi, faktor yang paling berpengaruh terhadap jumlah penyewaan adalah kategori **pengguna terdaftar (97%)** dan **jam peminjaman (42%)**. Berdasarkan distribusinya, sepeda paling sering dipinjam pada jam-jam sibuk, khususnya pada pukul 4 sore hingga 7 malam.
""")

# --- 8. SARAN/REKOMENDASI ---
st.header("Saran/Rekomendasi")
st.info("""
- 1. Berdasarkan pertumbuhan signifikan sebesar 31,17% (YoY) di Desember 2012, ditemukan bahwa pengguna terdaftar memiliki korelasi tertinggi (97%) terhadap jumlah peminjaman. Rekomendasi kami adalah dengan  memperkuat program loyalitas (seperti membership tahunan atau poin reward) karena kelompok ini / **Pengguna terdaftar** adalah kontributor pendapatan paling stabil, terutama untuk memitigasi fluktuasi jumlah pengguna baru (casual) di akhir tahun.

- 2. Data menunjukkan perbedaan permintaan yang ekstrem, di mana musim panas mencatatkan permintaan tertinggi sementara musim dingin mencatatkan angka terendah. Disarankan untuk menerapkan sistem pemeliharaan bergulir (rolling maintenance). Alokasikan 100% ketersediaan unit selama **musim panas** untuk **memaksimalkan revenue**, dan jadwalkan **pemeliharaan besar (overhaul)** armada pada **musim dingin**. Hal ini akan meminimalisir downtime layanan pada saat permintaan sedang melonjak.

- 3. Untuk menjaga stabilitas penyewaan, diperlukan '**Voucher Khusus Musim Dingin**' atau **insentif khusus** pada kuartal keempat. Target utama promosi ini adalah **jam-jam di luar sibuk** (off-peak hours) guna menstimulasi minat pengguna yang c**enderung menurun akibat faktor cuaca**.

- Faktor jam peminjaman (42%) menunjukkan pola distribusi yang sangat terpusat pada pukul 16.00 hingga 19.00. Guna menghindari kekosongan unit di titik-titik krusial, manajemen perlu melakukan rebalancing armada secara proaktif menuju area perkantoran atau hub transportasi utama sebelum pukul 4 sore. Langkah ini memastikan permintaan pada jam sibuk dapat terpenuhi secara maksimal tanpa adanya kehilangan potensi pelanggan akibat unit yang tidak tersedia.
""")
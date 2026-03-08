import pandas as pd
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
    
    q1, q3 = df['total_count'].quantile([0.25, 0.75])
    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    df = df[(df['total_count'] >= lower_bound) & (df['total_count'] <= upper_bound)]
    
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

# --- 3. HELPER PLOTTING FUNCTION ---
def plot_monthly_trend(data, title, color='skyblue'):
    monthly = data.groupby(pd.Grouper(key='dteday', freq='ME'))['total_count'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly['dteday'], monthly['total_count'], marker='o', linestyle='-', color=color)
    
    # Styling for Dark Theme
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
        fig = px.histogram(hour_df, x=feat, y='total_count', title=f'Distribution of {feat.capitalize()}', color_discrete_sequence=['#636EFA'], template="plotly_dark")
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    features_pie = ['season', 'year', 'holiday', 'workingday', 'weather_condition']
    for feat in features_pie:
        fig = px.pie(hour_df, names=feat, values='total_count', title=f'Share by {feat.replace("_", " ").capitalize()}')
        st.plotly_chart(fig, use_container_width=True)

# --- 5. CORRELATION ---
st.subheader('Correlation Matrix')
correlation = hour_df.select_dtypes(include=['number']).corr()
fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', ax=ax_corr)
st.pyplot(fig_corr)

# --- 6. BUSINESS QUESTIONS ---
st.header('Pertanyaan Bisnis')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Rental: Des 2012")
    st.info("""
    Berapa total terpinjam pada bulan Desember 2012?
    """)
    total = hour_df[(hour_df['year'] == 1) & (hour_df['month'] == 12)]['total_count'].sum()
    st.metric("Total Terpinjam", f"{total:,}")

with col2:
    st.subheader("Seasonality Analysis")
    st.info("""
    Tren Peminjaman Sepeda: Musim Paling Populer vs. Paling Sepi?
    """)
    season_map = {
        1: 'Musim Dingin (Winter) ❄️',
        2: 'Musim Semi (Spring) 🌸',
        3: 'Musim Panas (Summer) ☀️',
        4: 'Musim Gugur (Autumn/Fall) 🍂'
    }    
    seasonal_data = hour_df.groupby('season')['total_count'].sum()
    peak_season = season_map[seasonal_data.idxmax()]
    low_season = season_map[seasonal_data.idxmin()]
    st.write(f"✅ Paling Ramai: **{peak_season}**")
    st.write(f"❌ Paling Sepi: **{low_season}**")

st.subheader("Kinerja Peminjaman dalam Setahun Terakhir (2012)")
st.info("""
Bagaimana kinerja peminjaman per bulan dari tahun ke tahun?
""")

monthly_yoy = hour_df.groupby(['month', 'year'])['total_count'].sum().unstack()
monthly_yoy.columns = ['2011', '2012']

avg_growth = ((monthly_yoy['2012'].sum() - monthly_yoy['2011'].sum()) / monthly_yoy['2011'].sum()) * 100

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=hour_df, x='month', y='total_count', hue='year', palette='viridis', ax=ax)

ax.set_title('Monthly Bike Rentals: 2011 vs 2012', fontsize=16, fontweight='bold')
ax.set_xlabel('Month', fontsize=12, fontweight='bold') 
ax.set_ylabel('Total Rental Count', fontsize=12, fontweight='bold')
ax.legend(title='Year', labels=['2011', '2012'])
ax.grid(axis='y', linestyle='--', alpha=0.3)

st.pyplot(fig)

with st.expander("Lihat Detail Angka Pertumbuhan YoY"):
    # Menambahkan kolom persentase pertumbuhan per bulan
    monthly_yoy['Growth (%)'] = (monthly_yoy['2012'] - monthly_yoy['2011']) / monthly_yoy['2011'] * 100
    st.dataframe(monthly_yoy.style.format("{:.2f}"))

# --- 7. CONCLUSION ---
st.header("Conclusion")
st.info("""
1. Total sepeda terpinjam pada bulan Desember 2012 yaitu **114.538**.
2. Peminjaman paling banyak terjadi pada **musim panas (summer)**, sedangkan peminjaman paling sedikit terjadi pada **musim dingin (winter)**
3. Secara keseluruhan, kinerja peminjaman di tahun 2012 jauh melampaui 2011 di setiap bulannya. Tidak ada satu bulan pun yang mengalami penurunan. Ini menandakan bisnis atau layanan peminjaman sepeda tersebut berkembang dengan sangat pesat. Terjadi Lonjakan tinggi yang drastis di awal tahun dengan pertumbuhan rata-rata diatas 120%. 
4. Berdasarkan matriks korelasi, faktor yang paling berpengaruh terhadap jumlah penyewaan adalah kategori **pengguna terdaftar (97%)** dan **jam peminjaman (42%)**. Berdasarkan distribusinya, sepeda paling sering dipinjam pada jam-jam sibuk, khususnya pada pukul 4 sore hingga 7 malam.
""")
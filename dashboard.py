# streamlit_dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set style
sns.set(style='whitegrid')

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    return pd.read_csv('processed_air_quality_dataset.csv')

# Memuat dataset
data = load_data()

# Judul Aplikasi
st.title("Dashboard Kualitas Udara 2013-2017")
st.write("""
### Mengamati Pola Kualitas Udara di Kota Guanyuan, Tiantan, dan Dingling
Dashboard ini menyajikan visualisasi interaktif untuk menganalisis kualitas udara berdasarkan PM2.5, distribusi kualitas udara, serta faktor-faktor seperti kelembapan dan musim.
Setiap bagian pada dashboard ini dilengkapi dengan penjelasan yang dapat membantu Anda memahami pola yang muncul dari data tersebut.
""")

# Sidebar untuk filter kota
st.sidebar.header("Pengaturan")
city = st.sidebar.selectbox(
    "Pilih Kota",
    ['Guanyuan', 'Tiantan', 'Dingling']
)

# Filter dataset berdasarkan kota yang dipilih
filtered_data = data[data['station'] == city]

# Pilihan variabel untuk analisis korelasi
st.sidebar.subheader("Korelasi Variabel")
x_axis = st.sidebar.selectbox("Pilih variabel X", ['DEWP', 'TEMP', 'PRES', 'PM2.5'])
y_axis = st.sidebar.selectbox("Pilih variabel Y", ['PM2.5', 'SO2', 'NO2', 'CO', 'O3'])

# Menampilkan dataset jika diinginkan
if st.sidebar.checkbox("Tampilkan Data Mentah", False):
    st.subheader(f"Dataset Kota {city}")
    st.write(filtered_data)

# Bagian 1: Analisis Musim dan Rata-rata PM2.5
st.header(f"Variasi PM2.5 Berdasarkan Musim di {city}")
st.write("""
Bagian ini menampilkan rata-rata PM2.5 di setiap musim (musim panas, musim dingin, musim gugur, dan musim semi) untuk kota yang dipilih.
PM2.5 adalah partikel halus di udara yang berukuran lebih kecil dari 2.5 mikrometer dan dapat berdampak pada kesehatan pernapasan.
Nilai PM2.5 yang lebih tinggi dapat menunjukkan kualitas udara yang buruk.
""")
seasonal_avg = filtered_data.groupby('Season')['PM2.5'].mean()

# Visualisasi
fig, ax = plt.subplots()
seasonal_avg.plot(kind='bar', color='skyblue', ax=ax)
ax.set_xlabel('Season')
ax.set_ylabel('Average PM2.5')
ax.set_title(f'Rata-rata PM2.5 per Musim di {city}')
st.pyplot(fig)

# Bagian 2: Distribusi Kategori Kualitas Udara
st.header(f"Distribusi Kategori Kualitas Udara di {city}")
st.write("""
Bagian ini menunjukkan distribusi kategori kualitas udara berdasarkan data yang dikategorikan sebagai baik, sedang, tidak sehat, dan lainnya.  
Kategori kualitas udara didasarkan pada ambang batas PM2.5, di mana nilai yang lebih tinggi menunjukkan udara yang lebih tercemar.
""")
fig, ax = plt.subplots()
sns.countplot(x='Air_Quality_Category', data=filtered_data, palette='Set2', ax=ax)
ax.set_xlabel('Kategori Kualitas Udara')
ax.set_title(f'Distribusi Kategori Kualitas Udara di {city}')
st.pyplot(fig)

# Bagian 3: Korelasi Variabel
st.header(f"Korelasi {x_axis} vs {y_axis} di {city}")
st.write(f"""
Bagian ini menunjukkan hubungan antara {x_axis} dan {y_axis}. Korelasi ini dapat membantu kita melihat apakah ada hubungan linier antara kedua variabel.
Misalnya, jika kita memilih 'DEWP' (Titik embun) sebagai variabel X dan 'PM2.5' sebagai variabel Y, kita dapat melihat bagaimana tingkat kelembapan di udara mempengaruhi konsentrasi PM2.5.
""")
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(x=x_axis, y=y_axis, data=filtered_data, scatter_kws={'s': 10}, line_kws={'color': 'red'}, ax=ax)
ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
ax.set_title(f'{x_axis} vs {y_axis} di {city}')
st.pyplot(fig)

# Bagian 4: Tren Kualitas Udara per Tahun
st.header(f"Tren Rata-rata Kualitas Udara per Tahun di {city}")
st.write("""
Grafik ini menampilkan tren rata-rata kualitas udara dari tahun ke tahun di kota yang dipilih.  
Tren ini menunjukkan bagaimana kualitas udara berubah seiring waktu, apakah semakin membaik atau memburuk.
""")
filtered_data['datetime'] = pd.to_datetime(filtered_data['datetime'])
filtered_data['year'] = filtered_data['datetime'].dt.year
yearly_avg = filtered_data.groupby('year')['Air_Quality_Numeric'].mean()

# Visualisasi
fig, ax = plt.subplots()
yearly_avg.plot(kind='line', ax=ax, marker='o', color='green')
ax.set_xlabel('Year')
ax.set_ylabel('Rata-rata Kualitas Udara (Numeric)')
ax.set_title(f'Tren Kualitas Udara di {city} (2013-2017)')
st.pyplot(fig)

# Bagian 5: Analisis Kelembaban Udara (DEWP) terhadap PM2.5 per Musim
st.header(f"Korelasi DEWP dengan PM2.5 Berdasarkan Musim di {city}")
st.write("""
Di bagian ini, kita dapat melihat bagaimana kelembapan udara (DEWP - Titik embun) mempengaruhi konsentrasi PM2.5.
Titik embun adalah suhu di mana udara mulai mengembun, dan ini seringkali berkaitan dengan kelembapan udara.  
Dengan mengamati hubungan antara kedua variabel ini berdasarkan musim, kita dapat melihat apakah musim tertentu memiliki dampak yang lebih besar terhadap konsentrasi polutan.
""")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='DEWP', y='PM2.5', hue='Season', data=filtered_data, palette='coolwarm', ax=ax)
ax.set_xlabel('Titik Embun (DEWP)')
ax.set_ylabel('Tingkat PM2.5')
ax.set_title(f'Korelasi DEWP dengan PM2.5 di {city} Berdasarkan Musim')
st.pyplot(fig)

# Menampilkan footer dengan informasi tambahan
st.sidebar.markdown("""
---
**Dibuat oleh:** Rizky Alviaindo  
**Email:** risky.alviando@gmail.com
""")

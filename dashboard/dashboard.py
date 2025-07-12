import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as mticker

sns.set(style='dark')

st.header('Proyek Analisis Data: Bike Sharing Dataset')

st.markdown(""" ### Pertanyaan Bisnis:
- Bagaimana pengaruh musim dan cuaca terhadap jumlah pengguna?
- Pada jam berapa aktivitas pengguna paling tinggi dan paling rendah?""")

# Load dataset
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Konversi kolom 'dteday' ke format datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# tanggal yang valid
start_date = day_df['dteday'].min()
end_date = day_df['dteday'].max()

# Fitur interaktif pilihan tanggal
st.sidebar.header("Filter Data")
selected_start = st.sidebar.date_input("Pilih tanggal mulai:", start_date, min_value=start_date, max_value=end_date)
selected_end = st.sidebar.date_input("Pilih tanggal akhir:", end_date, min_value=start_date, max_value=end_date)

# Filter dataset berdasarkan tanggal yang dipilih
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(selected_start)) & 
                     (day_df['dteday'] <= pd.to_datetime(selected_end))]
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(selected_start)) & 
                           (hour_df['dteday'] <= pd.to_datetime(selected_end))]

st.write("### Preview Data Harian")
st.dataframe(filtered_df)


season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_map = {
    1: 'Good',
    2: 'Misty',
    3: 'Bad',
}

# Mengelompokkan data berdasarkan season dan weather situation
grouped_df = day_df.groupby(by=['season', 'weathersit']).agg({'cnt': 'sum'}).reset_index()
grouped_df['season'] = grouped_df['season'].map(season_map)
grouped_df['weathersit'] = grouped_df['weathersit'].map(weather_map)
st.write("### Total Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")
st.dataframe(grouped_df)

st.markdown("""
### Informasi
**Season:**
- 1 : Spring  
- 2 : Summer  
- 3 : Fall  
- 4 : Winter  

**Weathersit:**
- 1 : Good  
- 2 : Misty  
- 3 : Bad  
""")

grouped_df = filtered_df.groupby(by=['season', 'weathersit']).agg({'cnt': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=grouped_df, x='season', y='cnt', hue='weathersit', palette='viridis', ax=ax)
ax.set_xlabel('Season')
ax.set_ylabel('Total Count')
ax.set_title('Total Count of Users per Season and Weather Situation')
ax.legend(title='Weather Situation')
st.pyplot(fig)

# Analisis rata-rata suhu, kelembaban, dan kecepatan angin berdasarkan kondisi cuaca
f = filtered_df['weathersit'].map({1: 'Good (1)', 2: 'Misty (2)',3: 'Bad (3)'})
st.write("### Rata-rata Temperatur, Kecepatan Angin, dan Kelembaban Berdasarkan Kondisi Cuaca")
weather_agg = filtered_df.groupby(f).agg({
    'temp': 'mean',
    'windspeed': 'mean',
    'hum': 'mean',
})
st.dataframe(weather_agg)

# Total penggunaan sepeda berdasarkan musim
season_map = {1: 'Spring (1)', 2: 'Summer (2)', 3: 'Fall (3)', 4: 'Winter (4)'}
filtered_df['season_label'] = filtered_df['season'].map(season_map)

st.write("### Total Penggunaan Sepeda Berdasarkan Musim")
season_agg = filtered_df.groupby('season_label').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum',
})
st.dataframe(season_agg)

# Visualisasi penggunaan sepeda per musim
st.write("### Total Penggunaan Sepeda Berdasarkan Musim")

grouped_df = filtered_df.groupby(by='season').agg({'cnt': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=grouped_df, x='season', y='cnt', palette='Blues', ax=ax)

ax.ticklabel_format(style='plain', axis='y')
ax.set_xlabel('Season')
ax.set_ylabel('Total Users')
ax.set_title('Total User Count per Season')

st.pyplot(fig)


# Total penggunaan sepeda berdasarkan kondisi cuaca
weather_map = {1: 'Good Weather (1)', 2: 'Mist + Cloudy (2)', 3: 'Bad Weather (3)'}
filtered_df['weather_label'] = filtered_df['weathersit'].map(weather_map)

st.write("### Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca")
weather_usage = filtered_df.groupby('weather_label').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum',
})
st.dataframe(weather_usage)

# Visualisasi penggunaan sepeda berdasarkan kondisi cuaca
st.write("### Total Penggunaan Sepeda Berdasarkan Kondisi Cuaca")

grouped_df = filtered_df.groupby(by='weathersit').agg({'cnt': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=grouped_df, x='weathersit', y='cnt', palette='coolwarm', ax=ax)

ax.ticklabel_format(style='plain', axis='y')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Total Users')
ax.set_title('Total User Count by Weather Condition')

st.pyplot(fig)


# Preview data per jam dengan filtering
st.write("### Preview Data Per Jam")
st.dataframe(filtered_hour_df)

# Analisis penggunaan berdasarkan jam
per_hour = filtered_hour_df.groupby('hr').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum',
}).sort_values(by=['cnt'], ascending=False)

st.write("### 5 Jam dengan Penggunaan Tertinggi")
st.dataframe(per_hour.head(5))

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=per_hour.head(5).index, y=per_hour.head(5)['cnt'], palette='Blues', ax=ax)
ax.set_title("Top 5 Hours with Highest Usage")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Users")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)

st.write("### 5 Jam dengan Penggunaan Terendah")
st.dataframe(per_hour.tail(5))

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=per_hour.tail(5).index, y=per_hour.tail(5)['cnt'], palette='Reds', ax=ax)
ax.set_title("Bottom 5 Hours with Lowest Usage")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Users")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)

st.markdown("""
### Kesimpulan:

- #### **Penggunaan sepeda berdasarkan musim dan cuaca:**  
  <p style="text-align: justify;">
  Penggunaan sepeda terbanyak terjadi pada musim gugur, diikuti oleh musim panas dan salju, sementara musim semi memiliki jumlah pengguna terendah. Kondisi cuaca juga berpengaruh signifikan terhadap jumlah pengguna, di mana cuaca cerah (kategori 1) memiliki jumlah pengguna tertinggi hampir mencapai 2 juta pengguna. Diikuti oleh cuaca mendung atau sedikit hujan (kategori 2) yang hampir menyentuh 1 juta dengan 996 ribu pengguna. Sedangkan kondisi cuaca buruk (kategori 3) memiliki jumlah pengguna yang sangat rendah yaitu hanya 37 ribu total pengguna.  
  </p>  

  <p style="text-align: justify;">
  Jika dilihat dari perbandingan musim, tidak ada perbedaan yang terlalu berarti untuk jumlah penggunanya. Musim gugur memiliki jumlah pengguna terbanyak yang mencapai angka 1 juta pengguna. Diikuti posisi kedua oleh musim panas sebanyak 900 ribu pengguna. Peringkat ketiga dimiliki oleh musim salju dengan perolehan jumlah pengguna sebanyak 840 ribu pengguna. Dan posisi terakhir musim semi yang hanya memiliki 470 ribu total pengguna.  
  </p>  

  <p style="text-align: justify;">
  Distribusi pengguna berdasarkan kombinasi musim dan cuaca menunjukkan bahwa pada setiap musim, cuaca cerah selalu mendominasi dalam menarik lebih banyak pengguna. Hal ini menunjukkan bahwa faktor cuaca dan musim secara langsung mempengaruhi tingkat penggunaan sepeda, dengan preferensi pengguna yang lebih tinggi saat cuaca lebih baik dan di musim yang lebih kondusif untuk aktivitas luar ruangan.  
  </p>  

- #### **Penggunaan sepeda berdasarkan jam:**  
  <p style="text-align: justify;">
  Dari analisis grafik, terlihat bahwa penggunaan layanan mencapai puncaknya pada pukul 8, 16, 17, 18, dan 19, yang kemungkinan besar terkait dengan jam kerja dan aktivitas commuting, terutama pukul 17-18 menjadi waktu tersibuk yang masing-masing mencapai 300 ribu jumlah pengguna dengan pukul 17 memiliki 30 ribu pengguna lebih banyak dari pukul 18.  
  </p>  

  <p style="text-align: justify;">
  Sebaliknya, penggunaan paling rendah terjadi pada pukul 1-5 pagi, dengan pukul 3 dan 4 yang bahkan tidak menyentuh angka 10 ribu. Pukul 4 hanya memiliki 4.400 pengguna dan pukul 3 dengan 8.174 total pengguna.
  </p>
""", unsafe_allow_html=True)

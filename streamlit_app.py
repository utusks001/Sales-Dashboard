import pandas as pd  # pip install pandas openpyxl --user
import numpy as np  # pip install numpy 
import plotly.express as px # pip install plotly-express --user
import plotly.graph_objects as go
import matplotlib.pyplot as plt # pip install matplotlib --user
from matplotlib.gridspec import GridSpec
import seaborn as sns # pip install seaborn --user
import streamlit as st  # pip install streamlit --user

st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Fungsi untuk membaca data dari file Excel
def read_excel_data():
    file_path = "financial_sample.xlsx"
    sheet_name = "Sales"
    nrows = 700
    df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=nrows)
    return df

# Membaca data dari file Excel
data = read_excel_data()

# def get_data_from_csv():
#     df = pd.read_csv("financials.csv", sep=";")  # Membaca CSV dengan delimiter koma
#     return df

# # Membaca data dari file CSV
# data = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

# Filter untuk negara
all_countries = data["Country"].unique()
country_selection = st.sidebar.checkbox("Select All Country", value=True)
if country_selection:
    selected_countries = all_countries
else:
    selected_countries = st.sidebar.multiselect("Select the Country:", options=all_countries, default=all_countries)

# Filter untuk segmen pelanggan
all_segments = data["Segment"].unique()
segment_selection = st.sidebar.checkbox("Select All Segment", value=True)
if segment_selection:
    selected_segments = all_segments
else:
    selected_segments = st.sidebar.multiselect("Select the Segment:", options=all_segments, default=all_segments)

# Filter untuk produk 
all_products = data["Product"].unique() 
product_selection = st.sidebar.checkbox("Select All Products", value=True)
if product_selection:
    selected_products = all_products
else:
    selected_products = st.sidebar.multiselect("Select the Product:", options=all_products, default=all_products)

# Pembersihan data untuk nilai non-numerik di kolom Profit
df_selection = data.copy()  # Buat salinan dataframe untuk diubah

# Ganti nilai non-numerik ("-") dengan NaN
df_selection["Profit"] = pd.to_numeric(df_selection["Profit"], errors="coerce")

# Hapus baris dengan NaN di kolom Profit
df_selection = df_selection.dropna(subset=["Profit"])

# Seleksi dataframe berdasarkan filter yang dipilih
df_selection = df_selection.query(
    "Country in @selected_countries & Segment in @selected_segments & Product in @selected_products"
)

# Add 'Bulan' column to dataframe
df_selection["Bulan"] = pd.to_datetime(df_selection["Date"], format='%Y-%m')

# Cek apakah dataframe kosong:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  # Ini akan menghentikan aplikasi dari eksekusi lebih lanjut.

# ---- MAINPAGE ----
st.title("Financial Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Sales"].sum() * 16500)  # Menghitung total sales 
average_sale_by_transaction = int(round(df_selection["Sales"].mean() * 16500))  # Menghitung rata-rata sales per transaksi
total_profit = int(df_selection["Profit"].sum() * 16500) # Menghitung total profit
presentasi = total_profit / total_sales * 100

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales :")
    st.subheader(f"Rp. {total_sales:,}")
with middle_column:
    st.subheader("Avg Sales/Transaction :")
    st.subheader(f"Rp. {average_sale_by_transaction:,}")
with right_column:
    st.subheader("Total Profit :")
    st.subheader(f"Rp. {total_profit:,} ({presentasi:.2f} %)")

st.markdown("""---""")

# SALES BY PRODUCT [BAR CHART]
sales_by_product_city = df_selection.groupby(by=["Product", "Country"])[["Sales"]].sum().reset_index()
fig_product_sales = px.bar(
    sales_by_product_city,
    y="Sales",
    x="Product",
    # orientation="h",
    title="<b>Sales by Product</b>",
    color="Country",
    template="plotly_white",
)
# Mengubah font dan ukuran judul
fig_product_sales.update_layout(
    title={
        'text': "<b>Sales by Product</b>",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,  # Ukuran font
            'family': 'Arial, sans-serif',  # Font yang digunakan
        }
    },
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# SALES BY MONTH [LINE CHART]
# Group by Month and Country, summing Sales
sales_by_hour_city = df_selection.groupby(by=["Bulan", "Country"])[["Sales"]].sum().reset_index()

# Create the line plot
fig_hourly_sales = px.line(
    sales_by_hour_city,
    x="Bulan",
    y="Sales",
    title="<b>Sales by Month</b>",
    color="Country",
    template="plotly_white",
)

# Customize layout
fig_hourly_sales.update_layout(
    title={
        'text': "<b>Sales by Month</b>",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,  # Ukuran font
            'family': 'Arial, sans-serif',  # Font yang digunakan
        }
    },
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# SALES BY SEGMENT [BAR CHART]
sales_by_payment = df_selection.groupby(by=["Segment","Country"])[["Sales"]].sum().reset_index()
fig_payment_sales = px.bar(
    sales_by_payment,
    x="Segment",
    y="Sales",
    color="Country",
    title="<b>Sales by Segment</b>",
    barmode="group",
    template="plotly_white",
)

# Mengubah font dan ukuran judul
fig_payment_sales.update_layout(
    title={
        'text': "<b>Sales by Segment</b>",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,  # Ukuran font
            'family': 'Arial, sans-serif',  # Font yang digunakan
        }
    },
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# SALES BY COUNTRY [PIE CHART]
sales_by_City = df_selection.groupby(by=["Country"])[["Sales"]].sum()
fig_City_sales = px.pie(
    sales_by_City,
    values="Sales",
    names=sales_by_City.index,
    title="<b>Sales by Country</b>",
    template="plotly_white",
)
# Mengubah font dan ukuran judul
fig_City_sales.update_layout(
    title={
        'text': "<b>Sales by Country</b>",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,  # Ukuran font
            'family': 'Arial, sans-serif',  # Font yang digunakan
        }
    },
    plot_bgcolor="rgba(0,0,0,0)",
)

# Mengatur posisi teks pada pie chart
fig_City_sales.update_traces(textposition="inside", textinfo="percent+label")

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_payment_sales, use_container_width=True)
right_column.plotly_chart(fig_City_sales, use_container_width=True)

st.markdown("""---""")

# Group data by Discount Band
grouped_discount = data.groupby('Discount Band').agg({'Sales': 'sum'})
grouped_discount = grouped_discount.sort_values(by='Sales', ascending=False)

# Membersihkan data: menghapus tanda kurung dan mengganti '-' dengan NaN
data[['Manufacturing Price', 'Sale Price', 'Sales', 'Profit']] = (
    data[['Manufacturing Price', 'Sale Price', 'Sales', 'Profit']]
    .replace('-', np.nan)
    .replace(r'\((.*?)\)', r'-\1', regex=True)
    .replace(',', '', regex=True)
    .astype(float)
)

# Menghitung korelasi
correlation = data[['Manufacturing Price', 'Sale Price', 'Sales', 'Profit']].corr()

# Membuat subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Mengubah background color pada figure
fig.patch.set_facecolor('#00172B')  # Ganti dengan warna latar belakang yang diinginkan

# Plot Sales by Discount Band
ax1.bar(grouped_discount.index, grouped_discount['Sales'], color='#E694FF', alpha=0.7)
ax1.set_title('Sales by Discount Band', fontsize=14, color='white')  # Warna judul
ax1.set_xlabel('Discount Band', fontsize=12, color='white')  # Warna label x-axis
ax1.set_ylabel('Sales', fontsize=12, color='white')  # Warna label y-axis
ax1.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
ax1.set_facecolor('#00172B')  # Background color pada ax1

# Mengubah warna tick labels pada x-axis dan y-axis
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')

# Mengubah warna sumbu x dan y
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.spines['top'].set_color('white')
ax1.spines['right'].set_color('white')

# Plot heatmap of correlation
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, ax=ax2, cbar_kws={"shrink": .8}, annot_kws={"color": "black"})
ax2.set_title('Correlation Heatmap', fontsize=14, color='white')  # Warna judul
ax2.set_facecolor('#00172B')  # Background color pada ax2

# Mengubah warna label pada heatmap
for text in ax2.get_xticklabels():
    text.set_color('white')
for text in ax2.get_yticklabels():
    text.set_color('white')

# Mengubah warna tick labels pada heatmap
ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')

# Mengubah warna sumbu x dan y pada heatmap
ax2.spines['bottom'].set_color('white')
ax2.spines['left'].set_color('white')
ax2.spines['top'].set_color('white')
ax2.spines['right'].set_color('white')

# Menambahkan grid pada heatmap
ax2.grid(linewidth=0.5, linestyle='--', color='gray')

# Menambahkan warna latar belakang pada figure
plt.subplots_adjust(wspace=0.4)
st.pyplot(fig)


# Create a new dataframe with total monthly profit for each product
data['Date'] = pd.to_datetime(data['Date'])
monthly_product_profit = data.groupby([data['Date'].dt.year, data['Date'].dt.month, 'Product']).agg({'Profit': 'sum'})
monthly_product_profit.index.names = ['Year', 'Month', 'Product']
monthly_product_profit.reset_index(inplace=True)

# Create a 'Year-Month' column for easier plotting
monthly_product_profit['Year-Month'] = pd.to_datetime(monthly_product_profit[['Year', 'Month']].assign(day=1))

# Create a pivot table of 'Profit' with 'Product' and 'Discount Band' as dimensions
product_discount_profit = data.pivot_table(values='Profit', index='Product', columns='Discount Band', aggfunc='sum')

# Membuat subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot monthly profit for each product
for product in monthly_product_profit['Product'].unique():
    product_data = monthly_product_profit[monthly_product_profit['Product'] == product]
    ax1.plot(product_data['Year-Month'], product_data['Profit'], label=product)
ax1.set_title('Monthly Profit by Product', fontsize=14, color='white')
ax1.set_xlabel('Date', fontsize=12, color='white')
ax1.set_ylabel('Profit', fontsize=12, color='white')
ax1.legend()
ax1.grid()
ax1.set_facecolor('#00172B')

# Mengubah warna tick labels pada x-axis dan y-axis
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')

# Mengubah warna sumbu x dan y
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.spines['top'].set_color('white')
ax1.spines['right'].set_color('white')

# Plot a heatmap of the pivot table
sns.heatmap(product_discount_profit, annot=True, fmt='.0f', cmap='viridis', ax=ax2)
ax2.set_title('Profit across Products and Discount Bands', fontsize=14, color='white')

# Mengubah warna label pada heatmap
for text in ax2.get_xticklabels():
    text.set_color('white')
for text in ax2.get_yticklabels():
    text.set_color('white')

# Mengubah warna tick labels pada heatmap
ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')

# Mengubah warna sumbu x dan y pada heatmap
ax2.spines['bottom'].set_color('white')
ax2.spines['left'].set_color('white')
ax2.spines['top'].set_color('white')
ax2.spines['right'].set_color('white')

# Menambahkan grid pada heatmap
ax2.grid(linewidth=0.5, linestyle='--', color='gray')

# Mengubah background color pada figure
fig.patch.set_facecolor('#00172B')

# Menampilkan plot di Streamlit
st.pyplot(fig)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

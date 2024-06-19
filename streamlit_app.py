import pandas as pd  # pip install pandas openpyxl --user
import numpy as np  # pip install numpy 
import plotly.express as px # pip install plotly-express --user
import plotly.graph_objects as go
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

# Add 'Bulan' column to dataframe
df_selection["Bulan"] = pd.to_datetime(df_selection["Date"], format='%Y-%m')

# Seleksi dataframe berdasarkan filter yang dipilih
df_selection = df_selection.query(
    "Country in @selected_countries & Segment in @selected_segments & Product in @selected_products"
)

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

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

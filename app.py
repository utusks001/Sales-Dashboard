import pandas as pd  # pip install pandas openpyxl --user
import numpy as np  # pip install numpy 
import plotly.express as px # pip install plotly-express --user
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit --user

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# # ---- SIDEBAR ----
# st.sidebar.header("Please Filter Here:")
# city = st.sidebar.multiselect(
#     "Select the City:",
#     options=df["City"].unique(),
#     default=df["City"].unique()
# )

# customer_type = st.sidebar.multiselect(
#     "Select the Customer Type:",
#     options=df["Customer_type"].unique(),
#     default=df["Customer_type"].unique(),
# )

# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

# df_selection = df.query(
#     "City == @city & Customer_type ==@customer_type & Gender == @gender"
# )

# # Check if the dataframe is empty:
# if df_selection.empty:
#     st.warning("No data available based on the current filter settings!")
#     st.stop() # This will halt the app from further execution.

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

all_cities = df["City"].unique()
city_selection = st.sidebar.checkbox("Select All Cities", value=True)
if city_selection:
    selected_cities = all_cities
else:
    selected_cities = st.sidebar.multiselect("Select the City:", options=all_cities, default=all_cities)

all_customer_types = df["Customer_type"].unique()
customer_type_selection = st.sidebar.checkbox("Select All Customer Types", value=True)
if customer_type_selection:
    selected_customer_types = all_customer_types
else:
    selected_customer_types = st.sidebar.multiselect("Select the Customer Type:", options=all_customer_types, default=all_customer_types)

all_genders = df["Gender"].unique()
gender_selection = st.sidebar.checkbox("Select All Genders", value=True)
if gender_selection:
    selected_genders = all_genders
else:
    selected_genders = st.sidebar.multiselect("Select the Gender:", options=all_genders, default=all_genders)

df_selection = df.query(
    "City in @selected_cities & Customer_type in @selected_customer_types & Gender in @selected_genders"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title("Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
total_sales = total_sales * 16500
average_sale_by_transaction = int(round(df_selection["Total"].mean()))
average_sale_by_transaction = average_sale_by_transaction * 16500
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"Rp. {total_sales:,}")
with middle_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"Rp. {average_sale_by_transaction}")
with right_column:
    st.subheader("Average Rating:")
    st.subheader(f"{int(average_rating)}/10 {star_rating}")

st.markdown("""---""")

# # SALES BY PRODUCT LINE [BAR CHART]
# sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
# fig_product_sales = px.bar(
#     sales_by_product_line,
#     x="Total",
#     y=sales_by_product_line.index,
#     orientation="h",
#     title="<b>Sales by Product Line</b>",
#     color_discrete_sequence=["#005F85"] * len(sales_by_product_line),
#     template="plotly_white",
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_city = df_selection.groupby(by=["Product line", "City"])[["Total"]].sum().reset_index()
fig_product_sales = px.bar(
    sales_by_product_city,
    x="Total",
    y="Product line",
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color="City",
    template="plotly_white",
)
# Mengubah font dan ukuran judul
fig_product_sales.update_layout(
    title={
        'text': "<b>Sales by Product Line</b>",
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

# # SALES BY HOUR [LINE CHART]
# sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum().reset_index()
# fig_hourly_sales = px.line(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by Hour</b>",
#     color_discrete_sequence=["#0027B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )

# SALES BY HOUR [LINE CHART]
sales_by_hour_city = df_selection.groupby(by=["hour", "City"])[["Total"]].sum().reset_index()
fig_hourly_sales = px.line(
    sales_by_hour_city,
    x="hour",
    y="Total",
    title="<b>Sales by Hour</b>",
    color="City",
    template="plotly_white",
)
# Mengubah font dan ukuran judul
fig_hourly_sales.update_layout(
    title={
        'text': "<b>Sales by Hour</b>",
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

# SALES BY PAYMENT [BAR CHART]
sales_by_payment = df_selection.groupby(by=["Payment","City"])[["Total"]].sum().reset_index()
fig_payment_sales = px.bar(
    sales_by_payment,
    x="Payment",
    y="Total",
    color="City",
    title="<b>Sales by Payment</b>",
    barmode="group",
    template="plotly_white",
)
# fig_payment_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=dict(showgrid=False),
# )
# Mengubah font dan ukuran judul
fig_payment_sales.update_layout(
    title={
        'text': "<b>Sales by Payment</b>",
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

# SALES BY CITY [PIE CHART]
sales_by_City = df_selection.groupby(by=["City"])[["Total"]].sum()
fig_City_sales = px.pie(
    sales_by_City,
    values="Total",
    names=sales_by_City.index,
    title="<b>Sales by City</b>",
    template="plotly_white",
)
# Mengubah font dan ukuran judul
fig_City_sales.update_layout(
    title={
        'text': "<b>Sales by City</b>",
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

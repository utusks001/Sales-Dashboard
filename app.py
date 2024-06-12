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

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
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
average_sale_by_transaction = round(df_selection["Total"].mean())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US$ {total_sales:,}")
with middle_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US$ {average_sale_by_transaction}")
with right_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#005F85"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [LINE CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.line(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#0027B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("""---""")

# SALES BY PAYMENT [BAR CHART]
sales_by_payment = df_selection.groupby(by=["Payment"])[["Total"]].sum().sort_values(by="Total")
fig_payment_sales = px.bar(
    sales_by_payment,
    y="Total",
    x=sales_by_payment.index,
    title="<b>Sales by Payment</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_payment),
    template="plotly_white",
)
fig_payment_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# SALES BY CITY [PIE CHART]
sales_by_City = df_selection.groupby(by=["City"])[["Total"]].sum()
fig_City_sales = px.pie(
    sales_by_City,
    values="Total",
    names=sales_by_City.index,
    title="<b>Sales by City</b>",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig_branch_sales.update_traces(textposition="inside", textinfo="percent+label")

# Tambahkan layout atau konfigurasi tambahan jika diperlukan
fig_branch_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_payment_sales, use_container_width=True)
right_column.plotly_chart(fig_branch_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

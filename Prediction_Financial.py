import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX


# Fungsi untuk membaca data dari file Excel
# @st.cache
def load_data(file_path):
    return pd.read_excel(file_path, parse_dates=['Date'])

# Load data
df = load_data('financial_sample.xlsx')

# Menampilkan beberapa baris pertama dari data
st.write("Dataframe Head:", df.head())

# Menampilkan beberapa baris pertama dari data
st.write("Dataframe Tail:", df.tail())

# Mengatur index pada kolom Date
df.set_index('Date', inplace=True)

# Mengubah kolom Sales dan Profit menjadi numerik (jika tidak sudah numerik)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')

# Menghapus baris dengan nilai NaN
df.dropna(subset=['Sales', 'Profit'], inplace=True)

# Resampling data berdasarkan bulan untuk penjualan dan profit
monthly_sales = df['Sales'].resample('M').sum()
monthly_profit = df['Profit'].resample('M').sum()

# Menampilkan data penjualan dan profit bulanan
st.write("Monthly Sales:", monthly_sales.head())
st.write("Monthly Profit:", monthly_profit.head())

# Fungsi untuk membangun dan melatih model ARIMA
def build_and_train_model(data):
    train = data[:int(0.8 * len(data))]
    test = data[int(0.8 * len(data)):]
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    return results, test

# Membangun dan melatih model ARIMA untuk penjualan
sales_model, sales_test = build_and_train_model(monthly_sales)
profit_model, profit_test = build_and_train_model(monthly_profit)

# Melakukan prediksi
sales_predictions = sales_model.get_forecast(steps=len(sales_test))
sales_predicted_mean = sales_predictions.predicted_mean
sales_predicted_conf_int = sales_predictions.conf_int()

profit_predictions = profit_model.get_forecast(steps=len(profit_test))
profit_predicted_mean = profit_predictions.predicted_mean
profit_predicted_conf_int = profit_predictions.conf_int()

# Menampilkan hasil prediksi penjualan
fig, ax = plt.subplots(2, 1, figsize=(10, 10))

# Plot untuk prediksi penjualan
ax[0].plot(monthly_sales.index, monthly_sales, label='Actual Sales', color='gray')
ax[0].plot(sales_predicted_mean.index, sales_predicted_mean, label='Predicted Sales', color='red')
ax[0].fill_between(sales_predicted_conf_int.index,
                   sales_predicted_conf_int.iloc[:, 0],
                   sales_predicted_conf_int.iloc[:, 1], color='red', alpha=0.2)
ax[0].set_title('Sales Prediction')
ax[0].set_xlabel('Date')
ax[0].set_ylabel('Sales')
ax[0].legend()
ax[0].grid()

# Plot untuk prediksi profit
ax[1].plot(monthly_profit.index, monthly_profit, label='Actual Profit', color='gray')
ax[1].plot(profit_predicted_mean.index, profit_predicted_mean, label='Predicted Profit', color='brown')
ax[1].fill_between(profit_predicted_conf_int.index,
                   profit_predicted_conf_int.iloc[:, 0],
                   profit_predicted_conf_int.iloc[:, 1], color='brown', alpha=0.2)
ax[1].set_title('Profit Prediction')
ax[1].set_xlabel('Date')
ax[1].set_ylabel('Profit')
ax[1].legend()
ax[1].grid()

# Menampilkan plot prediksi di Streamlit
st.pyplot(fig)

# Menampilkan metrik evaluasi untuk penjualan
st.write("Sales Mean Absolute Error (MAE):", np.mean(np.abs(sales_predicted_mean - sales_test)))
st.write("Sales Root Mean Squared Error (RMSE):", np.sqrt(np.mean((sales_predicted_mean - sales_test) ** 2)))

# Menampilkan metrik evaluasi untuk profit
st.write("Profit Mean Absolute Error (MAE):", np.mean(np.abs(profit_predicted_mean - profit_test)))
st.write("Profit Root Mean Squared Error (RMSE):", np.sqrt(np.mean((profit_predicted_mean - profit_test) ** 2)))

# Memprediksi penjualan dan profit masa depan 12 bulan berikutnya
future_steps = 12  # Mengatur jumlah bulan yang ingin diprediksi
future_sales_predictions = sales_model.get_forecast(steps=future_steps)
future_sales_mean = future_sales_predictions.predicted_mean
future_sales_conf_int = future_sales_predictions.conf_int()

# Melakukan prediksi untuk profit masa depan 12 bulan berikutnya
future_profit_predictions = profit_model.get_forecast(steps=future_steps)
future_profit_mean = future_profit_predictions.predicted_mean
future_profit_conf_int = future_profit_predictions.conf_int()

# Membuat DataFrame dari hasil prediksi
future_dates = pd.date_range(start=monthly_sales.index[-1], periods=future_steps, freq='M') + pd.Timedelta(days=1)
future_df = pd.DataFrame({
    'Date': future_dates,
    'Predicted Sales': future_sales_mean.values,
    'Predicted Profit': future_profit_mean.values
})

# # Menyimpan DataFrame ke Excel
# file_name = 'prediction_results.xlsx'  # Nama file Excel untuk disimpan
# future_df.to_excel(file_name, index=False)


# Menampilkan prediksi penjualan dan profit masa depan
fig, ax = plt.subplots(2, 1, figsize=(10, 10))

# Plot untuk prediksi penjualan masa depan
ax[0].plot(monthly_sales.index, monthly_sales, label='Historical Sales')
ax[0].plot(future_sales_mean.index, future_sales_mean, label='Future Sales Predictions', color='red')
ax[0].fill_between(future_sales_conf_int.index,
                   future_sales_conf_int.iloc[:, 0],
                   future_sales_conf_int.iloc[:, 1], color='red', alpha=0.2)
ax[0].set_title('Future Sales Prediction')
ax[0].set_xlabel('Date')
ax[0].set_ylabel('Sales')
ax[0].legend()
ax[0].grid()

# Plot untuk prediksi profit masa depan
ax[1].plot(monthly_profit.index, monthly_profit, label='Historical Profit')
ax[1].plot(future_profit_mean.index, future_profit_mean, label='Future Profit Predictions', color='brown')
ax[1].fill_between(future_profit_conf_int.index,
                   future_profit_conf_int.iloc[:, 0],
                   future_profit_conf_int.iloc[:, 1], color='brown', alpha=0.2)
ax[1].set_title('Future Profit Prediction')
ax[1].set_xlabel('Date')
ax[1].set_ylabel('Profit')
ax[1].legend()
ax[1].grid()

# Menampilkan plot prediksi masa depan di Streamlit
st.pyplot(fig)

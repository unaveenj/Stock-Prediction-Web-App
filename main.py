import streamlit as st
import yfinance as yf
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

df = pd.read_csv("nasdaq_screener_1627469879819.csv")

START_DATE = "2015-01-01"
TODAY_DATE = date.today().strftime('%Y-%m-%d')
# st.write(TODAY_DATE)
#Title of webapp
st.title("Stock predictor")

stocks = tuple(df['Symbol'])
stock_name = tuple(df['Name'])
# print(stocks)
select_stocks = st.selectbox("Select stock for prediction",stocks)
selected_name = stock_name[stocks.index(select_stocks)]
st.text(f"{selected_name}")
n_years=st.slider("Years of prediction:", 1,4)
period = n_years * 365

@st.cache
def load_stock_data(ticker):
    data=yf.download(ticker,START_DATE,TODAY_DATE)
    data.reset_index(inplace=True)
    return data
data_load_state = st.text("Load data...")
data = load_stock_data(select_stocks)
data_load_state.text("Loading data done !!!")
# data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')
st.subheader("Statistics")
st.write(data)


def plot_graph():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'], name='Stock open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'], name='Stock close'))
    fig.layout.update(title_text="Time Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_graph()

# Forecasting

df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date":"ds","Close":"y"})

model=Prophet()
model.fit(df_train)
predictions = model.make_future_dataframe(periods=period)
forecast = model.predict(predictions)
# forecast['ds'] = forecast['ds'].dt.strftime('%d-%m-%Y')
st.subheader("Forecast Data")
st.write(forecast)

fig1=plot_plotly(model,forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2=model.plot_components(forecast)
st.write(fig2)
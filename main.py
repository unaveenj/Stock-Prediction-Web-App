import streamlit as st
import yfinance as yf
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import difflib

file_name='style.css'
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)




@st.cache
def load_stock_data(ticker):
    data=yf.download(ticker,START_DATE,TODAY_DATE)
    data.reset_index(inplace=True)
    return data

def plot_graph():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'], name='Stock open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'], name='Stock close'))
    fig.layout.update(title_text="Time Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_candlestick(data):
    #Make the dates as index
    data = data.set_index(pd.DatetimeIndex(data['Date'].values))
    figure = go.Figure(data=[go.Candlestick(
        x=data.index,
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        open=data['Open'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    figure.update_layout(
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False)
    # width=900,height=700)
    st.plotly_chart(figure)






START_DATE = "2015-01-01"
TODAY_DATE = date.today().strftime('%Y-%m-%d')
# st.write(TODAY_DATE)
#Title of webapp
st.title("Stock predictor")
st.sidebar.info("Choose US stocks or ETFs")
selection=['US','ETF','Crypto']
main_selection=st.sidebar.selectbox('Select US stock or ETF',selection)
st.sidebar.text("Credits to : @python-engineer tutorial")

#Telegram bot
# st.sidebar.image('https://i.ibb.co/5YBks9z/tele.png', width=200)
st.sidebar.text("Telegram bot available")
st.sidebar.markdown('[![this is an image link](https://i.ibb.co/Rp7XGt7/tele-small.jpg)](https://t.me/GaneshTutorial_bot)',unsafe_allow_html=True)
st.sidebar.text('Authors: \n1. @unaveenj - Web App\n2. @ssganesh- Telegram bot ')

if main_selection=='US':
    df = pd.read_csv("nasdaq_screener_1627469879819.csv")
    st.header("US Stocks!")
    stocks = tuple(df['Symbol'])
    stock_name = tuple(df['Name'])
    # print(stocks)
    # select_stocks = st.selectbox("Select stock for prediction",stocks)
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    st.text("Search for stock below")
    select_stocks = st.text_input("", "").upper()
    button_clicked = st.button("OK")
    if select_stocks in stocks:
        selected_name = stock_name[stocks.index(select_stocks)]
        st.text(f"{selected_name}")
        period=st.slider("Number of days:", 1,4*365)



        data_load_state = st.text("Load data...")
        data = load_stock_data(select_stocks)
        data_load_state.text("Loading data done !!!")
        check = st.checkbox('Click here for candlestick chart')
        if check:
            plot_candlestick(data)
        # data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')
        st.subheader("Statistics")
        st.write(data)



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

    elif select_stocks=="":
        st.warning("Please search for your stock")
    elif select_stocks not in stocks:
        error = difflib.get_close_matches(select_stocks, stocks)

        if len(error)==0 :
            st.warning("Stock doesn't exist in database")
        else:
            st.warning(f"Did u mean : {error}")


elif main_selection=='Crypto':
    df = pd.read_csv("crypto.csv")
    st.header("Crypto!")
    stocks = tuple(df['Symbol'])
    stock_name = tuple(df['Name'])
    # print(stocks)
    # select_stocks = st.selectbox("Select stock for prediction",stocks)
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    st.text("Search for crypto below")
    select_stocks = st.text_input("", "").upper()
    button_clicked = st.button("OK")
    select_stocks = select_stocks+'-USD'
    if select_stocks in stocks:
        selected_name = stock_name[stocks.index(select_stocks)]
        st.text(f"{selected_name}")
        period=st.slider("Number of days:", 1,4*365)



        data_load_state = st.text("Load data...")
        data = load_stock_data(select_stocks)
        data_load_state.text("Loading data done !!!")
        check = st.checkbox('Click here for candlestick chart')
        if check:
            plot_candlestick(data)
        # data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')
        st.subheader("Statistics")
        st.write(data)



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

    elif select_stocks=="-USD":
        st.warning("Please search for your crypto")
    elif select_stocks not in stocks:
        error = difflib.get_close_matches(select_stocks, stocks)

        if len(error)==0 :
            st.warning("Crypto doesn't exist in database")
        else:
            st.warning(f"Did u mean : {error}")


elif main_selection=='ETF':
    df = pd.read_csv("etfs.csv")
    st.header("US ETFs!")
    stocks = tuple(df['Symbol'])
    stock_name = tuple(df['Name'])
    # print(stocks)
    # select_stocks = st.selectbox("Select stock for prediction",stocks)
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    st.text("Search for ETFs below")
    select_stocks = st.text_input("", "").upper()
    button_clicked = st.button("OK")
    if select_stocks in stocks:
        selected_name = stock_name[stocks.index(select_stocks)]
        st.text(f"{selected_name}")
        period = st.slider("Number of days:", 1, 4 * 365)

        data_load_state = st.text("Load data...")
        data = load_stock_data(select_stocks)
        data_load_state.text("Loading data done !!!")
        check = st.checkbox('Click here for candlestick chart')
        if check:
            plot_candlestick(data)
        # data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')
        st.subheader("Statistics")
        st.write(data)

        plot_graph()

        # Forecasting

        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        model = Prophet()
        model.fit(df_train)
        predictions = model.make_future_dataframe(periods=period)
        forecast = model.predict(predictions)
        # forecast['ds'] = forecast['ds'].dt.strftime('%d-%m-%Y')
        st.subheader("Forecast Data")
        st.write(forecast)

        fig1 = plot_plotly(model, forecast)
        st.plotly_chart(fig1)

        st.write("Forecast components")
        fig2 = model.plot_components(forecast)
        st.write(fig2)

    elif select_stocks == "":
        st.warning("Please search for your ETF")
    elif select_stocks not in stocks:
        error = difflib.get_close_matches(select_stocks, stocks)

        if len(error) == 0:
            st.warning("ETF doesn't exist in database")
        else:
            st.warning(f"Did u mean : {error}")
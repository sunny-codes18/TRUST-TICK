import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
import pyttsx3
import time

# using pyttsx3 for voice engine
def greet_user_once():
    if 'greeted' not in st.session_state:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.setProperty("rate", 150)
        engine.say("Welcome to Trust Tick.")
        engine.runAndWait()
        time.sleep(0.2)
        engine.say("Your secure market insight engine.")
        engine.runAndWait()
        st.session_state['greeted'] = True

greet_user_once()

# Title and Tagline
st.title(" TRUST✔️ Stock Price Analyzer with Moving Averages")
st.info("Track trends. Trust the data. Tick the right stocks.")

# providing the tickers list of some popular company
popular_tickers = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Netflix (NFLX)": "NFLX",
    "Meta (META)": "META",
    "Nvidia (NVDA)": "NVDA",
    "Tata Consultancy (TCS.NS)": "TCS.NS",
    "Reliance Industries (RELIANCE.NS)": "RELIANCE.NS",
    "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS",
    "ICICI Bank (ICICIBANK.NS)": "ICICIBANK.NS",
    "Infosys (INFY.NS)": "INFY.NS",
    "TCS (TCS.NS)": "TCS.NS",
    "Larsen & Toubro (LT.NS)": "LT.NS",
    "Kotak Mahindra Bank (KOTAKBANK.NS)": "KOTAKBANK.NS",
    "Axis Bank (AXISBANK.NS)": "AXISBANK.NS",
    "State Bank of India (SBIN.NS)": "SBIN.NS",
    "HCL Technologies (HCLTECH.NS)": "HCLTECH.NS",
    "Bharti Airtel (BHARTIARTL.NS)": "BHARTIARTL.NS",
    "Bajaj Finance (BAJFINANCE.NS)": "BAJFINANCE.NS",
    "ITC (ITC.NS)": "ITC.NS",
    "Wipro (WIPRO.NS)": "WIPRO.NS",
    "Asian Paints (ASIANPAINT.NS)": "ASIANPAINT.NS",
    "Maruti Suzuki (MARUTI.NS)": "MARUTI.NS",
    "UltraTech Cement (ULTRACEMCO.NS)": "ULTRACEMCO.NS",
    "Nestle India (NESTLEIND.NS)": "NESTLEIND.NS",
    "Titan Company (TITAN.NS)": "TITAN.NS",
    "Tech Mahindra (TECHM.NS)": "TECHM.NS",
    "Sun Pharma (SUNPHARMA.NS)": "SUNPHARMA.NS",
    "Hindustan Unilever (HINDUNILVR.NS)": "HINDUNILVR.NS",
    "JSW Steel (JSWSTEEL.NS)": "JSWSTEEL.NS",
    "Tata Motors (TATAMOTORS.NS)": "TATAMOTORS.NS",
    "Grasim Industries (GRASIM.NS)": "GRASIM.NS",
    "Hindalco Industries (HINDALCO.NS)": "HINDALCO.NS",
    "Bajaj Finserv (BAJAJFINSV.NS)": "BAJAJFINSV.NS",
    "NTPC (NTPC.NS)": "NTPC.NS",
    "Adani Enterprises (ADANIENT.NS)": "ADANIENT.NS",
    "Adani Ports (ADANIPORTS.NS)": "ADANIPORTS.NS",
    "Coal India (COALINDIA.NS)": "COALINDIA.NS",
    "Power Grid Corporation (POWERGRID.NS)": "POWERGRID.NS",
    "Eicher Motors (EICHERMOT.NS)": "EICHERMOT.NS",
    "Divi's Laboratories (DIVISLAB.NS)": "DIVISLAB.NS",
    "Dr Reddy's Labs (DRREDDY.NS)": "DRREDDY.NS",
    "Tata Steel (TATASTEEL.NS)": "TATASTEEL.NS",
    "HDFC Life Insurance (HDFCLIFE.NS)": "HDFCLIFE.NS",
    "Bajaj Auto (BAJAJ-AUTO.NS)": "BAJAJ-AUTO.NS",
    "Britannia Industries (BRITANNIA.NS)": "BRITANNIA.NS",
    "Cipla (CIPLA.NS)": "CIPLA.NS",
    "Hero MotoCorp (HEROMOTOCO.NS)": "HEROMOTOCO.NS",
    "IndusInd Bank (INDUSINDBK.NS)": "INDUSINDBK.NS",
    "Apollo Hospitals (APOLLOHOSP.NS)": "APOLLOHOSP.NS",
    "SBI Life Insurance (SBILIFE.NS)": "SBILIFE.NS",
    "Tata Consumer Products (TATACONSUM.NS)": "TATACONSUM.NS",
    "BPCL (BPCL.NS)": "BPCL.NS",
    "UPL Ltd (UPL.NS)": "UPL.NS",
    "Shriram Finance (SHRIRAMFIN.NS)": "SHRIRAMFIN.NS",
    "Jio Financial Services (JIOFIN.NS)": "JIOFIN.NS",
    "ONGC (ONGC.NS)": "ONGC.NS",
    "Mahindra & Mahindra (M&M.NS)": "M&M.NS"

}
# select tickter
selected_label = st.selectbox("Choose a stock to analyze:", list(popular_tickers.keys()))
ticker = popular_tickers[selected_label]

# To enter the ticktter manullay if not present in list 
if st.checkbox("Want to enter ticker manually?"):
    ticker = st.text_input("Enter your stock ticker (e.g., INFY.NS or AAPL):", ticker).upper()

# selecting the starting date and ending date
starting_date = st.date_input(" Enter the starting date for analysis:", value=date(2024, 1, 1))
ending_date = st.date_input(" Enter the date up to which you want analysis:", value=date.today())

# Analyzing button 
if st.button("Analyze"):
    if starting_date >= ending_date:
        st.error("🔺 The end date must be after the start date.")
    else:
        
        data = yf.download(ticker, start=starting_date, end=ending_date)

        if data.empty:
            st.warning(f"No data found for ticker '{ticker}'. Please try again.")
        else:
            
            company_name = yf.Ticker(ticker).info.get('longName', ticker)
            st.subheader(f"📊Performing analysis for: **{company_name}**")

            
            data['MA50'] = data['Close'].rolling(window=50).mean()
            data['MA100'] = data['Close'].rolling(window=100).mean()
            data = data.dropna()  

            
            st.dataframe(data.tail())

            #plotting graph with Moving average of 50 days and 100 days for better understanding
            st.subheader("Price Chart with Moving Averages")
            fig, ax = plt.subplots(figsize=(14, 7))
            ax.plot(data['Close'], label='Closing Price', linewidth=2)
            ax.plot(data['MA50'], label='50-Day MA', linestyle='--')
            ax.plot(data['MA100'], label='100-Day MA', linestyle=':')
            ax.set_title(f"{company_name} ({ticker}) Stock Analysis")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price in USD")
            ax.legend()
            ax.grid(True)
            plt.tight_layout()
            st.pyplot(fig)

            # Diclaimer
            st.markdown("---")
            st.markdown("**Disclaimer:**")
            st.info(" Investment suggestions are generated based on market trends and technical data (like moving averages).") 
            st.info("Please use your own judgment or consult a financial advisor before making investment decisions.")
             
            #Investment suggestion
            st.subheader("Investment Suggestion")
            ma50 = data['MA50'].iloc[-1]
            ma100 = data['MA100'].iloc[-1]


            if ma50 > ma100:
                st.success("🟢 The 50-day trend is stronger than the 100-day trend. It might be a **good time to invest**.")
            elif ma50 < ma100:
                st.warning("🚨 The short-term trend is weaker than the long-term trend. Avoid investing!.")
            else:
                st.info(" The market trend is neutral. 🟡 Hold — wait for a clearer signal to invest..")


            st.subheader("Copyright")
            st.info("Copyright © 2025 sunny mishra All rights reserved." \
            "This software and its source code are the intellectual property of sunny mishra" \
            "  and may not be copied,modified,distributed,or used in any form without explicit written permission." \
            "Unauthorized use is strictly prohibited and will be legally prosecuted. ")

                    

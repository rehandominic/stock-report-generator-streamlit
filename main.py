import yfinance as yf
import streamlit as st
import pandas as pd
import json

st.set_page_config(layout='wide')
st.title("Comprehensive Stock Report Generator")
st.write(""" 
#### Enter the ticker of the Stock whose Comprehensive report you want to generate.
""")

tickerSymbol = st.text_input('Stock Ticker', 'MSFT')



if st.button('Create Report'):


    tickerData = yf.Ticker(tickerSymbol)
    ticker_info = tickerData.info
    valuation = "{:,}".format(ticker_info['enterpriseValue'])
    employees = "{:,}".format(ticker_info['fullTimeEmployees'])
    ebitda = "{:,}".format(ticker_info['ebitda'])
    grossProfits = "{:,}".format(ticker_info['grossProfits'])
    freeCashflow = "{:,}".format(ticker_info['freeCashflow'])
    sector = ticker_info['sector']
    price = ticker_info['currentPrice']
    logo_url = ticker_info['logo_url']
    open = ticker_info['open']
    percentChange = (((price - open)/open)*100)
    ticker_financials = tickerData.recommendations

    hcol1, hcol2, hcol3 = st.columns([5, 1, 2])

    hcol1.write("""
    # Comprehensive Report of {}
    """.format(ticker_info['longName']))

    # hcol1.write("""
    # ### Sector : **{}**     |   Ticker :  **{}**
    # """.format(sector, tickerSymbol))

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Sector", "{}".format(sector))
    col2.metric("Ticker", "{}".format(tickerSymbol))
    col3.metric("Price", "${}".format(price), round(percentChange, 2))

    hcol3.image(logo_url, width=100)

    col1, col2, col3 = st.columns([5, 1, 2])

    col1.write("""
    ## Overview
    """)
    col1.write(ticker_info['longBusinessSummary'])

    with col3:

        st.write("""
            ## Key Numbers
            """)

        st.write("""
            #### Valuation :  ${} 
            """.format(valuation))

        st.write("""
            #### EBITDA :  ${} 
            """.format(ebitda))

        st.write("""
            #### Gross Profit :  ${} 
            """.format(grossProfits))

        st.write("""
                    #### Free Cashflow :  ${} 
                    """.format(freeCashflow))

        st.write("""
                #### Employees :  {} People
                """.format(employees))


    tickerDF = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
    chart_col1, chart_col2 = st.columns(2)
    chart_col1.write("""
        ### Closing Price
        """)
    chart_col1.line_chart(tickerDF.Close)
    chart_col2.write("""
        ### Volume
        """)
    chart_col2.line_chart(tickerDF.Volume)

    st.write(ticker_financials)

    # for key, values in ticker_info.items():
    #     st.write(key, values)
    #st.write(ticker_info['sector'])


# tickerSymbol = 'GOOGL'
#

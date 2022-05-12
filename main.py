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

    ebitdaMargin = round(ticker_info['ebitdaMargins']*100, 1)
    grossMargin = round(ticker_info['grossMargins']*100, 1)
    profitMargin = round(ticker_info['profitMargins']*100, 1)
    revenueGrowth = round(ticker_info['revenueGrowth']*100, 1)
    earningsGrowth = round(ticker_info['earningsGrowth']*100, 1)
    recommendationKey = ticker_info['recommendationKey'].capitalize()

    quickRatio = round(ticker_info['quickRatio'], 1)
    currentRatio = round(ticker_info['currentRatio'], 1)
    shortRatio = round(ticker_info['shortRatio'], 1)
    try:
        beta = round(ticker_info['beta'], 1)
    except:
        beta = ticker_info['beta']
    pegRatio = round(ticker_info['pegRatio'], 1)
    payoutRatio = round(ticker_info['payoutRatio'], 1)

    debttoequity = round(ticker_info['debtToEquity'], 1)
    roe = round(ticker_info['returnOnEquity'], 1)
    roa = round(ticker_info['returnOnAssets'], 1)
    forwardpe = round(ticker_info['forwardPE'], 1)
    trailingpe = round(ticker_info['trailingPE'], 1)
    bookValue = round(ticker_info['bookValue'], 1)


    ticker_recommendations = tickerData.recommendations
    ticker_financials = tickerData.financials
    ticker_dividends = tickerData.dividends
    ticker_cashflow = tickerData.cashflow
    ticker_bs = tickerData.balance_sheet

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

    st.write("""
    ## Key Financial Indicators
    """)

    tcol1, tcol2, tcol3, tcol4, tcol5, tcol6 = st.columns(6)

    tcol1.metric("EBITDA Margin", "{}%".format(ebitdaMargin))
    tcol2.metric("Profit Margin", "{}%".format(profitMargin))
    tcol3.metric("Gross Margin", "{}%".format(grossMargin))
    tcol4.metric("Revenue Growth", "{}%".format(revenueGrowth))
    tcol5.metric("Earnings Growth", "{}%".format(earningsGrowth))
    tcol6.metric("Analyst Recommendation", "{}".format(recommendationKey))


    tcol1.metric("Quick Ratio", "{}".format(quickRatio))
    tcol2.metric("Current Ratio", "{}".format(currentRatio))
    tcol3.metric("Short Ratio", "{}".format(shortRatio))
    tcol4.metric("Beta", "{}".format(beta))
    tcol5.metric("Price to Earnings Growth Ratio", "{}".format(pegRatio))
    tcol6.metric("Payout Ratio", "{}".format(payoutRatio))


    tcol1.metric("Debt to Equity Ratio", "{}".format(debttoequity))
    tcol2.metric("ROE", "{}".format(roe))
    tcol3.metric("ROA", "{}".format(roa))
    tcol4.metric("Forward PE Ratio", "{}".format(forwardpe))
    tcol5.metric("Trailing PE Ratio", "{}".format(trailingpe))
    tcol6.metric("Book Value", "{}".format(bookValue))

    st.write("""
    ##
    """)

    tickerDF = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
    chart_col1, chart_col2 = st.columns(2)
    chart_col1.write("""
        ## Price Trend
        """)
    chart_col1.line_chart(tickerDF.Close)
    chart_col2.write("""
        ## Volume Trend
        """)
    chart_col2.line_chart(tickerDF.Volume)

    ch_col1, ch_col2 = st.columns(2)

    ch_col1.write("""
        ## Major Analysts Recommendation
        """)
    rec = ticker_recommendations.groupby(['To Grade'])['To Grade'].count().reset_index(drop=True)
    recDF = rec.to_frame()

    rec2 = ticker_recommendations.groupby(['To Grade'])['To Grade'].count()
    df_final = rec2.to_frame()
    df_final.index.names = ['Grade_names']
    reclist = list(df_final.index)

    column_names = reclist
    recDF['Label'] = column_names
    new_recDF = recDF.iloc[:, [1,0]]
    new_recDF.reset_index(drop=True, inplace=True)
    new_recDF.set_index(['Label'], inplace=True)
    #st.write(new_recDF)
    ch_col1.bar_chart(new_recDF)

    ch_col2.write("""
                ## Quarterly Dividends
                ###### In USD per quarter
                """)
    ch_col2.bar_chart(ticker_dividends.to_frame())


    st.write("""
        ## Financial Performance
        """)
    st.write(ticker_financials)

    t_col1, t_col2 = st.columns(2)

    t_col1.write("""
    ## Balance Sheet
    ###### In Millions of USD
    """)
    t_col1.write(ticker_bs/1000000)

    t_col2.write("""
        ## Cash Flow Statement
        ###### In Millions of USD
        """)
    t_col2.write(ticker_cashflow/1000000)


    # st.write(type(ticker_financials))
    # tf_transposed = ticker_financials.transpose()
    # st.write(tf_transposed)
    # st.write(type(tf_transposed['Gross Profit']))
    # gpDF = tf_transposed['Gross Profit'].to_frame()
    # st.write(type(gpDF))
    # st.write(gpDF)
    # gpDF.set_index([''], inplace=True)
    # st.line_chart(gpDF['Gross Profit'])
    #column_names = ['Long Term Sell', 'Buy', 'Equal-Weight', 'Hold', 'Long-term Buy', 'Market Perform', 'Neutral',
     #               'Outperform', 'Overweight', 'Perform', 'Sector Perform', 'Sell', 'Strong Buy', 'Underperform',
      #              'Underweight']


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import base64
import json

# Hide Setting Menu and Footer
hide_menu_style = """
		<style>
		#MainMenu {visibility: hidden; }
		footer {visibility: hidden; }
		<style>
		"""

def app():
	st.title('S&P 500 App')

	st.markdown("""
	This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
	* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, yfinance
	* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
	""")

	st.sidebar.header('User Input Features')

	# Web scraping of S&P 500 data

	@st.cache

	def load_data():
		url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
		html = pd.read_html(url, header = 0)
		df = html[0]
		return df
	df = load_data()
	sector = df.groupby('GICS Sector')

	# Sidebar - Sector selection

	sorted_sector_unique = sorted(df['GICS Sector'].unique())
	selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

	# Filtering data

	df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

	st.header('Display Companies in Selected Sector')
	st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' colums.')
	st.dataframe(df_selected_sector)

	# Download S&P500 data
	# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806

	def filedownload(df):
		csv = df.to_csv(index = False)
		b64 = base64.b64encode(csv.encode()).decode()
		href = f'<a href = "data:file/csv;base64,{b64}" download = "SP500.csv">Download CSV file</a>'
		return href

	st.markdown(filedownload(df_selected_sector), unsafe_allow_html = True)

	# https://pypi.org/project/yfinance/

	data = yf.download(tickers = list(df_selected_sector[:5].Symbol),
	                  period = "ytd",
	                  interval = "1d",
	                  group_by = 'ticker',
	                  auto_adjust = True,
	                  prepost = True,
	                  threads = True,
	                  proxy = None
	                  )

	# Plot Closing Price of Query Symbol

	def price_plot(symbol):
		df = pd.DataFrame(data[symbol].Close)
		df['Date'] = df.index
		plt.fill_between(df.Date, df.Close, color = 'skyblue', alpha = 0.3)
		plt.plot(df.Date, df.Close, color = 'skyblue', alpha = 0.8)
		plt.xticks(rotation = 90)
		plt.title(symbol, fontweight = 'bold')
		plt.xlabel('Date', fontweight = 'bold')
		plt.ylabel('Closing Price', fontweight = 'bold')
		return st.pyplot()

	num_company = st.sidebar.slider('Number of Companies', 1, 5)

	if st.button('Show Plots'):
		st.header('Stock Closing Price')
		for i in list(df_selected_sector.Symbol)[:num_company]:
			price_plot(i)

	#You can disable this warning by disabling the config option: 
	#deprecation.showPyplotGlobalUse
	#After December 1st, 2020, we will remove the ability to do this as it requires the use of Matplotlib's global figure object, which is not thread-safe

	st.set_option('deprecation.showPyplotGlobalUse', False)
import streamlit as st
from multiapp import MultiApp
from webs import dnapps, footapp, sp, ir, bostn
from PIL import Image

# Change Page Icon and Page Title
img = Image.open('datasc.jpg')
st.set_page_config(page_title='Data Science Projects', page_icon = img)

# Hide Setting Menu and Footer
hide_menu_style = """
		<style>
		#MainMenu {visibility: hidden; }
		footer {visibility: hidden; }
		<style>
		"""
st.markdown(hide_menu_style, unsafe_allow_html = True)

app = MultiApp()

st.markdown("""
# Data Science Practice Projects

This is showing multiple web application project using multi-page app framework.

""")

# Add all your application here

app.add_app("DNA Analyze", dnapps.app)
#app.add_app("Basketball Team Scorse Analyze", basketapp.app)
app.add_app("Football Team Analyze", footapp.app)
app.add_app("SP500 Stock Analyze", sp.app)
app.add_app("Iris Flower Prediction", ir.app)
app.add_app("Boston House Price Prediction", bostn.app)

# The main app
app.run()
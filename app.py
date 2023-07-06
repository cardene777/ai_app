import streamlit as st
import webbrowser

from audio_summary import app

# Create sidebar options
options = ['Home', 'Audio Summary']

# Create a sidebar with a selectbox for options
selection = st.sidebar.selectbox('Select Option', options)

# Define content for each option
if selection == 'Home':
    st.title('Home Page')
    st.write('Welcome to the home page!')
    if st.button('Open Page', key="open_page"):
        webbrowser.open("https://metamask.app.link/dapp/oaschoice.com")
elif selection == 'Audio Summary':
    app.main()

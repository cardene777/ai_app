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
    url = "https://metamask.app.link/dapp/oaschoice.com"
    if st.button('Open Page'):
        webbrowser.open_new_tab(url)
elif selection == 'Audio Summary':
    app.main()

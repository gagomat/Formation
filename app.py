import streamlit as st


from file_loading import load_spectrum_file
import plotly.express as px

st.write("Hello World")
print('toto')


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    spectrum = load_spectrum_file(uploaded_file)
    fig = px.scatter(spectrum.data)
    st.plotly_chart(fig, use_container_width=True)

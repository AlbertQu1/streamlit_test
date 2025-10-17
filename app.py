import streamlit as st 

st.header('Flip a Coin 🪙')

number_of_trials= st.slider('attemps', 1,10,25,50,100,500,1000)
start_button= st.button('Start')

if start_button:
    st.write(f'test running with {number_of_trials} attemps')

st.markdown('Under Construction  \nplease return later')

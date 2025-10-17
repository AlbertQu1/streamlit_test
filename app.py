import streamlit as st 
import scipy.stats as stats 
import time

st.header('Flip a Coin 🪙')

chart= st.line_chart([.5])

def toss_coin(n):
    trial_outcomes= stats.bernoulli.rvs(p=.5, size= n)
    mean = None
    outcome_0_count = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_0_count +=1
        if r == 1:
            outcome_1_count +=1
        mean = outcome_1_count / outcome_0_count
        chart.add_rows([mean])
        time.sleep(.05)
    return mean

number_of_trials= st.slider('attemps', 1,1000, 50, 1)
start_button= st.button('Start')

if start_button:
    st.write(f'test running with {number_of_trials} attemps')

st.markdown('Under Construction  \nplease return later')

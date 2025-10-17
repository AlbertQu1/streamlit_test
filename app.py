import pandas as pd
import streamlit as st 
import scipy.stats as stats 
import time

#aqui abrimos variables apra guardar el estado de streamlit
if 'outcome_no' not in st.session_state:
    st.session_state['outcome_no'] = 0

if'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'attemps', 'mean'] )


#aqui tenemos el titulo
st.header('Flip a Coin 🪙')
st.markdown('Under Construction  \nPlease return later')

chart= st.line_chart([.5])

def toss_coin(n):
    trial_outcomes= stats.bernoulli.rvs(p=.5, size= n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count +=1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(.05)
    return mean

number_of_trials= st.slider('Attemps', 1,1000, 50, 1)
start_button= st.button('Start')

if start_button:
    st.write(f'test running with {number_of_trials} attemps.')
    st.session_state['experiment_no']+= 1
    mean= toss_coin(number_of_trials)
    st.session_state['df_experiments_results']=pd.concat([
        st.session_state['experiment_results'],
        pd.DataFrame(data= [[st.session_state['experiment_no'],
                             number_of_trials,
                             mean]])
        ],
        axis=0)
    st.session_state['df_experiment_results']= st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
import pandas as pd
import streamlit as st 
import scipy.stats as stats 
import time

#aqui abrimos variables apra guardar el estado de streamlit
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'attempts', 'mean']
    )


#---UI---
st.header('Flip a Coin 🪙')
st.markdown('Under Construction  \nPlease return later')

chart= st.line_chart([0.5])

def toss_coin(n):
    trial_outcomes = stats.bernoulli.rvs(p=0.5, size= n)
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

number_of_trials= st.slider('Attempts', 1,1000, 50, 1)
start_button= st.button('Start')

if start_button:
    st.write(f'test running with {number_of_trials} attempts.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # agregar la fila y concatenar SOLO cuando se ejecutó el experimento
    row_add = pd.DataFrame(
        [[st.session_state['experiment_no'], number_of_trials, mean]],
        columns=['no', 'attempts', 'mean']
    )
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], row_add],
        axis=0,
        ignore_index=True
    )

st.write(st.session_state['df_experiment_results'])
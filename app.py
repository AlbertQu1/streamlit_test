import pandas as pd
import streamlit as st 
import scipy.stats as stats 
import time
import os
import re
import subprocess

#aqui abrimos variables apra guardar el estado de streamlit
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'attempts', 'mean']
    )


#---UI---
st.header('Flip a Coin 🪙')

# --- read markdown from this source file so changes on disk are reflected ---
def get_markdown_from_source():
    try:
        src_path = os.path.abspath(__file__)
        with open(src_path, 'r', encoding='utf-8') as f:
            src = f.read()
        m = re.search(r'st\.markdown\(\s*(""")[\s\S]*?(""")\s*\)', src)
        if m:
            # extract the full triple-quoted content following st.markdown("""...""")
            block = re.search(r'st\.markdown\(\s*"""\s*([\s\S]*?)\s*"""', src)
            if block:
                return block.group(1)
        # fallback: try to find a standalone triple-quoted block near the top
        block = re.search(r'("""|\'\'\')\s*Esta aplicación[\s\S]*?\1', src)
        if block:
            # remove the surrounding quotes
            return re.sub(r'^("""|\'\'\')\s*', '', re.sub(r'\s*("""|\'\'\')$', '', block.group(0)))
    except Exception:
        pass
    # default text if extraction fails
    return """
Esta aplicación creada con **Python** y **Streamlit** simula el lanzamiento de una moneda para ilustrar la **Ley de los Grandes Números**.
El usuario selecciona el número de intentos y el programa ejecuta una serie de lanzamientos aleatorios usando la distribución *Bernoulli* de SciPy.
"""

markdown_text = get_markdown_from_source()
st.markdown(markdown_text)

# botones para recargar y para commitear
col_r, col_c = st.columns([1,1])
if col_r.button("Reload markdown from disk"):
    # pulsar recarga la app; al recargar se volverá a leer el archivo y mostrará cambios guardados en disco
    st.experimental_rerun()

if col_c.button("Commit app.py"):
    try:
        src_dir = os.path.dirname(os.path.abspath(__file__))
        # ejecutar git desde el directorio del proyecto
        subprocess.run(['git', 'add', 'app.py'], check=True, cwd=src_dir, capture_output=True)
        res = subprocess.run(['git', 'commit', '-m', 'Update app.py markdown'], check=True, cwd=src_dir, capture_output=True)
        out = (res.stdout or res.stderr).decode('utf-8', errors='replace')
        st.success("Commit realizado:")
        st.code(out)
    except subprocess.CalledProcessError as e:
        msg = (e.stderr or e.stdout or str(e))
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8', errors='replace')
        st.error(f"Git error: {msg}")

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
import streamlit as st

from main import geraTreino

st.markdown('# Personal Treiner')
biotipo = st.text_area('BioTipo', height=180, placeholder='Ectomorfo, Mesomorfo ou Endomorfo')
periodização = st.text_area('Periodização', height=180, placeholder='1 dia, 3 dias ou 5 dias')
tipo  = st.text_area('Tipo', height=180, placeholder='Funcional, Maquinário, Peso Livre, Cardio ou HIIT')


if st.button('Gerar Treino'):
    with st.spinner('Generating...'):
        bullet_points, token_info = geraTreino(biotipo, periodização, tipo)
        st.divider()
        st.markdown(bullet_points)
        st.caption(token_info)

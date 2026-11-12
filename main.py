from src.app import main, data_chat, data_functions_chat
import streamlit as st

pg = st.navigation([  
    st.Page(main, title="Painel de Dados"), 
    st.Page(data_chat, title="Converse com os dados"),
    st.Page(data_functions_chat, title="Converse com os dados usando funções")
    ]
)
pg.run()
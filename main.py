import streamlit as st
from Front.frontend import drainage_calculation_page


st.set_page_config(page_title="PIPE D", page_icon="⏳", layout="wide")

def main():
   drainage_calculation_page()
            
            
if __name__ == "__main__":
    main()
    st.caption ('Copyright 2024, Cristian Ferreira Carlos, Todos os direitos reservados.' )
    st.caption ('https://www.linkedin.com/in/cristian-ferreira-carlos-256b19161/')

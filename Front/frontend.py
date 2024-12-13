import streamlit as st
from End.Vol_tub import calcular_tempo_drenagem
from fractions import Fraction

def selecionar_combustivel():
    """Permite ao usuário selecionar o tipo de combustível e retorna sua densidade e fator de viscosidade."""
    combustiveis = {
        'Diesel S10': {'densidade': 832, 'fator_viscosidade': 0.6},
        'Gasolina': {'densidade': 737, 'fator_viscosidade': 0.8},
        'Biodiesel B100': {'densidade': 880, 'fator_viscosidade': 0.5},
        'Álcool (Etanol)': {'densidade': 789, 'fator_viscosidade': 0.7}
    }
    
    st.write("Selecione o tipo de combustível:")
    opcao = st.selectbox("Escolha o combustível:", 
                     options=list(combustiveis.keys()),
                     format_func=lambda x: f"{x} (densidade: {combustiveis[x]['densidade']} kg/m³)",
                    key="combustivel_select")

    combustivel = combustiveis[opcao]
    st.write(f"Combustível selecionado: {opcao}")
    st.write(f"Densidade: {combustivel['densidade']} kg/m³")
    st.write(f"Fator de viscosidade: {combustivel['fator_viscosidade']}")
    return combustivel['densidade'], combustivel['fator_viscosidade']

def drainage_calculation_page():
    st.title("Cálculo de Drenagem de Tubulação")

    with st.expander("Informações e Ajuda:", expanded=False):
        st.markdown("""
            Esta ferramenta simula o tempo necessário para drenar uma tubulação.
            
            **Instruções:**
            1. Selecione o tipo de combustível.
            2. Insira o diâmetro e o comprimento da tubulação.
            3. Insira o diâmetro do dreno.
            4. Insira a inclinação da tubulação.
            5. Insira a altura da tubulação em relação ao solo.
            6. O resultado da simulação será exibido abaixo.

            *Nota:* Utilize frações como `3/4` para diâmetros de dreno fracionários.
        """)

    with st.form("drainage_form"):
        st.subheader("1. Selecione o Combustível")
        combustivel_densidade, combustivel_viscosidade = selecionar_combustivel()
        
        st.subheader("2. Parâmetros da Tubulação")
        col1, col2 = st.columns(2)
        
        with col1:
            diametro_tube = st.number_input(
                "Diâmetro da tubulação (polegadas):",
                min_value=0.01,
                format="%.2f",
                help="O diâmetro interno da tubulação em polegadas.",
            )
        with col2:
            comprimento_tube = st.number_input(
                "Comprimento da tubulação (metros):",
                min_value=0.1,
                format="%.2f",
                help="O comprimento total da tubulação em metros."
            )
        
        st.subheader("3. Parâmetros do Dreno")
        drain_input = st.text_input(
            "Diâmetro do dreno (polegadas):",
            help="O diâmetro do dreno em polegadas. Utilize frações como '3/4'."
        )
        
        st.subheader("4. Parâmetros Adicionais")
        col3, col4 = st.columns(2)
        
        with col3:
            inclinacao_graus = st.number_input(
                "Inclinação da tubulação (graus):",
                min_value=0.0,
                max_value=90.0,
                value = 0.0,
                format="%.2f",
                help="A inclinação da tubulação em relação à horizontal em graus."
            )
        with col4:
            altura_tubulacao = st.number_input(
                "Altura da tubulação em relação ao solo (metros):",
                min_value=0.01,
                value=0.1,
                format="%.2f",
                help="A altura da tubulação em relação ao solo em metros."
            )
        
        with st.expander("Parâmetros Avançados", expanded=False):
            st.write(f"Densidade do combustível: {combustivel_densidade} kg/m³")
            st.write(f"Fator de Viscosidade: {combustivel_viscosidade}")
        
        submitted = st.form_submit_button("Calcular Tempo de Drenagem")

        if submitted:
            if diametro_tube <= 0:
                st.error("Erro: O diâmetro da tubulação deve ser maior que zero.")
                return
            if comprimento_tube <= 0:
                st.error("Erro: O comprimento da tubulação deve ser maior que zero.")
                return
            
            with st.spinner("Calculando..."):
               calcular_tempo_drenagem(diametro_tube, comprimento_tube, drain_input, combustivel_densidade, combustivel_viscosidade, inclinacao_graus, altura_tubulacao)
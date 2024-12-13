import streamlit as st
import math
from fractions import Fraction

def calcular_volume_tubulacao(diametro_polegadas, comprimento_metros):
    """Calcula o volume de uma tubulação com base no diâmetro e comprimento."""
    diametro_metros = diametro_polegadas * 0.0254
    volume_m3 = math.pi * ((diametro_metros / 2)**2) * comprimento_metros
    volume_litros = volume_m3 * 1000
    return volume_m3, volume_litros

def calcular_tempo_drenagem(diameter_tube, length_tube, drain_input, densidade, fator_viscosidade, inclinacao_graus, altura_tubulacao):
    """Calcula o tempo necessário para drenar uma tubulação horizontal considerando altura variável."""
    
    volume_m3, volume_litros = calcular_volume_tubulacao(diameter_tube, length_tube)
    st.write(f"Volume total na tubulação: {volume_litros:.1f} litros")
    
    if not drain_input:
       st.error("Erro: Digite o diâmetro do dreno!")
       return

    try:
        if '/' in drain_input:
             diameter_drain = float(Fraction(drain_input)) * 0.0254
        else:
             diameter_drain = float(drain_input) * 0.0254
    except ValueError:
        st.error("Erro: Digite um número válido ou uma fração (exemplo: 3/4).")
        return

    # Constantes
    g = 9.81
    Cd = 0.61  # Coeficiente de descarga
    area_drain = math.pi * (diameter_drain / 2)**2
    time_step = 1.0
    total_time = 0
    current_volume = volume_m3
    
    altura_inicial_liquido = (diameter_tube * 0.0254) / 2  # Altura inicial do liquido = raio da tubulação
    altura_atual = altura_inicial_liquido
    
    soma_vazoes = 0
    contagem_vazoes = 0

    st.write("\nDrenagem iniciada...\n")
    progress_bar = st.progress(0)
    status_text = st.empty()

    progress_data = []
    
    while current_volume > 0.0001:
       # Calcula a altura atual do líquido
       altura_atual = min((current_volume / (math.pi * ((diameter_tube*0.0254 / 2)**2) * length_tube) ) * (diameter_tube*0.0254) , altura_inicial_liquido)  # Atualiza a altura com base no volume restante
       
       if altura_atual <= 0:
           break

       # Cálculo da velocidade de saída
       velocity_drain = Cd * math.sqrt(2 * g * altura_atual) * fator_viscosidade
       flow_rate = area_drain * velocity_drain  # m³/s
       flow_rate_h = flow_rate * 3600 #convertendo vazão para m³/h
       # Atualiza o volume drenado
       drained_volume = flow_rate * time_step
       drained_volume = min(drained_volume, current_volume)  # Não pode escoar mais que o volume atual
        
       current_volume -= drained_volume
       total_time += time_step
       
        # Acumular vazões para média
       soma_vazoes += flow_rate
       contagem_vazoes += 1
        
       progress_data.append({
             "time": total_time,
             "volume": current_volume * 1000,
             "flow_rate": flow_rate_h,
             "altura": altura_atual
         })
        
        # Mostrar progresso a cada 5 minutos
       if total_time % 300 == 0:
          progress_percentage = 1 - (current_volume / volume_m3)
          progress_bar.progress(progress_percentage)
          status_text.write(f"Tempo: {int(total_time / 60)} min - Volume restante: {current_volume * 1000:.1f} litros")
          status_text.write(f"Vazão atual: {flow_rate_h:.2f} m³/h")
    
    # Cálculo final de vazões
    if contagem_vazoes > 0:
      vazao_media = (soma_vazoes / contagem_vazoes) * 3600
      total_time_minutes = total_time / 60
      horas = int(total_time_minutes // 60)
      minutos = int(total_time_minutes % 60)
      segundos = int(total_time % 60)
    else:
      vazao_media = 0
      horas, minutos, segundos = 0, 0, 0
    
    st.write("\nDrenagem concluída!")
    st.write(f"Vazão média: {vazao_media:.2f} m³/h")
    st.write(f"\nTempo total para drenar: {horas} horas, {minutos} minutos e {segundos} segundos" if horas > 0
              else f"\nTempo total para drenar: {minutos} minutos e {segundos} segundos")

    # Criação do gráfico
    if progress_data:
      import pandas as pd
      import plotly.express as px

      df_progress = pd.DataFrame(progress_data)
      
       # Criar gráficos com Plotly Express
      fig1 = px.line(df_progress, x="time", y="volume", title="Volume de Líquido Restante ao Longo do Tempo", labels={"time": "Tempo (segundos)", "volume": "Volume (litros)"})
      fig2 = px.line(df_progress, x="time", y="flow_rate", title="Vazão de Drenagem ao Longo do Tempo", labels={"time": "Tempo (segundos)", "flow_rate": "Vazão (m³/h)"})
      fig3 = px.line(df_progress, x="time", y="altura", title="Altura do Fluido ao Longo do Tempo", labels={"time": "Tempo (segundos)", "altura": "Altura (metros)"})
       
      # Exibir gráficos
      st.plotly_chart(fig1, use_container_width=True)
      st.plotly_chart(fig2, use_container_width=True)
      st.plotly_chart(fig3, use_container_width=True)
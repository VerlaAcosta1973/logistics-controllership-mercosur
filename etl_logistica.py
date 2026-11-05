from datetime import datetime, timedelta
import random
import pandas as pd
from sqlalchemy import create_engine, text

# Configuração da Conexão com o PostgreSQL 17
USER = "postgres"
PASSWORD = "SUA_SENHA_AQUI"  # Substitua pela sua senha real do PostgreSQL
HOST = "localhost"
PORT = "5432"
DB = "db_custos_logistica"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
)

print("A estabelecer conexão e a limpar tabelas...")

with engine.begin() as conn:
  conn.execute(
      text(
          "TRUNCATE TABLE fato_viagens, dim_veiculo, dim_rota, dim_posto RESTART"
          " IDENTITY CASCADE;"
      )
  )

# 1. Dimensão Veículos (Frota de 26 Veículos - Foco em Volvo, Scania e Iveco)
veiculos_data = [
    {"placa": "ABC-1234", "modelo": "Volvo FH 540", "ano": 2021, "capacidade_toneladas": 30.0},
    {"placa": "DEF-5678", "modelo": "Scania R450", "ano": 2021, "capacidade_toneladas": 28.5},
    {"placa": "GHI-9012", "modelo": "Iveco S-Way", "ano": 2023, "capacidade_toneladas": 30.0},
    {"placa": "JKL-3456", "modelo": "Volvo FH 460", "ano": 2020, "capacidade_toneladas": 27.0},
    {"placa": "MNO-7890", "modelo": "Scania R500", "ano": 2023, "capacidade_toneladas": 32.0},
    {"placa": "PQR-2345", "modelo": "Iveco Stralis", "ano": 2019, "capacidade_toneladas": 27.0},
    {"placa": "STU-6789", "modelo": "Volvo FH 500", "ano": 2021, "capacidade_toneladas": 30.0},
    {"placa": "VWX-1239", "modelo": "Scania R540", "ano": 2022, "capacidade_toneladas": 33.0},
    {"placa": "YZA-4567", "modelo": "Volvo FH 540", "ano": 2022, "capacidade_toneladas": 30.0},
    {"placa": "BCD-8901", "modelo": "Scania R450", "ano": 2020, "capacidade_toneladas": 28.5},
    {"placa": "EFG-3452", "modelo": "Iveco S-Way", "ano": 2024, "capacidade_toneladas": 30.0},
    {"placa": "HIJ-6781", "modelo": "Volvo FH 460", "ano": 2023, "capacidade_toneladas": 27.0},
    {"placa": "KLM-9013", "modelo": "Scania R500", "ano": 2020, "capacidade_toneladas": 32.0},
    {"placa": "NOP-2346", "modelo": "Iveco Stralis", "ano": 2018, "capacidade_toneladas": 26.5},
    {"placa": "QRS-5679", "modelo": "Volvo FH 500", "ano": 2022, "capacidade_toneladas": 30.0},
    {"placa": "TUV-1122", "modelo": "Scania R540", "ano": 2023, "capacidade_toneladas": 33.0},
    {"placa": "WXY-3344", "modelo": "Volvo FH 540", "ano": 2019, "capacidade_toneladas": 30.0},
    {"placa": "ZAB-5566", "modelo": "Iveco S-Way", "ano": 2022, "capacidade_toneladas": 30.0},
    {"placa": "CDE-7788", "modelo": "Scania R450", "ano": 2022, "capacidade_toneladas": 28.5},
    {"placa": "FGH-9900", "modelo": "Volvo FH 460", "ano": 2021, "capacidade_toneladas": 27.0},
    {"placa": "IJK-1212", "modelo": "Scania R500", "ano": 2021, "capacidade_toneladas": 32.0},
    {"placa": "LMN-3434", "modelo": "Iveco S-Way", "ano": 2023, "capacidade_toneladas": 30.0},
    {"placa": "OPQ-5656", "modelo": "Volvo FH 500", "ano": 2020, "capacidade_toneladas": 30.0},
    {"placa": "RST-7878", "modelo": "Scania R540", "ano": 2024, "capacidade_toneladas": 33.0},
    {"placa": "UVW-9090", "modelo": "Volvo FH 540", "ano": 2023, "capacidade_toneladas": 30.0},
    {"placa": "XYZ-2468", "modelo": "Iveco Stralis", "ano": 2019, "capacidade_toneladas": 27.0},
]
df_veiculos = pd.DataFrame(veiculos_data)

# 2. Dimensão Rotas (Logística Internacional - Mercosul)
rotas_data = [
    {"pais_origem": "Brasil", "cidade_origem": "Uruguaiana (RS)", "pais_destino": "Argentina", "cidade_destino": "Buenos Aires (BA)", "distancia_km": 800.0, "tempo_medio_espera_fronteira_horas": 12.5},
    {"pais_origem": "Brasil", "cidade_origem": "São Paulo (SP)", "pais_destino": "Argentina", "cidade_destino": "Córdoba (CB)", "distancia_km": 2400.0, "tempo_medio_espera_fronteira_horas": 18.0},
    {"pais_origem": "Brasil", "cidade_origem": "Porto Alegre (RS)", "pais_destino": "Uruguai", "cidade_destino": "Montevidéu (MV)", "distancia_km": 950.0, "tempo_medio_espera_fronteira_horas": 8.0},
    {"pais_origem": "Brasil", "cidade_origem": "Curitiba (PR)", "pais_destino": "Chile", "cidade_destino": "Santiago (ST)", "distancia_km": 3100.0, "tempo_medio_espera_fronteira_horas": 24.0},
    {"pais_origem": "Brasil", "cidade_origem": "São Paulo (SP)", "pais_destino": "Argentina", "cidade_destino": "Rosário (Santa Fe)", "distancia_km": 2100.0, "tempo_medio_espera_fronteira_horas": 15.0},
    {"pais_origem": "Brasil", "cidade_origem": "Florianópolis (SC)", "pais_destino": "Argentina", "cidade_destino": "Mendoza (MD)", "distancia_km": 2850.0, "tempo_medio_espera_fronteira_horas": 22.0},
    {"pais_origem": "Brasil", "cidade_origem": "Campinas (SP)", "pais_destino": "Chile", "cidade_destino": "Valparaíso (VP)", "distancia_km": 3150.0, "tempo_medio_espera_fronteira_horas": 26.0},
    {"pais_origem": "Brasil", "cidade_origem": "Uruguaiana (RS)", "pais_destino": "Uruguai", "cidade_destino": "Rivera (RV)", "distancia_km": 420.0, "tempo_medio_espera_fronteira_horas": 5.0},
    {"pais_origem": "Brasil", "cidade_origem": "Joinville (SC)", "pais_destino": "Argentina", "cidade_destino": "Buenos Aires (BA)", "distancia_km": 1250.0, "tempo_medio_espera_fronteira_horas": 14.0},
    {"pais_origem": "Brasil", "cidade_origem": "Belo Horizonte (MG)", "pais_destino": "Argentina", "cidade_destino": "Córdoba (CB)", "distancia_km": 2980.0, "tempo_medio_espera_fronteira_horas": 19.0},
    {"pais_origem": "Brasil", "cidade_origem": "Porto Alegre (RS)", "pais_destino": "Chile", "cidade_destino": "Antofagasta (AN)", "distancia_km": 2900.0, "tempo_medio_espera_fronteira_horas": 28.0},
    {"pais_origem": "Brasil", "cidade_origem": "São Paulo (SP)", "pais_destino": "Uruguai", "cidade_destino": "Montevidéu (MV)", "distancia_km": 1900.0, "tempo_medio_espera_fronteira_horas": 10.0},
]
df_rotas = pd.DataFrame(rotas_data)

# 3. Dimensão Postos
postos_data = [
    {"nome_posto": "Posto Fronteira Sul", "localizacao": "Uruguaiana (BR)", "pais": "Brasil", "moeda": "BRL", "preco_litro_diesel": 6.15},
    {"nome_posto": "YPF Paso de los Libres", "localizacao": "Paso de los Libres (AR)", "pais": "Argentina", "moeda": "ARS", "preco_litro_diesel": 980.00},
    {"nome_posto": "Ancap Ruta 5", "localizacao": "Rivera (UY)", "pais": "Uruguai", "moeda": "UYU", "preco_litro_diesel": 63.50},
    {"nome_posto": "Copec Internacional", "localizacao": "Los Andes (CL)", "pais": "Chile", "moeda": "CLP", "preco_litro_diesel": 1180.00},
    {"nome_posto": "YPF Autopista Córdoba", "localizacao": "Córdoba (AR)", "pais": "Argentina", "moeda": "ARS", "preco_litro_diesel": 1010.00},
    {"nome_posto": "Petrobras Uruguaiana", "localizacao": "Uruguaiana (BR)", "pais": "Brasil", "moeda": "BRL", "preco_litro_diesel": 6.08},
]
df_postos = pd.DataFrame(postos_data)

# Inserindo Dimensões
df_veiculos.to_sql("dim_veiculo", engine, if_exists="append", index=False)
df_rotas.to_sql("dim_rota", engine, if_exists="append", index=False)
df_postos.to_sql("dim_posto", engine, if_exists="append", index=False)

id_veiculos = pd.read_sql("SELECT id_veiculo FROM dim_veiculo", engine)["id_veiculo"].tolist()
id_rotas = pd.read_sql("SELECT id_rota FROM dim_rota", engine)["id_rota"].tolist()
id_postos = pd.read_sql("SELECT id_posto FROM dim_posto", engine)["id_posto"].tolist()

distancias_dict = pd.read_sql("SELECT id_rota, distancia_km FROM dim_rota", engine).set_index("id_rota")["distancia_km"].to_dict()

# 4. Gerando Fato Viagens (Total quebrado e assimétrico)
random.seed(42)
viagens_data = []
data_inicio_base = datetime(2023, 1, 1)

total_viagens = random.randint(2043, 2187)
print(f"A gerar {total_viagens} viagens simuladas (2023-2025) com frota Volvo, Scania e Iveco...")

# Pesos de disponibilidade para gerar assimetria entre os caminhões
pesos_disponibilidade = [random.uniform(0.3, 1.0) for _ in range(len(id_veiculos))]

for _ in range(total_viagens):
  id_v = random.choices(id_veiculos, weights=pesos_disponibilidade, k=1)[0]
  id_r = random.choice(id_rotas)
  id_p = random.choice(id_postos)

  dias_aleatorios = random.randint(0, 1095)
  data_saida = data_inicio_base + timedelta(days=dias_aleatorios)
  duracao_viagem = random.randint(3, 15)
  data_chegada = data_saida + timedelta(days=duracao_viagem)

  distancia = distancias_dict[id_r]
  fator_inflacao = 1.0 + ((data_saida.year - 2023) * 0.07)

  litros = round((distancia / 2.8) * random.uniform(0.95, 1.05), 2)
  manutencao = round(random.uniform(400.0, 5500.0) * fator_inflacao, 2)
  pedagios = round(distancia * random.uniform(0.20, 0.32) * fator_inflacao, 2)
  impostos = round(random.uniform(1200.0, 6500.0) * fator_inflacao, 2)
  receita = round(distancia * random.uniform(5.8, 9.2) * fator_inflacao, 2)

  viagens_data.append({
      "id_veiculo": id_v,
      "id_rota": id_r,
      "id_posto": id_p,
      "data_saida": data_saida.strftime("%Y-%m-%d"),
      "data_chegada": data_chegada.strftime("%Y-%m-%d"),
      "litros_diesel_consumidos": litros,
      "custo_manutencao_corretiva": manutencao,
      "pedagios_totais": pedagios,
      "impostos_retidos": impostos,
      "receita_bruta_frete": receita,
  })

df_viagens = pd.DataFrame(viagens_data)
df_viagens.to_sql("fato_viagens", engine, if_exists="append", index=False)

print(f"Sucesso! Base populada com {total_viagens} viagens de frotas Volvo, Scania e Iveco.")
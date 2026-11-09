# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text

# ==============================================================================
# 1. CONEXÃO COM O POSTGRESQL 17
# ==============================================================================
# Atualizado com o nome exato do banco de dados: db_custos_logistica
# (Substitua 'sua_senha_aqui' pela sua senha real do PostgreSQL)
DB_URL = "postgresql+psycopg2://postgres:fernanda020606@localhost:5432/db_custos_logistica"

engine = create_engine(DB_URL)


# ==============================================================================
# 2. LIMPEZA IDEMPOTENTE DO BANCO DE DADOS
# ==============================================================================
def limpar_ambiente():
  """Apaga as tabelas com CASCADE para garantir reset limpo sem erros de Foreign Key."""
  with engine.begin() as conn:
    print("🧹 Limpando tabelas existentes no banco 'db_custos_logistica'...")
    conn.execute(text("DROP TABLE IF EXISTS fato_viagens CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_rota CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_veiculo CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_posto CASCADE;"))
    print("✅ Ambiente limpo com sucesso! Estrutura pronta para ser criada.")


# ==============================================================================
# 3. DIMENSÃO ROTAS (Mercosul - Exportação e Importação / Backhaul)
# ==============================================================================
def gerar_dim_rotas():
  rotas = [
      # --- EXPORTAÇÃO (Brasil ➔ Mercosul/Chile) ---
      {
          "id_rota": 1,
          "pais_origem": "Brasil",
          "cidade_origem": "Porto Alegre (RS)",
          "pais_destino": "Chile",
          "cidade_destino": "Antofagasta (AN)",
          "distancia_km": 3600,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 28.0,
      },
      {
          "id_rota": 2,
          "pais_origem": "Brasil",
          "cidade_origem": "Curitiba (PR)",
          "pais_destino": "Chile",
          "cidade_destino": "Santiago (ST)",
          "distancia_km": 3100,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 24.0,
      },
      {
          "id_rota": 3,
          "pais_origem": "Brasil",
          "cidade_origem": "Belo Horizonte (MG)",
          "pais_destino": "Argentina",
          "cidade_destino": "Córdoba (CB)",
          "distancia_km": 2850,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 16.0,
      },
      {
          "id_rota": 4,
          "pais_origem": "Brasil",
          "cidade_origem": "Campinas (SP)",
          "pais_destino": "Chile",
          "cidade_destino": "Valparaíso (VP)",
          "distancia_km": 3300,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 26.0,
      },
      {
          "id_rota": 5,
          "pais_origem": "Brasil",
          "cidade_origem": "Florianópolis (SC)",
          "pais_destino": "Argentina",
          "cidade_destino": "Mendoza (MD)",
          "distancia_km": 2400,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 18.0,
      },
      {
          "id_rota": 6,
          "pais_origem": "Brasil",
          "cidade_origem": "São Paulo (SP)",
          "pais_destino": "Argentina",
          "cidade_destino": "Córdoba (CB)",
          "distancia_km": 2400,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 18.0,
      },
      {
          "id_rota": 7,
          "pais_origem": "Brasil",
          "cidade_origem": "São Paulo (SP)",
          "pais_destino": "Argentina",
          "cidade_destino": "Rosário (Santa Fe)",
          "distancia_km": 2100,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 14.0,
      },
      {
          "id_rota": 8,
          "pais_origem": "Brasil",
          "cidade_origem": "São Paulo (SP)",
          "pais_destino": "Uruguai",
          "cidade_destino": "Montevidéu (MV)",
          "distancia_km": 1950,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 10.0,
      },
      {
          "id_rota": 9,
          "pais_origem": "Brasil",
          "cidade_origem": "Joinville (SC)",
          "pais_destino": "Argentina",
          "cidade_destino": "Buenos Aires (BA)",
          "distancia_km": 1650,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 12.0,
      },
      {
          "id_rota": 10,
          "pais_origem": "Brasil",
          "cidade_origem": "Porto Alegre (RS)",
          "pais_destino": "Uruguai",
          "cidade_destino": "Montevidéu (MV)",
          "distancia_km": 890,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 8.0,
      },
      {
          "id_rota": 11,
          "pais_origem": "Brasil",
          "cidade_origem": "Uruguaiana (RS)",
          "pais_destino": "Argentina",
          "cidade_destino": "Buenos Aires (BA)",
          "distancia_km": 720,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 10.0,
      },
      {
          "id_rota": 12,
          "pais_origem": "Brasil",
          "cidade_origem": "Uruguaiana (RS)",
          "pais_destino": "Uruguai",
          "cidade_destino": "Rivera (RV)",
          "distancia_km": 240,
          "tipo_operacao": "Exportação",
          "tempo_medio_espera_horas": 4.0,
      },
      # --- IMPORTAÇÃO / RETORNO (Mercosul/Chile ➔ Brasil - Backhaul) ---
      {
          "id_rota": 13,
          "pais_origem": "Argentina",
          "cidade_origem": "Buenos Aires (BA)",
          "pais_destino": "Brasil",
          "cidade_destino": "São Paulo (SP)",
          "distancia_km": 2200,
          "tipo_operacao": "Importação",
          "tempo_medio_espera_horas": 12.0,
      },
      {
          "id_rota": 14,
          "pais_origem": "Chile",
          "cidade_origem": "Santiago (ST)",
          "pais_destino": "Brasil",
          "cidade_destino": "Curitiba (PR)",
          "distancia_km": 3100,
          "tipo_operacao": "Importação",
          "tempo_medio_espera_horas": 22.0,
      },
      {
          "id_rota": 15,
          "pais_origem": "Uruguai",
          "cidade_origem": "Montevidéu (MV)",
          "pais_destino": "Brasil",
          "cidade_destino": "Porto Alegre (RS)",
          "distancia_km": 890,
          "tipo_operacao": "Importação",
          "tempo_medio_espera_horas": 7.0,
      },
      {
          "id_rota": 16,
          "pais_origem": "Argentina",
          "cidade_origem": "Córdoba (CB)",
          "pais_destino": "Brasil",
          "cidade_destino": "Campinas (SP)",
          "distancia_km": 2300,
          "tipo_operacao": "Importação",
          "tempo_medio_espera_horas": 15.0,
      },
      {
          "id_rota": 17,
          "pais_origem": "Argentina",
          "cidade_origem": "Mendoza (MD)",
          "pais_destino": "Brasil",
          "cidade_destino": "São Paulo (SP)",
          "distancia_km": 2550,
          "tipo_operacao": "Importação",
          "tempo_medio_espera_horas": 17.0,
      },
  ]

  df_rotas = pd.DataFrame(rotas)

  df_rotas.to_sql("dim_rota", engine, if_exists="replace", index=False)
  print("-> Tabela 'dim_rota' populada com sucesso.")
  return df_rotas


# ==============================================================================
# 4. DIMENSÃO VEÍCULOS (Frota de 26 cavalos/carretas)
# ==============================================================================
def gerar_dim_veiculos():
  veiculos = []
  modelos = ["Volvo FH 540", "Scania R450", "DAF XF 530", "Mercedes-Benz Actros"]

  for i in range(1, 27):
    veiculos.append({
        "id_veiculo": i,
        "placa": f"ABC{i:04d}",
        "modelo": random.choice(modelos),
        "ano_fabricacao": random.randint(2019, 2024),
        "capacidade_ton": 32.0,
        "media_kml_alvo": round(random.uniform(2.1, 2.5), 2),
    })

  df_veiculos = pd.DataFrame(veiculos)
  df_veiculos.to_sql("dim_veiculo", engine, if_exists="replace", index=False)
  print("-> Tabela 'dim_veiculo' populada com sucesso.")
  return df_veiculos


# ==============================================================================
# 5. DIMENSÃO POSTOS DE COMBUSTÍVEL (Mercosul)
# ==============================================================================
def gerar_dim_postos():
  postos = [
      {
          "id_posto": 1,
          "nome_posto": "Posto Marangon (Uruguaiana - BR)",
          "pais": "Brasil",
          "moeda": "BRL",
          "preco_diesel_litro": 6.15,
      },
      {
          "id_posto": 2,
          "nome_posto": "YPF Paso de los Libres (AR)",
          "pais": "Argentina",
          "moeda": "ARS",
          "preco_diesel_litro": 5.80,
      },
      {
          "id_posto": 3,
          "nome_posto": "Shell Uruguaiana (BR)",
          "pais": "Brasil",
          "moeda": "BRL",
          "preco_diesel_litro": 6.20,
      },
      {
          "id_posto": 4,
          "nome_posto": "Ancap Bella Unión (UY)",
          "pais": "Uruguai",
          "moeda": "UYU",
          "preco_diesel_litro": 7.10,
      },
      {
          "id_posto": 5,
          "nome_posto": "Copec Los Andes (CL)",
          "pais": "Chile",
          "moeda": "CLP",
          "preco_diesel_litro": 6.50,
      },
  ]

  df_postos = pd.DataFrame(postos)
  df_postos.to_sql("dim_posto", engine, if_exists="replace", index=False)
  print("-> Tabela 'dim_posto' populada com sucesso.")
  return df_postos


# ==============================================================================
# 6. TABELA FATO DE VIAGENS (Cálculo Financeiro Operacional)
# ==============================================================================
# ==============================================================================
# 6. TABELA FATO DE VIAGENS (Cálculo Financeiro Operacional)
# ==============================================================================


def gerar_fato_viagens(df_rotas, df_veiculos):
  viagens = []
  # Definindo o início há 3 anos (ex: 2023, 2024 e 2025)
  data_inicial = datetime(2023, 1, 1)
  total_dias_3_anos = 365 * 3  # Aproximadamente 1095 dias

  for i in range(1, 1030):
    rota = df_rotas.sample(1).iloc[0]
    veiculo = df_veiculos.sample(1).iloc[0]

    dias_viagem = max(1, int(rota["distancia_km"] / 600))
    # Sorteia uma data distribuída ao longo dos 3 anos
    data_saida = data_inicial + timedelta(
        days=random.randint(0, total_dias_3_anos), hours=random.randint(6, 20)
    )
    data_chegada = data_saida + timedelta(
        days=dias_viagem, hours=random.randint(2, 10)
    )

    # Tarifas por KM (Exportação vs Importação/Backhaul)
    if rota["tipo_operacao"] == "Exportação":
      tarifa_km = random.uniform(8.5, 11.0)
    else:
      tarifa_km = random.uniform(6.5, 9.0)

    receita_bruta = round(rota["distancia_km"] * tarifa_km, 2)
    impostos_retidos = round(receita_bruta * 0.04, 2)  # 4% de impostos retidos

    # Consumo e custos operacionais variáveis
    kml_real = round(
        veiculo["media_kml_alvo"] + random.uniform(-0.25, 0.2), 2
    )
    litros_combustivel = round(rota["distancia_km"] / kml_real, 2)
    custo_combustivel = round(
        litros_combustivel * random.uniform(5.90, 6.60), 2
    )

    custo_pedagio = round(rota["distancia_km"] * random.uniform(0.70, 1.10), 2)
    custo_diarias_motorista = round(dias_viagem * 250.0, 2)
    custo_manutencao_prev = round(
        rota["distancia_km"] * random.uniform(0.35, 0.55), 2
    )
    custo_manutencao_corretiva = round(
        rota["distancia_km"] * random.uniform(0.20, 0.40), 2
    )

    custo_total_operacional = round(
        custo_combustivel
        + custo_pedagio
        + custo_diarias_motorista
        + custo_manutencao_prev
        + custo_manutencao_corretiva,
        2,
    )

    resultado_operacional_direto = round(
        receita_bruta - custo_total_operacional, 2
    )

    viagens.append({
        "data_saida": data_saida,
        "data_chegada": data_chegada,
        "id_veiculo": veiculo["id_veiculo"],
        "id_rota": rota["id_rota"],
        "km_percorrido": rota["distancia_km"],
        "receita_bruta_total": receita_bruta,
        "impostos_retidos": impostos_retidos,
        "custo_combustivel": custo_combustivel,
        "custo_pedagio": custo_pedagio,
        "custo_diarias_motorista": custo_diarias_motorista,
        "custo_manutencao_prev": custo_manutencao_prev,
        "custo_manutencao_corretiva": custo_manutencao_corretiva,
        "custo_total_operacional": custo_total_operacional,
        "resultado_operacional_direto": resultado_operacional_direto,
    })

  # Converte para DataFrame
  df_fato = pd.DataFrame(viagens)

  # 1. ORDENAÇÃO CRONOLÓGICA: Do mais antigo para o mais recente
  df_fato = df_fato.sort_values(by="data_saida").reset_index(drop=True)

  # 2. ATRIBUIÇÃO DE ID SEQUENCIAL: Agora alinhado perfeitamente com a data
  df_fato["id_viagem"] = range(1, len(df_fato) + 1)

  # Reorganiza as colunas para o 'id_viagem' ficar na primeira posição
  cols = ["id_viagem"] + [col for col in df_fato.columns if col != "id_viagem"]
  df_fato = df_fato[cols]

  # Grava no PostgreSQL
  df_fato.to_sql("fato_viagens", engine, if_exists="replace", index=False)
  print(
      "-> Tabela 'fato_viagens' populada com 1.000 viagens ordenadas"
      " cronologicamente (2023-2025)."
  )



# ==============================================================================
# 7. EXECUÇÃO DO PIPELINE ETL
# ==============================================================================
if __name__ == "__main__":
  print("=== INICIANDO PIPELINE ETL (db_custos_logistica) ===")

  # 1. Reseta o ambiente de forma segura
  limpar_ambiente()

  # 2. Gera e insere as dimensões
  df_rotas = gerar_dim_rotas()
  df_veiculos = gerar_dim_veiculos()
  df_postos = gerar_dim_postos()

  # 3. Gera e insere a tabela fato
  gerar_fato_viagens(df_rotas, df_veiculos)

  print(
      "\n🎉 PARABÉNS! Pipeline concluído com sucesso absoluto no PostgreSQL!"
  )
  print(
      "Agora abra o Power BI e clique em 'Atualizar' para ver o dashboard"
      " renovado!"
  )
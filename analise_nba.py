import pandas as pd
import numpy as np

# ============================================
# Etapa 0: Carregando os arquivos CSV
# ============================================

player_info = pd.read_csv("Player Season Info.csv")
player_totals = pd.read_csv("Player Totals.csv")


# ============================================
# Etapa 1: Entender e preparar os dados
# ============================================

print("=== TAMANHO DAS BASES ORIGINAIS ===")
print("Player Info:", player_info.shape)
print("Player Totals:", player_totals.shape)

print("\n=== COLUNAS PLAYER INFO ===")
print(player_info.columns)

print("\n=== COLUNAS PLAYER TOTALS ===")
print(player_totals.columns)

print("\n=== VALORES NULOS PLAYER INFO ===")
print(player_info.isnull().sum().sort_values(ascending=False))

print("\n=== VALORES NULOS PLAYER TOTALS ===")
print(player_totals.isnull().sum().sort_values(ascending=False))


# ============================================
# Etapa 2: Criando cópias das bases
# ============================================

df_info = player_info.copy()
df_totals = player_totals.copy()

print("\nCópias criadas com sucesso!")
print("df_info:", df_info.shape)
print("df_totals:", df_totals.shape)


# ============================================
# Etapa 3: Verificando as ligas disponíveis
# ============================================

print("\n=== LIGAS DISPONÍVEIS ===")

print("Ligas em Player Info:")
print(df_info["lg"].unique())

print("\nLigas em Player Totals:")
print(df_totals["lg"].unique())


# ============================================
# Etapa 4: Filtrando apenas NBA
# ============================================

df_info = df_info[df_info["lg"] == "NBA"].copy()
df_totals = df_totals[df_totals["lg"] == "NBA"].copy()

print("\n=== APÓS FILTRAR APENAS NBA ===")
print("df_info:", df_info.shape)
print("df_totals:", df_totals.shape)

print("\nLigas restantes em df_info:")
print(df_info["lg"].unique())

print("\nLigas restantes em df_totals:")
print(df_totals["lg"].unique())


# ============================================
# Etapa 5: Verificando valores nulos após filtro
# ============================================

print("\n=== VALORES NULOS APÓS FILTRO NBA ===")

print("\nValores nulos em df_info:")
print(df_info.isnull().sum().sort_values(ascending=False).head(15))

print("\nValores nulos em df_totals:")
print(df_totals.isnull().sum().sort_values(ascending=False).head(15))


# ============================================
# Etapa 6: Tratando valores nulos
# ============================================

# Algumas estatísticas antigas podem estar nulas porque não eram registradas em todas as temporadas.
colunas_para_zero = [
    "gs", "mp", "x3p", "x3pa", "orb", "drb",
    "stl", "blk", "tov", "pf", "trp_dbl"
]

for coluna in colunas_para_zero:
    if coluna in df_totals.columns:
        df_totals[coluna] = df_totals[coluna].fillna(0)

print("\nColunas numéricas nulas tratadas com zero.")


# Tratando colunas percentuais
colunas_percentuais = [
    "fg_percent", "x3p_percent", "x2p_percent",
    "e_fg_percent", "ft_percent"
]

for coluna in colunas_percentuais:
    if coluna in df_totals.columns:
        df_totals[coluna] = df_totals[coluna].fillna(0)

print("Colunas percentuais nulas tratadas com zero.")


# Tratando posição dos jogadores
if "pos" in df_info.columns:
    df_info["pos"] = df_info["pos"].fillna("N/A")

if "pos" in df_totals.columns:
    df_totals["pos"] = df_totals["pos"].fillna("N/A")

print("Colunas de posição tratadas.")


# Tratando x2p, x2pa e trb de forma mais inteligente
# x2p = arremessos de 2 pontos convertidos
# x2pa = arremessos de 2 pontos tentados
# trb = rebotes totais

if all(col in df_totals.columns for col in ["x2p", "fg", "x3p"]):
    df_totals["x2p"] = df_totals["x2p"].fillna(df_totals["fg"] - df_totals["x3p"])

if all(col in df_totals.columns for col in ["x2pa", "fga", "x3pa"]):
    df_totals["x2pa"] = df_totals["x2pa"].fillna(df_totals["fga"] - df_totals["x3pa"])

if all(col in df_totals.columns for col in ["trb", "orb", "drb"]):
    df_totals["trb"] = df_totals["trb"].fillna(df_totals["orb"] + df_totals["drb"])


# Garantia final caso ainda sobre algum nulo nessas colunas
colunas_restantes = ["x2p", "x2pa", "trb"]

for coluna in colunas_restantes:
    if coluna in df_totals.columns:
        df_totals[coluna] = df_totals[coluna].fillna(0)

print("Nulos restantes em x2p, x2pa e trb tratados.")


# ============================================
# Etapa 7: Conferindo tratamento dos dados
# ============================================

print("\n=== CONFERINDO TRATAMENTO DOS DADOS ===")

print("\nValores nulos restantes em df_info:")
print(df_info.isnull().sum().sort_values(ascending=False).head(15))

print("\nValores nulos restantes em df_totals:")
print(df_totals.isnull().sum().sort_values(ascending=False).head(15))

print("\nTamanho das bases após tratamento:")
print("df_info:", df_info.shape)
print("df_totals:", df_totals.shape)

print("\nPlayer IDs nulos:")
print("df_info:", df_info["player_id"].isnull().sum())
print("df_totals:", df_totals["player_id"].isnull().sum())

print("\nA coluna pos existe em df_info?", "pos" in df_info.columns)
print("A coluna pos existe em df_totals?", "pos" in df_totals.columns)

print("\nPosições únicas em df_info:")
print(df_info["pos"].unique())

print("\nPosições únicas em df_totals:")
print(df_totals["pos"].unique())

print("\nQuantidade por posição em df_info:")
print(df_info["pos"].value_counts())

print("\nQuantidade por posição em df_totals:")
print(df_totals["pos"].value_counts())

# ============================================
# Etapa 8: Criando métricas por jogo
# ============================================

# Evitando divisão por zero, caso exista algum jogador com 0 jogos
df_totals = df_totals[df_totals["g"] > 0].copy()

df_totals["ppg"] = df_totals["pts"] / df_totals["g"]       # Points per game
df_totals["rpg"] = df_totals["trb"] / df_totals["g"]       # Rebounds per game
df_totals["apg"] = df_totals["ast"] / df_totals["g"]       # Assists per game
df_totals["spg"] = df_totals["stl"] / df_totals["g"]       # Steals per game
df_totals["bpg"] = df_totals["blk"] / df_totals["g"]       # Blocks per game
df_totals["tov_pg"] = df_totals["tov"] / df_totals["g"]    # Turnovers per game
df_totals["mpg"] = df_totals["mp"] / df_totals["g"]        # Minutes per game

print("Métricas por jogo criadas com sucesso!")

print(df_totals[
    [
        "season", "player", "team", "pos", "g",
        "pts", "ppg", "trb", "rpg", "ast", "apg", "mpg"
    ]
].head(10))

# ============================================
# Etapa 9: Criando métrica de eficiência
# ============================================

df_totals["efficiency_score"] = (
    df_totals["pts"] +
    df_totals["trb"] +
    df_totals["ast"] +
    df_totals["stl"] +
    df_totals["blk"] -
    df_totals["tov"]
)

df_totals["efficiency_per_game"] = df_totals["efficiency_score"] / df_totals["g"]

print("Métricas de eficiência criadas com sucesso!")

print(df_totals[
    [
        "season", "player", "team", "pos", "g",
        "pts", "trb", "ast", "stl", "blk", "tov",
        "efficiency_score", "efficiency_per_game"
    ]
].head(10))

# ============================================
# Etapa 10: Arredondando métricas
# ============================================

colunas_metricas = [
    "ppg", "rpg", "apg", "spg", "bpg",
    "tov_pg", "mpg", "efficiency_per_game"
]

df_totals[colunas_metricas] = df_totals[colunas_metricas].round(2)

print("Métricas arredondadas com sucesso!")

print(df_totals[
    [
        "season", "player", "team", "pos", "g",
        "ppg", "rpg", "apg", "spg", "bpg",
        "tov_pg", "mpg", "efficiency_per_game"
    ]
].head(10))

# ============================================
# Etapa 11: Criando dimensão de jogadores
# ============================================

dim_players = (
    df_info
    .groupby(["player_id", "player"], as_index=False)
    .agg(
        pos=("pos", "first"),
        primeira_temporada=("season", "min"),
        ultima_temporada=("season", "max"),
        total_temporadas=("season", "nunique")
    )
)

print("Dimensão de jogadores criada com sucesso!")
print("Formato da dim_players:", dim_players.shape)

print(dim_players.head(10))

# ============================================
# Etapa 12: Criando tabela fato de estatísticas
# ============================================

fact_player_stats = df_totals[
    [
        "season", "lg", "player_id", "player", "team", "pos", "age",
        "g", "gs", "mp",
        "fg", "fga", "fg_percent",
        "x3p", "x3pa", "x3p_percent",
        "x2p", "x2pa", "x2p_percent",
        "ft", "fta", "ft_percent",
        "orb", "drb", "trb",
        "ast", "stl", "blk", "tov", "pf", "pts",
        "ppg", "rpg", "apg", "spg", "bpg", "tov_pg", "mpg",
        "efficiency_score", "efficiency_per_game"
    ]
].copy()

print("Tabela fato criada com sucesso!")
print("Formato da fact_player_stats:", fact_player_stats.shape)

print(fact_player_stats.head(10))

# ============================================
# Etapa 13: Conferindo relacionamento entre tabelas
# ============================================

players_dim = set(dim_players["player_id"])
players_fact = set(fact_player_stats["player_id"])

players_sem_dim = players_fact - players_dim

print("Quantidade de player_id na dimensão:", len(players_dim))
print("Quantidade de player_id na fato:", len(players_fact))
print("Player IDs na fato sem correspondência na dimensão:", len(players_sem_dim))

# ============================================
# Etapa 14: Exportando arquivos finais
# ============================================

dim_players.to_csv("processed/dim_players.csv", index=False, encoding="utf-8-sig")
fact_player_stats.to_csv("processed/fact_player_stats.csv", index=False, encoding="utf-8-sig")

print("Arquivos exportados com sucesso!")
print("Arquivos gerados:")
print("processed/dim_players.csv")
print("processed/fact_player_stats.csv")
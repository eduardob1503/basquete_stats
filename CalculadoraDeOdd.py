import scipy.stats as stats
import pandas as pd
import unicodedata  # Importar para normalização de texto
import os  # Para verificar se o arquivo já existe

def calcular_valor_aposta(media, desvio, linha, odd):
    prob_acerto = 1 - stats.norm.cdf(linha, loc=media, scale=desvio)
    prob_erro = 1 - prob_acerto
    ev = (prob_acerto * odd) - (prob_erro * 1)
    
    return {
        "Probabilidade de acerto": f"{round(prob_acerto * 100, 2)}%",
        "EV": round(ev, 3),
        "Aposta de Valor": "Sim" if ev > 0 else "Não"
    }

# Carregar dados da planilha
file_path = "estatisticas_ultima_temporada_jogadores_completo.csv"
df = pd.read_csv(file_path, delimiter=";")

# Normalizar os nomes dos jogadores para remover acentos
df["Jogador"] = df["Jogador"].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', errors='ignore').decode('utf-8'))

# Selecionar estatísticas relevantes
estatisticas = ["PTS", "3P", "FGA", "AST", "TRB", "STL", "BLK", "PF","TOV"]
mercados = {"PTS": "Pontos", "3P": "Cestas de 3", "AST": "Assistências", "TRB": "Rebotes", "STL": "Roubos", "BLK": "Tocos", "FGA": "Tentativas de Arremesso", "PF": "Faltas", "TOV": "Turnover"}

def analisar_jogador(nome_jogador, linhas_aposta, odds_aposta):
    # Normalizar o nome do jogador para remover acentos
    nome_jogador = unicodedata.normalize('NFKD', nome_jogador).encode('ascii', errors='ignore').decode('utf-8')

    jogador = df[df["Jogador"] == nome_jogador]
    if jogador.empty:
        return f"Jogador {nome_jogador} não encontrado."
    
    resultados = []
    estatisticas_jogador = jogador[estatisticas].to_dict(orient="records")[0]
    
    for stat, mercado in mercados.items():
        linha = linhas_aposta.get(stat, 0)
        odd = odds_aposta.get(stat, 2.00)
        media = jogador[stat].values[0] if stat in jogador.columns else 0
        
        # Definir desvios padrão fixos
        if stat in ["PTS", "FGA"]:
            desvio = 7
        elif stat in ["AST", "TRB"]:
            desvio = 3
        else:
            desvio = 1
        
        resultado = calcular_valor_aposta(media, desvio, linha, odd)
        resultado["Mercado"] = mercado
        resultado["Linha"] = linha
        resultado["Odd"] = odd
        resultado["Média"] = media
        resultado["Jogador"] = nome_jogador  # Adiciona o nome do jogador à linha
        resultados.append(resultado)
    
    df_resultado = pd.DataFrame(resultados)
    df_resultado.insert(0, "Mercado", df_resultado.pop("Mercado"))
    
    return df_resultado

# Exemplo de uso
nome_jogador = "Anthony Davis"
linhas_aposta = {"PTS": 21.5, "3P": 0.5, "AST": 3.5, "TRB": 8.5, "FGA": 18.5,  "STL": 0.5, "BLK": 1.5, "PF": 2.5, "TOV": 2.5}
odds_aposta = {"PTS": 1.86, "3P": 1.62, "AST": 2.15, "TRB": 1.68, "FGA": 1.86,  "STL": 1.52, "BLK": 2.05, "PF": 2.4, "TOV": 2.2}

# Gerar DataFrame com os resultados
df_resultado = analisar_jogador(nome_jogador, linhas_aposta, odds_aposta)

# Caminho do arquivo CSV
csv_file = "resultado_apostas.csv"

# Verificar se o arquivo já existe
if os.path.exists(csv_file):
    # Se o arquivo existe, adiciona (append) os novos dados
    df_resultado.to_csv(csv_file, mode='a', header=False, index=False, sep=";", encoding="utf-8")
    print(f"Resultados adicionados ao arquivo {csv_file}")
else:
    # Se o arquivo não existe, cria o arquivo com cabeçalho
    df_resultado.to_csv(csv_file, mode='w', header=True, index=False, sep=";", encoding="utf-8")
    print(f"Novo arquivo {csv_file} criado com os resultados")
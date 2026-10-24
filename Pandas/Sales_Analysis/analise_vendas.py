# 1. IMPORTAÇÕES

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# 2. CONFIGURAÇÃO DOS CAMINHOS

pasta_projeto = Path(__file__).resolve().parent
pasta_graficos = pasta_projeto / "graficos"


# 3. CONFIGURAÇÃO DO LOGGING

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# 4. FUNÇÕES DE ANÁLISE

def calcular_faturamento(df, coluna):
    """
    Calcula o faturamento total agrupado por uma coluna.

    Args:
        df (pd.DataFrame): DataFrame com os dados de vendas.
        coluna (str): Nome da coluna usada para agrupar os dados.

    Returns:
        pd.Series: Faturamento total por grupo.
    """
    return df.groupby(coluna)["faturamento"].sum()


def criar_grafico(dados, titulo, eixo_x, nome_arquivo):
    """
    Cria e salva um gráfico de barras.

    Args:
        dados (pd.Series): Dados do gráfico.
        titulo (str): Título do gráfico.
        eixo_x (str): Nome do eixo X.
        nome_arquivo (str): Nome do arquivo PNG.
    """

    try:
        plt.figure(figsize=(8, 5))

        dados.plot(
            kind="bar",
            color="steelblue",
            edgecolor="black"
        )

        plt.title(titulo)
        plt.xlabel(eixo_x)
        plt.ylabel("Faturamento (R$)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(
            pasta_graficos / nome_arquivo,
            dpi=300,
            bbox_inches="tight"
        )

        logging.info(
            f"Gráfico salvo com sucesso: {nome_arquivo}"
        )

        plt.show()

    except Exception:
        logging.exception(
            f"Erro ao gerar o gráfico {nome_arquivo}."
        )
        raise

    finally:
        plt.close()


# 5. FUNÇÃO PRINCIPAL

def main():

    # CARREGAMENTO DOS DADOS

    caminho_csv = pasta_projeto / "vendas_treino.csv"

    try:
        df = pd.read_csv(caminho_csv)
        logging.info("Arquivo CSV carregado com sucesso.")

    except FileNotFoundError:
        logging.error(
            f"Arquivo CSV não encontrado: {caminho_csv}"
        )
        return

    except Exception as erro:
        logging.error(
            f"Erro ao carregar o CSV: {erro}"
        )
        return

    # VALIDAÇÃO INICIAL

    if df.empty:
        logging.error("O arquivo CSV está vazio.")
        return

    colunas_obrigatorias = {
        "produto",
        "cidade",
        "quantidade",
        "preco"
    }

    faltantes = colunas_obrigatorias - set(df.columns)

    if faltantes:
        logging.error(
            f"Colunas ausentes no CSV: {faltantes}"
        )
        return

    # VALIDAÇÃO DE CAMPOS TEXTUAIS

    df["produto"] = df["produto"].astype("string").str.strip()
    df["cidade"] = df["cidade"].astype("string").str.strip()

    produtos_vazios = (
        df["produto"].isna()
        | (df["produto"] == "")
    )

    cidades_vazias = (
        df["cidade"].isna()
        | (df["cidade"] == "")
    )

    if produtos_vazios.any():
        logging.error(
            f"Existem {produtos_vazios.sum()} registros com produto vazio."
        )
        return

    if cidades_vazias.any():
        logging.error(
            f"Existem {cidades_vazias.sum()} registros com cidade vazia."
        )
        return
    
    # VERIFICAÇÃO DE DUPLICATAS

    quantidade_duplicados = df.duplicated().sum()

    if quantidade_duplicados > 0:
        logging.warning(
            f"Foram encontradas "
            f"{quantidade_duplicados} linhas duplicadas."
        )
        logging.warning(
            "Os registros serão mantidos até a investigação."
        )

    # CONVERSÃO DOS TIPOS

    df["quantidade"] = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    )

    df["preco"] = pd.to_numeric(
        df["preco"],
        errors="coerce"
    )

    if df[["quantidade", "preco"]].isnull().any().any():
        logging.error(
            "Existem valores não numéricos nas colunas "
            "'quantidade' ou 'preco'."
        )
        return

    logging.info(
        "Validação inicial concluída com sucesso."
    )

    # QUALIDADE DOS DADOS

    print("\nTipos de dados:")
    print(df.dtypes)

    print("\nValores ausentes por coluna:")
    print(df.isnull().sum())

    print("\nQuantidade de linhas duplicadas:")
    print(quantidade_duplicados)

    print("\nEstatísticas da quantidade:")
    print(df["quantidade"].describe())

    print("\nEstatísticas do preço:")
    print(df["preco"].describe())

    print("\nQuantidades menores ou iguais a zero:")
    print((df["quantidade"] <= 0).sum())

    print("\nPreços negativos:")
    print((df["preco"] < 0).sum())

    print("\nPreços zerados:")
    print((df["preco"] == 0).sum())

    # PREPARAÇÃO DOS DADOS

    df["faturamento"] = (
        df["quantidade"] * df["preco"]
    )

    # ANÁLISE EXPLORATÓRIA

    print("\nPrimeiras linhas:")
    print(df.head())

    print("\nDimensões do conjunto de dados:")
    print(df.shape)

    # FATURAMENTO POR PRODUTO

    faturamento_produto = (
        calcular_faturamento(df, "produto")
        .sort_values(ascending=False)
    )

    print("\nFaturamento por produto:")
    print(faturamento_produto)

    # FATURAMENTO POR CIDADE

    faturamento_cidade = (
        calcular_faturamento(df, "cidade")
        .sort_values(ascending=False)
    )

    print("\nFaturamento por cidade:")
    print(faturamento_cidade)

    # VALIDAÇÃO DOS TOTAIS

    total_geral = df["faturamento"].sum()
    total_por_produto = faturamento_produto.sum()
    total_por_cidade = faturamento_cidade.sum()

    print("\nValidação dos totais:")
    print(f"Total geral: R$ {total_geral:.2f}")
    print(f"Total por produto: R$ {total_por_produto:.2f}")
    print(f"Total por cidade: R$ {total_por_cidade:.2f}")

    assert abs(
        total_geral - total_por_produto
    ) < 0.01, (
        "Diferença encontrada entre o total geral "
        "e o total por produto."
    )

    assert abs(
        total_geral - total_por_cidade
    ) < 0.01, (
        "Diferença encontrada entre o total geral "
        "e o total por cidade."
    )

    logging.info(
        "Validação de faturamento concluída."
    )

    # PRINCIPAIS INDICADORES

    produto_lider = faturamento_produto.idxmax()
    valor_produto_lider = faturamento_produto.max()
    participacao_produto = (
        valor_produto_lider / total_geral * 100
    )

    cidade_lider = faturamento_cidade.idxmax()
    valor_cidade_lider = faturamento_cidade.max()
    participacao_cidade = (
        valor_cidade_lider / total_geral * 100
    )

    print("\n=== PRINCIPAIS INDICADORES ===")

    print(
        f"Faturamento total: "
        f"R$ {total_geral:.2f}"
    )

    print(
        f"Produto líder: {produto_lider} "
        f"- R$ {valor_produto_lider:.2f} "
        f"({participacao_produto:.1f}% do total)"
    )

    print(
        f"Cidade líder: {cidade_lider} "
        f"- R$ {valor_cidade_lider:.2f} "
        f"({participacao_cidade:.1f}% do total)"
    )

    # RESUMO POR CIDADE

    resumo_cidade = (
        df.groupby("cidade")[
            ["quantidade", "faturamento"]
        ]
        .sum()
    )

    print("\nResumo por cidade:")
    print(resumo_cidade)

    resumo_cidade.to_csv(
        pasta_projeto / "resumo_por_cidade.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    logging.info(
        "Arquivo resumo_por_cidade.csv gerado."
    )

    # TABELA DINÂMICA

    tabela_pivot = df.pivot_table(
        index="produto",
        columns="cidade",
        values="faturamento",
        aggfunc="sum",
        fill_value=0
    )

    print("\nTabela dinâmica:")
    print(tabela_pivot)

    tabela_pivot.to_csv(
        pasta_projeto / "tabela_pivot.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    logging.info(
        "Arquivo tabela_pivot.csv gerado."
    )

    # GRÁFICOS

    criar_grafico(
        faturamento_produto,
        "Faturamento por Produto",
        "Produto",
        "faturamento_por_produto.png"
    )

    criar_grafico(
        faturamento_cidade,
        "Faturamento por Cidade",
        "Cidade",
        "faturamento_por_cidade.png"
    )

    logging.info(
        "Processamento concluído com sucesso."
    )

    print(
        "\nRelatórios e gráficos gerados com sucesso."
    )


# 6. EXECUÇÃO

if __name__ == "__main__":

    try:
        pasta_graficos.mkdir(exist_ok=True)

        logging.info(
            "Pasta de gráficos verificada."
        )

        main()

    except Exception:
        logging.exception(
        "Erro inesperado durante a execução do programa."
        )
        raise
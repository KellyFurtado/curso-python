# Sales Analysis — Análise de Vendas

## Sobre o projeto

Projeto de análise exploratória de dados de vendas desenvolvido em Python, utilizando Pandas para manipulação e análise de dados e Matplotlib para visualização.

O objetivo é calcular o faturamento, comparar resultados por produto e cidade, verificar a qualidade dos dados e gerar indicadores que apoiem a interpretação dos resultados.

## Tecnologias utilizadas

- Python
- Pandas
- Matplotlib
- pathlib
- logging

## Estrutura do projeto

```text
Sales_Analysis/
├── analise_vendas.py
├── vendas_treino.csv
├── README.md
├── resumo_por_cidade.csv
├── tabela_pivot.csv
└── graficos/
    ├── faturamento_por_produto.png
    └── faturamento_por_cidade.png
```

## Etapas da análise

1. Carregamento dos dados a partir de um arquivo CSV.
2. Tratamento de erros relacionados ao carregamento do arquivo.
3. Verificação de arquivo vazio e de colunas obrigatórias.
4. Validação dos tipos numéricos e dos campos de produto e cidade.
5. Inspeção de valores ausentes, duplicações e valores numéricos suspeitos.
6. Cálculo do faturamento por registro.
7. Análise do faturamento por produto e cidade com Pandas.
8. Validação dos totais calculados.
9. Identificação dos principais indicadores de faturamento.
10. Exportação de relatórios CSV.
11. Criação e salvamento de gráficos ordenados por faturamento.
12. Registro de informações e erros durante a execução com logging.

## Principais resultados

Considerando o conjunto de dados utilizado durante o desenvolvimento do projeto, foram obtidos os seguintes resultados:

- **Faturamento total:** R$ 28.230,00.
- **Produto com maior faturamento:** Notebook, com R$ 21.000,00, correspondendo a aproximadamente 74,4% do faturamento total.
- **Cidade com maior faturamento:** BH, com R$ 18.810,00, correspondendo a aproximadamente 66,6% do faturamento total.

Os totais foram comparados por três perspectivas: faturamento geral, faturamento por produto e faturamento por cidade. Os três valores coincidiram.

Os resultados acima refletem a versão do arquivo CSV utilizada durante o desenvolvimento e podem mudar caso os dados sejam atualizados.

As conclusões se limitam ao conjunto de dados utilizado e não devem ser generalizadas para um negócio real sem dados adicionais.

Faturamento não é sinônimo de lucro. Para calcular o lucro, seriam necessários dados sobre custos e outras despesas.

## Relatórios gerados

O programa gera os seguintes arquivos:

- `resumo_por_cidade.csv`: apresenta a quantidade vendida e o faturamento total por cidade.
- `tabela_pivot.csv`: apresenta o faturamento por produto e cidade.
- `graficos/faturamento_por_produto.png`: gráfico de faturamento por produto.
- `graficos/faturamento_por_cidade.png`: gráfico de faturamento por cidade.

Os relatórios CSV são salvos na pasta principal do projeto, enquanto os gráficos são armazenados na pasta `graficos`.

## Como executar

### 1. Pré-requisitos

É necessário ter Python instalado e o arquivo `vendas_treino.csv` na mesma pasta de `analise_vendas.py`.

### 2. Instale as dependências

No terminal, execute:

```bash
pip install pandas matplotlib
```

As bibliotecas `pathlib` e `logging` fazem parte da biblioteca padrão do Python e não precisam ser instaladas separadamente.

### 3. Execute o programa

No terminal, dentro da pasta do projeto, execute:

```bash
python analise_vendas.py
```

O programa exibirá as análises no terminal, registrará informações sobre a execução e salvará os relatórios e gráficos nos diretórios definidos pelo projeto.

## Aprendizados

Durante o desenvolvimento, foram praticados os seguintes conceitos:

- Leitura e manipulação de arquivos CSV com Pandas.
- Preparação e validação de dados.
- Agrupamentos com `groupby()`.
- Construção de tabelas dinâmicas com `pivot_table()`.
- Criação de funções reutilizáveis.
- Documentação de funções com docstrings.
- Visualização de dados com Matplotlib.
- Organização do código com a função `main()`.
- Uso de `pathlib` para gerenciamento de caminhos.
- Tratamento de exceções com `try/except`.
- Registro de informações, avisos e erros com `logging`.
- Validação automática dos totais calculados.
- Exportação de resultados para arquivos CSV.
- Interpretação de indicadores e resultados de negócio.

## Observações

Este projeto foi desenvolvido para fins de estudo e portfólio, com foco na prática de Python, Pandas, análise exploratória de dados e visualização.

O conjunto de dados utilizado é pequeno e serve para demonstrar técnicas de análise. As conclusões representam apenas os registros disponíveis no arquivo de treinamento.

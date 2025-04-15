# 📦 Sistema Inteligente de Recomendação de Estoque

Este projeto tem como objetivo o desenvolvimento de um sistema inteligente para a **gestão de estoque** utilizando **Streamlit**, **Python**, **Pandas** e **Matplotlib**. O sistema recomenda a quantidade ideal de reposição de produtos em centros de distribuição, levando em consideração a **demanda prevista**, **estoque atual**, **tempo de lead time** e **custo operacional**.

O sistema também inclui a consideração de **margem de segurança** para garantir que o estoque esteja sempre preparado para atender à demanda sem riscos de escassez.

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **Streamlit** - Framework para criação da interface web interativa.
- **Pandas** - Biblioteca para manipulação e análise de dados.
- **NumPy** - Biblioteca para cálculos numéricos.
- **Matplotlib** - Biblioteca para visualização de gráficos.

## 🎯 Funcionalidades

- **Recomendação de Reposição**: O sistema calcula automaticamente a quantidade ideal de reposição de produtos em centros de distribuição.
- **Margem de Segurança**: A margem de segurança pode ser ajustada para garantir que o estoque recomendado leve em conta variações inesperadas na demanda.
- **Cálculo de Custo Total**: O custo de **armazenagem** e o custo de **ruptura** (falta de estoque) são calculados automaticamente para fornecer uma visão completa dos custos envolvidos na gestão de estoque.
- **Visualizações**: Gráficos que mostram a comparação entre **estoque atual**, **demanda prevista** e as **quantidades recomendadas** para reposição.

## 📊 Como Funciona

1. **Leitura de Dados**: O sistema gera uma planilha de dados simulada contendo informações sobre **estoque atual**, **demanda prevista**, **custo de armazenagem**, **custo de ruptura**, entre outros dados.
2. **Filtros Interativos**: O usuário pode filtrar os dados por **centro de distribuição** e **produto**, além de ajustar os parâmetros de **margem de segurança** e **risco de ruptura**.
3. **Cálculos e Recomendações**: O sistema calcula a **demanda total**, o **estoque ideal**, o **buffer de segurança** e a **quantidade recomendada** para reposição com base nas entradas do usuário.
4. **Exibição de Dados**: Os resultados são exibidos em uma tabela interativa, permitindo ao usuário visualizar os dados filtrados.
5. **Gráficos**: O sistema também gera gráficos que ajudam a visualizar a relação entre **estoque atual**, **demanda prevista** e as **quantidades recomendadas** para reposição ao longo do tempo.

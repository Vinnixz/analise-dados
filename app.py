import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Simulação de dados
@st.cache_data
def gerar_dados():
    np.random.seed(42)
    centros = ["São Paulo", "Recife", "Brasília", "Belém", "Florianópolis"]
    produtos = ["Memória RAM", "Placa Mãe", "Processador", "HD", "SSD"]
    dias = pd.date_range(start="2025-04-01", periods=10)

    dados = []

    for centro in centros:
        for produto in produtos:
            for dia in dias:
                estoque = np.random.randint(50, 200)
                demanda = np.random.randint(60, 180)
                lead_time = np.random.randint(2, 6)
                custo_armazenagem = np.random.randint(1, 3)
                custo_ruptura = np.random.randint(5, 11)

                dados.append(
                    {
                        "data": dia,
                        "centro": centro,
                        "produto": produto,
                        "estoque_atual": estoque,
                        "demanda_prevista": demanda,
                        "lead_time_dias": lead_time,
                        "custo_armazenagem": custo_armazenagem,
                        "custo_ruptura": custo_ruptura,
                    }
                )

    df = pd.DataFrame(dados)

    # Parâmetros de negócio
    margem_segurança = 0.2
    dias_planejamento = 7

    # Função que retorna colunas intermediárias
    def calcular_reposicao(linha):
        demanda_total = linha["demanda_prevista"] * (1 + margem_segurança)
        buffer = linha["lead_time_dias"] * (
            linha["demanda_prevista"] / dias_planejamento
        )
        estoque_ideal = demanda_total + buffer
        quantidade = max(0, estoque_ideal - linha["estoque_atual"])

        return pd.Series(
            {
                "demanda_total": int(demanda_total),
                "buffer": int(buffer),
                "estoque_ideal": int(estoque_ideal),
                "quantidade_recomendada": int(quantidade),
            }
        )

    # Aplica a função a todo o dataframe
    valores = df.apply(calcular_reposicao, axis=1)
    df = pd.concat([df, valores], axis=1)

    return df


# Gera os dados
df = gerar_dados()

# Interface do Streamlit
st.title("📦 Sistema de Recomendação de Estoque - DataLog")

centros = df["centro"].unique()
produtos = df["produto"].unique()

centro_escolhido = st.selectbox("Escolha o Centro de Distribuição", centros)
produto_escolhido = st.selectbox("Escolha o Produto", produtos)

df_filtrado = df[
    (df["centro"] == centro_escolhido) & (df["produto"] == produto_escolhido)
]
with st.expander("❓ Explicações do Sistema"):
    st.markdown(
        """
    ### 📊 Explicações do Gráfico e Tabela

    **Estoque Atual**: Quantidade disponível no centro de distribuição no dia.  
    **Demanda Prevista**: Quantidade esperada de vendas no dia.  
    **Lead Time (dias)**: Tempo médio que um novo pedido leva para chegar.  
    **Demanda Total**: Demanda prevista com margem de segurança de 20% (demanda * 1.2).  
    **Buffer**: Estoque extra necessário para cobrir o lead time (lead_time * (demanda_prevista / 7)).  
    **Estoque Ideal**: Quantidade ideal a manter = demanda_total + buffer.  
    **Quantidade Recomendada**: Quanto precisa comprar ou produzir para atingir o estoque ideal.  
    Se o estoque atual já for suficiente, a recomendação é zero.

    ---
    """
    )
st.subheader(f"📊 Dados de {produto_escolhido} em {centro_escolhido}")
df_filtrado["data"] = df_filtrado["data"].dt.strftime("%d/%m/%y")
st.dataframe(
    df_filtrado[
        [
            "data",
            "estoque_atual",
            "demanda_prevista",
            "lead_time_dias",
            "demanda_total",
            "buffer",
            "estoque_ideal",
            "quantidade_recomendada",
        ]
    ],
    use_container_width=True,
)

# Gráfico de comparação
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    df_filtrado["data"], df_filtrado["estoque_atual"], label="Estoque Atual", marker="o"
)
ax.plot(
    df_filtrado["data"],
    df_filtrado["demanda_prevista"],
    label="Demanda Prevista",
    marker="x",
)
ax.plot(
    df_filtrado["data"],
    df_filtrado["quantidade_recomendada"],
    label="Reposição Recomendada",
    linestyle="--",
)
ax.plot(
    df_filtrado["data"],
    df_filtrado["estoque_ideal"],
    label="Estoque Ideal",
    linestyle=":",
    alpha=0.7,
)
ax.set_title(f"Estoque vs Demanda - {centro_escolhido} - {produto_escolhido}")
ax.set_xlabel("Data")
ax.set_ylabel("Quantidade")
ax.legend()
ax.grid(True)
st.pyplot(fig)

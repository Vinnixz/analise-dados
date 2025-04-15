import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@st.cache_data
def gerar_planilha_dados():
    np.random.seed(42)
    centros = ["São Paulo", "Recife", "Brasília", "Belém", "Florianópolis"]
    produtos = ["Memória RAM", "Placa Mãe", "Processador", "HD", "SSD"]
    dias = pd.date_range(start="2025-04-01", periods=10)

    dados = []
    for centro in centros:
        capacidade_maxima = int(np.random.randint(1000, 2000))
        tempo_processamento = int(round(np.random.uniform(1.0, 2.5)))
        custo_operacional = int(round(np.random.uniform(1000, 3000)))

        for produto in produtos:
            for dia in dias:
                estoque = int(np.random.randint(50, 200))
                demanda = int(np.random.randint(60, 180))
                lead_time = int(np.random.randint(2, 6))
                custo_armazenagem = int(np.random.randint(1, 3))
                custo_ruptura = int(np.random.randint(5, 11))
                valor_unitario = int(np.random.randint(200, 2000))

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
                        "valor_unitario": valor_unitario,
                        "capacidade_maxima": capacidade_maxima,
                        "tempo_processamento": tempo_processamento,
                        "custo_operacional": custo_operacional,
                    }
                )

    df = pd.DataFrame(dados)

    df["quantidade_recomendada"] = (
        df.get("quantidade_recomendada", pd.Series(dtype=float))
        .round(0)
        .astype("Int64")
    )
    df["estoque_ideal"] = (
        df.get("estoque_ideal", pd.Series(dtype=float)).round(0).astype("Int64")
    )

    df.to_csv("dados_estoque.csv", index=False)
    return df


st.title("📦 Sistema Inteligente de Recomendação de Estoque")

df = gerar_planilha_dados()

st.sidebar.header("🔍 Filtros")
centro_escolhido = st.sidebar.selectbox("Centro de Distribuição", df["centro"].unique())
produto_escolhido = st.sidebar.selectbox("Produto", df["produto"].unique())
margem = st.sidebar.slider("Margem de Segurança (%)", 0, 100, 20) / 100

df_filtrado = df[
    (df["centro"] == centro_escolhido) & (df["produto"] == produto_escolhido)
].copy()

dias_planejamento = 7
df_filtrado["demanda_total"] = df_filtrado["demanda_prevista"] * (1 + margem)
df_filtrado["buffer"] = df_filtrado["lead_time_dias"] * (
    df_filtrado["demanda_prevista"] / dias_planejamento
)
df_filtrado["estoque_ideal"] = df_filtrado["demanda_total"] + df_filtrado["buffer"]
df_filtrado["quantidade_recomendada"] = (
    df_filtrado["estoque_ideal"] - df_filtrado["estoque_atual"]
).clip(lower=0)

df_filtrado["demanda_total"] = df_filtrado["demanda_total"].round(0).astype("Int64")
df_filtrado["buffer"] = df_filtrado["buffer"].round(1)
df_filtrado["quantidade_recomendada"] = (
    df_filtrado["quantidade_recomendada"].round(0).astype("Int64")
)
df_filtrado["estoque_ideal"] = df_filtrado["estoque_ideal"].round(0).astype("Int64")

df_filtrado["custo_total"] = (
    df_filtrado["estoque_atual"] * df_filtrado["custo_armazenagem"]
) + (
    (df_filtrado["demanda_total"] - df_filtrado["estoque_atual"]).clip(lower=0)
    * df_filtrado["custo_ruptura"]
)

df_filtrado["custo_total"] = df_filtrado["custo_total"].apply(lambda x: f"R${x:,.2f}")

st.subheader(f"📊 Dados de {produto_escolhido} - {centro_escolhido}")
df_filtrado_show = df_filtrado[
    [
        "data",
        "estoque_atual",
        "demanda_prevista",
        "lead_time_dias",
        "demanda_total",
        "buffer",
        "estoque_ideal",
        "quantidade_recomendada",
        "custo_total",
    ]
]
df_filtrado_show["data"] = df_filtrado_show["data"].dt.strftime("%d/%m/%Y")
st.dataframe(df_filtrado_show, use_container_width=True)

st.subheader("📈 Visualizações")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    df_filtrado_show["data"],
    df_filtrado_show["estoque_atual"],
    label="Estoque Atual",
    marker="o",
)
ax.plot(
    df_filtrado_show["data"],
    df_filtrado_show["demanda_prevista"],
    label="Demanda Prevista",
    marker="x",
)
ax.plot(
    df_filtrado_show["data"],
    df_filtrado_show["quantidade_recomendada"],
    label="Reposição Recomendada",
    linestyle="--",
)
ax.plot(
    df_filtrado_show["data"],
    df_filtrado_show["estoque_ideal"],
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

with st.expander("ℹ️ Explicações e Metodologia"):
    st.markdown(
        """
    **Parâmetros Considerados:**
    - Margem de Segurança ajustável.
    - Cálculo de Estoque Ideal = Demanda Total + Buffer.
    - Reposição Recomendada = Estoque Ideal - Estoque Atual (mínimo 0).
    - Custo Total = Armazenagem + Custo de Ruptura.

    **Variáveis adicionais:**
    - Capacidade Máxima do Centro
    - Tempo de Processamento
    - Custo Operacional
    """
    )

# 📦 Gestão Inteligente de Estoque com Algoritmos de Recomendação

Projeto desenvolvido como parte de um projeto universitário, com o objetivo de aplicar algoritmos de recomendação para otimizar o controle de estoque em centros de distribuição.

🔗 **Acesse o projeto online aqui:**  
👉 [Abrir App no Streamlit](https://cjlyutdjboleyqkecmbtvr.streamlit.app/#13e204d7)

---

## 🎯 Objetivo

Criar uma ferramenta interativa para auxiliar na tomada de decisões sobre reposição de estoque, considerando:

- Demanda prevista
- Tempo médio de entrega (lead time)
- Margem de segurança
- Custos de armazenagem e ruptura

---

## 🧠 Lógica da Recomendação

A recomendação é feita com base em três principais componentes:

- **Demanda Total:**  
  Inclui uma margem de segurança de 20% sobre a demanda prevista.
  
  `demanda_total = demanda_prevista * 1.2`

- **Buffer de Segurança:**  
  Quantidade extra de estoque proporcional ao tempo de entrega.  
  
  `buffer = lead_time_dias * (demanda_prevista / 7)`

- **Estoque Ideal:**  
  Soma da demanda total + buffer.

  `estoque_ideal = demanda_total + buffer`

- **Quantidade Recomendada:**  
  Se o estoque atual estiver abaixo do ideal, calcula-se quanto deve ser comprado ou produzido.

  `quantidade_recomendada = max(0, estoque_ideal - estoque_atual)`

---

## 📊 Funcionalidades

- Filtro por centro de distribuição e produto
- Tabela interativa com os dados de simulação
- Gráfico com:
  - Estoque atual
  - Demanda prevista
  - Reposição recomendada
- Explicações interativas via botão “❓ Explicações do Sistema”

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

---


---

## ▶️ Como Executar Localmente

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-projeto.git
   cd seu-projeto

2. Crie uma venv
   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

3. Instale as dependências
    ```bash
    pip install -r requirements.txt

4. Rode o projeto
   ```bash
    streamlit run app.py
ou
  ```bash
  python -m streamlit run app.py

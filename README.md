# 📊 Sistema de Gestão de Ativos de TI

Uma aplicação desktop simples, desenvolvida em Python, para o gerenciamento e controle de ativos de TI (como notebooks, celulares e linhas telefônicas) de uma empresa.

## 🚀 Funcionalidades Principais

* **Listagem de Ativos:** Visualiza todos os ativos cadastrados em uma tabela organizada.
* **Operações CRUD:**
    * **Adicionar:** Cadastra novos ativos no banco de dados.
    * **Editar:** Atualiza informações de ativos existentes.
    * **Remover:** Exclui ativos do registro.
* **Busca Inteligente:** Permite buscar por qualquer termo em todas as colunas do banco de dados.
* **Ordenação:** Clicar no título de qualquer coluna ordena os dados (ascendente/descendente).
* **Interface Limpa:** Interface gráfica amigável construída com `ttkbootstrap`.

---

## 🔧 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica (GUI):**
    * `Tkinter` (biblioteca padrão do Python)
    * `ttkbootstrap` (para aplicar temas modernos ao Tkinter)
* **Banco de Dados:**
    * `SQLite3` (banco de dados local, leve e sem necessidade de servidor)

---

## 🏃‍♂️ Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone
    cd
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    python -m venv venv
    ```
    * No Windows: `.\venv\Scripts\activate`
    * No Linux/Mac: `source venv/bin/activate`

3.  **Instale as dependências:**
    O único requisito externo é o `ttkbootstrap`.
    ```bash
    pip install ttkbootstrap
    ```

4.  **Execute a aplicação:**
    ```bash
    python main.py
    ```
    O programa será iniciado e o banco de dados `ativos.db` será criado automaticamente na primeira execução.

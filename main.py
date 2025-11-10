import tkinter as tk
from tkinter import messagebox
import sqlite3
import database
import interface
import ttkbootstrap as ttk

class AssetManagerApp:
    def __init__(self, root):
        self.db = database
        self.ui = interface.MainApplicationUI(root, self)
        
        self.coluna_ordenacao_atual = "usuario_responsavel"
        self.ordem_atual = "ASC"
        self.id_original_em_edicao = None
        
        self.db.criar_tabela()
        status_insercao = self.db.inserir_dados_iniciais()
        if status_insercao and "Sucesso" in status_insercao:
            messagebox.showinfo("Inicialização do Banco", status_insercao)
        
        self.atualizar_lista_de_ativos()

    def atualizar_lista_de_ativos(self):
        try:
            ativos = self.db.listar_ativos(self.coluna_ordenacao_atual, self.ordem_atual)
            self.ui.popular_tabela(ativos)
            self.limpar_e_resetar()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os ativos: {e}")

    def ordenar_tabela(self, coluna):
        if self.coluna_ordenacao_atual == coluna:
            self.ordem_atual = "DESC" if self.ordem_atual == "ASC" else "ASC"
        else:
            self.coluna_ordenacao_atual = coluna
            self.ordem_atual = "ASC"
        self.atualizar_lista_de_ativos()

    def preparar_novo_ativo(self):
        self.limpar_e_resetar()
        self.ui.gerenciar_estado_campos(habilitar=True)
        self.ui.gerenciar_estado_botoes('adicionando')

    def editar_ativo(self):
        item_selecionado = self.ui.obter_item_selecionado()
        if not item_selecionado:
            messagebox.showwarning("Nenhum Item", "Por favor, selecione um item para editar.")
            return
            
        valores = self.ui.obter_valores_do_item(item_selecionado)
        self.id_original_em_edicao = valores[0]

        self.ui.gerenciar_estado_campos(habilitar=True)
        self.ui.gerenciar_estado_botoes('editando')

    def salvar(self):
        dados = self.ui.obter_dados_dos_campos()
        id_dispositivo_novo = dados.get("ids_dispositivos")

        if not id_dispositivo_novo:
            messagebox.showwarning("Campo Obrigatório", "O campo 'ID Dispositivo' é obrigatório.")
            return
        
        try:
            if self.id_original_em_edicao:
                self.db.atualizar_ativo(self.id_original_em_edicao, dados)
                messagebox.showinfo("Sucesso", "Ativo atualizado com sucesso!")
            else:
                self.db.adicionar_ativo(dados)
                messagebox.showinfo("Sucesso", "Ativo adicionado com sucesso!")
            
            self.atualizar_lista_de_ativos()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", f"O ID '{id_dispositivo_novo}' já existe.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar ativo: {e}")

    def remover(self):
        item_selecionado = self.ui.obter_item_selecionado()
        if not item_selecionado:
            messagebox.showwarning("Nenhum Item", "Selecione um item para remover.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover o ativo?"):
            id_para_remover = self.ui.obter_valores_do_item(item_selecionado)[0]
            try:
                self.db.remover_ativo(id_para_remover)
                messagebox.showinfo("Sucesso", "Ativo removido!")
                self.atualizar_lista_de_ativos()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao remover ativo: {e}")
    
    def buscar(self):
        termo = self.ui.obter_termo_busca()
        if not termo:
            return
        try:
            resultados = self.db.buscar_ativos(termo, self.coluna_ordenacao_atual, self.ordem_atual)
            self.ui.popular_tabela(resultados)
            if not resultados:
                messagebox.showinfo("Busca", "Nenhum resultado encontrado.")
        except Exception as e:
            messagebox.showerror("Erro de Busca", f"Ocorreu um erro ao buscar: {e}")

    def limpar_busca(self):
        self.ui.limpar_campo_busca()
        self.atualizar_lista_de_ativos()
        
    def limpar_e_resetar(self):
        self.id_original_em_edicao = None
        self.ui.preencher_campos([])
        self.ui.gerenciar_estado_campos(habilitar=False)
        self.ui.gerenciar_estado_botoes('inicial')
        if self.ui.tree.selection():
            self.ui.tree.selection_remove(self.ui.tree.selection()[0])

    def item_selecionado_na_tabela(self, event):
        item = self.ui.obter_item_selecionado()
        if not item: return
        self.id_original_em_edicao = None 
        valores = self.ui.obter_valores_do_item(item)
        self.ui.preencher_campos(valores)
        self.ui.gerenciar_estado_campos(habilitar=False)
        self.ui.gerenciar_estado_botoes('selecionado')

if __name__ == "__main__":
    root = tk.Tk()
    app = AssetManagerApp(root)
    root.mainloop()
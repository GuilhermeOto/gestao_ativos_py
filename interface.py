import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import messagebox

class MainApplicationUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Sistema de Gestão de Ativos")
        self.root.geometry("1280x720")
        self._criar_widgets()

    def _criar_widgets(self):
        frame_controles = ttk.Frame(self.root, padding="10")
        frame_controles.pack(fill=tk.X)
        style = ttk.Style()
        default_font = ("Arial", 12)
        style.configure('.', font=default_font)
        style.configure('Treeview.Heading', font=(default_font[0], default_font[1], 'bold'))
        style.configure('Treeview', rowheight=30)        
        
        self.colunas_map = {
            "ids_dispositivos": "ID Dispositivo", "tipo_dispositivo": "Tipo", "marca_modelo": "Marca/Modelo",
            "status_propriedade": "Próprio/Alugado", "usuario_responsavel": "Usuário", "possui_celular": "Possui Celular",
            "email": "Email", "linhas_telefonicas": "Linhas", "situacao_equipamento": "Situação Equip.",
            "situacao_linha": "Situação Linha", "empresa_alugados": "Empresa Aluguel", "imei1": "IMEI 1", "imei2": "IMEI 2"
        }
        
        self.entradas = {}
        frame_entradas = ttk.Frame(frame_controles)
        frame_entradas.pack(fill=tk.X)
        
        campos_por_linha = 7
        for i, (key, label_text) in enumerate(self.colunas_map.items()):
            frame_campo = ttk.Frame(frame_entradas)
            linha = 0 if i < campos_por_linha else 2
            coluna = i if i < campos_por_linha else i - campos_por_linha
            frame_campo.grid(row=linha, column=coluna, padx=5, pady=2, sticky='w')
            
            label = ttk.Label(frame_campo, text=label_text)
            label.pack(side=tk.TOP, anchor='w')
            entry = ttk.Entry(frame_campo, width=25)
            entry.pack(side=tk.TOP, fill=tk.X)
            entry.config(state='readonly')
            self.entradas[key] = entry

        frame_acoes = ttk.Frame(frame_controles, padding="10 0")
        frame_acoes.pack(fill=tk.X, pady=10)

        self.botao_adicionar = ttk.Button(frame_acoes, text="Adicionar Novo", command=self.controller.preparar_novo_ativo)
        self.botao_adicionar.pack(side=tk.LEFT, padx=(0, 5))
        
        self.botao_editar = ttk.Button(frame_acoes, text="Editar", command=self.controller.editar_ativo)
        self.botao_editar.pack(side=tk.LEFT, padx=5)
        
        self.botao_salvar = ttk.Button(frame_acoes, text="Salvar Alterações", command=self.controller.salvar)
        self.botao_salvar.pack(side=tk.LEFT, padx=5)

        self.botao_remover = ttk.Button(frame_acoes, text="Remover", command=self.controller.remover)
        self.botao_remover.pack(side=tk.LEFT, padx=5)
        
        self.botao_limpar = ttk.Button(frame_acoes, text="Cancelar", command=self.controller.limpar_e_resetar)
        self.botao_limpar.pack(side=tk.LEFT, padx=5)

        self.botao_recarregar = ttk.Button(frame_acoes, text="Atualizar Lista", command=self.controller.atualizar_lista_de_ativos)
        self.botao_recarregar.pack(side=tk.LEFT, padx=5)
        
        spacer = ttk.Frame(frame_acoes)
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.campo_busca = ttk.Entry(frame_acoes, width=40)
        self.campo_busca.pack(side=tk.LEFT, fill=tk.X, padx=(0, 5))
        self.botao_buscar = ttk.Button(frame_acoes, text="Buscar", command=self.controller.buscar)
        self.botao_buscar.pack(side=tk.LEFT)
        self.botao_limpar_busca = ttk.Button(frame_acoes, text="Mostrar Todos", command=self.controller.limpar_busca)
        self.botao_limpar_busca.pack(side=tk.LEFT, padx=(5,0))

        frame_tabela = ttk.Frame(self.root, padding="10")
        frame_tabela.pack(expand=True, fill=tk.BOTH)

        scrollbar_y = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(frame_tabela, columns=list(self.colunas_map.keys()), show='headings',
                                 yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        for key, text in self.colunas_map.items():
            self.tree.heading(key, text=text, command=lambda k=key: self.controller.ordenar_tabela(k))
            self.tree.column(key, width=120, anchor='w')
        
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind('<<TreeviewSelect>>', self.controller.item_selecionado_na_tabela)
        self.root.bind('<Configure>', self._redimensionar_colunas)
        
    def _redimensionar_colunas(self, event=None):
        largura_total = self.tree.winfo_width()
        if largura_total <= 1:
            return
        num_colunas = len(self.colunas_map)
        largura_coluna = max(int(largura_total / num_colunas), 80)
        for key in self.colunas_map.keys():
            self.tree.column(key, width=largura_coluna)
        colunas = list(self.colunas_map.keys())
        num_colunas = len(colunas)
        larguras_minimas = {
            "ids_dispositivos": 120,
            "usuario_responsavel": 150,
            "marca_modelo": 150,
            "email": 180
        }
        if self.tree.winfo_ismapped() and self.tree.yview() != (0.0, 1.0):
             largura_total -= 18
        largura_media = largura_total / num_colunas

        for col in colunas:
            largura_min = larguras_minimas.get(col, 80)
            largura_final = max(int(largura_media), largura_min)
            self.tree.column(col, width=largura_final, anchor='w')
             
    def gerenciar_estado_campos(self, habilitar=False):
        for entry in self.entradas.values():
            entry.config(state='normal' if habilitar else 'readonly')

    def gerenciar_estado_botoes(self, estado):
        if estado == 'inicial':
            self.botao_adicionar.config(state='normal')
            self.botao_editar.config(state='disabled')
            self.botao_salvar.config(state='disabled')
            self.botao_remover.config(state='disabled')
        elif estado == 'selecionado':
            self.botao_adicionar.config(state='normal')
            self.botao_editar.config(state='normal')
            self.botao_salvar.config(state='disabled')
            self.botao_remover.config(state='normal')
        elif estado == 'editando' or estado == 'adicionando':
            self.botao_adicionar.config(state='disabled')
            self.botao_editar.config(state='disabled')
            self.botao_salvar.config(state='normal')
            self.botao_remover.config(state='disabled')

    def popular_tabela(self, dados):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in dados:
            self.tree.insert('', 'end', values=row)

    def obter_dados_dos_campos(self):
        return {key: entry.get() for key, entry in self.entradas.items()}

    def preencher_campos(self, valores):
        self.gerenciar_estado_campos(habilitar=True) 
        self.limpar_campos()
        for i, key in enumerate(self.entradas.keys()):
            if i < len(valores):
                valor_str = valores[i] if valores[i] is not None else ""
                self.entradas[key].insert(0, valor_str)
    
    def limpar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
            
    def obter_item_selecionado(self):
        selection = self.tree.selection()
        return selection[0] if selection else None
    
    def obter_valores_do_item(self, item):
        return self.tree.item(item, 'values')

    def obter_termo_busca(self):
        return self.campo_busca.get()

    def limpar_campo_busca(self):
        self.campo_busca.delete(0, tk.END)
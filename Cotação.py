import requests 
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class CotacaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Atualização de Cotações")

        self.label = tk.Label(root, text="Cotações Atuais")
        self.label.pack(pady=10)
        
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Moeda", "Cotação", "Última Atualização")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Moeda", anchor=tk.W, width=100)
        self.tree.column("Cotação", anchor=tk.W, width=100)
        self.tree.column("Última Atualização", anchor=tk.W, width=150)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Moeda", text="Moeda", anchor=tk.W)
        self.tree.heading("Cotação", text="Cotação", anchor=tk.W)
        self.tree.heading("Última Atualização", text="Última Atualização", anchor=tk.W)

        self.tree.pack(padx=10, pady=10)

        self.update_button = tk.Button(root, text="Atualizar Cotações", command=self.atualizar_cotacoes)
        self.update_button.pack(pady=10)

        # Inicializa a tabela com valores padrão
        self.atualizar_cotacoes()

    def obter_cotacoes(self):
        requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,BTC-BRL,ETH-BRL,CNY-BRL,EUR-BRL")
        requisicao_dic = requisicao.json()

        cotacao_dolar = round(float(requisicao_dic["USDBRL"]["bid"]), 2)
        cotacao_btc = float(requisicao_dic["BTCBRL"]["bid"])
        cotacao_eth = float(requisicao_dic["ETHBRL"]["bid"]) 
        cotacao_euro = round(float(requisicao_dic["EURBRL"]["bid"]),2)
        cotacao_yuan = round(float(requisicao_dic["CNYBRL"]["bid"]),2)

        data_atualizacao = datetime.now()

        return [
            {"Moeda": "USD", "Cotação": cotacao_dolar, "Última Atualização": data_atualizacao},
            {"Moeda": "EUR", "Cotação": cotacao_euro, "Última Atualização": data_atualizacao},
            {"Moeda": "BTC", "Cotação": cotacao_btc, "Última Atualização": data_atualizacao},
            {"Moeda": "ETHER", "Cotação": cotacao_eth, "Última Atualização": data_atualizacao},
            {"Moeda": "CNY", "Cotação": cotacao_yuan, "Última Atualização": data_atualizacao},
        ]

    def atualizar_cotacoes(self):
        cotacoes = self.obter_cotacoes()

        # Limpa a tabela antes de atualizar
        for row in self.tree.get_children():
            self.tree.delete(row)

        for cotacao in cotacoes:
            self.tree.insert("", tk.END, values=(cotacao["Moeda"], cotacao["Cotação"], cotacao["Última Atualização"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = CotacaoApp(root)
    root.mainloop()
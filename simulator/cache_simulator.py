import tkinter as tk
from tkinter import ttk
import random

class CacheSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Cache")

        # Configurações iniciais
        self.db = {i: value for i, value in enumerate(["gato", "lobo", "sapo", "rato", "pato", "lince", "leão", "urso", "anta", "tatu"], 1)}
        self.cache = []
        self.cache_size = 5
        self.policy = "FIFO"
        self.cache_hits = 0
        self.cache_misses = 0
        self.usage_order = []  # Para LRU
        self.access_count = {}  # Para LFU

        # Configuração da interface
        self.create_interface()

    def create_interface(self):
        # Seleção de algoritmo
        frame_algorithms = tk.Frame(self.root)
        frame_algorithms.pack(pady=10)
        
        tk.Label(frame_algorithms, text="Algoritmo:").grid(row=0, column=0, sticky="w")
        self.algorithm_var = tk.StringVar(value="FIFO")
        
        for i, algo in enumerate(["FIFO", "LFU", "LRU"]):
            tk.Radiobutton(frame_algorithms, text=algo, variable=self.algorithm_var, value=algo, command=self.set_policy).grid(row=0, column=i + 1, sticky="w")

        # Exibição de item atual
        self.current_item_label = tk.Label(self.root, text="Item Atual: -")
        self.current_item_label.pack(pady=5)

        # Botão de gerar pedidos
        self.generate_button = tk.Button(self.root, text="Gerar Pedidos", command=self.generate_request)
        self.generate_button.pack(pady=5)

        # Tabelas
        frame_tables = tk.Frame(self.root)
        frame_tables.pack(pady=10)

        # Tabela de cache
        cache_frame = tk.Frame(frame_tables)
        cache_frame.pack(side="left", padx=10)
        tk.Label(cache_frame, text="CACHE").pack()

        self.cache_table = ttk.Treeview(cache_frame, columns=("Key", "Value"), show="headings", height=5)
        self.cache_table.heading("Key", text="Key")
        self.cache_table.heading("Value", text="Value")
        self.cache_table.pack()

        # Tabela de banco de dados
        db_frame = tk.Frame(frame_tables)
        db_frame.pack(side="left", padx=10)
        tk.Label(db_frame, text="Banco").pack()

        self.db_table = ttk.Treeview(db_frame, columns=("Key", "Value"), show="headings", height=10)
        self.db_table.heading("Key", text="Key")
        self.db_table.heading("Value", text="Value")
        self.db_table.pack()

        for key, value in self.db.items():
            self.db_table.insert("", "end", values=(key, value))

        # Estatísticas
        self.stats_label = tk.Label(self.root, text="Cache MISS: 0    Cache HIT: 0")
        self.stats_label.pack(pady=5)

        self.update_cache_table()

    def set_policy(self):
        self.policy = self.algorithm_var.get()

    def generate_request(self):
        # Gera um item aleatório do banco de dados
        item_key = random.choice(list(self.db.keys()))
        item_value = self.db[item_key]
        self.current_item_label.config(text=f"Item Atual: {item_key} - {item_value}")
        self.access_data(item_key, item_value)

    def access_data(self, key, value):
        if key in [item["key"] for item in self.cache]:
            self.cache_hits += 1
            print(f"Cache HIT: {key} - {value}")
            if self.policy == "LRU":
                self.usage_order.remove(key)
                self.usage_order.append(key)
            if self.policy == "LFU":
                self.access_count[key] += 1
        else:
            self.cache_misses += 1
            print(f"Cache MISS: {key} - {value}")
            self.load_to_cache(key, value)

        self.update_stats()
        self.update_cache_table()

    def load_to_cache(self, key, value):
        if len(self.cache) < self.cache_size:
            self.cache.append({"key": key, "value": value})
        else:
            self.replace_data(key, value)

        if self.policy == "LRU":
            self.usage_order.append(key)
        if self.policy == "LFU":
            self.access_count[key] = 1

    def replace_data(self, key, value):
        if self.policy == "FIFO":
            removed = self.cache.pop(0)
        elif self.policy == "LRU":
            lru_key = self.usage_order.pop(0)
            removed = next(item for item in self.cache if item["key"] == lru_key)
            self.cache.remove(removed)
        elif self.policy == "LFU":
            least_frequent = min(self.access_count, key=self.access_count.get)
            removed = next(item for item in self.cache if item["key"] == least_frequent)
            self.cache.remove(removed)
            del self.access_count[least_frequent]

        print(f"Substituindo {removed['key']} - {removed['value']} por {key} - {value}")
        self.cache.append({"key": key, "value": value})

    def update_cache_table(self):
        for row in self.cache_table.get_children():
            self.cache_table.delete(row)
        for i, item in enumerate(self.cache, 1):
            self.cache_table.insert("", "end", values=(i, item["value"]))

    def update_stats(self):
        self.stats_label.config(text=f"Cache MISS: {self.cache_misses}    Cache HIT: {self.cache_hits}")

# Criar a janela principal
root = tk.Tk()
app = CacheSimulatorGUI(root)
root.mainloop()

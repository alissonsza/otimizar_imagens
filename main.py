import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from otimizar import otimizar_imagem

class OtimizadorApp:
    def __init__(self, master):
        self.master = master
        master.title("Otimizador de Imagens")
        master.geometry("520x400")
        master.resizable(False, False)

        self.pasta_saida = ""

        # Frame principal para conteúdo
        self.frame_conteudo = tk.Frame(master)
        self.frame_conteudo.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Título
        self.label_titulo = tk.Label(self.frame_conteudo, text="Otimizador de Imagens em Lote", font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        # Botão Selecionar Pasta de Saída
        self.btn_pasta = tk.Button(self.frame_conteudo, text="Selecionar Pasta de Saída", font=("Arial", 11), command=self.selecionar_pasta)
        self.btn_pasta.pack()

        # Label com caminho da pasta
        self.label_pasta = tk.Label(self.frame_conteudo, text="Nenhuma pasta selecionada", fg="gray")
        self.label_pasta.pack(pady=5)

        # Botão Selecionar Imagens
        self.btn_selecionar = tk.Button(self.frame_conteudo, text="Selecionar Imagens para Otimizar", font=("Arial", 12), command=self.selecionar_imagens)
        self.btn_selecionar.pack(pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(self.frame_conteudo, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Caixa de resultados
        self.resultado = tk.Text(self.frame_conteudo, height=8, state="disabled", bg="#f4f4f4")
        self.resultado.pack(padx=5, pady=10, fill="both", expand=True)

        # RODAPÉ
        self.label_rodape = tk.Label(
            master,
            text="Desenvolvido por: B5AS - TIC PBIO",
            font=("Arial", 9),
            fg="gray"
        )
        self.label_rodape.pack(side="bottom", pady=3)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta de saída")
        if pasta:
            self.pasta_saida = pasta
            self.label_pasta.config(text=f"Pasta: {pasta}", fg="black")

    def selecionar_imagens(self):
        if not self.pasta_saida:
            messagebox.showwarning("Aviso", "Por favor, selecione a pasta de saída antes de continuar.")
            return

        arquivos = filedialog.askopenfilenames(
            title="Selecione imagens",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
        )

        if not arquivos:
            return

        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        self.progress["value"] = 0
        self.progress["maximum"] = len(arquivos)

        sucesso = 0
        for i, caminho in enumerate(arquivos):
            nome = os.path.basename(caminho)
            destino = os.path.join(self.pasta_saida, nome)

            ok, tamanho_antigo, tamanho_novo = otimizar_imagem(caminho, destino)

            if ok:
                sucesso += 1
                reducao = tamanho_antigo - tamanho_novo
                porcentagem = (reducao / tamanho_antigo) * 100 if tamanho_antigo > 0 else 0
                self.resultado.insert(tk.END, f"{nome}\n ↪ De {tamanho_antigo:.1f} KB → {tamanho_novo:.1f} KB ({porcentagem:.1f}% de redução)\n\n")
            else:
                self.resultado.insert(tk.END, f"{nome} - erro ao otimizar.\n\n")

            self.progress["value"] = i + 1
            self.master.update_idletasks()

        self.resultado.insert(tk.END, f"✅ {sucesso} de {len(arquivos)} imagem(ns) otimizadas com sucesso.")
        self.resultado.config(state="disabled")
        messagebox.showinfo("Finalizado", "Otimização concluída!")

# Iniciar app
if __name__ == "__main__":
    root = tk.Tk()
    app = OtimizadorApp(root)
    root.mainloop()

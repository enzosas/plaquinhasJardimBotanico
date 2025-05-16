import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
from placa import gera_placa

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Mapeamento interface e backend
layout_display_to_value = {
    "Layout 0": "layout0",
    "Layout 1": "layout1",
    "Layout 2": "layout2"
}

# Função do botão
def gerar_placa_botao():
    nomePop = entry_nomePop.get()
    nomeCie = entry_nomeCie.get()
    codigo = entry_codigo.get()
    url = entry_url.get()
    layout_display = combo_layout.get()

    layout = layout_display_to_value.get(layout_display)

    if not all([nomePop, nomeCie, codigo, url, layout]):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    try:
        gera_placa(nomePop, nomeCie, codigo, url, layout)
        messagebox.showinfo("Sucesso", f"Plaquinha de {nomePop} gerada!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Janela principal
app = ctk.CTk()
app.title("Gerador de Plaquinha Jardim Botânico UFSM")
app.resizable(False, False)

# Frame do Título
frame_titulo = ctk.CTkFrame(app, fg_color="#506C44")
frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

label_titulo = ctk.CTkLabel(frame_titulo, text="Gerador de Plaquinhas", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
label_titulo.pack(padx=20, pady=15)

# Frame do conteúdo
frame_conteudo = ctk.CTkFrame(app)
frame_conteudo.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Nome Popular
entry_nomePop = ctk.CTkEntry(frame_conteudo, placeholder_text="Nome Popular")
entry_nomePop.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

# Nome Científico
entry_nomeCie = ctk.CTkEntry(frame_conteudo, placeholder_text="Nome Científico")
entry_nomeCie.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# Código
entry_codigo = ctk.CTkEntry(frame_conteudo, placeholder_text="Código")
entry_codigo.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

# URL
entry_url = ctk.CTkEntry(frame_conteudo, placeholder_text="URL para QR Code")
entry_url.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

# Layout
combo_layout = ctk.CTkComboBox(frame_conteudo, values=list(layout_display_to_value.keys()), state="readonly")
combo_layout.set("Layout 0")
combo_layout.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

# Botão
botao_gerar = ctk.CTkButton(frame_conteudo, text="Gerar Plaquinha", command=gerar_placa_botao)
botao_gerar.grid(row=5, column=0, padx=20, pady=20)

# Ajustes de expansão
frame_conteudo.columnconfigure(0, weight=1)
app.columnconfigure(0, weight=1)

# Executa a interface
app.mainloop()

import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog as fd
from placa import gera_placa

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

VERDEPLACA = "#506C44"

# Mapeamento interface e backend
layout_display_to_value = {
    "Layout Quadrado": "layout0",
    "Layout Retangular": "layout1",
    "Layout QR Grande": "layout2"
}

# Funcao do botao
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
    
    # Abre janela para escolher diretorio
    diretorio_saida = fd.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")],
        initialfile=f"placa-{nomePop}.pdf",
        title="Salvar Plaquinha Como"
    )
    if not diretorio_saida:  # Usuario cancelou
        return

    try:
        gera_placa(nomePop, nomeCie, codigo, url, layout, diretorio_saida=diretorio_saida)
    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Janela principal
app = ctk.CTk()
app.title("Gerador de Plaquinha")
app.resizable(False, False)

# Frame do Titulo
frame_titulo = ctk.CTkFrame(app, fg_color=VERDEPLACA)
frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

label_titulo = ctk.CTkLabel(
    frame_titulo,
    text="Gerador de Plaquinha",
    font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
    text_color="white"
)
label_titulo.pack(padx=20, pady=15)

# Frame do conteudo
frame_conteudo = ctk.CTkFrame(app, fg_color="white")
frame_conteudo.grid(row=1, column=0, sticky="new", padx=10, pady=(0, 10))

# Nome Popular
label_nomePop = ctk.CTkLabel(
    frame_conteudo,
    text="Nome Popular",
    text_color="black",
    font=ctk.CTkFont(family="Helvetica", size=14)
)
label_nomePop.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")

entry_nomePop = ctk.CTkEntry(frame_conteudo, fg_color="white", border_color=VERDEPLACA)
entry_nomePop.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

# Nome Científico
label_nomeCie = ctk.CTkLabel(
    frame_conteudo,
    text="Nome Científico",
    text_color="black",
    font=ctk.CTkFont(family="Helvetica", size=14)
)
label_nomeCie.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

entry_nomeCie = ctk.CTkEntry(frame_conteudo, fg_color="white", border_color=VERDEPLACA)
entry_nomeCie.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

# Código
label_codigo = ctk.CTkLabel(
    frame_conteudo,
    text="Código",
    text_color="black",
    font=ctk.CTkFont(family="Helvetica", size=14)
)
label_codigo.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")

entry_codigo = ctk.CTkEntry(frame_conteudo, fg_color="white", border_color=VERDEPLACA)
entry_codigo.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

# URL
label_url = ctk.CTkLabel(
    frame_conteudo,
    text="URL para QR Code",
    text_color="black",
    font=ctk.CTkFont(family="Helvetica", size=14)
)
label_url.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")

entry_url = ctk.CTkEntry(frame_conteudo, fg_color="white", border_color=VERDEPLACA)
entry_url.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")

# Layout
label_layout = ctk.CTkLabel(
    frame_conteudo,
    text="Layout da Plaquinha",
    text_color="black",
    font=ctk.CTkFont(family="Helvetica", size=14)
)
label_layout.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")

combo_layout = ctk.CTkComboBox(
    frame_conteudo,
    values=list(layout_display_to_value.keys()),
    state="readonly",
    fg_color="white",
    border_color=VERDEPLACA,
    button_color=VERDEPLACA
)
combo_layout.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

# Botão
botao_gerar = ctk.CTkButton(
    frame_conteudo,
    text="Gerar Plaquinha",
    command=gerar_placa_botao,
    fg_color=VERDEPLACA
)
botao_gerar.grid(row=10, column=0, padx=20, pady=20)

# Ajustes de expansão
frame_conteudo.columnconfigure(0, weight=1)
app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)

# Executa a interface
app.mainloop()

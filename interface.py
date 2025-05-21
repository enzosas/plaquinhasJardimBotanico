import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog as fd
from placa import gera_placa


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

# Cores
VERDEPLACA = "#506C44"
VERDEPLACADARK = "#405636"
CINZAFRENTE = "#CECECE"

# Mapeamento entre o texto exibido e o valor real do layout
layout_display_to_value = {
    "Layout Quadrado": "layout0",
    "Layout Retangular": "layout1",
    "Layout QR Grande": "layout2"
}

# Botao
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

    diretorio_saida = fd.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")],
        initialfile=f"placa-{nomePop}.pdf",
        title="Salvar Plaquinha Como"
    )
    if not diretorio_saida:
        return

    try:
        gera_placa(nomePop, nomeCie, codigo, url, layout, diretorio_saida=diretorio_saida)
    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Janela principal
app = ctk.CTk()
app.title("Gerador de Plaquinha")
app.resizable(False, False)

# Cabecalho
frame_titulo = ctk.CTkFrame(app, fg_color=VERDEPLACA)
frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

label_titulo = ctk.CTkLabel(
    frame_titulo,
    text="Gerador de Plaquinha",
    font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
    text_color="white"
)
label_titulo.pack(padx=20, pady=15)

# Abas
tabview = ctk.CTkTabview(
    app, fg_color="white", 
    segmented_button_selected_color=VERDEPLACA, 
    segmented_button_selected_hover_color=VERDEPLACADARK, 
    segmented_button_unselected_color=CINZAFRENTE, 
    segmented_button_unselected_hover_color=CINZAFRENTE,
    segmented_button_fg_color=CINZAFRENTE)
tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
tab_placa = tabview.add("Manual")
tab_sobre = tabview.add("Automático por ID")

# Aba Manual

# Nome Popular
label_nomePop = ctk.CTkLabel(tab_placa, text="Nome Popular", text_color="black")
label_nomePop.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
entry_nomePop = ctk.CTkEntry(tab_placa, fg_color="white", border_color=CINZAFRENTE)
entry_nomePop.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

# Nome Científico
label_nomeCie = ctk.CTkLabel(tab_placa, text="Nome Científico", text_color="black")
label_nomeCie.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
entry_nomeCie = ctk.CTkEntry(tab_placa, fg_color="white", border_color=CINZAFRENTE)
entry_nomeCie.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

# Código
label_codigo = ctk.CTkLabel(tab_placa, text="Código", text_color="black")
label_codigo.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
entry_codigo = ctk.CTkEntry(tab_placa, fg_color="white", border_color=CINZAFRENTE)
entry_codigo.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

# URL
label_url = ctk.CTkLabel(tab_placa, text="URL para QR Code", text_color="black")
label_url.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
entry_url = ctk.CTkEntry(tab_placa, fg_color="white", border_color=CINZAFRENTE)
entry_url.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")

# Layout
label_layout = ctk.CTkLabel(tab_placa, text="Layout da Plaquinha", text_color="black")
label_layout.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")
combo_layout = ctk.CTkComboBox(
    tab_placa,
    values=list(layout_display_to_value.keys()),
    state="readonly",
    fg_color="white",
    border_color=CINZAFRENTE,
    button_hover_color=VERDEPLACADARK,
    button_color=VERDEPLACA
)
combo_layout.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

# Botão de gerar
botao_gerar = ctk.CTkButton(
    tab_placa,
    text="Gerar Plaquinha",
    command=gerar_placa_botao,
    fg_color=VERDEPLACA,
    hover_color=VERDEPLACADARK
)
botao_gerar.grid(row=10, column=0, padx=20, pady=20)

# Ajuste da largura da coluna da aba para expandir com a janela
tab_placa.columnconfigure(0, weight=1)


# Aba Automatico


# Expansao da janela
app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)

# Loop principal
app.mainloop()

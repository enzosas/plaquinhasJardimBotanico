import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog as fd
from placa import gera_placa
from base_de_dados import pesquisar_por_id, buscar_nome_popular_wikidata, buscar_nome_popular_wikipedia


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

# Cores
VERDEPLACA = "#506C44"
VERDEPLACADARK = "#405636"
CINZAFRENTE = "#CECECE"
CINZADESABILITADO = "#7F7F7F"

# Mapeamento entre o texto exibido e o valor real do layout
layout_display_to_value = {
    "Layout Quadrado": "layout0",
    "Layout Retangular": "layout1",
    "Layout QR Grande": "layout2"
}

# Botao Manual
def gerar_placa_botao_manual():
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

# Botao Automatico
def gerar_placa_botao_automatico():
    nomePop = entry_nomePop2.get()
    nomeCie = entry_nomeCie2.get()
    url = entry_link2.get()
    layout_display = combo_layout2.get()
    layout = layout_display_to_value.get(layout_display)
    id = entry_digiteID.get()

    if not all([nomePop, nomeCie, url, layout, id]):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos e importe os dados corretamente.")
        return

    codigo = id.zfill(5)

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


# Preencher automaticamente apos pesquisa
def preencher_campos_automaticamente_id():
    id = entry_digiteID.get()
    if not id:
        messagebox.showwarning("ID ausente", "Digite um ID para buscar.")
        return
    
    try:
        dados = pesquisar_por_id(id)
        
        if dados is None:
            messagebox.showwarning("ID não encontrado", f"Nenhum dado encontrado para o ID '{id}'.")
            return

        genus = str(dados.get("genus", "")).strip()
        sp1 = str(dados.get("sp1", "")).strip()
        nomeCientifico = f"{genus} {sp1}"
        link = f"https://jbsm.inf.ufsm.br/acervo/item/{id.zfill(5)}"
        nomePopular = buscar_nome_popular_wikidata(nomeCientifico)
        wikipedia = buscar_nome_popular_wikipedia(nomeCientifico)

        if not nomePopular:
            nomePopular = "Desconhecido"

        # Preencher campos
        entry_nomePop2.delete(0, "end")
        entry_nomePop2.insert(0, nomePopular)

        entry_nomeCie2.configure(state="normal")
        entry_nomeCie2.delete(0, "end")
        entry_nomeCie2.insert(0, nomeCientifico)
        entry_nomeCie2.configure(state="readonly")

        entry_link2.configure(state="normal")
        entry_link2.delete(0, "end")
        entry_link2.insert(0, link)
        entry_link2.configure(state="readonly")

        entry_wikipedia.configure(state="normal")
        entry_wikipedia.delete("1.0", "end")         
        entry_wikipedia.insert("1.0", str(wikipedia))
        entry_wikipedia.configure(state="disabled") 

    except Exception as e:
        messagebox.showerror("Erro na busca", str(e))


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
tab_manual = tabview.add("Manual")
tab_automatico_id = tabview.add("Automático por ID")
tab_nome_cientifico = tabview.add("Automático por Nome Científico")






# Aba Manual

# Nome Popular
label_nomePop = ctk.CTkLabel(tab_manual, text="Nome Popular", text_color="black")
label_nomePop.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
entry_nomePop = ctk.CTkEntry(tab_manual, fg_color="white", border_color=CINZAFRENTE)
entry_nomePop.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

# Nome Científico
label_nomeCie = ctk.CTkLabel(tab_manual, text="Nome Científico", text_color="black")
label_nomeCie.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
entry_nomeCie = ctk.CTkEntry(tab_manual, fg_color="white", border_color=CINZAFRENTE)
entry_nomeCie.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

# Código
label_codigo = ctk.CTkLabel(tab_manual, text="Código", text_color="black")
label_codigo.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
entry_codigo = ctk.CTkEntry(tab_manual, fg_color="white", border_color=CINZAFRENTE)
entry_codigo.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

# URL
label_url = ctk.CTkLabel(tab_manual, text="URL para QR Code", text_color="black")
label_url.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
entry_url = ctk.CTkEntry(tab_manual, fg_color="white", border_color=CINZAFRENTE)
entry_url.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")

# Layout
label_layout = ctk.CTkLabel(tab_manual, text="Layout da Plaquinha", text_color="black")
label_layout.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")
combo_layout = ctk.CTkComboBox(
    tab_manual,
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
    tab_manual,
    text="Gerar Plaquinha",
    command=gerar_placa_botao_manual,
    fg_color=VERDEPLACA,
    hover_color=VERDEPLACADARK
)
botao_gerar.grid(row=10, column=0, padx=20, pady=20)

# Ajuste da largura da coluna da aba para expandir com a janela
tab_manual.columnconfigure(0, weight=1)





# Tab Automatico ID

contadorRow = 0

# Ajuste das colunas para expansão
tab_automatico_id.columnconfigure(0, weight=1)
tab_automatico_id.columnconfigure(1, weight=1)

# Digite o ID
label_digiteID = ctk.CTkLabel(tab_automatico_id, text="Digite o ID:", text_color="black")
label_digiteID.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="w")
contadorRow += 1
entry_digiteID = ctk.CTkEntry(tab_automatico_id, fg_color="white", border_color=CINZAFRENTE)
entry_digiteID.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow += 1

# Botao de pesquisar
botao_pesquisar = ctk.CTkButton(
    tab_automatico_id,
    text="Importar informações",
    command=preencher_campos_automaticamente_id,
    fg_color=VERDEPLACA,
    hover_color=VERDEPLACADARK
)
botao_pesquisar.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=20)
contadorRow += 1

# Nome Popular
label_nomePop2 = ctk.CTkLabel(tab_automatico_id, text="Nome Popular", text_color="black")
label_nomePop2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow += 1
entry_nomePop2 = ctk.CTkEntry(tab_automatico_id, fg_color="white", border_color=CINZAFRENTE)
entry_nomePop2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow += 1

# Nome Científico
label_nomeCie2 = ctk.CTkLabel(tab_automatico_id, text="Nome Científico", text_color="black")
label_nomeCie2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow += 1
entry_nomeCie2 = ctk.CTkEntry(tab_automatico_id, fg_color="white", border_color=CINZAFRENTE, state="readonly", text_color=CINZADESABILITADO)
entry_nomeCie2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow += 1

# Link
label_link2 = ctk.CTkLabel(tab_automatico_id, text="Link", text_color="black")
label_link2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow += 1
entry_link2 = ctk.CTkEntry(tab_automatico_id, fg_color="white", border_color=CINZAFRENTE, state="readonly", text_color=CINZADESABILITADO)
entry_link2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow += 1

# Layout
label_layout2 = ctk.CTkLabel(tab_automatico_id, text="Layout da Plaquinha", text_color="black")
label_layout2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow += 1
combo_layout2 = ctk.CTkComboBox(
    tab_automatico_id,
    values=list(layout_display_to_value.keys()),
    state="readonly",
    fg_color="white",
    border_color=CINZAFRENTE,
    button_hover_color=VERDEPLACADARK,
    button_color=VERDEPLACA
)
combo_layout2.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow += 1

# Botão de gerar
botao_gerar_automatico = ctk.CTkButton(
    tab_automatico_id,
    text="Gerar Plaquinha",
    command=gerar_placa_botao_automatico,
    fg_color=VERDEPLACA,
    hover_color=VERDEPLACADARK
)
botao_gerar_automatico.grid(row=contadorRow, column=0, columnspan=2, padx=20, pady=20)
contadorRow += 1

# Wikipedia
label_wikipedia = ctk.CTkLabel(tab_automatico_id, text="Pesquisa Wikipedia", text_color="black")
label_wikipedia.grid(row=0, column=2, columnspan=2, padx=20, pady=(10, 0), sticky="w")
entry_wikipedia = ctk.CTkTextbox(tab_automatico_id, fg_color="white", border_color=CINZAFRENTE, border_width=1, height=100, wrap="word")
entry_wikipedia.grid(row=1, column=2, columnspan=2, rowspan=10, padx=20, pady=(0, 10), sticky="nsew")
entry_wikipedia.configure(state="disabled")

# Ajuste da largura da coluna da aba para expandir com a janela
tab_automatico_id.columnconfigure(0, weight=1)

# Expansao da janela
app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)




# Tab Automatico Nome Cientifico

tab_nome_cientifico.columnconfigure(0, weight=1)
tab_nome_cientifico.columnconfigure(1, weight=1)

contadorRow3 = 0

# Campo Nome Científico (em vez de ID)
label_nomeCie3 = ctk.CTkLabel(tab_nome_cientifico, text="Nome Científico", text_color="black")
label_nomeCie3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="w")
contadorRow3 += 1
entry_nomeCie3 = ctk.CTkEntry(tab_nome_cientifico, fg_color="white", border_color=CINZAFRENTE)
entry_nomeCie3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow3 += 1

# Botão buscar informações
botao_pesquisar_nome = ctk.CTkButton(
    tab_nome_cientifico,
    text="Importar Informações",
    # command=preencher_por_nome_cientifico,
    fg_color=VERDEPLACA,
    hover_color=VERDEPLACADARK
)
botao_pesquisar_nome.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=20)
contadorRow3 += 1

# Campo Nome Popular
label_nomePop3 = ctk.CTkLabel(tab_nome_cientifico, text="Nome Popular", text_color="black")
label_nomePop3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow3 += 1
entry_nomePop3 = ctk.CTkEntry(tab_nome_cientifico, fg_color="white", border_color=CINZAFRENTE)
entry_nomePop3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow3 += 1

# Código
label_codigo3 = ctk.CTkLabel(tab_nome_cientifico, text="Código", text_color="black")
label_codigo3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow3 += 1
entry_codigo3 = ctk.CTkEntry(tab_nome_cientifico, fg_color="white", border_color=CINZAFRENTE, state="readonly")
entry_codigo3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow3 += 1

# Campo Link
label_link3 = ctk.CTkLabel(tab_nome_cientifico, text="Link", text_color="black")
label_link3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow3 += 1
entry_link3 = ctk.CTkEntry(tab_nome_cientifico, fg_color="white", border_color=CINZAFRENTE, state="readonly", text_color=CINZADESABILITADO)
entry_link3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow3 += 1


# Layout
label_layout3 = ctk.CTkLabel(tab_nome_cientifico, text="Layout da Plaquinha", text_color="black")
label_layout3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w")
contadorRow3 += 1
combo_layout3 = ctk.CTkComboBox(
    tab_nome_cientifico,
    values=list(layout_display_to_value.keys()),
    state="readonly",
    fg_color="white",
    border_color=CINZAFRENTE,
    button_hover_color=VERDEPLACADARK,
    button_color=VERDEPLACA
)
combo_layout3.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
contadorRow3 += 1

# Botão de gerar
botao_gerar_automatico = ctk.CTkButton(
    tab_nome_cientifico,
    text="Gerar Plaquinha",
    # command=gerar_placa_botao_automatico,
    fg_color=VERDEPLACA,
    hover_color=VERDEPLACADARK
)
botao_gerar_automatico.grid(row=contadorRow3, column=0, columnspan=2, padx=20, pady=20)
contadorRow3 += 1

# Campo Wikipedia
label_wikipedia3 = ctk.CTkLabel(tab_nome_cientifico, text="Pesquisa Wikipedia", text_color="black")
label_wikipedia3.grid(row=0, column=2, columnspan=2, padx=20, pady=(10, 0), sticky="w")
entry_wikipedia3 = ctk.CTkTextbox(tab_nome_cientifico, fg_color="white", border_color=CINZAFRENTE, border_width=1, height=100, wrap="word")
entry_wikipedia3.grid(row=1, column=2, columnspan=2, rowspan=10, padx=20, pady=(0, 10), sticky="nsew")
entry_wikipedia3.configure(state="disabled")

# Loop principal
app.mainloop()

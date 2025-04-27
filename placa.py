import fitz
import qrcode
from pathlib import Path

def gera_placa(nomePop, nomeCie, codigo, urlQR):

    # Diretorio base e fontes
    base_dir = Path(__file__).parent
    fonteNegritoPath = base_dir / "open-sans.bold.ttf"
    fonteItalicoPath = base_dir / "open-sans.italic.ttf"
    fonteNormalPath = base_dir / "open-sans.regular.ttf"

    # Inicializa documento
    doc = fitz.open("placa-fundo.pdf")
    pagina = doc[0]

    # Dimensoes
    paginaWidth = pagina.rect.width
    paginaHeight = pagina.rect.height

    # Insercao fontes
    pagina.insert_font(fontfile=fonteNegritoPath, fontname="F0")
    pagina.insert_font(fontfile=fonteItalicoPath, fontname="F1")
    pagina.insert_font(fontfile=fonteNormalPath, fontname="F2")


    # Coordenadas e tamanhos uteis
    tamfonte_titulo = 100
    tamfonte_menor = 30
    pontoSuperiorEsquerdoX = 62 # Coordenada x do ponto mais ao noroeste onde sera escrito texto
    pontoSuperiorEsquerdoY = 55 # Coordenada y do ponto mais ao noroeste onde sera escrito texto
    espacamentoEntreCaixas = 10 
    multiplicadorFonte = 1.3
    altura = 200

    retanguloCientifico_pontoSuperiorEsquerdoY = pontoSuperiorEsquerdoY + tamfonte_titulo*multiplicadorFonte + espacamentoEntreCaixas
    retanguloCodigo_pontoSuperiorEsquerdoY = retanguloCientifico_pontoSuperiorEsquerdoY + tamfonte_menor*multiplicadorFonte + espacamentoEntreCaixas



    # Criacao dos retangulos
    retanguloTitulo = fitz.Rect(
        pontoSuperiorEsquerdoX, 
        pontoSuperiorEsquerdoY, 
        paginaWidth - pontoSuperiorEsquerdoX, 
        altura + (pontoSuperiorEsquerdoX)
    )
    
    retanguloCientifico = fitz.Rect(
        pontoSuperiorEsquerdoX,
        retanguloCientifico_pontoSuperiorEsquerdoY,
        paginaWidth - pontoSuperiorEsquerdoX, 
        altura + retanguloCientifico_pontoSuperiorEsquerdoY
    )

    retanguloCodigo = fitz.Rect(
        pontoSuperiorEsquerdoX,
        retanguloCodigo_pontoSuperiorEsquerdoY,
        paginaWidth - pontoSuperiorEsquerdoX, 
        altura + retanguloCodigo_pontoSuperiorEsquerdoY 
    )

    # Insercoes dos textos
    pagina.insert_textbox(retanguloTitulo, nomePop, fontname="F0", fontsize=tamfonte_titulo, color=(1, 1, 1), align=0)
    pagina.insert_textbox(retanguloCientifico, nomeCie, fontname="F1", fontsize=tamfonte_menor, color=(1, 1, 1), align=0)
    pagina.insert_textbox(retanguloCodigo, codigo, fontname="F2", fontsize=tamfonte_menor, color=(1, 1, 1), align=0)

    doc.save(f"placa-{nomePop}.pdf")
    doc.close()
    print(f"Plaquinha do {nomePop} gerada.")

gera_placa("Alecrim", "Rosmarinus officinalis", "12345678", "https://github.com/enzosas/plaquinhasJardimBotanico")






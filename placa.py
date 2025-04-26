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
    print(paginaWidth)
    print(paginaHeight)

    # Insercao fontes
    pagina.insert_font(fontfile=fonteNegritoPath, fontname="F0")
    pagina.insert_font(fontfile=fonteItalicoPath, fontname="F1")
    pagina.insert_font(fontfile=fonteNormalPath, fontname="F2")


    # Coordenadas e tamanhos uteis
    TAMFONTE_TITULO = 100
    TAMFONTE_MENOR = 30
    pontoSuperiorEsquerdoX = 62.5
    pontoSuperiorEsquerdoY = 55
    espacamentoEntreCaixas = 0
    alturaCaixaTitulo = 170
    alturaCaixaNomeCientifico = 100
    alturaCaixaCodigo = 100
    fix = -50

    # Criacao dos retangulos
    retanguloTitulo = fitz.Rect(
        pontoSuperiorEsquerdoX, 
        pontoSuperiorEsquerdoY, 
        paginaWidth - pontoSuperiorEsquerdoX, 
        pontoSuperiorEsquerdoY + alturaCaixaTitulo
    )
    
    retanguloCientifico = fitz.Rect(
        pontoSuperiorEsquerdoX,
        pontoSuperiorEsquerdoY + alturaCaixaTitulo + espacamentoEntreCaixas + fix,
        paginaWidth - pontoSuperiorEsquerdoX, 
        pontoSuperiorEsquerdoY + alturaCaixaTitulo + espacamentoEntreCaixas + alturaCaixaNomeCientifico + fix
    )

    retanguloCodigo = fitz.Rect(
        pontoSuperiorEsquerdoX,
        pontoSuperiorEsquerdoY + alturaCaixaTitulo + espacamentoEntreCaixas + alturaCaixaNomeCientifico + espacamentoEntreCaixas + 2*fix,
        paginaWidth - pontoSuperiorEsquerdoX, 
        pontoSuperiorEsquerdoY + alturaCaixaTitulo + espacamentoEntreCaixas + alturaCaixaNomeCientifico + espacamentoEntreCaixas + alturaCaixaCodigo + 2*fix
    )

    # Insercoes dos textos
    pagina.insert_textbox(retanguloTitulo, nomePop, fontname="F0", fontsize=TAMFONTE_TITULO, color=(1, 1, 1), align=0)
    pagina.insert_textbox(retanguloCientifico, nomeCie, fontname="F1", fontsize=TAMFONTE_MENOR, color=(1, 1, 1), align=0)
    pagina.insert_textbox(retanguloCodigo, codigo, fontname="F2", fontsize=TAMFONTE_MENOR, color=(1, 1, 1), align=0)

    doc.save(f"placa-{nomePop}.pdf")
    doc.close()
    print(f"Plaquinha do {nomePop} gerada.")

gera_placa("Alecrim", "Rosmarinus officinalis", "12345678", "https://github.com/enzosas/plaquinhasJardimBotanico")






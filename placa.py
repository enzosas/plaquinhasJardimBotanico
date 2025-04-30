import fitz
import qrcode
from pathlib import Path

def carrega_fontes(base_dir, pagina):
    
    # Diretorio base e fontes
    fonteNegritoPath = base_dir / "open-sans.bold.ttf"
    fonteItalicoPath = base_dir / "open-sans.italic.ttf"
    fonteNormalPath = base_dir / "open-sans.regular.ttf"
    
    # Insercao fontes
    pagina.insert_font(fontfile=fonteNegritoPath, fontname="F0")
    pagina.insert_font(fontfile=fonteItalicoPath, fontname="F1")
    pagina.insert_font(fontfile=fonteNormalPath, fontname="F2")

def gera_placa(nomePop, nomeCie, codigo, urlQR):

    # Inicializa documento
    doc = fitz.open("placa-fundo.pdf")
    pagina = doc[0]
    base_dir = Path(__file__).parent

    carrega_fontes(base_dir, pagina)

    # Dimensoes
    paginaWidth = pagina.rect.width
    paginaHeight = pagina.rect.height

    # Coordenadas e tamanhos uteis
    tamfonte_titulo = 100
    tamfonte_menor = 30
    multiplicadorFonte = 1.3
    espacamentoEntreCaixas = 10 
    pSE_x = 62 # Coordenada x do ponto mais ao noroeste onde sera escrito texto
    pSE_y = 55 # Coordenada y do ponto mais ao noroeste onde sera escrito texto
    retanguloCientifico_pSE_y = pSE_y + tamfonte_titulo*multiplicadorFonte + espacamentoEntreCaixas
    retanguloCodigo_pSE_y = retanguloCientifico_pSE_y + tamfonte_menor*multiplicadorFonte + espacamentoEntreCaixas

    # Criacao das caixas de texto
    def gera_caixa_texto(var, fonte):
        return fitz.Rect(pSE_x, var, paginaWidth - pSE_x, var + 2*fonte)
    
    retanguloTitulo = gera_caixa_texto(pSE_y, tamfonte_titulo)
    retanguloCientifico = gera_caixa_texto(retanguloCientifico_pSE_y, tamfonte_menor)
    retanguloCodigo = gera_caixa_texto(retanguloCodigo_pSE_y, tamfonte_menor)

    # Insercoes dos textos
    pagina.insert_textbox(retanguloTitulo, nomePop, fontname="F0", fontsize=tamfonte_titulo, color=(1, 1, 1), align=0)
    pagina.insert_textbox(retanguloCientifico, nomeCie, fontname="F1", fontsize=tamfonte_menor, color=(1, 1, 1), align=0)
    pagina.insert_textbox(retanguloCodigo, codigo, fontname="F2", fontsize=tamfonte_menor, color=(1, 1, 1), align=0)

    doc.save(f"placa-{nomePop}.pdf")
    doc.close()
    print(f"Plaquinha do {nomePop} gerada.")

gera_placa("Alecrim", "Rosmarinus officinalis", "12345678", "https://github.com/enzosas/plaquinhasJardimBotanico")






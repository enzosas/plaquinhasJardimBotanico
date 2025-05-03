import fitz
import qrcode
from PIL import Image
from pathlib import Path

def gera_QR(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(255, 255, 255), back_color=(80, 108, 68)).convert("RGBA")
    qr_img = qr_img.resize((1600, 1600), Image.Resampling.LANCZOS)
    return qr_img


def gera_placa(nomePop, nomeCie, codigo, urlQR):

    # Inicializa documento
    doc = fitz.open("placa-fundo.pdf")
    pagina = doc[0]
    base_dir = Path(__file__).parent

    # Diretorio base e fontes
    fonteNegritoPath = base_dir / "open-sans.bold.ttf"
    fonteItalicoPath = base_dir / "open-sans.italic.ttf"
    fonteNormalPath = base_dir / "open-sans.regular.ttf"

    # Insercao fontes
    pagina.insert_font(fontfile=fonteNegritoPath, fontname="F0")
    pagina.insert_font(fontfile=fonteItalicoPath, fontname="F1")
    pagina.insert_font(fontfile=fonteNormalPath, fontname="F2")

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

    # Funcao para criacao das caixas de texto
    def gera_caixa_texto(var, fonte):
        return fitz.Rect(pSE_x, var, paginaWidth - pSE_x, var + 2*fonte)

    # Funcao para diminuicao da fonte para que texto grande caiba na caixa
    def insere_texto_ajustado(pagina, retangulo, texto, fontnamevar, fontdir, fontsize_inicial):
        tamfonte = fontsize_inicial
        fonte = fitz.Font(fontfile=str(fontdir))
        while tamfonte >= 1:
            text_width = fonte.text_length(texto, fontsize=tamfonte)
            if text_width <= retangulo.width:
                pagina.insert_textbox(retangulo, texto, fontname=fontnamevar, fontsize=tamfonte, color=(1, 1, 1), align=0)
                return tamfonte
            tamfonte -= 1
        return tamfonte
    
    # Escreve os rotulos na placa de modo que o texto caiba na caixa e retorna o tamanho da fonte que ficou para alterar a posicao da caixa abaixo
    retanguloTitulo = gera_caixa_texto(pSE_y, tamfonte_titulo)
    fonteCustom1 = insere_texto_ajustado(pagina, retanguloTitulo, nomePop, "F0", fonteNegritoPath, tamfonte_titulo)
    
    retanguloCientifico_pSE_y = pSE_y + fonteCustom1*multiplicadorFonte + espacamentoEntreCaixas
    retanguloCientifico = gera_caixa_texto(retanguloCientifico_pSE_y, tamfonte_menor)
    fonteCustom2 = insere_texto_ajustado(pagina, retanguloCientifico, nomeCie, "F1", fonteItalicoPath, tamfonte_menor)

    retanguloCodigo_pSE_y = retanguloCientifico_pSE_y + fonteCustom2*multiplicadorFonte + espacamentoEntreCaixas
    retanguloCodigo = gera_caixa_texto(retanguloCodigo_pSE_y, tamfonte_menor)
    fonteCustom3 = insere_texto_ajustado(pagina, retanguloCodigo, codigo, "F2", fonteNormalPath, tamfonte_menor)

    # Gera QR code
    qr_img = gera_QR(urlQR)

    # Salva na memoria com streamline
    import io
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # QR Coordenadas
    qr_tam = 350
    qr_PID_x = paginaWidth - 70
    qr_PID_y = paginaHeight - 70

    # Insere QRCode na placa
    qr_rect = fitz.Rect(qr_PID_x - qr_tam, qr_PID_y - qr_tam, qr_PID_x, qr_PID_y)
    pagina.insert_image(qr_rect, stream=img_bytes)

    # Salva e baixa
    doc.save(f"placa-{nomePop}.pdf")
    doc.close()
    print(f"Plaquinha do {nomePop} gerada.")
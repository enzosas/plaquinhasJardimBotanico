import fitz
import qrcode
from pathlib import Path

def gera_QR(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=0,
    )
    qr.add_data(link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(255, 255, 255), back_color=(80, 108, 68)).convert("RGBA")
    return qr_img


def gera_placa(nomePop, nomeCie, codigo, urlQR, layout, diretorio_saida=None):

    # Diretorio base e fontes
    base_dir = Path(__file__).parent
    fonteNegritoPath = base_dir / "open-sans.bold.ttf"
    fonteItalicoPath = base_dir / "open-sans.italic.ttf"
    fonteNormalPath = base_dir / "open-sans.regular.ttf"

    # Funcao para criacao das caixas de texto
    def gera_caixa_texto(pSE_x, pontoY, fonte, paginaWidth):
        return fitz.Rect(pSE_x, pontoY, paginaWidth - pSE_x, pontoY + 2*fonte)

    # Funcao para diminuicao da fonte para que texto grande caiba na caixa
    def insere_texto_ajustado(pagina, retangulo, texto, fontnamevar, fontdir, fontsize_inicial, inserir=True):
        tamfonte = fontsize_inicial
        fonte = fitz.Font(fontfile=str(fontdir))
        while tamfonte >= 1:
            text_width = fonte.text_length(texto, fontsize=tamfonte)
            if text_width <= retangulo.width:
                if inserir:
                    pagina.insert_textbox(retangulo, texto, fontname=fontnamevar, fontsize=tamfonte, color=(1, 1, 1), align=0)
                return tamfonte
            tamfonte -= 1
        return tamfonte

    # Gera QR code
    qr_img = gera_QR(urlQR)

    # Salva na memoria com streamline
    import io
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Inicializa documento
    if layout == "layout0":
        doc = fitz.open("placa-fundo.pdf")
    elif layout == "layout1":
        doc = fitz.open("placa-fundo-1.pdf")
    elif layout == "layout2":
        doc = fitz.open("placa-fundo-2.pdf")
    else:
        print("erro layout")
        return

    pagina = doc[0]

    # Insercao fontes
    pagina.insert_font(fontfile=fonteNegritoPath, fontname="F0")
    pagina.insert_font(fontfile=fonteItalicoPath, fontname="F1")
    pagina.insert_font(fontfile=fonteNormalPath, fontname="F2")

    # Dimensoes
    paginaWidth = pagina.rect.width
    paginaHeight = pagina.rect.height

    # Tamanhos uteis
    tamfonte_titulo = 100
    tamfonte_menor = 30
    multiplicadorFonte = 1.3
    espacamentoEntreCaixas = 10 
    
    if layout == "layout0":
        
        pSE_x = 62 # Coordenada x do ponto mais ao noroeste onde sera escrito texto
        pSE_y = 55 # Coordenada y do ponto mais ao noroeste onde sera escrito texto
        
        # Escreve os rotulos na placa de modo que o texto caiba na caixa e retorna o tamanho da fonte que ficou para alterar a posicao da caixa abaixo
        retanguloTitulo = gera_caixa_texto(pSE_x, pSE_y, tamfonte_titulo, paginaWidth)
        fonteCustom1 = insere_texto_ajustado(pagina, retanguloTitulo, nomePop, "F0", fonteNegritoPath, tamfonte_titulo)
        
        retanguloCientifico_pSE_y = pSE_y + fonteCustom1*multiplicadorFonte + espacamentoEntreCaixas
        retanguloCientifico = gera_caixa_texto(pSE_x, retanguloCientifico_pSE_y, tamfonte_menor, paginaWidth)
        fonteCustom2 = insere_texto_ajustado(pagina, retanguloCientifico, nomeCie, "F1", fonteItalicoPath, tamfonte_menor)

        retanguloCodigo_pSE_y = retanguloCientifico_pSE_y + fonteCustom2*multiplicadorFonte + espacamentoEntreCaixas
        retanguloCodigo = gera_caixa_texto(pSE_x, retanguloCodigo_pSE_y, tamfonte_menor, paginaWidth)
        fonteCustom3 = insere_texto_ajustado(pagina, retanguloCodigo, codigo, "F2", fonteNormalPath, tamfonte_menor)
    
        # QR Coordenadas
        qr_tam = 350
        qr_PID_x = paginaWidth - 70
        qr_PID_y = paginaHeight - 70

        # Insere QRCode na placa
        qr_rect = fitz.Rect(qr_PID_x - qr_tam, qr_PID_y - qr_tam, qr_PID_x, qr_PID_y)
        pagina.insert_image(qr_rect, stream=img_bytes)

    if layout == "layout1":
        
        # QR Coordenadas
        qr_tam = 295
        qr_PSE_x = 40
        qr_PSE_y = 40
        
        # Insere QRCode na placa
        qr_rect = fitz.Rect(qr_PSE_x, qr_PSE_y, qr_PSE_x + qr_tam, qr_PSE_y + qr_tam)
        pagina.insert_image(qr_rect, stream=img_bytes)

        pSE_x = 1.7*qr_PSE_x + qr_tam # Coordenada x do ponto mais ao noroeste onde sera escrito texto
        pSE_y = 30 # Coordenada y do ponto mais ao noroeste onde sera escrito texto

        # Escreve os rotulos na placa de modo que o texto caiba na caixa e retorna o tamanho da fonte que ficou para alterar a posicao da caixa abaixo
        retanguloTitulo = fitz.Rect(pSE_x, pSE_y, paginaWidth - qr_PSE_x, pSE_y + 2*tamfonte_titulo)
        fonteCustom1 = insere_texto_ajustado(pagina, retanguloTitulo, nomePop, "F0", fonteNegritoPath, tamfonte_titulo)
        
        retanguloCientifico_pSE_y = pSE_y + fonteCustom1*multiplicadorFonte + espacamentoEntreCaixas
        retanguloCientifico = fitz.Rect(pSE_x, retanguloCientifico_pSE_y, paginaWidth - qr_PSE_x, retanguloCientifico_pSE_y + 2*tamfonte_titulo)
        fonteCustom2 = insere_texto_ajustado(pagina, retanguloCientifico, nomeCie, "F1", fonteItalicoPath, tamfonte_menor)

        retanguloCodigo_pSE_y = retanguloCientifico_pSE_y + fonteCustom2*multiplicadorFonte + espacamentoEntreCaixas
        retanguloCodigo = fitz.Rect(pSE_x, retanguloCodigo_pSE_y, paginaWidth - qr_PSE_x, retanguloCodigo_pSE_y + 2*tamfonte_titulo)
        fonteCustom3 = insere_texto_ajustado(pagina, retanguloCodigo, codigo, "F2", fonteNormalPath, tamfonte_menor)

    if layout == "layout2":
        
        pSE_x = 70 # Coordenada x do ponto mais ao noroeste onde sera escrito texto
        pSE_y = 40 # Coordenada y do ponto mais ao noroeste onde sera escrito texto
        tamanhoLimiteCaixaTexto = 110
        
        # Escreve os rotulos na placa de modo que o texto caiba na caixa e retorna o tamanho da fonte que ficou para alterar a posicao da caixa abaixo
        retanguloTeste = gera_caixa_texto(pSE_x, pSE_y, tamfonte_titulo, paginaWidth - tamanhoLimiteCaixaTexto)
        fonteNaoSeiExplicar = insere_texto_ajustado(pagina, retanguloTeste, nomePop, "F0", fonteNegritoPath, tamfonte_titulo, inserir=False)
        
        retanguloTitulo_pSE_y = pSE_y + tamfonte_titulo - fonteNaoSeiExplicar
        retanguloTitulo = gera_caixa_texto(pSE_x, retanguloTitulo_pSE_y, tamfonte_titulo, paginaWidth - tamanhoLimiteCaixaTexto)
        fonteCustom1 = insere_texto_ajustado(pagina, retanguloTitulo, nomePop, "F0", fonteNegritoPath, tamfonte_titulo)
        
        retanguloCientifico_pSE_y = retanguloTitulo_pSE_y + fonteCustom1*multiplicadorFonte + espacamentoEntreCaixas
        retanguloCientifico = gera_caixa_texto(pSE_x, retanguloCientifico_pSE_y, tamfonte_menor, paginaWidth - tamanhoLimiteCaixaTexto)
        fonteCustom2 = insere_texto_ajustado(pagina, retanguloCientifico, nomeCie, "F1", fonteItalicoPath, tamfonte_menor)

        retanguloCodigo_pSE_y = retanguloCientifico_pSE_y + fonteCustom2*multiplicadorFonte + espacamentoEntreCaixas
        retanguloCodigo = gera_caixa_texto(pSE_x, retanguloCodigo_pSE_y, tamfonte_menor, paginaWidth - tamanhoLimiteCaixaTexto)
        fonteCustom3 = insere_texto_ajustado(pagina, retanguloCodigo, codigo, "F2", fonteNormalPath, tamfonte_menor)
    
        # QR Coordenadas
        margem = 100
        qr_tam = paginaWidth - 2*margem
        qr_PID_x = paginaWidth - margem
        qr_PID_y = paginaHeight - 0.8*margem

        # Insere QRCode na placa
        qr_rect = fitz.Rect(qr_PID_x - qr_tam, qr_PID_y - qr_tam, qr_PID_x, qr_PID_y)
        pagina.insert_image(qr_rect, stream=img_bytes)

    print(f"before  {diretorio_saida}")
    nome_arquivo = f"placa-{nomePop}.pdf"

    # Define o diretorio de saida, testa se foi inserido diretorio e se foi inserido nome do arquivo no diretorio
    if diretorio_saida:
        diretorio_saida = Path(diretorio_saida)
        if diretorio_saida.suffix.lower() == ".pdf":
            caminho_final = diretorio_saida
        elif diretorio_saida.is_dir() or diretorio_saida.suffix == "":
            diretorio_saida.mkdir(parents=True, exist_ok=True)
            caminho_final = diretorio_saida / nome_arquivo
        else:
            caminho_final = diretorio_saida.with_suffix(".pdf")
    else:
        caminho_final = base_dir / nome_arquivo
        
    doc.save(str(caminho_final))
    doc.close()
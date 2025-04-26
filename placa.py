import fitz
import qrcode
from pathlib import Path

# Diretorio base e fontes
base_dir = Path(__file__).parent
fonteNegritoPath = base_dir / "open-sans.bold.ttf"
fonteItalicoPath = base_dir / "open-sans.light-italic.ttf"

# Variaveis da placa
nomePop = "Alecrim"
nomeCie = "Rosmarinus officinalis"
codigo = "12345678"
urlQR = "https://github.com/enzosas/plaquinhasJardimBotanico"

# Inicializa documento
doc = fitz.open("placa-fundo.pdf")
pagina = doc[0]

# Dimensoes
pagina_width = pagina.rect.width
pagina_height = pagina.rect.height
print(pagina_width)
print(pagina_height)

# Insercao fontes
pagina.insert_font(fontfile=fonteNegritoPath, fontname="F0")
pagina.insert_font(fontfile=fonteItalicoPath, fontname="F1")


pagina.insert_text((50, 50), nomePop, fontname="F0", fontsize=32, color=(1, 1, 1))
pagina.insert_text((50, 70), nomeCie, fontsize=12, color=(1, 1, 1))
pagina.insert_text((50, 90), codigo, fontsize=10, color=(1, 1, 1))

doc.save(f"placa-{nomePop}.pdf")
doc.close()
print(f"Plaquinha do {nomePop} gerada.")






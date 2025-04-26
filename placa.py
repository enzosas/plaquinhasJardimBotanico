import fitz
import qrcode
from pathlib import Path


base_dir = Path(__file__).parent
fontePath = base_dir / "OpenSans-VariableFont_wdth,wght.ttf"
fonteItalicoPath = base_dir / "OpenSans-Italic-VariableFont_wdth,wght.ttf"

nomePop = "Alecrim"
nomeCie = "Rosmarinus officinalis"
codigo = "12345678"
urlQR = "https://github.com/enzosas/plaquinhasJardimBotanico"

doc = fitz.open("placa-fundo.pdf")
pagina = doc[0]

pagina.insert_text((50, 50), nomePop, fontsize=16, color=(1, 1, 1))
pagina.insert_text((50, 70), nomeCie, fontsize=12, color=(1, 1, 1))
pagina.insert_text((50, 90), codigo, fontsize=10, color=(1, 1, 1))

doc.save(f"placa-{nomePop}.pdf")
doc.close()
print(f"Plaquinha do {nomePop} gerada.")






"""Aplica a Identidade Visual v4 da Oka ao site sem mexer no layout.

Troca a paleta antiga (azul, ciano, verde, vermelho, oceano) pela nova
(laranja dominante, amarelo e creme nos detalhes, grafite no fundo), troca o
símbolo antigo (anel + triângulo) pela oca e aplica o filtro de cor nos vídeos.

Uso: python3 tools/marca_v4.py   (roda na raiz do repositório; idempotente)
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# Paleta oficial e derivados
LARANJA, LARANJA_FUNDO = "#E08C43", "#C8702C"
AMARELO, CREME, GRAFITE = "#FDCE00", "#FDEADA", "#484747"
FUNDO = "#1B1A1A"

HEX = {
    "#0077E6": LARANJA_FUNDO,   # azul oka -> laranja profundo
    "#00B2CF": LARANJA,         # ciano -> laranja
    "#00D4A3": AMARELO,         # verde -> amarelo (detalhes)
    "#00E6B0": "#FFD84D",
    "#5ED29C": AMARELO,
    "#C23432": CREME,           # vermelho -> creme
    "#F8F8FF": CREME,           # texto
    "#E8F0F5": "#F7E6D6",
    "#AEBCC6": "#BDB2A8",
    "#010D20": FUNDO,           # fundo
    "#04121F": "#141313",
    "#0A1626": "#2A2929",       # faixas em destaque: grafite
}
RGB = {
    "0,119,230": "200,112,44",
    "0,178,207": "224,140,67",
    "0,212,163": "253,206,0",
    "194,52,50": "253,234,218",
    "1,13,32": "27,26,26",
}

# Símbolo da oca (viewBox do kit web)
SIMB_VB = "116.5 98.25 183.78 166.64"
SIMB_POLIS = [
    "265.82 164.17 145.82 164.43 135.72 145.83 279.52 145.52 265.82 164.17",
    "117.25 227.4 245.84 98.25 264.2 116.54 116.5 264.89 117.25 227.4",
    "300.28 263.47 154.62 118.43 170.86 102.13 298.3 229.01 300.28 263.47",
]
PONTO = '<ellipse{cls} cx="207.92" cy="219.64" rx="22.43" ry="22.63" fill="' + AMARELO + '"/>'
WORD_VB = "98.08 166.72 220.56 92.15"
WORD_PATH = (RAIZ / "brand" / "oka-wordmark-creme.svg").read_text()
WORD_D = re.search(r' d="([^"]+)"', WORD_PATH).group(1)


def simbolo(altura, desenho=None):
    """Símbolo laranja com o ponto amarelo. `desenho` = prefixo das classes
    de animação (draw/door ou bl-draw/bl-door): os polígonos nascem só com o
    contorno e são preenchidos pelo GSAP."""
    if desenho:
        polis = "".join(
            f'<polygon class="{desenho}-draw" points="{p}" fill="{LARANJA}" fill-opacity="0" stroke="{LARANJA}" stroke-width="3" stroke-linejoin="round"/>'
            for p in SIMB_POLIS)
        ponto = PONTO.format(cls=f' class="{desenho}-door"')
    else:
        polis = "".join(f'<polygon points="{p}" fill="{LARANJA}"/>' for p in SIMB_POLIS)
        ponto = PONTO.format(cls="")
    largura = round(altura * 183.78 / 166.64)
    return f'<svg width="{largura}" height="{altura}" viewBox="{SIMB_VB}" aria-hidden="true">{polis}{ponto}</svg>'


def wordmark(altura, extra=""):
    largura = round(altura * 220.56 / 92.15)
    return f'<svg{extra} width="{largura}" height="{altura}" viewBox="{WORD_VB}" role="img" aria-label="OKA"><path fill="{CREME}" d="{WORD_D}"/></svg>'


ANTIGO_SVG = r'<svg[^>]*viewBox="0 0 100 100"[^>]*>\s*<circle[^>]*okaRing.*?</svg>'

VIDEO_CSS = """
    /* ── Filtro de cor dos vídeos (marca v4): laranja dominante, luz amarela ── */
    .oka-tint { position:absolute; inset:0; pointer-events:none; }
    .oka-tint-cor { background:#E08C43; mix-blend-mode:color; }
    .oka-tint-luz { background:radial-gradient(60% 70% at 70% 35%, rgba(253,206,0,0.55), transparent 70%); mix-blend-mode:soft-light; }
    #bg-video,.bg-video-section { filter:grayscale(1) contrast(1.12); }
"""


def tingir(html):
    for a, b in HEX.items():
        html = re.sub(re.escape(a) + r"(?![0-9a-fA-F])", b, html, flags=re.I)
    for a, b in RGB.items():
        html = re.sub(r"rgba\(\s*" + a.replace(",", r",\s*") + r"\s*,", f"rgba({b},", html)
    return html


def processar(html):
    if "oka-tint" in html and "okaRing" not in html:
        return html  # já aplicado

    html = tingir(html)

    # Gradiente compartilhado do anel antigo
    html = re.sub(r'\n<!-- Shared logo gradient -->\n<svg width="0".*?</svg>\n', "\n", html, flags=re.S)

    # Preloader: símbolo desenhado + wordmark
    html = re.sub(
        r'(<div id="preloader">\s*)' + ANTIGO_SVG + r'\s*<span class="pl-word[^"]*">OKA</span>',
        lambda m: m.group(1) + simbolo(90, "draw").replace('class="draw-draw"', 'class="draw"').replace('class="draw-door"', 'class="door"')
        + "\n  " + wordmark(22, ' class="pl-word"'),
        html, flags=re.S)

    # Logo grande ("Por que OKA")
    html = re.sub(
        r'<svg id="big-logo"[^>]*>.*?</svg>(\s*<div>\s*)<p class="font-heading[^"]*">OKA</p>(\s*<p[^>]*>)Casa das Soluções Inteligentes',
        lambda m: simbolo(92, "bl").replace("<svg ", '<svg id="big-logo" ', 1).replace(' aria-hidden="true"', ' aria-label="Logo OKA"', 1)
        + m.group(1) + wordmark(34) + m.group(2) + "Tecnologia com raiz no futuro",
        html, flags=re.S)

    # Navbar e rodapé: símbolo + wordmark
    def logo_curto(m):
        alt = int(re.search(r'height="(\d+)"', m.group(0)).group(1))
        return simbolo(alt - 4) + "\n      " + wordmark(round(alt * 0.5))
    html = re.sub(ANTIGO_SVG + r'\s*<span class="font-heading[^"]*">OKA</span>', logo_curto, html, flags=re.S)

    # Assinatura do rodapé
    html = html.replace("© 2026 OKA — Casa das Soluções Inteligentes.", "© 2026 OKA · Tecnologia com raiz no futuro.")

    # Ícones
    html = html.replace('href="/brand/oka-mark.svg"', 'href="/brand/favicon.svg"')
    html = html.replace("oka-logo-full-light.png", "favicon-512.png").replace('"width": 1410,\n          "height": 390', '"width": 512,\n          "height": 512')

    # Vídeos: camadas de cor logo depois de cada <video>
    camadas = '<div class="oka-tint oka-tint-cor"></div><div class="oka-tint oka-tint-luz"></div>'
    html = re.sub(r'(<video id="bg-video"[^>]*></video>)', r'\1\n  ' + camadas.replace('class="oka-tint ', 'class="oka-tint z-0 '), html)
    html = re.sub(r'(<video class="bg-video-section[^>]*></video>)', r'\1\n  ' + camadas, html)
    if "<video" in html:
        html = html.replace("  </style>", VIDEO_CSS + "  </style>", 1)
    return html


def main():
    for f in [RAIZ / "index.html", *sorted((RAIZ / "blog").glob("**/index.html"))]:
        antes = f.read_text()
        depois = processar(antes)
        if depois != antes:
            f.write_text(depois)
            print("ok", f.relative_to(RAIZ))
    mf = RAIZ / "site.webmanifest"
    mf.write_text(tingir(mf.read_text()).replace("/brand/oka-mark.svg", "/brand/favicon.svg")
                  .replace("OKA — Casa das Soluções Inteligentes", "OKA · Tecnologia com raiz no futuro"))


if __name__ == "__main__":
    main()

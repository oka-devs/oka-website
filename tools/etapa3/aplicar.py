"""Etapa 3: títulos sem degradê e à esquerda, botões retos, Sobre junto do contato."""
import pathlib, re
RAIZ = pathlib.Path(__file__).resolve().parents[2]

BTN_CSS = """    .btn-cta { background:#FDEADA; color:#1B1A1A; border-radius:6px; transition:background .2s,color .2s; }
    .btn-cta:hover { background:#FFFFFF; }
    .btn-outline { border:1px solid rgba(253,234,218,0.28); border-radius:6px; transition:border-color .2s,background .2s; }
    .btn-outline:hover { border-color:rgba(253,234,218,0.6); background:rgba(253,234,218,0.06); }"""

def botoes(html):
    # CSS dos botões
    html = re.sub(r'    \.btn-cta \{[^\n]*\n    \.btn-cta:hover \{[^\n]*(\n    \.btn-outline \{[^\n]*\n    \.btn-outline:hover \{[^\n]*)?', BTN_CSS, html, count=1)
    # classes dos botões e links-botão
    def ajusta(m):
        c = m.group(1)
        if not re.search(r'btn-cta|btn-outline|btn-whatsapp|border border-white/15|bg-white text-black', c):
            return m.group(0)
        c = re.sub(r'\brounded-(full|xl)\b', 'rounded-md', c)
        c = c.replace('font-jakarta font-bold uppercase', 'font-inter font-semibold').replace(' tracking-wide', '')
        c = c.replace('bg-white text-black', 'bg-[#FDEADA] text-[#1B1A1A]').replace('hover:bg-white/90', 'hover:bg-white')
        c = c.replace('border border-white/15', 'border border-[#FDEADA]/25')
        return f'class="{c}"'
    return re.sub(r'class="([^"]*)"', ajusta, html)

def sem_degrade(html):
    html = html.replace('<span class="text-gradient">.</span>', '<span style="color:#E08C43">.</span>')
    return re.sub(r'<span class="text-gradient">([^<]*)</span>', r'\1', html)

# ── home ──
p = RAIZ / 'index.html'
s = p.read_text()
assert 'SOBRE + CONTATO' not in s
s = botoes(sem_degrade(s))

# etiqueta acima de "Conheça a Oka"
s, n = re.subn(r'\n\s*<!-- Eyebrow -->\n\s*<p id="h-eyebrow"[^\n]*</p>', '', s); assert n == 1, n
s = s.replace("      .fromTo('#h-eyebrow', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5 }, '-=0.35')\n", '')
s = s.replace("['#h-eyebrow', '#h-title', '#h-sub', '#h-cta']", "['#h-title', '#h-sub', '#h-cta']")
assert 'h-eyebrow' not in s

# cabeçalhos de seção alinhados à esquerda
s = s.replace('<div class="text-center mb-', '<div class="mb-')
for a in ['max-w-md mx-auto', 'max-w-xl mx-auto', 'max-w-2xl mx-auto']:
    s = s.replace(f'leading-relaxed">', 'leading-relaxed">') if False else s.replace(a, a.replace(' mx-auto', ''))
s = s.replace('<div class="reveal flex justify-center mb-12">', '<div class="reveal flex mb-12">')
s = s.replace('<div class="reveal text-center mt-14">', '<div class="reveal mt-14">')
s = s.replace('<p class="reveal text-center font-body text-polar/50 text-sm', '<p class="reveal font-body text-polar/50 text-sm')
s = s.replace('    <div class="reveal text-center">\n      <a href="#contato" class="btn-cta', '    <div class="reveal">\n      <a href="#contato" class="btn-cta')

# abas sem pílula em degradê
s = s.replace(""".abas { display:inline-flex; flex-wrap:wrap; justify-content:center; gap:6px; padding:5px; border-radius:999px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); }""",
              """.abas { display:inline-flex; flex-wrap:wrap; gap:28px; border-bottom:1px solid rgba(253,234,218,0.12); }""")
s = s.replace(""".aba { padding:9px 18px; border-radius:999px; font:500 14px 'Inter',sans-serif; color:rgba(253,234,218,0.62); cursor:pointer; transition:background .25s,color .25s; }""",
              """.aba { padding:10px 0; margin-bottom:-1px; border-bottom:2px solid transparent; font:500 15px 'Inter',sans-serif; color:rgba(253,234,218,0.55); cursor:pointer; transition:color .25s,border-color .25s; }""")
s = s.replace(""".aba[aria-selected="true"] { background:linear-gradient(135deg,#C8702C,#E08C43); color:#141313; }""",
              """.aba[aria-selected="true"] { color:#FDEADA; border-bottom-color:#E08C43; }""")

# Sobre + contato numa seção só, no fim
i = s.index('<!-- ════════ POR QUE OKA'); j = s.index('<!-- ════════ COMO FUNCIONA')
sobre = s[i:j]; s = s[:i] + s[j:]
fundo = sobre[sobre.index('  <!-- Cinematic background video -->'):sobre.index('\n\n  <div class="relative z-10')]
esq = sobre[sobre.index('    <!-- Left column -->'):sobre.index('    <!-- Right column: liquid-glass card -->')].rstrip()
i = s.index('<!-- ════════ CONTATO'); j = s.index('<!-- ════════ FOOTER')
contato = s[i:j]
form = contato[contato.index('    <!-- Formulário → WhatsApp -->'):contato.index('    <!-- Canal alternativo -->')].rstrip()
form = form.replace('class="reveal glass rounded-3xl p-7 md:p-9 text-left"', 'class="reveal glass rounded-2xl p-7 md:p-8 text-left"')
canal = contato[contato.index('    <!-- Canal alternativo -->'):contato.index('  </div>\n</section>')].rstrip()
canal = canal.replace('<div class="reveal text-center mt-8">', '<div class="reveal mt-10">')
novo = f'''<!-- ════════ SOBRE + CONTATO ════════ -->
<section id="porque-oka" class="relative py-28 px-6 overflow-hidden">
{fundo}

  <div class="relative z-10 max-w-6xl mx-auto grid md:grid-cols-2 gap-14 md:gap-20 items-start">
{esq}
{canal}
    </div>

    <div id="contato" class="scroll-mt-28">
      <h2 class="reveal-head font-heading font-bold text-polar leading-[1.02] mb-6" style="font-size:clamp(1.9rem,4.5vw,3rem);">Fale com a gente</h2>
      <p class="reveal font-body text-polar/60 text-base leading-relaxed mb-8">Escreva seu nome e o assunto. O WhatsApp abre com a mensagem pronta.</p>
{form}
    </div>
  </div>
</section>


'''
# a coluna esquerda termina com </div> de fechamento: abre-se espaço para o canal antes dele
novo = novo.replace(esq + '\n' + canal + '\n    </div>', esq[:esq.rstrip().rfind('</div>')].rstrip() + '\n' + canal + '\n    </div>')
s = s[:i] + novo + s[j:]
assert s.count('id="contato"') == 1 and s.count('id="porque-oka"') == 1

# menu: Sobre vai para o fim
link = '      <a href="#porque-oka" class="nav-link text-white/70 text-sm font-medium hover:text-white transition-colors duration-200">Sobre</a>\n'
assert link in s; s = s.replace(link, '', 1)
s = s.replace('      <a href="/blog/"      class="nav-link', link.replace('\n', '') + '\n      <a href="/blog/"      class="nav-link', 1) if False else s
blog_nav = '      <a href="/blog/"      class="nav-link text-white/70 text-sm font-medium hover:text-white transition-colors duration-200">Blog</a>\n'
assert blog_nav in s; s = s.replace(blog_nav, blog_nav + link, 1)
mlink = '  <a href="#porque-oka" class="font-inter text-2xl text-polar/80 hover:text-emerald transition-colors" data-close-menu>SOBRE</a>\n'
mblog = '  <a href="/blog/"      class="font-inter text-2xl text-polar/80 hover:text-emerald transition-colors" data-close-menu>BLOG</a>\n'
if mlink in s and mblog in s:
    s = s.replace(mlink, '', 1).replace(mblog, mblog + mlink, 1)
p.write_text(s)

# ── blog ──
for f in [RAIZ / 'blog' / 'index.html', *sorted((RAIZ / 'blog').glob('*/index.html'))]:
    t = f.read_text()
    t2 = botoes(sem_degrade(t))
    if t2 != t: f.write_text(t2)
print('ok')

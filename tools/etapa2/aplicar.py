"""Etapa 2 do site: troca ícones por demonstrações em movimento e reorganiza seções."""
import pathlib, re
RAIZ = pathlib.Path(__file__).resolve().parents[2]
p = RAIZ / 'index.html'
s = p.read_text()
assert 'mini-stage' not in s, 'etapa 2 já aplicada'

def entre(a, b, texto=None):
    t = s if texto is None else texto
    i = t.index(a); j = t.index(b, i)
    return i, j

# 1) CSS
s = s.replace('  </style>', (pathlib.Path(__file__).parent / 'estilo.css').read_text() + '  </style>', 1)

# 2) Serviços: ícones viram mini demonstrações
STAGES = [
 '''<div class="mini-stage loop" aria-hidden="true"><div class="ms-box l"><span></span><span></span><span></span></div><div class="ms-track"></div><span class="ms-doc"></span><span class="ms-doc d2"></span><span class="ms-doc d3"></span><div class="ms-box r"><span></span><span></span><span></span></div></div>''',
 '''<div class="mini-stage loop ms-chat" aria-hidden="true"><span class="b u">Tem horário amanhã?</span><span class="b a">Tenho 9h ou 10h30.</span><span class="b ok">✓ Marcado às 9h</span></div>''',
 '''<div class="mini-stage loop" aria-hidden="true"><div class="ms-bars"><span style="--h:45%"></span><span style="--h:70%"></span><span style="--h:55%"></span><span style="--h:85%"></span><span style="--h:100%"></span><span style="--h:65%"></span><span style="--h:40%"></span></div></div>''',
 '''<div class="mini-stage loop" aria-hidden="true"><div class="ms-phone"><div class="ms-screen"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div></div>''',
]
i, j = entre('<section id="servicos"', '</section>')
bloco = s[i:j]
it = iter(STAGES)
bloco, n = re.subn(r'<div class="icon-box mb-6[^"]*"[^>]*>\s*<svg.*?</svg>\s*</div>', lambda m: next(it), bloco, flags=re.S)
assert n == 4, n
bloco = re.sub(r'\n\s*<div class="absolute -top-12 left-1/2[^>]*></div>', '', bloco)
s = s[:i] + bloco + s[j:]

# 3) Portfólio: prévia em movimento no topo de cada card, sem etiquetas
PREV = {
 'LocaFácil': '''<div class="mini-stage alto loop pf-loca" aria-hidden="true"><div class="pf-row"><i></i>Apartamento 302<span class="pf-pill"><b>Pendente</b><em>Pago</em></span></div><div class="pf-row"><i></i>Caminhonete<span class="pf-pill"><b>Pendente</b><em>Pago</em></span></div><div class="pf-row"><i></i>Betoneira<span class="pf-pill"><b>Pendente</b><em>Pago</em></span></div></div>''',
 'Vereda': '''<div class="mini-stage alto loop pf-ver" aria-hidden="true"><div class="pf-pub"><p>Nova publicação</p><span></span><span></span><span></span></div><svg class="pf-seta" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="12" x2="19" y2="12"/><polyline points="13 6 19 12 13 18"/></svg><div class="pf-cal">''' + ''.join('<span class="alvo"></span>' if k == 10 else '<span></span>' for k in range(14)) + '''<em>Prazo na agenda</em></div></div>''',
 'Meety': '''<div class="mini-stage alto loop pf-meety" aria-hidden="true"><div class="pf-wave">''' + '<span></span>' * 28 + '''</div><div class="pf-linha"><i style="background:#E08C43"></i><span style="--w:78%"></span></div><div class="pf-linha"><i style="background:#FDCE00"></i><span style="--w:56%"></span></div><div class="pf-linha"><i style="background:#FDEADA"></i><span style="--w:68%"></span></div></div>''',
}
i, j = entre('<section id="portfolio"', '</section>')
bloco = s[i:j]
arts = bloco.split('      <article class="reveal glass rounded-2xl p-7 flex flex-col">')
for k in range(1, len(arts)):
    nome = next(n for n in PREV if f'>{n}' in arts[k] or f'{n} ' in arts[k])
    arts[k] = '\n        ' + PREV[nome] + arts[k]
    arts[k] = re.sub(r'\n\s*<div class="flex flex-wrap gap-2 mb-6">.*?</div>', '', arts[k], count=1)
    arts[k] = arts[k].replace('leading-relaxed mb-5">', 'leading-relaxed mb-6">', 1)
bloco = '      <article class="reveal glass rounded-2xl p-7 flex flex-col">'.join(arts)
s = s[:i] + bloco + s[j:]

# 4) "O que é IA" + "Na prática" viram uma seção com abas
i, j = entre('<!-- ════════ O QUE É UM AGENTE DE IA ════════ -->', '<!-- ════════ TREINAMENTOS ════════ -->')
velho = s[i:j]
ci, cj = entre('      <!-- Right: animated chat demo -->', '\n    </div>\n\n    <div class="reveal text-center mt-14">', velho)
chat = velho[ci:cj].replace('<!-- Right: animated chat demo -->\n', '').replace('reveal liquid-glass rounded-3xl p-5 chat-window order-1 md:order-2', 'liquid-glass rounded-3xl p-5 chat-window')
chat = chat.rstrip()
fi = velho.index('<div class="reveal glass rounded-3xl p-6 order-1">'); fj = velho.index('\n\n      <div class="order-2">', fi)
fluxo = velho[fi:fj].replace('reveal glass rounded-3xl p-6 order-1', 'glass rounded-3xl p-6').replace('>ao vivo<', '>exemplo<').replace('>Automação rodando<', '>Publicação recebida<')
bi_i = velho.index('<div class="reveal glass rounded-3xl p-6 order-1 md:order-2" id="bi-demo">'); bi_j = velho.index('\n    </div>\n  </div>\n</section>', bi_i)
bi = velho[bi_i:bi_j].replace('reveal glass rounded-3xl p-6 order-1 md:order-2', 'glass rounded-3xl p-6').replace('class="counter"', 'class="bi-counter"')
bi = re.sub(r'\s*<span class="font-inter text-xs text-emerald inline-flex items-center gap-1">.*?</span>', '', bi, count=1, flags=re.S)
# avatar do chat com o símbolo novo
chat = re.sub(r'<svg width="22" height="22" viewBox="0 0 100 100".*?</svg>',
  '<svg width="22" height="20" viewBox="116.5 98.25 183.78 166.64" aria-hidden="true"><polygon fill="#141313" points="265.82 164.17 145.82 164.43 135.72 145.83 279.52 145.52 265.82 164.17"/><polygon fill="#141313" points="117.25 227.4 245.84 98.25 264.2 116.54 116.5 264.89 117.25 227.4"/><polygon fill="#141313" points="300.28 263.47 154.62 118.43 170.86 102.13 298.3 229.01 300.28 263.47"/><ellipse fill="#FDEADA" cx="207.92" cy="219.64" rx="22.43" ry="22.63"/></svg>', chat, count=1, flags=re.S)

def painel(pid, ativo, titulo, texto, extra, demo):
    return f'''      <div id="{pid}" role="tabpanel" aria-labelledby="{pid}-aba" class="painel-aba grid md:grid-cols-2 gap-10 md:gap-14 items-center"{'' if ativo else ' hidden'}>
        <div>
          <h3 class="font-heading font-bold text-polar mb-4" style="font-size:clamp(1.5rem,3.5vw,2rem);">{titulo}</h3>
          <p class="font-body text-polar/55 text-base leading-relaxed mb-6">{texto}</p>
          {extra}
        </div>
        {demo.strip()}
      </div>
'''
SETA = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="8" x2="13" y2="8"/><polyline points="9 4 13 8 9 12"/></svg>'
novo = f'''<!-- ════════ NA PRÁTICA (abas: atendimento, prazos, painel) ════════ -->
<section id="na-pratica" class="py-28 px-6 relative overflow-hidden">
  <div class="absolute top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[300px] rounded-full pointer-events-none" style="background:radial-gradient(ellipse,rgba(253,206,0,0.07),transparent 70%);" aria-hidden="true"></div>
  <div class="relative z-10 max-w-6xl mx-auto">
    <div class="text-center mb-10">
      <h2 class="reveal-head font-heading font-bold text-polar mb-4" style="font-size:clamp(2rem,5vw,3.25rem);">Na <span class="text-gradient">prática</span></h2>
      <p class="reveal font-body text-polar/55 text-lg max-w-xl mx-auto leading-relaxed">Três rotinas que deixam de ser feitas à mão.</p>
    </div>
    <div class="reveal flex justify-center mb-12">
      <div class="abas" role="tablist" aria-label="Exemplos" id="abas-pratica">
        <button class="aba" role="tab" id="pr-atendimento-aba" aria-controls="pr-atendimento" aria-selected="true">Atendimento</button>
        <button class="aba" role="tab" id="pr-prazos-aba" aria-controls="pr-prazos" aria-selected="false" tabindex="-1">Prazos</button>
        <button class="aba" role="tab" id="pr-painel-aba" aria-controls="pr-painel" aria-selected="false" tabindex="-1">Painel</button>
      </div>
    </div>
    <div class="reveal">
{painel('pr-atendimento', True, 'Um cliente pede horário pelo WhatsApp.', 'Um agente de IA lê o pedido, consulta a agenda e marca. Quando não sabe responder, chama alguém da equipe.', '<div class="passos-mini"><span><b>1</b>Entende</span><span><b>2</b>Consulta</span><span><b>3</b>Resolve</span></div>', chat)}{painel('pr-prazos', False, 'Uma intimação é publicada. O prazo entra na agenda.', 'O sistema lê o andamento, calcula o prazo, lança na agenda e avisa o advogado responsável.', '<p class="font-body text-polar/40 text-sm leading-relaxed">Ninguém precisa conferir o diário oficial todo dia.</p>', fluxo)}{painel('pr-painel', False, 'Seus números num só lugar.', 'Os dados que estavam em várias planilhas viram um painel. Você abre e vê como está o mês.', '<p class="font-body text-polar/40 text-sm leading-relaxed">Sem montar relatório.</p>', bi)}    </div>
    <div class="reveal text-center mt-14">
      <a href="#contato" class="btn-outline inline-flex items-center gap-2 rounded-full px-7 py-3.5 text-polar font-inter font-semibold text-sm cursor-pointer">Quero algo assim {SETA}</a>
    </div>
  </div>
</section>


'''
s = s[:i] + novo + s[j:]

# 5) Treinamentos: menos cartões, níveis numa trilha
s = s.replace('Treinamentos de IA <span class="text-gradient">sob medida</span>', 'Treinamentos <span class="text-gradient">de IA</span>', 1)
s = s.replace('Ensinamos sua equipe a usar o Claude e o Claude Code no trabalho, do primeiro pedido à criação de ferramentas próprias.',
              'Ensinamos sua equipe a usar o Claude e o Claude Code no trabalho. Para escritórios e empresas, com exemplos tirados das tarefas de cada equipe.', 1)
i, j = entre('    <!-- Para quem -->', '    <!-- Da base ao avançado -->')
s = s[:i] + s[j:]
s = s.replace('''    <div class="grid md:grid-cols-3 gap-6 mb-16">
      <!-- Nível 01 -->''', '''    <div class="relative hidden md:block h-4 mb-6" id="trilha" aria-hidden="true">
      <div class="trilha-linha" style="left:calc(16.666% - 8px);right:calc(16.666% - 8px);top:7px;"><i></i></div>
      <div class="grid grid-cols-3 relative"><div class="flex justify-center"><span class="trilha-no"></span></div><div class="flex justify-center"><span class="trilha-no"></span></div><div class="flex justify-center"><span class="trilha-no"></span></div></div>
    </div>
    <div class="grid md:grid-cols-3 gap-6 mb-12">
      <!-- Nível 01 -->''', 1)
i, j = entre('    <!-- Formato / o que está incluído -->', '    <div class="reveal text-center">\n      <a href="#contato" class="btn-cta magnetic')
s = s[:i] + '''    <p class="reveal text-center font-body text-polar/50 text-sm leading-relaxed mb-12">Online ou presencial <span class="text-polar/25 mx-2">·</span> Apostila com casos da sua área <span class="text-polar/25 mx-2">·</span> Exercícios desde a primeira aula <span class="text-polar/25 mx-2">·</span> Dúvidas tiradas depois do curso</p>

''' + s[j:]

# 6) Como trabalhamos: linha que preenche com a rolagem
s = re.sub(r'\n\s*<p class="reveal text-blue-glacial text-xs font-semibold tracking-\[0\.22em\] uppercase mb-4">Como funciona</p>', '', s, count=1)
s, n = re.subn(r'<div class="hidden md:block absolute" style="top:26px;left:calc\(16\.666% \+ 20px\);right:calc\(16\.666% \+ 20px\);height:1px;[^"]*" aria-hidden="true"></div>',
               '<div class="proc-linha hidden md:block" id="proc-linha" style="top:26px;left:calc(16.666% + 27px);right:calc(16.666% + 27px);" aria-hidden="true"><i></i></div>', s, count=1)
assert n == 1

# 7) Menu
s = s.replace('<a href="#agente-ia"  class="nav-link text-white/70 text-sm font-medium hover:text-white transition-colors duration-200">O que é IA</a>',
              '<a href="#na-pratica" class="nav-link text-white/70 text-sm font-medium hover:text-white transition-colors duration-200">Na prática</a>', 1)
s = s.replace('<a href="#agente-ia"  class="font-inter text-2xl text-polar/80 hover:text-emerald transition-colors" data-close-menu>O QUE É IA</a>',
              '<a href="#na-pratica" class="font-inter text-2xl text-polar/80 hover:text-emerald transition-colors" data-close-menu>NA PRÁTICA</a>', 1)
assert '#agente-ia' not in s, 'sobrou link para #agente-ia'

# 8) JS: painel com contadores próprios, abas, loops visíveis e linhas com rolagem
ji, jj = entre('  /* ── BI: barras crescendo ── */', '  /* ── Formulário → WhatsApp ── */')
s = s[:ji] + (pathlib.Path(__file__).parent / 'script.js').read_text() + '\n' + s[jj:]
p.write_text(s)
print('ok')

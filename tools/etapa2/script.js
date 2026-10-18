  /* ── Painel de exemplo: barras e números (repete ao reabrir a aba) ── */
  const biDemo = (function () {
    const demo = document.getElementById('bi-demo');
    if (!demo) return { play() {} };
    const bars = [...demo.querySelectorAll('.bi-bar')];
    const nums = [...demo.querySelectorAll('.bi-counter')];
    const reduceM = matchMedia('(prefers-reduced-motion: reduce)').matches;
    function play() {
      bars.forEach(b => { b.style.transition = 'none'; b.style.height = '0'; });
      void demo.offsetHeight;
      bars.forEach((b, i) => {
        b.style.transition = '';
        const h = (b.dataset.h || 0) + '%';
        if (reduceM) b.style.height = h; else setTimeout(() => { b.style.height = h; }, 60 + i * 90);
      });
      nums.forEach(el => {
        const to = +el.dataset.to, suf = el.dataset.suffix || '';
        if (reduceM) { el.textContent = to + suf; return; }
        const o = { v: 0 };
        gsap.to(o, { v: to, duration: 1.4, ease: 'power2.out', onUpdate: () => { el.textContent = Math.round(o.v) + suf; } });
      });
    }
    return { play };
  })();

  /* ── Na prática: abas ── */
  (function () {
    const lista = document.getElementById('abas-pratica');
    if (!lista) return;
    const abas = [...lista.querySelectorAll('[role="tab"]')];
    const paineis = abas.map(a => document.getElementById(a.getAttribute('aria-controls')));
    function mostrar(i, foco) {
      abas.forEach((a, k) => {
        const on = k === i;
        a.setAttribute('aria-selected', on ? 'true' : 'false');
        a.tabIndex = on ? 0 : -1;
        paineis[k].hidden = !on;
      });
      if (foco) abas[i].focus();
      if (paineis[i].id === 'pr-painel') biDemo.play();
      ScrollTrigger.refresh();
    }
    abas.forEach((a, i) => {
      a.addEventListener('click', () => mostrar(i));
      a.addEventListener('keydown', e => {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        e.preventDefault();
        mostrar((i + (e.key === 'ArrowRight' ? 1 : abas.length - 1)) % abas.length, true);
      });
    });
  })();

  /* ── Loops de demonstração: só rodam quando estão na tela ── */
  (function () {
    const loops = document.querySelectorAll('.loop');
    if (!('IntersectionObserver' in window)) { loops.forEach(l => l.classList.add('anim-on')); return; }
    const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('anim-on', e.isIntersecting)), { threshold: 0.2 });
    loops.forEach(l => io.observe(l));
  })();

  /* ── Trilha dos treinamentos e linha do processo: preenchem com a rolagem ── */
  [['#trilha', '.trilha-linha i', '.trilha-no'], ['#processo', '#proc-linha i', '.step-badge']].forEach(([alvo, linha, nos]) => {
    const fill = document.querySelector(alvo + ' ' + linha) || document.querySelector(linha);
    const pontos = [...document.querySelectorAll(alvo + ' ' + nos)];
    if (!fill) return;
    const marcar = p => pontos.forEach((n, i) => n.classList.toggle('on', p >= i / Math.max(1, pontos.length - 1) - 0.02));
    if (reduce) { fill.style.transform = 'none'; marcar(1); return; }
    gsap.to(fill, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: alvo, start: 'top 80%', end: 'top 40%', scrub: 0.6, onUpdate: st => marcar(st.progress) } });
  });

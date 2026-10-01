(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  const closeMenu = () => {
    if (!menu || !nav) return;
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', '메뉴 열기');
    nav.classList.remove('is-open');
  };
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    nav.classList.toggle('is-open', open);
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });

  const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
  const panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));
  const activate = (tab, focus = false, updateHash = false) => {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    panels.forEach(panel => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
    if (focus) tab.focus();
    if (updateHash) history.replaceState(null, '', '#'+tab.id);
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(tab, false, true));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (index+1)%tabs.length;
      if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (index-1+tabs.length)%tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length-1;
      if (next === undefined) return;
      event.preventDefault();
      activate(tabs[next], true, true);
    });
  });
  const selectHashTab = () => {
    const chosen = tabs.find(tab => '#'+tab.id === location.hash);
    if (chosen) activate(chosen);
  };
  if (tabs.length) {
    activate(tabs[0]);
    selectHashTab();
    window.addEventListener('hashchange', selectHashTab);
    const orientation = () => document.querySelector('[role="tablist"]').setAttribute('aria-orientation', matchMedia('(max-width: 760px)').matches ? 'horizontal' : 'vertical');
    orientation();
    window.addEventListener('resize', orientation);
  }

  const dialog = document.getElementById('diagram-dialog');
  const image = document.getElementById('zoom-image');
  const canvas = document.querySelector('.zoom-canvas');
  const level = document.getElementById('zoom-level');
  let scale = 1;
  let origin;
  const applyScale = () => {
    if (!image) return;
    image.style.width = `${scale*100}%`;
    level.value = `${Math.round(scale*100)}%`;
    document.getElementById('zoom-out').disabled = scale <= 1;
    document.getElementById('zoom-in').disabled = scale >= 3;
  };
  document.querySelectorAll('[data-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      if (!dialog?.showModal) {
        window.open(button.dataset.zoom, '_blank', 'noopener');
        return;
      }
      origin = button;
      image.src = button.dataset.zoom;
      image.alt = button.dataset.title;
      document.getElementById('diagram-title').textContent = button.dataset.title;
      scale = 1;
      applyScale();
      dialog.showModal();
      canvas.scrollTop = 0;
      canvas.scrollLeft = 0;
      document.getElementById('dialog-close').focus();
    });
  });
  document.getElementById('zoom-in')?.addEventListener('click', () => { scale = Math.min(3, scale+0.25); applyScale(); });
  document.getElementById('zoom-out')?.addEventListener('click', () => { scale = Math.max(1, scale-0.25); applyScale(); });
  document.getElementById('zoom-reset')?.addEventListener('click', () => { scale = 1; applyScale(); canvas.scrollTop=0; canvas.scrollLeft=0; });
  document.getElementById('dialog-close')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog?.addEventListener('close', () => origin?.focus());
})();

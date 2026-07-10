/* Accessible navigation: mobile menu toggle + click/keyboard dropdowns.
   Progressive enhancement — without JS, links still work and (on desktop)
   dropdowns fall back to :focus-within in CSS. */
(function () {
	'use strict';

	var nav = document.querySelector('.site-nav');
	if (!nav) return;

	var toggle = nav.querySelector('.nav-toggle');
	var menu = nav.querySelector('.nav-list');
	var dropdowns = Array.prototype.slice.call(nav.querySelectorAll('.dropdown'));

	function setMenu(open) {
		nav.classList.toggle('menu-open', open);
		if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
	}

	function closeDropdowns(except) {
		dropdowns.forEach(function (d) {
			if (d === except) return;
			d.classList.remove('is-open');
			var t = d.querySelector('.dropdown-toggle');
			if (t) t.setAttribute('aria-expanded', 'false');
		});
	}

	/* Mobile hamburger */
	if (toggle && menu) {
		toggle.addEventListener('click', function () {
			setMenu(!nav.classList.contains('menu-open'));
		});
	}

	/* Dropdowns: click to toggle */
	dropdowns.forEach(function (d) {
		var t = d.querySelector('.dropdown-toggle');
		if (!t) return;
		t.addEventListener('click', function (e) {
			e.preventDefault();
			var willOpen = !d.classList.contains('is-open');
			closeDropdowns(d);
			d.classList.toggle('is-open', willOpen);
			t.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
		});
	});

	/* Close on outside click */
	document.addEventListener('click', function (e) {
		if (!nav.contains(e.target)) closeDropdowns(null);
	});

	/* Theme toggle — flips the effective theme and persists it */
	var themeBtn = nav.querySelector('.theme-toggle');
	if (themeBtn && typeof window.__applyTheme === 'function') {
		themeBtn.addEventListener('click', function () {
			var current = document.documentElement.getAttribute('data-theme');
			var effective = current ||
				(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
			window.__applyTheme(effective === 'dark' ? 'light' : 'dark', true);
		});
	}

	/* Escape closes any open dropdown, then the mobile menu; restores focus */
	document.addEventListener('keydown', function (e) {
		if (e.key !== 'Escape' && e.key !== 'Esc') return;
		var openDrop = nav.querySelector('.dropdown.is-open');
		if (openDrop) {
			closeDropdowns(null);
			var t = openDrop.querySelector('.dropdown-toggle');
			if (t) t.focus();
		} else if (nav.classList.contains('menu-open')) {
			setMenu(false);
			if (toggle) toggle.focus();
		}
	});

	/* Copy buttons on code blocks (structure is emitted at build time). */
	function copyText(text) {
		if (navigator.clipboard && navigator.clipboard.writeText) {
			return navigator.clipboard.writeText(text);
		}
		/* Fallback for older/insecure contexts: a throwaway textarea. */
		return new Promise(function (resolve, reject) {
			try {
				var ta = document.createElement('textarea');
				ta.value = text;
				ta.setAttribute('readonly', '');
				ta.style.position = 'absolute';
				ta.style.left = '-9999px';
				document.body.appendChild(ta);
				ta.select();
				document.execCommand('copy');
				document.body.removeChild(ta);
				resolve();
			} catch (err) {
				reject(err);
			}
		});
	}

	document.addEventListener('click', function (e) {
		var btn = e.target.closest && e.target.closest('.code-copy');
		if (!btn) return;
		var block = btn.closest('.code-block');
		var code = block && block.querySelector('pre code');
		if (!code) return;
		var label = btn.querySelector('.code-copy-text');
		copyText(code.innerText).then(function () {
			btn.classList.add('copied');
			if (label) label.textContent = 'Copied';
			clearTimeout(btn._resetTimer);
			btn._resetTimer = setTimeout(function () {
				btn.classList.remove('copied');
				if (label) label.textContent = 'Copy';
			}, 1600);
		}).catch(function () {
			if (label) label.textContent = 'Press Ctrl+C';
		});
	});
})();

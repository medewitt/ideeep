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
})();

/* Shared behaviour for every page. Each block is guarded, because the
   elements it touches only exist on some of them. */

// sticky nav
const nav = document.getElementById('nav');
if (nav) {
  addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 30), { passive: true });
}

// mobile menu
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');
if (menuBtn && mobileMenu) {
  const setMenu = open => {
    mobileMenu.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
  };
  menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
  mobileMenu.addEventListener('click', e => { if (e.target.tagName === 'A') setMenu(false); });
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
}

// footer year
const yr = document.getElementById('yr');
if (yr) yr.textContent = new Date().getFullYear();

// local time, where it's shown
const lt = document.getElementById('localtime');
if (lt) {
  const tick = () => {
    lt.textContent = new Intl.DateTimeFormat('en-CA', {
      hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'America/Toronto'
    }).format(new Date()) + ' ET';
  };
  tick();
  setInterval(tick, 30000);
}

// seamless ticker — duplicate the strip so the -50% loop has no gap
const track = document.getElementById('tickTrack');
if (track && track.firstElementChild) {
  track.appendChild(track.firstElementChild.cloneNode(true));
}

// scroll reveal — progressive enhancement, never a way for content to go missing
const rv = document.querySelectorAll('.rv');
if (rv.length && 'IntersectionObserver' in window) {
  const showAll = () => rv.forEach(el => el.classList.add('in'));
  document.documentElement.classList.add('js-reveal');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px' });
  rv.forEach((el, i) => {
    el.style.transitionDelay = (i % 5) * 60 + 'ms';
    io.observe(el);
  });
  // safety net: if the observer never reports (background tab, odd embed), show everything
  setTimeout(showAll, 4000);
}

// enquiry form — posts in place via FormSubmit, no mail client needed
const form = document.getElementById('enquiryForm');
if (form) {
  const sendBtn = document.getElementById('sendBtn');
  const status = document.getElementById('formStatus');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (form.querySelector('.hp').value) return; // honeypot tripped
    sendBtn.disabled = true;
    status.className = 'status';
    status.textContent = 'Sending…';
    try {
      const res = await fetch('https://formsubmit.co/ajax/mikeallrounder33@gmail.com', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      });
      if (!res.ok) throw new Error('Request failed');
      form.reset();
      status.className = 'status ok';
      status.textContent = 'Sent — thank you. You’ll hear back within a day.';
    } catch (err) {
      status.className = 'status err';
      status.textContent = 'Something went wrong. Please email mikeallrounder33@gmail.com directly.';
    }
    sendBtn.disabled = false;
  });
}

// ===== PROFILE CONTENT =====
const profiles = {
    professional: {
        heroTag:     'OT Security &nbsp;&middot;&nbsp; Cybersecurity &nbsp;&middot;&nbsp; Data Analytics',
        heroSummary: 'Remediated critical OT vulnerabilities across 6 industrial units. Security-focused IT professional with 3 years of experience in OT security, incident response, and enterprise systems.',
        heroPrimary: { label: '&#9654; Explore Career', href: '#experience', download: false },
        heroSecondary: { label: '&#8659; Download CV',  href: 'CV_sadhvika.pdf', download: true },
        aboutHeading: 'Security Engineer &amp; OT Specialist',
        aboutBio1: "Currently pursuing a Master's in Information and Communication Engineering at TU Darmstadt, Germany. With hands-on experience at Evonik and Infosys, I bridge the gap between operational technology security and enterprise IT systems.",
        aboutBio2: 'Fluent in English (C2), conversational in German (B2), and native in Hindi, Kannada, and Tamil.',
        contactSub: 'Open to cybersecurity roles in OT/IT security, GRC, and threat intelligence.',
        navLabel:   'Professional',
    },
    personal: {
        heroTag:     'Engineer &nbsp;&middot;&nbsp; Multilingual &nbsp;&middot;&nbsp; Curious Mind',
        heroSummary: "Engineer by training, curious by nature. I've built industrial security dashboards, fraud detection models, and taught 100+ students to code — all while learning a new language. Currently calling Germany home.",
        heroPrimary: { label: '&#9654; My Story',  href: '#about', download: false },
        heroSecondary: { label: '&#9993; Say Hello', href: 'mailto:sadhvikachandra613@gmail.com', download: false },
        aboutHeading: 'Engineer &amp; Global Citizen',
        aboutBio1: "Pursuing a Master's in ICE at TU Darmstadt, Germany — far from home, loving every bit of it. I've worked across industrial cybersecurity, enterprise systems, and education tech. I like connecting dots across disciplines.",
        aboutBio2: "When I'm not hunting security vulnerabilities, you'll find me learning German, exploring European cities, or explaining algorithms to curious students. Fluent in 5 languages and always working on a sixth.",
        contactSub: 'Always happy to connect — whether you want to chat tech, languages, or life in Germany.',
        navLabel:   'Personal',
    },
};

// ===== APPLY PROFILE =====
function applyProfile(key) {
    const p = profiles[key];
    document.body.classList.remove('profile-professional', 'profile-personal');
    document.body.classList.add(`profile-${key}`);

    document.getElementById('hero-tag').innerHTML       = p.heroTag;
    document.getElementById('hero-summary').textContent = p.heroSummary;
    document.getElementById('about-heading').innerHTML  = p.aboutHeading;
    document.getElementById('about-bio-1').textContent  = p.aboutBio1;
    document.getElementById('about-bio-2').textContent  = p.aboutBio2;
    document.getElementById('contact-sub').textContent  = p.contactSub;

    const btnP = document.getElementById('hero-btn-primary');
    btnP.innerHTML = p.heroPrimary.label;
    btnP.href = p.heroPrimary.href;
    p.heroPrimary.download ? btnP.setAttribute('download','') : btnP.removeAttribute('download');

    const btnS = document.getElementById('hero-btn-secondary');
    btnS.innerHTML = p.heroSecondary.label;
    btnS.href = p.heroSecondary.href;
    p.heroSecondary.download ? btnS.setAttribute('download','') : btnS.removeAttribute('download');

    const switcher = document.getElementById('profile-switcher');
    document.getElementById('nav-profile-label').textContent = p.navLabel;
    switcher.classList.add('visible');
}

// ===== INTRO SEQUENCE =====
(function () {
    const intro   = document.getElementById('intro');
    const introAnim = document.getElementById('intro-anim');
    document.body.style.overflow = 'hidden';

    // Step 1 — dissolve stripes
    setTimeout(() => {
        document.querySelectorAll('.stripe').forEach(s => s.classList.add('dissolve'));
    }, 720);

    // Step 2 — fade out logo, show profile picker
    setTimeout(() => {
        introAnim.style.transition = 'opacity 0.45s ease';
        introAnim.style.opacity = '0';
        introAnim.style.pointerEvents = 'none';
    }, 2200);

    setTimeout(() => {
        introAnim.remove();
        intro.classList.add('show-profiles');
    }, 2650);

    // Profile card click
    document.querySelectorAll('.profile-card').forEach(card => {
        card.addEventListener('click', () => {
            const key = card.dataset.profile;
            applyProfile(key);

            intro.style.transition = 'opacity 0.7s ease';
            intro.style.opacity = '0';
            intro.style.pointerEvents = 'none';

            setTimeout(() => {
                intro.remove();
                document.body.style.overflow = '';
            }, 700);
        });
    });
})();

// ===== PROFILE SWITCHER (navbar) =====
document.getElementById('profile-switcher').addEventListener('click', () => {
    // Re-create the profile overlay without the animation
    const overlay = document.createElement('div');
    overlay.className = 'intro show-profiles';
    overlay.id = 'intro-repick';
    overlay.style.background = 'rgba(0,0,0,0.97)';
    overlay.innerHTML = `
        <div class="profiles-screen" style="opacity:1;pointer-events:all;position:relative;inset:auto;">
            <h2 class="profiles-heading">Switch Profile</h2>
            <div class="profiles-list">
                <button class="profile-card" data-profile="professional">
                    <div class="profile-avatar avatar-pro">
                        <svg viewBox="0 0 24 24" fill="white" width="52" height="52">
                            <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5L12 1z"/>
                        </svg>
                    </div>
                    <span class="profile-name">Professional</span>
                </button>
                <button class="profile-card" data-profile="personal">
                    <div class="profile-avatar avatar-personal">
                        <svg viewBox="0 0 24 24" fill="white" width="52" height="52">
                            <circle cx="12" cy="8" r="4"/>
                            <path d="M12 14c-5.33 0-8 2.67-8 4v1h16v-1c0-1.33-2.67-4-8-4z"/>
                        </svg>
                    </div>
                    <span class="profile-name">Personal</span>
                </button>
            </div>
            <button class="repick-cancel">Cancel</button>
        </div>`;

    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.35s ease';
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(() => { overlay.style.opacity = '1'; });

    function closeOverlay() {
        overlay.style.opacity = '0';
        setTimeout(() => { overlay.remove(); document.body.style.overflow = ''; }, 350);
    }

    overlay.querySelectorAll('.profile-card').forEach(card => {
        card.addEventListener('click', () => {
            applyProfile(card.dataset.profile);
            closeOverlay();
        });
    });
    overlay.querySelector('.repick-cancel').addEventListener('click', closeOverlay);
});

// ===== NAVBAR SCROLL =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

// ===== SMOOTH SCROLL =====
document.addEventListener('click', e => {
    const link = e.target.closest('a[href^="#"]');
    if (!link) return;
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const top = target.getBoundingClientRect().top + window.scrollY - 72;
    window.scrollTo({ top, behavior: 'smooth' });
});

// ===== FADE-IN ON SCROLL =====
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

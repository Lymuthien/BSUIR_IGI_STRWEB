document.addEventListener('DOMContentLoaded', () => {

    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    function applyTheme(t) {
        if (t === 'dark') {
            body.classList.add('dark');
            body.style.background = '#1a1a1a';
            document.documentElement.style.setProperty('--accent', '#4caf7d');
            document.documentElement.style.setProperty('--accent-2', '#556846');
            document.documentElement.style.setProperty('--muted', '#9e9e9e');
            document.documentElement.style.setProperty('--bg-gradient', 'linear-gradient(180deg, #2d2d2d 0%, #1f1f1f 100%)');
            document.documentElement.style.setProperty('--a-color', '#9dc178');
            document.documentElement.style.setProperty('--a-visited-color', '#bec1b0');
            document.documentElement.style.setProperty('--a-hover-bg', 'rgba(139, 195, 74, 0.2)');
        } else {
            body.classList.remove('dark');
            body.style.background = '';
            body.style.color = '';
            document.documentElement.style.setProperty('--accent', '#3a8d5a');
            document.documentElement.style.setProperty('--accent-2', '#b8dca0');
            document.documentElement.style.setProperty('--muted', '#6b7280');
            document.documentElement.style.setProperty('--bg-gradient', 'linear-gradient(180deg,#f7fbf6 0%, #eef6ec 100%)');
            document.documentElement.style.setProperty('--a-color', '#0b3f18');
            document.documentElement.style.setProperty('--a-visited-color', '#505e55');
            document.documentElement.style.setProperty('--a-hover-bg', 'rgba(255, 255, 255, 0.35)');
        }
        localStorage.setItem('lr3_theme', t);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = localStorage.getItem('lr3_theme') || 'light';
            applyTheme(current === 'light' ? 'dark' : 'light');
        });
        applyTheme(localStorage.getItem('lr3_theme') || 'light');
    }

});
function initProducts() {
    const serviceList = document.getElementById('serviceList');
    if (!serviceList) return;

    const pagerContainer = document.getElementById('productsPager') || document.createElement('div');
    if (!pagerContainer.parentNode) {
        serviceList.parentNode.appendChild(pagerContainer);
    }

    const allItems = Array.from(serviceList.querySelectorAll('.service-item'));
    if (allItems.length === 0) return;

    const perSelect = document.getElementById('productsPer');

    let per = Number(perSelect.value) || 3;
    let page = Number(sessionStorage.getItem('service_list_page')) || 1;

    function renderPage() {
        const total = allItems.length;
        const pages = Math.max(1, Math.ceil(total / per));
        if (page < 1) page = 1;
        if (page > pages) page = pages;

        allItems.forEach((it, idx) => {
            const start = (page - 1) * per;
            if (idx >= start && idx < start + per) {
                it.style.display = '';
            } else {
                it.style.display = 'none';
            }
        });

        pagerContainer.innerHTML = '';
        const pagesCount = Math.max(1, Math.ceil(total / per));
        const prev = document.createElement('button');
        prev.textContent = '<';
        prev.disabled = page === 1;
        prev.addEventListener('click', () => {
            page = Math.max(1, page - 1);
            sessionStorage.setItem('service_list_page', String(page));
            renderPage();
        });
        pagerContainer.appendChild(prev);

        const maxButtons = 5;
        let startPage = Math.max(1, page - Math.floor(maxButtons / 2));
        let endPage = Math.min(pagesCount, startPage + maxButtons - 1);
        if (endPage - startPage + 1 < maxButtons) {
            startPage = Math.max(1, endPage - maxButtons + 1);
        }
        for (let i = startPage; i <= endPage; i++) {
            const b = document.createElement('button');
            b.textContent = String(i);
            b.disabled = i === page;
            b.addEventListener('click', () => {
                page = i;
                sessionStorage.setItem('service_list_page', String(page));
                renderPage();
            });
            pagerContainer.appendChild(b);
        }

        const next = document.createElement('button');
        next.textContent = '>';
        next.disabled = page === pagesCount;
        next.addEventListener('click', () => {
            page = Math.min(pagesCount, page + 1);
            sessionStorage.setItem('service_list_page', String(page));
            renderPage();
        });
        pagerContainer.appendChild(next);

        const info = document.createElement('span');
        info.style.marginLeft = '8px';
        info.className = 'small';
        info.textContent = `Страница ${page} из ${pagesCount} — всего ${total} элементов`;
        pagerContainer.appendChild(info);
    }

    perSelect.addEventListener('change', (e) => {
        per = Number(e.target.value) || 3;
        page = 1;
        sessionStorage.setItem('service_list_page', String(page));
        renderPage();
    });

    renderPage();
}
initProducts();

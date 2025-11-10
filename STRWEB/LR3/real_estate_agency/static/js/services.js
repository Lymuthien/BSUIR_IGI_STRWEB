function initProducts() {
    const root = document.getElementById('productsRoot');
    const productsGrid = document.getElementById('productsGrid');
    if (root && productsGrid) {
        fetch('/static/lr3/products.json').then(r => r.json()).then(data => {
            const perSelect = document.getElementById('productsPer');
            let per = Number(perSelect.value || 3);
            let page = 1;

            function draw() {
                const grid = document.getElementById('productsGrid');
                grid.innerHTML = '';
                const start = (page - 1) * per;
                const arr = data.slice(start, start + per);
                arr.forEach(p => {
                    const c = document.createElement('div');
                    c.className = 'card';
                    c.innerHTML = `<img src="${p.img}" style="width:100%;height:160px;object-fit:cover;border-radius:8px;"><h4>${p.title}</h4><p class="small">${p.price}</p><p>${p.desc}</p>`;
                    grid.appendChild(c);
                });
                const pag = document.getElementById('productsPager');
                pag.innerHTML = '';
                const pages = Math.max(1, Math.ceil(data.length / per));
                for (let i = 1; i <= pages; i++) {
                    const b = document.createElement('button');
                    b.textContent = i;
                    b.disabled = i === page;
                    b.addEventListener('click', () => {
                        page = i;
                        draw();
                        // store page in session to keep on reload within session
                        sessionStorage.setItem('products_json_page', String(page));
                    });
                    pag.appendChild(b);
                }
            }

            const savedPage = Number(sessionStorage.getItem('products_json_page'));
            if (!isNaN(savedPage) && savedPage >= 1) {
            }

            perSelect.addEventListener('change', () => {
                per = Number(perSelect.value);
                page = 1;
                draw();
            });
            draw();
        }).catch(err => {
            console.error('Failed to load products.json', err);
        });
        return;
    }

    const serviceList = document.getElementById('serviceList');
    if (!serviceList) return; // nothing to paginate here

    const pagerContainer = document.getElementById('productsPager') || document.createElement('div');
    if (!pagerContainer.parentNode) {
        serviceList.parentNode.appendChild(pagerContainer);
    }

    const allItems = Array.from(serviceList.querySelectorAll('.service-item'));
    if (allItems.length === 0) return;

    const perSelect = document.getElementById('productsPer') || (function() {
        // create a small select if not present
        const wrapper = document.createElement('div');
        wrapper.style.marginBottom = '8px';
        const label = document.createElement('label');
        label.textContent = 'Показывать на странице: ';
        const sel = document.createElement('select');
        sel.id = 'productsPer';
        [3,6,9].forEach(n => {
            const o = document.createElement('option');
            o.value = String(n); o.textContent = String(n);
            sel.appendChild(o);
        });
        label.appendChild(sel);
        wrapper.appendChild(label);
        serviceList.parentNode.insertBefore(wrapper, serviceList);
        return sel;
    })();

    let per = Number(perSelect.value) || 3;
    let page = Number(sessionStorage.getItem('service_list_page')) || 1;

    function renderPage() {
        per = Math.max(1, Number(per) || 3);
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
        prev.textContent = '←';
        prev.disabled = page === 1;
        prev.addEventListener('click', () => { page = Math.max(1, page - 1); sessionStorage.setItem('service_list_page', String(page)); renderPage(); });
        pagerContainer.appendChild(prev);

        const maxButtons = 7;
        let startPage = Math.max(1, page - Math.floor(maxButtons / 2));
        let endPage = Math.min(pagesCount, startPage + maxButtons - 1);
        if (endPage - startPage + 1 < maxButtons) {
            startPage = Math.max(1, endPage - maxButtons + 1);
        }
        for (let i = startPage; i <= endPage; i++) {
            const b = document.createElement('button');
            b.textContent = String(i);
            b.disabled = i === page;
            b.addEventListener('click', () => { page = i; sessionStorage.setItem('service_list_page', String(page)); renderPage(); });
            pagerContainer.appendChild(b);
        }

        const next = document.createElement('button');
        next.textContent = '→';
        next.disabled = page === pagesCount;
        next.addEventListener('click', () => { page = Math.min(pagesCount, page + 1); sessionStorage.setItem('service_list_page', String(page)); renderPage(); });
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

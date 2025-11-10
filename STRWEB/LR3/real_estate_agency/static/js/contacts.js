document.addEventListener('DOMContentLoaded', function () {
    // Настройки
    const PAGE_SIZE = 3;
    const table = document.querySelector('.employees-table');
    const selectAllCheckbox = document.getElementById('select-all');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr')).filter(r => !r.classList.contains('empty-row'));
    const totalItems = rows.length;
    const totalPages = Math.max(1, Math.ceil(totalItems / PAGE_SIZE));

    // Хранилище выбранных id (сохраняет выбор при переключении страниц)
    const selectedIds = new Set();

    // Проставим data-employee-id и обработчики для индивидуальных чекбоксов
    rows.forEach(row => {
        const cb = row.querySelector('input.employee-checkbox');
        if (cb) {
            const id = cb.value;
            row.dataset.employeeId = id;
            cb.addEventListener('change', function () {
                if (cb.checked) selectedIds.add(id);
                else selectedIds.delete(id);
                // обновляем состояние select-all для текущей страницы
                updateSelectAllCheckbox();
            });
            // если чекбокс уже отмечен в разметке при загрузке — учтём это
            if (cb.checked) selectedIds.add(cb.value);
        }
    });

    // Создаем блок навигации и вставляем под таблицей
    const paginationWrapper = document.createElement('div');
    paginationWrapper.className = 'client-pagination pagination';
    paginationWrapper.setAttribute('aria-label', 'Навигация по страницам работников');

    const navList = document.createElement('ul');
    navList.style.margin = '0';
    navList.style.padding = '0';
    navList.style.display = 'flex';
    navList.style.gap = '6px';
    navList.style.listStyle = 'none';
    navList.style.alignItems = 'center';

    paginationWrapper.appendChild(navList);

    const pageInfo = document.createElement('div');
    pageInfo.className = 'page-info';
    pageInfo.style.marginTop = '8px';
    paginationWrapper.appendChild(pageInfo);

    table.parentNode.insertBefore(paginationWrapper, table.nextSibling);

    let currentPage = 1;

    function renderPage(page) {
        if (page < 1) page = 1;
        if (page > totalPages) page = totalPages;
        currentPage = page;

        const from = (currentPage - 1) * PAGE_SIZE;
        const to = from + PAGE_SIZE;

        rows.forEach((row, idx) => {
            if (idx >= from && idx < to) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
            // Обновляем чекбокс состояния из selectedIds
            const cb = row.querySelector('input.employee-checkbox');
            if (cb) {
                cb.checked = selectedIds.has(cb.value);
            }
        });

        renderPaginationControls();
        updateSelectAllCheckbox();
        pageInfo.textContent = `Страница ${currentPage} из ${totalPages} — всего записей: ${totalItems}`;
    }

    function renderPaginationControls() {
        navList.innerHTML = '';

        // Prev
        const prevLi = document.createElement('li');
        if (currentPage > 1) {
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = '«';
            a.addEventListener('click', function (e) {
                e.preventDefault();
                renderPage(currentPage - 1);
            });
            prevLi.appendChild(a);
        } else {
            prevLi.className = 'disabled';
            prevLi.textContent = '«';
        }
        navList.appendChild(prevLi);

        // Номера страниц — показываем максимум 5 навигационных кнопок вокруг текущей
        const windowSize = 5;
        let start = Math.max(1, currentPage - Math.floor(windowSize / 2));
        let end = Math.min(totalPages, start + windowSize - 1);
        if (end - start + 1 < windowSize) {
            start = Math.max(1, end - windowSize + 1);
        }

        for (let p = start; p <= end; p++) {
            const li = document.createElement('li');
            if (p === currentPage) {
                li.className = 'active';
                const span = document.createElement('span');
                span.textContent = String(p);
                li.appendChild(span);
            } else {
                const a = document.createElement('a');
                a.href = '#';
                a.textContent = String(p);
                a.addEventListener('click', (e) => {
                    e.preventDefault();
                    renderPage(p);
                });
                li.appendChild(a);
            }
            navList.appendChild(li);
        }

        // Next
        const nextLi = document.createElement('li');
        if (currentPage < totalPages) {
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = '»';
            a.addEventListener('click', function (e) {
                e.preventDefault();
                renderPage(currentPage + 1);
            });
            nextLi.appendChild(a);
        } else {
            nextLi.className = 'disabled';
            nextLi.textContent = '»';
        }
        navList.appendChild(nextLi);
    }

    // Select-all: влияет только на видимые строки
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function () {
            const visibleRows = rows.filter(row => row.style.display !== 'none');
            visibleRows.forEach(row => {
                const cb = row.querySelector('input.employee-checkbox');
                if (!cb) return;
                cb.checked = selectAllCheckbox.checked;
                if (cb.checked) selectedIds.add(cb.value);
                else selectedIds.delete(cb.value);
            });
            updateSelectAllCheckbox();
        });
    }

    function updateSelectAllCheckbox() {
        if (!selectAllCheckbox) return;
        const visibleRows = rows.filter(row => row.style.display !== 'none');
        if (visibleRows.length === 0) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
            return;
        }
        const checkedCount = visibleRows.reduce((c, row) => {
            const cb = row.querySelector('input.employee-checkbox');
            return c + (cb && cb.checked ? 1 : 0);
        }, 0);

        if (checkedCount === 0) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
        } else if (checkedCount === visibleRows.length) {
            selectAllCheckbox.checked = true;
            selectAllCheckbox.indeterminate = false;
        } else {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = true;
        }
    }

    // Покажем первую страницу
    renderPage(1);
});

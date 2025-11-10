document.addEventListener('DOMContentLoaded', function () {
    // Настройки
    const PAGE_SIZE = 3;
    const table = document.querySelector('.employees-table');
    const selectAllCheckbox = document.getElementById('select-all');
    if (!table) return;

    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
    // Собираем только непустые ряды (отфильтровываем пустую строку шаблона)
    let rows = Array.from(tbody.querySelectorAll('tr')).filter(r => !r.classList.contains('empty-row'));
    const totalItems = rows.length;
    let totalPages = Math.max(1, Math.ceil(totalItems / PAGE_SIZE));

    // Хранилище выбранных id (сохраняет выбор при переключении страниц и при сортировке)
    const selectedIds = new Set();

    // Сортировка: ключ и направление (1 = asc, -1 = desc)
    let sortKey = null;
    let sortDir = 1;

    // Проставим data-атрибуты и обработчики для индивидуальных чекбоксов
    rows.forEach(row => {
        const cb = row.querySelector('input.employee-checkbox');
        if (cb) {
            const id = cb.value;
            row.dataset.employeeId = id;
            // Удобно сохранять основные поля в data-*
            const idCell = row.querySelector('.cell-id');
            const nameCell = row.querySelector('.cell-name');
            const posCell = row.querySelector('.cell-position');
            const emailCell = row.querySelector('.cell-email');
            const phoneCell = row.querySelector('.cell-phone');

            row.dataset.id = idCell ? idCell.textContent.trim() : '';
            row.dataset.name = nameCell ? nameCell.textContent.trim() : '';
            row.dataset.position = posCell ? posCell.textContent.trim() : '';
            row.dataset.email = emailCell ? emailCell.textContent.trim() : '';
            row.dataset.phone = phoneCell ? phoneCell.textContent.trim() : '';

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

    // Создаем блок навигации и вставляем под таблицей (если ещё нет)
    let paginationWrapper = document.querySelector('.client-pagination.pagination');
    if (!paginationWrapper) {
        paginationWrapper = document.createElement('div');
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
    }

    const navList = paginationWrapper.querySelector('ul');
    const pageInfo = paginationWrapper.querySelector('.page-info');

    let currentPage = 1;

    // Обработчики заголовков для сортировки
    const sortableHeaders = Array.from(thead.querySelectorAll('th.sortable'));
    sortableHeaders.forEach(th => {
        const key = th.dataset.sortKey;
        if (!key) return;
        th.addEventListener('click', function () {
            if (sortKey === key) {
                sortDir = -sortDir; // переключаем направление
            } else {
                sortKey = key;
                sortDir = 1; // по умолчанию возрастание
            }
            // при сортировке логично показать первую страницу
            currentPage = 1;
            applySort();
            renderPage(currentPage);
            updateSortIndicators();
        });
    });

    function applySort() {
        if (!sortKey) return;
        // Сортируем массив rows — сравним data-sortKey
        rows.sort((a, b) => {
            const va = (a.dataset[sortKey] || '').trim();
            const vb = (b.dataset[sortKey] || '').trim();

            // для id — числовое сравнение
            if (sortKey === 'id') {
                const na = Number(va) || 0;
                const nb = Number(vb) || 0;
                return sortDir * (na - nb);
            }
            // Для остальных — локаль чувствительная к регистру
            const cmp = va.localeCompare(vb, undefined, { numeric: true, sensitivity: 'base' });
            return sortDir * cmp;
        });

        // После сортировки перестроим DOM (порядок в tbody)
        rows.forEach(r => tbody.appendChild(r));
    }

    function updateSortIndicators() {
        // Сбрасываем все
        sortableHeaders.forEach(th => {
            th.classList.remove('active');
            const ind = th.querySelector('.sort-indicator');
            if (ind) ind.textContent = '';
        });
        if (!sortKey) return;
        const activeTh = thead.querySelector(`th[data-sort-key="${sortKey}"]`);
        if (activeTh) {
            activeTh.classList.add('active');
            const ind = activeTh.querySelector('.sort-indicator');
            if (ind) ind.textContent = sortDir === 1 ? '▲' : '▼';
        }
    }

    function renderPage(page) {
        if (page < 1) page = 1;
        totalPages = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
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
        pageInfo.textContent = `Страница ${currentPage} из ${totalPages} — всего записей: ${rows.length}`;
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

    // Включаем сортировку по умолчанию (если нужно) — по id desc пример:
    // sortKey = 'id'; sortDir = -1; applySort(); renderPage(1); updateSortIndicators();

    // Покажем первую страницу
    applySort();
    updateSortIndicators();
    renderPage(1);
});

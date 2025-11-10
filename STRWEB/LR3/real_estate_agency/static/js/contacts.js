document.addEventListener('DOMContentLoaded', function () {
    // Настройки
    const PAGE_SIZE = 3;
    const table = document.querySelector('.employees-table');
    const selectAllCheckbox = document.getElementById('select-all');
    if (!table) return;
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
    // Собираем только непустые ряды (отфильтровываем пустую строку шаблона)
    const allRows = Array.from(tbody.querySelectorAll('tr')).filter(r => !r.classList.contains('empty-row'));
    let filteredRows = allRows.slice();
    const totalItems = allRows.length;
    let totalPages = Math.max(1, Math.ceil(filteredRows.length / PAGE_SIZE));
    // Хранилище выбранных id (сохраняет выбор при переключении страниц и при сортировке)
    const selectedIds = new Set();
    // Сортировка: ключ и направление (1 = asc, -1 = desc)
    let sortKey = null;
    let sortDir = 1;
    // Блок деталей
    const detailsBlock = document.querySelector('.employee-details');
    // Проставим data-атрибуты и обработчики для индивидуальных чекбоксов
    allRows.forEach(row => {
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
            const descCell = row.querySelector('.cell-description');
            const photoImg = row.querySelector('.cell-photo img');
            row.dataset.id = idCell ? idCell.textContent.trim() : '';
            row.dataset.name = nameCell ? nameCell.textContent.trim() : '';
            row.dataset.position = posCell ? posCell.textContent.trim() : '';
            row.dataset.email = emailCell ? emailCell.textContent.trim() : '';
            row.dataset.phone = phoneCell ? phoneCell.textContent.trim() : '';
            row.dataset.description = descCell ? descCell.textContent.trim() : '';
            row.dataset.photo = photoImg ? photoImg.src : '';
            cb.addEventListener('change', function () {
                if (cb.checked) selectedIds.add(id);
                else selectedIds.delete(id);
                // обновляем состояние select-all для текущей страницы
                updateSelectAllCheckbox();
            });
            // если чекбокс уже отмечен в разметке при загрузке — учтём это
            if (cb.checked) selectedIds.add(cb.value);
        }
        // Обработчик клика на строку (кроме чекбокса)
        row.addEventListener('click', function (e) {
            if (!e.target.matches('input[type="checkbox"]')) {
                showDetails(row);
            }
        });
    });
    // Функция показа деталей
    function showDetails(row) {
        if (!detailsBlock) return;
        const html = `
            <h3>Детали сотрудника</h3>
            <p>ID: ${row.dataset.id}</p>
            <p>ФИО: ${row.dataset.name}</p>
            <p>Должность: ${row.dataset.position}</p>
            <p>Email: ${row.dataset.email}</p>
            <p>Телефон: ${row.dataset.phone}</p>
            <p>Описание: ${row.dataset.description}</p>
            ${row.dataset.photo ? `<img src="${row.dataset.photo}" style="max-width: 100px; height: auto;" alt="Фото сотрудника">` : ''}
            <button class="close-details">Закрыть</button>
        `;
        detailsBlock.innerHTML = html;
        detailsBlock.style.display = 'block';
        // Обработчик закрытия
        detailsBlock.querySelector('.close-details').addEventListener('click', function () {
            detailsBlock.style.display = 'none';
        });
    }
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
    // Фильтрация
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', applyFilter);
    }
    function applyFilter() {
        const query = searchInput.value.trim().toLowerCase();
        if (!query) {
            filteredRows = allRows.slice();
        } else {
            filteredRows = allRows.filter(row => {
                return row.dataset.id.toLowerCase().includes(query) ||
                       row.dataset.name.toLowerCase().includes(query) ||
                       row.dataset.position.toLowerCase().includes(query) ||
                       row.dataset.email.toLowerCase().includes(query) ||
                       row.dataset.phone.toLowerCase().includes(query) ||
                       row.dataset.description.toLowerCase().includes(query);
            });
        }
        // После фильтрации применяем сортировку и рендерим первую страницу
        applySort();
        currentPage = 1;
        renderPage(currentPage);
    }
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
        // Сортируем массив filteredRows — сравним data-sortKey
        filteredRows.sort((a, b) => {
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
        filteredRows.forEach(r => tbody.appendChild(r));
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
        totalPages = Math.max(1, Math.ceil(filteredRows.length / PAGE_SIZE));
        if (page > totalPages) page = totalPages;
        currentPage = page;
        const from = (currentPage - 1) * PAGE_SIZE;
        const to = from + PAGE_SIZE;
        // Сначала скрываем все filteredRows
        filteredRows.forEach(row => {
            row.style.display = 'none';
        });
        filteredRows.forEach((row, idx) => {
            if (idx >= from && idx < to) {
                row.style.display = '';
            }
            // Обновляем чекбокс состояния из selectedIds
            const cb = row.querySelector('input.employee-checkbox');
            if (cb) {
                cb.checked = selectedIds.has(cb.value);
            }
        });
        // Показываем все allRows, которые не в filteredRows, как hidden (но они уже в DOM)
        allRows.forEach(row => {
            if (!filteredRows.includes(row)) {
                row.style.display = 'none';
            }
        });
        // Обработка пустого результата
        let noResultsRow = tbody.querySelector('.no-results-row');
        const visibleCount = filteredRows.filter(r => r.style.display !== 'none').length;
        if (filteredRows.length === 0 || visibleCount === 0) {
            if (!noResultsRow) {
                noResultsRow = document.createElement('tr');
                noResultsRow.className = 'no-results-row';
                const td = document.createElement('td');
                td.colSpan = 8;
                td.className = 'text-center';
                td.textContent = 'Сотрудники не найдены';
                noResultsRow.appendChild(td);
                tbody.appendChild(noResultsRow);
            }
            noResultsRow.style.display = '';
        } else {
            if (noResultsRow) {
                noResultsRow.style.display = 'none';
            }
        }
        // Если есть исходная empty-row и filteredRows не пуст, скрываем её
        const emptyRow = tbody.querySelector('.empty-row');
        if (emptyRow) {
            emptyRow.style.display = (allRows.length > 0) ? 'none' : '';
        }
        renderPaginationControls();
        updateSelectAllCheckbox();
        pageInfo.textContent = `Страница ${currentPage} из ${totalPages} — всего записей: ${filteredRows.length}`;
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
            const visibleRows = filteredRows.filter(row => row.style.display !== 'none');
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
        const visibleRows = filteredRows.filter(row => row.style.display !== 'none');
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
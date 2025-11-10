document.addEventListener('DOMContentLoaded', function () {
    // Настройки
    const PAGE_SIZE = 3;
    const table = document.querySelector('.employees-table');
    const selectAllCheckbox = document.getElementById('select-all');
    if (!table) return;
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
    const detailsBlock = document.querySelector('.employee-details');
    const bonusBlock = document.querySelector('.bonus-text');
    const awardBtn = document.getElementById('award-bonus-btn');
    const preloader = document.getElementById('preloader');
    // Хранилище выбранных id (сохраняет выбор при переключении страниц и при сортировке)
    const selectedIds = new Set();
    // Сортировка: ключ и направление (1 = asc, -1 = desc)
    let sortKey = null;
    let sortDir = 1;
    let allRows = [];
    let filteredRows = [];
    let totalPages = 1;
    let currentPage = 1;
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
    // Добавление формы
    const addBtn = document.querySelector('.add-employee-btn');
    const addForm = document.querySelector('.add-form');
    const addName = document.getElementById('add-name');
    const addPosition = document.getElementById('add-position');
    const addEmail = document.getElementById('add-email');
    const addPhone = document.getElementById('add-phone');
    const addDescription = document.getElementById('add-description');
    const addPhotoUrl = document.getElementById('add-photo-url');
    const validationMessage = document.querySelector('.validation-message');
    const addSubmit = document.getElementById('add-submit');
    addBtn.addEventListener('click', () => {
        addForm.style.display = 'block';
        // Сброс формы
        addName.value = '';
        addPosition.value = '';
        addEmail.value = '';
        addPhone.value = '';
        addDescription.value = '';
        addPhotoUrl.value = '';
        validationMessage.textContent = '';
        addSubmit.disabled = true;
        resetFieldStyles();
    });
    function resetFieldStyles() {
        [addName, addPosition, addEmail, addPhone, addDescription, addPhotoUrl].forEach(field => {
            field.style.border = '';
            field.style.backgroundColor = '';
        });
    }
    // Функции валидации
    function validateURL(url) {
        if (!url) return { valid: true, message: '' }; // Необязательное поле?
        const startsWithHttp = /^https?:\/\//i.test(url);
        const endsWithPhpHtml = /\.(php|html)$/i.test(url);
        if (startsWithHttp && endsWithPhpHtml) {
            return { valid: true, message: '' };
        } else {
            return { valid: false, message: 'Невалидный URL: должен начинаться с http:// или https:// и заканчиваться на .php или .html' };
        }
    }
    function validatePhone(phone) {
        if (!phone.trim()) return { valid: false, message: 'Телефон обязателен' };

        // Удаляем non-digits
        const digits = phone.replace(/\D/g, '');

        // Проверяем начало: 8... (11 digits) или 375... (12 digits)
        if (!((digits.startsWith('8') && digits.length === 11) || (digits.startsWith('375') && digits.length === 12))) {
            return { valid: false, message: 'Невалидная длина или префикс. Должно быть 11 (для 8...) или 12 (для 375...) цифр.' };
        }

        // Проверяем код оператора (29 для MTC)
        const codePos = digits.startsWith('8') ? 1 : 3; // После 8 или 375
        if (digits.substring(codePos, codePos + 2) !== '29' && digits.substring(codePos, codePos + 3) !== '029') {
            return { valid: false, message: 'Код оператора должен быть 29 или 029.' };
        }

        // Проверяем ровно 7 цифр после кода
        const afterCodePos = digits.startsWith('8') ? 4 : 5; // 8029... or 37529...
        if (digits.substring(afterCodePos).length !== 7) {
            return { valid: false, message: 'После кода оператора должно быть ровно 7 цифр.' };
        }

        // Для скобок: простая проверка баланса (опционально, если нужно строго)
        const openParens = (phone.match(/\(/g) || []).length;
        const closeParens = (phone.match(/\)/g) || []).length;
        if (openParens !== closeParens) {
            return { valid: false, message: 'Несбалансированные скобки.' };
        }

        return { valid: true, message: '' };
    }
    // Проверка всех полей
    function checkAllValid() {
        const fields = [addName, addPosition, addEmail, addDescription];
        const allFilled = fields.every(f => f.value.trim() !== '') && addPhone.value.trim() !== '';
        const phoneValid = validatePhone(addPhone.value).valid;
        const urlValid = validateURL(addPhotoUrl.value).valid;
        return allFilled && phoneValid && urlValid;
    }
    // Валидация поля
    function validateField(field, validateFunc) {
        const { valid, message } = validateFunc(field.value);
        if (!valid) {
            field.style.border = '1px solid red';
            field.style.backgroundColor = 'pink';
            validationMessage.textContent = message;
        } else {
            field.style.border = '';
            field.style.backgroundColor = '';
            validationMessage.textContent = '';
        }
    }
    // Обработчики
    addPhone.addEventListener('blur', () => validateField(addPhone, validatePhone));
    addPhotoUrl.addEventListener('blur', () => validateField(addPhotoUrl, validateURL));
    // Проверка на ввод для активации кнопки
    [addName, addPosition, addEmail, addPhone, addDescription, addPhotoUrl].forEach(input => {
        input.addEventListener('input', () => {
            if (validationMessage.textContent) {
                // Сброс сообщения если начали править
                validationMessage.textContent = '';
            }
            addSubmit.disabled = !checkAllValid();
        });
    });
    // Добавление
    addSubmit.addEventListener('click', async () => {
        // Финальная валидация
        validateField(addPhone, validatePhone);
        validateField(addPhotoUrl, validateURL);
        if (!checkAllValid()) return;
        const newEmployee = {
            name: addName.value.trim(),
            position: addPosition.value.trim(),
            email: addEmail.value.trim(),
            phone: addPhone.value.trim(),
            description: addDescription.value.trim(),
            photo_url: addPhotoUrl.value.trim() || null
        };
        preloader.style.display = 'flex';
        try {
            const csrfToken = getCookie('csrftoken');
            const response = await fetch('/accounts/api/employees/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(newEmployee)
            });
            if (!response.ok) {
                throw new Error('Ошибка добавления');
            }
            addForm.style.display = 'none';
            loadEmployees();
        } catch (error) {
            console.error('Ошибка:', error);
            validationMessage.textContent = 'Ошибка добавления сотрудника';
        } finally {
            preloader.style.display = 'none';
        }
    });
    // Функция для получения cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // Функция загрузки данных с сервера
    async function loadEmployees() {
        preloader.style.display = 'flex';
        try {
            const response = await fetch('/accounts/api/employees/');
            if (!response.ok) {
                throw new Error('Ошибка загрузки данных');
            }
            const employees = await response.json();
            // Очищаем tbody
            tbody.innerHTML = '';
            if (employees.length === 0) {
                const emptyRow = document.createElement('tr');
                emptyRow.className = 'empty-row';
                const td = document.createElement('td');
                td.colSpan = 8;
                td.className = 'text-center';
                td.textContent = 'Сотрудники не найдены';
                emptyRow.appendChild(td);
                tbody.appendChild(emptyRow);
                return;
            }
            // Создаём строки
            allRows = employees.map(emp => {
                const row = document.createElement('tr');
                // Чекбокс
                const cbTd = document.createElement('td');
                const cb = document.createElement('input');
                cb.type = 'checkbox';
                cb.className = 'employee-checkbox';
                cb.name = 'selected_employees';
                cb.value = emp.id;
                cbTd.appendChild(cb);
                row.appendChild(cbTd);
                // ID
                const idTd = document.createElement('td');
                idTd.className = 'cell-id';
                idTd.textContent = emp.id;
                row.appendChild(idTd);
                // Name
                const nameTd = document.createElement('td');
                nameTd.className = 'cell-name';
                nameTd.textContent = emp.name;
                row.appendChild(nameTd);
                // Position
                const posTd = document.createElement('td');
                posTd.className = 'cell-position';
                posTd.textContent = emp.position;
                row.appendChild(posTd);
                // Email
                const emailTd = document.createElement('td');
                emailTd.className = 'cell-email';
                emailTd.textContent = emp.email;
                row.appendChild(emailTd);
                // Phone
                const phoneTd = document.createElement('td');
                phoneTd.className = 'cell-phone';
                phoneTd.textContent = emp.phone;
                row.appendChild(phoneTd);
                // Description
                const descTd = document.createElement('td');
                descTd.className = 'cell-description';
                descTd.textContent = emp.description;
                row.appendChild(descTd);
                // Photo
                const photoTd = document.createElement('td');
                photoTd.className = 'cell-photo';
                if (emp.photo_url) {
                    const img = document.createElement('img');
                    img.src = emp.photo_url;
                    img.style.maxWidth = '50%';
                    img.style.height = 'auto';
                    img.alt = 'Фото сотрудника';
                    photoTd.appendChild(img);
                }
                row.appendChild(photoTd);
                // Data атрибуты
                row.dataset.employeeId = emp.id;
                row.dataset.id = emp.id || '';
                row.dataset.name = emp.name || '';
                row.dataset.position = emp.position || '';
                row.dataset.email = emp.email || '';
                row.dataset.phone = emp.phone || '';
                row.dataset.description = emp.description || '';
                row.dataset.photo = emp.photo_url || '';
                // Обработчики
                cb.addEventListener('change', function () {
                    if (cb.checked) selectedIds.add(emp.id.toString());
                    else selectedIds.delete(emp.id.toString());
                    updateSelectAllCheckbox();
                    updateAwardButton();
                });
                row.addEventListener('click', function (e) {
                    if (!e.target.matches('input[type="checkbox"]')) {
                        showDetails(row);
                    }
                });
                // Добавляем в tbody
                tbody.appendChild(row);
                return row;
            });
            filteredRows = allRows.slice();
            // Инициализируем
            applySort();
            updateSortIndicators();
            renderPage(1);
        } catch (error) {
            console.error('Ошибка:', error);
            // Можно показать ошибку в UI
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">Ошибка загрузки данных</td></tr>';
        } finally {
            preloader.style.display = 'none';
        }
    }
    // Загружаем данные при старте
    loadEmployees();
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
    // Select-all: влияет только на все отфильтрованные строки (все страницы)
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function () {
            filteredRows.forEach(row => {
                const cb = row.querySelector('input.employee-checkbox');
                if (!cb) return;
                cb.checked = selectAllCheckbox.checked;
                if (cb.checked) selectedIds.add(cb.value);
                else selectedIds.delete(cb.value);
            });
            updateSelectAllCheckbox();
            updateAwardButton();
        });
    }
    function updateSelectAllCheckbox() {
        if (!selectAllCheckbox) return;
        if (filteredRows.length === 0) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
            return;
        }
        const checkedCount = filteredRows.reduce((c, row) => {
            const cb = row.querySelector('input.employee-checkbox');
            return c + (cb && cb.checked ? 1 : 0);
        }, 0);
        if (checkedCount === 0) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
        } else if (checkedCount === filteredRows.length) {
            selectAllCheckbox.checked = true;
            selectAllCheckbox.indeterminate = false;
        } else {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = true;
        }
    }
    // Обновление кнопки Премировать (активна если есть выбранные)
    function updateAwardButton() {
        awardBtn.disabled = selectedIds.size === 0;
    }
    // Функционал премирования
    awardBtn.addEventListener('click', function () {
        if (selectedIds.size === 0) return;
        // Собираем фамилии (предполагаем, что фамилия - первое слово в name)
        const selectedSurnames = allRows
            .filter(row => selectedIds.has(row.dataset.employeeId))
            .map(row => row.dataset.name.split(' ')[0] || 'Без фамилии');
        if (selectedSurnames.length === 0) return;
        const text = `Премия выдается следующим сотрудникам: ${selectedSurnames.join(', ')}.`;
        bonusBlock.textContent = text;
        bonusBlock.style.display = 'block';
        // Опционально: сброс выбора после
        // selectedIds.clear();
        // renderPage(currentPage);
    });
    // Включаем сортировку по умолчанию (если нужно) — по id desc пример:
    // sortKey = 'id'; sortDir = -1; applySort(); renderPage(1); updateSortIndicators();
});
(function() {
    const root = document.getElementById('formGenRoot');
    if (!root) return;

    const flag = document.getElementById('fg_generate_flag');
    const container = document.getElementById('generatedContainer');
    const tmpl = document.getElementById('tmpl-generated-item');

    // storage key
    const STORAGE_KEY = 'lr3_generated_dynamic';

    // load saved array
    function loadItems() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
        } catch (e) {
            return [];
        }
    }

    function saveItems(arr) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
    }

    // create DOM for a single element card, returns element with dataset.index
    function createItemNode(item, index) {
        const node = tmpl.content.firstElementChild.cloneNode(true);
        node.dataset.index = index;

        const inputEl = node.querySelector('.gen-element');
        const ctlName = node.querySelector('.ctl-name');
        const ctlPlaceholder = node.querySelector('.ctl-placeholder');
        const ctlValue = node.querySelector('.ctl-value');
        const ctlPattern = node.querySelector('.ctl-pattern');
        const ctlRequired = node.querySelector('.ctl-required');
        const ctlReadonly = node.querySelector('.ctl-readonly');
        const btnDelete = node.querySelector('.ctl-delete');
        const btnFocus = node.querySelector('.ctl-focus');

        // apply attributes from item to real input
        function applyAttrsToInput() {
            inputEl.type = item.type || 'url';
            if (item.name) inputEl.setAttribute('name', item.name);
            else inputEl.removeAttribute('name');
            if (item.placeholder) inputEl.setAttribute('placeholder', item.placeholder);
            else inputEl.removeAttribute('placeholder');
            if (item.value) inputEl.value = item.value;
            else inputEl.value = '';
            if (item.pattern) inputEl.setAttribute('pattern', item.pattern);
            else inputEl.removeAttribute('pattern');
            if (item.required) inputEl.setAttribute('required', '');
            else inputEl.removeAttribute('required');
            if (item.readonly) inputEl.setAttribute('readonly', '');
            else inputEl.removeAttribute('readonly');
        }

        // populate controllers initial values
        ctlName.value = item.name || '';
        ctlPlaceholder.value = item.placeholder || '';
        ctlValue.value = item.value || '';
        ctlPattern.value = item.pattern || '';
        ctlRequired.checked = !!item.required;
        ctlReadonly.checked = !!item.readonly;

        // initial apply
        applyAttrsToInput();

        // live binding: whenever controller changes, update 'item' object, apply to input, persist storage
        function scheduleSave() {
            // update storage array
            const arr = loadItems();
            arr[index] = item;
            saveItems(arr);
        }

        // set handlers
        ctlName.addEventListener('input', (e) => {
            item.name = e.target.value || null;
            applyAttrsToInput();
            scheduleSave();
        });
        ctlPlaceholder.addEventListener('input', (e) => {
            item.placeholder = e.target.value || null;
            applyAttrsToInput();
            scheduleSave();
        });
        ctlValue.addEventListener('input', (e) => {
            item.value = e.target.value || null;
            applyAttrsToInput();
            scheduleSave();
        });
        ctlPattern.addEventListener('input', (e) => {
            item.pattern = e.target.value || null;
            applyAttrsToInput();
            scheduleSave();
        });
        ctlRequired.addEventListener('change', (e) => {
            item.required = e.target.checked;
            applyAttrsToInput();
            scheduleSave();
        });
        ctlReadonly.addEventListener('change', (e) => {
            item.readonly = e.target.checked;
            applyAttrsToInput();
            scheduleSave();
        });

        // clicking the generated input shows a quick snapshot of attributes (for UX)
        inputEl.addEventListener('click', () => {
            const attrs = [];
            if (inputEl.name) attrs.push('name="' + inputEl.name + '"');
            if (inputEl.placeholder) attrs.push('placeholder="' + inputEl.placeholder + '"');
            if (inputEl.value) attrs.push('value="' + inputEl.value + '"');
            if (inputEl.pattern) attrs.push('pattern="' + inputEl.pattern + '"');
            if (inputEl.required) attrs.push('required');
            if (inputEl.readOnly) attrs.push('readonly');
            // small tooltip-like inline alert (non-blocking)
            const old = node.querySelector('.gen-attrs-tip');
            if (old) old.remove();
            const tip = document.createElement('div');
            tip.className = 'gen-attrs-tip small';
            tip.style.marginTop = '6px';
            tip.textContent = 'Атрибуты: ' + (attrs.length ? attrs.join(' ') : '(нет)');
            node.appendChild(tip);
            setTimeout(() => {
                if (tip.parentNode) tip.remove();
            }, 2500);
        });

        // delete handler
        btnDelete.addEventListener('click', () => {
            // remove from DOM and storage
            const arr = loadItems();
            arr.splice(index, 1);
            saveItems(arr);
            // re-render all (to fix indexes)
            renderAll();
        });

        btnFocus.addEventListener('click', () => inputEl.focus());

        return node;
    }

    // add a new item (with optional defaults)
    function addNewItem(defaults) {
        const arr = loadItems();
        const newItem = Object.assign({
            type: 'url',
            name: '',
            placeholder: '',
            value: '',
            pattern: '',
            required: false,
            readonly: false
        }, defaults || {});
        arr.push(newItem);
        saveItems(arr);
        renderAll();
        return arr.length - 1;
    }

    // render all items from storage
    function renderAll() {
        const arr = loadItems();
        container.innerHTML = '';
        arr.forEach((it, idx) => {
            const node = createItemNode(it, idx);
            container.appendChild(node);
        });
    }

    // when user sets the checkbox, add element and immediately uncheck (so user can click again)
    flag.addEventListener('change', (e) => {
        if (e.target.checked) {
            addNewItem(); // create new
            // uncheck so user can add again easily
            setTimeout(() => {
                flag.checked = false;
            }, 100);
        }
    });

    // init on load
    renderAll();

    // expose small API for debugging (optional)
    window.lr3FormGen = {
        add: addNewItem,
        render: renderAll,
        save: () => saveItems(loadItems())
    };

})();
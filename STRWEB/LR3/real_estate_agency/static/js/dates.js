function DateRecordProto(day, month, year) {
    this.day = String(day);
    this.month = String(month);
    this.year = String(year);
}
DateRecordProto.prototype.getFull = function() {
    return `${this.day.padStart(2,'0')}.${this.month.padStart(2,'0')}.${this.year}`;
};
DateRecordProto.prototype.isSpring = function() {
    return [3, 4, 5].includes(Number(this.month));
};
DateRecordProto.prototype.toObj = function() {
    return {
        day: this.day,
        month: this.month,
        year: this.year
    };
};

function DateManagerProto(storageKey) {
    this.storageKey = storageKey || 'lr3_proto_dates';
    this.items = [];
    // load from storage
    try {
        const raw = localStorage.getItem(this.storageKey);
        if (raw) {
            const arr = JSON.parse(raw);
            this.items = arr.map(o => new DateRecordProto(o.day, o.month, o.year));
        }
    } catch (e) {
        this.items = [];
    }
}

DateManagerProto.prototype.getItems = function() {
    return this.items.slice();
};
DateManagerProto.prototype.setItems = function(arr) {
    this.items = arr.slice();
    try {
        localStorage.setItem(this.storageKey, JSON.stringify(this.items.map(i => i.toObj())));
    } catch (e) {}
};
DateManagerProto.prototype.addFromForm = function(formEl) {
    // formEl: элемент формы, ожидаем поля day, month, year
    const d = formEl.day.value.trim(),
        m = formEl.month.value.trim(),
        y = formEl.year.value.trim();
    if (!d || !m || !y) return false;
    const rec = new DateRecordProto(d, m, y);
    this.items.push(rec);
    this.setItems(this.items);
    return rec;
};
DateManagerProto.prototype.renderAll = function(container) {
    const root = (typeof container === 'string') ? document.getElementById(container) : container;
    if (!root) return;
    root.innerHTML = '';
    const ul = document.createElement('ul');
    this.items.forEach((it, idx) => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${it.getFull()}</strong> – ${it.isSpring() ? '<span>Spring</span>' : '<span>Not spring</span>'}
                        <div class="small">index: ${idx}</div>`;
        ul.appendChild(li);
    });
    root.appendChild(ul);
};
DateManagerProto.prototype.renderResult = function(container) {
    const root = (typeof container === 'string') ? document.getElementById(container) : container;
    if (!root) return;
    const total = this.items.length;
    const springs = this.items.filter(i => i.isSpring());
    const html = `<div><strong>Всего дат:</strong> ${total}</div>
                  <div><strong>Весенних дат:</strong> ${springs.length}</div>
                  <div class="small">Список весенних: ${springs.map(s=>s.getFull()).join(', ') || '(пусто)'}</div>`;
    // append or replace small result area
    let resBox = root.querySelector('.lr3-dates-summary');
    if (!resBox) {
        resBox = document.createElement('div');
        root.prepend(resBox);
    }
    resBox.innerHTML = html;
};

function SpringDateProto(day, month, year, source) {
    DateRecordProto.call(this, day, month, year);
    this.source = source || 'user';
}
SpringDateProto.prototype = Object.create(DateRecordProto.prototype);
SpringDateProto.prototype.constructor = SpringDateProto;
SpringDateProto.prototype.note = function() {
    return `(${this.source}) ${this.getFull()}`;
};

function SpringDateManagerProto(storageKey, sourceDefault) {
    DateManagerProto.call(this, storageKey || 'lr3_proto_spring_dates');
    this.sourceDefault = sourceDefault || 'user';
    try {
        const raw = localStorage.getItem(this.storageKey);
        if (raw) {
            const arr = JSON.parse(raw);
            this.items = arr.map(o => new SpringDateProto(o.day, o.month, o.year, o.source || this.sourceDefault));
        }
    } catch (e) {}
}
SpringDateManagerProto.prototype = Object.create(DateManagerProto.prototype);
SpringDateManagerProto.prototype.constructor = SpringDateManagerProto;

SpringDateManagerProto.prototype.addFromForm = function(formEl) {
    const d = formEl.day.value.trim(),
        m = formEl.month.value.trim(),
        y = formEl.year.value.trim();
    const src = formEl.source ? (formEl.source.value || this.sourceDefault) : this.sourceDefault;
    if (!d || !m || !y) return false;
    const rec = new SpringDateProto(d, m, y, src);
    this.items.push(rec);
    try {
        localStorage.setItem(this.storageKey, JSON.stringify(this.items.map(i => ({
            day: i.day,
            month: i.month,
            year: i.year,
            source: i.source
        }))))
    } catch (e) {}
    return rec;
};
SpringDateManagerProto.prototype.getSpringDates = function() {
    return this.items.filter(i => i.isSpring());
};
SpringDateManagerProto.prototype.renderResult = function(container) {
    const root = (typeof container === 'string') ? document.getElementById(container) : container;
    if (!root) return;
    const total = this.items.length;
    const springs = this.getSpringDates();
    const html = `<div><strong>Всего (SpringManager):</strong> ${total}</div>
                  <div><strong>Весенних:</strong> ${springs.length}</div>
                  <div class="small">Весенние с источником:<br>${springs.map(s => s.note()).join('<br>') || '(пусто)'}</div>`;
    let resBox = root.querySelector('.lr3-dates-summary');
    if (!resBox) {
        resBox = document.createElement('div');
        root.prepend(resBox);
    }
    resBox.innerHTML = html;
};


class DateRecord {
    constructor(day, month, year) {
        this.day = String(day);
        this.month = String(month);
        this.year = String(year);
    }
    getFull() {
        return `${this.day.padStart(2,'0')}.${this.month.padStart(2,'0')}.${this.year}`;
    }
    isSpring() {
        return [3, 4, 5].includes(Number(this.month));
    }
    toObj() {
        return {
            day: this.day,
            month: this.month,
            year: this.year
        };
    }
}

class SpringDates extends DateRecord {
    constructor(day, month, year, source) {
        super(day, month, year);
        this.source = source || 'user';
    }
    note() {
        return `Spring date: ${this.getFull()} from ${this.source}`;
    }
    toObj() {
        const base = super.toObj();
        base.source = this.source;
        return base;
    }
}

class DateManager {
    constructor(storageKey) {
        this.storageKey = storageKey || 'lr3_class_dates';
        this.items = [];
        // load
        try {
            const raw = localStorage.getItem(this.storageKey);
            if (raw) {
                const arr = JSON.parse(raw);
                this.items = arr.map(o => new DateRecord(o.day, o.month, o.year));
            }
        } catch (e) {
            this.items = [];
        }
    }
    getItems() {
        return this.items.slice();
    }
    setItems(arr) {
        this.items = arr.slice();
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.items.map(i => i.toObj())));
        } catch (e) {}
    }
    addFromForm(formEl) {
        const d = formEl.day.value.trim(),
            m = formEl.month.value.trim(),
            y = formEl.year.value.trim();
        if (!d || !m || !y) return false;
        const rec = new DateRecord(d, m, y);
        this.items.push(rec);
        this.setItems(this.items);
        return rec;
    }
    renderAll(container) {
        const root = (typeof container === 'string') ? document.getElementById(container) : container;
        if (!root) return;
        root.innerHTML = '';
        const ul = document.createElement('ul');
        this.items.forEach((it, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${it.getFull()}</strong> – ${it.isSpring() ? '<span>Spring</span>' : '<span>Not spring</span>'}`;
            ul.appendChild(li);
        });
        root.appendChild(ul);
    }
    renderResult(container) {
        const root = (typeof container === 'string') ? document.getElementById(container) : container;
        if (!root) return;
        const total = this.items.length;
        const springs = this.items.filter(i => i.isSpring());
        const html = `<div><strong>Всего (class):</strong> ${total}</div>
                      <div><strong>Весенних:</strong> ${springs.length}</div>
                      <div class="small">Весенние: ${springs.map(s => s.getFull()).join(', ') || '(пусто)'}</div>`;
        let resBox = root.querySelector('.lr3-dates-summary');
        if (!resBox) {
            resBox = document.createElement('div');
            root.prepend(resBox);
        }
        resBox.innerHTML = html;
    }
}

class SpringDateManager extends DateManager {
    constructor(storageKey, sourceDefault) {
        super(storageKey || 'lr3_class_spring_dates');
        this.sourceDefault = sourceDefault || 'user';
        // rehydrate as SpringDates if possible
        try {
            const raw = localStorage.getItem(this.storageKey);
            if (raw) {
                const arr = JSON.parse(raw);
                this.items = arr.map(o => new SpringDates(o.day, o.month, o.year, o.source || this.sourceDefault));
            }
        } catch (e) {}
    }
    addFromForm(formEl) {
        const d = formEl.day.value.trim(),
            m = formEl.month.value.trim(),
            y = formEl.year.value.trim();
        const src = formEl.source ? (formEl.source.value || this.sourceDefault) : this.sourceDefault;
        if (!d || !m || !y) return false;
        const rec = new SpringDates(d, m, y, src);
        this.items.push(rec);
        this.setItems(this.items); // will save via parent setItems
        return rec;
    }
    getSpringDates() {
        return this.items.filter(i => i.isSpring());
    }
    renderResult(container) {
        const root = (typeof container === 'string') ? document.getElementById(container) : container;
        if (!root) return;
        const total = this.items.length;
        const springs = this.getSpringDates();
        const html = `<div><strong>Всего (Spring class):</strong> ${total}</div>
                      <div><strong>Весенних:</strong> ${springs.length}</div>
                      <div class="small">Весенние с источником:<br>${springs.map(s => s.note()).join('<br>') || '(пусто)'}</div>`;
        let resBox = root.querySelector('.lr3-dates-summary');
        if (!resBox) {
            resBox = document.createElement('div');
            root.prepend(resBox);
        }
        resBox.innerHTML = html;
    }
}


(function() {
    const datesForm = document.getElementById('datesForm');
    const datesResult = document.getElementById('datesResult') || document.getElementById('datesResultProto');

    const protoManager = new DateManagerProto('lr3_proto_dates');
    const protoSpringManager = new SpringDateManagerProto('lr3_proto_spring_dates', 'proto_source');

    const classManager = new DateManager('lr3_class_dates');
    const classSpringManager = new SpringDateManager('lr3_class_spring_dates', 'class_source');

    const useClassVariant = (window.location.search.indexOf('class_dates=1') !== -1) || false;

    function renderAllAndResult() {
        if (useClassVariant) {
            classManager.renderAll(datesResult);
            classManager.renderResult(datesResult);
            classSpringManager.renderAll(datesResult);
            classSpringManager.renderResult(datesResult);
        } else {
            protoManager.renderAll(datesResult);
            protoManager.renderResult(datesResult);
            protoSpringManager.renderAll(datesResult);
            protoSpringManager.renderResult(datesResult);
        }
    }

    if (!datesForm) {
        if (datesResult) renderAllAndResult();
        return;
    }

    datesForm.addEventListener('submit', function(e) {
        e.preventDefault();
        try {
            protoManager.addFromForm(datesForm);
            protoSpringManager.addFromForm(datesForm);
        } catch (e) {
            console.error(e);
        }
        try {
            classManager.addFromForm(datesForm);
            classSpringManager.addFromForm(datesForm);
        } catch (e) {
            console.error(e);
        }
        // re-render chosen variant
        renderAllAndResult();
        // reset form inputs if desired
        datesForm.reset();
    });

    renderAllAndResult();

    const downloadAnchor = document.getElementById('springDownload');
    if (downloadAnchor) {
        downloadAnchor.addEventListener('click', function(ev) {
            ev.preventDefault();
            const arr = useClassVariant ? classSpringManager.getSpringDates() : protoSpringManager.getSpringDates();
            const content = JSON.stringify(arr.map(d => d.toObj ? d.toObj() : {
                day: d.day,
                month: d.month,
                year: d.year,
                source: d.source || ''
            }), null, 2);
            const blob = new Blob([content], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            downloadAnchor.href = url;
            downloadAnchor.download = 'g.txt';
            setTimeout(() => {
                URL.revokeObjectURL(url);
            }, 2000);
            downloadAnchor.click();
        });
    }
    (function() {
        const checkbox = document.getElementById('toggleClassVariant');
        if (!checkbox) return;

        const params = new URLSearchParams(window.location.search);
        const classMode = params.has('class_dates');

        checkbox.checked = classMode;

        checkbox.addEventListener('change', function() {
            const url = new URL(window.location.href);
            if (checkbox.checked) {
                url.searchParams.set('class_dates', '1');
            } else {
                url.searchParams.delete('class_dates');
            }
            window.location.href = url.toString();
        });
    })();

})();
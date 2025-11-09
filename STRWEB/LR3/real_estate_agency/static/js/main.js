document.addEventListener('DOMContentLoaded', () => {

    // SLIDER CLASS
    class Slider {
        constructor(node, options = {}) {
            this.root = node;
            this.slidesWrap = node.querySelector('.slides');
            this.slides = Array.from(node.querySelectorAll('.slide'));
            this.index = 0;

            this.options = Object.assign({
                loop: true,
                navs: true,
                pags: true,
                auto: false,
                stopMouseHover: true,
                delay: 5
            }, options);

            this.build();
            if (this.options.auto) this.startAuto();
        }
        build() {
            if (this.options.navs) {
                const navs = document.createElement('div');
                navs.className = 'navs';
                const prev = document.createElement('button');
                prev.textContent = '<';
                prev.addEventListener('click', () => this.prev());
                const next = document.createElement('button');
                next.textContent = '>';
                next.addEventListener('click', () => this.next());
                navs.appendChild(prev);
                navs.appendChild(next);
                this.root.appendChild(navs);
            }

            if (this.options.pags) {
                const pags = document.createElement('div');
                pags.className = 'pags';
                this.slides.forEach((s, i) => {
                    const b = document.createElement('button');
                    b.addEventListener('click', () => this.go(i));
                    pags.appendChild(b);
                });
                this.root.appendChild(pags);
                this.pags = pags.querySelectorAll('button');
            }

            this.update();

            if (this.options.stopMouseHover && this.options.auto) {
                this.root.addEventListener('mouseenter', () => this.stopAuto());
                this.root.addEventListener('mouseleave', () => this.startAuto());
            }
        }

        update() {
            this.slidesWrap.style.transform = `translateX(-${this.index*100}%)`;

            if (this.pags)
                this.pags.forEach((b, i) => {
                    b.classList.toggle('active', i === this.index);
                });
            const counter = this.root.querySelector('.counter');
            if (counter)
                counter.textContent = `${this.index+1}/${this.slides.length}`;
            const caption = this.root.querySelector('.caption');
            if (caption)
                caption.textContent = this.slides[this.index].dataset.caption || '';
        }

        next() {
            if (this.index + 1 < this.slides.length)
                this.index++;
            else if (this.options.loop)
                this.index = 0;
            else
                return;
            this.update();
        }
        prev() {
            if (this.index - 1 >= 0)
                this.index--;
            else if (this.options.loop)
                this.index = this.slides.length - 1;
            else
                return;
            this.update();
        }
        go(i) {
            this.index = Math.max(0, Math.min(i, this.slides.length - 1));
            this.update();
        }
        startAuto() {
            this.stopAuto();
            const delay = (this.options.delay || 5) * 1000;
            this._timer = setInterval(() => {
                if (this.options.auto) {
                    this.next();
                }
            }, delay);
        }
        stopAuto() {
            if (this._timer)
                clearInterval(this._timer);
            this._timer = null;
        }
        setLoop(value) {
            this.options.loop = value;
        }

        setAuto(value) {
            this.options.auto = value;
            if (value) {
                this.startAuto();
            } else {
                this.stopAuto();
            }
        }

        setDelay(value) {
            this.options.delay = value;
            if (this.options.auto) {
                this.startAuto();
            }
        }
    }

    // initialize sliders found
    document.querySelectorAll('.slider').forEach(sl => {
        // read options from data attributes or from admin form if present
        const options = {};
        ['loop', 'navs', 'pags', 'auto', 'stopmousehover'].forEach(k => {
            const v = sl.dataset[k];
            if (typeof v !== 'undefined') options[k === 'stopmousehover' ? 'stopMouseHover' : k] = (v === 'true');
        });
        if (sl.dataset.delay)
            options.delay = parseFloat(sl.dataset.delay);
        const s = new Slider(sl, options);

        const adminDelay = document.getElementById('sliderDelay');
        if (adminDelay) {
            const sliderLoop = document.getElementById('sliderLoop');
            const sliderAuto = document.getElementById('sliderAuto');
            adminDelay.addEventListener('change', (e) => {
                const delay = Number(e.target.value) || 5;
                s.setDelay(delay);
            });
            sliderLoop.addEventListener('change', (e) => {
                s.setLoop(e.target.checked);
            });

            sliderAuto.addEventListener('change', (e) => {
                s.setAuto(e.target.checked);
            });
        }
    });

});
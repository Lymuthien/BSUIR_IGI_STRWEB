document.addEventListener('DOMContentLoaded', () => {

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

            this._mouseEnterHandler = () => {
                if (this.options.stopMouseHover && this.options.auto) {
                    this.stopAuto();
                }
            };

            this._mouseLeaveHandler = () => {
                if (this.options.stopMouseHover && this.options.auto) {
                    this.startAuto();
                }
            };

            this.build();
            if (this.options.auto) this.startAuto();
        }

        createNavs() {
            if (this.navsElement) {
                this.navsElement.remove();
            }

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
            this.navsElement = navs;
        }

        createPags() {
            if (this.pagsElement) {
                this.pagsElement.remove();
            }

            const pags = document.createElement('div');
            pags.className = 'pags';
            this.slides.forEach((s, i) => {
                const b = document.createElement('button');
                b.addEventListener('click', () => this.go(i));
                pags.appendChild(b);
            });
            this.root.appendChild(pags);
            this.pagsElement = pags;
            this.pags = pags.querySelectorAll('button');
        }

        build() {
            if (this.options.navs) {
                this.createNavs()
            }

            if (this.options.pags) {
                this.createPags()
            }

            this.update();

            this.setMouse(this.options.stopMouseHover);
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
        setMouse(value) {
            this.options.stopMouseHover = value;

            this.root.removeEventListener('mouseenter', this._mouseEnterHandler);
            this.root.removeEventListener('mouseleave', this._mouseLeaveHandler);

            if (value && this.options.auto) {
                this.root.addEventListener('mouseenter', this._mouseEnterHandler);
                this.root.addEventListener('mouseleave', this._mouseLeaveHandler);
            }
        }

        setAuto(value) {
            this.options.auto = value;
            if (value) {
                this.startAuto();
            } else {
                this.stopAuto();
            }

            this.setMouse(this.options.stopMouseHover);
        }

        setDelay(value) {
            this.options.delay = value;
            if (this.options.auto) {
                this.startAuto();
            }
        }

        setNavs(value) {
            this.options.navs = value;
            if (value) {
                this.createNavs();
            } else if (this.navsElement) {
                this.navsElement.remove();
                this.navsElement = null;
            }
        }

        setPags(value) {
            this.options.pags = value;
            if (value) {
                this.createPags();
            } else if (this.pagsElement) {
                this.pagsElement.remove();
                this.pagsElement = null;
                this.pags = null;
            }
            this.update();
        }
    }

    document.querySelectorAll('.slider').forEach(sl => {
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
            adminDelay.addEventListener('change', (e) => {
                const delay = Number(e.target.value) || 5;
                s.setDelay(delay);
            });
        }

        const sliderLoop = document.getElementById('sliderLoop');
        if (sliderLoop) {
            sliderLoop.addEventListener('change', (e) => {
                s.setLoop(e.target.checked);
            });
        }

        const sliderAuto = document.getElementById('sliderAuto');
        if (sliderAuto) {
            sliderAuto.addEventListener('change', (e) => {
                s.setAuto(e.target.checked);
            });
        }

        const sliderNavs = document.getElementById('sliderNavs');
        if (sliderNavs) {
            sliderNavs.addEventListener('change', (e) => {
                s.setNavs(e.target.checked);
            });
        }
        const sliderPags = document.getElementById('sliderPags');
        if (sliderPags) {
            sliderPags.addEventListener('change', (e) => {
                s.setPags(e.target.checked);
            });
        }

        const sliderMouse = document.getElementById('sliderMouse');
        if (sliderMouse) {
            sliderMouse.addEventListener('change', (e) => {
                s.setMouse(e.target.checked);
            });
        }
    });
});
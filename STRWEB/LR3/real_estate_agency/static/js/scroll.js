document.addEventListener('DOMContentLoaded', function() {
    const parallaxSection = document.getElementById('parallax-section');
    const bg = document.getElementById('parallax-bg');
    const text = document.getElementById('parallax-text');
    const buildings = document.getElementById('buildings');
    const buildings1 = document.getElementById('buildings-1');
    const clouds2 = document.getElementById('clouds-2');
    const people = document.getElementById('people');

    if (!parallaxSection) return;

    window.addEventListener('scroll', function() {
        let value = window.scrollY;
        const sectionHeight = parallaxSection.offsetHeight;

        if (value > sectionHeight) {
            value = sectionHeight;
        }

        const scrollProgress = Math.min(value / sectionHeight, 1);

        if (bg) bg.style.transform = `translateY(${value * 0.5}px)`;
        if (text) text.style.transform = `translateY(${value}px)`;

        if (clouds2) clouds2.style.transform = `translateX(${-value * 0.2}px)`;

        if (buildings && buildings1) {
            const buildingProgress = Math.max(0, (scrollProgress - 0.1) / 0.6);

            if (buildingProgress > 0) {
                buildings.style.opacity = Math.min(buildingProgress * 1.5, 1);
                buildings.style.transform = `translateY(${(1 - buildingProgress) * 20}px)`;

                const building2Progress = Math.max(0, (scrollProgress - 0.2) / 0.5);

                buildings1.style.opacity = Math.min(building2Progress * 1.3, 1);
                buildings1.style.transform = `translateY(${130 - building2Progress * 60}px) translateX(-110px)`;
            } else {
                buildings.style.opacity = 0;
                buildings.style.transform = 'translateY(100px)';
                buildings1.style.opacity = 0;
                buildings1.style.transform = 'translateY(100px)';
            }
        }

        if (people) {
            const peopleProgress = Math.min(scrollProgress, 1);
            const translateY = peopleProgress * 100;
            const scale = 1 - (peopleProgress * 0.2);
            people.style.transform = `translateX(-50%) translateY(${translateY}px) scale(${scale})`;
        }
    });

    window.dispatchEvent(new Event('scroll'));
});
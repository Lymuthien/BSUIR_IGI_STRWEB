document.addEventListener('DOMContentLoaded', function() {
    if (!sessionStorage.getItem('birthdayVerified')) {
        showBirthdayModal();
    }

    function showBirthdayModal() {
        const modal = document.getElementById('birthdayModal');
        if (!modal) return;

        modal.style.display = 'flex';

        const birthForm = document.getElementById('birthForm');
        const birthResult = document.getElementById('birthResult');
        const dobInput = document.getElementById('dobInput');

        setTimeout(() => dobInput.focus(), 100);

        birthForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const d = new Date(dobInput.value);

            if (isNaN(d)) {
                birthResult.textContent = 'Пожалуйста, введите корректную дату';
                birthResult.style.color = 'red';
                return;
            }

            const now = new Date();
            let age = now.getFullYear() - d.getFullYear();
            const m = now.getMonth() - d.getMonth();

            if (m < 0 || (m === 0 && now.getDate() < d.getDate())) {
                age--;
            }

            const weekday = d.toLocaleDateString('ru-RU', {
                weekday: 'long'
            });

            sessionStorage.setItem('birthdayVerified', 'true');
            sessionStorage.setItem('userAge', age.toString());

            birthResult.textContent = `Возраст: ${age} лет. День недели: ${weekday}.`;
            birthResult.style.color = '#2c5530';

            if (age < 18) {
                setTimeout(() => {
                    alert('Вы несовершеннолетний(ая). Для использования сайта необходимо разрешение родителей.');
                    closeModal();
                }, 500);
            } else {
                setTimeout(() => {
                    closeModal();
                }, 2000);
            }
        });

        function closeModal() {
            modal.style.display = 'none';
        }
    }

    const logoutLinks = document.querySelectorAll('a[href*="logout"], form[action*="logout"]');

    logoutLinks.forEach(link => {
        link.addEventListener('click', function() {
            sessionStorage.removeItem('birthdayVerified');
            sessionStorage.removeItem('userAge');
        });
    });
});
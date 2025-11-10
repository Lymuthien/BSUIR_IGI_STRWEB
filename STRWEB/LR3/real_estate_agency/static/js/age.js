document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, показывалось ли уже модальное окно в этой сессии
    // sessionStorage очищается при закрытии браузера, но сохраняется при перезагрузке
    // Для сброса при logout нужно дополнительное действие (см. ниже)
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
        
        // Фокусируемся на поле ввода
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
            
            // Корректируем возраст если день рождения еще не наступил в этом году
            if (m < 0 || (m === 0 && now.getDate() < d.getDate())) {
                age--;
            }
            
            // Получаем день недели
            const weekday = d.toLocaleDateString('ru-RU', {
                weekday: 'long'
            });
            
            // Сохраняем в sessionStorage что проверка пройдена
            sessionStorage.setItem('birthdayVerified', 'true');
            sessionStorage.setItem('userAge', age.toString());
            
            // Показываем результат
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
        
        // Не даем закрыть модальное окно кликом вне его
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    }
});
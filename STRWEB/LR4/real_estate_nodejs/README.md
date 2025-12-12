## MongoDB:
- Подключение - server/config/database.js
- Модели (с валидаторами - Review, и типами данных) - server/models

## Аутентификация + авторизация:
- Разные способы + управление сессиями - server/config/passport.js
- проверка авт/аут - server/middleware/auth.js

## CRUD: все запросы (включая фильтрацию) - server/routes

## Формы - EstateForm.

## Наполнение: server/scripts/seed.js

## Таймзона: client/utils/dateUtils.js

## AI API:
- Ограничение запросов и логика - server/routes/estates.js
- В utils aiService

## Валидация форм
- На сервере в server/routes 
- На клиенте: EstateForm.js: Файл: client/src/components/EstateForm.js (строки 84-105)
Функция: validate() — проверка всех полей

### Примеры компонентов
- Navigation - функциональный с декларативной функцией 
- EstateCard - стрелочная функция
- MarketAnalyzer, DealFlow -классовый, setState
- DateTimeDisplay - useState, значение по умолчанию
- PropertyMatcher - useAuth -> useContext
- DealFlow - 189 строчка передача параметра в обработчик, Promise асинхронность.

### Навигация: Navigation.js

### Компонент в Home.js (комп в комп)
- DateTimeDisplay
- MarketAnalyzer 
- PropertyMatcher

## Обработчики событий
### onSubmit:
- `client/src/components/EstateForm.js` (строка 142)
- `client/src/pages/Reviews.js` (строка 77)
- `client/src/pages/EstateDetail.js` (строка 356)
- `client/src/pages/Login.js` (строка 74)
- `client/src/pages/Register.js` (строка 105)
- `client/src/pages/Catalog.js` (строка 148)
- `client/src/components/PropertyMatcher.js` (строка 74)

### onFocus:
- `client/src/components/EstateForm.js` - поля формы (address, cost, area, description, category)
- `client/src/pages/Register.js` - все поля формы (firstName, lastName, email, password, confirmPassword, phoneNumber, birthDate)
- `client/src/pages/Login.js` - поля email и password
- `client/src/pages/Reviews.js` - textarea для отзыва
- `client/src/pages/Catalog.js` - поле поиска (строка 155)

### onBlur:
- `client/src/components/EstateForm.js` - валидация при потере фокуса (строки 90-105)
- `client/src/pages/Register.js` - валидация при потере фокуса (строки 95-113)
- `client/src/pages/Login.js` - валидация при потере фокуса (строки 54-62)
- `client/src/pages/Reviews.js` - валидация textarea (строка 99)
- `client/src/pages/Catalog.js` - поле поиска (строка 156)

### onKeyPress:
- `client/src/components/EstateForm.js` - textarea для description (строка 317)
- `client/src/pages/Login.js` - поля email и password (строки 109, 120)
- `client/src/pages/Register.js` - все поля формы
- `client/src/pages/Reviews.js` - textarea для отзыва (строка 99)
- `client/src/pages/Catalog.js` - поле поиска, Enter выполняет поиск (строка 157)

### onMouseEnter/onMouseLeave:
- `client/src/components/DistrictMap.js` - интерактивные районы на карте (строки 51, 55)
- `client/src/components/EstateCard.js` - карточка объекта (строки 34-35, 36-37)

### onClick:
- `client/src/components/Navigation.js` (строка 74) - кнопка Logout
- `client/src/components/DealFlow.js` (строки 189, 195) - кнопки Complete/Cancel
- `client/src/pages/EstateDetail.js` (строки 192, 214, 348, 388) - различные кнопки
- `client/src/pages/Reviews.js` (строка 69) - переключение формы
- `client/src/components/PropertyMatcher.js` (строки 130, 135) - кнопки поиска и сброса
- `client/src/components/DistrictMap.js` (строка 50) - клик на район

### onChange:
- Все формы используют `onChange` для обработки изменений полей

## CSS

### Flexbox:
- `client/src/styles/index.css` (строка 40) - `#root`
- `client/src/styles/Catalog.css` (строки 14, 20) - `.filter-form`, `.filter-row`
- `client/src/styles/EstateCard.css` (строки 7, 39, 73, 93, 128, 137) - различные контейнеры
- `client/src/styles/Navigation.css` (строка 20) - навигация
- `client/src/styles/DealFlow.css` (строки 20, 33, 74, 97) - элементы управления
- `client/src/styles/PropertyMatcher.css` (строка 20) - форма подбора
- `client/src/styles/EstateDetail.css` (строки 43, 80, 87, 114, 134, 158) - детали объекта
- `client/src/styles/Reviews.css` (строки 7, 19, 38, 64) - отзывы
- `client/src/styles/MarketAnalyzer.css` (строка 20) - анализ рынка

### Grid:
- `client/src/styles/Catalog.css` (строка 31) - `.estates-grid` - галерея объектов
- `client/src/styles/EstateCard.css` (строка 86) - карточка объекта
- `client/src/styles/DealFlow.css` (строка 67) - `.deal-info`
- `client/src/styles/EstateForm.css` (строка 11) - форма
- `client/src/styles/PropertyMatcher.css` (строка 26) - форма подбора
- `client/src/styles/MarketAnalyzer.css` (строка 33) - статистика

### Transitions/Animations:
- `client/src/styles/index.css` (строка 11) - переменная `--transition: all 0.3s ease`
- `client/src/styles/Catalog.css` (строки 59, 62-71) - анимация `slideIn` для карточек
- `client/src/styles/DateTimeDisplay.css` (строки 7, 46, 49-54) - переходы и анимация `fadeIn`
- `client/src/styles/Home.css` (строки 11, 29, 37-44) - анимация `fadeInDown`
- `client/src/styles/Login.css` (строки 14, 17-25, 49, 95) - анимация `fadeInUp` и transitions
- `client/src/styles/Register.css` (строки 12, 15-23, 47) - анимация `fadeInUp` и transitions
- `client/src/styles/EstateCard.css` (строки 6, 29) - transitions для hover
- `client/src/styles/EstateDetail.css` (строки 13, 125) - transitions
- `client/src/styles/Navigation.css` (строки 3, 9, 18, 30, 48) - transitions для навигации
- `client/src/styles/DealFlow.css` (строки 6, 42) - transitions
- `client/src/styles/PropertyMatcher.css` (строки 6, 75) - transitions
- `client/src/styles/MarketAnalyzer.css` (строки 6, 45-46) - transitions и анимация

### Псевдоклассы (:hover, :focus, :active):
- `:hover`:
  - `client/src/styles/EstateCard.css` (строки 12, 32) - карточка объекта
  - `client/src/styles/Catalog.css` - через наследование
  - `client/src/styles/DealFlow.css` (строка 46) - элементы сделок
  - `client/src/styles/EstateDetail.css` (строка 16) - изображения
  - `client/src/styles/Reviews.css` (строка 32) - карточки отзывов
  - `client/src/styles/PropertyMatcher.css` (строка 78) - элементы списка
  - `client/src/styles/DateTimeDisplay.css` (строка 10) - отображение времени
  - `client/src/styles/Navigation.css` (строка 12, 34) - навигация
  - `client/src/styles/MarketAnalyzer.css` (строка 49) - статистические карточки
  - `client/src/styles/Home.css` (строка 32) - кнопки
  - `client/src/styles/EstateForm.css` (строки 81, 92) - кнопки формы
  - `client/src/styles/Login.css` (строка 103) - кнопки

- `:focus`:
  - `client/src/styles/EstateForm.css` (строка 36) - поля формы
  - `client/src/styles/Navigation.css` (строка 38) - ссылки навигации
  - `client/src/styles/PropertyMatcher.css` (строка 42) - поля формы
  - `client/src/styles/Login.css` (строка 53) - поля формы
  - `client/src/styles/Register.css` (строка 51) - поля формы

- `:active`:
  - `client/src/styles/Navigation.css` (строки 43, 56) - ссылки и кнопки

### Адаптивный дизайн:
- `client/src/styles/Catalog.css` (строки 37-50, 52-56) - медиа-запросы для мобильных и планшетов
- `client/src/styles/EstateDetail.css` (строка 216) - медиа-запрос для мобильных
- `client/src/styles/Reviews.css` (строка 71) - медиа-запрос для мобильных
- `client/src/styles/DealFlow.css` (строка 125) - медиа-запрос для мобильных
- `client/src/styles/EstateForm.css` (строка 98) - медиа-запрос для мобильных
- `client/src/styles/DateTimeDisplay.css` (строка 60) - медиа-запрос для мобильных
- `client/src/styles/EstateCard.css` (строка 137) - медиа-запрос для мобильных
- `client/src/styles/Login.css` (строка 127) - медиа-запрос для мобильных
- `client/src/styles/Navigation.css` (строка 60) - медиа-запрос для мобильных
- `client/src/styles/MarketAnalyzer.css` (строка 85) - медиа-запрос для мобильных
- `client/src/styles/PropertyMatcher.css` (строка 83) - медиа-запрос для мобильных
- `client/src/styles/Home.css` (строка 48) - медиа-запрос для мобильных
- `client/src/styles/Register.css` (строка 68) - медиа-запрос для мобильных

### CSS Variables для темизации:
- `client/src/styles/index.css` (строки 1-13) - все CSS переменные определены в `:root`:
  - `--primary-color`
  - `--secondary-color`
  - `--success-color`
  - `--danger-color`
  - `--warning-color`
  - `--info-color`
  - `--light-color`
  - `--dark-color`
  - `--border-radius`
  - `--transition`
  - `--shadow`
  - `--shadow-lg`

- Использование переменных:
  - `client/src/styles/Catalog.css` (строка 7) - `var(--border-radius)`, `var(--shadow)`
  - `client/src/styles/DateTimeDisplay.css` (строка 7) - `var(--transition)`
  - `client/src/styles/EstateCard.css` (строка 6) - `var(--transition)`
  - И многие другие файлы используют CSS переменные

### Семантические классы:
- Все CSS классы используют семантические названия:
  - `.estate-card`, `.estate-detail`, `.deal-flow`
  - `.catalog-page`, `.filter-form`, `.estates-grid`
  - `.review-form`, `.review-item`
  - `.navigation`, `.navbar`, `.nav-link`
  - `.form-group`, `.form-control`, `.form-actions`
  - `.hero-section`, `.dashboard-page`

### Хуки
- useState - управление состоянием
- useEffect - жизненный цикл
- useContext - контекст аутентификации
- useReducer - состояние каталога

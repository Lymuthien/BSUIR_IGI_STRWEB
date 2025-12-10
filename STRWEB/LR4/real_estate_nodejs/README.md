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

## CSS требования

### Flexbox Layout:
- `client/src/styles/index.css` (строка 40) - `#root`
- `client/src/styles/Catalog.css` (строки 14, 20) - `.filter-form`, `.filter-row`
- `client/src/styles/EstateCard.css` (строки 7, 39, 73, 93, 128, 137) - различные контейнеры
- `client/src/styles/Navigation.css` (строка 20) - навигация
- `client/src/styles/DealFlow.css` (строки 20, 33, 74, 97) - элементы управления
- `client/src/styles/PropertyMatcher.css` (строка 20) - форма подбора
- `client/src/styles/EstateDetail.css` (строки 43, 80, 87, 114, 134, 158) - детали объекта
- `client/src/styles/Reviews.css` (строки 7, 19, 38, 64) - отзывы
- `client/src/styles/MarketAnalyzer.css` (строка 20) - анализ рынка

### Grid Layout:
- `client/src/styles/Catalog.css` (строка 31) - `.estates-grid` - галерея объектов
- `client/src/styles/EstateCard.css` (строка 86) - карточка объекта
- `client/src/styles/DealFlow.css` (строка 67) - `.deal-info`
- `client/src/styles/EstateForm.css` (строка 11) - форма
- `client/src/styles/PropertyMatcher.css` (строка 26) - форма подбора
- `client/src/styles/MarketAnalyzer.css` (строка 33) - статистика

### CSS Transitions/Animations:
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


# Real Estate Agency - Node.js + React Application

Веб-приложение риэлторского агентства, разработанное с использованием Node.js (Express) для сервера и React для клиента.

## Структура проекта

```
real_estate_nodejs/
├── server/          # Express сервер
│   ├── models/      # Mongoose модели
│   ├── routes/      # API маршруты
│   ├── middleware/  # Middleware
│   ├── config/      # Конфигурация
│   ├── utils/       # Утилиты (AI сервисы)
│   └── scripts/     # Скрипты (seed данные)
└── client/          # React приложение
    ├── src/
    │   ├── components/  # React компоненты
    │   ├── pages/       # Страницы
    │   ├── services/    # API сервисы
    │   ├── context/     # React Context
    │   ├── utils/       # Утилиты
    │   └── styles/      # CSS стили
    └── public/
```

## Технологии

### Клиент
- React 18
- React Router DOM
- Axios
- Bootstrap 5
- date-fns + date-fns-tz
- CSS (Flexbox/Grid, Animations, Responsive)

## Установка и запуск

### Сервер

1. Перейти в папку server:
```bash
cd server
```

2. Установить зависимости:
```bash
npm install
```

3. Создать `.env` файл:
```env
PORT=3001
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/real_estate_agency
SESSION_SECRET=your-secret-key-change-in-production
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_VISION_API_KEY=your-google-vision-api-key
CLIENT_URL=http://localhost:3000
```

4. Запустить MongoDB

5. Заполнить базу данных тестовыми данными:
```bash
npm run seed
```

6. Запустить сервер:
```bash
npm run dev
```

Сервер будет доступен на `http://localhost:3001`

### Клиент

1. Перейти в папку client:
```bash
cd client
```

2. Установить зависимости:
```bash
npm install
```

3. Создать `.env` файл (опционально):
```env
REACT_APP_API_URL=http://localhost:3001/api
```

4. Запустить приложение:
```bash
npm start
```

Приложение будет доступно на `http://localhost:3000`

## Основные возможности

### Авторизация
- Регистрация и вход по email/паролю
- Вход через Google OAuth
- Роли пользователей: client, employee, admin

### Каталог недвижимости
- Просмотр всех объектов (публичный доступ)
- Поиск по адресу и описанию
- Фильтрация по цене, площади, статусу
- Сортировка по цене, площади, дате
- Детальный просмотр объекта

### CRUD операции (для авторизованных)
- Создание объектов недвижимости
- Редактирование объектов
- Удаление объектов
- Создание и управление отзывами

### AI функции
- Google Vision AI - анализ фотографий недвижимости

### Асинхронность
- XMLHttpRequest - загрузка файлов с прогрессом
- setTimeout - таймеры и периодические обновления
- Promise/async-await - цепочки операций и параллельные запросы

### Отображение дат и времени
- Текущее время в локальной таймзоне и UTC
- Даты создания/обновления записей
- Форматирование дат с учетом таймзоны пользователя

## Модели данных

1. **User** - Пользователи (client, employee, admin)
2. **Estate** - Объекты недвижимости
3. **Service & ServiceCategory** - Услуги и категории
4. **Sale** - Сделки
5. **Review** - Отзывы

## React компоненты

### Типы компонентов
- Функциональные компоненты (декларативные функции)
- Функциональные компоненты (стрелочные функции)
- Классовые компоненты

### Примеры компонентов
- `Navigation` - навигация (функциональный)
- `EstateCard` - карточка объекта (стрелочная функция)
- `MarketAnalyzer` - анализ рынка (классовый)
- `PropertyMatcher` - подбор объектов (useContext)
- `DealFlow` - управление сделками (классовый)
- `AsyncOperations` - демонстрация асинхронности

### Обработчики событий
- onClick - логаут кнопка. components/navigation.js
- onChange - формы, селекты
- onSubmit - формы
- onFocus - фокус на элементах
- onBlur - потеря фокуса
- onKeyPress - клавиатура
- onMouseEnter/onMouseLeave - наведение

### Хуки
- useState - управление состоянием
- useEffect - жизненный цикл
- useContext - контекст аутентификации
- useReducer - состояние каталога
- useRef - ссылки на элементы

## CSS особенности

- Flexbox и Grid Layout
- CSS Transitions и Animations
- Псевдоклассы (:hover, :focus, :active)
- Адаптивный дизайн (mobile-first)
- CSS Variables для темизации

## API Endpoints

- `GET /api` - информация о сервере
- `POST /api/auth/register` - регистрация
- `POST /api/auth/login` - вход
- `POST /api/auth/logout` - выход
- `GET /api/auth/me` - текущий пользователь
- `GET /api/estates` - список объектов (поиск, фильтры, сортировка)
- `GET /api/estates/:id` - детали объекта
- `POST /api/estates` - создание объекта (требуется авторизация)
- `PUT /api/estates/:id` - обновление объекта (требуется авторизация)
- `DELETE /api/estates/:id` - удаление объекта (требуется авторизация)
- `POST /api/reviews` - создание отзыва
- `POST /api/estates/:id/analyze-image` - анализ изображения (Google Vision AI)


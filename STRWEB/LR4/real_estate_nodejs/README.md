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

### Сервер
- Node.js
- Express.js
- MongoDB + Mongoose
- Passport.js (Local + Google OAuth)
- Multer (загрузка файлов)
- Express Validator
- OpenAI API
- Google Vision API

### Клиент
- React 18
- React Router DOM
- Axios
- Bootstrap 5
- date-fns + date-fns-tz
- CSS (Flexbox/Grid, Animations, Responsive)

## Установка и запуск

### Требования
- Node.js 16+
- MongoDB 4.4+
- API ключи для OpenAI и Google Vision (опционально)

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
OPENAI_API_KEY=your-openai-api-key
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
- OpenAI GPT - генерация описаний и AI-консультант

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
- `AIConsultant` - AI консультант (хуки)
- `AsyncOperations` - демонстрация асинхронности

### Обработчики событий
- onClick - кнопки, ссылки
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
- `POST /api/ai/consultation` - AI консультация

## Тестовые данные

Скрипт seed создает:
- 4 пользователя (admin, employee, 2 clients)
- 4 категории услуг
- 4 услуги
- 12 объектов недвижимости
- 2 отзыва

## Примечания

- Для работы Google OAuth необходимо настроить OAuth credentials в Google Cloud Console
- Для работы AI функций необходимы API ключи OpenAI и Google Vision
- MongoDB должна быть запущена перед запуском сервера

## Лицензия

ISC


# Быстрый старт

## Шаг 1: Установка MongoDB

Убедитесь, что MongoDB установлена и запущена:
```bash
# Проверить статус MongoDB
mongod --version
```

## Шаг 2: Запуск сервера

```bash
cd server
npm install
# Создать .env файл (скопировать из .env.example и заполнить)
npm run seed  # Заполнить базу тестовыми данными
npm run dev   # Запустить в режиме разработки
```

Сервер будет доступен на `http://localhost:3001`

## Шаг 3: Запуск клиента

В новом терминале:
```bash
cd client
npm install
npm start
```

Клиент будет доступен на `http://localhost:3000`

## Тестовые аккаунты

После выполнения `npm run seed` будут созданы:

**Admin:**
- Email: admin@agency.com
- Password: admin123

**Employee:**
- Email: employee1@agency.com
- Password: emp123

**Client:**
- Email: client1@example.com
- Password: client123

## Важные замечания

1. MongoDB должна быть запущена перед запуском сервера
2. Для Google OAuth нужно настроить OAuth credentials в Google Cloud Console
3. AI функции требуют API ключи (опционально, приложение работает и без них)
4. Для работы с изображениями создайте папку `server/uploads`

## Структура .env файла сервера

```env
PORT=3001
MONGODB_URI=mongodb://localhost:27017/real_estate_agency
SESSION_SECRET=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OPENAI_API_KEY=your-openai-api-key
GOOGLE_VISION_API_KEY=your-vision-api-key
CLIENT_URL=http://localhost:3000
```

## Основные URL

- Главная: http://localhost:3000
- Каталог: http://localhost:3000/catalog
- API: http://localhost:3001/api
- Демо асинхронности: http://localhost:3000/async-demo

## Функциональность

### Для всех пользователей:
- Просмотр каталога недвижимости
- Поиск и фильтрация объектов
- Просмотр деталей объекта
- AI консультант

### Для авторизованных пользователей:
- Создание/редактирование объектов (employee/admin)
- Создание отзывов
- Управление сделками (employee/admin)

### Для неавторизованных:
- Только просмотр каталога
- Поиск и сортировка
- Авторизация


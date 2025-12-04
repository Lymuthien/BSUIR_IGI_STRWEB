# Real Estate Agency Server

Node.js + Express + MongoDB server for Real Estate Agency application.

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Configure environment variables in `.env`:
- Set `MONGODB_URI` (default: mongodb://localhost:27017/real_estate_agency)
- Set `SESSION_SECRET` (generate a random secret)
- Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` for Google OAuth
- Set `OPENAI_API_KEY` for AI features
- Set `GOOGLE_VISION_API_KEY` for image analysis

4. Make sure MongoDB is running

5. Seed the database:
```bash
npm run seed
```

## Running

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm start
```

Server will run on `http://localhost:3001` by default.

## API Endpoints

- `GET /api` - Server info
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `GET /api/auth/google` - Google OAuth login
- `GET /api/estates` - Get estates (public, with search/sort/filter)
- `GET /api/estates/:id` - Get single estate
- `POST /api/estates` - Create estate (authenticated)
- `PUT /api/estates/:id` - Update estate (authenticated)
- `DELETE /api/estates/:id` - Delete estate (authenticated)
- `GET /api/reviews` - Get reviews
- `POST /api/reviews` - Create review (authenticated)
- `GET /api/services` - Get services
- `POST /api/ai/consultation` - AI chat consultation

## Models

- User (with roles: client, employee, admin)
- Estate
- Service & ServiceCategory
- Sale
- Review

## Authentication

Uses Passport.js with:
- Local strategy (email/password)
- Google OAuth 2.0 strategy

## AI Features

- Google Vision AI for estate photo analysis
- OpenAI GPT for generating descriptions and consultations


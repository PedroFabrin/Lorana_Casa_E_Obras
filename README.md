# Lorana Casa & Obras — API

REST API for **Lorana Casa & Obras**, an e-commerce platform for a Brazilian construction materials store. Built as my final project (TCC) for the Information Systems degree at Toledo Prudente Centro Universitário.

🔗 **Live demo:** https://lorana-web.fly.dev
🖥️ **Frontend:** [Lorana_Casa_E_Obras_Gui](https://github.com/PedroFabrin/Lorana_Casa_E_Obras_Gui)

## Features

- **Authentication** — JWT access tokens with token revocation on logout and bcrypt password hashing
- **Catalog** — products, categories, sections and product images, with pagination and filters
- **Cart & orders** — full cart flow, checkout and order tracking
- **Payments** — pluggable payment gateways: InfinitePay, Mercado Pago and a mock gateway for development
- **Customer data** — user profiles and delivery addresses
- **Admin** — dashboard metrics and sales reports
- **Database migrations** — versioned schema with Alembic, plus a catalog seed script

## Tech stack

| Layer | Technology |
|---|---|
| Framework | FastAPI, Uvicorn |
| Database | MariaDB, SQLAlchemy, Alembic |
| Validation | Pydantic |
| Security | python-jose (JWT), bcrypt |
| Payments | InfinitePay, Mercado Pago SDK |
| Infrastructure | Docker, Docker Compose, Fly.io |

## Architecture

The code follows a layered architecture, keeping HTTP handling, business rules and persistence separate:

```
app/
├── main.py            # FastAPI app entrypoint
├── api/routes.py      # Registers all routers
├── controller/        # HTTP layer: routes and request handling
├── service/           # Business rules
│   └── paymentService/
│       └── gateways/  # base.py + InfinitePay, Mercado Pago and mock implementations
├── model/             # SQLAlchemy models
├── schema/            # Pydantic request/response schemas
└── utils/             # JWT, auth, security and email helpers
migration/             # Alembic migrations
scripts/               # Catalog seed script
```

### Payment gateways

Payments use the **strategy pattern**: every provider implements the same abstract interface (`gateways/base.py`), so the store can switch between InfinitePay, Mercado Pago or the mock gateway without touching the order logic. Adding a new provider means adding one new class.

## Getting started

**Requirements:** Docker and Docker Compose.

1. Clone the repository and create a `.env` file in the project root with your database credentials, JWT secret and payment gateway keys.
2. Start the containers:

```bash
docker compose up --build
```

3. Apply the database migrations inside the API container:

```bash
docker exec -it lorana_api alembic upgrade head
```

4. Open the interactive API docs at **http://localhost:8000/docs**.

## Deployment

The API and the MariaDB database run as separate apps on **Fly.io** (`fly.toml` and `fly-db/`).

## Author

**Pedro Fabrin** — Backend Developer (Python, FastAPI, AI/LLMs)
[LinkedIn](https://www.linkedin.com/in/pedro-henrique-parizoto-fabrin-08765325b) · [GitHub](https://github.com/PedroFabrin)

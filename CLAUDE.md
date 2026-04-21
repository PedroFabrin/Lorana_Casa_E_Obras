# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack

- **FastAPI** — web framework, entrypoint at `app/main.py`
- **SQLAlchemy** — ORM (classic `Column` style, not `Mapped`)
- **Alembic** — database migrations, config at `alembic.ini`, scripts in `migration/`
- **MariaDB** — via `pymysql` driver (`mysql+pymysql://`)
- **Docker Compose** — two services: `api` (FastAPI) and `db` (MariaDB)

## Commands

All commands run inside the API container:

```bash
docker exec -it lorana_api bash
```

| Action | Command |
|---|---|
| Start containers | `docker compose up -d --build` |
| Stop containers | `docker compose down` |
| View API logs | `docker compose logs api` |
| Create migration | `alembic revision --autogenerate -m "description"` |
| Apply migrations | `alembic upgrade head` |
| Rollback migration | `alembic downgrade -1` |

## Architecture

```
app/
├── main.py               # FastAPI app instance, registers router
├── api/routes.py         # Single APIRouter, all routes registered here
├── controller/           # Route handlers (one subpackage per entity)
├── service/              # Business logic (one subpackage per entity)
├── schema/               # Pydantic schemas for request/response
└── model/                # SQLAlchemy models (one subpackage per entity)
    ├── base.py           # DeclarativeBase — all models inherit from here
    └── userModel/
        └── user_model.py
```

## Model conventions

- Each model lives in its own subfolder: `app/model/<entityName>Model/<entity>_model.py`
- Always inherit from `Base` in `app/model/base.py`
- Use `Column` assignment syntax (not `Mapped` annotations)
- Use `sqlalchemy.dialects.mysql.BIGINT` for unsigned integers — the generic `BIGINT` does not accept `unsigned=True`
- Primary key: `BIGINT(unsigned=True)`, `autoincrement=True`, `index=True`

Example:

```python
from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import BIGINT
from app.model.base import Base

class ExampleModel(Base):
    __tablename__ = "example"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(255), index=True, nullable=False)
```

## Registering a new model for migrations

After creating a new model, import it in `migration/env.py` so Alembic detects it:

```python
from app.model.userModel.user_model import UserModel
from app.model.newModel.new_model import NewModel  # add here
```

## Environment

- `DATABASE_URL` inside the container must use `db` as the host (Docker service name), not `127.0.0.1`
- `127.0.0.1:3306` is only for external tools like HeidiSQL connecting from outside Docker

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

---

## Architecture

```
app/
├── main.py                          # FastAPI app instance, registers router
├── database.py                      # SQLAlchemy engine, SessionLocal, get_db
├── api/routes.py                    # Registers all controller routers
├── utils/security.py                # hash_password, verify_password
├── schema/
│   ├── pagination.py                # PaginationParams base (reused by all filters)
│   └── <entity>Schema/
│       └── <entity>_schema.py
├── controller/<entity>Controller/
│   └── <entity>_controller.py
├── service/<entity>Service/
│   └── <entity>_service.py
└── model/
    ├── base.py                      # DeclarativeBase
    ├── __init__.py                  # Imports all models (required for Alembic)
    └── <entity>Model/
        └── <entity>_model.py
```

---

## Model conventions

- Each model lives in `app/model/<entityName>Model/<entity>_model.py`
- Always inherit from `Base` in `app/model/base.py`
- Use `Column` assignment syntax (not `Mapped` annotations)
- Use `sqlalchemy.dialects.mysql.BIGINT` for unsigned integers
- Every model must have `created_at`, `updated_at`, `deleted_at`
- Deletion is always **soft delete** — set `deleted_at = datetime.now()`, never `db.delete()`
- All queries must filter `deleted_at == None` to exclude soft-deleted records

```python
from sqlalchemy import Column, VARCHAR, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql import func
from app.model.base import Base

class ExampleModel(Base):
    __tablename__ = "example"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
```

After creating a new model, import it in `app/model/__init__.py` and `migration/env.py`.

---

## Schema conventions

- Each entity has its own subfolder: `app/schema/<entity>Schema/<entity>_schema.py`
- Standard schemas per entity: `Create`, `Update`, `Filter`, `Response`, `ListResponse`
- `Update` always includes `<entity>_id: int` in the body (no ID in the URL)
- `Filter` always inherits from `PaginationParams` (`app/schema/pagination.py`)
- `Response` must have `model_config = {"from_attributes": True}`
- `ListResponse` wraps the paginated result with `total`, `page`, `page_size`, `data`

```python
from app.schema.pagination import PaginationParams

class ExampleFilter(PaginationParams):
    name: Optional[str] = None

class ExampleUpdate(BaseModel):
    example_id: int
    name: Optional[str] = None

class ExampleResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

class ExampleListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[ExampleResponse]
```

---

## Service conventions

- Each entity has its own subfolder: `app/service/<entity>Service/<entity>_service.py`
- All functions return a tuple `(result, error)`
  - Success: `({"status": "success", "data": schema.model_dump()}, None)`
  - Error: `(None, "error message string")`
- All logic and error handling lives in the service — the controller only handles the response
- Build the schema object explicitly before calling `.model_dump()`
- List functions return `EntityListResponse` with pagination
- Passwords must always be hashed via `app/utils/security.hash_password` before saving

```python
def create_example(db: Session, data: ExampleCreate):
    try:
        # validations
        result = ExampleResponse.model_validate(entity)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)
```

---

## Controller conventions

- Each entity has its own subfolder: `app/controller/<entity>Controller/<entity>_controller.py`
- The controller only calls the service and returns `JSONResponse` — no logic
- All endpoints return JSON with `{"status": "success", ...}` or `{"status": "error", "message": "..."}`
- Register the router in `app/api/routes.py`

```python
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_example(data: ExampleCreate, db: Session = Depends(get_db)):
    result, error = example_service.create_example(db, data)
    if error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status": "error", "message": error})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
```

Standard routes per entity:

| Method | Route | Body |
|---|---|---|
| `POST` | `/<entity>/create` | `EntityCreate` |
| `POST` | `/<entity>/list` | `EntityFilter` (with pagination) |
| `PUT` | `/<entity>/update` | `EntityUpdate` (with `entity_id`) |
| `DELETE` | `/<entity>/delete/{id}` | — |

---

## Environment

- `DATABASE_URL` inside the container must use `db` as host (Docker service name)
- `127.0.0.1:3306` is only for external tools like HeidiSQL
- Timezone is set to `America/Sao_Paulo` in both containers

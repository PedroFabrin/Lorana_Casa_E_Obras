# Lorana Casa e Obras

## Docker

### Subir os containers
```bash
docker compose up --build
```

### Subir em background
```bash
docker compose up -d --build
```

### Parar os containers
```bash
docker compose down
```

### Parar e remover volumes (apaga os dados do banco)
```bash
docker compose down -v
```

### Ver containers rodando
```bash
docker ps
```

### Acessar o terminal do container da API
```bash
docker exec -it lorana_api bash
```

### Ver logs da API
```bash
docker compose logs api
```

### Ver logs do banco
```bash
docker compose logs db
```

---

## Alembic

### Inicializar o Alembic (apenas na primeira vez)
```bash
alembic init migration
```

### Criar uma nova migration
```bash
alembic revision --autogenerate -m "descricao da migration"
```

### Aplicar todas as migrations pendentes
```bash
alembic upgrade head
```

### Reverter a última migration
```bash
alembic downgrade -1
```

### Reverter todas as migrations
```bash
alembic downgrade base
```

### Ver o histórico de migrations
```bash
alembic history
```

### Ver a migration atual aplicada
```bash
alembic current
```

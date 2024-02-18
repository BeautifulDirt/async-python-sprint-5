Поднять контейнер **Redis** командой:

`docker run --rm  --name redis-fastapi -p 6379:6379 -d redis`

Поднять контейнер **Postgres** командой:

`docker run --rm  --name postgres-fastapi -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=collection -d postgres:14.5`

Сгенерировать **SECRET_KEY** командой:

`openssl rand -hex 32`
# Microservices with Redis and PostgreSQL

## Services

- **Backend**: Publishes user updates to a Redis topic.
- **Pubsub**: Reads updates, stores them in PostgreSQL, and republishes for real-time updates.
- **Dashboard**: Serves WebSocket connections for real-time updates.

## Running the project

1. Build and start the services:
   ```bash
   docker-compose up --build

## News example
```json
{
  "action": "UPDATE",
  "data": {"title": "Awesome title", "news": "Attention! Breaking news!"}
}
```


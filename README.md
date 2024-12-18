# Microservices with Redis and PostgreSQL

## Technology stack
[![Stack](https://skillicons.dev/icons?i=python,fastapi,redis,postgres,js,html,css,docker)](https://skillicons.dev)

## Services

- **Backend**: Publishes user updates to a Redis topic.
- **Pubsub**: Reads updates, stores them in PostgreSQL, and republishes for real-time updates.
- **Dashboard**: Serves WebSocket connections for real-time updates.

## Running the project

1. Build and start the services:
   ```bash
   docker-compose up --build

## News example
* `"action": "UPDATE"` is a message that triggers Database update
* `"data: {}` is the data that needs to be loaded to the database
* Sample:
   ```json
   {
     "action": "UPDATE",
     "data": {"title": "Awesome title", "news": "Attention! Breaking news!"}
   }
   ```

## If you want to monitor subscriptions for debugging
* Connect to the redis container and open redis-cli
```commandline
docker exec -it redis redis-cli
```
* Subscribe to the topic
```commandline
SUBSCRIBE news-updates
```

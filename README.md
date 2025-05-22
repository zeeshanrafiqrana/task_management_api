# Async Task Management API

A FastAPI application that manages tasks with background processing capabilities.

## Features

- Create, list, update, and delete tasks
- Background processing for long-running tasks
- Task status notifications
- Async SQLAlchemy for database operations
- Alembic for database migrations
- Comprehensive test suite

## Tech Stack

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Docker
- Poetry

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Poetry (optional for local development)

### Running with Docker

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/zeeshanrafiqrana/task_management_api.git
   cd task_management_api
   \`\`\`

2. Create a `.env` file with the following content:
   \`\`\`
   POSTGRES_SERVER=db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=taskdb
   \`\`\`

3. Start the application with Docker Compose:
   \`\`\`bash
   docker-compose up -d
   \`\`\`

4. The API will be available at http://localhost:8000

### Local Development

1. Install dependencies:
   \`\`\`bash
   poetry install
   \`\`\`

2. Set up the database:
   \`\`\`bash
   # Start PostgreSQL (if not using Docker)
   # Configure your .env file with database credentials
   
   # Run migrations
   poetry run alembic upgrade head
   \`\`\`

3. Run the application:
   \`\`\`bash
   poetry run uvicorn app.main:app --reload
   \`\`\`

4. Run tests:
   \`\`\`bash
   poetry run pytest
   \`\`\`

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks` - List all tasks (with filtering and pagination)
- `GET /api/v1/tasks/{task_id}` - Get task details
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `POST /api/v1/tasks/{task_id}/process` - Start background processing

## Monitoring

In a production environment, this application could be monitored using:

1. **Application Performance Monitoring (APM)**:
   - Datadog, New Relic, or Elastic APM to track request performance, errors, and dependencies

2. **Logging**:
   - ELK Stack (Elasticsearch, Logstash, Kibana) or Graylog for centralized logging
   - Structured logging with correlation IDs for tracing requests

3. **Metrics**:
   - Prometheus for collecting metrics
   - Grafana for visualization
   - Key metrics to monitor:
     - Request rate, latency, and error rate
     - Background task processing time and failure rate
     - Database connection pool usage
     - Memory and CPU usage

4. **Alerting**:
   - Set up alerts for critical errors, high latency, or failed background tasks
   - PagerDuty or OpsGenie for on-call notifications

5. **Health Checks**:
   - Regular health checks to ensure the API and database are responsive
   - Kubernetes liveness and readiness probes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

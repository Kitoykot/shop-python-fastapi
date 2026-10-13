
# Project Instructions

## General

- Always communicate with the developer in Russian.
- Keep technical terms, variable names, class names, and identifiers in English.
- Write all code in English, except custom exception messages.
- Write custom exception messages in Russian.
- Do not add comments in code. Do not remove existing comments unless relevant to the task.
- Follow existing project conventions.
- Prefer simple, readable, and maintainable solutions.
- Do not introduce unnecessary abstractions.

## Technology Stack

- Python 3.14 (Dockerfile and Ruff target version)
- FastAPI with synchronous endpoint handlers and dependencies
- Pydantic v2
- SQLAlchemy 2.0 with synchronous Session
- PostgreSQL (psycopg v3)
- Alembic
- Redis + RQ (background jobs)
- APScheduler
- Ruff (linting and formatting)

Use modern syntax and recommended practices for the installed versions.

Do not introduce new libraries or frameworks without approval.

## Architecture Guidelines

Follow the current architecture:

Router/Controller -> Service -> Repository

Router and Controller responsibilities are combined in endpoint functions in
`app/http/controllers/api/v1/`. The shared `router.py` assembles resource routers.
Do not introduce a separate Controller layer or migrate to async as part of unrelated tasks.

### Router/Controller

- Define HTTP endpoints and HTTP methods.
- Handle request validation using Pydantic schemas.
- Handle FastAPI dependency injection.
- Call Services and convert their results into HTTP response schemas.
- Convert request schemas into internal DTOs using the existing create_dto() or to_dto() methods.
- Return HTTP responses.
- Do not contain business logic.
- Do not access Repositories directly.
- Do not execute database queries.
- Do not import SQLAlchemy ORM models.

### Dependencies

- Use `app/dependencies/` to assemble Services, Repositories, UnitOfWork, and external clients.
- Manage database session lifetime through get_db().
- Keep authentication and role checks in the existing auth dependencies.
- Dependency factories may import Repositories for construction; endpoint functions must not access them directly.

### Service

- Implement business logic and application workflows.
- Coordinate Repositories and external integrations.
- Use DTOs for communication with Repositories.
- Remain independent of FastAPI and HTTP concepts.
- Never import or access SQLAlchemy ORM models.
- Do not execute SQLAlchemy queries directly.
- Raise domain-specific exceptions for expected business errors.
- Keep new business workflows in Services and preserve existing Repository and DTO contracts.

### Repository

- Handle PostgreSQL access using synchronous SQLAlchemy 2.0.
- SessionRepository handles Redis-backed sessions using the synchronous Redis client.
- Implement queries, filtering, inserts, updates, and deletes.
- Use SQLAlchemy ORM models internally.
- Never expose ORM models outside the Repository layer.
- Convert ORM models into DTOs before returning results.
- Accept DTOs or explicitly defined primitive parameters.
- Return DTOs, collections of DTOs, or None when appropriate.
- Do not depend on FastAPI or HTTP response schemas.
- Keep new application workflows in Services. Preserve existing query policies and helpers unless the task changes them.
- Existing conventions include Product.active(), Product.is_available, expired-order selection, and token generation and expiration in SessionRepository.
- Do not raise FastAPI HTTPException.

## ORM Isolation Rules

Runtime access to application data through SQLAlchemy ORM belongs in Repositories.
Model definitions, migration metadata, and integration test setup are exceptions.

- Only Repositories may import and use ORM models for runtime application data access.
- Services must never receive ORM instances.
- Controllers and Routers must never receive ORM instances.
- Public Repository methods must never return ORM instances. Private helpers may use and return ORM instances within the Repository.
- ORM instances must never be passed between application layers.
- Repositories must convert ORM instances into DTOs.
- DTOs must not expose SQLAlchemy-specific implementation details.
- ORM model definitions may reside in a dedicated models package for SQLAlchemy and Alembic.
- Alembic configuration may import ORM models for migration metadata.
- Integration tests and fixtures may import ORM models to prepare and inspect database state.

## DTO Guidelines

Use standard dataclasses for internal DTOs in `app/dto/` and Pydantic v2 for
HTTP request and response schemas in `app/http/requests/` and `app/http/responses/`.

- Use DTOs to exchange data between application layers.
- Keep internal DTOs independent of SQLAlchemy and FastAPI.
- Use explicit field types.
- Convert ORM objects into dataclass DTOs explicitly inside Repositories, following existing __to_dto() helpers.
- Use model_validate(..., from_attributes=True) to convert DTOs into HTTP response schemas.
- Keep internal DTOs separate from HTTP request and response schemas.
- Preserve the UpdateProductDto.fields contract for partial updates and use model_dump(exclude_unset=True) in its request converter.
- Match DTO field types to the data they carry, including nullable values.
- Do not migrate internal DTOs to Pydantic without an explicit task to do so.
- Do not return ORM models from Services, Controllers, or Repositories.

## Database Guidelines

- Use SQLAlchemy 2.0-style syntax.
- Use select(), insert(), update(), and delete().
- Use Session, create_engine, and sessionmaker as configured in config/postgresql/connection.py.
- Use the postgresql+psycopg dialect.
- Keep request workflows synchronous while they use synchronous database and Redis clients.
- Keep database queries inside Repositories.
- Use parameterized queries.
- Avoid unnecessary database queries and N+1 problems.
- Use transactions when multiple operations must be atomic.
- Follow the existing transaction boundary of the workflow being modified.
- Standalone writes in UserRepository, ProductRepository, CategoryRepository, and CartRepository currently commit inside the Repository.
- Order and payment workflows use with self.unit_of_work in Services to commit or roll back related writes together.
- Methods named *_during_transaction must not commit; use flush() when generated values are needed before commit.
- Do not call Repository methods that commit inside a UnitOfWork workflow. Add a transaction-compatible operation when needed.
- Do not globally change transaction management as part of an unrelated task.
- Do not change database schemas without Alembic migrations.
- Do not modify existing migrations without explicit approval.

## Error Handling

- Use the existing AppException base class for custom application exceptions.
- All custom application exceptions must inherit from AppException.
- Define exception attributes following the existing conventions:
  - `code`: HTTP status code as an integer.
  - `message`: human-readable error message in Russian, static on the class or dynamic on the instance.
- For static messages, define code and message as class attributes without overriding __init__.
- Dynamic messages may use __init__, following ItemCountException and ItemIsNotAvailableException: keep code on the class, set self.message in Russian, and call super().__init__(self.message).
- Keep exception class names in English.
- Follow the existing exception naming conventions.
- Raise existing domain exceptions for expected business errors.
- When handling expected database conflicts, catch specific errors and preserve the original cause. Do not add broad database-error wrappers to unrelated code.
- Do not add unnecessary try/except blocks.
- Do not silently suppress exceptions.
- Do not catch broad Exception unless there is a justified reason.
- Let FastAPI and Pydantic handle standard request validation errors.
- Raise custom application exceptions for expected business errors.
- Never raise HTTPException inside Services or Repositories.
- Convert AppException instances into HTTP responses using the existing exception handling mechanism.
- Do not expose internal exception details to API clients.
- Preserve useful error information for debugging and logging.

## Background Jobs

- Use RQ for background job processing.
- Keep background job functions independent of HTTP concepts.
- Reuse Services for business logic when appropriate.
- Do not pass ORM instances or active database sessions to background jobs.
- Pass serializable identifiers or dataclass DTOs, following notify_order_paid(order: OrderDataDto).
- Create and manage database sessions within job execution when needed.
- Keep RQ job functions synchronous.
- Use the standalone BlockingScheduler command in app/commands/scheduler.py for scheduled task execution.
- Avoid duplicating scheduled jobs across multiple application workers.

## Working Rules

- Read relevant files before making changes.
- Inspect related application layers when modifying behavior.
- Follow the existing architecture strictly.
- Do not modify unrelated code.
- Do not add dependencies without permission.
- Do not change project architecture without approval.
- Do not introduce unnecessary abstractions.
- Do not overwrite existing implementations without inspecting them.
- Explain important technical decisions.
- Ask for clarification when requirements are unclear.
- Do not use placeholders in generated code.
- Never output incomplete code such as:
  - "# ... existing code ..."
  - "# TODO: implement"
- Provide complete code or precise, applicable diffs.
- Prefer minimal, focused changes.

## Code Quality

- Follow existing coding conventions.
- Use explicit type hints for function parameters and return values.
- Use modern Python typing syntax.
- Follow Pydantic v2 conventions for HTTP schemas and dataclass conventions for internal DTOs.
- Use the repository's ruff.toml settings, including single quotes and Python 3.14 syntax.
- Keep functions and classes focused.
- Avoid duplicated logic.
- Prefer composition over unnecessary inheritance.
- Use meaningful names for variables, functions, and classes.
- Avoid premature optimization.
- Do not add unnecessary defensive checks.
- Ensure generated code follows Ruff rules.

## Verification

- Run Ruff checks on modified Python files.
- Run Ruff formatting checks when appropriate.
- Run relevant tests when available.
- Unit tests in tests/unit use mocks; integration tests in tests/integration require the dedicated PostgreSQL and Redis test services.
- Check integration test configuration before running: Redis fixtures use flushdb(). Never point them at application data.
- Do not claim tests passed unless they were executed.
- Report checks that could not be performed.
- Review changes for architectural violations.
- Ensure ORM models never escape the Repository layer.
- Summarize changes after completing a task.

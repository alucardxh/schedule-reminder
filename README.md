### Key Features
- **Asynchronous & Efficient:** Built on top of `asyncio` and `AsyncIOScheduler` for non-blocking I/O operations.
- **Dynamic Data Loading:** Reloads event configurations (`events.json`) on each trigger without requiring a service restart.
- **Secure Configuration:** Environment-variable-driven setup for sensitive Telegram credentials using `python-dotenv`.
- **Docker-Ready & Self-Hostable:** Easily containerized and deployed with a clean multi-stage or single-stage Docker architecture.

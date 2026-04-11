# 📦 RAG System Project Structure

```text
rag-system/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── query.py        # Handles user query requests
│   │           ├── ingestion.py    # Handles document ingestion APIs
│   │           └── health.py       # Health check endpoint
│   │
│   ├── core/
│   │   ├── config.py              # App configuration (env, settings)
│   │   ├── logging.py             # Logging setup
│   │   └── security.py            # Auth, validation, security utils
│   │
│   ├── services/
│   │   ├── rag/                   # RAG pipeline (retrieval + generation)
│   │   ├── ingestion/             # Data ingestion pipeline
│   │   ├── memory/                # Session + conversation memory
│   │   ├── llm/                   # LLM providers (Ollama, OpenAI, etc.)
│   │   └── tools/                 # External tools (search, APIs)
│   │
│   ├── repositories/              # Data access layer (DB, vector store)
│   ├── models/                    # Pydantic schemas / domain models
│   ├── workers/                   # Background jobs (async tasks)
│   ├── utils/                     # Shared utilities/helpers
│   └── main.py                    # FastAPI entrypoint
│
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── e2e/                       # End-to-end tests
│
├── scripts/
│   ├── ingest_data.py             # CLI for ingestion
│   └── rebuild_index.py           # Rebuild vector index
│
├── docker/
│   ├── Dockerfile                 # Container definition
│   └── docker-compose.yml         # Multi-service setup
│
├── pyproject.toml                 # Project config & dependencies (uv)
├── uv.lock                        # Locked dependency versions
├── .env                           # Environment variables
├── .python-version                # Python version (optional)
└── README.md                      # Project documentation
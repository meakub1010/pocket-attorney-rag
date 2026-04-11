pocket-attorney-rag/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── query.py
│   │           ├── ingestion.py
│   │           └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── services/
│   │   ├── rag/
│   │   ├── ingestion/
│   │   ├── memory/
│   │   ├── llm/
│   │   └── tools/
│   │
│   ├── repositories/
│   ├── models/
│   ├── workers/
│   ├── utils/
│   └── main.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── ingest_data.py
│   └── rebuild_index.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── pyproject.toml      🔥 (replaces requirements.txt)
├── uv.lock             🔥 (auto-generated lockfile)
├── .env
├── .python-version     🔥 (optional, for Python version)
└── README.md
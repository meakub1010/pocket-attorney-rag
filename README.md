# 📦 RAG System Project Structure

```text
pocket-attorney-rag/
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



- POSTGRES PgAdmin login
conntect to server
any name
host: db
password:admin
port: 5432

- Sample user
{
  "first_name": "Ishmael",
  "last_name": "Muhammad",
  "email": "ishmael@example.com",
  "password": "User@1234"
}



## sample questions and expected answer as per chat GPT

1. Equality Before Law

Question:
What does the constitution say about equality before law?

Expected Answer:
According to Article 27, all citizens are equal before law and are entitled to equal protection of law.
Actual Answer:
Article 27 states that all citizens are equal before law and are entitled to equal protection of law.

2. Non-Discrimination

Question:
Can the State discriminate based on religion or race?

Expected Answer:
Article 28(1) states that the State shall not discriminate against any citizen on grounds only of religion, race, caste, sex or place of birth.
Actual Answer:
According to Article 28(1), no, the State cannot discriminate against any citizen on grounds only of religion or race.


3. Equal Rights for Women

Question:
Do women have equal rights with men?

Expected Answer:
According to Article 28(2), women shall have equal rights with men in all spheres of the State and public life.
Actual Answer: 
Yes. According to Article 28(2), women have equal rights with men in all spheres of the State and public life.



4. Equality of Opportunity

Question:
What is equality of opportunity?

Expected Answer:
According to Article 29, all citizens shall have equal opportunity in respect of employment or office in the service of the Republic.
Actual Answer:
According to Article 29, equality of opportunity means that all citizens should have equal opportunities in terms of employment or holding an office in the service of the Republic.

5. Right to Life

Question:
What does the constitution say about the right to life?

Expected Answer:
Article 32 states that no person shall be deprived of life or personal liberty except in accordance with law.
Actual Answer:
According to Article 32 of the constitution, every person has the right to life, and this right is not taken away except according to law.


6. Arrest Rights

Question:
Does a person have the right to know the reason for arrest?

Expected Answer:
According to Article 33, no person shall be detained in custody without being informed of the grounds for such arrest.
Actual Answer:
According to Article 33 - Safeguards as to arrest, a person has the right to know the reason for their arrest. The article states: \"No person shall be detained in custody without being informed of the grounds for such arrest.\" This means that before an individual is arrested and held in custody, they have the right to know why they are being arrested.

7. Forced Labour

Question:
Is forced labour allowed?

Expected Answer:
Article 34 states that all forms of forced labour are prohibited.
Actual Answer:
No, forced labour is not allowed. According to Article 34, all forms of forced labour are prohibited.

8. Freedom of Movement

Question:
Can citizens move freely throughout Bangladesh?

Expected Answer:
According to Article 36, every citizen has the right to move freely throughout Bangladesh, subject to reasonable restrictions.
Actual Answer:
Yes, citizens can move freely throughout Bangladesh subject to reasonable restrictions.

9. Freedom of Speech

Question:
Does the constitution guarantee freedom of speech?

Expected Answer:
Article 39 guarantees freedom of thought and conscience, as well as freedom of speech and expression.
Actual Answer:
Yes, the constitution guarantees freedom of speech as part of \"Freedom of thought and expression\" (Article 39).

10. Freedom of Religion

Question:
Do citizens have the right to practice religion?

Expected Answer:
According to Article 41, every citizen has the right to profess, practice or propagate any religion.
Actual Answer:
Yes, citizens have the right to practice their religion.\n\nAccording to Article 41, every citizen has the right to \"practice\" any religion.


11. Right to Property

Question:
What rights do citizens have regarding property?

Expected Answer:
Article 42 states that every citizen has the right to acquire, hold, transfer or otherwise dispose of property.
Actual Answer:
According to Article 42, citizens have the right to acquire, hold, transfer, or otherwise dispose of property. In simpler terms, they have the right to own and manage their property as they see fit.

12. Protection of Home

Question:
Does the constitution protect a citizen’s home from unlawful search?

Expected Answer:
According to Article 43, every citizen has the right to be secure in his home against entry, search and seizure.
Actual Answer:
Yes, according to Article 43 of the Constitution, a citizen's home is protected against entry by any person, including law enforcement. This means that the government or its agents do not have automatic permission to enter and search an individual's home without a valid reason, warrant, or other legal authority.

13. Freedom of Profession

Question:
Can citizens choose any profession?

Expected Answer:
Article 40 states that every citizen has the right to enter upon any lawful profession or occupation.
Actual Answer:
Yes, citizens can choose any lawful profession. According to Article 40, every citizen has the right to enter upon any lawful profession or occupation. This means that as long as the chosen profession is legal and not against the law, citizens have the freedom to pursue it.


14. Enforcement of Fundamental Rights

Question:
Can citizens go to court to enforce fundamental rights?

Expected Answer:
According to Article 44, the right to move the High Court Division for enforcement of fundamental rights is guaranteed.
Actual Answer:
Yes, citizens can go to court to enforce their fundamental rights. According to Article 44, it is guaranteed that citizens have the right to move the High Court Division for enforcement of fundamental rights.



15. Invalid Laws

Question:
What happens if a law conflicts with fundamental rights?

Expected Answer:
Article 26 states that laws inconsistent with fundamental rights shall become void to the extent of such inconsistency.
Actual Answer:
If a law conflicts with fundamental rights, it becomes void to the extent of such inconsistency, as stated in Article 26.

## Claude Evaluation on above questions/amswers

![img.png](img.png)
![img.png](app/data/img.png)
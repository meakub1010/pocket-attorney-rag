
def build_legal_prompt(question: str, docs: list[dict]) -> str:
    context_blocks = []

    for d in docs:
        block = f"""
{d['article']} - {d['title']}
Category: {d['category']}

{d['answer']}
"""
        context_blocks.append(block.strip())

    context = "\n\n---\n\n".join(context_blocks)

    # return f"""
    # Context:
    # {context}
    #
    # Question:
    # {question}
    # """

    return f"""
You are a legal assistant.

Answer the question strictly based on the provided context.

Context:
{context}

Question:
{question}

Rules:
- Cite article numbers (e.g., Article 28(2))
- Do not add information not in context
- If not found, say "Not found in provided context"
- Make sure you elaborate the answer to make it more readable
"""
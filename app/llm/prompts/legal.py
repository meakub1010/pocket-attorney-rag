def build_legal_prompt(question: str, docs: list[dict]) -> str:
    context_blocks = []

    for d in docs:
        block = f"""
{d["article"]} - {d["title"]}
Category: {d["category"]}

{d["answer"]}
"""
        context_blocks.append(block.strip())

    context = "\n\n---\n\n".join(context_blocks)

    STANDARD_PROMPT = """
You are a legal assistant.

Answer the question strictly based on the provided context.

Context:
{context}

Question:
{question}

Rules:

- Cite article numbers when available (e.g., Article 28(2)).
- Use simple and easy-to-understand language.
- You may briefly paraphrase or explain the meaning of the text for clarity.
- Keep the explanation grounded in the provided context only.
- Do not introduce external legal knowledge or interpretation.
- Do not speculate or infer beyond the provided text.
- Keep answers concise unless the question asks for detail.
- If the answer cannot reasonably be derived from the context, respond ONLY with:
  "Not found in provided context."
"""
    STRICT_PROMPT = """
    You are a legal assistant.

    Answer the question strictly based on the provided context.

    Context:
    {context}

    Question:
    {question}

    Rules:

    - Use ONLY statements explicitly present in the context.
    - You may rephrase ONLY if meaning is unchanged.
    - Do NOT add explanations or interpretations.
    - Do NOT expand meaning.
    - If not found: "Not found in provided context."
    """

    EXPLAINED_PROMPT = """
    You are a legal assistant.

    Answer the question using only the provided context.
    You may explain the meaning in simple language.

    Context:
    {context}

    Question:
    {question}

    Rules:
    - Stay strictly grounded in context.
    - You may paraphrase for clarity.
    - Do not introduce external legal knowledge.
    - Do not speculate beyond the context.
    - Keep answers simple and concise.
    """

    HYBRID_PROMPT = """
    You are a legal assistant.

    Provide two parts:

    1. Legal statement from the context (quote or near-quote)
    2. Simple explanation in one line

    Context:
    {context}

    Question:
    {question}

    Rules:
    - Use only provided context.
    - Do not add external knowledge.
    - Keep output concise.
    """

    q = question.lower()

    if any(x in q for x in ["exact article", "quote", "what does the law say", "define"]):
        print("STRICT_PROMPT")
        return STRICT_PROMPT.format(
        question=question,
        context=context, )

    if any(x in q for x in [
        "can i", "does it allow", "is it legal", "what does it mean"
    ]):
        print("EXPLAINED_PROMPT")
        return EXPLAINED_PROMPT.format(
        question=question,
        context=context, )

    return HYBRID_PROMPT.format(
        question=question,
        context=context, )
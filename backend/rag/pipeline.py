from rag import init_rag as rag_state
from config import SYSTEM_PROMPT, TOP_K, SIMILARITY_THRESHOLD

def retrieve_chunks(question: str, top_k: int = TOP_K):
    return rag_state.collection.query(query_texts=[question], n_results=top_k)

def format_retrieved_context(results):
    ids, docs, metas, distances = results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]
    return [
        {
            "id": doc_id,
            "text": doc,
            "section_number": meta["section_number"],
            "section_title":  meta["section_title"],
            "page_number":    meta["page_number"],
            "source":         meta.get("source", ""),
            "distance":       distance,
        }
        for doc_id, doc, meta, distance in zip(ids, docs, metas, distances)
    ]

def should_refuse_answer(chunks, threshold=SIMILARITY_THRESHOLD):
    return not chunks or chunks[0]["distance"] > threshold

def build_context_for_llm(chunks):
    return "\n\n".join(
        f"[SOURCE {i+1}]\nDocument: {c['source']}\nSection: {c['section_number']} - {c['section_title']}\nPage: {c['page_number']}\n\n{c['text']}"
        for i, c in enumerate(chunks)
    )

def generate_grounded_answer(question, chunks):
    context = build_context_for_llm(chunks)
    user_prompt = f"Question:\n{question}\n\nContext:\n{context}"
    response = response = rag_state.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content

def extract_used_sections(answer: str, chunks: list) -> list:
    return [
        c for c in chunks
        if c["section_number"] in answer
    ]

def ask_hr_policy(question: str, top_k: int = TOP_K, threshold: float = SIMILARITY_THRESHOLD):
    raw_chunks = retrieve_chunks(question, top_k)
    chunks = format_retrieved_context(raw_chunks)
    if should_refuse_answer(chunks, threshold):
        return {"question": question, "answer": "Je n'ai pas trouvé cette information dans le document de politique RH actuel.", "sources": [], "retrieved_chunks": chunks}
    answer = generate_grounded_answer(question, chunks)
    used_chunks = extract_used_sections(answer, chunks)
    sources = [
        {"section_number": c["section_number"], "section_title": c["section_title"], "page_number": c["page_number"]}
        for c in used_chunks
    ]
    return {"question": question, "answer": answer, "sources": sources, "retrieved_chunks": chunks}
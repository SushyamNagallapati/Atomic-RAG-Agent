# atomic_pipeline.py

from retriever import get_relevant_documents
from llama_model import ask_ollama
from insurance_prompt import INSURANCE_ASSISTANT_PROMPT

# Define keywords and their associated atomic questions
KEYWORD_TO_QUESTIONS = {
    "covid": [
        "Does the policy cover COVID treatment?",
        "Does the policy include hospitalization?",
        "Is March 2023 within the active policy period?"
    ],
    "disability": [
        "Does the policy cover accidental disability?",
        "Are disabilities due to accidents eligible for coverage?",
        "Is there a daily benefit for disability?"
    ],
    "hospital": [
        "Does the policy include hospital stay benefits?",
        "Is emergency hospitalization covered?"
    ],
    "claim": [
        "How do I file a claim under this policy?",
        "Are there any claim deadlines or conditions?"
    ],
    "premium": [
        "What is the premium payment schedule?",
        "Is there a grace period for premium payment?"
    ]
}

def split_into_atomic_questions(user_query: str) -> list:
    user_query_lower = user_query.lower()
    atomic_questions = []
    matched_keywords = []

    for keyword, questions in KEYWORD_TO_QUESTIONS.items():
        if keyword in user_query_lower:
            matched_keywords.append(keyword)
            atomic_questions.extend(questions)

    if not atomic_questions:
        print("⚠️ No keyword match found. Falling back to default.")
        atomic_questions = [user_query]
    else:
        print(f"🔑 Matched Keywords: {matched_keywords}")

    return atomic_questions

def answer_atomic_question(question: str) -> str:
    docs = get_relevant_documents(question)
    print("📄 Retrieved Chunks from Vector DB:")
    for i, doc in enumerate(docs):
        print(f"\n--- Chunk {i+1} ---\n{doc.page_content[:500]}...\n")

    context = "\n\n".join([doc.page_content for doc in docs])

    full_prompt = INSURANCE_ASSISTANT_PROMPT.format(input=f"{question}\n\nContext:\n{context}")
    return ask_ollama(full_prompt)

def assemble_final_answer(answers: list) -> str:
    return "\n".join([f"✔️ {a}" for a in answers])

if __name__ == "__main__":
    user_query = input("Ask your question: ")

    atomic_questions = split_into_atomic_questions(user_query)
    print("\n🔍 Atomic questions:")
    for i, q in enumerate(atomic_questions, 1):
        print(f"{i}. {q}")

    print("\n🤖 Answering...\n")
    answers = [answer_atomic_question(q) for q in atomic_questions]

    final = assemble_final_answer(answers)
    print("\n🧠 Final Combined Answer:\n")
    print(final)

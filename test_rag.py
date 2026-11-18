
from app.rag.rag_service import initialize_rag

rag_chain = initialize_rag("data/mydata.pdf")

while True:
    question = input("Ask a question: ")

    if question.lower() == "exit":
        break

    response = rag_chain({"question": question})

    print("Answer:", response.content)
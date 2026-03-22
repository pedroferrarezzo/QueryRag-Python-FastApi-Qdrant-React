from config.env import GEMINI_API_KEY
from google import genai
from model import Document

def contact_ai(prompt: str, documents: list[Document]):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    context = "\n\n".join([
        doc.metadata.chunk for doc in documents
    ])
    final_prompt = f"""
Responda a pergunta com base no contexto abaixo.

Contexto:
{context}

Pergunta:
{prompt}
"""
    
    # https://github.com/google-gemini/api-examples/blob/856e8a0f566a2810625cecabba6e2ab1fe97e496/python/text_generation.py#L37-L45
    content_response_iterator = client.models.generate_content_stream(
                                    model="gemini-2.5-flash", contents=final_prompt
                                )

    return content_response_iterator
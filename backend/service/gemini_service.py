from typing import AsyncIterator

from config.env import GEMINI_API_KEY
from google import genai
from exceptions.invalid_value_exception import InvalidValueException
from model import Document
from repository.minio_repository import download_file
from google.genai import types
from exceptions import LmmException

client = genai.Client(api_key=GEMINI_API_KEY)

async def contact_ai(prompt: str, documents: list[Document], prompt_raw_bytes: bytes | None, prompt_mime_type: str | None) -> AsyncIterator[types.GenerateContentResponse]:
    """Contata a Gemini API para obter uma resposta baseada no prompt e no contexto do documento, utilizando um modelo multimodal se um arquivo estiver presente."""
    
    if not documents:
        raise InvalidValueException("Os documentos são obrigatórios para contatar a Gemini API.")
    
    if not prompt and not prompt_raw_bytes:
        raise InvalidValueException("O prompt ou os bytes do prompt são obrigatórios para contatar a Gemini API.")
    
    if prompt and (prompt_raw_bytes or prompt_mime_type):
        raise InvalidValueException("O prompt em texto e os bytes do prompt não podem ser utilizados juntos. Escolha um dos dois para contatar a Gemini API.")
    
    if (prompt_raw_bytes and not prompt_mime_type) or (not prompt_raw_bytes and prompt_mime_type):
        raise InvalidValueException("Tanto os bytes do prompt quanto o tipo MIME são necessários para contatar a Gemini API com um arquivo.")

    context = [doc.metadata.chunk for doc in documents if doc.metadata.chunk]
    final_prompt = f"""
Você é o assistente de IA do sistema QueryRag, que tem como finalidade responder perguntas estritamente com base no contexto fornecido.

INSTRUÇÕES:
1. Com base no bloco "DOCUMENTOS", e também dos arquivos em anexo (se houver), identifique quais deles respondem à pergunta do usuário (presente no bloco "PERGUNTA" ou nos arquivos em anexo);
2. Responda a pergunta do usuário exclusivamente com base nos documentos selecionados no passo anterior (não mencione os documentos utilizados para formulação da sua resposta);
3. Se nenhum dos documentos for capaz de responder a pergunta, não a responda, e informe o usuário.

PERGUNTA:
{prompt if prompt else "Presente no arquivo em anexo."}

DOCUMENTOS:
{chr(10).join(context)}
"""
    parts = [types.Part.from_text(text=final_prompt)]    
    if prompt_raw_bytes and prompt_mime_type:
        parts.append(types.Part.from_bytes(data=prompt_raw_bytes, mime_type=prompt_mime_type))

    for document in documents:
        if document.metadata.object_storage_key and document.metadata.type:
            object_file_bytes = await download_file(document.metadata.object_storage_key)
            # Eventualmente pode ser alterado para from_url, caso o objeto seja acessível publicamente via URL, evitando a necessidade de download e reupload do arquivo para a API do Gemini
            parts.append(types.Part.from_bytes(data=object_file_bytes, mime_type=document.metadata.type))

    content = types.Content(
            role="user",
            parts=parts
        )  
    # https://github.com/google-gemini/api-examples/blob/856e8a0f566a2810625cecabba6e2ab1fe97e496/python/text_generation.py#L37-L45
    try:
        # Futuramente podemos utilizar um modelo que seja generativo multimodal
        content_response_iterator = await client.aio.models.generate_content_stream(
                                        model="gemini-2.5-flash", contents=[content]
                                    )

        return content_response_iterator

    except Exception as e:
        raise LmmException(
            "Erro durante a comunicação com a API do Gemini para geração de conteúdo",
            e
        ) from e

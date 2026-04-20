from typing import AsyncIterator

from exceptions import InvalidValueException, LmmException
from model import Document, Metadata, Object
from dto import DocumentDto
from ports import LmmModel

class LmmService:
    """Serviço responsável por orquestrar a interação com modelos de linguagem multimodal de forma agnóstica ao provedor."""

    def __init__(self, repository: LmmModel):
        """Inicializa o serviço com uma instância do repositório de modelos de linguagem multimodal."""
        self._repository = repository

    async def contact_ai(
        self,
        prompt: str,
        document_dtos: list[DocumentDto],
        prompt_raw_bytes: bytes | None,
        prompt_mime_type: str | None
    ) -> AsyncIterator:
        """Orquestra a preparação do contexto e delega a geração de conteúdo a um provedor de LLM multimodal."""
        
        if not document_dtos:
            raise InvalidValueException("Os documentos são obrigatórios para contatar o LMM.")
        
        if not prompt and not prompt_raw_bytes:
            raise InvalidValueException("O prompt ou os bytes do prompt são obrigatórios para contatar o LMM.")
        
        if prompt and (prompt_raw_bytes or prompt_mime_type):
            raise InvalidValueException("O prompt em texto e os bytes do prompt não podem ser utilizados juntos. Escolha um dos dois para contatar o LMM.")
        
        if (prompt_raw_bytes and not prompt_mime_type) or (not prompt_raw_bytes and prompt_mime_type):
            raise InvalidValueException("Tanto os bytes do prompt quanto o tipo MIME são necessários para contatar o LMM com um arquivo.")

        context = [doc.metadata.chunk for doc in document_dtos if doc.metadata.chunk]
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
        objects = [
            Object(
                key=doc.metadata.object.key,
                url=doc.metadata.object.url,
                include_in_prompt=doc.metadata.object.include_in_prompt
            )
            for doc in document_dtos
        ]
        metadatas = [
            Metadata(
                type=doc.metadata.type,
                chunk=doc.metadata.chunk,
                source=doc.metadata.source,
                object=object
            )
            for doc, object in zip(document_dtos, objects)
        ]
        documents = [
            Document (
                metadata=metadata,
                score=doc.score,
                rerank_score=doc.rerank_score
            )
            for doc, metadata in zip(document_dtos, metadatas)
        ]
        
        try:
           
            return await self._repository.get_interator(
                final_prompt=final_prompt,
                documents=documents,
                prompt_raw_bytes=prompt_raw_bytes,
                prompt_mime_type=prompt_mime_type
            )
            
        except Exception as e:
            raise LmmException(
                "Erro durante a comunicação com o LMM para geração de conteúdo",
                e
            ) from e
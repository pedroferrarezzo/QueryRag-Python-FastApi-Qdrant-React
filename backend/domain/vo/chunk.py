from pydantic import BaseModel, field_validator

from domain.exceptions import InvalidValueException

class Chunk(BaseModel):
    """Value Object para armazenar um pedaço de conteúdo."""

    content: str | bytes
    """Conteúdo do pedaço."""

    @field_validator("content", mode="after")
    @classmethod
    def validate_content_rules(cls, value):
        if isinstance(value, str):
            if not cls._is_valid_chunk(value):
                raise InvalidValueException("Chunk inválido: o conteúdo é muito curto ou tem baixa proporção de caracteres alfanuméricos.")
            
        return value

    @staticmethod
    def _is_valid_chunk(text: str) -> bool:
        """Valida se um chunk é útil para gerar um embedding, filtrando chunks muito curtos ou com baixa proporção de caracteres alfanuméricos, o que pode indicar que o chunk é "quebrado" ou contém principalmente símbolos, e portanto pode não ser útil para representação semântica."""
        text = text.strip()

        if len(text) < 50:
            return False

        letters = sum(c.isalnum() for c in text)

        # Calcula a proporção de caracteres alfanuméricos em relação ao total de caracteres. 
        # Se for muito baixo, provavelmente é um chunk "quebrado" ou com muitos símbolos, o que pode indicar que não é um chunk útil para embedding.
        ratio = letters / len(text)

        # mais restritivo
        if ratio < 0.6:
            return False

        # evita chunks "visualmente estruturais"
        if text.count("|") > 3:
            return False

        return True
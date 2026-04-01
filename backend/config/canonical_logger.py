import logging
import contextvars

_log_context = contextvars.ContextVar("context", default={})

class LogContextFilter(logging.Filter):
    """Filtro de log para adicionar o contexto de log às mensagens de log."""
    def filter(self, record):
        context = _log_context.get()
        # Cria uma string com todos os valores: "chave1=valor1 chave2=valor2"
        record.log_context = " ".join([f"{k}={v}" for k, v in context.items()])
        return True

def put_log_context(key, value):
    """Adiciona um par chave-valor ao contexto de log."""
    ctx = _log_context.get().copy()
    ctx[key] = value
    _log_context.set(ctx)

def clear_log_context():
    """Limpa o contexto de log, resetando para o dicionário vazio."""
    _log_context.set({})

def configure_logging():
    """Configura o logger para incluir os dados do contexto de log em cada mensagem."""
    logger = logging.getLogger("app")

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(log_context)s] %(message)s')
    handler.setFormatter(formatter)

    handler.addFilter(LogContextFilter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

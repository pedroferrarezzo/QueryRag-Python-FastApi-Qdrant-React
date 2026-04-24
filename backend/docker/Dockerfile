FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends libmagic1 libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup app \
    && adduser --ingroup app app 
 
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    # Necessário pois o processo da aplicação é executado como um usuário não-root, e algumas libs precisam escrever em seus diretórios de instalação para funcionar corretamente.
    && chown -R app:app /usr/local/lib/python3.11/site-packages/

COPY --chown=app:app . .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs', timeout=5)" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends libmagic1 && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system app \
    && adduser --system --ingroup app app 

# A lib static-ffmpeg precisa gravar/executar binários dentro da pasta de pacotes do Python (ex: .lock). 
# Como o usuário 'app' será utilizado para subir o processo da aplicação, ele precisa ser o dono dessa pasta também.    
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && chown -R app:app /usr/local/lib/python3.11/site-packages/static_ffmpeg/

COPY --chown=app:app . .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs', timeout=5)" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
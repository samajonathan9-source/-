# RATISS One — image Docker (serveur API).
# MCT = Modele de Comprehension Topologique. Build reproductible.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# dependances systeme minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# dependances Python
COPY ratiss_skynet/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r requirements.txt

# code + modele (le modele est un pointeur Git LFS ; monter les poids reels
# via un volume ou les telecharger au premier demarrage)
COPY ratiss_skynet ./ratiss_skynet
COPY models ./models

WORKDIR /app/ratiss_skynet
ENV RATIS_MODEL_DIR=/app/models/RATISS-One
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "api/server.py"]

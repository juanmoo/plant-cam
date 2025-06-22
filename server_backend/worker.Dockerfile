FROM python:3.11-slim
WORKDIR /app
COPY src/requirements.txt ./
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt
COPY src/ ./
COPY static/ /static
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
CMD ["celery","-A","tasks.celery_app","worker","--loglevel=info"]
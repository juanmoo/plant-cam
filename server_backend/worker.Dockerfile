FROM python:3.11-slim
WORKDIR /app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./
COPY static ./static
ENV PYTHONUNBUFFERED=1
CMD ["celery","-A","tasks.celery_app","worker","--loglevel=info"]
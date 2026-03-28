FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY supportdesk_openenv /app/supportdesk_openenv
COPY main.py baseline.py openenv.yaml /app/

RUN pip install --no-cache-dir .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]


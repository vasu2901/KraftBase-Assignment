
FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "user-service.main:app", "--host", "0.0.0.0", "--port", "8000"]


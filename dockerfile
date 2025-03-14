FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PORT = 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
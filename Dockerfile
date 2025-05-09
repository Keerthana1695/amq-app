FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install flask python-qpid-proton

EXPOSE 8080

CMD ["python", "app.py"]

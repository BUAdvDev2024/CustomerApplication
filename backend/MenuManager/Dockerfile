FROM python:3.13-slim

WORKDIR /src

COPY src/requirements.txt /src
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8080

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
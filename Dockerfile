FROM python:3.9-alpine

ENV TZ America/Mexico_City

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["app.py"]

ENTRYPOINT ["python3"]

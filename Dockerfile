FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV IN_DOCKER=true

EXPOSE 8888

CMD ["sh", "-c", "if [ \"$RUN_TESTS\" = 'true' ] ; then pytest --disable-warnings ; else uvicorn main:app --host 0.0.0.0 --port 8888 ; fi"]


FROM python:3.12-slim

RUN groupadd -r user && useradd -r -g user user

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/ ./app

RUN chown -R user:user /app

USER user

EXPOSE 80

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "80"]
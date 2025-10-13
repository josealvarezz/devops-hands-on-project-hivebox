FROM python:3.14-slim@sha256:5cfac249393fa6c7ebacaf0027a1e127026745e603908b226baa784c52b9d99b

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
FROM python:3.12-bullseye

WORKDIR /app

ADD requirements.txt /app/
RUN python -m pip install -r requirements.txt

COPY . .

CMD [ "uvicorn" , "main:app" , "--host" , "0.0.0.0" , "--port" , "8000" ]

# syntax=docker/dockerfile:1
FROM python:3.9.5-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc g++ musl-dev linux-headers libffi-dev rust cargo openssl-dev  
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "app.py"]
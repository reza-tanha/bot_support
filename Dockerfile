FROM python:latest
# FROM nginx:1.19.0-alpine
WORKDIR /app


# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy data
COPY nginx .
COPY requirements.txt .
COPY config .
COPY entrypoint.sh .

# install dependencies
RUN pip install -r requirements.txt && \    
    apt-get update && \
    apt-get install -y nginx

# COPY ./nginx/nginx.conf /etc/nginx/ 
COPY nginx/default.conf /etc/nginx/conf.d/
# run entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]


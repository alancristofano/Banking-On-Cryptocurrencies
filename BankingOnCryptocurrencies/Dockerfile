FROM python:3.6 
ENV PYTHONUNBUFFERED 1
RUN mkdir /app 
WORKDIR /app
COPY requisitos.txt /app/
RUN pip3 install -r /app/requisitos.txt
ADD . /app/
EXPOSE 8000


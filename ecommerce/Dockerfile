FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ecommerce
COPY requirements.txt /ecommerce

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y

RUN pip install --upgrade pip

RUN pip install -r /ecommerce/requirements.txt

COPY . /ecommerce

COPY entrypoint.sh .

ENTRYPOINT ["/ecommerce/entrypoint.sh"]
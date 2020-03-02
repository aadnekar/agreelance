FROM python:3
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./config/requirements.txt
RUN pip install -r ./config/requirements.txt

COPY . ./code


# CMD sh init.sh && python3 manage.py runserver 0.0.0.0:8000
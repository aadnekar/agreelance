FROM python:3
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /code
WORKDIR /code
COPY . ./code
RUN pip install -r code/requirements.txt


# CMD sh init.sh && python3 manage.py runserver 0.0.0.0:8000
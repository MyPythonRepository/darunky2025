FROM python:3.12-slim

RUN apt update & mkdir /darunky

WORKDIR /darunky

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r requirements.txt

CMD ["python", "src/manage.py", "runserver"]

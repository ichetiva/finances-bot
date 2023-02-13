FROM python:3.10

WORKDIR /code

COPY Pipfile* /code/
RUN pip install -U pipenv
RUN pipenv install --deploy --system --ignore-pipfile

COPY ./src /code/

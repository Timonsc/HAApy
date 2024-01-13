FROM python:3.10.2-slim

RUN pip install poetry

COPY . .

RUN poetry install

ENTRYPOINT [ "poetry", "run", "python", "-m", "haa.py" ]
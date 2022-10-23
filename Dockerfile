FROM python:3.10
COPY / app
COPY pyproject.toml /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} \
    PYTHONUNBUFFERED=1
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main
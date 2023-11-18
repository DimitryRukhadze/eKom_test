FROM python:3.11.6-slim
RUN apt-get update && apt-get install -y curl
WORKDIR /
RUN curl -sSL https://install.python-poetry.org | python3.11 -
ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN poetry install --no-dev
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
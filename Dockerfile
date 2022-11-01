FROM python:3.10-slim

WORKDIR /opt/todolist/

COPY src/requirements.txt .

RUN pip install -r requirements.txt

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHON_PATH=/opt/todolist

RUN groupadd --system service && useradd --system -g service api

COPY ./src .
USER api


ENTRYPOINT ["bash", "entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

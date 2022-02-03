FROM python:3.7-slim

RUN pip install pipenv

ENV SRC_DIR /home/ycube/tek/tek3/Epitech_dashboard/youtube_connection

WORKDIR ${SRC_DIR}

COPY Pipfile Pipfile.lock ${SRC_DIR}/

RUN pipenv install --system --clear

COPY ./ ${SRC_DIR}/

WORKDIR ${SRC_DIR}/flask_youtube_search

CMD ["flask", "run", "-h", "O.O.O.O"]
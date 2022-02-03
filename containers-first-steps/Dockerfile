FROM python:3.7-slim

RUN pip install pipenv

ENV SRC_DIR /usr/local/src/containers-first-steps/home/ycube/tek/tek3/Epitech_dashboard/containers-first-steps

WORKDIR ${SRC_DIR}

COPY Pipfile Pipfile.lock ${SRC_DIR}/

RUN pipenv install --system --clear

COPY ./ ${SRC_DIR}/

WORKDIR ${SRC_DIR}/src/webapp

CMD ["flask", "run", "-h", "0.0.0.0"]
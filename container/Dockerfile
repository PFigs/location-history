FROM python:3 as setup

WORKDIR /app

RUN pip install pipenv==2020.8.13
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pipenv lock --requirements --dev > dev-requirements.txt

RUN cat requirements.txt && cat dev-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r dev-requirements.txt

COPY . .

RUN pip install -e .

CMD [ "timemap-report" ]

FROM setup as test

RUN ./.ci/build.sh
RUN ./.ci/test.sh

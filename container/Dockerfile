FROM python:3 as build

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
RUN ./.ci/build.sh
RUN ./.ci/test.sh

FROM python:3 

WORKDIR /app

COPY --from=build /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /app/dist/*.whl . 
COPY --from=build /app/tests/gmaps_sample.json .history.json 
COPY --from=build /app/examples/*.py . 
COPY --from=build /app/defaults.yml .

RUN pip install --no-cache-dir *.whl && rm *.whl

CMD [ "python", "location_report.py" ]


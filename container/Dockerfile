FROM python:3 as build

WORKDIR /app

COPY dev-requirements.txt ./
RUN pip install --no-cache-dir -r dev-requirements.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

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


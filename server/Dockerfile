FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY ./env ./env

RUN /bin/bash -c "source env/bin/activate"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python"]
CMD ["app.py"]
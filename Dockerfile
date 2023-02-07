FROM datamechanics/spark:3.1-latest

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /opt/application/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app/ app/
COPY main.py .
COPY ./postgresql-42.5.1.jar /opt/spark/jars

CMD ["python3", "main.py"]
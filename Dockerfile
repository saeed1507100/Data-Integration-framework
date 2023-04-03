FROM apache/airflow:2.5.2
COPY requirements.txt .
COPY app app
COPY setup.py .
COPY .kaggle .kaggle

RUN pip install --user --upgrade pip

# Install python dependencies
RUN pip install --no-cache-dir --root-user-action=ignore .
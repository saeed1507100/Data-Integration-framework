FROM apache/airflow:2.5.2
COPY requirements.txt .
COPY app app
COPY setup.py .
COPY keys keys
COPY .env ./.env
RUN mkdir data/

ENV KAGGLE_USERNAME=$KAGGLE_USERNAME \
    KAGGLE_KEY=$KAGGLE_KEY \
    SUPABASE_DB_REFERENCE_ID=$SUPABASE_DB_REFERENCE_ID \
    SUPABASE_DB_PASSWORD=$SUPABASE_DB_PASSWORD \
    GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS

RUN pip install --user --upgrade pip

# Install python dependencies
RUN pip install --no-cache-dir --root-user-action=ignore .
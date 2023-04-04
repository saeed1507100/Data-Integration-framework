# Introduction
## Data-Integration-framework
A tool to transfer data between multiple ranges of data stores without coding. Currently supports :
- **Sources**: google-cloud-bigquery, kaggle
- **destinations**: postgresql

# Environment setup
### **1. Build the extended docker container for airflow**

```commandline
docker buildx build . --tag extended_airflow:latest --platform linux/amd64
```
We have specified the platform to resolve the architecture related problems associated with M1 chip with ARM64 architecture.

### **2. Initialize the database**
```commandline
docker compose up airflow-init
```
### **3. Start Airflow**
When we have successfully initialized the database, we can start the airflow by running the following command.
```commandline
docker compose up -d
```

### **4. Restart Docker Containers**
When we add some new feature to the dockerfile or python packages, we can rebuild and run the docker containers by following shell script.
```commandline
sh rerun_airflow_docker.sh
```

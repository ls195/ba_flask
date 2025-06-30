FROM python:3.11-slim

WORKDIR /locust

RUN pip install locust

EXPOSE 8089

# "flask:5000" ist der Service-Name aus docker-compose (siehe unten)
CMD ["locust", "--host=http://flask:8000"]


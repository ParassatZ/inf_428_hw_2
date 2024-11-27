FROM python:3.10-slim
RUN pip install elasticsearch pandas numpy
COPY . /app
WORKDIR /app
EXPOSE 9200
CMD ["python", "task_2.py"]

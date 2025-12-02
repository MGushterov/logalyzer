FROM python:3.12-alpine3.22
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY logalyzer ./logalyzer
ENV PYTHONPATH=/usr/local/app

ENTRYPOINT ["python", "-m", "logalyzer"]
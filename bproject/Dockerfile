FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Debug Tools
RUN apk --no-cache add curl

# Run command
CMD python manage.py runserver 0.0.0.0:8000

FROM python:3.7

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system
ADD . ./

# Server
STOPSIGNAL SIGINT
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

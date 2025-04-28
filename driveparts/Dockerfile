FROM python
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install django-cors-headers
WORKDIR /app/www/driveparts
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER root
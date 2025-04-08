# Dockerfile

FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements
COPY requirements/requirements.txt /app/requirements.txt

# Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy the rest of the project
COPY . .

# Collect static files (Django)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('prozio', 'email@example.com', 'ciao123')"
#Start Django via Daphne (ASGI)
CMD ["uvicorn", "pizza_hub.asgi:django_app", "--host", "0.0.0.0", "--port", "8000"]
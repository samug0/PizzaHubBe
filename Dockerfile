# Dockerfile

FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements
COPY requirements/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ./requirements/requirements.txt

# Copy the project
COPY . .

# Collect static files (Django)
RUN python manage.py collectstatic --noinput


RUN python manage.py --noinput
# Expose port
EXPOSE 8000

# Start Django via Daphne (ASGI)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "pizza_hub.asgi:application"]

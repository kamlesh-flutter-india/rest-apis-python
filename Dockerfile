FROM python:3.13.7
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
# EXPOSE 5000 5678
CMD ['gunicorn','--bind','0.0.0.0:80','app:create_app()']
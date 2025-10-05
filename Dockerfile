FROM python:3.13.7
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000 5678
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
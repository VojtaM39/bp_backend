FROM vojtam39/openpose:latest

WORKDIR /app
COPY . ./
CMD ["python", "main.py"]


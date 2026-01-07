FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cấp quyền thực thi
RUN chmod +x ./entrypoint.sh || true

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

# LƯU Ý: Đổi app.main -> src.main
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
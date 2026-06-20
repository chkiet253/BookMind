# Stage 1: Tải và đóng gói các thư viện (Wheel)
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Tiến hành build các thư viện thành file wheels cục bộ
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage (Chỉ copy code và thư viện đã build sạch)
FROM python:3.11-slim

WORKDIR /app

# Copy các thư viện đã được cài đặt từ Stage 1 qua
COPY --from=builder /root/.local /root/.local
COPY . .

# Thêm đường dẫn thư viện vào biến môi trường hệ thống trong Docker
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "src.api.v1.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
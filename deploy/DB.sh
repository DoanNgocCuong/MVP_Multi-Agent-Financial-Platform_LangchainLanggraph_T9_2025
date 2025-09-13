# ===========================================
# DOCKER POSTGRESQL SETUP - COMPLETE WORKFLOW
# ===========================================

# 1. Chạy PostgreSQL container (tạo user + database tự động)
docker run --name postgres-ai-financial \
  -e POSTGRES_USER=ai_financial \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=ai_financial \
  -p 5432:5432 \
  -d postgres:15

# 2. Đợi container khởi động (2-3 giây)
sleep 3

# 3. Kiểm tra container đã chạy chưa
docker ps

# 4. Test kết nối trực tiếp (không cần tạo gì thêm)
docker exec -it postgres-ai-financial psql -U ai_financial -d ai_financial

# Trong psql shell, test:
# \l                    -- List databases (sẽ thấy ai_financial)
# \du                   -- List users (sẽ thấy ai_financial) 
# SELECT current_user;  -- Confirm current user
# \q                    -- Quit

# ===========================================
# CONTAINER MANAGEMENT
# ===========================================

# Stop container
docker stop postgres-ai-financial

# Start lại container (data vẫn còn)
docker start postgres-ai-financial

# Remove container hoàn toàn (mất data)
docker rm postgres-ai-financial

# View logs nếu có lỗi
docker logs postgres-ai-financial

# ===========================================
# DATABASE URL FOR .ENV
# ===========================================
# DATABASE_URL=postgresql://ai_financial:your_password@localhost:5432/ai_financial
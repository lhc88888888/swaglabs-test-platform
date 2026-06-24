FROM python:3.11-slim

# 替换 Debian 源为阿里云镜像（加速构建）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright 浏览器及系统依赖
RUN playwright install-deps chromium
RUN playwright install chromium

# 复制项目代码
COPY . .

# 默认命令：运行全部测试并生成 Allure 结果
CMD ["pytest", "-s"]
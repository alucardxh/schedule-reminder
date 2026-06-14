FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONPATH="/app:/app/src"

# 1. 仅复制依赖配置文件
COPY pyproject.toml uv.lock ./

# 2. 【核心修改】只同步第三方依赖，不安装当前项目，这样就不会卡在找不到源码这一步
RUN uv sync --frozen --no-dev --no-install-project

# 3. 复制你的所有源码（包括 src 目录）
COPY . .

# 4. 源码到位后，补一次同步，把你的 schedule-reminder 真正安装进环境
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "schedule_reminder.main"]
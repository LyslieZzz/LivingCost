# 城市生活成本查询 API

基于 FastAPI 构建的城市生活成本查询后端服务。

## 快速开始

### 使用 Docker Compose（推荐）

```bash
# 复制环境变量文件
cp .env.example .env

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f api
```

服务启动后访问：
- API 文档：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

### 本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 运行测试

```bash
pytest
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/cities` | GET | 获取城市列表 |
| `/api/cities/{cityKey}/costs` | GET | 获取城市生活成本详情 |
| `/api/cities/{cityKey}/estimate` | GET | 获取城市月度预估 |
| `/api/categories/{categoryKey}/comparison` | GET | 获取分类价格对比 |
| `/api/compare?cities=beijing,shanghai` | GET | 多城市对比 |

## 项目结构

```
backend/
├── app/
│   ├── main.py           # 应用入口
│   ├── config.py         # 配置管理
│   ├── database.py       # 数据库连接
│   ├── exceptions.py     # 异常处理
│   ├── models/           # SQLAlchemy 模型
│   ├── schemas/          # Pydantic 模型
│   ├── routers/          # API 路由
│   └── services/         # 业务逻辑
├── database/             # SQL 文件
├── tests/                # 单元测试
├── Dockerfile
└── docker-compose.yml
```

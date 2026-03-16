# 数据库设计文档

城市生活成本查询系统的数据库表结构设计。

## 文件说明

| 文件 | 说明 |
|------|------|
| `schema.sql` | 数据库表结构定义（建表语句） |
| `seed.sql` | 初始数据（城市、分类、价格项目） |
| `queries.sql` | API 对应的查询示例 |

## 快速开始

```bash
# 1. 创建数据库
mysql -u root -p -e "CREATE DATABASE living_cost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 执行建表脚本
mysql -u root -p living_cost < schema.sql

# 3. 导入初始数据
mysql -u root -p living_cost < seed.sql
```

## 表结构概览

```
┌─────────────────┐     ┌─────────────────┐
│     cities      │     │   categories    │
├─────────────────┤     ├─────────────────┤
│ city_key (PK)   │     │ category_key(PK)│
│ name            │     │ name            │
│ emoji           │     │ icon            │
│ center_def      │     │ sort_order      │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ monthly_estimates│     │     items       │
├─────────────────┤     ├─────────────────┤
│ city_key (FK)   │     │ id (PK)         │
│ single_estimate │     │ category_key(FK)│
└─────────────────┘     │ name            │
                        │ description     │
         ┌──────────────│ unit            │
         │              │ is_big_price    │
         │              │ is_salary       │
         │              └────────┬────────┘
         │                       │
         ▼                       ▼
    ┌─────────────────────────────────┐
    │          city_prices            │
    ├─────────────────────────────────┤
    │ city_key (FK) + item_id (FK)    │
    │ price                           │
    │ UNIQUE(city_key, item_id)       │
    └─────────────────────────────────┘
```

## 表详细说明

### cities - 城市表

存储支持的城市基本信息。

| 字段 | 类型 | 说明 |
|------|------|------|
| city_key | VARCHAR(50) | 城市唯一标识 |
| name | VARCHAR(100) | 城市中文名称 |
| emoji | VARCHAR(10) | 城市图标 |
| center_def | VARCHAR(200) | 市中心定义 |

### categories - 分类表

存储消费分类（餐饮、交通、租房等）。

| 字段 | 类型 | 说明 |
|------|------|------|
| category_key | VARCHAR(50) | 分类唯一标识 |
| name | VARCHAR(100) | 分类中文名称 |
| icon | VARCHAR(10) | 分类图标 |
| sort_order | INT | 排序顺序 |

### items - 价格项目表

存储具体消费项目的元数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 项目ID |
| category_key | VARCHAR(50) | 所属分类 |
| name | VARCHAR(200) | 项目名称 |
| description | VARCHAR(500) | 项目描述 |
| unit | VARCHAR(50) | 单位 |
| is_big_price | BOOLEAN | 是否为大额价格 |
| is_salary | BOOLEAN | 是否为薪资数据 |
| sort_order | INT | 排序顺序 |

### city_prices - 城市价格表

存储各城市的具体价格数据（核心关联表）。

| 字段 | 类型 | 说明 |
|------|------|------|
| city_key | VARCHAR(50) | 城市标识 |
| item_id | INT | 项目ID |
| price | DECIMAL(12,2) | 价格 |

### monthly_estimates - 月度预估表

存储各城市的月度支出预估。

| 字段 | 类型 | 说明 |
|------|------|------|
| city_key | VARCHAR(50) | 城市标识 |
| single_estimate | DECIMAL(10,2) | 单人月度预估 |

## 索引说明

| 索引名 | 表 | 字段 | 用途 |
|--------|-----|------|------|
| idx_items_category | items | category_key | 按分类查询项目 |
| idx_items_sort | items | category_key, sort_order | 分类内排序 |
| idx_city_prices_city | city_prices | city_key | 按城市查询价格 |
| idx_city_prices_item | city_prices | item_id | 按项目查询价格 |
| uk_city_item | city_prices | city_key, item_id | 唯一约束 |

## API 查询映射

| API | 主要查询表 |
|-----|-----------|
| GET /api/cities | cities |
| GET /api/cities/{cityKey}/costs | cities + categories + items + city_prices |
| GET /api/categories/{categoryKey}/comparison | items + city_prices |
| GET /api/compare | cities + monthly_estimates + city_prices |
| GET /api/cities/{cityKey}/estimate | monthly_estimates + cities |

详细查询语句请参考 `queries.sql`。

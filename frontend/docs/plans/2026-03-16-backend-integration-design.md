# 前端后端集成设计文档

日期：2026-03-16

## 概述

将前端从静态数据模式改造为调用后端 API，创建独立的 API 服务模块统一管理 API 调用和错误处理。

## 当前状态

- 前端使用 `js/data.js` 中的静态数据 (`CITY_DATA`, `MONTHLY_ESTIMATE`)
- 无 API 调用层
- 后端 API 已就绪，运行在 `http://localhost:8000`

## 设计方案

### 1. API 模块结构 (`js/api.js`)

```javascript
// 配置
const API_BASE_URL = 'http://localhost:8000/api';

// 缓存
const cache = {
  cities: null,           // 城市列表
  cityData: {},           // { beijing: {...}, shanghai: {...} }
  estimates: {}           // { beijing: {...}, shanghai: {...} }
};

// 核心函数
async function fetchCities()                         // 获取城市列表
async function fetchCityCosts(cityKey)               // 获取城市完整数据
async function fetchCityEstimate(cityKey)            // 获取月度预估
async function fetchCategoryComparison(categoryKey)  // 获取跨城市对比

// 辅助函数
function handleError(error)                          // 统一错误处理
function clearCache()                                // 清除缓存
```

**缓存策略**：
- 首次请求后存入缓存
- 后续请求直接返回缓存数据
- 页面刷新时缓存重置

### 2. app.js 改造

**改动点**：

1. **初始化流程**：改为异步，先获取城市列表再渲染
2. **城市切换**：`switchCity()` 改为异步函数
3. **价格范围计算**：使用后端 comparison API 或预加载数据
4. **加载状态**：添加 loading 提示
5. **错误处理**：网络错误时显示友好提示

**数据流**：
```
页面加载 → 显示loading → API请求 → 缓存 → 渲染
```

### 3. 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 网络错误 | 显示"网络连接失败，请检查后端服务是否运行" |
| 404 | 显示"城市数据不存在" |
| 500 | 显示"服务器错误，请稍后重试" |

### 4. UI 反馈

- Loading 状态：内容区域显示加载提示
- 错误状态：显示错误信息 + 重试按钮
- 成功状态：正常渲染内容

## 文件变更

| 文件 | 操作 | 说明 |
|-----|------|-----|
| `js/api.js` | 新建 | API 调用模块 |
| `js/app.js` | 修改 | 改为异步模式 |
| `js/data.js` | 可删除 | 不再需要静态数据 |
| `index.html` | 修改 | 引入 api.js |

## 后端 API 端点

| 端点 | 方法 | 用途 |
|-----|------|-----|
| `/api/cities` | GET | 获取城市列表 |
| `/api/cities/{city_key}/costs` | GET | 获取城市完整数据 |
| `/api/cities/{city_key}/estimate` | GET | 获取月度预估 |
| `/api/categories/{category_key}/comparison` | GET | 获取跨城市价格对比 |

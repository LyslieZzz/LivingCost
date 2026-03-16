# 前端后端集成实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将前端从静态数据模式改造为调用后端 API，创建独立的 API 服务模块。

**Architecture:** 创建 `js/api.js` 作为 API 层，包含缓存机制和错误处理。修改 `js/app.js` 为异步模式，通过 API 层获取数据。保留原有 UI 渲染逻辑不变。

**Tech Stack:** 原生 JavaScript、Fetch API、async/await

---

## Task 1: 创建 API 模块

**Files:**
- Create: `frontend/js/api.js`

**Step 1: 创建 api.js 文件**

```javascript
const API_BASE_URL = 'http://localhost:8000/api';

const cache = {
  cities: null,
  cityData: {},
  priceRanges: {}
};

async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message = errorData.error?.message || `HTTP ${response.status}`;
    throw new Error(message);
  }
  return response.json();
}

async function fetchCities() {
  if (cache.cities) {
    return cache.cities;
  }
  const response = await fetch(`${API_BASE_URL}/cities`);
  const data = await handleResponse(response);
  cache.cities = data.cities;
  return cache.cities;
}

async function fetchCityCosts(cityKey) {
  if (cache.cityData[cityKey]) {
    return cache.cityData[cityKey];
  }
  const response = await fetch(`${API_BASE_URL}/cities/${cityKey}/costs`);
  const data = await handleResponse(response);
  cache.cityData[cityKey] = data;
  return data;
}

async function fetchAllCitiesData() {
  const cities = await fetchCities();
  const promises = cities.map(city => fetchCityCosts(city.key));
  await Promise.all(promises);
  return cache.cityData;
}

async function fetchCategoryComparison(categoryKey) {
  if (cache.priceRanges[categoryKey]) {
    return cache.priceRanges[categoryKey];
  }
  const response = await fetch(`${API_BASE_URL}/categories/${categoryKey}/comparison`);
  const data = await handleResponse(response);
  cache.priceRanges[categoryKey] = data;
  return data;
}

function getCachedCityData(cityKey) {
  return cache.cityData[cityKey] || null;
}

function getCachedPriceRange(categoryKey, itemIndex) {
  const comparison = cache.priceRanges[categoryKey];
  if (!comparison || !comparison.items[itemIndex]) {
    return null;
  }
  const item = comparison.items[itemIndex];
  return { min: item.min, max: item.max };
}

function clearCache() {
  cache.cities = null;
  cache.cityData = {};
  cache.priceRanges = {};
}

window.API = {
  fetchCities,
  fetchCityCosts,
  fetchAllCitiesData,
  fetchCategoryComparison,
  getCachedCityData,
  getCachedPriceRange,
  clearCache
};
```

**Step 2: 验证文件创建成功**

在浏览器控制台检查 `window.API` 是否存在。

---

## Task 2: 修改 index.html 引入 API 模块

**Files:**
- Modify: `frontend/index.html:80-81`

**Step 1: 在 data.js 之前引入 api.js**

将：
```html
  <script src="js/data.js"></script>
  <script src="js/app.js"></script>
```

改为：
```html
  <script src="js/api.js"></script>
  <script src="js/app.js"></script>
```

---

## Task 3: 改造 app.js 为异步模式

**Files:**
- Modify: `frontend/js/app.js`

**Step 1: 添加状态管理和 UI 辅助函数**

在文件开头（DOMContentLoaded 回调内部）添加：

```javascript
  let currentCity = 'beijing';
  let isLoading = false;

  const cityButtons = document.querySelectorAll('.city-btn');
  const dataSection = document.getElementById('dataSection');
  const singleCost = document.getElementById('singleCost');
  const avgSalary = document.getElementById('avgSalary');
  const centerDef = document.getElementById('centerDef');

  function showLoading() {
    isLoading = true;
    dataSection.innerHTML = '<div class="loading-state">加载中...</div>';
  }

  function showError(message) {
    dataSection.innerHTML = 
      '<div class="error-state">' +
        '<p>' + message + '</p>' +
        '<button class="retry-btn" onclick="location.reload()">重试</button>' +
      '</div>';
  }
```

**Step 2: 修改 getPriceRange 函数使用缓存**

将原来的 `getPriceRange` 函数：
```javascript
  function getPriceRange(categoryKey, itemIndex) {
    const prices = Object.keys(CITY_DATA).map(cityKey => {
      const cat = CITY_DATA[cityKey].categories[categoryKey];
      return cat ? cat.items[itemIndex].price : 0;
    });
    return { min: Math.min(...prices), max: Math.max(...prices) };
  }
```

改为：
```javascript
  function getPriceRange(categoryKey, itemIndex) {
    const cached = API.getCachedPriceRange(categoryKey, itemIndex);
    if (cached) {
      return cached;
    }
    const allData = Object.values(API.getCachedCityData('beijing') ? 
      Object.keys(cache.cityData).reduce((acc, key) => {
        acc[key] = API.getCachedCityData(key);
        return acc;
      }, {}) : {});
    
    let min = Infinity, max = -Infinity;
    Object.keys(API.cityData || {}).forEach(cityKey => {
      const cityData = API.getCachedCityData(cityKey);
      if (cityData && cityData.categories[categoryKey]) {
        const price = cityData.categories[categoryKey].items[itemIndex]?.price;
        if (price !== undefined) {
          min = Math.min(min, price);
          max = Math.max(max, price);
        }
      }
    });
    return { min: min === Infinity ? 0 : min, max: max === -Infinity ? 0 : max };
  }
```

**Step 3: 修改 renderSummary 函数使用 API 数据**

将原来的：
```javascript
  function renderSummary(cityKey) {
    const city = CITY_DATA[cityKey];
    const estimate = MONTHLY_ESTIMATE[cityKey];
    const salary = city.categories.salary.items.find(i => i.isSalary);

    singleCost.textContent = '¥' + estimate.single.toLocaleString();
    avgSalary.textContent = '¥' + salary.price.toLocaleString();
    centerDef.textContent = city.centerDef;
  }
```

改为：
```javascript
  function renderSummary(cityData) {
    const salary = cityData.categories.salary.items.find(i => i.isSalary);

    singleCost.textContent = '¥' + cityData.monthlyEstimate.single.toLocaleString();
    avgSalary.textContent = '¥' + salary.price.toLocaleString();
    centerDef.textContent = cityData.city.centerDef;
  }
```

**Step 4: 修改 renderCity 函数使用 API 数据**

将原来的：
```javascript
  function renderCity(cityKey) {
    const city = CITY_DATA[cityKey];
    dataSection.innerHTML = '';

    renderSummary(cityKey);

    const categoryOrder = ['dining', 'market', 'transport', 'utilities', 'leisure', 'clothing', 'housing', 'salary'];

    categoryOrder.forEach((catKey) => {
      const category = city.categories[catKey];
      if (category) {
        const card = renderCategory(catKey, category);
        dataSection.appendChild(card);
      }
    });

    requestAnimationFrame(() => {
      document.querySelectorAll('.category-body').forEach(body => {
        body.style.maxHeight = body.scrollHeight + 'px';
      });
    });
  }
```

改为：
```javascript
  function renderCity(cityData) {
    dataSection.innerHTML = '';

    renderSummary(cityData);

    const categoryOrder = ['dining', 'market', 'transport', 'utilities', 'leisure', 'clothing', 'housing', 'salary'];

    categoryOrder.forEach((catKey) => {
      const category = cityData.categories[catKey];
      if (category) {
        const card = renderCategory(catKey, category);
        dataSection.appendChild(card);
      }
    });

    requestAnimationFrame(() => {
      document.querySelectorAll('.category-body').forEach(body => {
        body.style.maxHeight = body.scrollHeight + 'px';
      });
    });
  }
```

**Step 5: 修改 switchCity 为异步函数**

将原来的：
```javascript
  function switchCity(cityKey) {
    if (cityKey === currentCity) return;
    currentCity = cityKey;

    cityButtons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.city === cityKey);
    });

    dataSection.style.opacity = '0';
    dataSection.style.transform = 'translateY(10px)';

    setTimeout(() => {
      renderCity(cityKey);
      dataSection.style.opacity = '1';
      dataSection.style.transform = 'translateY(0)';
    }, 200);
  }
```

改为：
```javascript
  async function switchCity(cityKey) {
    if (cityKey === currentCity || isLoading) return;
    currentCity = cityKey;

    cityButtons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.city === cityKey);
    });

    dataSection.style.opacity = '0';
    dataSection.style.transform = 'translateY(10px)';

    try {
      const cityData = await API.fetchCityCosts(cityKey);
      
      setTimeout(() => {
        renderCity(cityData);
        dataSection.style.opacity = '1';
        dataSection.style.transform = 'translateY(0)';
      }, 200);
    } catch (error) {
      console.error('Failed to load city data:', error);
      showError('加载城市数据失败: ' + error.message);
    }
  }
```

**Step 6: 添加初始化函数并修改启动逻辑**

将文件末尾的：
```javascript
  cityButtons.forEach(btn => {
    btn.addEventListener('click', () => switchCity(btn.dataset.city));
  });

  dataSection.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
  renderCity(currentCity);
```

改为：
```javascript
  async function init() {
    showLoading();
    
    try {
      await API.fetchAllCitiesData();
      
      const categoryOrder = ['dining', 'market', 'transport', 'utilities', 'leisure', 'clothing', 'housing', 'salary'];
      await Promise.all(categoryOrder.map(cat => API.fetchCategoryComparison(cat)));
      
      const cityData = API.getCachedCityData(currentCity);
      if (cityData) {
        renderCity(cityData);
      } else {
        throw new Error('无法获取城市数据');
      }
    } catch (error) {
      console.error('Initialization failed:', error);
      showError('初始化失败，请确保后端服务已启动: ' + error.message);
    }
  }

  cityButtons.forEach(btn => {
    btn.addEventListener('click', () => switchCity(btn.dataset.city));
  });

  dataSection.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
  init();
```

---

## Task 4: 添加 Loading 和 Error 样式

**Files:**
- Modify: `frontend/css/style.css`

**Step 1: 在 style.css 末尾添加样式**

```css
/* Loading and Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: var(--text-secondary);
}

.loading-state {
  font-size: 1.1rem;
}

.error-state p {
  margin-bottom: 20px;
  color: #e74c3c;
}

.retry-btn {
  padding: 10px 24px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: var(--primary-dark);
}
```

---

## Task 5: 删除静态数据文件

**Files:**
- Delete: `frontend/js/data.js`

**Step 1: 删除 data.js 文件**

该文件不再需要，所有数据从 API 获取。

---

## Task 6: 测试集成

**Step 1: 启动后端服务**

```bash
cd backend
docker-compose up -d
```

或者直接运行：
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Step 2: 在浏览器中打开前端**

打开 `frontend/index.html`，检查：
- [ ] 页面正常加载，显示北京数据
- [ ] 切换城市按钮正常工作
- [ ] 价格范围条正确显示
- [ ] 控制台无错误

**Step 3: 测试错误处理**

停止后端服务，刷新页面，检查：
- [ ] 显示错误提示
- [ ] 重试按钮可用

---

## 完成检查清单

- [ ] `js/api.js` 创建完成
- [ ] `index.html` 引入 api.js
- [ ] `js/app.js` 改为异步模式
- [ ] `css/style.css` 添加 loading/error 样式
- [ ] `js/data.js` 已删除
- [ ] 后端启动后前端正常工作
- [ ] 后端停止时显示错误提示

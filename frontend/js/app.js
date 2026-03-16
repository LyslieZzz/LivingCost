document.addEventListener('DOMContentLoaded', () => {
  let currentCity = 'beijing';
  let isLoading = false;

  const cityButtons = document.querySelectorAll('.city-btn');
  const dataSection = document.getElementById('dataSection');
  const singleCost = document.getElementById('singleCost');
  const avgSalary = document.getElementById('avgSalary');
  const centerDef = document.getElementById('centerDef');

  const CATEGORY_ORDER = ['dining', 'market', 'transport', 'utilities', 'leisure', 'clothing', 'housing', 'salary'];

  function showLoading() {
    dataSection.innerHTML =
      '<div class="loading-state" style="text-align:center;padding:48px;color:var(--text-secondary)">' +
      '<div style="font-size:1.25rem;margin-bottom:8px">加载中...</div>' +
      '<div style="font-size:0.9rem">正在获取城市生活成本数据</div>' +
      '</div>';
  }

  function showError(message) {
    dataSection.innerHTML =
      '<div class="error-state" style="text-align:center;padding:48px">' +
      '<div style="color:#dc2626;font-size:1.1rem;margin-bottom:12px">' + (message || '加载失败') + '</div>' +
      '<button type="button" class="retry-btn" style="margin-top:16px;padding:10px 24px;background:var(--primary);color:#fff;border:none;border-radius:var(--radius-sm);cursor:pointer;font-size:1rem">重试</button>' +
      '</div>';
    const retryBtn = dataSection.querySelector('.retry-btn');
    if (retryBtn) retryBtn.addEventListener('click', () => init());
  }

  function formatPrice(price) {
    if (price >= 10000) {
      const wan = price / 10000;
      return wan % 1 === 0 ? wan + '万' : wan.toFixed(2) + '万';
    }
    return price % 1 === 0 ? price.toLocaleString() : price.toFixed(2);
  }

  function formatRangeNum(price) {
    if (price >= 10000) {
      const wan = price / 10000;
      return wan % 1 === 0 ? wan + '万' : wan.toFixed(1) + '万';
    }
    return price % 1 === 0 ? price.toFixed(0) : price.toFixed(2);
  }

  function getPriceRange(categoryKey, itemIndex) {
    const cached = window.API && window.API.getCachedPriceRange(categoryKey, itemIndex);
    return cached || { min: 0, max: 0 };
  }

  function getRangeBarPosition(price, min, max) {
    if (max === min) return { left: 35, width: 30 };
    const spreadFactor = 0.15;
    const rangeMin = min * (1 - spreadFactor);
    const rangeMax = max * (1 + spreadFactor);
    const totalRange = rangeMax - rangeMin;

    const pos = ((price - rangeMin) / totalRange) * 100;
    const barWidth = Math.max(8, 12);
    const left = Math.max(0, Math.min(pos - barWidth / 2, 100 - barWidth));
    return { left, width: barWidth, rangeMin, rangeMax };
  }

  function renderSummary(cityData) {
    const salary = cityData.categories.salary.items.find(i => i.isSalary);

    singleCost.textContent = '¥' + cityData.monthlyEstimate.single.toLocaleString();
    avgSalary.textContent = '¥' + salary.price.toLocaleString();
    centerDef.textContent = cityData.city.centerDef;
  }

  function renderCategory(categoryKey, category) {
    const card = document.createElement('div');
    card.className = 'category-card';

    const header = document.createElement('div');
    header.className = 'category-header';
    header.innerHTML =
      '<span class="category-icon">' + category.icon + '</span>' +
      '<span class="category-title">' + category.name + '</span>' +
      '<span class="category-toggle">▼</span>';

    header.addEventListener('click', () => {
      card.classList.toggle('collapsed');
    });

    const body = document.createElement('div');
    body.className = 'category-body';

    const table = document.createElement('div');
    table.className = 'item-table';

    category.items.forEach((item, index) => {
      const range = getPriceRange(categoryKey, index);
      const barPos = getRangeBarPosition(item.price, range.min, range.max);

      const row = document.createElement('div');
      row.className = 'item-row';

      const priceClasses = ['item-price'];
      if (item.isBigPrice) priceClasses.push('big-price');
      if (item.isSalary) priceClasses.push('salary-price');

      const showBar = !item.isBigPrice && !item.isSalary;

      let priceHTML = '¥' + formatPrice(item.price);
      let unitHTML = '<span class="unit"> ' + item.unit + '</span>';

      let rangeBarHTML = '';
      if (showBar) {
        rangeBarHTML =
          '<div class="range-bar-wrap">' +
            '<span class="range-min">' + formatRangeNum(range.min) + '</span>' +
            '<div class="range-track">' +
              '<div class="range-fill" style="left:' + barPos.left + '%;width:' + barPos.width + '%"></div>' +
            '</div>' +
            '<span class="range-max">' + formatRangeNum(range.max) + '</span>' +
          '</div>';
      } else {
        rangeBarHTML = '<div class="no-range-placeholder"></div>';
      }

      row.innerHTML =
        '<div class="item-info">' +
          '<div class="item-name">' + item.name + '</div>' +
          (item.desc ? '<div class="item-desc">' + item.desc + '</div>' : '') +
        '</div>' +
        '<div class="' + priceClasses.join(' ') + '">' +
          priceHTML + unitHTML +
        '</div>' +
        rangeBarHTML;

      table.appendChild(row);
    });

    body.appendChild(table);
    card.appendChild(header);
    card.appendChild(body);

    return card;
  }

  function renderCity(cityData) {
    dataSection.innerHTML = '';

    renderSummary(cityData);

    CATEGORY_ORDER.forEach((catKey) => {
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

  async function switchCity(cityKey) {
    if (isLoading) return;
    if (cityKey === currentCity) return;
    const prevCity = currentCity;
    currentCity = cityKey;

    cityButtons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.city === cityKey);
    });

    dataSection.style.opacity = '0';
    dataSection.style.transform = 'translateY(10px)';

    try {
      isLoading = true;
      const cityData = await window.API.fetchCityCosts(cityKey);
      setTimeout(() => {
        renderCity(cityData);
        dataSection.style.opacity = '1';
        dataSection.style.transform = 'translateY(0)';
      }, 200);
    } catch (err) {
      currentCity = prevCity;
      cityButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.city === prevCity);
      });
      showError(err.message || '加载城市数据失败');
      dataSection.style.opacity = '1';
      dataSection.style.transform = 'translateY(0)';
    } finally {
      isLoading = false;
    }
  }

  async function init() {
    try {
      isLoading = true;
      showLoading();

      await window.API.fetchAllCitiesData();

      await Promise.all(CATEGORY_ORDER.map(catKey => window.API.fetchCategoryComparison(catKey)));

      const cityData = window.API.getCachedCityData(currentCity);
      if (cityData) {
        renderCity(cityData);
      } else {
        showError('无法获取默认城市数据');
      }
    } catch (err) {
      showError(err.message || '初始化失败');
    } finally {
      isLoading = false;
    }
  }

  cityButtons.forEach(btn => {
    btn.addEventListener('click', () => switchCity(btn.dataset.city));
  });

  dataSection.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
  init();
});

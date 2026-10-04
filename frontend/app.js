const API_URL = "http://localhost:8000/api/dashboard";

function formatCurrency(value) {
  return `$${Number(value || 0).toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

async function loadDashboard() {
  try {
    const response = await fetch(API_URL, { cache: "no-store" });
    if (!response.ok) throw new Error("Failed to load dashboard");
    const data = await response.json();
    renderSummary(data.market_summary || {});
    renderAssets(data.assets || []);
    renderHistory(data.history || {});
    renderNews(data.news || []);
    renderSocial(data.social || []);
    renderAlerts(data.alerts || []);
  } catch (error) {
    document.getElementById("market-summary").textContent = "The market monitor is unavailable right now. Please restart the backend.";
    console.error(error);
  }
}

function renderSummary(summary) {
  const strongest = summary.strongest_signal || { symbol: "N/A" };
  const bias = summary.market_bias || "neutral";
  document.getElementById("market-summary").textContent =
    `Tracking ${summary.crypto_count || 0} crypto assets and ${summary.stock_count || 0} equities. Market bias: ${bias}. Strongest current move: ${strongest.symbol}.`;

  const signals = [
    `Crypto market breadth: ${summary.crypto_count || 0} tracked assets`,
    `Equity coverage: ${summary.stock_count || 0} tracked stocks`,
    `Current bias: ${bias}`
  ];

  const signalList = document.getElementById("signal-list");
  signalList.innerHTML = signals.map((signal) => `<li>${signal}</li>`).join("");
}

function renderAssets(assets) {
  const assetGrid = document.getElementById("asset-grid");
  assetGrid.innerHTML = assets.map((asset) => {
    const isUp = Number(asset.change_pct || 0) >= 0;
    const badgeClass = isUp ? "up" : "down";
    const badgeText = isUp ? "Bullish" : "Risk";
    return `
      <article class="asset-card">
        <div class="asset-card-header">
          <div class="symbol">${asset.symbol}</div>
          <span class="badge ${badgeClass}">${badgeText}</span>
        </div>
        <div class="asset-price">${formatCurrency(asset.price)}</div>
        <div class="asset-meta"><span>24h</span><strong>${Number(asset.change_pct || 0).toFixed(2)}%</strong></div>
        <div class="asset-meta"><span>Signal</span><strong>${Number(asset.signal_score || 0).toFixed(2)}</strong></div>
        <div class="asset-meta"><span>Rumor</span><strong>${Number(asset.rumor_index || 0).toFixed(2)}</strong></div>
      </article>
    `;
  }).join("");
}

function createSparkline(points, color) {
  if (!points || points.length === 0) return "";
  const width = 220;
  const height = 60;
  const min = Math.min(...points);
  const max = Math.max(...points);
  const range = max - min || 1;

  const path = points.map((value, index) => {
    const x = (index / (points.length - 1)) * width;
    const y = height - ((value - min) / range) * (height - 8) - 4;
    return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
  }).join(' ');

  return `
    <svg class="sparkline" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-label="sparkline">
      <path d="${path}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linecap="round"></path>
    </svg>
  `;
}

function renderHistory(history) {
  const historyGrid = document.getElementById("history-grid");
  const symbols = Object.entries(history || {});
  if (!symbols.length) {
    historyGrid.innerHTML = "No trend data available.";
    return;
  }

  historyGrid.innerHTML = symbols.slice(0, 6).map(([symbol, points]) => {
    const isPositive = Number(points[points.length - 1] || 0) >= Number(points[0] || 0);
    const color = isPositive ? "#57d38a" : "#f46d6d";
    return `
      <div class="history-card">
        <div class="history-header">
          <strong>${symbol}</strong>
          <span class="trend ${isPositive ? 'up' : 'down'}">${isPositive ? 'Up' : 'Down'}</span>
        </div>
        ${createSparkline(points, color)}
        <div class="history-footer">
          <span>${formatCurrency(points[0])}</span>
          <span>${formatCurrency(points[points.length - 1])}</span>
        </div>
      </div>
    `;
  }).join("");
}

function renderNews(news) {
  const newsList = document.getElementById("news-list");
  newsList.innerHTML = news.map((item) => `
    <li>
      <a class="feed-item" href="${item.url || '#'}" target="_blank" rel="noreferrer">
        <h3>${item.title}</h3>
        <p>${item.summary}</p>
        <div class="meta-row">
          <span>${item.published || 'recent'}</span>
          <span class="score">sentiment ${Number(item.sentiment || 0).toFixed(2)} / rumor ${Number(item.rumor_index || 0).toFixed(2)}</span>
        </div>
      </a>
    </li>
  `).join("");
}

function renderSocial(social) {
  const socialList = document.getElementById("social-list");
  socialList.innerHTML = social.map((item) => `
    <li>
      <div class="feed-item">
        <h3>${item.symbol} • ${item.author}</h3>
        <p>${item.content}</p>
        <div class="meta-row">
          <span>${item.engagement || 0} engagement</span>
          <span class="score">sentiment ${Number(item.sentiment || 0).toFixed(2)} / rumor ${Number(item.rumor_index || 0).toFixed(2)}</span>
        </div>
      </div>
    </li>
  `).join("");
}

function renderAlerts(alerts) {
  const alertsList = document.getElementById("alerts-list");
  alertsList.innerHTML = alerts.map((alert) => `
    <li>
      <div class="feed-item">
        <h3>${alert.symbol} • ${alert.type}</h3>
        <p>${alert.summary}</p>
        <div class="meta-row">
          <span>${alert.severity}</span>
        </div>
      </div>
    </li>
  `).join("");
}

loadDashboard();
setInterval(loadDashboard, 60000);

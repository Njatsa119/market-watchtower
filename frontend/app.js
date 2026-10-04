const API_URL = "http://localhost:8000/api/dashboard";

async function loadDashboard() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to load dashboard");
    const data = await response.json();
    renderSummary(data.market_summary || {});
    renderAssets(data.assets || []);
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
        <div class="asset-price">$${Number(asset.price || 0).toLocaleString(undefined, { maximumFractionDigits: 2 })}</div>
        <div class="asset-meta"><span>24h</span><strong>${Number(asset.change_pct || 0).toFixed(2)}%</strong></div>
        <div class="asset-meta"><span>Signal</span><strong>${Number(asset.signal_score || 0).toFixed(2)}</strong></div>
        <div class="asset-meta"><span>Rumor</span><strong>${Number(asset.rumor_index || 0).toFixed(2)}</strong></div>
      </article>
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

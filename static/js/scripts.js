async function fetchCryptoData() {
    console.log("Fetching crypto data...");
    const response = await fetch('/cryptos');
    const data = await response.json();
    console.log("Crypto data:", data);
    const table = document.getElementById('crypto-table');
    const tableBody = table.getElementsByTagName('tbody')[0];
    const tableHead = table.getElementsByTagName('thead')[0];

    tableBody.innerHTML = ''; // Clear existing data
    tableHead.innerHTML = ''; // Clear existing headers

    // Create table headers
    const headerRow = tableHead.insertRow();
    ['Symbol', 'Current Price', '24h Change', 'Market Cap'].forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });

    data.forEach(crypto => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = crypto.symbol.toUpperCase();
        row.insertCell(1).textContent = `$${crypto.current_price.toFixed(2)}`;
        row.insertCell(2).textContent = `${crypto['24h_change'].toFixed(2)}%`;
        row.insertCell(3).textContent = `$${crypto.market_cap.toLocaleString()}`;
    });
    console.log("Crypto table updated.");
}

async function fetchStockData() {
    console.log("Fetching stock data...");
    const response = await fetch('/stocks');
    const data = await response.json();
    console.log("Stock data:", data);
    const table = document.getElementById('stock-table');
    const tableBody = table.getElementsByTagName('tbody')[0];
    const tableHead = table.getElementsByTagName('thead')[0];

    tableBody.innerHTML = ''; // Clear existing data
    tableHead.innerHTML = ''; // Clear existing headers

    // Create table headers
    const headerRow = tableHead.insertRow();
    ['Ticker', 'Current Price', 'Day High', 'Day Low'].forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });

    data.forEach(stock => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = stock.ticker;
        row.insertCell(1).textContent = `$${stock.current_price.toFixed(2)}`;
        row.insertCell(2).textContent = `$${stock.day_high.toFixed(2)}`;
        row.insertCell(3).textContent = `$${stock.day_low.toFixed(2)}`;
    });
    console.log("Stock table updated.");
}

async function trainRLAgent() {
    console.log("Training RL Agent...");
    const response = await fetch('/train_rl_agent', { method: 'POST' });
    const result = await response.json();
    console.log("RL Agent training result:", result);
    updateTable('rl-agent-table', result, ['timestamp', 'price', 'volume']);
}

async function evaluateRLAgent() {
    console.log("Evaluating RL Agent...");
    const response = await fetch('/evaluate_rl_agent', { method: 'POST' });
    const result = await response.json();
    console.log("RL Agent evaluation result:", result);
    updateTable('rl-agent-table', result, ['timestamp', 'price', 'volume', 'short_mavg', 'long_mavg']);
}

async function runTrendFollower() {
    console.log("Running Trend Follower strategy...");
    const response = await fetch('/run_trend_follower', { method: 'POST' });
    const result = await response.json();
    console.log("Trend Follower result:", result);
    if (result.error) {
        document.getElementById('strategy-results').textContent = result.error;
    } else {
        updateTable('strategy-table', result, ['timestamp', 'price', 'volume', 'short_mavg', 'long_mavg']);
    }
}

async function runMeanReversion() {
    console.log("Running Mean Reversion strategy...");
    const response = await fetch('/run_mean_reversion', { method: 'POST' });
    const result = await response.json();
    console.log("Mean Reversion result:", result);
    if (result.error) {
        document.getElementById('strategy-results').textContent = result.error;
    } else {
        updateTable('strategy-table', result, ['price', 'mean', 'std', 'z_score', 'signal', 'positions', 'buy_signal', 'sell_signal']);
    }
}

async function fetchStrategyResults() {
    console.log("Fetching strategy results...");
    const response = await fetch('/run_trend_follower', { method: 'POST' });
    const result = await response.json();
    console.log("Fetched strategy results:", result);
    if (result.error) {
        alert(result.error);
    } else {
        return result;
    }
}

async function showStrategyResults() {
    console.log("Showing strategy results...");
    const data = await fetchStrategyResults();
    if (data) {
        console.log("Rendering chart with data:", data);
        renderChart(data);
        document.getElementById('chart-container').style.display = 'block'; // Show the chart container
    }
}

function renderChart(data) {
    console.log("Rendering chart...");
    const ctx = document.getElementById('strategyChart').getContext('2d');
    const labels = data.map(entry => new Date(entry.timestamp));
    const prices = data.map(entry => entry.price);

    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Price',
                data: prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
    console.log("Chart rendered successfully.");
}

function updateTable(tableId, data, columns) {
    const table = document.getElementById(tableId);
    const tableBody = table.getElementsByTagName('tbody')[0];
    const tableHead = table.getElementsByTagName('thead')[0];
    
    tableBody.innerHTML = ''; // Clear existing data
    tableHead.innerHTML = ''; // Clear existing headers

    // Create table headers
    const headerRow = tableHead.insertRow();
    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column.charAt(0).toUpperCase() + column.slice(1).replace('_', ' ');
        headerRow.appendChild(th);
    });

    // Display the data entries with specified columns
    data.Data.forEach(entry => {
        const row = tableBody.insertRow();
        columns.forEach(column => {
            row.insertCell().textContent = entry[column];
        });
    });
}

// Test with sample data
const sampleData = [
    { timestamp: '2024-02-19', price: 52138.49 },
    { timestamp: '2024-02-20', price: 51764.31 },
    { timestamp: '2024-02-21', price: 52286.79 },
    { timestamp: '2024-02-22', price: 51842.76 },
    { timestamp: '2024-02-23', price: 51319.50 }
];
renderChart(sampleData); 
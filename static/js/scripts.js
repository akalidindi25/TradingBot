async function fetchCryptoData() {
    const response = await fetch('/cryptos');
    const data = await response.json();
    const tableBody = document.getElementById('crypto-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear existing data

    data.forEach(crypto => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = crypto.symbol.toUpperCase();
        row.insertCell(1).textContent = `$${crypto.current_price.toFixed(2)}`;
        row.insertCell(2).textContent = `${crypto['24h_change'].toFixed(2)}%`;
        row.insertCell(3).textContent = `$${crypto.market_cap.toLocaleString()}`;
    });
}

async function fetchStockData() {
    const response = await fetch('/stocks');
    const data = await response.json();
    const tableBody = document.getElementById('stock-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear existing data

    data.forEach(stock => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = stock.ticker;
        row.insertCell(1).textContent = `$${stock.current_price.toFixed(2)}`;
        row.insertCell(2).textContent = `$${stock.day_high.toFixed(2)}`;
        row.insertCell(3).textContent = `$${stock.day_low.toFixed(2)}`;
    });
} 
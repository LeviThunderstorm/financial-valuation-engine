document.addEventListener("DOMContentLoaded", () => {
    fetchHistory();

    document.getElementById("dcfForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            ticker: document.getElementById("ticker").value,
            share_price: parseFloat(document.getElementById("share_price").value),
            free_cash_flow: parseFloat(document.getElementById("free_cash_flow").value),
            growth_rate: parseFloat(document.getElementById("growth_rate").value),
            discount_rate: parseFloat(document.getElementById("discount_rate").value),
            shares_outstanding: parseFloat(document.getElementById("shares_outstanding").value)
        };

        try {
            const response = await fetch("/api/v1/valuation/dcf", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Valuation calculation failed");

            const data = await response.json();
            displayResult(data);
            fetchHistory(); // Refresh logs table
        } catch (error) {
            alert("Error connecting to analytics engine: " + error.message);
        }
    });
});

function displayResult(data) {
    const resultBox = document.getElementById("result");
    const badge = document.getElementById("resBadge");

    document.getElementById("resTicker").innerText = data.ticker;
    document.getElementById("resIntrinsic").innerText = `$${data.intrinsic_value.toFixed(2)}`;
    document.getElementById("resUpside").innerText = `${data.implied_upside_percent}%`;

    badge.innerText = data.status.replace("_", " ");
    badge.className = `badge ${data.status.replace(" ", "_")}`;

    resultBox.style.display = "block";
}

async function fetchHistory() {
    try {
        const response = await fetch("/api/v1/valuation/history");
        if (!response.ok) return;

        const logs = await response.json();
        const tbody = document.getElementById("historyTable");
        tbody.innerHTML = "";

        logs.forEach(log => {
            const row = document.createElement("tr");
            const statusClass = log.valuation_status.replace(" ", "_");
            row.innerHTML = `
                <td><strong>${log.ticker}</strong></td>
                <td>$${log.share_price.toFixed(2)}</td>
                <td>$${log.intrinsic_value.toFixed(2)}</td>
                <td><span class="badge ${statusClass}">${log.valuation_status}</span></td>
            `;
            tbody.appendChild(row);
        });
    } catch (e) {
        console.error("Failed to load history:", e);
    }
}
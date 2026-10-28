
async function loadDashboard() {
    try {
        // Get dashboard totals from the Flask backend
        const dashboardResponse = await fetch(
            "http://127.0.0.1:5000/api/dashboard"
        );
        const dashboardData = await dashboardResponse.json();

        document.getElementById("zones").textContent =
            dashboardData.active_zones;

        document.getElementById("people").textContent =
            dashboardData.people_affected;

        document.getElementById("resources").textContent =
            dashboardData.available_resources;

        // Get disaster zone details
        const zonesResponse = await fetch(
            "http://127.0.0.1:5000/api/zones"
        );
        const zones = await zonesResponse.json();
        
        // Draw or update the disaster priority chart
        const chartCanvas = document.getElementById("priorityChart");

        if (chartCanvas && window.Chart) {
            if (window.priorityChartInstance) {
                window.priorityChartInstance.destroy();
            }

            window.priorityChartInstance = new Chart(chartCanvas, {
                type: "bar",
                data: {
                    labels: zones.map(zone => zone.location),
                    datasets: [{
                        label: "Priority Score",
                        data: zones.map(zone => zone.priority),
                        backgroundColor: zones.map(zone => {
                            if (zone.priority >= 70) return "#dc3545";
                            if (zone.priority >= 40) return "#ffc107";
                            return "#198754";
                        }),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: "Priority (0–100)"
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: "Disaster Zone Priority Comparison"
                        }
                    }
                }
            });
        }


        const reportList = document.getElementById("report-list");
        reportList.innerHTML = "";

        zones.forEach((zone) => {
            const card = document.createElement("div");
            card.className = "report-card";

            card.innerHTML = `
                <h3>${zone.name}</h3>
                <p><strong>Location:</strong> ${zone.location}</p>
                <p><strong>Severity:</strong> ${zone.severity}</p>
                <p><strong>People affected:</strong> ${zone.people_affected}</p>
                <p><strong>Resources available:</strong> ${zone.resources_available}</p>
                <p><strong>Priority score:</strong> ${zone.priority}</p>
            `;

            reportList.appendChild(card);
        });
    } catch (error) {
        console.error("Could not load dashboard data:", error);
        alert(
            "Could not connect to the backend. Make sure the Flask server is running."
        );
    }
}

loadDashboard();

document.getElementById("disaster-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = document.getElementById("form-message");
    message.textContent = "Submitting report...";

    const report = {
        name: document.getElementById("zone-name").value.trim(),
        location: document.getElementById("zone-location").value.trim(),
        severity: document.getElementById("zone-severity").value,
        people_affected: Number(document.getElementById("people-affected").value),
        resources_available: Number(document.getElementById("resources-available").value)
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/api/zones", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(report)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not submit report");
        }

        message.textContent =
            `Report saved! Calculated priority: ${result.priority}`;

        document.getElementById("disaster-form").reset();
        await loadDashboard();
    } catch (error) {
        message.textContent = "Error: " + error.message;
    }
});

document.getElementById("load-allocation").addEventListener("click", async () => {
    const results = document.getElementById("allocation-results");
    results.textContent = "Loading recommendations...";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/allocate");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to load recommendations");
        }

        results.replaceChildren();

        data.recommendations.forEach(item => {
            const card = document.createElement("div");
            card.className = "allocation-card";

            const heading = document.createElement("h3");
            heading.textContent = item.zone;

            const location = document.createElement("p");
            location.textContent = "Location: " + item.location;

            const priority = document.createElement("p");
            priority.textContent = "Priority score: " + item.priority;

            const resources = document.createElement("p");
            resources.textContent =
                "Recommended resources: " + item.recommended_resources;

            card.append(heading, location, priority, resources);
            results.appendChild(card);
        });
    } catch (error) {
        results.textContent = "Error loading recommendations: " + error.message;
    }
});


async function loadWeather() {
    const details = document.getElementById("weather-details");

    try {
        const response = await fetch("http://127.0.0.1:5000/api/weather");

        if (!response.ok) {
            throw new Error("Weather API request failed");
        }

        const data = await response.json();
        const weather = data.current_weather;
        const units = data.units || {};

        details.replaceChildren();

        const fields = [
            ["Temperature", "temperature_2m"],
            ["Humidity", "relative_humidity_2m"],
            ["Precipitation", "precipitation"],
            ["Wind speed", "wind_speed_10m"]
        ];

        fields.forEach(([label, key]) => {
            const p = document.createElement("p");
            p.textContent = `${label}: ${weather[key] ?? "N/A"} ${units[key] || ""}`;
            details.appendChild(p);
        });

        document.getElementById("weather-location").textContent =
            "Current weather for Ludhiana (Open-Meteo)";
    } catch (error) {
        details.textContent = "Could not load weather. Check the Flask server and internet connection.";
    }
}

document.getElementById("refresh-weather").addEventListener("click", loadWeather);
loadWeather();


async function loadDisasterMap() {
    const mapElement = document.getElementById("disaster-map");
    const message = document.getElementById("map-message");

    if (!mapElement || !window.L) {
        if (message) message.textContent = "Map library did not load. Check your internet connection.";
        return;
    }

    // Approximate coordinates for common Indian locations
    const coordinates = {
        "ludhiana": [30.9010, 75.8573],
        "chandigarh": [30.7333, 76.7794],
        "delhi": [28.6139, 77.2090],
        "amritsar": [31.6340, 74.8723],
        "punjab": [31.1471, 75.3412]
    };

    const map = L.map(mapElement).setView([30.9, 75.8], 7);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 19
    }).addTo(map);

    try {
        const response = await fetch("http://127.0.0.1:5000/api/zones");

        if (!response.ok) {
            throw new Error("Could not retrieve disaster zones");
        }

        const zones = await response.json();
        const plottedPoints = [];

        zones.forEach(zone => {
            const locationKey = String(zone.location || "").trim().toLowerCase();
            const point = coordinates[locationKey];

            if (!point) return;

            plottedPoints.push(point);

            L.marker(point)
                .addTo(map)
                .bindPopup(
                    `<strong>${String(zone.name)}</strong><br>` +
                    `Location: ${String(zone.location)}<br>` +
                    `Severity: ${String(zone.severity)}<br>` +
                    `Priority: ${Number(zone.priority)}`
                );
        });

        if (plottedPoints.length > 0) {
            map.fitBounds(plottedPoints, { padding: [30, 30], maxZoom: 10 });
            message.textContent =
                `Showing ${plottedPoints.length} mapped disaster zone(s). Select a marker for details.`;
        } else {
            message.textContent =
                "No recognized locations to display. Add coordinates for your reported cities.";
        }

        setTimeout(() => map.invalidateSize(), 200);
    } catch (error) {
        message.textContent = "Could not load disaster locations. Check that Flask is running.";
    }
}

loadDisasterMap();




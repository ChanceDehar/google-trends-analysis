const map = L.map('map', {
    dragging: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false,
    zoomControl: false
}).setView([-41.2865, 174.7762], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

if (resultsData.top_region && resultsData.top_region.lat && resultsData.top_region.lng) {
    const marker = L.marker([resultsData.top_region.lat, resultsData.top_region.lng]).addTo(map);
    marker.bindPopup(`<b>${resultsData.top_region.name}</b><br>Highest search interest`).openPopup();
    
    map.setView([resultsData.top_region.lat, resultsData.top_region.lng], 7);
}
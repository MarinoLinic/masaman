document.addEventListener('DOMContentLoaded', function () {
	// Create the map
	var map = L.map('map').setView([0, 0], 2) // Adjust coordinates as needed

	// Load GeoJSON data
	fetch('map_data.geojson')
		.then((response) => response.json())
		.then((data) => {
			L.geoJSON(data, {
				style: function (feature) {
					return { color: 'black', fillColor: feature.properties.color, weight: 1 }
				},
				onEachFeature: function (feature, layer) {
					layer.bindPopup(`<b>${feature.properties.name}</b>`)
				},
			}).addTo(map)
		})

	// Add a tile layer for context (optional)
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; OpenStreetMap contributors',
	}).addTo(map)
})

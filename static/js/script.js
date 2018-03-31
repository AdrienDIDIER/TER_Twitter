/* Area location filter */
var map = L.map('map');
map.setView([43.6109200, 3.8772300], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
}).addTo(map);

var locationFilter = new L.LocationFilter().addTo(map);
var region_input = document.getElementById("region");

locationFilter.on("change", function (e) {
	var bounds = locationFilter.getBounds().toBBoxString();
    region_input.value = bounds;
});

function toast(text) {
	 return M.toast(text, 4000)
}
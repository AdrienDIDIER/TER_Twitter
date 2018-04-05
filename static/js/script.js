/* Area location filter */
if(document.getElementById('map') != null){
    var map = L.map('map');
    map.setView([45.5, 2], 4);

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
        region_input.value = locationFilter.getBounds().toBBoxString();
    });
}

/* Ajax Bouton start/stop */
$(document).ready(function () {
    $(document).on("click", '#start-stream_button', function () {
        $(this).prop("disabled", true);
        $('#stop-stream_button').prop("disabled", false);
        $.ajax({
            url: '/session/' + $(this).attr('action-target'),
            data: $('form').serialize(),
            type: 'POST',

            success: function (response) {
                /**/
            },
            error: function (error) {
               /**/
            }
        });
    });
    $(document).on("click", '#stop-stream_button', function () {
        $(this).attr("disabled", "disabled");
        $('#start-stream_button').prop("disabled", false);
        refresh_number_tweets();
        $.ajax({
            url: '/session/stream/stop',
            data: '',
            type: 'GET',

            success: function (response) {
                /**/
            },
            error: function (error) {
                /**/
            }
        });
    });

    window.setInterval(function () {
        if($('#start-stream_button').is(":disabled")){
            refresh_number_tweets();
        }
    }, 1000);
});

function refresh_number_tweets(){
    var target = $('#div_number_of_tweets');
    target.load(' #div_number_of_tweets', function () {
        target.fadeOut(1, function () {
            target.fadeIn(500);
        });
    });
}

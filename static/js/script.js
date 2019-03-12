/* Area location filter */
if (document.getElementById('map') != null) {
    var map = L.map('map');
    map.setView([45.5, 2], 4);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        id: 'mapbox.streets'
    }).addTo(map);

    var locationFilter = new L.LocationFilter().addTo(map);
    var region_input = document.getElementById("region");

    locationFilter.on("change", function (e) {
        region_input.value = locationFilter.getBounds().toBBoxString();
    });
}

/* Cartographie */
if (document.getElementById('mapid') != null) {
    map2 = L.map('mapid');
    map2.setView([51.505, -0.09], 2);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        id: 'mapbox.streets'
    }).addTo(map2);
}

function addMarker(marker){
    var latlng = L.latLng(marker.coordinates[1],marker.coordinates[0]);
    L.marker(latlng).addTo(map2);
}

function refresh_geo(){
    ajax_geolocalisation();
}

function refresh_download_btn() {
    var div = $('#div_download_btn'); // Ma div
    var btn = $('#download_btn'); // Mon bouton
    if (!btn.length) {
        div.load(' #div_download_btn', function () {
            div.fadeOut(1, function () {
                div.fadeIn(500);
            });
        });
    }
}

function refresh_number_tweets() {
    var target = $('#div_number_of_tweets');
    target.load(' #div_number_of_tweets', function () {
        target.fadeOut(1, function () {
            target.fadeIn(500);
        });
    });
}

$(function () {
    $('.session_card').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false
    });
});

$(function () {
    $('.card_interface').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false
    });
})

$(document).ready(function () {
    $('.tooltipped').tooltip({delay: 50});
});

function refresh_wordcloud(stream) {
    if (!stream) {
        $('#loading_circle').show();
        var wordcloud = $('#wordcloud');
        /* Si un wordcloud a déjà été généré */
        if (wordcloud.find('svg') !== 0) {
            wordcloud.find('svg').find("g").remove();
            /* Vide le wordcloud pour en accueillir un nouveau */
        }
    }

    ajax_wordcloud();
}

$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 2, // Creates a dropdown of 15 years to control year
    firstDay: 1,
    labelMonthNext: 'Mois suivant',
    labelMonthPrev: 'Mois précédent',
    labelMonthSelect: 'Selectionner le mois',
    labelYearSelect: 'Selectionner une année',
    monthsFull: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
    monthsShort: ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec'],
    weekdaysFull: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
    weekdaysShort: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
    weekdaysLetter: ['D', 'L', 'M', 'M', 'J', 'V', 'S'],
    today: 'Aujourd\'hui',
    clear: 'Réinitialiser',
    format: 'yyyy-mm-dd',
    onSet: function () {
        $('.picker__close').click();
    }
});

function refresh_histogram(first_load, value) {
    if (!first_load) {
        var histogram = $('#histogram');
        histogram.load(' #histogram', function () {
            histogram.fadeOut(1, function () {
                histogram.fadeIn(500);
            });
        });
    }
    ajax_freq_per_date(null, value);
}

$('.timepicker').pickatime({
    default: 'now', // Set default time: 'now', '1:30AM', '16:30'
    fromnow: 0,       // set default time to * milliseconds from now (using with default = 'now')
    twelvehour: false, // Use AM/PM or 24-hour format
    donetext: 'OK', // text for done-button
    cleartext: 'Clear', // text for clear-button
    canceltext: 'Cancel', // Text for cancel-button,
    container: undefined, // ex. 'body' will append picker to body
    autoclose: false, // automatic close timepicker
    ampmclickable: true, // make AM PM clickable
});


$(document).ready(function () {
    $('.modal').modal();
    $('select').material_select();
});

function load_containers() {
    $('#no_tweet_div').remove();
    $('#wordcloud_container').show();
    $('.progress').show();
    $('hr').show();
    $('.flow-text').show();
    $('#interaction_container').show();
    $('#histogram_area').show();
    $('#location_panel').show();

}

/* On vide le mini wordcloud et la liste des tweets */
function refresh_lw_tw() {
    $('#little-wordcloud').empty();
    $('#twitterwidget').empty();
}

$(document).on("click", '.smooth_scroll_btn', function () {
    switch ($(this).attr('data_id')) {
        case "general_wc":
            $('#wordcloud_container').show();
            $('#wordcloud_container').parent().nextAll('hr').first().show();
            document.getElementById('wordcloud_container').scrollIntoView({
                behavior: 'smooth'
            });
            break;
        case"histogram":
            $('#histogram_area').show();
            $('#histogram_area').parent().nextAll('hr').first().show();
            document.getElementById('histogram_area').scrollIntoView({
                behavior: 'smooth'
            });
            break;
        case "periode":
            document.getElementById('little-wordcloud').scrollIntoView({
                behavior: 'smooth'
            });
            break;
        case "location":
            $('#location_panel').show();
            $('#location_panel').parent().nextAll('hr').first().show();
            document.getElementById('location_panel').firstElementChild.scrollIntoView({
                behavior: 'smooth'
            });
            break;

    }

});

// Panel toolbox
$(document).ready(function() {
    $('.collapse-link').on('click', function() {
        var $BOX_PANEL = $(this).closest('.x_panel'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');

        // fix for some div with hardcoded fix class
        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function(){
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }
        switch($ICON.text()) {
            case "expand_more":
                $ICON.text("expand_less");
                break;
            case "expand_less":
                $ICON.text("expand_more");
                break;
        }
    });

    $('.close-link').click(function () {
        $(this).closest('.x_panel').parent().hide();
        $(this).closest('.x_panel').parent().parent().nextAll('hr').first().hide();
    });
});
// /Panel toolbox

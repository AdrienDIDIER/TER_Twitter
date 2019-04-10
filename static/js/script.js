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

    var southWest = L.latLng(-90, -180);
    var northEast = L.latLng(90, 180);

    var map2 = L.map('mapid', {
        maxBounds: L.latLngBounds(southWest, northEast),
        zoom: 1.5,
        maxZoom: 18,
        minZoom: 1.5,
        center: [0, 0],
        zoomSnap: 0.25,
    });
    map2.setView([51.505, -0.09], 1);

    lgMarkers = new L.LayerGroup();
    map2.addLayer(lgMarkers);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        id: 'mapbox.streets'
    }).addTo(map2);
}

if (document.getElementById('mapid2') != null) {

    var southWest = L.latLng(-90, -180);
    var northEast = L.latLng(90, 180);

    var map3 = L.map('mapid2', {
        maxBounds: L.latLngBounds(southWest, northEast),
        zoom: 1.5,
        maxZoom: 18,
        minZoom: 1.5,
        center: [0, 0],
        zoomSnap: 0.25,
    });
    map3.setView([51.505, -0.09], 1);

    lgMarkers2 = new L.LayerGroup();
    map3.addLayer(lgMarkers2);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        id: 'mapbox.streets'
    }).addTo(map3);
}


/* si on click sur + pour parameter */
$(document).on("click", '#session_parameter_button', function(){
    var param= '.'+$(this).val();
    if ($(param).is(":visible")){
        $(param).hide();
        $(this).children(":first").text("add");
    }
    else if ($(param).is(":hidden")) {
        $(param).show();
        $(this).children(":first").text("remove");
    }
});



function clearMarker(session) {
    if(!session){
        map2.invalidateSize();
        lgMarkers.clearLayers();
    }

}

function addMarker(marker,session) {
    if(session){
        if(session==1) {
            var latlng = L.latLng(marker.coordinates[1], marker.coordinates[0]);
            L.marker(latlng).addTo(lgMarkers).update();
        }
        if (session==2) {
            var latlng = L.latLng(marker.coordinates[1], marker.coordinates[0]);
            L.marker(latlng).addTo(lgMarkers2).update();
        }
    }
    else{
        var latlng = L.latLng(marker.coordinates[1], marker.coordinates[0]);
        L.marker(latlng).addTo(lgMarkers).update();
    }

}


function refresh_geo(session) {
    ajax_geolocalisation(session);
}

function refresh_sunburst(start,session){
    if(start){
        if(session!=null && session==2) {
            var pol = '#sunburst_panel' + session
            var polarity = $(pol);
            polarity.find('svg').remove();
            $('#loading_circle_sunburst2').show();
        }
        else {
            var polarity = $('#sunburst_panel');
            polarity.find('svg').remove();
            $('#loading_circle_sunburst').show();
        }
    }else{
        ajax_tweet_sunburst(session);
    }
}

function refresh_tweet_polarity(start,session){
    if(start){
        if(session!= null && session==2) {
            var pol = '#polarity_panel' + session
            console.log(pol);
            var polarity = $(pol);
            polarity.find('svg').remove();
            $('#loading_circle_polarity2').show();
        }
        else {
            var polarity = $('#polarity_panel');
            polarity.find('svg').remove();
            $('#loading_circle_polarity').show();
        }
    }else{
        ajax_tweet_polarity(session);
    }
}

function refresh_tweet_frequency_words(start,session){
    if(start){
        if(session!=null && session==2) {
            var pol = '#bar_char_panel' + session
            var polarity = $(pol);
            polarity.find('svg').remove();
            $('#loading_circle_bar_chart2').show();
        }
        else {
            var polarity = $('#bar_chart_panel');
            polarity.find('svg').remove();
            $('#loading_circle_bar_chart').show();
        }
    }else{
        ajax_tweet_frequency_words(session);
    }
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

$(document).ready(function verify() {
    var sessions = checkbox_sessions();
    var count = 0;
    var s_checked = [];

    for (var i = 0; i < sessions.length; i++) {
        s_checked[i]=0;
    }
    for (var i = 0; i < sessions.length; i++) {
        var id = sessions[i];
        document.getElementById(id).value = i;
        checkbox= document.getElementById(id);
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                s_checked[this.value] = 1;
                count++;
                console.log(s_checked);
            } else {
                s_checked[this.value] = 0;
                count--;
                console.log(s_checked);
            }

            if (count == 2) {
                document.getElementsByClassName("sessionsdouble")[0].style.visibility = "visible";
                var href = "/sessions";
                for(var i=0;i<s_checked.length;i++){
                    if(s_checked[i]==1){
                        href+="/"+sessions[i];
                    }
                }
                document.getElementById("doublesessions").href = href;
            } else {
                document.getElementsByClassName("sessionsdouble")[0].style.visibility = "hidden";
            }
        });
    }

});

function checkbox_sessions() {

    var sessions = [];
    $('.id_session').each(function () {
        sessions.push($(this).text());
    });
    return sessions;
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
    $('#polarity_panel').show();
    $('#bar_chart_panel').show();
    $('#sunburst_panel').show();

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
            $('#location_panel').each(function() {$(this).show()});
            $('#location_panel').parent().nextAll('hr').first().show();
            document.getElementById('location_panel').firstElementChild.scrollIntoView({
                behavior: 'smooth'
            });
            if($('#location_panel2').length){
                $('#location_panel2').show();
                $('#location_panel2').parent().nextAll('hr').first().show();
            }
            break;
        case "polarity":
            $('#polarity_panel').show();
            $('#polarity_panel').parent().nextAll('hr').first().show();
            document.getElementById('polarity_panel').firstElementChild.scrollIntoView({
                behavior: 'smooth'
            });
            if($('#polarity_panel2').length){
                $('#polarity_panel2').show();
                $('#polarity_panel2').parent().nextAll('hr').first().show();
            }
            break;
        case "bar_chart":
            $('#bar_chart_panel').show();
            $('#bar_chart_panel').parent().nextAll('hr').first().show();
            document.getElementById('bar_chart_panel').firstElementChild.scrollIntoView({
                behavior: 'smooth'
            });
            if($('#bar_chart_panel2').length){
                $('#bar_chart_panel2').show();
                $('#bar_chart_panel2').parent().nextAll('hr').first().show();
            }
            break;
        case "sunburst":
            $('#sunburst_panel').show();
            $('#sunburst_panel').parent().nextAll('hr').first().show();
            document.getElementById('sunburst_panel').firstElementChild.scrollIntoView({
                behavior: 'smooth'
            });
            if($('#sunburst_panel2').length){
                $('#sunburst_panel2').show();
                $('#sunburst_panel2').parent().nextAll('hr').first().show();
            }
            break;

    }

});

// Panel toolbox
$(document).ready(function () {
    $('.collapse-link').on('click', function () {
        var $BOX_PANEL = $(this).closest('.x_panel'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');

        // fix for some div with hardcoded fix class
        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function () {
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }
        switch ($ICON.text()) {
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



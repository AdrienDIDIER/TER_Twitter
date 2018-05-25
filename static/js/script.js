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

/* Ajax Bouton start/stop */
$(document).ready(function () {
    refresh_wordcloud(false);
    refresh_histogram(true);
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
                first_refresh = false;
            },
            error: function (error) {
                /**/
            }
        });
    });
    $(document).on("click", '#start-dated_tweets_button', function () {
        console.log("toto");
        var button_target = $(this);
        button_target.attr("disabled", "disabled");
        $('#loading_circle').show();
        $.ajax({
            url: '/session/' + button_target.attr('action-target'),
            data: '',
            type: 'POST',

            success: function (response) {
                refresh_number_tweets();
                refresh_wordcloud(false);
                refresh_histogram(false);
                button_target.prop("disabled", false);
            },
            error: function (error) {
                /**/
            }
        });

    });

    var first_refresh = false;

    window.setInterval(function () {
        var stream_button_pressed = $('#start-stream_button').is(":disabled");
        var datedtweets_button_pressed = $('#start-dated_tweets_button').is(":disabled");
        if (stream_button_pressed || datedtweets_button_pressed) {
            refresh_number_tweets();
            refresh_download_btn();
            if (!first_refresh) {
                first_refresh = true;
                refresh_wordcloud(true);
            }

            ajax_freq_per_date(function repeat() {
                if (datedtweets_button_pressed) {
                    $('#histogram').load(' #histogram', function () {
                        console.log("ok");
                        ajax_freq_per_date(repeat, null);
                    });
                }
            }, null);
        }
    }, 1000);

    /* A l'appui d'un intervalle pour l'histogramme */
    $('input[type=radio][name=time_interval]').change(function () {
        refresh_histogram(false, this.value);
    });
});

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
    $('.card').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false
    });
});

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

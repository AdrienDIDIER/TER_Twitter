$(document).ready(function () {
    refresh_wordcloud(false);
    refresh_histogram(true);
    /* Si l'on démarre un stream */
    $(document).on("click", '#start-stream_button', function () {
        $(this).prop("disabled", true);
        $('#stop-stream_button').prop("disabled", false);
        load_containers();

        $.ajax({
            url: '/session/' + $(this).attr('action-target'),
            data: $('form').serialize(),
            type: 'POST',

            success: function (response) {/**/},
            error: function (error) {/**/}
        });
    });

    /* Si l'on stop le stream */
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
            error: function (error) {/**/}
        });
    });

    /* Si l'on démarre un batch de tweets passés */
    $(document).on("click", '#start-dated_tweets_button', function () {
        var button_target = $(this);
        button_target.attr("disabled", "disabled");
        load_containers();
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
            error: function (error) {/**/}
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
                        ajax_freq_per_date(repeat, null);
                    });
                }
            }, null);
        }
    }, 1000);

    /* A l'appui d'un intervalle pour l'histogramme */
    $('input[type=radio][name=time_interval]').change(function () {
        refresh_histogram(false, this.value);
        /* On vide le mini wordcloud et la liste des tweets */
        $('#little-wordcloud').empty();
        $('#twitterwidget').empty();
    });
});
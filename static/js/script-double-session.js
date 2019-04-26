$(document).ready(function () {
    $.ajax({
        url: '/load_double_sessions/' + $('#session_target').attr('data-session'),
        data: '',
        type: 'GET',
        success: function (response) {/**/},
        error: function (error) {/**/}
    });

    setTimeout(function(){
        refresh_geo(1);
        refresh_tweet_polarity(false,1);
        refresh_tweet_frequency_words(false, 1);
        refresh_sunburst(false,1);
        session2_launch();
    }, 1000);
    function session2_launch(){
        setTimeout(function () {
            $.ajax({
                url: '/load_double_sessions/' + $('#session_target2').attr('data-session'),
                data: '',
                type: 'GET',
                success: function (response) {/**/},
                error: function (error) {/**/}
            });
        },1200);

        setTimeout(function(){
            refresh_geo(2);
            refresh_tweet_polarity(false,2);
            refresh_tweet_frequency_words(false,2);
            refresh_sunburst(false,2);
        }, 2000);

    }});

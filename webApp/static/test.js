$(document).ready(function() {
    var mymap = L.map('mapid').setView([51.505, -0.09], 13);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        accessToken: token
    }).addTo(mymap);

    $.ajax({
        type: 'GET',
        url: '/trips', 
        success: function(r) {
            let tripIDs = r.split(',');
            for(tripID of tripIDs) {
                $('#routes').append($('<option>', {
                    value: 1,
                    text: tripID
                }));
            }
        },
        error: function() {
          alert("Could not successfully reach server/trips")
        }
    });

    //listen for 'submit'
    $('.container').find('form').on('submit', function(event) {
        return false;
        // $.ajax({
        //     type: 'POST',
        //     url: '/tweets', 
        //     "data": $textbox,
        //     success: function() {
        //     $('main #tweetSection').html("")    // clear all html
        //     loadTweets()}                       // load tweets again
        //     // error: function() {     //sometimes problematic... remove?
        //     //   alert("Could not load tweets")}
        // })
    });
});

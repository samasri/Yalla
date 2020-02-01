$(document).ready(function() {
    var mymap = L.map('mapid').setView([43.8524, -79.4162], 11);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        accessToken: token
    }).addTo(mymap);

    $.ajax({
        type: 'GET',
        url: '/routes',
        success: function(r) {
            let routeIDs = JSON.parse(r);
            $('#routes').append($('<option>', {
                value: -1,
                text: "None"
            }));
            for(routeID of routeIDs) {
                $('#routes').append($('<option>', {
                    value: routeID.routeID,
                    text: routeID.routeID
                }));
            }
        },
        error: function() {
          alert("Could not successfully reach server/trips")
        }
    });

    var displayedMarkers = L.layerGroup().addTo(mymap);
    $("#routes").change (function(){
        $('#loading').show();
        $("#routes").hide();
        $("#mapid").hide();
        var routeID = $(this).children("option:selected").val();
        displayedMarkers.clearLayers();
        if(routeID != -1 ) {
            $.ajax({
                type: 'GET',
                url: '/stops/',
                data: {"routeID": routeID},
                success: function(coordinatesString) {
                    $('#loading').hide();
                    $("#routes").show();
                    $("#mapid").show();
                    let coordinates = JSON.parse(coordinatesString);
                    for(coordinate of coordinates) L.marker([coordinate.lat, coordinate.lon]).addTo(displayedMarkers);
                },
                error: function() {
                    $('#loading').hide();
                    $("#routes").show();
                    $("#mapid").show();
                    alert("Could not successfully reach server/stops")
                }
            });
        }
        return false;
    });
});

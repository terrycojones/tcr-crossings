var map,
    pinnedFeature = null,
    commentText = document.getElementById('comment-text');

var COUNTRY_NAME = {
    'AL': 'Albania',
    'AU': 'Austria',
    'BH': 'Bosnia Herzegovina',
    'BU': 'Bulgaria',
    'CR': 'Croatia',
    'GR': 'Greece',
    'HU': 'Hungary',
    'IT': 'Italy',
    'KO': 'Kosovo',
    'MA': 'Macedonia',
    'MO': 'Montenegro',
    'RO': 'Romania',
    'SE': 'Serbia',
    'SL': 'Slovenia',
    'TU': 'Turkey',
};

// Set map height manually on window resize.
$(window).resize(function () {
    var h = $(window).height(),
        offsetTop = 50;  // Navbar height.

    $('#map').css('height', (h - offsetTop));
}).resize();

// Below CSRF stuff from https://docs.djangoproject.com/en/1.9/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});
// Above CSRF stuff from https://docs.djangoproject.com/en/1.9/ref/csrf/

// From mustache.
var entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;'
  };

var escapeHtml = function (string){
    return String(string).replace(/[&<>"'\/]/g, function (s){
      return entityMap[s];
    });
};

var hideInfo = function(){
    document.getElementById('info').style.display = 'none';
    document.getElementById('info-overview').style.display = 'none';
    document.getElementById('info-comments').style.display = 'none';
};

var showInfo = function(){
    document.getElementById('info').style.display = 'block';
    showOverviewTab();
};

var showOverviewTab = function(){
    $('#crossing-tabs a[href="#overview"]').tab('show');
    document.getElementById('info-overview').style.display = 'block';
    document.getElementById('info-comments').style.display = 'none';
};

var showCommentsTab = function(){
    $('#crossing-tabs a[href="#comments"]').tab('show');
    document.getElementById('info-overview').style.display = 'none';
    document.getElementById('info-comments').style.display = 'block';
};

var enableCommentSubmit = function(){
    // $('#comment-submit').prop('disabled', false);
};

var disableCommentSubmit = function(){
    // $('#comment-submit').prop('disabled', true);
};

// Submit comments.
$('#comment-submit').click(function(e){
    e.preventDefault();

    if (!pinnedFeature){
        console.log('Comment submit clicked, but no crossing selected!');
        alert('Comment submit clicked, but no crossing selected!');
        return;
    }

    if (commentText.value === ''){
        console.log('Comment submit clicked, but no comment text.');
        return;
    }

    var crossingId = pinnedFeature.get('crossing').id;

    $.ajax('/crossings/' + crossingId + '/comment',
           {
               method: 'POST',
               data: {
                   crossingId: crossingId,
                   text: commentText.value,
               }
           })
        .done(function(){
            // Clear comment text area.
            var commentList = $('#comment-list'),
                li = $('<li>').addClass('comment');
            li.html(escapeHtml(commentText.value) +
                    '<div class="comment-date">' +
                    moment().fromNow() +
                    '</div>');
            commentList.prepend(li);
            // Clear the comment area.
            commentText.value = '';
        })
        .fail(function(){
            alert('Error submitting comment for crossing ' + crossingId);
        });
});

// Arrange to close the info box when its close button is clicked.
$('#close-info-comments').click(function(){
    pinnedFeature = null;
    hideInfo();
});

$('#close-info-overview').click(function(){
    pinnedFeature = null;
    hideInfo();
});

// Handle clicks on the Overview tab.
$('#crossing-tabs a[href="#overview"]').click(function (e) {
    e.preventDefault();
    showOverviewTab();
})


// Handle clicks on the Comments tab.
$('#crossing-tabs a[href="#comments"]').click(function (e) {
    e.preventDefault();
    showCommentsTab();

    if (!pinnedFeature){
        console.log('Comments tab clicked, but no crossing selected!');
        alert('Comment tab clicked, but no crossing selected!');
        return;
    }

    // Clear the comment box and set the Submit button to be disabled.
    //
    // TODO: Only do this when a new crossing is selected. That way we
    // let the user go back & forth between the overview & the comments
    // without wiping their text.
    commentText.value = '';
    disableCommentSubmit();

    var crossingId = pinnedFeature.get('crossing').id;
    $.ajax('/crossings/' + crossingId + '/comments.json')
        .done(populateComments)
        .fail(function(){
            alert('Error fetching comments for crossing ' + crossingId);
        });
})

var textChange = function(){
    if (commentText.value === ''){
        disableCommentSubmit();
    }
    else {
        enableCommentSubmit()
    }
};

// Handle textarea changes in the comment box.  See:
// http://stackoverflow.com/questions/2823733/textarea-onchange-detection
// and note that FF does not fire 'change' events in textareas, for some
// inexplicable reason.
if (commentText.addEventListener) {
    commentText.addEventListener('input', function() {
        // event handling code for sane browsers
        textChange();
    }, false);
} else if (commentText.attachEvent) {
    commentText.attachEvent('onpropertychange', function() {
        // IE-specific event handling code
        textChange();
    });
}


var populateComments = function(comments){
    var i, comment, li;
    var commentList = $('#comment-list');
    commentList.children().remove();

    for (i = 0; i < comments.length; i++){
        comment = comments[i];
        li = $('<li>').addClass('comment');
        li.html(escapeHtml(comment.fields.text) +
                '<div class="comment-date">' +
                moment(comment.fields.lastUpdate).fromNow() +
                '</div>');
        commentList.prepend(li);
    }
};

var updateInfo = function(feature){

    var crossing = feature.get('crossing');
    var attrs = [
        'name', 'countryFrom', 'countryTo', 'countryFromPlace', 'countryToPlace',
        'bikeCrossing', 'crossingType', 'hours', 'latitude', 'longitude', 'notes',
        'otherNames'
    ];
    var i, element, attr, value;

    for (i = 0; i < attrs.length; i++){

        attr = attrs[i];
        element = document.getElementById('crossing-' + attr);
        if (element){
            value = crossing[attr];
            if (value){
                element.innerHTML = value;
            }
            else {
                element.innerHTML = '';
            }
        }
        else {
            console.log('Could not find doc element with id', attr);
        }
    }

    // Show the Overview tab.
    showOverviewTab();

    // Set the crossing name in the comments tab.
    element = document.getElementById('crossing-name-in-comments');
    element.innerHTML = crossing.name;
};

var handleMouseEvent = function(pixel, clicked){
    var feature = map.forEachFeatureAtPixel(pixel, function(feature){
        return feature;
    });

    if (feature){
        if (pinnedFeature){
            if (feature === pinnedFeature){
                if (clicked){
                    // User clicked on the feature that's currently pinned.
                    // Hide it.
                    pinnedFeature = null;
                    hideInfo();
                }
                else {
                    // This is a mouseover of the currently pinned feature.
                    // Do nothing.
                }
            }
            else {
                // Different feature.
                if (clicked){
                    // User clicked on a different feature than the one
                    // that's currently pinned.
                    updateInfo(feature);
                    pinnedFeature = feature;
                }
                else {
                    // This is a mouseover of a different feature when we
                    // have a pinned feature.  Do nothing.
                }
            }
        }
        else {
            // No feature is pinned.
            if (clicked){
                // User clicked on a feature. Pin it.
                pinnedFeature = feature;
            }
            updateInfo(feature);
            showInfo();
        }
    }
    else {
        // No feature under mouse. Hide the info, unless it's pinned.
        if (!pinnedFeature){
            hideInfo();
        }
    }
};

var addCrossings = function(crossings){
    var i, features = [];

    for (i = 0; i < crossings.length; i++){
        var crossing = crossings[i].fields;
        var width = 5;
        var white = [255, 255, 255, 1];
        var blue = [0, 153, 255, 1];
        var feature = new ol.Feature({
            geometry: new ol.geom.Point(
                ol.proj.fromLonLat([crossing.longitude, crossing.latitude]))
        });

        // Store the id of the crossing.
        crossing.id = crossings[i].pk;

        // Change country abbrevs to country names.
        crossing.countryFrom = COUNTRY_NAME[crossing.countryFrom];
        crossing.countryTo = COUNTRY_NAME[crossing.countryTo];
        
        feature.setStyle(new ol.style.Style({
            image: new ol.style.Circle({
                radius: width * 2,
                fill: new ol.style.Fill({
                    color: blue
                }),
                stroke: new ol.style.Stroke({
                    color: white,
                    width: width / 2
                })
            }),
            zIndex: Infinity
        }));

        feature.set('crossing', crossing, true);

        features[i] = feature;
    }

    var vectorSource = new ol.source.Vector({
        features: features
    });

    var vectorLayer = new ol.layer.Vector({
        source: vectorSource
    });

    /*
    // Mapbox silly old-fashioned map.
    var rasterLayer = new ol.layer.Tile({
        source: new ol.source.TileJSON({
            url: 'http://api.tiles.mapbox.com/v3/mapbox.geography-class.json',
            crossOrigin: ''
        })
    });
    */

    /*
    This is the originally deployed (ugly) OSM site:

    var rasterLayer = new ol.layer.Tile({
        // Vanilla OSM doesn't look as good (to me) as MapQuest.
        // source: new ol.source.MapQuest({layer: 'osm'})
        // but MapQuest just changed (July 12 2016) to be non-free!
        source: new ol.source.OSM()
    });
    */

    var mapboxToken = 'pk.eyJ1IjoidGVycnljb2pvbmVzIiwiYSI6ImNpcjl4ZnllZzAwNGNpZmx3YmY3dXVxNGIifQ.4ybBGHp3Zoqs-5I-tqXxJw';
    var rasterLayer = new ol.layer.Tile({
        source: new ol.source.XYZ({
            tileSize: [512, 512],
            // I tried outdoors-v9 but the map does not display initially, it's necessary to zoom.
            // I don't know why. But streets-v9 works fine.
            url: ('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{z}/{x}/{y}?access_token=' +
                  mapboxToken)
        })
    });

    map = new ol.Map({
        target: 'map',
        // logo: false,
        layers: [rasterLayer, vectorLayer],
        view: new ol.View({
            center: ol.proj.fromLonLat([16.372778, 48.209206]), // Vienna
            zoom: 5.5
        })
    });

    map.on('pointermove', function(evt){
        if (evt.dragging){
            return;
        }
        var pixel = map.getEventPixel(evt.originalEvent);
        handleMouseEvent(pixel, 0);
    });

    map.on('click', function(evt){
        handleMouseEvent(evt.pixel, 1);
    });
};

$.ajax('/crossings/')
    .done(addCrossings)
    .fail(function(){
        alert('Error fetching crossings data.');
    });

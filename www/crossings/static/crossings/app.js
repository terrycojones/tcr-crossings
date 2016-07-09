var map,
    pinnedFeature = null,
    commentText = document.getElementById('comment-text');

var hideInfo = function(){
    document.getElementById('info').style.display = 'none';
    document.getElementById('info-overview').style.display = 'none';
    document.getElementById('info-comments').style.display = 'none';
};

var showInfo = function(){
    document.getElementById('info').style.display = 'block';
    document.getElementById('info-overview').style.display = 'block';
    document.getElementById('info-comments').style.display = 'none';
};

var enableCommentSubmit = function(){
    // $('#comment-submit').prop('disabled', false);
};

var disableCommentSubmit = function(){
    // $('#comment-submit').prop('disabled', true);
};

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
    $(this).tab('show');
    document.getElementById('info-overview').style.display = 'block';
    document.getElementById('info-comments').style.display = 'none';
})


// Handle clicks on the Comments tab.
$('#crossing-tabs a[href="#comments"]').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
    document.getElementById('info-overview').style.display = 'none';
    document.getElementById('info-comments').style.display = 'block';

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

    for (i = 0; i < comments.length; i++){
        comment = comments[i];
        console.log('populateComments loop:', comment);
        li = $('<li>').addClass('comment');
        li.text(comment.fields.text);
        commentList.append(li);
    }
    console.log('populateComments', comments);
};

var updateInfo = function(feature){

    var crossing = feature.get('crossing');
    var attrs = [
        'name', 'country1', 'country2', 'country1Place', 'country2Place',
        'active', 'bikeCrossing', 'crossingType', 'hours', 'latitude',
        'longitude', 'notes', 'otherNames', 'tcr4Survey'
    ];
    var i, element, attr;

    for (i = 0; i < attrs.length; i++){

        attr = attrs[i];
        element = document.getElementById('crossing-' + attr);
        if (element){
            element.innerHTML = crossing[attr];
        }
        else {
            console.log('Could not find doc element with id', attr);
        }
    }
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

var addCrossings = function(data){
    var crossings = data.crossings;
    var i;
    var features = [];

    for (i = 0; i < crossings.length; i++){
        var crossing = crossings[i];
        var width = 5;
        var white = [255, 255, 255, 1];
        var blue = [0, 153, 255, 1];
        var feature = new ol.Feature({
            geometry: new ol.geom.Point(
                ol.proj.fromLonLat([crossing.longitude, crossing.latitude]))
        });
        
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

    var rasterLayer = new ol.layer.Tile({
        // ol.source.MapQuest() looks better but doesn't work, as ol.js
        // references an unknown variable (c).
        source: new ol.source.OSM()
    });

    /*

    // Mapbox!
    var rasterLayer = new ol.layer.Tile({
        source: new ol.source.TileJSON({
            url: 'http://api.tiles.mapbox.com/v3/mapbox.geography-class.json',
            crossOrigin: ''
        })
    });
    */

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

$.ajax('/static/crossings/crossings.json')
    .done(addCrossings)
    .fail(function(){
        alert('Error fetching crossings data.');
    });

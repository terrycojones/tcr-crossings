var map,
    pinnedFeature = null;

var hideInfo = function(){
    document.getElementById('info').style.visibility = 'hidden';
};

var showInfo = function(){
    document.getElementById('info').style.visibility = 'visible';
};

// Arrange to close the info box when its close button is clicked.
$('#close-info').click(function(){
    pinnedFeature = null;
    hideInfo();
});

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
        source: new ol.source.OSM()
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

var jqxhr = $.ajax('/static/crossings/crossings.json')
    .done(function(data){
        addCrossings(data);
    })
    .fail(function(){
        alert('Error fetching crossings data.');
    });

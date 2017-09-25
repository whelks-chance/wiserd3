// global namespace
var DataPortal = DataPortal || {};

function UnavailableFunctionError(message) {
    this.name = 'MyError';
    this.message = message || 'Default Message';
    this.stack = (new Error()).stack;
}
UnavailableFunctionError.prototype = Object.create(Error.prototype);
UnavailableFunctionError.prototype.constructor = UnavailableFunctionError;


DataPortal.tpt = 'can';
DataPortal.use_welsh = false;

// TODO populate this
DataPortal.translation = {};
DataPortal.translation.current_language = 'en';
DataPortal.translation._translate = function(phrase, opts){
    return phrase;
};
DataPortal.translation.translate = function(phrase, opts){
    opts = opts || {};
    opts.lang = opts.lang || DataPortal.translation.current_language;
    // if(!opts.lang){
    //     opts['lang'] = DataPortal.translation.current_language;
    // }
    return DataPortal.translation._translate(phrase, opts);
};
//shortcut
var trans = DataPortal.translation.translate;

DataPortal.django = {};
// TODO populate with request object from context
DataPortal.django.request = {};
DataPortal.django.request.user = {};
DataPortal.django.request.user.is_superuser = {};

DataPortal.django._url_dict = {};
DataPortal.django.extra_urls = function(name, args){
    throw new UnavailableFunctionError('extra_urls was not defined');
};
DataPortal.django.urls = function(name, args){
    args = args || {};
    if(DataPortal.django._url_dict[name]) {
        return DataPortal.django._url_dict[name]
    } else {
        DataPortal.django.extra_urls(name, args);
    }
};

DataPortal.django.add_urls = function(new_urls_dict){
    for (var attrname in new_urls_dict) {
        DataPortal.django._url_dict[attrname] = new_urls_dict[attrname];
    }
};


DataPortal.django.static_urls = function(name, args){
    args = args || {};
    return '/static/' + name;
};

DataPortal.mapping = {};
DataPortal.mapping.north_arrow = function(){
    return DataPortal.use_welsh? 'G' : 'N';
};
DataPortal.mapping.opacity = function(){
    switch (this.tpt) {
        case 'naw':
            return 1;
        default:
            return 0.7
    }
};
DataPortal.mapping.colour_scheme = function(name){
    switch (name) {
        case 'naw':
            return ['ffd2e8', 'hotpink', '4c1f36'];
        case 'WISERD':
            return ['cbb4cd', '54075b', '2a032d'];
        case 'b_w':
            return ['white', 'black'];
        case 'pink':
            return ['lightpink', 'pink', 'hotpink', 'deeppink'];
        case 'w':
            return ['white', 'white'];

        default:
            return ['ffd2e8', 'hotpink', '4c1f36'];
    }
};

DataPortal.mapping.geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

DataPortal.mapping.topojson_geographies = function(){
//    Todo ajax them, or grab from template
//    Todo Store after first pull so only ajax'd once
//    build a list of these objects {
//     'geog_short_code': "{{ geography.geog_short_code }}",
//     'name': "{{ geography.name }}" }
};
DataPortal.mapping.local_data_layers = function(){
//    Todo ajax them, or grab from template
};
DataPortal.mapping.layer_uuids = function(){
//    Todo from template
};
DataPortal.mapping.remote_searches = function(){
//    Todo from template
};
DataPortal.mapping.remote_data_layers = function(){
//    Todo from template
};

DataPortal.util = {
    guid: {
        uid: 0,
        next_uid: function() {
            DataPortal.util.guid.uid += 1;
            return DataPortal.util.guid.uid;
        }
    },
    resetFormElement: function(e) {
        e.wrap('<form>').closest('form').get(0).reset();
        e.unwrap();
    }
};

DataPortal.mapping.gui = {
    show_sidebar: function() {
        this.right_sidebar.show();
        this.right_sidebar_col.css({'width': '25%'});
        this.map_div_col.css({'width': '75%'});
        this.show_right_sidebar_btn.hide();
        this.hide_right_sidebar_btn.show();
    },
    hide_sidebar: function() {
        this.right_sidebar.hide();
        this.right_sidebar_col.css({'width': '4em'});
        this.map_div_col.css({'width': 'calc(100% - 4em'});
        this.hide_right_sidebar_btn.hide();
        this.show_right_sidebar_btn.show();
    },
    init: function(){
        $('.nav-ul').each(function(i, obj) {
            // here "this" refers to each of the nav-ul items, not DataPortal.mapping.gui
            $(this).metisMenu();
        });
        this.show_right_sidebar_btn = $('#show_right_sidebar');
        this.hide_right_sidebar_btn = $('#hide_right_sidebar');
        this.right_sidebar = $('#right_sidebar');
        this.right_sidebar_col = $('#right_sidebar_col');
        this.map_div_col = $('#map_div_col');
        // bind function to this object so we can get the variables we just set
        // otherwise "this" in the functions above refers to the button clicked
        this.hide_right_sidebar_btn.click(this.hide_sidebar.bind(this));
        this.show_right_sidebar_btn.click(this.show_sidebar.bind(this));
        this.show_right_sidebar_btn.hide();
    }
};

// {#            L.CRS.EPSG4326;#}
DataPortal.mapping.map = {
    wkt: '',
    center_lat_lng: '',
    search_area_geojson: '',
    geoJson_area_km2: '',

    map_height: 0,
    header_height: 0,
    map: null,

    init: function(){
        this.map_height = window.innerHeight;
        this.header_height = $('.navbar-header').height();

        var view_point = [52.4, -3.51];
        var view_zoom = 8;
        if (DataPortal.tpt === 'can'){
            view_point = [65.4, -100.51];
            view_zoom = 3;
        }

        this.map_div = $('#map_div');
        this.map_div.css({
            height: this.map_height - this.header_height - 5
        });

        DataPortal.mapping.gui.right_sidebar.css({
            height: this.map_height - this.header_height - 5
        });
        this.map = L.map('map_div',
            {crs: L.CRS.EPSG3857}
            ).setView(view_point, view_zoom);

        this.hash = new L.Hash(this.map);
    },
    decorate: function(){
        this.powered_by = L.control({position: "topright"});
        this.powered_by.onAdd = function(map) {
            var div = L.DomUtil.create("div", "powered_by");
            div.innerHTML = "<a target='_blank' href=" + DataPortal.django.urls('dashboard') + "><div class='powered_txt'>" + trans('Powered by the WISERD Dataportal') + "</div></a>";
            return div;
        };
        this.powered_by.addTo(this.map);

        L.easyPrint({
            title: trans("Print and download"),
            position: 'topleft',
            // {#                sizeModes: "native",#}
            sizeModes: ['CurrentSize', 'A4Landscape', 'A4Portrait']
            // {#        elementsToHide: 'right_sidebar_col, h2'#}
        }).addTo(this.map);

        this.layer_group = new L.LayerGroup();

        this.add_tilelayers.apply(this);
    },
    tilelayers: {},
    add_tilelayers: function() {
        console.log('add_tilelayers');
        console.log(this);

        // This has to be a function, because django urls must be loaded first.
        this.tilelayers.openstreetmap = L.tileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                // {#            L.tileLayer('http://i7.cscloud.cf.ac.uk/osmcarto/{z}/{x}/{y}.png?access_token={accessToken}', {#}
                // {#                        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',#}
                attribution: '<a target="_blank" href="' + DataPortal.django.urls('licence_attribution') + '">Licence & attribution</a> | Map data &copy; <a target="_blank" href="http://openstreetmap.org">OpenStreetMap</a> | Contains Ordnance Survey, Office of National Statistics and National Records Scotland data © Crown copyright and database right [2014]. Ordnance Survey data covered by OS OpenData Licence. Any further sub-licences must retain this attribution.',
                // {#                        maxZoom: 15,#}
                id: 'your.mapbox.project.id',
                accessToken: 'your.mapbox.public.access.token',
                maxZoom: 20,
                maxNativeZoom: 18
            });
        this.tilelayers.openstreetmap.addTo(DataPortal.mapping.map.map);

        this.tilelayers.openstreetmap_bw = L.tileLayer(
            'https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
            {
                attribution: '<a target="_blank" href="' + DataPortal.django.urls('licence_attribution') + '">Licence & attribution</a> | Map data &copy; <a target="_blank" href="http://openstreetmap.org">OpenStreetMap</a>',
                maxZoom: 20,
                id: 'your.mapbox.project.id',
                accessToken: 'your.mapbox.public.access.token'
            });


        this.layers_config = {
            'OpenStreetMap': this.tilelayers.openstreetmap,
            'BW': this.tilelayers.openstreetmap_bw
        };


        this.autolayers_config = {
            overlays: [], //custom overlays group that are static
            baseLayers: this.layers_config, //custom baselayers group that are static
            selectedBasemap: 'Streets', //selected basemap when it loads
            selectedOverlays: ["ASTER Digital Elevation Model 30M", "ASTER Digital Elevation Model Color 30M", "Cities"], //which overlays should be on by default
            mapServers: []
        };

        this.layerControl = L.control.autolayers(
            this.autolayers_config
        ).addTo(this.map);

        this.scale = L.control.scale().addTo(this.map);

        this.north = L.control({position: "bottomleft"});
        this.north.onAdd = function(map) {
            this._div = L.DomUtil.create("div", "north_arrow");
            this._div.innerHTML = DataPortal.mapping.north_arrow() + '<br><i class="fa fa-long-arrow-up arrow_center"></i>';
        return this._div;
        };
        this.north.addTo(this.map);

        this.info = L.control();
        this.info.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };
    },
    update_info: function(props) {
        // method that we will use to update the control based on feature properties passed
        console.log(props);
        if (props == null) {
            // {#                    console.log('empty props');#}

            $('#right-component1').html('');
        }
        var value = '';
        if (props) {
            if (props.hasOwnProperty('response_rate')) {
                value = props.response_rate;
            }
            else if (props.hasOwnProperty('REMOTE_VALUE')) {
                value = props.REMOTE_VALUE;
            } else {

                var cleanedprops = JSON.parse(JSON.stringify(props));
                delete cleanedprops['STRING_DATA'];
                delete cleanedprops['model'];

                // {#                        cleanedprops['STRING_DATA'] = null;#}
                // {#                        cleanedprops['model'] = null;#}
                var ppTable = prettyPrint(cleanedprops);
                // {#                        value += JSON.stringify(props);#}
                value = $(ppTable).prop('outerHTML')
            }
        }
        var info_text = '<div style="min-height: 10%">';
        if (props) {

            var header_title = '';

            if (props.DATA_TITLE) {
                header_title = props.DATA_TITLE;
            } else {
                header_title = DataPortal.translation.translate('Region_Data');
            }

            if (DataPortal.use_welsh) {
                if (props.DATA_TITLE_ALT1) {
                    header_title = props.DATA_TITLE_ALT1;
                }
            }

            info_text += '<h3>' + header_title + '</h3>';

            if (props.NAME) {
                info_text += '<h4>' + props.NAME + '</h4>';
            }
            // {# Only show alt name it it isn't the same as 'name' #}
            if (props.ALTNAME) {
                if (props.NAME) {
                    if (props.NAME != props.ALTNAME) {
                        info_text += '<h4>' + props.ALTNAME + '</h4>';
                    }
                } else {
                    info_text += '<h4>' + props.ALTNAME + '</h4>';
                }
            } else if (props.NameWelsh) {
                if (props.NAME) {
                    if (props.NAME != props.NameWelsh) {
                        info_text += '<h4>' + props.NameWelsh + '</h4>';
                    }
                } else {
                    info_text += '<h4>' + props.NameWelsh + '</h4>';
                }
            }
            info_text += '<p><b>' + trans('Total') + ' : </b>' + (value + (props.PERCENTAGE == true ? '%' : '')) + '</p>';

            if (props.DATA_GLOBAL_AVERAGE) {
                info_text += '<p><b>' + trans('Global Average') + '</b> : ' + props.DATA_GLOBAL_AVERAGE + '</p>';
            }

            var groups = {};

            if (props.STRING_DATA) {
                var strings = '';
                for (var item in props.STRING_DATA) {
                    if (props.STRING_DATA[item]['grouping']) {
                        if (groups.hasOwnProperty(props.STRING_DATA[item]['grouping'])) {
                            groups[props.STRING_DATA[item]['grouping']]['list'].push(
                                get_sidebar_text(props, item)
                            )
                        } else {
                            groups[props.STRING_DATA[item]['grouping']] = {
                                'title': props.STRING_DATA[item]['grouping'],
                                'list': [get_sidebar_text(props, item)]
                            }
                        }
                    } else {
                        strings += get_sidebar_text(props, item);
                    }
                }

                for (var group in groups) {
                    strings += '<div class="sidebar_group">';
                    for (var item_field in groups[group]['list']) {
                        strings += groups[group]['list'][item_field];
                    }
                    strings += '</div>';
                }

                info_text += strings;
            } else {
                // {#                        info_text += '<h4>Hover over a region</h4>';#}
            }

            if (DataPortal.django.request.user.is_superuser) {
                if (props.SEARCH_UUID) {
                    info_text += '<a target="_blank" ' +
                        'href="' + DataPortal.django.urls('search_data', {0: props.SEARCH_UUID}) + 'Search layer data</a>';
                }
            }


            info_text += '</div>';
            // {#                FIXME this is nuts #}
            // {#                this._div.innerHTML = info_text;#}
            var right_pane = $('#right-component1');
            right_pane.html(info_text);

            if (props.SEARCH_UUID) {
                right_pane.append(
                    $('<div/>')
                        .addClass('btn btn-info')
                        .text('Download Dataset')
                        .on('click', function () {
                            var dl_link = DataPortal.django.urls('download_dataset_zip') + '?dataset_id=' + props.SEARCH_UUID;
                            window.open(dl_link, '_blank');
                        })
                );
            }


        }
    },
    addLegend: function(unique_layer_name_text, layer_name_text, contentHTML, search_uuid){

        // {#                var a_uid = get_next_uid();#}
        // {#                var tab_id = ("collapse_" + a_uid + '_' + div_id).replace(/\W/g, '');#}
        var tab_id = ("collapse_" + unique_layer_name_text).replace(/\W/g, '');
        var accordionInner = $('<div/>')
            .attr('id', 'accordion_inner_' + tab_id)
            .attr('search_uuid', search_uuid)
            .addClass("panel panel-default")
            .append(
                $('<div/>')
                    .addClass("panel-heading")
                    .append(
                        $('<h4/>')
                            .addClass("panel-title")
                            .append(
                                $('<a/>')
                                    .attr('data-toggle', "collapse")
                                    .attr('data-parent', "#legend_accordion")
                                    .attr('href', "#" + tab_id)
                                    .text(layer_name_text)
                            )
                    )
            )
            .append(
                $('<div/>')
                    .attr('id', tab_id)
                    .addClass("panel-collapse collapse in")
                    .append(
                        $('<div/>')
                            .addClass("panel-body")
                            .wrapInner(contentHTML)
                    )
            ).append($('<div/>').attr('id', 'findme_' + search_uuid).attr('find_me', search_uuid));
        var accordionDiv = $('#legend_accordion');
        $(accordionDiv).append(accordionInner);
    }
};


DataPortal.mapping.LayerStore = {
    layers: [],
    wms_layers: {},

    add_layer: function(layer) {
        console.log('adding layer');
        console.log(layer);

        this.layers.push(layer);
    },

    number_of_layers: function() {
        return this.layers.length;
    },

    get_layer: function(uid) {
        for (var i = 0; i < layer.length; i++) {
            if (DataPortal.mapping.LayerStore.layers[i].layer_uid == uid) {
                return this.layers[i];
            }
        }
        return null;
    },
    toggle_layer: function(toggle_button) {

        console.log('this');
        console.log(this);
        console.log('toggle_button');
        console.log(toggle_button);
        var btn_layer_name = $(toggle_button).data('layer_name');

        // // {#                Remove the class regardless what's about to happen, can be added back again #}
        $(toggle_button).removeClass('wms_layer_active');
        if (this.wms_layers.hasOwnProperty(btn_layer_name)) {
            map.removeLayer(this.wms_layers[btn_layer_name]);
            delete this.wms_layers[btn_layer_name];
        } else {
            var btn_layer_url = $(toggle_button).data('layer_url');

            $(toggle_button).addClass('wms_layer_active');
            var legend_url = $(toggle_button).data('legend_img');
            if (legend_url) {
                DataPortal.mapping.map.addLegend(btn_layer_name + '_' + DataPortal.util.guid.next_uid(), btn_layer_name, '<img src="' + legend_url + '" style="width:100%; max-width:8em !important">', '');
            }

            // // {#                    var inspire = L.tileLayer.wms("http://inspire.wales.gov.uk/maps/wms", {#}
            var inspire = L.tileLayer.wms(btn_layer_url, {
                layers: btn_layer_name,
                format: 'image/png',
                transparent: true,
                attribution: "wales.gov"
            });
            inspire.addTo(DataPortal.mapping.map.map);
            DataPortal.mapping.map.layerControl.addOverlay(inspire, btn_layer_name + '-wms');
            this.wms_layers[btn_layer_name] = inspire;
            inspire.addTo(DataPortal.mapping.map.map);


            try {
                var wfs = $(toggle_button).data('wfs');
                var typeNS = $(toggle_button).data('wfs_namespace');
                var geometryFields = $(toggle_button).data('wfs_geometry_field');

                if (wfs && typeNS && geometryFields) {

                    var geometryFieldsArr = geometryFields.split(',');
                    // {#                            for (var geometryIdx in geometryFieldsArr) {#}
                    try {

                        var wfst = new L.WFST({
                            url: btn_layer_url,
                            typeNS: typeNS,
                            typeName: btn_layer_name,
                            // {#                                        geometryField: geometryFieldsArr[geometryIdx],#}
                            geometryField: 'fme_geometry',
                            crs: epsg27700,
                            style: {
                                color: 'blue',
                                weight: 2
                            }
                        });

                        wfst.addTo(map).once('load', function () {
                            map.fitBounds(wfst);
                        });
                        DataPortal.mapping.map.layerControl.addOverlay(wfst, btn_layer_name + '-wfs');

                        wfst.on('click', function (e) {
                            console.log('click');
                            console.log(e.layer.feature);

                            var right_pane = $('#right-component1');

                            var ppTable = prettyPrint(e.layer.feature);
                            right_pane.empty().append($(ppTable));

                        });

                    } catch (e) {
                        console.log('Failed wfs geometryfield = fme_geometry');
                        console.log(e);
                    }
                }
            }catch (e){
                console.log('wfs fail');
                console.log(e);
            }
        }
    }

};
//shortcut
// var store = DataPortal.LayerStore;

DataPortal.mapping.MapLayer = {
    layer_uid: '',
    geography_id: '',
    dataset_id: '',
    codelist: {},
    topojson_data: null,
    topojson_layer: null,
    colorpicker: null,
    color_scheme: '',
    bin_type: '',
    num_bins: 0,
    name: '',
    nomis_variable: '',
    is_percentage: false,
    suppressed_data: null,
    csv_url: '',
    feature_data: [],
    feature_string_data: [],
    legend: null
};

window.ready = function(){
};

$(document).ready(function () {
    // console.log('django init calling');
    // DataPortal.django.init();

    DataPortal.mapping.gui.init();

    console.log('map init calling');
    DataPortal.mapping.map.init();

    console.log('decorate called');
    DataPortal.mapping.map.decorate();


    var epsg27700 = new L.Proj.CRS("EPSG:27700","+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489 +units=m +no_defs");


    // var hide_right_sidebar_btn = $('#hide_right_sidebar');
    // var show_right_sidebar_btn = $('#show_right_sidebar');
    // show_right_sidebar_btn.hide();
    //
    // hide_right_sidebar_btn.click(DataPortal.mapping.gui.hide_sidebar());
    //
    // show_right_sidebar_btn.click(DataPortal.mapping.gui.show_sidebar());
    // function show_sidebar() {
    //     $('#right_sidebar').show();
    //     $('#right_sidebar_col').css({'width': '25%'});
    //     $('#map_div_col').css({'width': '75%'});
    //     show_right_sidebar_btn.hide();
    //     hide_right_sidebar_btn.show();
    // }
    //
    // function hide_sidebar() {
    //     $('#right_sidebar').hide();
    //     $('#right_sidebar_col').css({'width': '4em'});
    //     $('#map_div_col').css({'width': 'calc(100% - 4em'});
    //     hide_right_sidebar_btn.hide();
    //     show_right_sidebar_btn.show();
    // }



    // // {# FIXME sigh, why are there 4 things here?? #}

    // a dict holding names and objects for wms layers currently on the map
    var wms_layers = {};

    var topojson_layers = {};

    var leaflet_layers = [];
    var layer_name_counter = {};


    function toggle_layer(toggle_button) {
        var btn_layer_name = $(toggle_button).data('layer_name');

        // // {#                Remove the class regardless what's about to happen, can be added back again #}
        $(toggle_button).removeClass('wms_layer_active');
        if (wms_layers.hasOwnProperty(btn_layer_name)) {
            map.removeLayer(wms_layers[btn_layer_name]);
            delete wms_layers[btn_layer_name];
        } else {
            var btn_layer_url = $(toggle_button).data('layer_url');

            $(toggle_button).addClass('wms_layer_active');
            var legend_url = $(toggle_button).data('legend_img');
            if (legend_url) {
                addLegend(btn_layer_name + '_' + DataPortal.util.guid.next_uid(), btn_layer_name, '<img src="' + legend_url + '" style="width:100%; max-width:8em !important">', '');
            }

            // // {#                    var inspire = L.tileLayer.wms("http://inspire.wales.gov.uk/maps/wms", {#}
            var inspire = L.tileLayer.wms(btn_layer_url, {
                layers: btn_layer_name,
                format: 'image/png',
                transparent: true,
                attribution: "wales.gov"
            });
            inspire.addTo(map);
            DataPortal.mapping.map.layerControl.addOverlay(inspire, btn_layer_name + '-wms');
            wms_layers[btn_layer_name] = inspire;
            inspire.addTo(map);


            try {
                var wfs = $(toggle_button).data('wfs');
                var typeNS = $(toggle_button).data('wfs_namespace');
                var geometryFields = $(toggle_button).data('wfs_geometry_field');

                if (wfs && typeNS && geometryFields) {

                    var geometryFieldsArr = geometryFields.split(',');
                    // {#                            for (var geometryIdx in geometryFieldsArr) {#}
                    try {

                        var wfst = new L.WFST({
                            url: btn_layer_url,
                            typeNS: typeNS,
                            typeName: btn_layer_name,
                            // {#                                        geometryField: geometryFieldsArr[geometryIdx],#}
                            geometryField: 'fme_geometry',
                            crs: epsg27700,
                            style: {
                                color: 'blue',
                                weight: 2
                            }
                        });

                        wfst.addTo(map).once('load', function () {
                            map.fitBounds(wfst);
                        });
                        DataPortal.mapping.map.layerControl.addOverlay(wfst, btn_layer_name + '-wfs');

                        wfst.on('click', function (e) {
                            console.log('click');
                            console.log(e.layer.feature);

                            var right_pane = $('#right-component1');

                            var ppTable = prettyPrint(e.layer.feature);
                            right_pane.empty().append($(ppTable));

                        });

                    } catch (e) {
                        console.log('Failed wfs geometryfield = fme_geometry');
                        console.log(e);
                    }
                }
            }catch (e){
                console.log('wfs fail');
                console.log(e);
            }


        }
    }

    function toggle_wiserd_layer(toggle_button) {

        var wiserd_layer_uuid = $(toggle_button).data('wiserd_layer_uuid');
        if(wiserd_layer_uuid) {
            do_layer_uuids([wiserd_layer_uuid], DataPortal.django.urls('data_api'));
        }
        else {

            var btn_layer_name = $(toggle_button).data('layer_name');

            var btn_layer_field = $(toggle_button).data('field');

            // {#                Remove the class regardless what's about to happen, can be added back again #}
            $(toggle_button).removeClass('wms_layer_active');
            if (map_layers.hasOwnProperty(btn_layer_name)) {
                map.removeLayer(map_layers[btn_layer_name]);
                delete map_layers[btn_layer_name];
            } else {
                $(toggle_button).addClass('wms_layer_active');

                get_geojson_layer('wiserd_layer', [btn_layer_name], btn_layer_field);
            }
        }
    }

    // $('.wms_toggle').click(function () {
    //     toggle_layer(this)
    // });

    // Don't just call it, bind first then call with "this"
    $('.wms_toggle').click(DataPortal.mapping.LayerStore.toggle_layer.bind(this));

    // TODO as above
    $('.wiserd_layer_toggle').click(function () {
        toggle_wiserd_layer(this)
    });

        // TODO as above
    $('.upload_layer_toggle').click(function () {
        toggle_upload_layer(this)
    });

    $('.remote_data_uid').click(function () {
        var uid = null;
        if ($(this).data('naw_key_search_uid')) {
            uid = $(this).data('naw_key_search_uid');
        }
        if ($(this).data('m4w_key_search_uid')) {
            uid = $(this).data('m4w_key_search_uid');
        }
        if (uid) {
            do_layer_single_uuid(uid, DataPortal.django.urls('data_api'));
        }
    });

    function toggle_upload_layer(toggle_button) {
        var btn_layer_name = $(toggle_button).data('layer_name');

        // {#                Remove the class regardless what's about to happen, can be added back again #}
        $(toggle_button).removeClass('wms_layer_active');
        if (map_layers.hasOwnProperty(btn_layer_name)) {
            map.removeLayer(map_layers[btn_layer_name]);
            delete map_layers[btn_layer_name];
        } else {
            $(toggle_button).addClass('wms_layer_active');

            get_geojson_layer('upload_layer', [btn_layer_name], null);
        }
    }

    // {#            below is map stuff #}









// // method that we will use to update the control based on feature properties passed
//     info.update = function (props) {
//         console.log(props);
//         if (props == null) {
//             // {#                    console.log('empty props');#}
//
//             $('#right-component1').html('');
//         }
//         var value = '';
//         if (props) {
//             if (props.hasOwnProperty('response_rate')) {
//                 value = props.response_rate;
//             }
//             else if (props.hasOwnProperty('REMOTE_VALUE')) {
//                 value = props.REMOTE_VALUE;
//             } else {
//
//                 var cleanedprops = JSON.parse(JSON.stringify(props));
//                 delete cleanedprops['STRING_DATA'];
//                 delete cleanedprops['model'];
//
//                 // {#                        cleanedprops['STRING_DATA'] = null;#}
//                 // {#                        cleanedprops['model'] = null;#}
//                 var ppTable = prettyPrint(cleanedprops);
//                 // {#                        value += JSON.stringify(props);#}
//                 value = $(ppTable).prop('outerHTML')
//             }
//         }
//         var info_text = '<div style="min-height: 10%">';
//         if (props) {
//
//             var header_title = '';
//
//             if (props.DATA_TITLE) {
//                 header_title = props.DATA_TITLE;
//             } else {
//                 header_title = DataPortal.translation.translate('Region_Data');
//             }
//
//             if(DataPortal.use_welsh){
//                 if (props.DATA_TITLE_ALT1) {
//                     header_title = props.DATA_TITLE_ALT1;
//                 }
//             }
//
//             info_text += '<h3>' + header_title + '</h3>';
//
//             if (props.NAME) {
//                 info_text += '<h4>' + props.NAME + '</h4>';
//             }
//             // {# Only show alt name it it isn't the same as 'name' #}
//             if (props.ALTNAME) {
//                 if (props.NAME) {
//                     if (props.NAME != props.ALTNAME) {
//                         info_text += '<h4>' + props.ALTNAME + '</h4>';
//                     }
//                 } else {
//                     info_text += '<h4>' + props.ALTNAME + '</h4>';
//                 }
//             } else if (props.NameWelsh) {
//                 if (props.NAME) {
//                     if (props.NAME != props.NameWelsh) {
//                         info_text += '<h4>' + props.NameWelsh + '</h4>';
//                     }
//                 } else {
//                     info_text += '<h4>' + props.NameWelsh + '</h4>';
//                 }
//             }
//             info_text += '<p><b>' + trans('Total') + ' : </b>' + (value + (props.PERCENTAGE == true ? '%': '')) + '</p>';
//
//             if (props.DATA_GLOBAL_AVERAGE) {
//                 info_text += '<p><b>' + trans('Global Average') + '</b> : ' + props.DATA_GLOBAL_AVERAGE + '</p>';
//             }
//
//             var groups = {};
//
//             if (props.STRING_DATA) {
//                 var strings = '';
//                 for (var item in props.STRING_DATA) {
//                     if (props.STRING_DATA[item]['grouping']) {
//                         if (groups.hasOwnProperty(props.STRING_DATA[item]['grouping'])){
//                             groups[props.STRING_DATA[item]['grouping']]['list'].push(
//                                 get_sidebar_text(props, item)
//                             )
//                         } else {
//                             groups[props.STRING_DATA[item]['grouping']] = {
//                                 'title': props.STRING_DATA[item]['grouping'],
//                                 'list': [get_sidebar_text(props, item)]
//                             }
//                         }
//                     } else {
//                         strings += get_sidebar_text(props, item);
//                     }
//                 }
//
//                 for (var group in groups) {
//                     strings += '<div class="sidebar_group">';
//                     for (var item_field in groups[group]['list']) {
//                         strings += groups[group]['list'][item_field];
//                     }
//                     strings += '</div>';
//                 }
//
//                 info_text += strings;
//             } else {
//                 // {#                        info_text += '<h4>Hover over a region</h4>';#}
//             }
//
//             if (DataPortal.django.request.user.is_superuser){
//                 if (props.SEARCH_UUID) {
//                     info_text += '<a target="_blank" ' +
//                         'href="' + DataPortal.django.urls('search_data', {0: props.SEARCH_UUID}) + 'Search layer data</a>';
//                 }
//             }
//
//
//             info_text += '</div>';
//             // {#                FIXME this is nuts #}
//             // {#                this._div.innerHTML = info_text;#}
//             var right_pane = $('#right-component1');
//             right_pane.html(info_text);
//
//             if (props.SEARCH_UUID) {
//                 right_pane.append(
//                     $('<div/>')
//                         .addClass('btn btn-info')
//                         .text('Download Dataset')
//                         .on('click', function(){
//                             var dl_link = DataPortal.django.urls('download_dataset_zip') + '?dataset_id=' + props.SEARCH_UUID;
//                             window.open(dl_link, '_blank');
//                         })
//                 );
//             }
//
//         }
//     };
    // {#            info.addTo(map);#}

    function get_sidebar_text(props, item) {
        var strings = '';
        if (props.STRING_DATA[item]['value']) {
            var string_data_value = props.STRING_DATA[item]['value'].toString();
            // {#  is it a link? #}
            if (string_data_value.toLowerCase().indexOf('http://') == 0 ||
                string_data_value.toLowerCase().indexOf('https://') == 0) {
                if (string_data_value.toLowerCase().indexOf('.jpg') > -1 ||
                    string_data_value.toLowerCase().indexOf('.png') > -1) {
                    // {#  it's an image? #}
                    strings += ''
                        // {#                                    + '<p><b>' + props.STRING_DATA[item]['title'] + '</b></p>'#}
                        + '<p><img class="sidebar_img" src="' + string_data_value + '"></p>';
                } else {
                    // {#                                        It's a hyperlink #}
                    strings += ''
                        // {#                                    + '<p><b>' + props.STRING_DATA[item]['title']#}
                        // {#                                    + '</b></p>'#}
                        + '<p><a target="_blank" href="'
                        + string_data_value
                        + '">' + props.STRING_DATA[item]['title'] + '</a></p>';
                }
            }
            else {
                if (string_data_value.length) {

                    strings += '<p><b>' + props.STRING_DATA[item]['title']
                        + '</b> : ' + string_data_value + '</p>';
                    // {#                        console.log(string_data_value);#}
                }
            }
        }
        return strings;
    }

    var geojson;
    function resetHighlight(e) {
        e.target.resetStyle(e.target);
        info.update();
    }

    function highlightFeature(e) {
        var layer = e.target;
        layer.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });
        // {#                if (!L.Browser.ie && !L.Browser.opera) {#}
        // {#                layer.bringToFront();#}
        // {#                }#}
        info.update(layer.feature.properties);
    }

    function djb2(str){
        var hash = 5381;
        for (var i = 0; i < str.length; i++) {
            hash = ((hash << 5) + hash) + str.charCodeAt(i); /* hash * 33 + c */
        }
        return hash;
    }

    function hashStringToColor(str) {
        var hash = djb2(str);
        var r = (hash & 0xFF0000) >> 16;
        var g = (hash & 0x00FF00) >> 8;
        var b = hash & 0x0000FF;
        return "#" + ("0" + r.toString(16)).substr(-2) + ("0" + g.toString(16)).substr(-2) + ("0" + b.toString(16)).substr(-2);
    }

    function getColorFromString(string_value) {
        switch (string_value) {

            case 'LAB':
                return '#e4002b';
            case 'Lab':
                return '#e4002b';

            case 'CON':
                return '#0057b8';
            case 'Con':
                return '#0057b8';

            case 'LIB':
                return '#fdbb30';
            case 'LD':
                return '#fdbb30';

            case 'PLC':
                return '#4c8c2b';
            case 'PC':
                return '#4c8c2b';

            case 'NAT':
                return '#4c8c2b';
            case 'UKIP':
                return '#70147A';
            case 'OTH':
                return '#888b8d';
            case 'DT':
                return '#993366';
            case 'SNP':
                return '#FFF95D';
            case 'DUP':
                return '#cc0202';
            case 'SDLP':
                return '#99FF66';
            case 'SF':
                return '#008800';
            case 'UUP':
                return '#9999FF';
            case 'Ind':
                return '#dddddd';
            case 'Spk':
                return '#ffffff';
            case 'Green':
                return '#6AB023';
            default:
                return hashStringToColor(string_value)
        }

    }

    // {#        TODO check what this is returning #}
    function getColor(d, feature_data, chroma_scale) {

        if (chroma_scale) {
            return chroma_scale(parseFloat(d));
        }

        if (feature_data) {
            var scale = chroma.scale('OrRd').classes(feature_data);
            return scale(parseFloat(d));
        }

        d = parseFloat(d);
        return chroma.random();

        return d > 80 ? '#800026' :
            d > 75  ? '#BD0026' :
                d > 70  ? '#E31A1C' :
                    d > 60  ? '#FC4E2A' :
                        d > 50   ? '#FD8D3C' :
                            d > 40   ? '#FEB24C' :
                                d > 30   ? '#FED976' :
                                    '#FFEDA0';
    }

    function remove_layer(remove_button){
        DataPortal.mapping.map.map.removeLayer(map_layers[$(remove_button).data('layername')]);
    }

    function replace_layer(replace_button){
        map_layers[$(replace_button).data('layername')].addTo(DataPortal.mapping.map.map);
    }

    // {#            get_geojson_layer('survey', JSON.parse('{{ surveys|safe }}'));#}

    function get_geojson_layer(layer_type, layer_names, btn_layer_field){
        add_ajax_waiting(trans('Fetching map layer...'));

        var ajax_url = DataPortal.django.urls('get_geojson');

        if( layer_type == 'upload_layer'){
            ajax_url = DataPortal.django.urls('get_imported_feature');
        } else {
            ajax_url = DataPortal.django.urls('get_geojson');
        }

        $.ajax({
            url: ajax_url,
            type: 'POST',
            data: {
                'layer_type': layer_type,
                'layer_names': layer_names,
                'field': btn_layer_field
                // {#                        'area_names': {{ area_names|safe }}#}
            },
            success: function(data) {

                var name = layer_names[0];

                $('.replace_layer').click(function () {
                    replace_layer(this)
                });
                $('.remove_layer').click(function () {
                    remove_layer(this)
                });

                $('.show_layer').click(function () {
                    var btn_span = $(this);
                    if(btn_span.data('visible')) {
                        btn_span.data('visible', false);
                        btn_span.removeClass('fa-eye').addClass('fa-eye-slash');
                    } else {
                        btn_span.data('visible', true);
                        btn_span.removeClass('fa-eye-slash').addClass('fa-eye');
                    }
                });

                if (layer_type == 'survey') {
                    geojson = L.geoJson(data, {
                        onEachFeature: function (feature, layer) {
                            // {#                                    layer.bindPopup(feature.properties.area_name + '<br>' + feature.properties.response_rate + '%');#}
                            layer.on({
                                mouseover: highlightFeature,
                                mouseout: resetHighlight
                            });
                        },
                        style: function (feature) {
                            return {
                                fillColor: getColor(feature.properties.response_rate),
                                weight: 2,
                                opacity: 1,
                                color: 'white',
                                dashArray: '3',
                                fillOpacity: 0.7
                            };
                        }

                    });
                    geojson.addTo(DataPortal.mapping.map.map);
                    geojson.bringToFront();
                    map_layers[data['properties']['name']] = geojson;
                }

                if (layer_type == 'wiserd_layer') {

                    if (data['properties']['remote_value_key']) {

                        handleUploadedLayer(data, 'Spectral', 'q', '8', '', data['properties']['name'], '', {'remote_value_key': data['properties']['remote_value_key']});
                    }
                    else {

                        var myLayer = L.geoJson(data, {
                            onEachFeature: function (feature, layer) {

                                layer.on({
                                    click: function (e) {
                                        alert('click');

                                        var layer = e.target;
                                        // {#                                                console.log(layer);#}
                                        info.update(layer.feature.properties);

                                        layer.setStyle({
                                            weight: 5,
                                            color: '#666',
                                            dashArray: '',
                                            fillOpacity: 0.7
                                        });
                                    },
                                    // {#                                            mouseout: function (e) {#}
                                    // {#                                                console.log(e.target);#}
                                    // {#                                                myLayer.resetStyle(e.target);#}
                                    // {#                                                info.update();#}
                                    // {#                                            }#}
                                });
                            },
                            style: function (feature) {
                                return {
                                    fillColor: '#0044AA',
                                    fillOpacity: 0.7,
                                    weight: 2,
                                    opacity: 1,
                                    color: 'orangered',
                                    dashArray: '3'
                                };
                            }
                        });
                        DataPortal.mapping.map.layerControl.addOverlay(myLayer, name);
                        myLayer.addTo(DataPortal.mapping.map.map);
                        map_layers[data['properties']['name']] = myLayer;


                        if (layer_type == 'upload_layer') {

                            topojson_layers[layer_names] = data;
                            $("#chloropleth_option_form").data(
                                {layer_names: layer_names}
                            ).dialog("open");

                        }
                    }
                }
            },
            error: function() {
                alert(trans('Sorry, an error occurred. Please try again, or report it.'))
            },
            complete: function() {
                ajax_finished();

            }
        });
    }


    function handleUploadedLayer(data, color_scheme, bin_breakdown, num_bins,
                                 nomis_variable, layer_name_text, csv_url, layer_data){

        console.log('handling new layer');
        // {#                console.log(data);#}
        // {#                console.log(layer_data);#}
        var remote_value_key = 'REMOTE_VALUE';
        if (layer_data['remote_value_key']) {
            remote_value_key = layer_data['remote_value_key'];
        }

        try {

            info.update();

            if (layer_name_counter.hasOwnProperty(layer_name_text)) {
                var counter = layer_name_counter[layer_name_text];
                var tmp_layer_name_text = layer_name_text + '_' + counter;
                layer_name_counter[layer_name_text] = (counter += 1);
                layer_name_text = tmp_layer_name_text;
            } else {
                layer_name_counter[layer_name_text] = 1
            }
            var a_uid = DataPortal.util.guid.next_uid()();
            var unique_layer_name_text = layer_name_text + '_' + a_uid;


            // {#                console.log(color_scheme, bin_breakdown, num_bins, nomis_variable, layer_name_text, csv_url);#}
            var is_percentage = false;
            var suppressed_data = false;
            var fake_data = false;
            var opacity = DataPortal.mapping.opacity();
            if (color_scheme == 'w') {
                opacity = 0;
            }
            color_scheme = DataPortal.mapping.colour_scheme(color_scheme);

            if (nomis_variable) {
                if (nomis_variable == 20301) {
                    is_percentage = true;
                }
            }
            var feature_data = [];
            var feature_string_data = [];
            var search_uuid = '0000';

            if (data['objects']) {
                // {#                        Topojson #}

                var data_objects = data['objects'];
                for (var b in data_objects) {
                    var geometries_properties = data_objects[b]['geometries'];
                    for (var a in geometries_properties) {
                        if (geometries_properties[a]['properties']['DATA_STATUS'] == 'Q') {
                            suppressed_data = true;
                        }
                        if (geometries_properties[a]['properties'][remote_value_key]) {
                            var remote_value = geometries_properties[a]['properties'][remote_value_key];
                            if (isNaN(remote_value)) {
                                feature_string_data.push(remote_value);
                            } else {
                                feature_data.push(parseFloat(remote_value));
                            }
                        }
                        if (geometries_properties[a]['properties']['SEARCH_UUID']) {
                            search_uuid = geometries_properties[a]['properties']['SEARCH_UUID'];
                        }
                    }
                }
            }


            if (data['features']) {
                // {#                        Geojson (points) #}

                var data_objects = data['features'];
                for (var b in data_objects) {
                    var geometries_properties = data_objects[b]['properties'];
                    if (geometries_properties['DATA_STATUS']) {
                        if (geometries_properties['DATA_STATUS'] == 'Q') {
                            suppressed_data = true;
                        }
                    }
                    if (geometries_properties[remote_value_key]) {
                        var remote_value = geometries_properties[remote_value_key];
                        if (isNaN(remote_value)) {
                            feature_string_data.push(remote_value);
                        } else {
                            feature_data.push(parseFloat(remote_value));
                        }
                    }
                    if (geometries_properties['SEARCH_UUID']) {
                        search_uuid = geometries_properties['SEARCH_UUID'];
                    }
                }
            }


            if (fake_data) {
                alert('WARNING: some required data not found, so has been spoofed with random data.');
                console.log('SPOOFED remove me')
            }

            var unique_feature_string_data = [];
            for (var string_idx in feature_string_data) {
                if (unique_feature_string_data.indexOf(feature_string_data[string_idx]) == -1) {
                    unique_feature_string_data.push(feature_string_data[string_idx]);
                    // {#                        alert(feature_string_data[string_idx]);#}
                }
            }


            if (suppressed_data) {
                alert("{% trans 'Sorry, an error occurred. \n\n' %}" +
                    "{% trans 'It looks like your query was too specific, for example, when data are suppressed due to statistical confidentiality considerations. \n\n' %}" +
                    "{% trans 'In this case, try a larger area to map data for.' %}")
            }


            if (feature_string_data.length > 0) {
            } else {
                if (feature_data.length == 0) {
                    throw "feature_data_0";
                }
            }

            var chroma_scale = null;
            var grades = null;

            if (feature_data.length > 1) {

                // {#                    console.log(feature_data);#}
                var data_len = feature_data.length;
                if (num_bins > data_len) {
                    num_bins = data_len;
                }

                // {#  Calculating the bins for quantiles with 'q' option, 'e'  and 'k' available #}
                grades = chroma.limits(feature_data, bin_breakdown, parseInt(num_bins));
                // {#                    console.log(grades);#}

                // {#  Calculating the function we can pass values to, in order to get nice rgb color codes #}
                chroma_scale = chroma.scale(color_scheme).classes(grades);
                // {#                    console.log(chroma_scale);#}
            }



            var myLayer = new L.TopoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    // {#                        console.log(feature);#}
                    // {#                        if (feature.properties.RENDER == true) {#}

                    if (isNaN(feature.properties[remote_value_key])) {

                        // {#                            if (feature.properties[remote_value_key]) {#}

                        var iconClassName = 'marker_bkgd fa fa-2x fa-fw ';
                        if (layer_data['point_icon']) {
                            iconClassName += layer_data['point_icon']
                        } else {
                            iconClassName += 'fa-institution';
                        }

                        var myIcon = L.divIcon({
                            // {#                                    html: '<div style="border: 2px solid black"></div>',#}
                            className: iconClassName,
                            iconSize: [28, 28],
                            iconAnchor: [15, 15],
                            popupAnchor: [0, 0],
                            shadowSize: [0, 0]
                        });
                        var marker = L.marker(latlng, {icon: myIcon}).addTo(DataPortal.mapping.map.map);
                        marker.valueOf()._icon.style.backgroundColor = getColorFromString(feature.properties[remote_value_key]);
                        marker.valueOf()._icon.style.color = 'white';

                        return marker
                    } else {
                        return L.circleMarker(latlng, DataPortal.mapping.geojsonMarkerOptions);
                    }
                }
            });

            leaflet_layers.push({
                name: layer_name_text,
                layer: myLayer,
                attribution: 'hello world'
            });

            myLayer.eachLayer(function (layer) {
                if (typeof layer.setStyle === 'function') {
                    // {#                            console.log(layer);#}
                    layer.setStyle(styleFeature(layer.feature, grades, chroma_scale, opacity, remote_value_key));
                }

                layer.on({
                    add: function (e) {
                        var layer = e.target;
                        if (layer._icon) {
                            if (e.target.feature.properties.REMOTE_VALUE) {
                                e.target._icon.style.backgroundColor = getColorFromString(e.target.feature.properties.REMOTE_VALUE);
                            }
                            if (e.target.feature.properties.category) {
                                e.target._icon.style.backgroundColor = getColorFromString(e.target.feature.properties.category);
                            }

                            e.target._icon.style.color = 'white';
                            e.target._icon.style.border = '';
                        }
                    },
                    mouseover: function (e) {

                        var layer = e.target;

                        if (layer.setStyle) {
                            layer.setStyle({
                                weight: 5,
                                color: '#666',
                                dashArray: '',
                                fillOpacity: DataPortal.mapping.opacity()
                            });
                        }

                        var col;
                        var remote_value = layer.feature.properties[remote_value_key];
                        if(isNaN(remote_value)) {
                            col = getColorFromString(remote_value);
                        } else {
                            col = getColor(remote_value, feature_data, chroma_scale).hex();
                        }
                        var adv_col = '#' + ('000000' + (('0xffffff' ^ col.replace('#', '0x')).toString(16))).slice(-6);

                        if (layer._icon) {
                            layer._icon.style.backgroundColor = col;
                            layer._icon.style.color = adv_col;
                        }

                        if(layer.feature.geometry.type == 'LineString') {
                            console.log(e.originalEvent);

                            // {#                                    console.log('mouseover line ' + col + ' : ' + adv_col);#}

                            layer.setStyle({
                                fillColor: adv_col,
                                weight: 5,
                                opacity: 1,
                                color: adv_col,
                                dashArray: '3',
                                fillOpacity: DataPortal.mapping.opacity()
                            });
                        }
                    },
                    mouseout: function (e) {
                        var layer = e.target;

                        if (layer.setStyle) {
                            layer.setStyle({
                                fillOpacity: DataPortal.mapping.opacity(),
                                weight: 2,
                                opacity: 1,
                                color: 'white',
                                dashArray: '3'
                            });
                        }

                        var col;
                        var remote_value = layer.feature.properties[remote_value_key];
                        if(isNaN(remote_value)) {
                            col = getColorFromString(remote_value);
                        } else {
                            col = getColor(remote_value, feature_data, chroma_scale).hex();
                        }

                        if (layer._icon) {
                            layer._icon.style.backgroundColor = col;
                            layer._icon.style.color = 'white';
                            layer._icon.style.border = '';
                        }

                        if(layer.feature.geometry.type == 'LineString') {
                            // {#                                    console.log('mouseout line ' + col);#}

                            layer.setStyle({
                                fillColor: col,
                                weight: 5,
                                opacity: 1,
                                color: col,
                                dashArray: '3',
                                fillOpacity: DataPortal.mapping.opacity()
                            });
                        }
                    },
                    click: function(e) {
                        console.log(e.originalEvent);
                        console.log('icon item 3');
                        show_sidebar();

                        try {
                            layer.bringToFront();
                        }catch (e){}

                        info.update(layer.feature.properties);

                        var html = '';
                        // look through each layer in order and see if the clicked point,
                        // e.latlng, overlaps with one of the shapes in it.

                        for (var i = 0; i < leaflet_layers.length; i++) {

                            var match = leafletPip.pointInLayer(
                                // the clicked point
                                e.latlng,
                                // this layer
                                leaflet_layers[i].layer,
                                // whether to stop at first match
                                true);

                            // if there's overlap, add some content to the popup: the layer name
                            // and a table of attributes

                            // {#                            TODO - we've just checked all layers for a click, #}
                            // {#                            TODO and totally ignored them #}
                            // {#                            if (match.length) {#}
                            // {#                                console.log(match[0].feature.properties);#}
                            // {#                                html += '<strong>' + leaflet_layers[i].name + '</strong>';#}
                            // {#                                html += propertyTable(match[0].feature.properties) + '<br><br>';#}
                            // {#                            }#}
                        }
                        if (html) {
                            // {#                            map.openPopup(html, e.latlng);#}
                            $('#right-component1').append(html);
                        }

                        // {#                                This is just for the Canada Commute things #}
                        if(layer.feature.properties['csduid']){
                            $.ajax({
                                url: DataPortal.django.urls('cancommute_to_location'),
                                type: 'GET',
                                data: {
                                    'csduid': layer.feature.properties['csduid']
                                },
                                success: function (data) {
                                    handleUploadedLayer(
                                        data,
                                        'naw',
                                        'q',
                                        '5',
                                        '',
                                        'routes',
                                        '',
                                        {'remote_value_key': 'total'}
                                    );
                                }
                            });
                        }
                    }
                });

            });
            // {#                    myLayer.eachLayer(handleLayer);#}

            DataPortal.mapping.map.layerControl.addOverlay(myLayer, layer_name_text);

            DataPortal.mapping.map.map.on('overlayremove', function (eventLayer) {
                if (eventLayer.name == layer_name_text) {
                    // {#                        console.log('trying to remove : ' + '#accordion_inner_collapse_' + unique_layer_name_text);#}
                    $('#accordion_inner_collapse_' + unique_layer_name_text.replace(/\W/g, '')).remove();
                }
            });
            DataPortal.mapping.map.map.on('overlayadd', function (eventLayer) {

                console.log('eventLayer');
                console.log(eventLayer);

                if (eventLayer.name == layer_name_text) {
                    console.log(layer_name_text);
                    var div_inner = build_legend(feature_data,
                        unique_feature_string_data,
                        chroma_scale,
                        grades, is_percentage);
                    if (eventLayer._wdp_legend){
                        addLegend(unique_layer_name_text, layer_name_text, eventLayer._wdp_legend, search_uuid);
                    } else {
                        addLegend(unique_layer_name_text, layer_name_text, div_inner, search_uuid);
                        eventLayer._wdp_legend = div_inner;
                    }
                }
            });


            var is_clustermarkers = false;
            var is_heatmap = false;

            myLayer.eachLayer(function (layer) {
                if (layer.feature.type === 'Feature') {
                    // {# enable this line if we want clustered markers #}
                    // {#        is_clustermarkers = true;#}
                    // {#        is_heatmap = true;#}

                }
            });

            if (is_clustermarkers) {
                var markers = L.markerClusterGroup();
                myLayer.eachLayer(function (layer) {
                    if (layer.feature.type === 'Feature') {
                        markers.addLayer(layer);
                    }
                });
                DataPortal.mapping.map.map.addLayer(markers);
                DataPortal.mapping.map.map.fitBounds(markers.getBounds(), { paddingBottomRight: [200, 0] });

                // {#                        markers.bringToFront();#}

            }
            else if (is_heatmap){
                var heat_data = [];
                myLayer.eachLayer(function (layer) {
                    if (layer.feature.type === 'Feature') {
                        // {#                            console.log(layer);#}
                        heat_data.push([layer.feature.geometry.coordinates[1],
                            layer.feature.geometry.coordinates[0],
                            layer.feature.REMOTE_VALUE])
                    }
                });

                var heat = L.heatLayer(heat_data, {radius: 25});
                heat.addTo(DataPortal.mapping.map.map);
            }
            else{
                myLayer.addTo(DataPortal.mapping.map.map);
                DataPortal.mapping.map.map.fitBounds(myLayer.getBounds(), { paddingBottomRight: [200, 0] });

                myLayer.bringToFront();
            }
        } catch (e) {

            if (e == 'feature_data_0') {
                alert("{% trans 'Sorry, an error occurred. \n\n' %}" +
                    "{% trans 'Layer: ' %}" + layer_name_text + "\n\n" +
                    "{% trans 'No data could be found for this query. \n\n' %}" +
                    "{% trans 'Please try again, or report it.' %}")
            } else {

                console.log(e);

                alert("{% trans 'Sorry, an error occurred. \n\n' %}" +
                    "{% trans 'Unfortunately, some types of dataset are incompatible with this service. \n\n' %}" +
                    "{% trans 'Try being more specific with the dataset variable you are trying to map. \n\n' %}" +
                    "{% trans 'Or, it may be the case that your query was too specific. For example, when data are suppressed due to statistical confidentiality considerations. ' %}" +
                    "{% trans 'In this case, try a larger area to map data for.' %}")
            }
        }

    }

    var layers = {};
    function recordLayerOrders() {
        DataPortal.mapping.map.map.eachLayer(function(layer) {
            if( layer instanceof L.TileLayer ) {
                console.log('Recording layer ' + layer + ' as ' + layers[layer]);
                console.log(layer);
                layers[layer] = layer.zIndex;
            }
        });
    }
    function updateLayerOrders() {
        DataPortal.mapping.map.map.eachLayer(function(layer) {
            if( layer instanceof L.TileLayer ) {
                console.log('Setting layer ' + layer + ' to ' + layers[layer]);
                layer.setZIndex(layers[layer]);
            }
        });
    }


    function build_legend(feature_data, unique_feature_string_data, chroma_scale, grades, is_percentage) {
        console.log('Legend:');
        console.log({
            'feature_data': feature_data,
            'unique_feature_string_data': unique_feature_string_data,
            'chroma_scale': chroma_scale,
            'grades': grades,
            'is_percentage': is_percentage
        });
        var labels = [], from, to;

        // {#                console.log('feature_data');#}
        // {#                console.log(feature_data);#}
        if (feature_data.length > 1) {
            // {#  For each bin in the quantiles, we need a representative color for the Legend #}
            for (var i = 0; i < grades.length -1; i++) {
                from = grades[i];
                to = grades[i + 1];

                var legend_row = '<p style="padding: 0 1em;"><i style="background:' + getColor(from, grades, chroma_scale) + '"></i> ';
                legend_row += from.toFixed(2);
                if (to) {
                    legend_row += (to).toFixed(2) ? (i == 0 ? ' &ndash; ': ' &le; ') + (to).toFixed(2) + (is_percentage ? '%' : '') : (is_percentage ? '%+' : '+');
                } else {
                    legend_row += (is_percentage ? '%' : '');
                }
                legend_row += unique_feature_string_data;
                legend_row += '</p>';
                labels.push(legend_row);
            }
        }

        // {#                console.log('unique_feature_string_data');#}
        // {#                console.log(unique_feature_string_data);#}
        if (unique_feature_string_data.length > 0) {
            for (var string_idx in unique_feature_string_data.sort()) {
                var legend_string_row = '<p style="white-space: nowrap; padding: 0 1em;"><i style="background:' + getColorFromString(unique_feature_string_data[string_idx]) + '"></i> ' + unique_feature_string_data[string_idx] + '</p>';
                labels.push(legend_string_row);
            }
        }
        var div_inner = labels.join('');
        div_inner += '</div>';
        return div_inner;
    }



    var legend_two = L.control({
        id: 'legend_control',
        position: 'bottomright'
    });
    legend_two.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'legend info');

        var accordionDiv = $('<div/>')
            .attr("id", "legend_accordion")
            .addClass("panel-group");

        $(div).attr("id", "legend").append(accordionDiv)
            .css({'max-height': DataPortal.mapping.map.map_div.height() * 0.8, 'overflow-y': 'auto'});
        // {#                        .draggable().resizable();#}
        return div;
    };
    legend_two.addTo(DataPortal.mapping.map.map);

    // {#            FIXME re add and move me#}
    // {#            var div = L.DomUtil.create('div', 'info legend');#}
    // {#            var legendHeaderDiv = $('<div/>')#}
    // {#                    .addClass("panel-heading")#}
    // {#                    .text('Legend');#}
    // {#            var accordionDiv = $('<div/>')#}
    // {#                    .attr("id", "legend_accordion")#}
    // {#                    .addClass("panel-group");#}
    // {#            $(div).append(legendHeaderDiv).append(accordionDiv);#}
    // {#            $('#right-component2').append(div);#}

    // {#            $('.legend').resizable({handles: 'n, e, s, w'});#}

    function propertyTable(o) {
        // {#                var t = '<table>';#}
        // {#                for (var k in o) {#}
        // {#                    if (typeof(o[k]) != 'object') {#}
        // {#                        t += '<tr><th>' + k + '</th><td>' + o[k] + '</td></tr>';#}
        // {#                    }#}
        // {#                }#}
        // {#                t += '</table>';#}

        var propertyList = '';
        for (var k in o) {
            if (typeof(o[k]) != 'object') {
                propertyList += '<p><b>' + k + '</b></p><p>' + o[k] + '</p>';
                // {#                        .replace('""', '"')#}
            }
        }
        return propertyList;
    }

    function styleFeature(feature, feature_data, chroma_scale, opacity, remote_value_key) {

        // {#                console.log('is this a line?');#}
        // {#            console.log(feature, feature_data, chroma_scale, opacity);#}

        var colour = '';
        if (remote_value_key) {
            var remote_value = feature.properties[remote_value_key];

        } else {
            var remote_value = feature.properties.REMOTE_VALUE;
        }
        // {#                console.log(remote_value);#}
        if (remote_value === undefined){
            return {
                fill: DataPortal.django.static_urls('leaflet-polygon-fillPattern-master/example/image.gif'),
                stroke: '#fff',
                'stroke-width': 2,
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: opacity
            }
        } else {

            if (isNaN(remote_value)) {
                colour = getColorFromString(remote_value);
            } else {
                colour = getColor(remote_value, feature_data, chroma_scale);
            }

            if(feature.geometry.type == 'LineString'){
                return {
                    fillColor: colour,
                    weight: 5,
                    opacity: 1,
                    color: colour,
                    dashArray: '3',
                    fillOpacity: opacity
                };
            }

            return {
                fillColor: colour,
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: opacity
            };
        }
    }

    var map_layers = {};
    var featureGroup = L.featureGroup().addTo(DataPortal.mapping.map.map);

    DataPortal.mapping.map.map.addControl( new L.Control.Search({
        textPlaceholder: trans('Search'),
        url: 'http://nominatim.openstreetmap.org/search?format=json&q={s}',
        jsonpParam: 'json_callback',
        propertyName: 'display_name',
        propertyLoc: ['lat','lon'],
        circleLocation: false,
        markerLocation: true,
        autoType: false,
        autoCollapse: true,
        minLength: 2,
        zoom:10
    }) );

    L.Control.Screenshot = L.Control.extend({
        options: {
            position: 'topleft'
        },
        onAdd: function (map2) {
            var controlDiv = L.DomUtil.create('div', 'leaflet-control-command');
            L.DomEvent
                .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
                .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
                .addListener(controlDiv, 'click', function () { take_screenshot()});

            var controlUI = L.DomUtil.create('div', 'leaflet-control-command-interior', controlDiv);
            controlUI.title = '{% trans "Screenshot" %}';
            controlUI.innerHTML = '<a><i class="fa fa-camera"></a>';
            return controlDiv;
        }
    });

    var screenshot_control = new L.Control.Screenshot();
    screenshot_control.addTo(DataPortal.mapping.map.map);


    L.Control.Reset = L.Control.extend({
        options: {
            position: 'topleft'
        },
        onAdd: function (map2) {
            var controlDiv = L.DomUtil.create('div', 'leaflet-control-command');
            L.DomEvent
                .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
                .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
                .addListener(controlDiv, 'click', function () { reset_map()});

            var controlUI = L.DomUtil.create('div', 'leaflet-control-command-interior', controlDiv);
            controlUI.title = '{% trans "Reset" %}';
            controlUI.innerHTML = '<a><i class="fa fa-refresh"></a>';
            return controlDiv;
        }
    });

    var reset_map_btn = new L.Control.Reset();
    reset_map_btn.addTo(DataPortal.mapping.map.map);


    if (DataPortal.tpt == 'default' ) {

        var drawControl = new L.Control.Draw({
            edit: {
                featureGroup: featureGroup
            },
            draw: {
                polygon: true,
                polyline: false,
                rectangle: {
                    shapeOptions: {
                        color: '#888888'
                    }
                },
                circle: true,
                marker: false
            }
        }).addTo(DataPortal.mapping.map.map);

        DataPortal.mapping.map.map.on('draw:created', showPolygonArea);
        DataPortal.mapping.map.map.on('draw:edited', showPolygonAreaEdited);

    }

    function convertPolygonToOS(shape_geojson){

        var new_coordinates = [];
        var new_geometry = {
            "type": "Polygon",
            "coordinates": [[]]
        };

        for (var a = 0; a < shape_geojson['geometry']['coordinates'][0].length; a++) {
            var ll2 = new LatLng(shape_geojson['geometry']['coordinates'][0][a][1],
                shape_geojson['geometry']['coordinates'][0][a][0]);
            var os2 = ll2.toOSRef();
            new_coordinates.push([os2.easting, os2.northing]);
        }

        new_geometry['coordinates'] = [new_coordinates];

        return new_geometry

    }
    function showPolygonAreaEdited(e) {
        e.layers.eachLayer(function(layer) {
            showPolygonArea({ layer: layer });
        });
    }

    function showPolygonArea(e) {

        featureGroup.clearLayers();
        featureGroup.addLayer(e.layer);

        geoJson_area_km2 = (LGeo.area(e.layer) / 1000000).toFixed(2);
        e.layer.bindPopup(geoJson_area_km2 + ' km<sup>2</sup>');
        e.layer.openPopup();

        search_area_geojson = e.layer.toGeoJSON();
        $('#output').val(search_area_geojson);
        var new_geojson = convertPolygonToOS(search_area_geojson);
        wkt = $.geo.WKT.stringify(new_geojson);

        DataPortal.mapping.map.map.fitBounds(featureGroup.getBounds());
        center_lat_lng = featureGroup.getBounds().getCenter();
        // {#                viewreset is really slow #}
        DataPortal.mapping.map.map.addOneTimeEventListener('moveend', function() {
            // {#                    alert('moveend');#}
            setTimeout(function(){
                leafletImage(DataPortal.mapping.map.map, doImage);
            }, 1000);
        });
    }

    var most_recent_search_png = '';
    function doImage(err, canvas) {
        // {#                alert('doimage');#}
        // {#                var snapshot = document.getElementById('snapshot');#}

        var img = document.createElement('img');
        var dimensions = DataPortal.mapping.map.map.getSize();
        img.width = dimensions.x;
        img.height = dimensions.y;
        most_recent_search_png = canvas.toDataURL("image/jpeg", 0.5);
        img.src = most_recent_search_png;
        // {#                img.style.width = '100%';#}
        // {#                snapshot.innerHTML = '';#}
        // {#                snapshot.appendChild(img);#}

        $.ajax({
            url: DataPortal.django.urls('spatial_search'),
            type: 'POST',
            data: {
                geography: wkt,
                // {#                        geojson: search_area_geojson,#}
                centre_lat_lng: [center_lat_lng.lat, center_lat_lng.lng],
                geo_area_km2: geoJson_area_km2,
                start: 0,
                limit: 15,
                type: "Qual",
                uid_only: true,
                image_png: most_recent_search_png
            },
            success: function(data) {
                // {#                        alert(JSON.stringify(data['data']));#}

                if (data['uid']) {
                    // {#                            console.log("{% url 'tables' %}?search_id=" + data['uid']);#}
                    // {#                            var snapshot = document.getElementById('output');#}
                    // {#                            snapshot.innerHTML = "{% url 'tables' %}?search_id=" + data['uid'];#}

                    setTimeout(function(){
                        // {#                                TODO FINDME re-enable this #}
                        window.location = "{% url 'tables' %}?search_id=" + data['uid'];
                    }, 1000);
                }
            },
            complete: function() {
                ajax_finished();
            }
        });
    }

    String.prototype.format = function() {
        var formatted = this;
        for (var i = 0; i < arguments.length; i++) {
            var regexp = new RegExp('\\{'+i+'\\}', 'gi');
            formatted = formatted.replace(regexp, arguments[i]);
        }
        return formatted;
    };

    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    // {#            setTimeout(function() {#}
    // {#                $('#side-menu').removeData("plugin_metisMenu").metisMenu({toggle: false});#}
    // {#            }, 2000);#}
    // {#            setTimeout(function() {#}
    // {#                $('#side-menu').removeData("plugin_metisMenu").metisMenu({toggle: false});#}
    // {#            }, 5000);#}

    $( "#chloropleth_option_form" ).dialog({
        autoOpen: false,
        height: DataPortal.mapping.map.map_div.height() * 0.9,
        width: $('#page-wrapper').width() * 0.7,
        position: {
            my: "center",
            at: "center",
            of: DataPortal.mapping.map.map_div
        },
        modal: true,
        buttons: [
            {
                text: "{% trans 'Show New Layer' %}",
                click: function() {
                    if ($("#bintype").val() != '') {
                        if ($("#binno").val() != '') {

                            var layer_id = $(this).data('layer_names');
                            var dataset_name = $(this).data('dataset_name');
                            var topojson_data = topojson_layers[$(this).data('layer_names')];
                            var nomis_variable = $(this).data('nomis_variable');
                            var layer_name_text = $("#layer_name_text_entry").val();
                            var csv_url = $(this).data('csv_url');

                            var colorpicker = $("#colorpicker").val();
                            var bin_type = $("#bintype").val();
                            var bin_num = $("#binno").val();

                            var point_icon = $('.lead .picker-target').data("icon_fa");

                            var saveToLocalStorage = $(this).data('localStorage');
                            if (saveToLocalStorage) {
                                var all_topojson_data = $(this).data('all_topojson_data');
                                all_topojson_data['layer_data']['colorpicker'] = colorpicker;
                                all_topojson_data['layer_data']['bin_type'] = bin_type;
                                all_topojson_data['layer_data']['bin_num'] = bin_num;
                                all_topojson_data['layer_data']['name'] = layer_name_text;
                                all_topojson_data['layer_data']['point_icon'] = point_icon;

                                if(typeof(Storage) !== "undefined") {
                                    var localLayers = {};
                                    if (localStorage.DataPortalLocalLayers) {
                                        localLayers = JSON.parse(localStorage.getItem('DataPortalLocalLayers'));
                                    }
                                    localLayers[layer_id] = all_topojson_data;

                                    try {
                                        localStorage.setItem("DataPortalLocalLayers", JSON.stringify(localLayers));
                                    } catch (e) {
                                        if (isQuotaExceeded(e)) {
                                            alert(trans('You have reached the maximum amount of data which can be stored locally in your browser.\n\nYou will need to delete some layers before more can be stored.\n\nThe data can still be shown on the map, but you will continue to see this error each time new data is added.'));
                                        } else {
                                            console.log(e);
                                        }
                                    }
                                } else {
                                    alert(trans('Sorry! Your browser does not support local data storage. You will need to add data each time you refresh the page'));
                                }
                            }

                            var new_layer = new MapLayer();
                            new_layer.layer_id = $(this).data('layer_names');
                            new_layer.topojson_data = topojson_layers[$(this).data('layer_names')];
                            new_layer.nomis_variable = $(this).data('nomis_variable');
                            new_layer.layer_name_text = $("#layer_name_text_entry").val();
                            new_layer.csv_url = $(this).data('csv_url');
                            new_layer.colorpicker = $("#colorpicker").val();
                            new_layer.bin_type = $("#bintype").val();
                            new_layer.bin_num = $("#binno").val();
                            new_layer.point_icon = point_icon;


                            DataPortal.mapping.LayerStore.add_layer(new_layer);


                            $.ajax({
                                url: "{% url 'data_api' %}",
                                type: 'GET',
                                data: {
                                    method: 'record_nomis_search',
                                    layer_id: layer_id,
                                    layer_name: layer_name_text,
                                    colorpicker: colorpicker,
                                    bin_type: bin_type,
                                    bin_num: bin_num,
                                    point_icon: point_icon,
                                    layer_data: {
                                        layer_id: layer_id,
                                        layer_name: layer_name_text,
                                        colorpicker: colorpicker,
                                        bin_type: bin_type,
                                        bin_num: bin_num,
                                        point_icon: point_icon
                                    }
                                },
                                success: function(data) {},
                                error: function() {}
                            });

                            handleUploadedLayer(
                                topojson_data,
                                colorpicker,
                                bin_type,
                                bin_num,
                                nomis_variable,
                                layer_name_text,
                                csv_url,
                                {
                                    'layer_id': layer_id,
                                    'layer_name': layer_name_text,
                                    'colorpicker': colorpicker,
                                    'bin_type': bin_type,
                                    'bin_num': bin_num,
                                    'point_icon': point_icon
                                }
                            );

                            $(this).dialog("close");

                        }
                    }
                }
            },
            {
                text: trans('Cancel'),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ],
        close: function() {
        }
    });

    $("#new_layer_btn").click(function(e){
        $( "#search-remote-form").dialog( "open" );
    });

    $("#import_local_data_btn").click(function(e){
        var dataset_radio = $('#local_column_headers_radio');
        dataset_radio.find('div').remove().end();

        DataPortal.util.resetFormElement($('#local-data-drop-zone'));

        $('#local-data-drop-zone').show();
        $('#mapmydata_help').off('click').on('click', do_mapmydata_tutorial_1);
        $("#local-data-form").dialog( "open" );
    });

    $('#dataset_select').change(function(e){
        // {#                alert(e);#}
    });

    $('#remote_search_term').keyup(function(event){
        if(event.keyCode == 13){
            $("#remote_search_btn").click();
        }
    });

    $("#remote_search_btn").click(function(e){
        var search_term = $('#remote_search_term').val();
        add_ajax_waiting(trans ('Searching NomisWeb/ StatsWales...'));

        console.log(DataPortal.django._url_dict);

        $.ajax({
            url: DataPortal.django.urls('data_api'),
            type: 'GET',
            data: {
                'method': 'remote_search',
                'remote_api': 'nomis',
                'search_term': search_term,
                'method_data': {
                    'search_term': search_term
                }
            },
            success: function (data) {

                build_datatable(data, '#remote_results_table', "{% url 'data_api' %}");


                var dataset_radio = $('#dataset_radio');
                dataset_radio.find('input').remove().end();
                dataset_radio.find('label').remove().end();

                if (data['success'] == false) {
                    alert(trans('Sorry, an error occurred. Please try again, or report it.\n\n') + data['message'])
                } else {

                    for (var rd_radio in data['datasets']) {
                        var remote_dataset_radio = data['datasets'][rd_radio];
                        var radio_div = $('<div>');

                        radio_div.append($('<input>', {
                            value: remote_dataset_radio.id,
                            id: remote_dataset_radio.id,
                            type: 'radio',
                            name: 'nomis_search_radio',
                            text: remote_dataset_radio.name
                        }).attr({'source': remote_dataset_radio.source}));
                        radio_div.append($('<label>', {
                            value: remote_dataset_radio.id,
                            for: remote_dataset_radio.id,
                            text: remote_dataset_radio.name
                        }).attr({'source': remote_dataset_radio.source})
                            .addClass(remote_dataset_radio.source));

                        // {#                                dataset_radio.append(radio_div);#}

                    }
                    dataset_radio.buttonset();
                    dataset_radio.find('input[type=radio]').change(function () {
                        $('#add_to_map_dialog_btn').button('enable');
                    });

                    if (data['datasets'].length == 0) {
                        alert("{% trans 'Sorry, no results were found for that search.\n' %}" +
                            "{% trans 'Please refine the search terms and try again' %}");
                    } else {
                        dataset_radio.find('input[type=radio]').change(function () {
                            $('#add_to_map_dialog_btn').button('enable');
                        });
                    }
                }
            },
            error: function() {
                alert(trans('Sorry, an error occurred. Please try again, or report it.\n\n'));
            },
            complete: function() {
                ajax_finished();
            }
        });
    });

    $( "#welcome_form" ).dialog({
        autoOpen: false,
        height: DataPortal.mapping.map.map_div.height() * 0.8,
        position: {
            my: "center",
            at: "center",
            of: DataPortal.mapping.map.map_div
        },
        width: DataPortal.mapping.map.map_div.width() / 2,
        modal: true,
        buttons: [
            {
                id: 'cancel',
                text: trans ('Cancel'),
                click: function(){
                    $( this ).dialog( "close" );

                }
            },
            {
                id: 'learn_more',
                text: trans('Learn More'),
                click: function(){
                    $( this ).dialog( "close" );

                    do_tutorial();
                }
            }
        ]
    });

    $( "#search-remote-form" ).dialog({
        autoOpen: false,
        height: DataPortal.mapping.map.map_div.height() * 0.9,
        position: {
            my: "center",
            at: "center",
            of: DataPortal.mapping.map.map_div
        },
        width: DataPortal.mapping.map.map_div.width() * 0.9,
        modal: true,
        buttons: [
            // {#                    {#}
            // {#                        id: 'add_to_map_dialog_btn',#}
            // {#                        text: '{% trans 'Add to Map' %}',#}
            // {#                        disabled: true,#}
            // {#                        click: function() {#}
            // {#                            add_ajax_waiting('{% trans 'Inspecting dataset ...' %}');#}
            // {##}
            // {#                            $( this ).dialog( "close" );#}
            // {#                            var dataset_radio = $("#dataset_radio");#}
            // {#                            var dataset_id = dataset_radio.find(":radio:checked").attr('id');#}
            // {#                            var dataset_name = dataset_radio.find(":radio:checked").text();#}
            // {#                            var source = dataset_radio.find(":radio:checked").attr('source');#}
            // {##}
            // {#                            ready_and_load_remote_var_form("{% url 'data_api' %}", dataset_id, source, dataset_name);#}
            // {##}
            // {#                        }},#}
            {
                text: trans('Cancel'),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ],
        close: function() {
        }
    });
    // {#            $('#add_to_map_dialog_btn').button("disable");#}

    var dataset_define_vars_radios = [];
    function dataset_define_vars_radio_select(myRadio) {
        for (var input_select in dataset_define_vars_radios) {
        }
    }

    $( "#dataset_define_vars_form" ).dialog({
        autoOpen: false,
        height: DataPortal.mapping.map.map_div.height() * 0.8,
        position: {
            my: "center",
            at: "center",
            of: DataPortal.mapping.map.map_div
        },
        width: DataPortal.mapping.map.map_div.width()/2,
        modal: true,
        buttons: [
            {
                text: "{% trans 'Render to Map' %}",
                click: function() {


                    var codelists = $(this).data('codelists');
                    var codelist_selected = [];

                    var nomis_variable = $("#nomis_variable").val();
                    // {#                        console.log('codelists');#}
                    // {#                        console.log(codelists);#}

                    var missing_measures = [];
                    for(var remote_codelist in codelists) {
                        var codelist_selector = "div[id='" + remote_codelist + "_radio']";
                        var remote_codelist_selected_item = $(codelist_selector).find(":radio:checked");
                        var remote_codelist_selection = remote_codelist_selected_item.attr('value');

                        if (remote_codelist_selection == null) {
                            missing_measures.push(codelists[remote_codelist]['name']);
                        }

                        codelist_selected.push({
                            option: remote_codelist,
                            variable: remote_codelist_selection
                        });
                        if (remote_codelist == 'MEASURES') {
                            nomis_variable = remote_codelist_selection;
                        }
                    }


                    // {#                        console.log(codelist_selected);#}

                    var dataset_id = $(this).data('dataset_id');
                    var source = $(this).data('source');

                    var topojson_geography = $('#topojson_geography_radio').find(":radio:checked").attr('value');
                    if (topojson_geography == null) {
                        missing_measures.push("{% trans 'Geography' %}");
                    }
                    if (missing_measures.length > 0) {
                        var err_msg = trans('Please select an option for each selection : \n\n') + missing_measures.join('\n');
                        alert(err_msg);
                        return;
                    }

                    $( this ).dialog( "close" );

                    add_ajax_waiting(trans('Fetching map layer...'));

                    get_remote_dataset_topojson(
                        "{% url 'remote_data_topojson' %}",
                        topojson_geography,
                        dataset_id,
                        codelist_selected,
                        source,
                        function(data){
                            get_remote_dataset_csv_url(
                                "{% url 'data_api' %}",
                                topojson_geography,
                                dataset_id,
                                codelist_selected,
                                function(csv_url) {

                                    ajax_finished();
                                    var layer_name = data['search_uuid'];
                                    topojson_layers[layer_name] = data['topojson'];
                                    $( "#chloropleth_option_form").data({
                                        layer_names: layer_name,
                                        nomis_variable: nomis_variable,
                                        csv_url: csv_url
                                    }).dialog( "open" );
                                }
                            );
                        }
                    );
                }
            },
            {
                text: trans('Cancel'),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ],
        close: function() {
        }
    });

    // {#            $('#screenshot').click(function() {#}
    // {#                leafletImage(map, screenshot_open_tab);#}
    // {#            });#}

    function do_screenshot(map_canvas, callback) {
        html2canvas(
            DataPortal.mapping.map.map_div.find('> div.leaflet-control-container > div.leaflet-bottom.leaflet-left'), {}
        ).then(function(left_overlay_canvas) {

            var ctx3 = map_canvas.getContext('2d');
            ctx3.drawImage(
                left_overlay_canvas,
                0,
                map_canvas.height - left_overlay_canvas.height
            );

            html2canvas(
                DataPortal.mapping.map.map_div.find('> div.leaflet-control-container > div.leaflet-bottom.leaflet-right'), {}
            ).then(function(right_overlay_canvas) {
                ctx3.drawImage(
                    right_overlay_canvas,
                    map_canvas.width - right_overlay_canvas.width,
                    map_canvas.height - right_overlay_canvas.height
                );


                html2canvas(
                    map_div.find('> div.leaflet-control-container > div.leaflet-top.leaflet-right > div.powered_by'), {}
                ).then(function(right_overlay_canvas) {
                    ctx3.drawImage(
                        right_overlay_canvas,
                        map_canvas.width - right_overlay_canvas.width,
                        0
                    );

                    var canvas_data_url = map_canvas.toDataURL("image/png", 0.5);

                    if (callback) {
                        callback(canvas_data_url);
                    }
                    return canvas_data_url;
                });
            });
        });
    }

    function reset_map() {
        DataPortal.mapping.map.map.setView([52.4, -3.51], 8);
    }

    function take_screenshot() {
        leafletImage(DataPortal.mapping.map.map, do_screenshot_open_tab);
    }

    function do_screenshot_open_tab(err, map_canvas) {
        do_screenshot(map_canvas, function(canvas_data_url){
            window.open(canvas_data_url, '_blank');
        });
    }

    // {#            var local_dataset_define_vars_radios = [];#}
    // {#            function local_dataset_define_vars_radio_select(myRadio) {#}
    // {#                for (var input_select in local_dataset_define_vars_radios) {#}
    // {#                }#}
    // {#            }#}

    $( "#local_dataset_define_vars_form" ).dialog({
        autoOpen: false,
        height: DataPortal.mapping.map.map_div.height() * 0.8,
        position: {
            my: "center",
            at: "center",
            of: DataPortal.mapping.map.map_div
        },
        width: DataPortal.mapping.map.map_div.width()/2,
        modal: true,
        open: function( event, ui ) {
//                   Clear this out
            // {#                    local_dataset_define_vars_radios = [];#}

            var available_data = $(this).data('available_data');
            var unicode_data = $(this).data('unicode_data');

            var dataset_radio = $('#local_data_cell_radio');
            dataset_radio.find('div').remove().end();

            var codelist_label = $('<div>', {text: 'Available Data'});
            dataset_radio.append(codelist_label);

            var codelist_radio_div = $('<div>', {id: 'local_available_data_radio'});
            for(var available_data_option_idx in available_data) {
                var available_data_option = available_data[available_data_option_idx];

                var radio_text = '';
                if (available_data_option['full_name']){
                    radio_text = available_data_option['full_name'];
                } else {
                    radio_text = available_data_option['data_name']
                }

                var radio_div = $('<div>');
                var radio_input = $('<input>', {
                    value: available_data_option['data_name'],
                    id: available_data_option['data_name'],
                    type: 'radio',
                    name: 'available_data_option',
                    text: radio_text
                });
                radio_div.append(radio_input);
                radio_div.append($('<label>', {
                    class: 'dialog_radio_option',
                    value: available_data_option['data_name'],
                    for: available_data_option['data_name'],
                    text: radio_text
                }));
                codelist_radio_div.append(radio_div);
            }

            for(var available_data_option_idx in unicode_data) {
                var available_data_option = unicode_data[available_data_option_idx];

                var uradio_text = '';
                if (available_data_option['full_name']){
                    uradio_text = available_data_option['full_name'];
                } else {
                    uradio_text = available_data_option['data_name']
                }

                var radio_div = $('<div>');
                var radio_input = $('<input>', {
                    value: available_data_option['data_name'],
                    id: available_data_option['data_name'],
                    type: 'radio',
                    name: 'available_data_option',
                    text: uradio_text
                });
                radio_div.append(radio_input);
                radio_div.append($('<label>', {
                    class: 'dialog_radio_option',
                    value: available_data_option['data_name'],
                    for: available_data_option['data_name'],
                    text: uradio_text + ' category'
                }));
                codelist_radio_div.append(radio_div);
            }

            codelist_radio_div.buttonset();
            dataset_radio.append(codelist_radio_div);
            codelist_radio_div.find('input')[0].click();

        },
        buttons: [
            {
                text: trans('Render to Map'),
                click: function() {
                    add_ajax_waiting(trans('Fetching map layer...'));
                    $( this ).dialog( "close" );

                    var local_available_data_selection = $('#local_available_data_radio').find(":radio:checked").attr('value');

                    var survey_id = $(this).data('survey_id');

                    // {#                        var topojson_geography = $('#topojson_geography_radio').find(":radio:checked").attr('value');#}
                    var topojson_geography = $(this).data('boundary_name');


                    get_local_dataset_topojson(
                        "{% url 'local_data_topojson' %}",
                        topojson_geography,
                        survey_id,
                        local_available_data_selection,
                        function(data) {
                            ajax_finished();

                            var layer_name = data['search_uuid'];
                            topojson_layers[layer_name] = data['topojson'];

                            $( "#chloropleth_option_form").data({
                                layer_names: layer_name,
                                nomis_variable: '20301',
                                csv_url: ''
                            }).dialog( "open" );
                        }
                    );

                }
            },
            {
                text: trans('Cancel'),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });


    var local_data_layer_data = DataPortal.mapping.local_data_layers();
    for (var local_data_layer_idx in local_data_layer_data) {

        (function(){
            var local_data_layer = local_data_layer_data[local_data_layer_idx];
            // {#                console.log(local_data_layer);#}

            (function(){
                get_local_dataset_metadata(
                    DataPortal.django.urls('data_api'),
                    local_data_layer['survey_id'],
                    local_data_layer['boundary_name'],
                    function(metadata){
                        // {#                                    alert(metadata['local_data_metadata']['data_names']);#}
                        $("#local_dataset_define_vars_form").data({
                            survey_id: local_data_layer['survey_id'],
                            source: local_data_layer['source'],
                            boundary_name: local_data_layer['boundary_name'],
                            available_data: metadata['local_data_metadata']['data_names'],
                            unicode_data: metadata['local_data_metadata']['unicode_data']
                        }).dialog('open');
                    }
                );
            })();

            local_data_layer['colorpicker'] = 'Spectral';
            local_data_layer['bin_type'] = 'k';
            local_data_layer['bin_num'] = '8';
            local_data_layer['data_name'] = 'data_name';

        }());
    }

    // {#        var local_search_layer_data = {{ local_searches|jsonify }};#}
    // {#        do_local_layers(local_search_layer_data, "{% url 'remote_data_topojson' %}");#}

    var layer_uuids = DataPortal.mapping.layer_uuids();
    do_layer_uuids(layer_uuids, DataPortal.django.urls('data_api'));

    function do_layer_uuids(layer_uuids, search_layer_topojson_url) {
        for (var uuid_idx in layer_uuids) {
            var uuid = layer_uuids[uuid_idx];
            do_layer_single_uuid(uuid, search_layer_topojson_url);
        }
    }

    function do_layer_single_uuid(uuid, search_layer_topojson_url) {

        window.location.hash += '/' + uuid;

        add_ajax_waiting(trans('Fetching map layer...'));

        $.ajax({
            url: search_layer_topojson_url,
            type: 'GET',
            data: {
                method: 'search_layer_topojson',
                search_uuid: uuid
            },
            success: function (topojson_data) {
                // {#                        console.log(topojson_data);#}

                var layer_data = topojson_data['layer_data'];

                handleUploadedLayer(
                    topojson_data['topojson'],
                    layer_data['colorpicker'],
                    layer_data['bin_type'],
                    layer_data['bin_num'],
                    '',
                    layer_data['name'],
                    '',
                    layer_data
                );
            },
            complete: function() {
                ajax_finished();
            }
        });
    }


    function do_layer_by_name(name) {
        add_ajax_waiting(trans('Fetching map layer...'));
        $.ajax({
            url: DataPortal.django.urls('data_api'),
            type: 'GET',
            data: {
                method: 'topojson_layer_by_name',
                name: name
            },
            success: function (topojson_data) {
                handleUploadedLayer(
                    topojson_data['topojson'],
                    topojson_data['layer_data']['colorpicker'],
                    topojson_data['layer_data']['bin_type'],
                    topojson_data['layer_data']['bin_num'],
                    '',
                    topojson_data['layer_data']['name'],
                    '', topojson_data['layer_data']
                );
            },
            complete: function() {
                ajax_finished();
            }
        });
    }
    // {#        lsoa_pembrokshire_point#}
    // {#        'pcode_district'#}
    // {#        'pcode_point'#}
    // {#                        do_layer_by_name('pcode_point');#}

    var remote_data_layer_data = DataPortal.mapping.remote_searches();
    for (var remote_data_layer_idx in remote_data_layer_data) {

        (function(){
            var remote_data_layer = remote_data_layer_data[remote_data_layer_idx];
            // {#                console.log(remote_data_layer);#}

            get_remote_dataset_topojson(
                "{% url 'remote_data_topojson' %}",
                remote_data_layer['geography_id'],
                remote_data_layer['dataset_id'],
                remote_data_layer['codelist'],
                remote_data_layer['source'],
                function(topojson_data) {
                    // {#                            console.log(remote_data_layer);#}

                    handleUploadedLayer(
                        topojson_data['topojson'],
                        remote_data_layer['colorpicker'],
                        remote_data_layer['bin_type'],
                        remote_data_layer['bin_num'],
                        '',
                        remote_data_layer['name'],
                        '',
                        remote_data_layer
                    );
                }
            );
        }());
    }

    var remote_layer_mapping = DataPortal.mapping.remote_data_layers();
    for (var remote_data_map_idx in remote_layer_mapping) {
        var remote_data_map = remote_layer_mapping[remote_data_map_idx];

        ready_and_load_remote_var_form(
            "{% url 'data_api' %}",
            remote_data_map['id'],
            remote_data_map['src'],
            '0001'
        );
    }


    $( "#local-data-form" ).dialog({
        autoOpen: false,
        height: DataPortal.mapping.map.map_div.height() * 0.8,
        position: {
            my: "center",
            at: "center",
            of: DataPortal.mapping.map.map_div
        },
        width: DataPortal.mapping.map.map_div.width() * 0.8,
        modal: true,
        buttons: [
            {
                id: 'save_local_data_dialog_btn',
                text: trans('Save'),
                click: function() {

                    var local_data_name = $('#local_data_name_input').val();
                    var local_data_boundary = $('#local_data_boundary_select').val();
                    var local_data_value_column = $('#local_data_value_radio').find(":radio:checked").attr('value');
                    var local_data_geography_column = $('#local_data_geography_radio').find(":radio:checked").attr('value');
                    if(local_data_geography_column == null || local_data_value_column == null) {
                        alert("{% trans 'Please select a Geography ID column and a data value column' %}");
                    } else {
                        add_ajax_waiting(trans('Fetching map layer...'));

                        var topojson_layer_name = '';
                        var codes = [];
                        var ordered_data = {};
                        for (var area in area_values) {
                            if (area_values.hasOwnProperty(area)) {

                                var geo_string = area_values[area][local_data_geography_column];

                                if (geo_string != null) {

                                    if (isPostcodeish(geo_string)) {
                                        topojson_layer_name = 'pcode_point';

                                        //    Need to format this in a way we expect:
                                        //    AA111AA or AA1 1AA - not 'AA11 1AA'
                                        //    console.log(geo_string);
                                        //    second thoughts, do it later to retain XLS value as a key

                                        if (geo_string.length > 7) {
                                            // {#                                            console.log('>7');#}
                                            geo_string = geo_string.slice(0, 4) + geo_string.slice(5, geo_string.length);
                                            // {#                                            console.log(geo_string);#}
                                        }
                                        codes.push(geo_string.slice(0, -2))
                                    }

                                    else if (geo_string.length > 3 && geo_string.substring(0, 3) == 'W01') {
                                        topojson_layer_name = 'lsoa';
                                        codes.push(geo_string.slice(0, -1));
                                    }

                                    else if (geo_string.length > 3 && geo_string.substring(0, 3) == 'W09') {
                                        topojson_layer_name = 'assembly_constituency';
                                        codes.push(geo_string);
                                    }

                                    else if (geo_string.length > 3 && geo_string.substring(0, 3) == 'W10') {
                                        topojson_layer_name = 'assembly_region';
                                        codes.push(geo_string);
                                    }

                                    else {
                                        topojson_layer_name = local_data_boundary;
                                        codes.push(geo_string);
                                    }

                                    ordered_data[geo_string] = area_values[area][local_data_value_column];
                                }
                            }
                        }

                        codes = _.uniq(codes);
                        console.log('XLS found ' + Object.keys(ordered_data).length + ' items');

                        $.ajax({
                            url: DataPortal.django.urls('data_api'),
                            type: 'GET',
                            data: {
                                method: 'topojson_layer_by_name',
                                name: topojson_layer_name,
                                codes: codes
                            },
                            success: function (all_topojson_data) {

                                var secondary_data_keys = [];
                                $('#local_data_secondary_check').find(":checkbox:checked").each(function (index) {
                                    secondary_data_keys.push($(this).attr('value'));
                                });
                                console.log('outer 2nd keys');
                                console.log(secondary_data_keys);
                                all_topojson_data = thing(all_topojson_data, ordered_data, local_data_name,
                                    area_values, local_data_geography_column, secondary_data_keys);

                                // {#                                    console.log(jQuery.extend(true, {}, all_topojson_data));#}

                                var layer_name = all_topojson_data['search_uuid'];
                                topojson_layers[layer_name] = all_topojson_data['topojson'];

                                $('#layer_name_text_entry').val(local_data_name);

                                $( "#chloropleth_option_form").data({
                                    layer_names: layer_name,
                                    nomis_variable: '20301',
                                    csv_url: '',
                                    localStorage: true,
                                    all_topojson_data: all_topojson_data
                                }).dialog( "open" );
                            },
                            error: function (xhr, ajaxOptions, thrownError) {
                                console.log(xhr);
                                console.log(ajaxOptions);
                                console.log(thrownError);

                                alert(xhr.status);
                                alert(thrownError);
                            },
                            complete: function() {
                                ajax_finished();
                                $("#local-data-form").dialog( "close" );
                            }
                        });


                    }
                }
            },
            {
                text: trans('Cancel'),
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
            // {#                    {#}
            // {#                        text: '{% trans 'Help' %}',#}
            // {#                        id: 'mapmydata_help',#}
            // {#                        click: do_mapmydata_tutorial#}
            // {#                    }#}
        ],
        close: function() {
        }
    });



    if (localStorage.DataPortalLocalLayers) {

        var localLayers = JSON.parse(localStorage.getItem('DataPortalLocalLayers'));

        var local_layer_names = Object.keys(localLayers);


        // {#                alert('You have ' + local_layer_names.length + ' layers stored locally :\n\n ' + local_layer_names);#}

        for (var name in local_layer_names) {
            if (local_layer_names.hasOwnProperty(name)) {

                var topojson_data = localLayers[local_layer_names[name]];
                handleUploadedLayer(
                    topojson_data['topojson'],
                    topojson_data['layer_data']['colorpicker'],
                    topojson_data['layer_data']['bin_type'],
                    topojson_data['layer_data']['bin_num'],
                    '',
                    topojson_data['layer_data']['name'],
                    '', topojson_data['layer_data']
                );
            }
        }
    }


    var X = XLSX;
    var XW = {
        /* worker message */
        msg: 'xlsx',
        /* worker scripts */
        rABS: './xlsxworker2.js',
        norABS: './xlsxworker1.js',
        noxfer: './xlsxworker.js'
    };

    var rABS = typeof FileReader !== "undefined" && typeof FileReader.prototype !== "undefined" && typeof FileReader.prototype.readAsBinaryString !== "undefined";
    if(!rABS) {
        document.getElementsByName("userabs")[0].disabled = true;
        document.getElementsByName("userabs")[0].checked = false;
    }

    var use_worker = typeof Worker !== 'undefined';
    if(!use_worker) {
        document.getElementsByName("useworker")[0].disabled = true;
        document.getElementsByName("useworker")[0].checked = false;
    }

    var transferable = use_worker;
    if(!transferable) {
        document.getElementsByName("xferable")[0].disabled = true;
        document.getElementsByName("xferable")[0].checked = false;
    }

    var wtf_mode = false;

    function fixdata(data) {
        var o = "", l = 0, w = 10240;
        for(; l<data.byteLength/w; ++l) o+=String.fromCharCode.apply(null,new Uint8Array(data.slice(l*w,l*w+w)));
        o+=String.fromCharCode.apply(null, new Uint8Array(data.slice(l*w)));
        return o;
    }

    function ab2str(data) {
        var o = "", l = 0, w = 10240;
        for(; l<data.byteLength/w; ++l) o+=String.fromCharCode.apply(null,new Uint16Array(data.slice(l*w,l*w+w)));
        o+=String.fromCharCode.apply(null, new Uint16Array(data.slice(l*w)));
        return o;
    }

    function s2ab(s) {
        var b = new ArrayBuffer(s.length*2), v = new Uint16Array(b);
        for (var i=0; i != s.length; ++i) v[i] = s.charCodeAt(i);
        return [v, b];
    }

    function xw_noxfer(data, cb) {
        var worker = new Worker(XW.noxfer);
        worker.onmessage = function(e) {
            switch(e.data.t) {
                case 'ready': break;
                case 'e': console.error(e.data.d); break;
                case XW.msg: cb(JSON.parse(e.data.d)); break;
            }
        };
        var arr = rABS ? data : btoa(fixdata(data));
        worker.postMessage({d:arr,b:rABS});
    }

    function xw_xfer(data, cb) {
        var worker = new Worker(rABS ? XW.rABS : XW.norABS);
        worker.onmessage = function(e) {
            switch(e.data.t) {
                case 'ready': break;
                case 'e': console.error(e.data.d); break;
                default: xx=ab2str(e.data).replace(/\n/g,"\\n").replace(/\r/g,"\\r"); console.log("done"); cb(JSON.parse(xx)); break;
            }
        };
        if(rABS) {
            var val = s2ab(data);
            worker.postMessage(val[1], [val[1]]);
        } else {
            worker.postMessage(data, [data]);
        }
    }

    function xw(data, cb) {
        transferable = document.getElementsByName("xferable")[0].checked;
        if(transferable) xw_xfer(data, cb);
        else xw_noxfer(data, cb);
    }

    function to_json(workbook) {
        var result = {};
        workbook.SheetNames.forEach(function(sheetName) {
            var roa = X.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
            if(roa.length > 0){
                result[sheetName] = roa;
            }
        });
        return result;
    }

    function to_csv(workbook) {
        var result = [];
        workbook.SheetNames.forEach(function(sheetName) {
            var csv = X.utils.sheet_to_csv(workbook.Sheets[sheetName]);
            if(csv.length > 0){
                result.push("SHEET: " + sheetName);
                result.push("");
                result.push(csv);
            }
        });
        return result.join("\n");
    }



    function process_wb(wb) {
        var output_json = to_json(wb);
        var output = JSON.stringify(output_json, 2, 2);
        do_layer_single_local(output_json);

        if(typeof console !== 'undefined') console.log("output", new Date());
    }

    var drop = document.getElementById('drop');
    function handleDrop(e) {
        e.stopPropagation();
        e.preventDefault();
        rABS = document.getElementsByName("userabs")[0].checked;
        use_worker = document.getElementsByName("useworker")[0].checked;
        var files = e.dataTransfer.files;
        var f = files[0];
        {
            var reader = new FileReader();
            var name = f.name;
            reader.onload = function(e) {
                if(typeof console !== 'undefined') console.log("onload", new Date(), rABS, use_worker);
                var data = e.target.result;
                if(use_worker) {
                    xw(data, process_wb);
                } else {
                    var wb;
                    if(rABS) {
                        wb = X.read(data, {type: 'binary'});
                    } else {
                        var arr = fixdata(data);
                        wb = X.read(btoa(arr), {type: 'base64'});
                    }
                    process_wb(wb);
                }
            };
            if(rABS) reader.readAsBinaryString(f);
            else reader.readAsArrayBuffer(f);
        }
    }

    function handleDragover(e) {
        e.stopPropagation();
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
    }

    if(drop.addEventListener) {
        drop.addEventListener('dragenter', handleDragover, false);
        drop.addEventListener('dragover', handleDragover, false);
        drop.addEventListener('drop', handleDrop, false);
    }


    var xlf = document.getElementById('xlf');
    function handleFile(e) {
        rABS = document.getElementsByName("userabs")[0].checked;
        use_worker = document.getElementsByName("useworker")[0].checked;
        var files = e.target.files;
        var f = files[0];
        {
            var reader = new FileReader();
            var name = f.name;
            reader.onload = function(e) {
                if(typeof console !== 'undefined') console.log("onload", new Date(), rABS, use_worker);
                var data = e.target.result;
                if(use_worker) {
                    xw(data, process_wb);
                } else {
                    var wb;
                    if(rABS) {
                        wb = X.read(data, {type: 'binary'});
                    } else {
                        var arr = fixdata(data);
                        wb = X.read(btoa(arr), {type: 'base64'});
                    }
                    process_wb(wb);
                }
            };
            if(rABS) reader.readAsBinaryString(f);
            else reader.readAsArrayBuffer(f);
        }
    }

    if(xlf.addEventListener) xlf.addEventListener('change', handleFile, false);

    var area_values = {};
    function do_layer_single_local(json_object) {

        console.log(json_object);

        $('#local-data-drop-zone').hide();

        ordered_data = {};
        var worksheet_name = Object.keys(json_object)[0];
        area_values = json_object[worksheet_name];
        var column_headers = Object.keys(area_values[0]);

        var dataset_radio = $('#local_column_headers_radio');
        dataset_radio.find('div').remove().end();
        // {#                dataset_radio.addClass('row');#}

        $('#mapmydata_help').off('click').on('click', do_mapmydata_tutorial_2);

        var geog_column = $('<div>').addClass('col-md-4 col-sm-12');
        var codelist_label = $('<div>', {
            text: trans('Select geography id column'),
            id: 'geography_label'
        });
        geog_column.append(codelist_label);

        var codelist_radio_div = $('<div>', {id: 'local_data_geography_radio'});
        for(var column_header_idx in column_headers) {
            if(column_headers.hasOwnProperty(column_header_idx))
                var column_header_option = column_headers[column_header_idx];

            var radio_text = column_header_option;

            var radio_div = $('<div>');
            radio_div.append($('<input>', {
                value: column_header_option,
                id: column_header_option,
                type: 'radio',
                name: 'available_data_option',
                text: radio_text
            }));
            radio_div.append($('<label>', {
                class: 'dialog_radio_option',
                value: column_header_option,
                for: column_header_option,
                text: radio_text
            }));
            codelist_radio_div.append(radio_div);
        }
        codelist_radio_div.buttonset();
        geog_column.append(codelist_radio_div);

        dataset_radio.append(geog_column);




        var data_column = $('<div>').addClass('col-md-4 col-sm-12');


        var codelist_label = $('<div>', {
            text: trans('Select data value column'),
            id: 'data_column_label'
        });
        data_column.append(codelist_label);

        var local_data_value_radio_div = $('<div>', {id: 'local_data_value_radio'});
        for(var column_header_idx in column_headers) {
            if(column_headers.hasOwnProperty(column_header_idx))
                var column_header_option = column_headers[column_header_idx];
            // {#                        var radio_text = column_header_option;#}

            var radio_div = $('<div>');
            radio_div.append($('<input>', {
                value: column_header_option,
                id: column_header_option + '_value',
                type: 'radio',
                name: 'local_data_value_option',
                text: column_header_option
            }));
            radio_div.append($('<label>', {
                class: 'dialog_radio_option',
                value: column_header_option,
                for: column_header_option + '_value',
                text: column_header_option
            }));
            local_data_value_radio_div.append(radio_div);
        }
        var radio_div = $('<div>');
        radio_div.append($('<input>', {
            value: 'local_data_no_value',
            id: 'local_data_no_value_radio',
            type: 'radio',
            name: 'local_data_value_option',
            text: 'Pointer Only'
        }));
        radio_div.append($('<label>', {
            class: 'dialog_radio_option',
            value: column_header_option,
            for: 'local_data_no_value_radio',
            text: 'Pointer Only'
        }));
        local_data_value_radio_div.append(radio_div);
        local_data_value_radio_div.buttonset();
        data_column.append(local_data_value_radio_div);

        dataset_radio.append(data_column);


        var codelist_column = $('<div>').addClass('col-md-4 col-sm-12');


        var codelist_label = $('<div>', {
            text: trans('Select additional secondary data'),
            id: 'secondary_data_label'
        });
        codelist_column.append(codelist_label);

        var local_data_secondary_check_div = $('<div>', {id: 'local_data_secondary_check'});
        for(var column_header_idx in column_headers) {
            if(column_headers.hasOwnProperty(column_header_idx))
                var column_header_option = column_headers[column_header_idx];

            var radio_text = column_header_option;

            var radio_div = $('<div>');
            radio_div.append($('<input>', {
                value: column_header_option,
                id: column_header_option + '_secondary',
                type: 'checkbox',
                name: 'local_data_secondary_option',
                text: radio_text
            }));
            radio_div.append($('<label>', {
                class: 'dialog_radio_option',
                value: column_header_option,
                for: column_header_option + '_secondary',
                text: radio_text
            }));
            local_data_secondary_check_div.append(radio_div);
        }
        local_data_secondary_check_div.buttonset();
        codelist_column.append(local_data_secondary_check_div);

        dataset_radio.append(codelist_column);
    }






    if ($.cookie("WDP_returning_user")) {
        var view = parseInt($.cookie("WDP_returning_user"));
        view += 1;
        $.cookie("WDP_returning_user", view, {expires: 365, path: '/'});
        // {#                $('#welcome_form').dialog('open');#}

    } else {
        $('#welcome_form').dialog('open');
        $.cookie("WDP_returning_user", 0, {expires: 365, path: '/'});
    }


















































































    function add_geojson(data, name) {
        // {#                console.log('Adding new data ' + name);#}
        // {#                console.log(data);#}

        // {#                                var geojson_obj = L.geoJson();#}
        var geojson_obj = L.Proj.geoJson();
        geojson_obj.addData(data, {
            style: function (feature) {
                return {
                    fillColor: '#0044AA',
                    fillOpacity: 0.7,
                    weight: 2,
                    opacity: 1,
                    color: 'orangered',
                    dashArray: '3'
                };
            }
        });

        geojson_obj.on({
            click: function(e) {
                console.log(data);

                var content = '';
                if (data.hasOwnProperty('properties')) {

                    if (data['properties'].hasOwnProperty('html')) {
                        content += data['properties']['html'];
                    }
                    if (data['properties'].hasOwnProperty('name')) {
                        content += data['properties']['name'] + '\n</br>';
                    }
                    if (data['properties'].hasOwnProperty('postcode')) {
                        content += data['properties']['postcode'] + '\n</br>';
                    }
                    if (data['properties'].hasOwnProperty('number_of_households')) {
                        content += 'Households: ' + data['properties']['number_of_households'] + '\n</br>';
                    }
                    if (data['properties'].hasOwnProperty('scheme_number_of_members')) {
                        content += 'Members: ' + data['properties']['scheme_number_of_members'] + '\n</br>';
                    }
                    if (data['properties'].hasOwnProperty('id')) {
                        content += data['properties']['id'];
                    }
                }

                L.popup()
                    .setLatLng(e.latlng)
                    .setContent(content)
                    .openOn(DataPortal.mapping.map.map);
            }
        });



        var display_name = name;
        if (data.hasOwnProperty('properties')) {
            if (data['properties'].hasOwnProperty('name')) {
                display_name = data['properties']['name'];
            }

            if (data['properties'].hasOwnProperty('fields')) {
                if (data['properties']['fields'].hasOwnProperty('_')) {
                    display_name = data['properties']['fields']['_'];
                }
                if (data['properties']['fields'].hasOwnProperty('Primary_Catchment')) {
                    display_name = data['properties']['fields']['Primary_Catchment'];
                }
                if (data['properties']['fields'].hasOwnProperty('Welsh_Medium_Catchment')) {
                    display_name = data['properties']['fields']['Welsh_Medium_Catchment'];
                }
                if (data['properties']['fields'].hasOwnProperty('Secondary_School_Current_Clusters')) {
                    display_name = data['properties']['fields']['Secondary_School_Current_Clusters'];
                }
                if (data['properties']['fields'].hasOwnProperty('Secondary__School__Current__Clusters')) {
                    display_name = data['properties']['fields']['Secondary__School__Current__Clusters'];
                }
                if (data['properties']['fields'].hasOwnProperty('School_Name')) {
                    display_name = data['properties']['fields']['School_Name'];
                }
            }
        }
        // {#                console.log(name + ' ' + display_name);#}

        DataPortal.mapping.map.layerControl.addOverlay(geojson_obj, display_name);
        geojson_obj.addTo(DataPortal.mapping.map.map);
        // {#                map.fitBounds(geojson_obj.getBounds(), { paddingBottomRight: [200, 0] });#}

    }


    var do_nhw = false;

    if(do_nhw) {
        $.ajax({
            url: "{% static 'big.geojson' %}",
            type: 'GET',
            data: {},
            crossDomain: true,
            dataType: 'json',
            success: function (data) {
                // {#                    console.log(data);#}
                // {#                    alert(data.length);#}
                for (var feature_idx in data['features']) {
                    // {#                        console.log(data['features'][feature_idx]);#}

                    add_geojson(data['features'][feature_idx], 'nw');
                }
                // {#                    add_geojson(data, 'nw');#}


            },
            error: function () {
                alert('Sorry, an error occurred. Please try again, or report it.')
            },
            complete: function () {
            }
        });

    }

    $('#point_data_icon_select').toggle(true);

    // {#            $( "#chloropleth_option_form").data({#}
    // {#                layer_names: 'remove me',#}
    // {#                nomis_variable: '20301',#}
    // {#                csv_url: ''#}
    // {#            }).dialog( "open" );#}



    $.ajax({
        url: DataPortal.django.static_urls('lle.json'),
        type: 'GET',
        data: {},
        crossDomain: true,
        dataType: 'json',
        success: function (data) {

            console.log(data);

            var options = {
                valueNames: [
                    'name',
                    { name: 'tile_name', attr: 'data-layer_name'},
                    { name: 'source', attr: 'data-layer_url'
                    },
                    { name: 'legend_img', attr: 'data-legend_img'
                    },
                    { name: 'wfs_namespace', attr: 'data-wfs_namespace'
                    },
                    { name: 'wfs_geometry_field', attr: 'data-wfs_geometry_field'
                    }
                ],
                item: '<li><a href="#" data-wfs="true" class="wms_toggle lle_flex tile_name source legend_img wfs_namespace wfs_geometry_field"><i class="fa fa-map-marker fa-fw"></i><p class="name"></p></a></li>'

            };

            var userList = new List('lle_wms', options, data);

            $('.wms_toggle').click(function () {
                DataPortal.mapping.LayerStore.toggle_layer(this)
            });

        },
        error: function () {
            alert('Sorry, an error occurred. Please try again, or report it.')
        },
        complete: function () {
        }
    });


    if (DataPortal.tpt == 'm4w') {
        var policy_papers_options = {
            valueNames: ['name']
        };
        var policyPaperList = new List('policy_papers', policy_papers_options);
    }

    $('.secondary_info').click(function () {

        var has_info = $(this).data('secondary_info');
        var qualdcinfo_id = $(this).data('qualdcinfo');
        var qualdcinfo_short_list = $(this).data('qualdcinfo_short_list');

        if (qualdcinfo_short_list) {

            var right_pane = $('#right-component1');
            right_pane.html('<h2>Policy Details</h2>');

            var qual_dc_ids = qualdcinfo_short_list.split(',');
            for (var idx in qual_dc_ids) {
                $.ajax({
                    url: DataPortal.django.urls(
                        'api:metadata:QualDcInfo-detail',
                        {pk: qual_dc_ids[idx]}
                    ),
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        var qualdcinfo_short_list_html = '<h4>Title</h4><p>' + data['title'] + '</p><h4>Link</h4><p>' + data['source'] + '</p>';
                        $('<div/>').html(urlify(qualdcinfo_short_list_html)).addClass('sidebar_group').appendTo(right_pane);
                    },
                    error: function() {}
                });
            }

        }

        if (qualdcinfo_id) {
            $.ajax({
                url: DataPortal.django.urls(
                    'api:metadata:QualDcInfo-detail',
                    {pk: qualdcinfo_id}
                ),
                type: 'GET',
                dataType: 'json',
                success: function(data) {
                    var qual_dc_keys = ['title','subject','description','publisher','contributor',
                        'date','type','format','source','language'];

                    var model_data = '';
                    for (var idx in qual_dc_keys) {
                        var key = qual_dc_keys[idx];
                        if (data[key] && data[key].length) {
                            model_data += '<h4>' + titleCase(key) + '</h4><p>' + data[key] + '</p>';
                        }
                    }

                    var info_text = '<h2>Record Details</h2>' + model_data;
                    var right_pane = $('#right-component1');
                    right_pane.html(urlify(info_text));
                },
                error: function(){
                    var info_text = '<h2>Record Details</h2><p>None found</p>';
                    var right_pane = $('#right-component1');
                    right_pane.html(urlify(info_text));
                }
            });
        }





    });

});
    
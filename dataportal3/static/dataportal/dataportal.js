/**
 * Created by ubuntu on 19/11/15.
 */

// function get_i18n_text(text_key, lang_key) {
//     // alert(text_key + ' : ' + lang_key);
//
//     if(i18n_text.hasOwnProperty(text_key)) {
//         var text_set = i18n_text[text_key];
//         if(text_set.hasOwnProperty(lang_key)) {
//             return i18n_text[text_key][lang_key];
//         } else {
//             return text_key + ' : ' + lang_key
//         }
//     } else {
//         return text_key;
//     }
//
// }

function get_remote_dataset_csv_url(data_api_url, topojson_geography, dataset_id, codelist_selected, callback) {
    var csv_url = '';
    $.ajax({
        url: data_api_url,
        type: 'GET',
        data: {
            'method': 'data_urls',
            'geography': topojson_geography,
            'dataset_id': dataset_id,
            'codelist_selected': JSON.stringify(codelist_selected)
        },
        success: function (data) {
            csv_url = data['data_urls']['dataset_url_csv'];
        },
        error: function () {
            alert('Sorry, an error occurred. Please try again, or report it.')
        },
        complete: function () {
            callback(csv_url);
        }
    });
}

function get_remote_dataset_topojson(remote_data_topojson_url, topojson_geography,
                                     dataset_id, codelist_selected, source, callback) {
    $.ajax({
        url: remote_data_topojson_url,
        type: 'GET',
        data: {
            'geography': topojson_geography,
            'dataset_id': dataset_id,
            'codelist_selected': JSON.stringify(codelist_selected),
            'source': source
        },
        success: function(data){
            callback(data);
        },
        error: function() {
            alert('Sorry, an error occurred. Please try again, or report it.')
        },
        complete: function() {
            waitingDialog.hide();
        }
    })
}

function get_local_dataset_metadata(local_data_metadata_url, survey_id, boundary_name, callback) {
    $.ajax({
        url: local_data_metadata_url,
        type: 'GET',
        data: {
            'method': 'local_data_metadata',
            'survey_id': survey_id,
            'boundary_name': boundary_name
        },
        success: function(data){
            callback(data);
        },
        error: function() {
            alert('Sorry, an error occurred. Please try again, or report it.')
        },
        complete: function() {
            waitingDialog.hide();
        }
    })
}

function get_local_dataset_topojson(local_data_topojson_url, boundary_name, survey_id, data_name, callback) {
    $.ajax({
        url: local_data_topojson_url,
        type: 'GET',
        data: {
            'boundary_name': boundary_name,
            'survey_id': survey_id,
            'data_name': data_name
        },
        success: function(data){
            callback(data);
        },
        error: function() {
            alert('Sorry, an error occurred. Please try again, or report it.')
        },
        complete: function() {
            waitingDialog.hide();
        }
    })
}

function isPostcodeish(input_string) {
    var re = /(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))/g;
    return re.exec(input_string)
}

function thing(all_topojson_data, ordered_data, local_data_name,
               area_values, local_data_geography_column,
               secondary_data_keys) {

    var topojson_data = all_topojson_data['topojson'];

    // Collected name for all the geometries
    var geom_name = Object.keys(topojson_data['objects'])[0];

    //The geometry objects
    var geometries = topojson_data['objects'][geom_name]['geometries'];

    //An array to add the modified geometries to, instead of making changes in-place
    // TODO Probably something which could be made more efficient
    var new_data = [];

    // Title for the layer, recorded in each geometry
    // This then appears as the Big text in the sidebar
    // console.log('local_data_name');
    // console.log(local_data_name);

    //Basically an array of arrays holding the whole XLS
    // console.log('area_values');
    // console.log(area_values);

    //The column of the XLS to use to define geometry names
    // Column contains eg W01000001, "North Wales" or CF24 1aa
    // console.log('local_data_geography_column');
    // console.log(local_data_geography_column);

    // An object with the local_data_name mapped to the value - both from the XLS
    // console.log('ordered_data');
    // console.log(ordered_data);

    // Will appear in the sidebar, but doesn't affect the colour of the map
    // console.log('secondary_data_keys');
    // console.log(secondary_data_keys);

    var db_boundary_key = 'code';

    for (var geom in geometries) {
        if (geometries.hasOwnProperty(geom)) {

            var area_code = null;
            if (geometries[geom]['properties'].hasOwnProperty('postcode')) {
                area_code = geometries[geom]['properties']['postcode'];
            } else {
                area_code = geometries[geom]['properties'][db_boundary_key];
            }

            // assume that 'code' in the topojson is an appropriate key
            // if not, try name, and if it hits, use that.
            // if not, try altname, if it hits, use that as the area_name
            // very brute-force, trial and error
            if (!area_code || ordered_data[area_code] == null) {
                var boundary_name = geometries[geom]['properties']['name'];
                if ( boundary_name && ordered_data[boundary_name]) {
                    db_boundary_key = 'name';
                    area_code = geometries[geom]['properties'][db_boundary_key];
                } else {
                    var alt_boundary_name = geometries[geom]['properties']['altname'];

                    if ( alt_boundary_name && ordered_data[alt_boundary_name]) {
                        db_boundary_key = 'altname';
                        area_code = geometries[geom]['properties'][db_boundary_key];
                    }
                }
            }
            // Which key did we end up with, after the above brute force search?
            // console.log('db_boundary_key');
            // console.log(db_boundary_key);

            // Name of the area we're using to match a boundary with the ordered data
            // console.log('area_code');
            // console.log(area_code);

            if (area_code && ordered_data[area_code] != null) {

                geometries[geom]['properties']['REMOTE_VALUE'] = ordered_data[area_code];
                geometries[geom]['properties']['RENDER'] = true;
                geometries[geom]['properties']['DATA_TITLE'] = local_data_name;

                var string_data = [];
                // Grab all the secondary data and group it together
                for (var secondary_idx in secondary_data_keys) {
                    if (secondary_data_keys.hasOwnProperty(secondary_idx)) {

                        var key = secondary_data_keys[secondary_idx];
                        for (var area_value_key in area_values) {
                            if (area_values.hasOwnProperty(area_value_key)) {
                                var area_item = area_values[area_value_key];

                                var xls_areacode = area_item[local_data_geography_column];
                                var cleaned_xls_areacode = clean_xls_areacode(xls_areacode);

                                if (cleaned_xls_areacode == area_code) {
                                    string_data.push(
                                        {
                                            "grouping": [],
                                            "value": area_values[area_value_key][key],
                                            "title": key
                                        }
                                    );
                                }
                            }
                        }
                    }
                }

                delete ordered_data[area_code];

                geometries[geom]['properties']['STRING_DATA'] = string_data;
                new_data.push(geometries[geom]);
            }

        }
    }

    console.log('Error mapping: ');
    console.log(ordered_data);
    var unmapped_data_string = '';
    for(var unmapped in ordered_data) {
        if (ordered_data.hasOwnProperty(unmapped)) {
            unmapped_data_string += unmapped + ' : ' + ordered_data[unmapped] + '\n';
        }
    }

    alert('Failed to map the following data.\n' +
        'Please check each have a valid geography id and value.\n\n'
        + unmapped_data_string);

    // {#                        delete topojson_data['topojson']['objects'][geom_name];#}
    //Replace the previous geoms with this new array we've built up
    all_topojson_data['topojson']['objects'][geom_name]['geometries'] = new_data;
    all_topojson_data['layer_data']['name'] = local_data_name;

    // var layer_name = all_topojson_data['search_uuid'];
    // topojson_layers[layer_name] = all_topojson_data['topojson'];

    return all_topojson_data;
}

function clean_xls_areacode(unclean_areacode) {
    // console.log(unclean_areacode);
    var clean_areacode = unclean_areacode;
    if (isPostcodeish(unclean_areacode)) {
    //    Need to format this in a way we expect:
    //    AA111AA or AA1 1AA - not 'AA11 1AA'
        if(unclean_areacode.length > 7) {
            clean_areacode = unclean_areacode.slice(0, 4) + unclean_areacode.slice(5, unclean_areacode.length);
            // console.log('Cleaned ' + clean_areacode + ' from ' + unclean_areacode);
        }
        return clean_areacode;
    } else {
        return clean_areacode;
    }
}

$.ui.dialog.prototype.options.responsive = true;
$.ui.dialog.prototype.options.scaleH = 0.8;
$.ui.dialog.prototype.options.scaleW = 0.8;
$.ui.dialog.prototype.options.showTitleBar = true;
$.ui.dialog.prototype.options.showCloseButton = true;
var _open = $.ui.dialog.prototype.open;
$.ui.dialog.prototype.open = function () {
    var self = this;

    // apply original arguments
    _open.apply(this, arguments);

    // get dialog original size on open
    var oHeight = self.element.parent().outerHeight(),
        oWidth = self.element.parent().outerWidth(),
        isTouch = $("html").hasClass("touch");

    // responsive width & height
    var resize = function () {

        //check if responsive
        // dependent on modernizr for device detection / html.touch
        if (self.options.responsive === true || (self.options.responsive === "touch" && isTouch)) {
            var elem = self.element,
                wHeight = $(window).height(),
                wWidth = $(window).width(),
                dHeight = elem.parent().outerHeight(),
                dWidth = elem.parent().outerWidth(),
                setHeight = Math.min(wHeight * self.options.scaleH, oHeight),
                setWidth = Math.min(wWidth * self.options.scaleW, oWidth);

            if ((oHeight + 100) > wHeight || elem.hasClass("resizedH")) {
                elem.dialog("option", "height", setHeight).parent().css("max-height", setHeight);
                elem.addClass("resizedH");
            }
            if ((oWidth + 100) > wWidth || elem.hasClass("resizedW")) {
                elem.dialog("option", "width", setWidth).parent().css("max-width", setWidth);
                elem.addClass("resizedW");
            }

            // only recenter & add overflow if dialog has been resized
            if (elem.hasClass("resizedH") || elem.hasClass("resizedW")) {
                elem.dialog("option", "position", "center");
                elem.css("overflow", "auto");
            }
        }

        // add webkit scrolling to all dialogs for touch devices
        if (isTouch) {
            elem.css("-webkit-overflow-scrolling", "touch");
        }
    };

    // call resize()
    resize();

    // resize on window resize
    $(window).on("resize", function () {
        resize();
    });

    // resize on orientation change
    window.addEventListener("orientationchange", function () {
        resize();
    });

    // hide titlebarit means you have to rethink your architecture. If you don’t see why, spend a few weeks writing Javascript front-ends and get back to me
    if (!self.options.showTitleBar) {
        self.uiDialogTitlebar.css({
            "height": 0,
                "padding": 0,
                "background": "none",
                "border": 0
        });
        self.uiDialogTitlebar.find(".ui-dialog-title").css("display", "none");
    }

    //hide close button
    if (!self.options.showCloseButton) {
        self.uiDialogTitlebar.find(".ui-dialog-titlebar-close").css("display", "none");
    }

    // close on clickOut
    if (self.options.clickOut && !self.options.modal) {
        // use transparent div - simplest approach (rework)
        $('<div id="dialog-overlay"></div>').insertBefore(self.element.parent());
        $('#dialog-overlay').css({
            "position": "fixed",
                "top": 0,
                "right": 0,
                "bottom": 0,
                "left": 0,
                "background-color": "transparent"
        });
        $('#dialog-overlay').click(function (e) {
            e.preventDefault();
            e.stopPropagation();
            self.close();
        });
        // else close on modal click
    } else if (self.options.clickOut && self.options.modal) {
        $('.ui-widget-overlay').click(function (e) {
            self.close();
        });
    }

    // add dialogClass to overlay
    if (self.options.dialogClass) {
        $('.ui-widget-overlay').addClass(self.options.dialogClass);
    }
};
//end open

$.fn.dataTable.ext.errMode = 'throw';

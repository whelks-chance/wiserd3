/**
 * Created by ubuntu on 19/11/15.
 */

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

function get_remote_dataset_topojson(remote_data_topojson_url, topojson_geography, dataset_id, codelist_selected, callback) {
    $.ajax({
        url: remote_data_topojson_url,
        type: 'GET',
        data: {
            'geography': topojson_geography,
            'dataset_id': dataset_id,
            'codelist_selected': JSON.stringify(codelist_selected)
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


function thing(all_topojson_data, ordered_data, local_data_name, area_values, local_data_geography_column, secondary_data_keys) {

    var topojson_data = all_topojson_data['topojson'];
    var geom_name = Object.keys(topojson_data['objects'])[0];
    var geometries = topojson_data['objects'][geom_name]['geometries'];
    var new_data = [];

    console.log(area_values);
    console.log(geometries);

    console.log('inner 2nd keys');
    console.log(secondary_data_keys);

    for (var geom in geometries) {
        if (geometries.hasOwnProperty(geom)) {
            var area_code = geometries[geom]['properties']['code'];
            geometries[geom]['properties']['REMOTE_VALUE'] = ordered_data[area_code];
            geometries[geom]['properties']['DATA_TITLE'] = local_data_name;

            var string_data = [];
            // $('#local_data_secondary_check').find(":checkbox:checked").each(function (index) {


            for (var secondary_idx in secondary_data_keys) {
                if (secondary_data_keys.hasOwnProperty(secondary_idx)) {
                    // var key = $(this).attr('value');

                    var key = secondary_data_keys[secondary_idx];

                    for (var area_value_key in area_values) {
                        if (area_values.hasOwnProperty(area_value_key)) {
                            var area_item = area_values[area_value_key];

                            if (area_item[local_data_geography_column] == area_code) {
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
            
            geometries[geom]['properties']['STRING_DATA'] = string_data;
            new_data.push(geometries[geom]);

            // });
        }
    }

    // {#                        delete topojson_data['topojson']['objects'][geom_name];#}
    all_topojson_data['topojson']['objects'][geom_name]['geometries'] = new_data;
    all_topojson_data['layer_data']['name'] = local_data_name;

    // var layer_name = all_topojson_data['search_uuid'];
    // topojson_layers[layer_name] = all_topojson_data['topojson'];

    return all_topojson_data;
}

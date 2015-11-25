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


function get_local_dataset_topojson(remote_data_topojson_url, boundary_name, survey_id, data_name, callback) {
    $.ajax({
        url: remote_data_topojson_url,
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

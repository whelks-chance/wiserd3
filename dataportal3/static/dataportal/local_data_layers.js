/**
 * Created by ubuntu on 02/02/16.
 */




function do_local_layers(remote_data_layer_data, remote_data_topojson_url) {

    for (var remote_data_layer_idx in remote_data_layer_data) {
        (function () {
            var remote_data_layer = remote_data_layer_data[remote_data_layer_idx];
            console.log(remote_data_layer);

            get_remote_dataset_topojson(
                remote_data_topojson_url,
                remote_data_layer['geography_id'],
                remote_data_layer['dataset_id'],
                remote_data_layer['codelist'],
                function (topojson_data) {
                    console.log(remote_data_layer);

                    handleUploadedLayer(
                        topojson_data['topojson'],
                        remote_data_layer['colorpicker'],
                        remote_data_layer['bin_type'],
                        remote_data_layer['bin_num'],
                        '',
                        remote_data_layer['name'],
                        ''
                    );
                }
            );
        }());
    }
}
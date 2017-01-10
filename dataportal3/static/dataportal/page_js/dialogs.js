/**
 * Created by ianh on 31/12/16.
 */




function build_datatable(data, div_id, data_api_url) {

var calcDataTableHeight = function() {
    return $('#table_div').height() - (em*9);
};


    $(window).resize(function() {
        var oSettings = survey_table.fnSettings();
        oSettings.oScroll.sY = calcDataTableHeight();
        survey_table.fnDraw();
    });

    var table_div = $(div_id);
    table_div.toggle(true);

    var table_body = table_div.find('tbody');
    if ( ! $.fn.DataTable.isDataTable( div_id ) ) {

        var selected = [];
        var search_remote_form = $('#search-remote-form').height();
        var input_container = $('#search-remote-form-input-container').height();

        var survey_table = table_div.DataTable({

            "sScrollY": calcDataTableHeight(),

            deferRender:    true,
            // scrollY:        (search_remote_form - input_container) * 0.7,
            // scrollY: '100hv',
            scrollCollapse: true,
            // ordering: false,
            // searching: false,
            // processing: true,
            // "pageLength": 30,
            scroller:       {
                loadingIndicator: true
            },
            serverSide: false,
            "bAutoWidth": false,
            responsive: true,
            "oLanguage": datatables_language,
            data: data['datasets'],
            "rowCallback": function( row, data ) {
                if ( $.inArray(data.DT_RowId, selected) !== -1 ) {
                    $(row).addClass('selected');
                }
            },
            columns: [
                {'data': 'name', width: '50%', "targets": 0},
                {
                    'data': 'source',
                    "hidden": true
                },
                {
                    "rowIndex": -2,
                    "data": 'id',
                    "render": function ( data, type, full, meta ) {
                        return "<a target='_blank' " +
                            "href='/survey/" + data + "' class='btn btn-success view_metadata'>Metadata</a>"
                    },
                    "hidden": true
                },
                {
                    "rowIndex": -1,
                    "data": 'id',
                    "render": function ( data, type, full, meta ) {
                        return "<div class='btn btn-success view_survey'>View</div>"
                    },
                    "hidden": true
                }
            ]
        });
        survey_table.scroller.measure();


        table_body.on('click', '.view_survey', function () {
            var dataa = survey_table.row($(this).parents('tr')).data();
            console.log(dataa);

            ready_and_load_remote_var_form(data_api_url, dataa['id'], dataa['source'], dataa['name']);
        });


        $('#remote_results_table tbody').on('click', 'tr', function () {
            var id = this.id;
            var index = $.inArray(id, selected);

            // $('#remote_results_table tbody tr').each(function( index ) {
            // $( this ).removeClass('selected');
            // });
            if ( index === -1 ) {
                selected = [];
                selected.push( id );
                $('#add_to_map_dialog_btn').button('enable');
            } else {
                selected.splice( index, 1 );
            }

            // $(this).toggleClass('selected');
        });
    }
}



function setup_search_remote_form(parent_div, api_url) {

    $("#search-remote-form").dialog({

        autoOpen: false,
        dialogClass:"dialogClass",

        height: parent_div.height() * 0.9,
        position: {
            my: "center",
            at: "center",
            of: parent_div
        },
        width: parent_div.width() * 0.9,
        modal: true,
        buttons: [
            {
                id: 'add_to_map_dialog_btn',
                text: 'Add to Map',
                disabled: true,
                click: function () {

                    $(this).dialog("close");
                    var dataset_radio = $("#dataset_radio");
                    var dataset_id = dataset_radio.find(":radio:checked").attr('id');
                    var dataset_name = dataset_radio.find(":radio:checked").text();
                    var source = dataset_radio.find(":radio:checked").attr('source');

                    // ready_and_load_remote_var_form("{% url 'data_api' %}", dataset_id, source, dataset_name);
                    alert("{% url 'data_api' %}", dataset_id, source, dataset_name);
                }
            },
            {
                //TODO fix trans
                text: 'Cancel',
                click: function () {
                    $(this).dialog("close");
                }
            }
        ],
        close: function () {
        }
    });


    $('#remote_search_term').keyup(function(event){
        if(event.keyCode == 13){
            $("#remote_search_btn").click();
        }
    });


    $("#remote_search_btn").click(function(e){
        var search_term = $('#remote_search_term').val();
        //TODO trans
        add_ajax_waiting('Searching NomisWeb/ StatsWales...');

        $.ajax({
            url: api_url,
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

                build_datatable(data, '#remote_results_table', api_url);


                var dataset_radio = $('#dataset_radio');
                dataset_radio.find('input').remove().end();
                dataset_radio.find('label').remove().end();

                if (data['success'] == false) {
                    //TODO trans
                    alert('Sorry, an error occurred. Please try again, or report it.\n\n' + data['message'])
                } else {

                    // for (var rd_radio in data['datasets']) {
                    //     var remote_dataset_radio = data['datasets'][rd_radio];
                    //     var radio_div = $('<div>');
                    //
                    //     radio_div.append($('<input>', {
                    //         value: remote_dataset_radio.id,
                    //         id: remote_dataset_radio.id,
                    //         type: 'radio',
                    //         name: 'nomis_search_radio',
                    //         text: remote_dataset_radio.name
                    //     }).attr({'source': remote_dataset_radio.source}));
                    //     radio_div.append($('<label>', {
                    //         value: remote_dataset_radio.id,
                    //         for: remote_dataset_radio.id,
                    //         text: remote_dataset_radio.name
                    //     }).attr({'source': remote_dataset_radio.source})
                    //         .addClass(remote_dataset_radio.source));
                    //     dataset_radio.append(radio_div);
                    // }
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
                //TODO trans
                alert('Sorry, an error occurred. Please try again, or report it.\n\n');
            },
            complete: function() {
                ajax_finished();
            }
        });
    });


}


function ready_and_load_remote_var_form(url, dataset_id, source, dataset_name) {
    add_ajax_waiting(i18n_translation['map.inspecting_dataset']);

    $.ajax({
        // url: "{% url 'data_api' %}",
        url : url,
        type: 'GET',
        data: {
            'method': 'remote_metadata',
            'dataset_id': dataset_id,
            'source': source
        },
        success: function (data) {
            try {
                $('#dataset_title').remove().end().append('<h3>' + dataset_name + '</h2>');

                var dataset_radio = $('#data_cell_radio');
                dataset_radio.find('div').remove().end();

                for (var remote_codelist in data['metadata']['codelists']) {
                    var remote_codelist_data = data['metadata']['codelists'][remote_codelist];

                    var codelist_label = $('<div>', {text: remote_codelist_data['name']});
                    dataset_radio.append(codelist_label);

                    var codelist_radio_div = $('<div>', {id: remote_codelist + '_radio'});

                    for (var remote_codelist_option in remote_codelist_data['measures']) {
                        var remote_codelist_option_data = remote_codelist_data['measures'][remote_codelist_option];

                        var radio_div = $('<div>');

                        radio_div.append($('<input>', {
                            value: remote_codelist_option_data.id,
                            id: remote_codelist + '_' + remote_codelist_option_data.id,
                            type: 'radio',
                            name: (remote_codelist + '_option'),
                            text: remote_codelist_option_data.name
                        }));
                        radio_div.append($('<label>', {
                            class: 'dialog_radio_option',
                            value: remote_codelist_option_data.id,
                            for: remote_codelist + '_' + remote_codelist_option_data.id,
                            text: remote_codelist_option_data.name
                        }));
                        codelist_radio_div.append(radio_div);
                    }
                    codelist_radio_div.buttonset();

                    dataset_radio.append(codelist_radio_div);
                }

                var geography_options = $('#topojson_geography_radio');
                geography_options.find('div').remove().end();

                if (data['metadata'].hasOwnProperty('geographies')) {

                    for (var remote_geography_option in data['metadata']['geographies']) {
                        var remote_geography_option_data = data['metadata']['geographies'][remote_geography_option];

                        var radio_div = $('<div>');

                        radio_div.append($('<input>', {
                            value: remote_geography_option_data.id,
                            id: 'geog_' + remote_geography_option_data.id,
                            type: 'radio',
                            name: 'geog_option',
                            text: remote_geography_option_data.name
                        }));
                        radio_div.append($('<label>', {
                            class: 'dialog_radio_option',
                            value: remote_geography_option_data.id,
                            for: 'geog_' + remote_geography_option_data.id,
                            text: remote_geography_option_data.name
                        }));
                        geography_options.append(radio_div);
                    }
                } else {
                    var radio_div = $('<div>');

                    for (var geography_idx in DataPortal.TopoJsonGeographies) {
                        var geography = DataPortal.TopoJsonGeographies[geography_idx];
                        radio_div.append($('<input>', {
                            type: "radio",
                            name: "geographies",
                            id: 'geog_' + geography['geog_short_code'],
                            value: geography['geog_short_code']
                        }));

                        radio_div.append($('<label>', {
                            class: 'dialog_radio_option',
                            value: geography['geog_short_code'],
                            for: 'geog_' + geography['geog_short_code'],
                            text: geography['name']
                        }));
                    }
                    geography_options.append(radio_div);

                }

                geography_options.buttonset();

                $('#dataset_define_vars_form').data({
                    'dataset_id': dataset_id,
                    'source': source,
                    'dataset_name': dataset_name,
                    'codelists': data['metadata']['codelists']
                }).dialog('open');
            } catch (e) {
                ajax_finished();
            }
        },
        error: function () {
            alert(i18n_translation['map.ready_and_load_remote_var_form.err']);
        },
        complete: function () {
            ajax_finished();
        }
    });


}

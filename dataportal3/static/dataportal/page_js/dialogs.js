/**
 * Created by ianh on 31/12/16.
 */



function build_datatable(data, div_id) {
    var table_div = $(div_id);
    table_div.toggle(true);

    var table_body = table_div.find('tbody');

    // for (var item in data['datasets']) {
    //     var tr = $('<tr>');
    //     tr.append($('<td>'), {text: item.name});
    //     tr.append($('<td>'), {text: item.id});
    //     tr.append($('<td>'), {text: item.source});
    // }
    //
    // table_body.append(tr);



    if ( ! $.fn.DataTable.isDataTable( div_id ) ) {

        var selected = [];

        var search_remote_form = $('#search-remote-form').height();
        var input_container = $('#search-remote-form-input-container').height();

        var survey_table = table_div.DataTable({

            deferRender:    true,
            scrollY:        (search_remote_form - input_container) * 0.7,
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
            "columnDefs": [
                { "width": "50%", "targets": 0 }
            ],
            columns: [
                {'data': 'name', width: '50%', "targets": 0},
                {'data': 'source'},
                // {'data': 'id'}
                {
                    "targets": -1,
                    "data": 'id',
                    "render": function ( data, type, full, meta ) {
                        return "<a target='_blank' " +
                            "href='/survey/" + data + "' class='btn btn-success view_survey'>View</a>"
                    }
                }
            ]
        });

        $('#remote_results_table tbody').on('click', 'tr', function () {
            var id = this.id;
            var index = $.inArray(id, selected);

            $('#remote_results_table tbody tr').each(function( index ) {
                $( this ).removeClass('selected');
            });
            // $('#add_to_map_dialog_btn').button('disable');

            if ( index === -1 ) {
                selected = [];
                selected.push( id );
                $('#add_to_map_dialog_btn').button('enable');
            } else {
                selected.splice( index, 1 );
            }

            $(this).toggleClass('selected');
        } );


    }


}



function setup_search_remote_form(parent_div, remote_api_url) {

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
            url: remote_api_url,
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

                build_datatable(data, '#remote_results_table');


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
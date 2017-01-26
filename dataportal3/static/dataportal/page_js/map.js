/**
 * Created by ianh on 17/08/16.
 */


L.TopoJSON = L.GeoJSON.extend({
    addData: function(jsonData) {
        if (jsonData.type === "Topology") {
            for (key in jsonData.objects) {
                geojson = topojson.feature(jsonData, jsonData.objects[key]);
                L.GeoJSON.prototype.addData.call(this, geojson);
            }
        }
        else {
            L.GeoJSON.prototype.addData.call(this, jsonData);
        }
    }
});
// Copyright (c) 2013 Ryan Clark


function do_intro() {
    //Unlike other pages which dive into the tutorial bootstro, we show a dialog first here.
    $( "#welcome_form" ).dialog('open');

}


function do_choro_tutorial() {
    bootstro.start('', {
        onStep: function(obj) {
            // alert('1 --- ' + obj.idx + ' --- ' + obj.direction);
        },
        items: [
            {
                selector: '#bintype',
                title: i18n_translation['map.bintype.title'],
                content: i18n_translation['map.bintype.content'],
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#binno',
                title: i18n_translation['map.binno.title'],
                content: i18n_translation['map.binno.content'],
                placement: 'bottom',
                step: 1
            },
            {
                selector: '#colorpicker',
                title: i18n_translation['map.colorpicker.title'],
                content: i18n_translation['map.colorpicker.content'],
                placement: 'bottom',
                step: 2
            },
            {
                selector: '#layer_name_text_entry',
                title: i18n_translation['map.layer_name_text_entry.title'],
                content: i18n_translation['map.layer_name_text_entry.content'],
                placement: 'bottom',
                step: 3
            }

        ]
    });
}

function do_remote_data_tutorial() {
    bootstro.start('', {
        onStep: function(obj) {
            // alert('1 --- ' + obj.idx + ' --- ' + obj.direction);
        },
        items: [
            {
                selector: '#remote_search_term',
                title: i18n_translation['map.remote_search_term.title'],
                content: i18n_translation['map.remote_search_term.content'],
                placement: 'bottom',
                step: 0
            }

        ]
    });
}


function do_local_dataset_define_vars_tutorial() {

    bootstro.start('', {
        onStep: function(obj) {
            // alert('1 --- ' + obj.idx + ' --- ' + obj.direction);
        },
        items: [
            {
                selector: '#local_dataset_define_vars_form',
                title: i18n_translation['map.local_dataset_define_vars_form.title'],
                content: i18n_translation['map.local_dataset_define_vars_form.content'],
                placement: 'right',
                step: 0
            }

        ]
    });
}

function do_dataset_define_vars_tutorial() {

    bootstro.start('', {
        onStep: function(obj) {
            // alert('1 --- ' + obj.idx + ' --- ' + obj.direction);
        },
        items: [
            {
                selector: '#data_cell_radio > div:nth-child(2)',
                title: i18n_translation['map.dataset_define_vars_form.title'],
                content: i18n_translation['map.dataset_define_vars_form.content'],
                placement: 'bottom',
                step: 0
            }
            //  {
            //     selector: '#',
            //     title: 'Variables',
            //     content: 'Make sure to select a variable from each section.',
            //     placement: 'bottom',
            //     step: 1
            // }
        ]
    });
}

$(document).ready(function () {
    $('#search_remote_help').click(do_remote_data_tutorial);
    $('#choro_help').click(do_choro_tutorial);
    $('#dataset_define_vars_help').click(function(){
        do_dataset_define_vars_tutorial();
    });

    $('#local_dataset_define_vars_help').click(function(){
        do_local_dataset_define_vars_tutorial();
    });

    // $('#chloro_test').click(function (){
    //     $( "#chloropleth_option_form").data(
    //         {}
    //     ).dialog( "open" );
    // });

    $(document).on('click', '.action-placement', function(e) {
        $('.action-placement').removeClass('active');
        $(this).addClass('active');
        $('.icp-opts').data('iconpicker').updatePlacement($(this).text());
        e.preventDefault();
        return false;
    });

    $('.icp-auto').iconpicker({
            templates: {
                popover: '<div class="iconpicker-popover popover" style="width: 100%"><div class="arrow"></div>' +
                '<div class="popover-title"></div><div class="popover-content"></div></div>',
                footer: '<div class="popover-footer"></div>',
                buttons: '<button class="iconpicker-btn iconpicker-btn-cancel btn btn-default btn-sm">Cancel</button>' +
                ' <button class="iconpicker-btn iconpicker-btn-accept btn btn-primary btn-sm">Accept</button>',
                search: '<input type="search" class="form-control iconpicker-search" placeholder="Type to filter" />',
                iconpicker: '<div class="iconpicker"><div class="iconpicker-items"></div></div>',
                iconpickerItem: '<a role="button" href="#" class="iconpicker-item"><i></i></a>'
            }
        }
    );

    $('.icp-dd').iconpicker({
        placement: 'top'
    });

    $('.icp').on('iconpickerSelected', function(e) {
        // alert(e.iconpickerValue);
        console.log(e.iconpickerValue);
        var picker_target = $('.lead .picker-target');
        picker_target.get(0).className = 'picker-target fa-3x ' +
            e.iconpickerInstance.options.iconBaseClass + ' ' +
            e.iconpickerInstance.options.fullClassFormatter(e.iconpickerValue);
        picker_target.attr('data-icon_fa', e.iconpickerValue);
    });


});

function do_mapmydata_tutorial_1() {
    bootstro.start('', {
        onStep: function(obj) {
            // alert('1 --- ' + obj.idx + ' --- ' + obj.direction);
        },
        items: [
            {
                selector: '#drop',
                title: i18n_translation['map.mapmydata.drop.title'],
                content: i18n_translation['map.mapmydata.drop.content'],
                placement: 'bottom',
                step: 0
            }
            ,{
                selector: '#xlf',
                title: i18n_translation['map.mapmydata.xlf.title'],
                content: i18n_translation['map.mapmydata.xlf.content'],
                placement: 'bottom',
                step: 1
            }
        ]
    });

}

function do_mapmydata_tutorial_2() {
    bootstro.start('', {
        onStep: function(obj) {
        },
        items: [
            {
                selector: '#geography_label',
                title: i18n_translation['map.mapmydata_2.geography_label.title'],
                content: i18n_translation['map.mapmydata_2.geography_label.content'],
                placement: 'bottom',
                step: 0
            }
            ,{
                selector: '#data_column_label',
                title: i18n_translation['map.mapmydata_2.data_column_label.title'],
                content: i18n_translation['map.mapmydata_2.data_column_label.content'],
                placement: 'bottom',
                step: 1
            }
            ,{
                selector: '#secondary_data_label',
                title: i18n_translation['map.mapmydata_2.secondary_data_label.title'],
                content: i18n_translation['map.mapmydata_2.secondary_data_label.content'],
                placement: 'bottom',
                step: 2
            }

        ]
    });

}

function do_tutorial() {
    bootstro.start('', {
        onStep: function(obj) {
            // {#  alert(' --- ' + obj.idx + ' --- ' + obj.direction);#}

            if (obj.idx == 3) {
                if(!$('#map_layers_menu_li').hasClass('active')) {
                    $('#map_layers_menu_link').click();
                }
            }
        },
        items: [
            {
                selector: '#lang_toggle_split',
                title: i18n_translation['map.lang_toggle_split.title'],
                content: i18n_translation['map.lang_toggle_split.content'],
                placement: 'bottom',
                step: 0
            }
            ,{
                selector: '#map_div_col',
                title: i18n_translation['map.map_div_col.title'],
                content: i18n_translation['map.map_div_col.content'],
                placement: 'right',
                step: 1
            }
            ,{
                selector: '#map_div',
                title: i18n_translation['map.map_div.title'],
                content: i18n_translation['map.map_div.content'],
                placement: 'right',
                step: 2
            }
            ,{
                selector: '#side-menu',
                title: i18n_translation['map.side-menu.title'],
                content: i18n_translation['map.side-menu.content'],
                placement: 'right',
                step: 3
            }
            ,{
                selector: '#right_sidebar_col',
                title: i18n_translation['map.right_sidebar_col.title'],
                content: i18n_translation['map.right_sidebar_col.content'],
                placement: 'left',
                step: 4
            }

        ]
    });
}

// $(document).ready(function () {
//
//     var X = XLSX;
//     var XW = {
//         /* worker message */
//         msg: 'xlsx',
//         /* worker scripts */
//         rABS: './xlsxworker2.js',
//         norABS: './xlsxworker1.js',
//         noxfer: './xlsxworker.js'
//     };
//
//     var rABS = typeof FileReader !== "undefined" && typeof FileReader.prototype !== "undefined" && typeof FileReader.prototype.readAsBinaryString !== "undefined";
//     if (!rABS) {
//         document.getElementsByName("userabs")[0].disabled = true;
//         document.getElementsByName("userabs")[0].checked = false;
//     }
//
//     var use_worker = typeof Worker !== 'undefined';
//     if (!use_worker) {
//         document.getElementsByName("useworker")[0].disabled = true;
//         document.getElementsByName("useworker")[0].checked = false;
//     }
//
//     var transferable = use_worker;
//     if (!transferable) {
//         document.getElementsByName("xferable")[0].disabled = true;
//         document.getElementsByName("xferable")[0].checked = false;
//     }
//
//     var wtf_mode = false;
//
//     function fixdata(data) {
//         var o = "", l = 0, w = 10240;
//         for (; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
//         o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
//         return o;
//     }
//
//     function ab2str(data) {
//         var o = "", l = 0, w = 10240;
//         for (; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint16Array(data.slice(l * w, l * w + w)));
//         o += String.fromCharCode.apply(null, new Uint16Array(data.slice(l * w)));
//         return o;
//     }
//
//     function s2ab(s) {
//         var b = new ArrayBuffer(s.length * 2), v = new Uint16Array(b);
//         for (var i = 0; i != s.length; ++i) v[i] = s.charCodeAt(i);
//         return [v, b];
//     }
//
//     function xw_noxfer(data, cb) {
//         var worker = new Worker(XW.noxfer);
//         worker.onmessage = function (e) {
//             switch (e.data.t) {
//                 case 'ready':
//                     break;
//                 case 'e':
//                     console.error(e.data.d);
//                     break;
//                 case XW.msg:
//                     cb(JSON.parse(e.data.d));
//                     break;
//             }
//         };
//         var arr = rABS ? data : btoa(fixdata(data));
//         worker.postMessage({d: arr, b: rABS});
//     }
//
//     function xw_xfer(data, cb) {
//         var worker = new Worker(rABS ? XW.rABS : XW.norABS);
//         worker.onmessage = function (e) {
//             switch (e.data.t) {
//                 case 'ready':
//                     break;
//                 case 'e':
//                     console.error(e.data.d);
//                     break;
//                 default:
//                     xx = ab2str(e.data).replace(/\n/g, "\\n").replace(/\r/g, "\\r");
//                     console.log("done");
//                     cb(JSON.parse(xx));
//                     break;
//             }
//         };
//         if (rABS) {
//             var val = s2ab(data);
//             worker.postMessage(val[1], [val[1]]);
//         } else {
//             worker.postMessage(data, [data]);
//         }
//     }
//
//     function xw(data, cb) {
//         transferable = document.getElementsByName("xferable")[0].checked;
//         if (transferable) xw_xfer(data, cb);
//         else xw_noxfer(data, cb);
//     }
//
//     function to_json(workbook) {
//         var result = {};
//         workbook.SheetNames.forEach(function (sheetName) {
//             var roa = X.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
//             if (roa.length > 0) {
//                 result[sheetName] = roa;
//             }
//         });
//         return result;
//     }
//
//     function to_csv(workbook) {
//         var result = [];
//         workbook.SheetNames.forEach(function (sheetName) {
//             var csv = X.utils.sheet_to_csv(workbook.Sheets[sheetName]);
//             if (csv.length > 0) {
//                 result.push("SHEET: " + sheetName);
//                 result.push("");
//                 result.push(csv);
//             }
//         });
//         return result.join("\n");
//     }
//
//
//     function process_wb(wb) {
//         var output_json = to_json(wb);
//         var output = JSON.stringify(output_json, 2, 2);
//         do_layer_single_local(output_json);
//
//         if (typeof console !== 'undefined') console.log("output", new Date());
//     }
//
//     var drop = document.getElementById('drop');
//
//     function handleDrop(e) {
//         e.stopPropagation();
//         e.preventDefault();
//         rABS = document.getElementsByName("userabs")[0].checked;
//         use_worker = document.getElementsByName("useworker")[0].checked;
//         var files = e.dataTransfer.files;
//         var f = files[0];
//         {
//             var reader = new FileReader();
//             var name = f.name;
//             reader.onload = function (e) {
//                 if (typeof console !== 'undefined') console.log("onload", new Date(), rABS, use_worker);
//                 var data = e.target.result;
//                 if (use_worker) {
//                     xw(data, process_wb);
//                 } else {
//                     var wb;
//                     if (rABS) {
//                         wb = X.read(data, {type: 'binary'});
//                     } else {
//                         var arr = fixdata(data);
//                         wb = X.read(btoa(arr), {type: 'base64'});
//                     }
//                     process_wb(wb);
//                 }
//             };
//             if (rABS) reader.readAsBinaryString(f);
//             else reader.readAsArrayBuffer(f);
//         }
//     }
//
//     function handleDragover(e) {
//         e.stopPropagation();
//         e.preventDefault();
//         e.dataTransfer.dropEffect = 'copy';
//     }
//
//     if (drop.addEventListener) {
//         drop.addEventListener('dragenter', handleDragover, false);
//         drop.addEventListener('dragover', handleDragover, false);
//         drop.addEventListener('drop', handleDrop, false);
//     }
//
//
//     var xlf = document.getElementById('xlf');
//
//     function handleFile(e) {
//         rABS = document.getElementsByName("userabs")[0].checked;
//         use_worker = document.getElementsByName("useworker")[0].checked;
//         var files = e.target.files;
//         var f = files[0];
//         {
//             var reader = new FileReader();
//             var name = f.name;
//             reader.onload = function (e) {
//                 if (typeof console !== 'undefined') console.log("onload", new Date(), rABS, use_worker);
//                 var data = e.target.result;
//                 if (use_worker) {
//                     xw(data, process_wb);
//                 } else {
//                     var wb;
//                     if (rABS) {
//                         wb = X.read(data, {type: 'binary'});
//                     } else {
//                         var arr = fixdata(data);
//                         wb = X.read(btoa(arr), {type: 'base64'});
//                     }
//                     process_wb(wb);
//                 }
//             };
//             if (rABS) reader.readAsBinaryString(f);
//             else reader.readAsArrayBuffer(f);
//         }
//     }
//
//     if (xlf.addEventListener) xlf.addEventListener('change', handleFile, false);
//
// });



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

            console.log('ready_and_load_remote_var_form');
            console.log(data);

            try {
                // $('#dataset_title').remove().end().append('<h3>' + dataset_name + '</h2>');
                $('#dataset_title').html('<h4 class="dataset_title">' + dataset_name + '</h4>');

                var dataset_radio = $('#data_cell_radio');
                dataset_radio.find('div').remove().end();

                for (var remote_codelist in data['metadata']['codelists']) {
                    var remote_codelist_data = data['metadata']['codelists'][remote_codelist];

                    var codelist_label = $('<div>', {id: remote_codelist_data['name'] + '_label', text: remote_codelist_data['name']});
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
                console.log(e);

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

function build_datatable(data, div_id, data_api_url) {

    var calcDataTableHeight = function() {
        return $('#table_div').height() - (em*8);
    };

    $(window).resize(function() {
        var oSettings = survey_table.settings;
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
            deferRender:    true,
            // scrollY:        (search_remote_form - input_container) * 0.7,
            "sScrollY": calcDataTableHeight(),

            scrollCollapse: false,
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
                    'data': 'source'
                },
                {
                    "rowIndex": -2,
                    "data": 'id',
                    "render": function ( data, type, full, meta ) {
                        return "<a target='_blank' " +
                            "href='/survey/" + data + "' class='btn btn-success view_metadata'>" + i18n_translation['map.metadata'] + "</a>";
                    }
                },
                {
                    "rowIndex": -1,
                    "data": 'id',
                    "render": function ( data, type, full, meta ) {
                        return "<div class='btn btn-success view_survey'>" + i18n_translation['map.view'] + "</div>";
                    }
                },
                {
                    "data": 'text1',
                    "defaultContent": "<i>Not found</i>",
                    "hidden": true,
                    "className": 'none'
                    // "visible": false
                },
                {
                    "data": 'text2',
                    "defaultContent": "<i>Not found</i>",
                    "hidden": true,
                    // "visible": false,
                    "className": 'none'
                }
            ]
        });

    }
    else
    {
        table_div.DataTable().clear().rows.add(data['datasets']).draw();
    }


    table_body.on('click', '.view_survey', function () {
        var dataa = survey_table.row($(this).parents('tr')).data();

        // console.log(dataa);

        $('#search-remote-form').dialog( "close" );

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

var calcDataTableHeight = function() {
    return $('#table_div').height() - (em*8);
};





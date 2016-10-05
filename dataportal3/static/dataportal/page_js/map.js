/**
 * Created by ianh on 17/08/16.
 */


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
            },
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
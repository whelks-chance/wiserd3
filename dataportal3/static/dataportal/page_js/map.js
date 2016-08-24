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
                title: 'Select bin type',
                content: 'etc',
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#binno',
                title: 'Select number of bins',
                content: 'etc',
                placement: 'bottom',
                step: 1
            },
            {
                selector: '#colorpicker',
                title: 'Select Colour scheme',
                content: 'etc',
                placement: 'bottom',
                step: 2
            },
            {
                selector: '#layer_name_text_entry',
                title: 'Name it',
                content: 'etc',
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
                title: 'Search term goes here',
                content: 'The thing to searc Nomis/ StatsWales for - keyword',
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
                title: 'tutorial',
                content: 'blargh',
                placement: 'right',
                step: 0
            }

        ]
    });
}

$(document).ready(function () {
    $('#search_remote_help').click(do_remote_data_tutorial);
    $('#choro_help').click(do_choro_tutorial);
    $('#dataset_define_vars_help').click(function(){
        alert('dataset_define_vars_help');
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
                title: 'Drop a file',
                content: 'This is where the Excel file goes. Drag-and-drop it here.',
                placement: 'bottom',
                step: 0
            }
            ,{
                selector: '#xlf',
                title: 'Select file from filesystem',
                content: 'Regular file selection dialog box',
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
                title: 'Geography column',
                content: 'Pick a column showing the geography',
                placement: 'bottom',
                step: 0
            }
            ,{
                selector: '#data_column_label',
                title: 'Data value',
                content: 'Pick a column showing the data to be mapped',
                placement: 'bottom',
                step: 1
            }
            ,{
                selector: '#secondary_data_label',
                title: 'Any other data to display',
                content: 'This will be displayed in the sidebar when clicking on the map later.',
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
                title: 'Change language',
                content: 'These buttons can be used to toggle the language the site displays in.' +
                '<br><br>' +
                'If you sign-up and login, this preference will be stored for future visits.',
                placement: 'bottom',
                step: 0
            }
            ,{
                selector: '#map_div_col',
                title: 'The Map',
                content: 'The Map is the primary focus here.<br><br>' +
                'Layers of data are displayed, and most can be selected to show further detail.',
                placement: 'right',
                step: 1
            }
            ,{
                selector: '#map_div',
                title: 'Legend',
                content: 'Once data layers have been added, the legend will be displayed here.<br><br>' +
                'Colours and the number of categories are selected when the layer is first added.',
                placement: 'right',
                step: 2
            }
            ,{
                selector: '#side-menu',
                title: 'Side menu',
                content: '<p>This is where new map layers are added.</p>' +
                '<h4>RemoteData</h4><p>Import data from Nomis and/or StatsWales</p>' +
                '<h4>MapMyData</h4><p>Upload an Excel file with geographies and values for mapping</p>' +
                '<h4>Welsh Government Data</h4><p>WMS layers made available by LLE, Welsh Government</p>',
                placement: 'right',
                step: 3
            }
            ,{
                selector: '#right_sidebar_col',
                title: 'Info Pane',
                content: 'When regions on the map are selected, ' +
                'the corresponding data for that area are shown here',
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
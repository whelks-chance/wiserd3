/**
 * Created by ianh on 17/08/16.
 */


function do_intro() {
    //Unlike other pages which dive into the tutorial bootstro, we show a dialog first here.
    $( "#welcome_form" ).dialog('open');

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

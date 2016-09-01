
function do_intro() {
    bootstro.start('', {
        onStep: function(obj) {
            // {#  alert(' --- ' + obj.idx + ' --- ' + obj.direction);#}
        if (obj.idx == 2) {
            if (!$('#Recent_Search_Results_li').hasClass('active')) {
                $('#Recent_Search_Results_btn').click();
            }
        }
        },
        items: [
            {
                selector: '#lang_toggle_split',
                title: 'Change language',
                content: 'These buttons can be used throughout the website to toggle the language the site displays in.' +
                '<br><br>' +
                'If you sign-up and login, this preference will be stored for future visits.',
                placement: 'bottom',
                step: 0
            },

            {
                selector: '#dashboard_grid',
                title: 'The Dashboard',
                content: 'These buttons take you to different sections of the DataPortal',
                placement: 'left',
                step: 1
            },

            {
                selector: '#nav_bar_side',
                title: 'Side Menu',
                content: 'Content',
                placement: 'right',
                step: 2

            }

        ]
    });
}


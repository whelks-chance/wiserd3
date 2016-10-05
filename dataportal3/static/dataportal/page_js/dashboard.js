
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
                title: i18n_translation['dashboard.lang_toggle_split.title'],
                content: i18n_translation['dashboard.lang_toggle_split.content'],
                placement: 'bottom',
                step: 0
            },

            {
                selector: '#dashboard_grid',
                title: i18n_translation['dashboard.dashboard_grid.title'],
                content: i18n_translation['dashboard.dashboard_grid.content'],
                placement: 'left',
                step: 1
            },

            {
                selector: '#nav_bar_side',
                title: i18n_translation['dashboard.nav_bar_side.title'],
                content: i18n_translation['dashboard.nav_bar_side.content'],
                placement: 'right',
                step: 2

            }

        ]
    });
}


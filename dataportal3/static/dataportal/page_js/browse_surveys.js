
function do_intro() {
    bootstro.start('', {
        prevButton: '',
        onStep: function(obj) {
            // alert(' --- ' + obj.idx + ' --- ' + obj.direction);

        },
        items: [
            {
                selector: '#survey_table',
                title: i18n_translation['browse_surveys.survey_table.title'],
                content: i18n_translation['browse_surveys.survey_table.content'],
                placement: 'top',
                step: 0
            },
            {
                selector: '#survey_table_filter',
                title: i18n_translation['browse_surveys.survey_table_filter.title'],
                content: i18n_translation['browse_surveys.survey_table_filter.content'],
                placement: 'left',
                step: 1
            },
            {
                selector: '#survey_table_length',
                title: i18n_translation['browse_surveys.survey_table_length.title'],
                content: i18n_translation['browse_surveys.survey_table_length.content'],
                placement: 'right',
                step: 2
            }
        ]
    });


}
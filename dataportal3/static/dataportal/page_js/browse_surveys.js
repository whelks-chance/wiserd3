
function do_intro() {
    bootstro.start('', {
        prevButton: '',
        onStep: function(obj) {
            // alert(' --- ' + obj.idx + ' --- ' + obj.direction);

        },
        items: [
            {
                selector: '#survey_table',
                title: 'Browse Surveys',
                content: 'This page allows you to browse all the surveys available.',
                placement: 'top',
                step: 0
            },
            {
                selector: '#survey_table_filter',
                title: 'Filter',
                content: 'You can filter the table of surveys using key words.',
                placement: 'left',
                step: 1
            },
            {
                selector: '#survey_table_length',
                title: 'View',
                content: 'This button allows you to choose the number of surveys you view per page.',
                placement: 'right',
                step: 2
            }
        ]
    });


}
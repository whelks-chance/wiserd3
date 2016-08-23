/**
 * Created by ianh on 17/08/16.
 */




function do_intro(lang) {
    
    $('#survey_dc_tab_li').click();

    bootstro.start('', {
        // prevButton: '',
        onStep: function(obj) {
            // alert(' --- ' + obj.idx + ' --- ' + obj.direction);

        },
        items: [
            {
                selector: '#question_row_jump',
                title: 'Jump to Questions',
                content: get_i18n_text('question_row_jump', lang),
                placement: 'bottom',
                step: 1
            },
            {
                selector: '#question_row',
                title: 'Question table',
                content: 'This shows the questions discovered during the search',
                placement: 'top',
                step: 2
            },
            {
                selector: '#survey_row_jump',
                title: 'Jump to Surveys',
                content: 'This shows the surveys discovered during the search',
                placement: 'bottom',
                step: 3
            },
            {
                selector: '#survey_row',
                title: 'Survey table',
                content: 'This shows the surveys discovered during the search',
                placement: 'top',
                step: 4
            },
            {
                selector: '#qual_row_jump',
                title: 'Jump to Qualitative records',
                content: 'This button shows the Qualitative records discovered during the search',
                placement: 'bottom',
                step: 5
            },
            {
                selector: '#qual_row',
                title: 'Qualitative Records',
                content: 'This shows the Qualitative records discovered during the search',
                placement: 'top',
                step: 6
            },
            {
                selector: '#search_box',
                title: 'Search box',
                content: 'Data can be searched here. This shows the current search, and can be modified or refined to search again',
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#survey_questions_table_filter',
                title: 'Filter',
                content: 'Filter searches to refine the results',
                placement: 'left',
                step: 7
            }
            

        ]
    });


}



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
                title: i18n_translation['search.question_row_jump.title'],
                content: i18n_translation['search.question_row_jump.content'],
                placement: 'bottom',
                step: 1
            },
            {
                selector: '#question_row',
                title: i18n_translation['search.question_row.title'],
                content: i18n_translation['search.question_row.content'],
                placement: 'top',
                step: 2
            },
            {
                selector: '#survey_row_jump',
                title: i18n_translation['search.survey_row_jump.title'],
                content: i18n_translation['search.survey_row_jump.content'],
                placement: 'bottom',
                step: 3
            },
            {
                selector: '#survey_row',
                title: i18n_translation['search.survey_row.title'],
                content: i18n_translation['search.survey_row.content'],
                placement: 'top',
                step: 4
            },
            {
                selector: '#qual_row_jump',
                title: i18n_translation['search.qual_row_jump.title'],
                content: i18n_translation['search.qual_row_jump.content'],
                placement: 'bottom',
                step: 5
            },
            {
                selector: '#qual_row',
                title: i18n_translation['search.qual_row.title'],
                content: i18n_translation['search.qual_row.content'],
                placement: 'top',
                step: 6
            },
            {
                selector: '#search_box',
                title: i18n_translation['search.search_box.title'],
                content: i18n_translation['search.search_box.content'],
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#survey_questions_table_filter',
                title: i18n_translation['search.survey_questions_table_filter.title'],
                content: i18n_translation['search.survey_questions_table_filter.content'],
                placement: 'left',
                step: 7
            }
            

        ]
    });


}



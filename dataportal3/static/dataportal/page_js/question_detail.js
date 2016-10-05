/**
 * Created by ianh on 18/08/16.
 */


function do_intro(lang) {

    $('#question_tab_li').click();

    bootstro.start('', {
        prevButton: '',
        onStep: function(obj) {
            // alert(' --- ' + obj.idx + ' --- ' + obj.direction);

            if (obj.idx == 0 || obj.idx == 1) {
                $('#question_tab_li').click();
            }
             if (obj.idx == 2 || obj.idx == 3) {
                $('#results_tab_li').click();
            }
            if (obj.idx == 4 || obj.idx == 5) {
                $('#response_table_li').click();
            }
        },
        items: [
            {
                selector: '#question_tab_li',
                title: i18n_translation['question_detail.question_tab_li.title'],
                content: i18n_translation['question_detail.question_tab_li.content'],
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#question_tab',
                title: i18n_translation['question_detail.question_tab.title'],
                content: i18n_translation['question_detail.question_tab.content'],
                placement: 'top',
                step: 1
            },
            {
                selector: '#results_tab_li',
                title: i18n_translation['question_detail.results_tab_li.title'],
                content: i18n_translation['question_detail.results_tab_li.content'],
                placement: 'bottom',
                step: 2
            },
            {
                selector: '#results_tab',
                title: i18n_translation['question_detail.results_tab.title'],
                content: i18n_translation['question_detail.results_tab.content'],
                placement: 'top',
                step: 3
            },
            {
                selector: '#response_table_li',
                title: i18n_translation['question_detail.response_table_li.title'],
                content: i18n_translation['question_detail.response_table_li.content'],
                placement: 'bottom',
                step: 4
            },
            {
                selector: '#response_table',
                title: i18n_translation['question_detail.response_table.title'],
                content: i18n_translation['question_detail.response_table.content'],
                placement: 'top',
                step: 5
            }


        ]
    });


}

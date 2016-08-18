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
            // if (obj.idx == 4 || obj.idx == 5) {
            //     $('#survey_questions_li').click();
            // }
        },
        items: [
            {
                selector: '#question_tab_li',
                title: 'Question Metadata',
                content: get_i18n_text('question_tab_li', lang),
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#question_tab',
                title: 'Question Metadata',
                content: get_i18n_text('question_tab', lang),
                placement: 'top',
                step: 1
            },
            {
                selector: '#results_tab_li',
                title: 'Jump to Surveys',
                content: 'This shows the surveys discovered during the search',
                placement: 'bottom',
                step: 2
            },
            {
                selector: '#results_tab',
                title: 'Survey table',
                content: 'This shows the surveys discovered during the search',
                placement: 'top',
                step: 3
            }
            // {
            //     selector: '#survey_questions_li',
            //     title: 'Jump to Qualitative records',
            //     content: 'This button shows the Qualitative records discovered during the search',
            //     placement: 'bottom',
            //     step: 4
            // },
            // {
            //     selector: '#survey_questions',
            //     title: 'Qualitative Records',
            //     content: 'This shows the Qualitative records discovered during the search',
            //     placement: 'top',
            //     step: 5
            // }


        ]
    });


}

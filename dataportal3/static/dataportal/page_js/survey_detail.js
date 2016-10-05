/**
 * Created by ianh on 16/08/16.
 */


function do_intro() {
    bootstro.start('', {
        prevButton: '',
        onStep: function(obj) {
            // alert(' --- ' + obj.idx + ' --- ' + obj.direction);


            if (obj.idx == 0 || obj.idx == 1) {
                $('#survey_dc_tab_li').click();
                // $('#survey_dc_tab').tab('show');

            }
             if (obj.idx == 3 || obj.idx == 4) {
                $('#survey_tab_li').click();
                // $('#survey_tab').tab('show');

            }
            if (obj.idx == 5 || obj.idx == 6) {
                $('#survey_questions_li').click();
                // $('#survey_questions').tab('show');

            }
        },
        items: [
            {
                selector: '#survey_dc_tab_li',
                title: i18n_translation['survey_detail.survey_dc_tab_li.title'],
                content: i18n_translation['survey_detail.survey_dc_tab_li.content'],
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#survey_dc_tab',
                title: i18n_translation['survey_detail.survey_dc_tab.title'],
                content: i18n_translation['survey_detail.survey_dc_tab.content'],
                placement: 'top',
                step: 1
            },
            {
                selector: '#text_input_source_url',
                title: i18n_translation['survey_detail.text_input_source_url.title'],
                content: i18n_translation['survey_detail.text_input_source_url.content'],
                placement: 'bottom',
                step: 2
            },
            {
                selector: '#survey_tab_li',
                title: i18n_translation['survey_detail.survey_tab_li.title'],
                content: i18n_translation['survey_detail.survey_tab_li.content'],
                placement: 'bottom',
                step: 3
            },
            {
                selector: '#survey_tab',
                title: i18n_translation['survey_detail.survey_tab.title'],
                content: i18n_translation['survey_detail.survey_tab.content'],
                placement: 'top',
                step: 4
            },
            {
                selector: '#survey_questions_li',
                title: i18n_translation['survey_detail.survey_questions_li.title'],
                content: i18n_translation['survey_detail.survey_questions_li.content'],
                placement: 'bottom',
                step: 5
            },
            {
                selector: '#survey_questions',
                title: i18n_translation['survey_detail.survey_questions.title'],
                content: i18n_translation['survey_detail.survey_questions.content'],
                placement: 'top',
                step: 6
            }

        ]
    });


}


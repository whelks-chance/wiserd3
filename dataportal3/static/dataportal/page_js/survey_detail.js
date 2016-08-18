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
                title: 'Dublin Core Tab',
                content: 'This button shows the Dublin Core data',
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#survey_dc_tab',
                title: 'Dublin Core Tab',
                content: 'The Dublin Core tab' +
                '<br><br>' +
                'This has standardised data focussing on the collection and repository of the Survey data',
                placement: 'top',
                step: 1
            },
            {
                selector: '#text_input_source_url',
                title: 'Download',
                content: 'Data url',
                placement: 'bottom',
                step: 2
            },
            {
                selector: '#survey_tab_li',
                title: 'Survey Tab',
                content: 'This button shows the WISERD Survey Metadata',
                placement: 'bottom',
                step: 3
            },
            {
                selector: '#survey_tab',
                title: 'Survey Tab',
                content: 'The survey tab' +
                '<br><br>' +
                'This has WISERD metadata specific to the interests of the Social Sciences',
                placement: 'top',
                step: 4
            },
            {
                selector: '#survey_questions_li',
                title: 'Survey Questions Tab',
                content: 'This button shows the surveys questions',
                placement: 'bottom',
                step: 5
            },
            {
                selector: '#survey_questions',
                title: 'Survey Questions Tab',
                content: 'The Survey Questions Tab' +
                '<br><br>' +
                'This has the questions from the survey',
                placement: 'top',
                step: 6
            }



        ]
    });


}


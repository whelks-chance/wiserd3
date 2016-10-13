/**
 * Created by kdickson on 22/09/16.
 */

function do_intro() {
    bootstro.start('', {
        prevButton: '',
        onStep: function (obj) {
            // alert(' --- ' + obj.idx + ' --- ' + obj.direction);
        },
        items: [
            {
                selector: '#contents',
                title: i18n_translation['user_help_guide.help_guide_title'],
                content: i18n_translation['user_help_guide.help_guide_contents'],
                placement: 'bottom',
                step: 0
            },
        ]
    }
    )};
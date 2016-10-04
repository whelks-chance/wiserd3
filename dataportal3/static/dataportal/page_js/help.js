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
                selector: '#help_title',
                title: i18n_translation['help_support.help_title.title'],
                content: i18n_translation['help_support.help_title.content'],
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#user_guide_link',
                title: i18n_translation['help_support.user_guide_link.title'],
                content: i18n_translation['help_support.user_guide_link.content'],
                placement: 'right',
                step: 1
            },
            {
                selector: '#support_people',
                title: i18n_translation['help_support.support_people.title'],
                content: i18n_translation['help_support.support_people.content'],
                placement: 'top',
                step: 2
            },
            {
                selector: '#useful_links',
                title: i18n_translation['help_support.useful_links.title'],
                content: i18n_translation['help_support.useful_links.content'],
                placement: 'top',
                step: 3
            }
        ]
    }
    )};
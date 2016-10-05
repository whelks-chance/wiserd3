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
                selector: '#events_logo',
                title: i18n_translation['events.events_logo.title'],
                content: i18n_translation['events.events_logo.content'],
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#download_box',
                title: i18n_translation['events.download_box.title'],
                content: i18n_translation['events.download_box.content'],
                placement: 'right',
                step: 1
            }
        ]
    }
    )}
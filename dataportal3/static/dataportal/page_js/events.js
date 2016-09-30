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
                title: 'Events and Presentations',
                content: 'Welcome to the events page, here you can find out about events that the DataPortal team will be attending as well as the accompanying presentations.',
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#download_box',
                title: 'Downloadable content',
                content: 'The presentation can be downloaded via this link.',
                placement: 'right',
                step: 1
            },
        ]
    }
    )};
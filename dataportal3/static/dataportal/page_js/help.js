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
                title: 'Help and Support',
                content: 'help',
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#user_guide_link',
                title: 'User Guide',
                content: 'help',
                placement: 'right',
                step: 1
            },
            {
                selector: '#support_people',
                title: 'The Experts',
                content: 'content',
                placement: 'bottom',
                step: 2
            },

        ]
    }
    )};
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
                content: 'This page provides help and support to you while using the DataPortal',
                placement: 'bottom',
                step: 0
            },
            {
                selector: '#user_guide_link',
                title: 'User Guide',
                content: 'If you need more assistance than these tip boxes here is the link to a detailed user help guide.',
                placement: 'right',
                step: 1
            },
            {
                selector: '#support_people',
                title: 'The Experts',
                content: 'If you have questions or need more support please contact the experts.',
                placement: 'top',
                step: 2
            },
            {
                selector: '#useful_links',
                title: 'Useful Links',
                content: 'Please find links related to the DataPortal here.',
                placement: 'top',
                step: 3
            },

        ]
    }
    )};
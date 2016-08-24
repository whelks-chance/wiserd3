
function do_intro() {
    bootstro.start('', {
        onStep: function(obj) {
            // {#  alert(' --- ' + obj.idx + ' --- ' + obj.direction);#}

        },
        items: [
            {
                selector: '#lang_toggle_split',
                title: 'Change language',
                content: 'These buttons can be used to toggle the language the site displays in.' +
                '<br><br>' +
                'If you sign-up and login, this preference will be stored for future visits.',
                placement: 'bottom',
                step: 0
            }

        ]
    });
}
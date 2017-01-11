/**
 * Created by ianh on 16/08/16.
 */


function do_intro() {
    bootstro.start('', {
        prevButton: '',
        onStep: function (obj) {
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

function wordCloud(selector) {
    var fill = d3.scale.category20();
    var svg = d3.select(selector).append("svg")
        .attr("width", 600)
        .attr("height", 500)
        .append("g")
        .attr("transform", "translate(250,250)");
    function draw(words) {
        var cloud = svg.selectAll("g text")
            .data(words, function(d) { return d.text; });
        //Entering words
        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i); })
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; });
        cloud
            .transition()
            .duration(600)
            .style("font-size", function(d) { return d.size + "px"; })
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("fill-opacity", 1);
        cloud.exit()
            .transition()
            .duration(200)
            .style('fill-opacity', 1e-6)
            .attr('font-size', 1)
            .remove();
    }
    return {
        update: function(words) {
            d3.layout.cloud().size([500, 500])
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", draw)
                .start();
        }
    }
}


function do_wordcloud(element_name, survey_api_url) {

    var json = (function()
    {
        $.ajax({
            'type': 'GET',
            'async': false,
            'global': false,
            'url': survey_api_url,
            'dataType': 'json',
            'success' : function (data) {
                json = data['results'][0]['keywords'];
            }
        });
        return [json];
    });

    var words = ["test data goes here from different file at some point"
    ];

    console.log(words);
    words = json();
    console.log(words);

    function getWords(i) {
        return words[i]
            .replace(/[!\.,:;\?]/g, '')
            .split(' ')
            .map(function(d) {
                return {text: d, size: 10 + Math.random() * 60};
            })
    }
    function showNewWords(vis, i) {
        i = i || 0;
        vis.update(getWords(i ++ % words.length));
        setTimeout(function() { showNewWords(vis, i + 1)}, 2000)
    }
    var myWordCloud = wordCloud(element_name);
    showNewWords(myWordCloud);

}


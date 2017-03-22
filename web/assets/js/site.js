$(function() {
    var query = get_params('query');
    var $search_input = $('#top-bar-search-input');
    var $search_submit = $('#top-bar-search-submit');

    if (query != '') {
        $search_input.val(query);
    }

    $search_submit.on('click', function() {
        query = $search_input.val();
        //if (query === '') { return false; }
        
        var url = '/search?query=' + query;
        window.open(url, '_self');
    });
});

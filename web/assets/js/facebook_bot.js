(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.com/en_US/messenger.Extensions.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'Messenger'));

window.extAsyncInit = function() {

    // check if should close webview window right away
    //var closing_webview = get_params('closing_webview');
    //if (closing_webview === 'true') {
    //    MessengerExtensions.requestCloseBrowser();
    //}

};

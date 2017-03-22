// general
function toggleMenu(id, class_) {
    var class_ = class_ || id;
    var x = document.getElementById(id);

    if (x.className === class_) {
        x.className += " responsive";
    } else {
        x.className = class_;
    }
}

$(function() {    
    var $secondary_links = $('#secondary-links');
    var $nav_secondary_left = $('#nav-secondary-left');
    var $nav_secondary_right = $('#nav-secondary-right');
    var secondary_nav_links = $secondary_links.find('.secondary-nav-link');

    var min_left = -300,
        max_left = 0,
        step = 100
        left = $secondary_links.position().left;

    var check_top_offset = function() {
        var last_index = secondary_nav_links.length - 1;
        return secondary_nav_links[0].offsetTop === secondary_nav_links[last_index].offsetTop;
    }

    $nav_secondary_right.on('click', function() {        
        if (!check_top_offset()) {
            $nav_secondary_right.removeClass('disabled');
            $nav_secondary_left.removeClass('disabled');

            left -= step;
            $secondary_links.css('left', left);
        } else {
            $nav_secondary_right.addClass('disabled');
        }
    });

    $nav_secondary_left.on('click', function() {
        if (left + step <= max_left) {
            $nav_secondary_right.removeClass('disabled');
            $nav_secondary_left.removeClass('disabled');

            left += step;
            $secondary_links.css('left', left);
            $nav_secondary_left.removeClass('disabled');
        } else {
            $nav_secondary_left.addClass('disabled');
        }
    });
});

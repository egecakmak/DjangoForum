var opsPopOver = {
    'html':true,    
    content: function(){
        return $('#login-form').html();
    },
};

$(function(){
    $('#popover-menu-guest').popover(opsPopOver)

});


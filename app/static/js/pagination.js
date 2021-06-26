function ajax_get_update()
    {
        $.get(url, function(results){
            //get the parts of the result you want to update. Just select the needed parts of the response
            var videoList = $("#videoList", results);
            var span = $("span.step-links", results);
            //update the ajax_table_result with the return value
            $('#ajax_videoList_result').html(videoList);
            $('.step-links').html(span);
        }, "html");
    }

//bind the corresponding links in your document to the ajax get function
$(document).ready(function() {
    $('.step-links #prev').click(function(e){
        e.preventDefault();
        url = ($('.step-links #prev')[0].href);
        ajax_get_update();
    });
    $('.step-links #next').click(function(e){
        e.preventDefault();
        url = ($('.step-links #next')[0].href);
        ajax_get_update();
    });
});
//since the links are reloaded we have to bind the links again
//to the actions
$(document).ajaxStop(function(){
    $('.step-links #prev').click(function(e){
        e.preventDefault();
        url = ($('.step-links #prev')[0].href);
        ajax_get_update();
    });
    $('.step-links #next').click(function(e){
        e.preventDefault();
        url = ($('.step-links #next')[0].href);
        ajax_get_update();
    });
});

function ajax_get_updatePost()
    {
        $.get(url, function(results){
            //get the parts of the result you want to update. Just select the needed parts of the response
            var postList = $("#postList", results);
            var span = $("span.step-links-post", results);
            //update the ajax_table_result with the return value
            $('#ajax_postList_result').html(postList);
            $('.step-links-post').html(span);
        }, "html");
    }

//bind the corresponding links in your document to the ajax get function
$(document).ready(function() {
    $('.step-links-post #prev').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #prev')[0].href);
        ajax_get_updatePost();
    });
    $('.step-links-post #next').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #next')[0].href);
        ajax_get_updatePost();
    });
    $('.step-links-post #first').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #first')[0].href);
        ajax_get_updatePost();
    });
    $('.step-links-post #last').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #last')[0].href);
        ajax_get_updatePost();
    });
});
//since the links are reloaded we have to bind the links again
//to the actions
$(document).ajaxStop(function(){
    $('.step-links-post #prev').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #prev')[0].href);
        ajax_get_updatePost();
    });
    $('.step-links-post #next').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #next')[0].href);
        ajax_get_updatePost();
    });
    $('.step-links-post #first').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #first')[0].href);
        ajax_get_updatePost();
    });
    $('.step-links-post #last').click(function(e){
        e.preventDefault();
        url = ($('.step-links-post #last')[0].href);
        ajax_get_updatePost();
    });
});
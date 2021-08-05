$(document).ready(function(){
    $('body').on('change', '.communitySelect', function(e){
        e.preventDefault();
        var id = $(this).attr('videoId');
        var target = $(this).parents().siblings('.groupBody');
        $.ajax({
            url: '/edit/video/'+id+'/community',
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.html){
                    target.html(res.html)
                }
            }
        })
    })
    $('body').on('change', '.groupSelect', function(e){
        e.preventDefault();
        var id = $(this).attr('videoId');
        $.ajax({
            url: '/edit/video/'+id+'/group',
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
        })
    })
    $('body').on('change', '.titleInput', function(e){
        e.preventDefault();
        var id = $(this).attr('videoId');
        $.ajax({
            url: '/edit/video/'+id+'/title',
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
        })
    })
    $('body').on('change', '.urlInput', function(e){
        e.preventDefault();
        var id = $(this).attr('videoId');
        var input = $(this);
        $.ajax({
            url: '/edit/video/'+id+'/url',
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.url){
                    input.val(res.url);
                }
            }
        })
    })
    $('body').on('click', '.deleteImage', function(e){
        e.preventDefault();
        var id = $(this).attr('videoId');
        var row = $(this).parentsUntil('tbody')
        $.ajax({
            url: '/edit/video/'+id+'/delete',
            type: 'post',
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.success){
                    row.hide();
                }
            }
        })
    })
})
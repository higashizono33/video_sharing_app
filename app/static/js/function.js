$(document).ready(function(){
    $(document).on('click','.show-comment', function(e){
        e.preventDefault();
        var id = $(this).attr('postId');
        $('.comment-card-'+id).toggle();
    })
    $('#form_post').on('submit', function(e){
        e.preventDefault();
        var id = $(this).attr('videoId');
        $.ajax({
            url: '/video/'+id,
            type: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.error){
                    $('.p_error').html('*'+res.error)
                } else {
                    $('#postList').html(res.html);
                    var first_page = 
                    '<span class="current">Page 1 of 4.</span> \n'+
                    '<a id="next" href="?post_page=2">next</a> \n'+
                    '<a id="last" href="?post_page=4">last »</a> \n'
                    
                    $('.step-links-post').html(first_page);
                    $('.modal-body input').attr('value', id);
                    $('#text_post').val('');
                    $('.p_error').text('');
                }
            }
        })
    })
    $(document).on('click', '.like_btn', function(e){
        e.preventDefault();
        $.ajax({
            url: $(this).attr('href'),
            type: 'get',
            dataType: 'json',
            success: function(res){
                $('#like_section').html(res.html);
            }
        })
    })
    $('body').on('click', '.lead', function(e){
        e.preventDefault();
        var form = $(this).siblings('form');
        var p = $(this);
        var videoId = $(this).attr('videoId');
        $(p).hide();
        $(form).show();
        $(form).on('focusout', function(){
            $.ajax({
                url: '/add_description/' + videoId,
                type: 'post',
                data: $(form).serialize(),
                dataType: 'json',
                success: function(res){
                    if(res.error){
                        $(form).find('.desc_error').html('*'+res.error)
                    } else {
                        $(form).hide();
                        $(p).html(res.description+'<span class="glyphicon ms-2">&#x270f;</span>');
                        $(p).show();
                    }
                }
            })
        })
    })
})
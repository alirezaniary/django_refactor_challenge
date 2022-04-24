$(document).ready(function () {
	$(window).scroll(function () {
		var s = $(window).scrollTop(),
			d = $(document).height() - $('.comment').height(),
			c = $(window).height(),
			scrollPercent = (s / (d-c)) * 100;
		var position = scrollPercent;
		$("#progressbar").attr('style', 'width: ' + position + '%; transition: none;');
	});


	function renderLike (status){
		if(status.id){
			if(status.is_like){
				$('.like, .dislike-fill').hide()
				$('.like-fill, .dislike').show()
			}
			else{
				$('.dislike, .like-fill').hide()
				$('.dislike-fill, .like').show()
			}
		}
		else{
			$('.like, .dislike').show()
			$('.like-fill, .dislike-fill').hide()
		}
	}


	function renderBookmark (status){
		if(status.id){
			$('.bookmark').hide()
			$('.bookmark-fill').show()
		}
		else{
			$('.bookmark').show()
			$('.bookmark-fill').hide()
		}
	}


	function renderComment (status){
		$('#comment-temp').show().children('div').children().text(status.text)
	}


	var input_data = JSON.parse($('#json').text());


	$.get('/api/like/0/', input_data, function(status){
		renderLike(status);
	});


	$.get('/api/bookmark/0/', input_data, function(status){
		renderBookmark(status);
	});


	function changeCount(obj, num){
		obj.text(+obj.text() + num)
	}

	
	function sendAJAX(inputData, method, like){
		$.ajax(`/api/like/0/?user=${inputData.user}&article=${inputData.article}`,
			{
			headers: {'X-CSRFTOKEN': inputData.csrfmiddlewaretoken},
			type: method,
			data: inputData,
			success: function(result,status,xhr) {
				renderLike(result || status);
				if(result){
					changeCount($(like ? '#like-count' : '#dislike-count'), 1)
				 	changeCount($(like ? '#dislike-count' : '#like-count'), -1)
				}
				else{
					changeCount($(like ? '#like-count' : '#dislike-count'), -1)
				}
			}
			});
	}
	
	
	
	input_data.csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val();

	$('#like-inline, #like-side').click(function(){
		input_data.is_like = true
		
		if($('.like-fill').css('display') == 'none'){
			if($('.dislike-fill').css('display') == 'none'){
				$.post('/api/like/', input_data, function(status){
					renderLike(status)
					changeCount($('#like-count'), 1)
					});	
			}
			else{
				 sendAJAX(input_data, 'PUT', true)
				 
				}
		}
		else{
			sendAJAX(input_data, 'DELETE', true)			
			}
	});
	
	$('#dislike-inline, #dislike-side').click(function(){
		input_data.is_like = false
		if($('.dislike-fill').css('display') == 'none'){
			if($('.like-fill').css('display') == 'none'){
				$.post('/api/like/', input_data, function(status){
					renderLike(status)
					changeCount($('#dislike-count'), 1)
					});	
			}
			else{
				 sendAJAX(input_data, 'PUT', false)
				}
		}
		else{
			sendAJAX(input_data, 'DELETE', false)
			}
	});
	
	
	$('.bookmark').click(function(){
		$.post('/api/bookmark/', input_data, function(status){
			renderBookmark(status)
		});
	});
	
	$('.bookmark-fill').click(function(){
		$.ajax(`/api/bookmark/0/?user=${input_data.user}&article=${input_data.article}`,
			{
			headers: {'X-CSRFTOKEN': input_data.csrfmiddlewaretoken},
			type: 'DELETE',
			data: input_data,
			success: function(result,status,xhr) {
				renderBookmark(status);
				}
			});	
	});
	
	
	
	$('.comment-btn, .response-btn').click(function(e){
		e.preventDefault()
		for(field of $(this).parent().serializeArray()){
			input_data[field.name] = field.value	
		}
		$(this).siblings('#id_text').val('')
		console.log(input_data)
		$.post('/api/comment/', input_data, function(status){
			renderComment(status)
			$('html, body').animate({
				scrollTop: ($('#comment-temp').offset().top-50)
			},500);
		});
	});
	

	function renderClike (status){
		if(status.id){
			id = status.comment
			if(status.is_like){
				$(`#p-${id} .clike, #p-${id} .disclike-fill`).hide()
				$(`#p-${id} .clike-fill, #p-${id} .disclike`).show()
			}
			else{
				$(`#p-${id} .disclike, #p-${id} .clike-fill`).hide()
				$(`#p-${id} .disclike-fill, #p-${id} .clike`).show()
			}
		}
		else{
			id = status
			$(`#p-${id} .clike, #p-${id} .disclike`).show()
			$(`#p-${id} .clike-fill, #p-${id} .disclike-fill`).hide()
		}
	}
	
	

	
	function sendAJAXc(inputData, method, like){
		id = inputData.comment
		$.ajax(`/api/clike/0/?user=${inputData.user}&comment=${inputData.comment}`,
			{
			headers: {'X-CSRFTOKEN': inputData.csrfmiddlewaretoken},
			type: method,
			data: inputData,
			success: function(result,status,xhr) {
				status = id

				renderClike(result || status);
				if(result){
					changeCount($(like ? `#p-${id} #clike-count` : `#p-${id} #disclike-count`), 1)
				 	changeCount($(like ? `#p-${id} #disclike-count` : `#p-${id} #clike-count`), -1)
				}
				else{
					changeCount($(like ? `#p-${id} #clike-count` : `#p-${id} #disclike-count`), -1)
				}
			}
			});
	}
	
	
	$('.clike-inline').click(function(){
		input_data.is_like = true
		id = $(this).prop('id')
		input_data.comment = id
		
		if($(`#p-${id} .clike-fill`).css('display') == 'none'){
			if($(`#p-${id} .disclike-fill`).css('display') == 'none'){
				$.post('/api/clike/', input_data, function(status){
					renderClike(status)
					changeCount($(`#p-${id} #clike-count`), 1)
					});	
			}
			else{
				 sendAJAXc(input_data, 'PUT', true)
				 
				}
		}
		else{
			sendAJAXc(input_data, 'DELETE', true)			
			}
	});
	
	
	$('.disclike-inline').click(function(){
		input_data.is_like = false
		id = $(this).prop('id')
		input_data.comment = id
		
		if($(`#p-${id} .disclike-fill`).css('display') == 'none'){
			if($(`#p-${id} .clike-fill`).css('display') == 'none'){
				$.post('/api/clike/', input_data, function(status){
					renderClike(status)
					changeCount($(`#p-${id} #disclike-count`), 1)
					});	
			}
			else{
				 sendAJAXc(input_data, 'PUT', false)
				 
				}
		}
		else{
			sendAJAXc(input_data, 'DELETE', false)			
			}
	});
	
	
	
	$('#follow').click(function(){
		$.post('/api/follow/', input_data, function(status){
			if(status.id){
				$('#un-follow').show()
				$('#follow').hide()
				changeCount($('#followers'), 1)
			}
		});
	});
	
	$('#un-follow').click(function(){
		$.ajax(`/api/follow/0/?user=${input_data.user}&author=${input_data.author}`,
			{
			headers: {'X-CSRFTOKEN': input_data.csrfmiddlewaretoken},
			type: 'DELETE',
			data: input_data,
			success: function(result,status,xhr) {
				$('#un-follow').hide()
				$('#follow').show()
				changeCount($('#followers'), -1)
				}
			});	
	});
console.log('eend')
});

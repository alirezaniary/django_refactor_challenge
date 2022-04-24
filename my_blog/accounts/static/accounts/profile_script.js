$(document).ready(function () {
	input_data = {csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()}
	
	function articleRenderer(articles){
		$artTemp = $('#templates .art')
		for(art of articles.results){
			$art = $artTemp.clone()
			$art.find('img').prop('src', art.img_path)
			artPath = `/@${art.username}/${art.id}`
			$art.find('a').prop('href', artPath)
			$art.find('h5').text(art.title)
			$art.find('.text-truncate').text(art.text)
			tags = art.tag.map(x => x.name);
			$art.find('small').text(tags)
			$art.find('.is_active').prop('checked', art.is_active).prop('id', art.id)
			$art.find('.is_valid').prop('checked', art.is_valid).prop('id', art.id)
			if($('#id').text() == art.username) $art.find('.is_valid').prop('disabled', true)
			if($('#id').text() != art.username) $art.find('.is_active').prop('disabled', true)
			$art.appendTo('#content')
			}
		
		
		$('.is_valid').click(function(){
			input_data.id = $(this).prop('id')
			input_data.validator = $('#id').attr('user')
			
			if ($(this).is(':checked')) {
				input_data.is_valid = true
			}
			else{
			  	input_data.is_valid = false
			}
			
			sendAJAX(input_data, 'article', 'PATCH', 'editor')
		})
		
		
		$('.is_active').click(function(){
			input_data.id = $(this).prop('id')
			if ($(this).is(':checked')) {
				input_data.is_active = true
			}
			else{
			  	input_data.is_active = false
			}
			console.log(input_data)
			sendAJAX(input_data, 'article', 'PATCH', 'profile')
		})
		
	}
	
	
	function commentRenderer(comments){
		$comTemp = $('#templates .comment')
		for(com of comments.results){
			$com = $comTemp.clone()
			$com.find('.card-body').prop('id', com.id)
			$com.find('#text').text(com.text)
			$com.find('.text-muted').text(com.pub_date)
			$com.find('a').text(com.article_title).prop('href', com.article_link)
			$com.find('.is_valid').prop('checked', com.is_valid).prop('id', com.id)
			if($('#id').attr('user') == com.user) $com.find('.is_valid').prop('disabled', true)
			$com.appendTo('#content')
		}
		$('.is_valid').click(function(){
			input_data.id = $(this).prop('id')
			input_data.validator = $('#id').attr('user')
			
			if ($(this).is(':checked')) {
				input_data.is_valid = true
			}
			else{
			  	input_data.is_valid = false
			}
			console.log(input_data)
			sendAJAX(input_data, 'comment', 'PATCH', 'editor')
			});
	}
	
	
	function authorRenderer(authors){
		$autTemp = $('#templates .author')
		for(aut of authors.results){
			$.get(`/api/author/${aut.author}/`,function(result){
			$aut = $autTemp.clone()
			$aut.prop('id',result.id)
			$aut.find('h4').text(result.full_name)
			$aut.find('.bio').text(result.bio)
			userUrl = `/@${result.username}/`
			$aut.find('a').prop('href', userUrl)
			$aut.find('img').prop('src', result.img_path)
			$aut.find('.number1').text(result.publications)
			$aut.find('.number2').text(result.followers)
			$aut.find('#un-follow').click(function(){
				$.ajax(`/api/follow/0/?user=${aut.user}&author=${aut.author}`,
					{
					headers: {'X-CSRFTOKEN': input_data.csrfmiddlewaretoken},
					type: 'DELETE',
					success: function(result,status,xhr) {
						$('#' + aut.author).hide()
						}
					});
				});
			$aut.appendTo('#content')
			});
		}
	}
	
	
	function flushContent(){
		$('#content').empty()
		$('#buttons').empty()
	}
	

	
	
	function sendAJAX(inputData, url, method, role){
		$.ajax(`/api/${url}/${inputData.id}/?${role}=${$('#id').text()}`,
			{
			headers: {'X-CSRFTOKEN': inputData.csrfmiddlewaretoken},
			type: method,
			data: inputData,
			success: function(result){
				console.log(result)
			}
			}).fail(function( jqXHR, textStatus, errorThrown ){
				alert(jqXHR, textStatus, errorThrown)
			})
		input_data = {csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()}
		}



	function nextPage(link, func){
		$('<a>').text('صفحه بعد').prop('href', '#').addClass('btn btn-outline-success').appendTo('#buttons').click(function(){
			$.get(link, function(result){
				flushContent()
				func(result);
				if(result.next) nextPage(result.next, func)
				if(result.previous) previusPage(result.previous, func)
			});
		})
	}

	function previusPage(link, func){
		$('<a>').text('صفحه قبل').prop('href', '#').addClass('btn btn-outline-success').appendTo('#buttons').click(function(){
			$.get(link, function(result){
				flushContent()
				func(result);
				if(result.next) nextPage(result.next, func)
				if(result.previous) previusPage(result.previous, func)
			});
		})
	}
	



	$('#author-articles').click(function(){
		flushContent()
		$.get('/api/article/', {profile: $('#id').text()}, function(data){
			articleRenderer(data);
			if(data.next) nextPage(data.next, articleRenderer)
			if(data.previous) previusPage(data.previous, articleRenderer)
		});
	});
	
	
	$('.not-valid-articles').click(function(){
		flushContent()
		$.get('/api/article/', {editor: $('#id').text(),
								topic: $(this).prop('id')}, function(data){
			articleRenderer(data);
			if(data.next) nextPage(data.next, articleRenderer)
			if(data.previous) previusPage(data.previous, articleRenderer)
			});
	});
	
	
	$('#bookmarked-articles').click(function(){
		flushContent()
		$.get('/api/article/', {bookmark: $('#id').text()}, function(data){
			articleRenderer(data);
			if(data.next) nextPage(data.next, articleRenderer)
			if(data.previous) previusPage(data.previous, articleRenderer)
			});
	});
	
	
	$('#liked-articles').click(function(){
		flushContent()
		$.get('/api/article/', {liked: $('#id').text()}, function(data){
			articleRenderer(data);
			if(data.next) nextPage(data.next, articleRenderer)
			if(data.previous) previusPage(data.previous, articleRenderer)
			});
	});
	
	
	$('#user-comments').click(function(){
		flushContent()
		$.get('/api/comment/', {profile: $('#id').text()}, function(data){
			commentRenderer(data);
			if(data.next) nextPage(data.next, commentRenderer)
			if(data.previous) previusPage(data.previous, commentRenderer)
			});
	});
	
	$('.not-valid-comments').click(function(){
		flushContent()
		$.get('/api/comment/', {editor: $('#id').text(),
								topic: $(this).prop('id')}, function(data){
			commentRenderer(data);
			if(data.next) nextPage(data.next, commentRenderer)
			if(data.previous) previusPage(data.previous, commentRenderer)
			});
	});
	
	
	$('#following-authors').click(function(){
		flushContent()
		$.get('/api/follow/', {profile: $('#id').text()}, function(data){
			authorRenderer(data);
			if(data.next) nextPage(data.next, authorRenderer)
			if(data.previous) previusPage(data.previous, authorRenderer)
			});
	});
	console.log('dd')
});

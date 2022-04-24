// progressbar measures height of article
// ToDo exclude comments
$(document).ready(function () {

	// navbar and footer hide and seek
	var prevScrollpos = window.pageYOffset;
	window.onscroll = function() {
	var currentScrollPos = window.pageYOffset;
	  if (prevScrollpos > currentScrollPos) {
		document.getElementById("navbar").style.top = "0";
		$('.dropdown-menu-nav').removeClass('d-none')
	  } else {
		document.getElementById("navbar").style.top = -$('#navbar').outerHeight() + 'px';
		$('.dropdown-menu-nav').addClass('d-none')
		$('#search-results').hide()
	  }
	  if (prevScrollpos < currentScrollPos) {
		document.getElementById("footer").style.bottom = "0";
	  } else {
		document.getElementById("footer").style.bottom = -$('#footer').outerHeight() + 'px';
	  }
	  prevScrollpos = currentScrollPos;
	}

	function tagRenderer(tags){
		$('#tagS').remove()
		$tagSection = $('<div>').addClass('card-body').append(
			$('<label>').text('جستجو در برچسب ها').addClass('p-2 bg-secondary')
		).prop('id', 'tagS')
		for(tag of tags.results){

			$tagSection.append(
				$('<a>').addClass('px-1 text-decoration-none').text(tag.name).prop('href', `/tags/${tag.name}`)
			)
		}
		$('#search-results').append($tagSection)
	}


	function topicRenderer(topics){
		$('topicS').remove()
		$topicSection = $('<div>').addClass('card-body').append(
			$('<label>').text('جستجو در دسته بندی ها').addClass('p-2 bg-secondary')
		).prop('id', 'topicS')
		for(topic of topics.results){

			$topicSection.append(
				$('<a>').addClass('px-1 text-decoration-none').text(topic).prop('href', `/tags/${topic}`)
			)
		}
		$('#search-results').append($topicSection)
	}

	function artRenderer(arts){
		$('#artS').remove()
		$articleSection = $('<div>').addClass('card-body d-flex flex-column').append(
                          $('<label>').text('جستجو در مقالات').addClass('p-2 bg-secondary')
                ).prop('id', 'artS')

		for(art of arts){
			$articleSection.append(
				$('<a>').addClass('px-1 text-decoration-none').text(art.title).prop('href', `/@${art.username}/${art.id}`)
			)
		}
		$('#search-results').append($articleSection)
	}

	$('#search-bar').keyup(function(event){
			if(! $('#search-results').is(":visible")) $('#search-results').show()
			var keycode = (event.keyCode ? event.keyCode : event.which);
			$('#search-results').empty()
			if(keycode>=37 && keycode<=40){
				console.log('salam chetory')
			}
			else{
				$('#search-results').empty()
				if (keycode != 8){
					$.get('/api/search/',{q: $(this).val()},
					function(data){
						artRenderer(data);
						}
	  				);
  				}

  				$.get('/api/tag/',{name: $(this).val()},
				function(data){
					if(data.results.length) tagRenderer(data);
					}
  				);

  				$.get('/api/topic/',{name: $(this).val()},
				function(data){
					if(data.results.length) topicRenderer(data);
					}
  				);
  			}
	});
	
	$(window).click(function () { $('#search-results').hide() }); 
	$('#search-results').click(function (event) {event.stopPropagation();});
console.log('ho')
});

Pace.start();

var domain = document.domain;
if (domain == 'localhost' || domain == '127.0.0.1')
	domain += ':8000';

var o2api = {
	endpoint: 'http://'+domain+'/api/v1/{0}/?format=json{1}'
};

/* REST API */
$(document).ready(function(){
	if($('#page-ombudsman').length){
		o2api.ombudsman = {};
		$.get(o2api.endpoint.format('ombudsmanoffice', ''), function(data){
			o2api.ombudsman.meta = data.meta;
			
			var tpl = $('#tpl-ombudsman').html();
		    $('#list-items').html(_.template(tpl, {objects: data.objects}));
		    
			$('#more-results').removeClass('disabled');
		    $('#search').removeClass('disabled');
		});
	    pageOmbudsman();
	} else if($('#page-ombudsman-view').length){
		o2api.ombudsmanView = {};
		o2api.ombudsmanView.ombudsmanId = ombudsmanId;
		o2api.ombudsmanView.ombudsmanSlug = ombudsmanSlug;
		
		$.get(o2api.endpoint.format('tickets', '&belongs_to={0}'.format(o2api.ombudsmanView.ombudsmanId)), function(data){
			o2api.ombudsmanView.meta = data.meta;
			
			var tpl = $('#tpl-ticket').html();
		    $('#list-items').html(_.template(tpl, {objects: data.objects}));
		    
			$('#more-results').removeClass('disabled');
		    $('#search').removeClass('disabled');
		});
	    pageOmbudsmanView();
	} else if($('#page-users').length){
		o2api.users = {};
		$.get(o2api.endpoint.format('users', ''), function(data){
			o2api.users.meta = data.meta;
			
			var tpl = $('#tpl-users').html();
		    $('#list-items').html(_.template(tpl, {objects: data.objects}));
		    
			$('#more-results').removeClass('disabled');
		    $('#search').removeClass('disabled');
		});
	    pageUsers();
	} else if($('#page-user-view').length){
		o2api.userView = {};
		o2api.userView.userId = userId;
		
		$.get(o2api.endpoint.format('tickets', '&created_by={0}'.format(o2api.userView.userId)), function(data){
			o2api.userView.meta = data.meta;
			
			var tpl = $('#tpl-ticket').html();
		    $('#list-items').html(_.template(tpl, {objects: data.objects}));
		    
			$('#more-results').removeClass('disabled');
		    $('#search').removeClass('disabled');
		});
	    pageUserView();
	}
	
	function pageOmbudsman(){
	    $('#more-results').click(function(e){
	    	e.preventDefault();
    		o2api.ombudsman.filter = getFilterOmbudsman();

		    $('#more-results').addClass('disabled');
		    if(o2api.ombudsman.meta.next) {
			    $('#search').addClass('disabled');
		    	$.get(o2api.ombudsman.meta.next, function(data){
		    		o2api.ombudsman.meta = data.meta;
		    		
		    		var tpl = $('#tpl-ombudsman').html();
		    		$('#list-items').append(_.template(tpl, {objects: data.objects}));
	
				    $('#more-results').removeClass('disabled');
				    $('#search').removeClass('disabled');
		    	});
		    }
		    return false;
	    });
	    
	    $('#search').click(function(e){
	    	e.preventDefault();
    		o2api.ombudsman.filter = getFilterOmbudsman();

		    $('#more-results').addClass('disabled');
		    $('#search').addClass('disabled');
		    
	    	$.get(o2api.endpoint.format('ombudsmanoffice', o2api.ombudsman.filter), function(data){
	    		o2api.ombudsman.meta = data.meta;
	    		
	    		if(data.objects.length > 0){	    		
					var tpl = $('#tpl-ombudsman').html();
				    $('#list-items').html(_.template(tpl, {objects: data.objects}));
				    $('#more-results').removeClass('disabled');
	    		} else {
	    			$('#list-items').html('<div class="alert alert-orange"><h3>Nenhum registro encontrado</h3></div>');
	    		}
	    		
			    $('#search').removeClass('disabled');
	    	});
	    	return false;
	    });
	}
	
	function pageOmbudsmanView(){
	    $('#more-results').click(function(e){
	    	e.preventDefault();
    		o2api.ombudsmanView.filter = getFilterOmbudsmanView();

		    $('#more-results').addClass('disabled');
		    if(o2api.ombudsmanView.meta.next) {
			    $('#search').addClass('disabled');
		    	$.get(o2api.ombudsmanView.meta.next, function(data){
		    		o2api.ombudsmanView.meta = data.meta;
		    		
		    		var tpl = $('#tpl-ticket').html();
		    		$('#list-items').append(_.template(tpl, {objects: data.objects}));
	
				    $('#more-results').removeClass('disabled');
				    $('#search').removeClass('disabled');
		    	});
		    }
		    return false;
	    });
	    
	    $('#search').click(function(e){
	    	e.preventDefault();
    		o2api.ombudsmanView.filter = getFilterOmbudsmanView();

		    $('#more-results').addClass('disabled');
		    $('#search').addClass('disabled');
		    
	    	$.get(o2api.endpoint.format('tickets', o2api.ombudsmanView.filter), function(data){
	    		o2api.ombudsmanView.meta = data.meta;
	    		
	    		if(data.objects.length > 0){	    		
					var tpl = $('#tpl-ticket').html();
				    $('#list-items').html(_.template(tpl, {objects: data.objects}));
				    $('#more-results').removeClass('disabled');
	    		} else {
	    			$('#list-items').html('<div class="alert alert-orange"><h3>Nenhum registro encontrado</h3></div>');
	    		}
	    		
			    $('#search').removeClass('disabled');
	    	});
	    	return false;
	    });
	}
	
	function pageUsers(){
	    $('#more-results').click(function(e){
	    	e.preventDefault();
    		o2api.users.filter = getFilterUsers();

		    $('#more-results').addClass('disabled');
		    if(o2api.users.meta.next) {
			    $('#search').addClass('disabled');
		    	$.get(o2api.users.meta.next, function(data){
		    		o2api.users.meta = data.meta;
		    		
		    		var tpl = $('#tpl-users').html();
		    		$('#list-items').append(_.template(tpl, {objects: data.objects}));
	
				    $('#more-results').removeClass('disabled');
				    $('#search').removeClass('disabled');
		    	});
		    }
		    return false;
	    });
	    
	    $('#search').click(function(e){
	    	e.preventDefault();
    		o2api.users.filter = getFilterUsers();

		    $('#more-results').addClass('disabled');
		    $('#search').addClass('disabled');
		    
	    	$.get(o2api.endpoint.format('users', o2api.users.filter), function(data){
	    		o2api.users.meta = data.meta;
	    		
	    		if(data.objects.length > 0){	    		
					var tpl = $('#tpl-users').html();
				    $('#list-items').html(_.template(tpl, {objects: data.objects}));
				    $('#more-results').removeClass('disabled');
	    		} else {
	    			$('#list-items').html('<div class="alert alert-orange"><h3>Nenhum registro encontrado</h3></div>');
	    		}
	    		
			    $('#search').removeClass('disabled');
	    	});
	    	return false;
	    });
	}
	
	function pageUserView(){
	    $('#more-results').click(function(e){
	    	e.preventDefault();
    		o2api.userView.filter = getFilterUserView();

		    $('#more-results').addClass('disabled');
		    if(o2api.userView.meta.next) {
			    $('#search').addClass('disabled');
		    	$.get(o2api.userView.meta.next, function(data){
		    		o2api.userView.meta = data.meta;
		    		
		    		var tpl = $('#tpl-ticket').html();
		    		$('#list-items').append(_.template(tpl, {objects: data.objects}));
	
				    $('#more-results').removeClass('disabled');
				    $('#search').removeClass('disabled');
		    	});
		    }
		    return false;
	    });
	    
	    $('#search').click(function(e){
	    	e.preventDefault();
    		o2api.userView.filter = getFilterUserView();

		    $('#more-results').addClass('disabled');
		    $('#search').addClass('disabled');
		    
	    	$.get(o2api.endpoint.format('tickets', o2api.userView.filter), function(data){
	    		o2api.userView.meta = data.meta;
	    		
	    		if(data.objects.length > 0){	    		
					var tpl = $('#tpl-ticket').html();
				    $('#list-items').html(_.template(tpl, {objects: data.objects}));
				    $('#more-results').removeClass('disabled');
	    		} else {
	    			$('#list-items').html('<div class="alert alert-orange"><h3>Nenhum registro encontrado</h3></div>');
	    		}
	    		
			    $('#search').removeClass('disabled');
	    	});
	    	return false;
	    });
	}
	
	function getFilterOmbudsman(){
		var ombudsmanName = $('#ombudsman-name').val();
		var institutionName = $('#institution-name').val();
		var institutionType = $("input[name=institution-type]:checked").val();
		var institutionCountry = $('#institution-country').val() === 'ALL' ? '' : $('#institution-country').val();
		var institutionState = $('#institution-state').val() === 'ALL' ? '' : $('#institution-state').val();
		var institutionCity = $('#institution-city').val() === 'ALL' ? '' : $('#institution-city').val();
		
		return '&name__icontains={0}&institution_name__icontains={1}&institution_type__icontains={2}'.format(
			ombudsmanName, 
			institutionName, 
			institutionType
			/*institutionCountry, 
			institutionState, 
			institutionCity*/
		);
	}
	
	function getFilterOmbudsmanView(){
		var ticketTitle = $('#ticket-title').val();
		var ticketCategory = $('#ticket-categories').val() === 'ALL' ? '' : $('#ticket-categories').val();
		
		return '&belongs_to={0}&title__icontains={1}&category__icontains={2}'.format(
			o2api.ombudsmanView.ombudsmanId,
			ticketTitle, 
			ticketCategory 
		);
	}
	
	function getFilterUsers(){
		var userUsername = $('#user-username').val();
		var userFirstName = $('#user-first-name').val();
		var userLastName = $('#user-last-name').val();
		var userSex = $("input[name=user-sex]:checked").val();
		var userCountry = $('#user-country').val() === 'ALL' ? '' : $('#user-country').val();
		var userState = $('#user-state').val() === 'ALL' ? '' : $('#user-state').val();
		var userCity = $('#user-city').val() === 'ALL' ? '' : $('#user-city').val();
		
		return '&username__icontains={0}&first_name__icontains={1}&last_name__icontains={2}&sex__icontains={3}'.format(
			userUsername, 
			userFirstName, 
			userLastName, 
			userSex 
			/*userCountry, 
			userState,
			userCity*/
		);
	}
	
	function getFilterUserView(){
		var ticketTitle = $('#ticket-title').val();
		var ticketOmbudsman = $('#ticket-ombudsman').val() === 'ALL' ? '' : $('#ticket-ombudsman').val();
		
		if(ticketOmbudsman.length)
			return '&created_by={0}&belongs_to={1}&title__icontains={2}'.format(
				o2api.userView.userId,
				ticketOmbudsman,
				ticketTitle
			);
		else
			return '&created_by={0}&title__icontains={1}'.format(
				o2api.userView.userId,
				ticketTitle
			);
	}
});

$(document).ready(function(){
	windowResize();
    $(window).resize(function() {
    	windowResize();
	});
    
    $(".collapse").collapse();
    
    $("[rel='tooltip']").tooltip();
    
    $("a[rel^='prettyPhoto']").prettyPhoto();
    
    $(".fit-vid").fitVids();

    $('select').selectpicker();
    
    $('.datepicker').datepicker({
    	format: 'dd/mm/yyyy'
    });
    
    $("input, select, textarea").not("[type='submit']").not("[type='button']").jqBootstrapValidation();
    
	$('.animation').waypoint(function() {
        $(this).addClass('animated');
	});
	
	$('.scrolltop a').on('click', function() {
		$('html, body').animate({scrollTop:0}, 'slow');
		return false;
	});
	
	if (!isTouchDevice() && $(window).width() > 767) {
		var topbar = $("#top-bar").height();
		$('.header-top-wrap').scrollToFixed({
			preFixed: function()  {
				$('.header-top-wrap').addClass("nav-fixed");
				$(document).scroll(function(){
					if ($(document).scrollTop() > topbar+100 ) {
						$('.header-top-wrap .container').css({
							'padding-top' : '5px',
							'padding-bottom' : '5px'
						});
					} 
					else {
						$('.header-top-wrap .container').css({
							'padding-top' : '35px',
							'padding-bottom' : '35px'
						});
					}
				})
			},
			postFixed: function() {
				$('.header-top-wrap').removeClass("nav-fixed")
			}
		})
	}
});


/* ISOTOPE */
$(window).load(function(){  
	// cache container
	var $container = $('#portfolio-page');
	// initialize isotope
	$container.isotope({
	  // options...
	});
	
	// filter items when filter link is clicked
	$('#filters a').click(function(){
	  var selector = $(this).attr('data-filter');
	  $container.isotope({ filter: selector });
	  
	  //active classes
	  $('#filters li a').removeClass('active');
	  $(this).addClass('active');
	  
	  return false;
	});
	
	if ( isTouchDevice() ) {
	$('#sort-portfolio').click(function(){
	  $('#filters').toggle(1);
	  return false;
		})
	}

});

function isTouchDevice() {
  return !!('ontouchstart' in window) || !!('onmsgesturechange' in window);
};

function windowResize(){
	if ($(window).width() > 767) {
        $('li:has(ul)').addClass('dropdown');
        $('li:has(ul)').children('a').addClass('dropdown-tg');
        $('li ul li').children('a').removeClass('dropdown-tg');

		$('#login').addClass('link-effect-1');
		$('#register').addClass('link-effect-1');
	} else {
		$('#login').removeClass('link-effect-1');
		$('#register').removeClass('link-effect-1');
	}
}

if (!String.prototype.format) {
	String.prototype.format = function() {
		var args = arguments;
		return this.replace(/{(\d+)}/g, function(match, number) { 
			return typeof args[number] != 'undefined'
				? args[number]
			: match
			;
		});
	};
}

if (!String.prototype.replaceAll) {
	String.prototype.replaceAll = function (find, replace) {
	    var str = this;
	    return str.replace(new RegExp(find.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), 'g'), replace);
	};
}
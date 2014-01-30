/*! SocialCount - v0.1.5 - 2013-01-22
* https://github.com/filamentgroup/SocialCount
* Copyright (c) 2013 zachleat; Licensed MIT */
(function(e,t,n){function s(e,n){var r=t.createElement("social").style,i="webkit Moz o ms".split(" ");if(n in r)return!0;for(var s=0,o=i.length;s<o;s++)if(i[s]+e in r)return!0;return!1}function o(e){var t=e.split("/");return t.pop(),t.join("/")+"/"}function u(){var e;return n("script").each(function(){var t=this.src||"",n;if(t.match(a.scriptSrcRegex))return e=o(t),!1}),e}var r,i,a={isGradeA:"querySelectorAll"in t&&!e.blackberry&&!("ontouchstart"in window)&&!("onmsgesturechange"in window),minCount:1,serviceUrl:"service/index.php",initSelector:".socialcount",classes:{gradeA:"grade-a",active:"active",touch:"touch",hover:"hover",noTransforms:"no-transforms",showCounts:"counts",countContent:"count",minCount:"minimum",activateOnHover:"activate-on-hover",activateOnClick:"activate-on-click"},thousandCharacter:"K",millionCharacter:"M",missingResultText:"-",activateOnClick:!1,selectors:{facebook:".facebook",twitter:".twitter",googleplus:".googleplus"},locale:t.documentElement?t.documentElement.lang||"":"",googleplusTooltip:"table.gc-bubbleDefault",scriptSrcRegex:/socialcount[\w.]*.js/i,plugins:{init:[],bind:[]},cache:{},removeFileName:o,resolveServiceDir:u,isCssAnimations:function(){return s("AnimationName","animationName")},isCssTransforms:function(){return s("Transform","transform")},getUrl:function(e){return e.attr("data-url")||location.href},getShareText:function(e){return e.attr("data-share-text")||""},getFacebookAction:function(e){return(e.attr("data-facebook-action")||"like").toLowerCase()},isCountsEnabled:function(e){return e.attr("data-counts")==="true"},isSmallSize:function(e){return e.is(".socialcount-small")},getCounts:function(e,t){var r=a.selectors,s=a.cache,o={},f,l,c;for(c in r)f=e.find(r[c]),l=f.find("."+a.classes.countContent),l.length?o[c]=l:(o[c]=i.clone(),f.append(o[c]));return s[t]||(s[t]=n.ajax({url:u()+a.serviceUrl,data:{url:t},dataType:"json"})),s[t].done(function(t){for(var n in t)t.hasOwnProperty(n)&&o[n]&&t[n]>a.minCount&&o[n].addClass(a.classes.minCount).html(a.normalizeCount(t[n]))}),s[t]},init:function(e){var t=a.getFacebookAction(e),n=[t],r=a.isSmallSize(e),i=a.getUrl(e),s=a.plugins.init,o=a.isCountsEnabled(e);a.isGradeA&&n.push(a.classes.gradeA),a.isCssTransforms()||n.push(a.classes.noTransforms),o&&n.push(a.classes.showCounts),a.activateOnClick?n.push(a.classes.activateOnClick):n.push(a.classes.activateOnHover),a.locale&&n.push(a.locale),e.addClass(n.join(" "));for(var u=0,f=s.length;u<f;u++)s[u].call(e);a.isGradeA&&a.bindEvents(e,i,t,r),o&&!r&&a.getCounts(e,i)},normalizeCount:function(e){return!e&&e!==0?a.missingResultText:e>=1e6?Math.floor(e/1e6)+a.millionCharacter:e>=1e5?Math.floor(e/1e3)+a.thousandCharacter:e>1e3?(e/1e3).toFixed(1).replace(/\.0/,"")+a.thousandCharacter:e},bindEvents:function(e,i,s,o){function u(e,i,s){var o=!1,u=!1;e.closest("li").bind("mouseenter",function(e){var t=n(this).closest("li");t.addClass(a.classes.hover),u=!0,n(document).on("mouseenter.socialcount mouseleave.socialcount",a.googleplusTooltip,function(e){o=e.type==="mouseenter",!o&&!u&&t.removeClass(a.classes.hover)})}).bind("mouseleave",function(e){var t=this;window.setTimeout(function(){u=!1,!o&&!u&&(n(document).off(".socialcount"),n(t).closest("li").removeClass(a.classes.hover))},0)}),e.one(a.activateOnClick?"click":"mouseover",function(e){a.activateOnClick&&(e.preventDefault(),e.stopPropagation());var o=n(this),u=o.closest("li"),f=r.clone(),l=n(i),c=n('<div class="button"/>').append(l),h,p,d=n.Deferred();d.promise().always(function(){var e=u.find("iframe");e.length?e.bind("load",function(){f.remove()}):f.remove()}),u.addClass(a.classes.active).append(f).append(c),s?(h=t.createElement("script"),h.src=s,h.attachEvent?h.attachEvent("onreadystatechange",function(){(h.readyState==="loaded"||h.readyState==="complete")&&d.resolve()}):n(h).bind("load",d.resolve),t.body.appendChild(h)):l.is("iframe")&&d.resolve()})}if(!o){var f=a.getShareText(e);u(e.find(a.selectors.facebook+" a"),'<iframe src="//www.facebook.com/plugins/like.php?href='+encodeURI(i)+(a.locale?"&locale="+a.locale:"")+"&amp;send=false&amp;layout=button_count&amp;width=100&amp;show_faces=true&amp;action="+s+'&amp;colorscheme=light&amp;font=arial&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden;" allowTransparency="true"></iframe>'),u(e.find(a.selectors.twitter+" a"),'<a href="https://twitter.com/share" class="twitter-share-button" data-url="'+encodeURI(i)+'"'+(f?' data-text="'+f+'"':"")+' data-count="none" data-dnt="true">Tweet</a>',"//platform.twitter.com/widgets.js"),u(e.find(a.selectors.googleplus+" a"),'<div class="g-plusone" data-size="medium" data-annotation="none"></div>',"//apis.google.com/js/plusone.js")}var l=a.plugins.bind;for(var c=0,h=l.length;c<h;c++)l[c].call(e,u,i,o)}};n(function(){r=n("<div>").addClass("loading").html(a.isCssAnimations()?(new Array(4)).join('<div class="dot"></div>'):"Loading"),i=n("<span>").addClass(a.classes.countContent).html("&#160;"),n(a.initSelector).each(function(){var e=n(this);a.init(e)})}),window.SocialCount=a})(window,window.document,jQuery);
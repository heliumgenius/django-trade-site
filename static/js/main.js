document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('img[data-fallback]').forEach(function(i){i.addEventListener('error',function(){var w=i.closest('.card-img-wrapper,.product-image-wrapper');var f=i.getAttribute('data-fallback')||'Product';var e=document.createElement('div');e.className=w&&w.classList.contains('product-image-wrapper')?'product-img-fallback-lg':'product-img-fallback';e.textContent=f.substring(0,20);if(i.parentElement)i.parentElement.replaceChild(e,i)})});
    document.querySelectorAll('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(e){var t=document.querySelector(this.getAttribute('href'));if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth'})}})});
    var p=window.location.pathname;document.querySelectorAll('.navbar-nav .nav-link').forEach(function(l){var h=l.getAttribute('href');if(h&&p.indexOf(h)!==-1&&h.length>3)l.classList.add('active')});
});

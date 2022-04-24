var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
});

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
});

var darkMode = document.getElementById('darkMode');


window.addEventListener('load', function () {
  if (darkMode) {
    initTheme();
    darkMode.addEventListener('change', function () {
      resetTheme();
    });
  }
});

function initTheme() {
  var darkThemeSelected = localStorage.getItem('darkMode') !== null && localStorage.getItem('darkMode') === 'dark';
  darkMode.checked = darkThemeSelected;
  darkThemeSelected ? document.body.setAttribute('data-theme', 'dark') : document.body.removeAttribute('data-theme');
  //darkThemeSelected ? document.getElementById(imgID).src = darkImg : document.getElementById(imgID).src = lightImg;
  //darkThemeSelected ? document.getElementById(darkLabel).innerHTML = darkLang : document.getElementById(darkLabel).innerHTML = lightLang;
}

function resetTheme() {
  if (darkMode.checked) {
    document.body.setAttribute('data-theme', 'dark');
    localStorage.setItem('darkMode', 'dark');
    //document.getElementById(imgID).src = darkImg;
    //document.getElementById(darkLabel).innerHTML = darkLang;
  } else {
    document.body.removeAttribute('data-theme');
    localStorage.removeItem('darkMode');
    //document.getElementById(imgID).src = lightImg;
    //document.getElementById(darkLabel).innerHTML = lightLang;
  }
}

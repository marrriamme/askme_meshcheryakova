(() => {
  'use strict'

  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const setTheme = () => {
    document.documentElement.setAttribute('data-bs-theme', 'light');
  }

  setTheme(); 

  window.addEventListener('DOMContentLoaded', () => {
    setStoredTheme('light'); 
    setTheme(); 


  });
})();

function toggleActive(element) {
  element.classList.toggle('active');
}
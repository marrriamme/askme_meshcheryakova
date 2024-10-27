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



function toggleActive(event, type) {
  event.preventDefault();
  const icon = event.currentTarget.querySelector('img');
  const countElement = icon.nextElementSibling; // Соседний элемент, содержащий число

  let count = parseInt(countElement.innerText);
  
  if (type === 'like') {
      icon.classList.toggle('active');
      countElement.innerText = icon.classList.contains('active') ? count + 1 : count - 1;
  } else if (type === 'dislike') {
      icon.classList.toggle('active');
      countElement.innerText = icon.classList.contains('active') ? count + 1 : count - 1;
  }
}



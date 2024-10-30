function toggleActive(event, type, questionId) {
  event.preventDefault();

  const likeIcon = document.getElementById(`like-${questionId}`);
  const dislikeIcon = document.getElementById(`dislike-${questionId}`);
  const countElement = document.getElementById(`like-counter-${questionId}`);

  let count = parseInt(countElement.innerText);

  if (type === 'like') {
    if (likeIcon.classList.contains('active')) {
      likeIcon.classList.remove('active');
      countElement.innerText = count - 1;
    } else {
      if (dislikeIcon.classList.contains('active')) {
        dislikeIcon.classList.remove('active');
        countElement.innerText = count + 2;
      } else {
        countElement.innerText = count + 1;
      }
      likeIcon.classList.add('active');
    }
  } else if (type === 'dislike') {
    if (dislikeIcon.classList.contains('active')) {
      dislikeIcon.classList.remove('active');
      countElement.innerText = count + 1;
    } else {
      if (likeIcon.classList.contains('active')) {
        likeIcon.classList.remove('active');
        countElement.innerText = count - 2;
      } else {
        countElement.innerText = count - 1;
      }
      dislikeIcon.classList.add('active');
    }
  }
}



function setCorrectAnswer(answerId) {
  const checkboxes = document.querySelectorAll('.form-check-input');
  checkboxes.forEach(checkbox => {
    if (checkbox.id !== `correct-${answerId}`) {
      checkbox.checked = false;
    }
  });
}

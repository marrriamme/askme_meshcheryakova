function toggleQuestionActive(event, type, cardID) {
  event.preventDefault();

  const likeIcon = document.getElementById(`question-like-${cardID}`);
  const dislikeIcon = document.getElementById(`question-dislike-${cardID}`);
  const countElement = document.getElementById(`question-like-counter-${cardID}`);

  toggleHTMLElements(type, likeIcon, dislikeIcon, countElement)
}

function toggleAnswerActive(event, type, cardID) {
  event.preventDefault();

  const likeIcon = document.getElementById(`answer-like-${cardID}`);
  const dislikeIcon = document.getElementById(`answer-dislike-${cardID}`);
  const countElement = document.getElementById(`answer-like-counter-${cardID}`);

  toggleHTMLElements(type, likeIcon, dislikeIcon, countElement)
}

function toggleHTMLElements(type, likeIcon, dislikeIcon, countElement) {
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



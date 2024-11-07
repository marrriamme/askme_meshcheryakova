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



function setCorrectAnswer(answerId) {
  var checkbox = document.getElementById('correct-' + answerId);
  var url = '/set-correct-answer/' + answerId + '/';  // Путь для обновления состояния ответа на сервере

  // Отправляем запрос на сервер для обновления флага
  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({ 'is_correct': checkbox.checked })
  }).then(function(response) {
      if (checkbox.checked) {
          checkbox.parentNode.classList.add('text-success');  // Зеленый цвет для выбранного ответа
      } else {
          checkbox.parentNode.classList.remove('text-success');  // Убираем зеленый цвет
      }
  });
}
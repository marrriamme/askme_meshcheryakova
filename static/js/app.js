// function toggleQuestionActive(event, type, cardID) {
//   event.preventDefault();

//   const likeIcon = document.getElementById(`question-like-${cardID}`);
//   const dislikeIcon = document.getElementById(`question-dislike-${cardID}`);
//   const countElement = document.getElementById(`question-like-counter-${cardID}`);

//   toggleHTMLElements(type, likeIcon, dislikeIcon, countElement)
// }

// function toggleAnswerActive(event, type, cardID) {
//   event.preventDefault();

//   const likeIcon = document.getElementById(`answer-like-${cardID}`);
//   const dislikeIcon = document.getElementById(`answer-dislike-${cardID}`);
//   const countElement = document.getElementById(`answer-like-counter-${cardID}`);

//   toggleHTMLElements(type, likeIcon, dislikeIcon, countElement)
// }

// function toggleHTMLElements(type, likeIcon, dislikeIcon, countElement) {
//   let count = parseInt(countElement.innerText);

//   if (type === 'like') {
//     if (likeIcon.classList.contains('active')) {
//       likeIcon.classList.remove('active');
//       countElement.innerText = count - 1;
//     } else {
//       if (dislikeIcon.classList.contains('active')) {
//         dislikeIcon.classList.remove('active');
//         countElement.innerText = count + 2;
//       } else {
//         countElement.innerText = count + 1;
//       }
//       likeIcon.classList.add('active');
//     }
//   } else if (type === 'dislike') {
//     if (dislikeIcon.classList.contains('active')) {
//       dislikeIcon.classList.remove('active');
//       countElement.innerText = count + 1;
//     } else {
//       if (likeIcon.classList.contains('active')) {
//         likeIcon.classList.remove('active');
//         countElement.innerText = count - 2;
//       } else {
//         countElement.innerText = count - 1;
//       }
//       dislikeIcon.classList.add('active');
//     }
//   }
// }


function likeQuestion(questionId) {
    const url = document.querySelector(`#question-like-${questionId}`).closest('a').getAttribute('data-url');
    
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCSRFToken() 
        }
    })
    .then(response => {
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('question-like-counter-' + questionId).textContent = data.rating;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function dislikeQuestion(questionId) {
    const url = document.querySelector(`#question-dislike-${questionId}`).closest('a').getAttribute('data-url');
    
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCSRFToken() 
        }
    })
    .then(response => {
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('question-like-counter-' + questionId).textContent = data.rating;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Функция для получения CSRF-токена
function getCSRFToken() {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfTokenElement ? csrfTokenElement.value : '';
}


function likeAnswer(answerId) {
    const url = document.querySelector(`#answer-like-${answerId}`).closest('a').getAttribute('data-url');
    
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCSRFToken() 
        }
    })
    .then(response => {
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('answer-like-counter-' + answerId).textContent = data.rating;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function dislikeAnswer(answerId) {
    const url = document.querySelector(`#answer-dislike-${answerId}`).closest('a').getAttribute('data-url');
    
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCSRFToken() 
        }
    })
    .then(response => {
        if (response.status === 403) {
            console.error("CSRF token error.");
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('answer-like-counter-' + answerId).textContent = data.rating;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function getCSRFToken() {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfTokenElement ? csrfTokenElement.value : '';
}

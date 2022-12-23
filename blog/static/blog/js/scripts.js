// Добавление рейтинга к статьям
// 1. в файле scripts.js - в документе, с помощью querySelector - ищем форму rating
const rating = document.querySelector('form[name=rating]');

// 2. когда у формы вызовится событие change
rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    // 3. создавая FormData и передав нашу форму, мы получим значение наших полей
    let data = new FormData(this);
    // 4. с помощью fetch, на url из нашей action={% url %}, передаём пост запросы, в теле body нашу data
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
    // 5. При успешном ответе - Рейтинг установлен, при отрицательном - Ошибка
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});
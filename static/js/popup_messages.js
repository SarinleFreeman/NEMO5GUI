document.addEventListener('DOMContentLoaded', function () {
    console.log('Script loaded');
    const messages = document.querySelectorAll('#message-list li');
    messages.forEach(function (message) {
        console.log('Showing message:', message.innerText);
        alert(message.innerText);
    });
});
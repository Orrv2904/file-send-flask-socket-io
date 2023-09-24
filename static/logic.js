const socket = io.connect(`http://${document.domain}:${location.port}`);

socket.on('connect', () => {
    console.log('Conectado al servidor de Socket.IO');
});

const joinButton = document.querySelector('#join');
const sendButton = document.querySelector('#send');

joinButton.addEventListener('click', () => {
    const username = document.querySelector('#username').value;
    const room = document.querySelector('#room').value;

    socket.emit('join', { username, room });
});

sendButton.addEventListener('click', () => {
    const username = document.querySelector('#username').value;
    const room = document.querySelector('#room').value;
    const message = document.querySelector('#message').value;

    socket.emit('message', { username, room, message });
});

socket.on('joined', (message) => {
    const messagesDiv = document.querySelector('#messages');
    messagesDiv.innerHTML += `<p>${message}</p>`;
});

socket.on('message', (data) => {
    const messagesDiv = document.querySelector('#messages');
    messagesDiv.innerHTML += `<p><strong>${data.username}:</strong> ${data.message}</p>`;
});

//Envio de imagenes
const fileInput = document.querySelector('#file');
const sendFileButton = document.querySelector('#sendFile');

sendFileButton.addEventListener('click', () => {
    const file = fileInput.files[0];
    const username = document.querySelector('#username').value;
    const room = document.querySelector('#room').value;

    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const imageData = event.target.result;

            socket.emit('image', { username, room, image: imageData });
        };
        reader.readAsDataURL(file);
    }
});

socket.on('image', (data) => {
    const messagesDiv = document.querySelector('#messages');
    const imageElement = document.createElement('img');
    imageElement.src = data.image;
    messagesDiv.appendChild(imageElement);
});

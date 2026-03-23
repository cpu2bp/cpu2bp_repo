const heading = document.querySelector('h1');
const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff'];
let colorIndex = 0;

setInterval(() => {
    if (heading) {
        heading.style.color = colors[colorIndex];
        colorIndex = (colorIndex + 1) % colors.length;
    }
}, 1000);

const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

let circle = {
    x: 120,
    y: 25,
    radius: 30,
    color: 'blue'
};

let isDragging = false;
let dragStartX, dragStartY;

function drawCircle() {
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.arc(circle.x, circle.y, circle.radius, 0, 2 * Math.PI);
    ctx.fillStyle = circle.color;
    ctx.fill();
    ctx.closePath();
}

if (canvas) {
    canvas.addEventListener('mousedown', (e) => {
        const mouseX = e.clientX - canvas.offsetLeft;
        const mouseY = e.clientY - canvas.offsetTop;

        const dx = mouseX - circle.x;
        const dy = mouseY - circle.y;
        if (dx * dx + dy * dy < circle.radius * circle.radius) {
            isDragging = true;
            dragStartX = mouseX - circle.x;
            dragStartY = mouseY - circle.y;
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const mouseX = e.clientX - canvas.offsetLeft;
            const mouseY = e.clientY - canvas.offsetTop;
            circle.x = mouseX - dragStartX;
            circle.y = mouseY - dragStartY;
            drawCircle();
        }
    });

    canvas.addEventListener('mouseup', () => {
        isDragging = false;
    });

    canvas.addEventListener('mouseout', () => {
        isDragging = false;
    });

    drawCircle();
}
// In your main.js file
async function fetchUserInfo() {
    // Replace with the actual local IP of your remote PC
    const remotePcIp = '10.76.190.65';
    try {
        const response = await fetch(`http://${remotePcIp}:5000/api/userinfo`);
        const data = await response.json();

        // Now you can display the data on your page
        const displayElement = document.createElement('p');
        if (data.username) {
            displayElement.textContent = `User on remote PC: ${data.username}`;
        } else {
            displayElement.textContent = 'No user logged into the remote PC.';
        }
        document.body.appendChild(displayElement);

    } catch (error) {
        console.error('Could not connect to the remote PC:', error);
        const errorElement = document.createElement('p');
        errorElement.textContent = 'Could not connect to the remote PC. Is the server running?';
        document.body.appendChild(errorElement);
    }
}

// Call the function when the page loads
fetchUserInfo();
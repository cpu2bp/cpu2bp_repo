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
    x: 500,
    y: 50,
    radius: 80,
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

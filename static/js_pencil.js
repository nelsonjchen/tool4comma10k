const PxBrush = window['px-brush'].default;

const canvas = document.getElementById('main-canvas');
const pxBrush = new PxBrush(canvas);

const ctx = canvas.getContext('2d');
let currentSize = 10;
let curZoom = 1;
let curClass = 0;

const classes = config.classes;
let currentCanvasState;

let mode = 'brush';

console.log(classes);

classes.forEach((col, i) => {
    console.log(col, i);
    $("#pencils1").append(
        `<div id='pencil-color-${col['id']}' data-class='pencil-${col['id']}' class='c-p-div btn-outline-secondary'><p class='c-p-text'>${col['name']}</p><div class='color-pencil' style='background:${col['color']}'></div></div>`
    );
});


$(".c-p-div").click((evt) => {
    console.log($(evt.target).data("class"));
    $(".c-p-div").css({"border": "none", "background": "#eee"});
    $(evt.target).css({"border": "1px #333 solid", "background": "#aaa"});
    curClass = parseInt($(evt.target).data("class").split('-')[1]);
});

function getMousePos(canvas, evt, zoom) {
    const rect = canvas.getBoundingClientRect();
    // console.log(evt.clientX, evt.clientY, rect, evt);
    return {
        x: (evt.clientX - rect.left) / zoom,
        y: (evt.clientY - rect.top) / zoom
        // x: evt.screenX - rect.left,
        // y: evt.screenY - rect.top
    };

}

// Start off with Nothing
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, canvas.width, canvas.height);

currentCanvasState = ctx.getImageData(0, 0, canvas.width, canvas.height);

// ON MOUSE DOWN

let isMouseDown = false;
let lastPosition = null;

let curDrawCommands = [];
let globalPaths = [];
let overlayImg = null;

function mousedown(canvas, evt) {
    if (mode === 'brush') {
        let currentPosition = getMousePos(canvas, evt, curZoom);
        isMouseDown = true;
        pxBrush.draw({
            from: currentPosition,
            to: currentPosition,
            size: currentSize,
            color: classes[curClass].color,
        });
        console.log("Reset Command Buffer");
        curDrawCommands = [
            {
                from: currentPosition,
                to: currentPosition,
            }
        ];
    } else if (mode === 'fill') {
        let currentPosition = getMousePos(canvas, evt, curZoom);
        ctx.fillStyle = classes[curClass].color;
        ctx.fillFlood(currentPosition.x, currentPosition.y, 10);

    }


}

// ON MOUSE MOVE

function mousemove(canvas, evt) {

    if (isMouseDown) {
        const currentPosition = getMousePos(canvas, evt, curZoom);
        if (lastPosition == null) {
            lastPosition = currentPosition;
        }

        pxBrush.draw({
            from: lastPosition,
            to: currentPosition,
            size: currentSize,
            color: classes[curClass].color,
        });
        curDrawCommands.push(
            {
                from: lastPosition,
                to: currentPosition,
            }
        );
        lastPosition = currentPosition;
    }
}

// ON MOUSE UP

function mouseup() {
    if (mode === 'brush') {
        isMouseDown = false;
        lastPosition = null;
        globalPaths.push(
            {
                draw_commands: curDrawCommands,
                className: curClass,
                color: classes[curClass].color,
                size: currentSize
            }
        );
        drawAllPaths();
    }
}

function drawAllPaths() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (overlayImg !== null) {
        ctx.drawImage(overlayImg, 0, 0);
    }
    globalPaths.forEach((pathObj) => {
        const draw_commands = pathObj.draw_commands;
        const color = pathObj.color;
        const size = pathObj.size;
        let draw_count = 0;
        draw_commands.forEach((draw_command) => {
            pxBrush.draw({
                from: draw_command.from,
                to: draw_command.to,
                size: size,
                color: color,
            });
            draw_count += 1;
        });
        console.log(`Drawn pxBrush ${draw_count} times`);
    });
    currentCanvasState = ctx.getImageData(0, 0, canvas.width, canvas.height);
    console.log(currentCanvasState);
}


canvas.addEventListener('mousedown', function () {
    mousedown(canvas, event);
});
canvas.addEventListener('mousemove', function () {
    mousemove(canvas, event);
});
canvas.addEventListener('mouseup', mouseup);


$('#undo').click(() => {
    globalPaths.pop();
    drawAllPaths();
});


$("#download").click((evt) => {
    window.requestAnimationFrame(drawAllPaths);
    console.log("Generating download");
    const image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
    const link = document.createElement('a');
    link.download = img_name;
    link.href = image;
    link.click();
});

$("#save_to_disk").click((evt) => {
    window.requestAnimationFrame(drawAllPaths);
    const image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
    const data = new FormData();

    $.post('/masks/' + img_name, {image: image}).done(function (data) {
    });
});

$("#load").click((evt) => {
    overlayImg = new Image();
    overlayImg.src = '/masks/' + img_name + '?' + Date.now();
    overlayImg.onload = drawAllPaths;
    overlayImg.onerror = function () {
        overlayImg = null;
    }
});

$('#clear').click(() => {
    overlayImg = null;
    globalPaths = [];
    drawAllPaths();
});

$(document).on('input', '#myRange', function () {
    // console.log($(this).val());
    currentSize = $(this).val();
    // console.log(currentSize);
    $("#brush-size").html(currentSize);
    $(".color-pencil").each(function (index) {
        $(this).css({"width": currentSize, "height": currentSize, "border-radius": currentSize / 2});
    });
});

$(document).on('input', '#myRangeOpacity', function () {

    $("#main-canvas").css({"opacity": $(this).val() / 10});
    $("#overlay-opacity").html($(this).val() / 10);
});


$(document).on('input', '#myRangeZoom', function () {
    curZoom = $(this).val();
    $("#overlay-zoom").html(curZoom);
    $("#main-canvas").css({"transform": "scale(" + curZoom + ")"});
    $("#main-img").css({"transform": "scale(" + curZoom + ")"});

    // currentSize = $("#myRange").val()/curZoom;
    // console.log(currentSize);
});


$('#previous').click(() => {
    window.location.href = '/pencil?id=' + (parseInt(img_id) - 1)
});

$('#next').click(() => {
    window.location.href = '/pencil?id=' + (parseInt(img_id) + 1)
});


$('#go-to-button').click(() => {
    const togoto = $('#go-to').val();
    window.location.href = '/pencil?id=' + togoto;
});

$('#brush').click((evt) => {
    mode = 'brush';
    $('.modes').removeClass("active");
    $(evt.target).addClass("active");

});

$('#fill').click((evt) => {
    mode = 'fill';
    $('.modes').removeClass("active");
    $(evt.target).addClass("active");
});


$('#commit').click(() => {

    $.ajax({
        url: "/hub-action/?imgfile=" + img_name,
        success: function (data) {
            console.log(data);
        },
    });


});

// KEYBOARD SHORTCUTS

document.addEventListener("keyup", function(event) {
    console.log(event)
    switch (event.key) {
        case "1":
            document.getElementById('pencil-color-0').click()
            break;
        case "2":
            document.getElementById('pencil-color-1').click()
            break;
        case "3":
            document.getElementById('pencil-color-2').click()
            break;
        case "4":
            document.getElementById('pencil-color-3').click()
            break;
        case "5":
            document.getElementById('pencil-color-4').click()
            break;
        case "6":
            document.getElementById('pencil-color-5').click()
            break;
        case "q":
            document.getElementById('myRange').value = 2;
            document.getElementById('myRange').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "w":
            document.getElementById('myRange').value = 4;
            document.getElementById('myRange').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "e":
            document.getElementById('myRange').value = 6;
            document.getElementById('myRange').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "r":
            document.getElementById('myRange').value = 10;
            document.getElementById('myRange').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "t":
            document.getElementById('myRange').value = 20;
            document.getElementById('myRange').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "a":
            document.getElementById('myRangeOpacity').value = 1;
            document.getElementById('myRangeOpacity').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "s":
            document.getElementById('myRangeOpacity').value = 2;
            document.getElementById('myRangeOpacity').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "d":
            document.getElementById('myRangeOpacity').value = 5;
            document.getElementById('myRangeOpacity').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "f":
            document.getElementById('myRangeOpacity').value = 7;
            document.getElementById('myRangeOpacity').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "z":
            document.getElementById('myRangeZoom').value = 0.00;
            document.getElementById('myRangeZoom').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "x":
            document.getElementById('myRangeZoom').value = 1.25;
            document.getElementById('myRangeZoom').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "c":
            document.getElementById('myRangeZoom').value = 2.00;
            document.getElementById('myRangeZoom').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "v":
            document.getElementById('myRangeZoom').value = 2.50;
            document.getElementById('myRangeZoom').dispatchEvent(
                new Event('input', {
                bubbles: true,
                cancelable: true,
            }));
            break;
        case "`":
            document.getElementById('load').click()
            break;
        case "Tab":
            document.getElementById('undo').click()
            break;
        default:
            console.log(`Pressed ${event}`)
    }
});

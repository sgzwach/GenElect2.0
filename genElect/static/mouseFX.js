let body;
let explodeDistance = 100;
let explodeSpeed = 30;
let explodeLag = 10;
let explodeClearLag = 100;
let explodeArms = 20;
let explodeChrapnelSize = 20;
let explodeChrapnelSizeFudge = 0;
let explodeCharacter = 'Jack';

let useRandomColor = true;
let color = "red";

let followClearLag = 300;

let mouseSVG = `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1000 1000" enable-background="new 0 0 1000 1000" xml:space="preserve">
<metadata> Svg Vector Icons : http://www.onlinewebfonts.com/icon </metadata>
<g><g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"><path d="M2225.1,5001.6c-118.8-32.6-208.8-91.9-304.5-195.4c-101.5-111.1-151.3-227.9-176.2-409.9c-11.5-93.9-17.2-1451.8-13.4-3775l5.7-3629.4l46-114.9c63.2-157.1,220.3-314.1,375.4-371.6c95.8-36.4,143.6-42.1,277.7-36.4c270.1,13.4,316,45.9,905.9,651.2c273.9,283.5,505.6,507.5,511.4,499.9c7.7-9.6,204.9-467.3,440.5-1018.9c419.5-986.4,429-1003.6,538.2-1120.4c206.8-222.2,498-310.3,773.8-233.7c93.8,24.9,940.4,381.1,1087.9,455.8c101.5,49.8,229.8,172.4,296.9,279.6c95.8,151.3,124.5,272,114.9,471.2l-9.6,174.3L6670.4-2376c-235.6,547.8-430.9,1005.5-436.7,1018.9c-7.6,17.2,166.6,24.9,754.6,28.7l762.3,5.7l128.3,61.3c214.5,101.5,339,262.4,383.1,499.9c26.8,143.6-13.4,327.5-99.6,463.5c-32.6,51.7-1174.1,1170.2-2689,2635.4C2552.6,5160.6,2732.6,5001.6,2454.9,5018.9C2368.7,5022.7,2276.8,5016.9,2225.1,5001.6z M2596.7,4262.3c84.3-82.4,1244.9-1202.8,2578-2489.9C6507.6,485.4,7614.7-587.1,7633.8-614c30.6-38.3,32.5-51.7,11.5-76.6c-21.1-24.9-139.8-28.7-965.3-30.6c-517.1,0-1017-7.7-1108.9-13.4c-174.3-13.4-204.9-30.6-204.9-109.2c0-21.1,254.7-633.9,565-1363.7c377.3-886.8,565-1348.3,565-1392.4c0-42.1-15.3-84.3-42.1-113c-51.7-55.5-978.7-453.9-1057.2-453.9c-111.1,0-134.1,46-720.2,1426.9c-308.3,727.8-568.8,1333-578.4,1346.4c-11.5,11.5-47.9,23-82.4,23c-55.5,0-130.2-72.8-815.9-775.7c-750.8-771.9-815.9-829.3-848.5-745.1c-21.1,51.7-13.4,7201.4,7.6,7255.1c9.6,26.8,32.6,49.8,49.8,49.8C2426.2,4413.6,2510.5,4346.6,2596.7,4262.3z"/></g></g>
</svg>`
document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("mousemove", (e) => { moveMouseFX(e) });
    document.body.addEventListener("click", (e) => { mouseClickFX(e) },false);
    body = document.querySelector("body");
});

function getRandomColor() {
    let r = Math.floor(Math.random() * 255);
    let g = Math.floor(Math.random() * 255);
    let b = Math.floor(Math.random() * 255);
    return `rgb(${r},${g},${b})`
}

function moveMouseFX(e) {
    mouseLeft = e.clientX;
    mouseTop = e.clientY;
    let cursorDiv = document.createElement("div");
    cursorDiv.innerHTML = mouseSVG;
    cursorDiv.classList.add("cursor");
    cursorDiv.style.left = mouseLeft;
    cursorDiv.style.top = mouseTop;
    let path = cursorDiv.querySelector("path");
    if(useRandomColor)
        path.style = `fill: ${getRandomColor()}`;
    else
        path.style = `fill: ${color}`;
    body.appendChild(cursorDiv);
    setTimeout(()=>{body.removeChild(cursorDiv)},followClearLag);
}

function updateExplodeNode(x,y,dx,dy,i){
    if(i < explodeDistance){
        let div = document.createElement("div");
        div.innerHTML = explodeCharacter;
        let rand = Math.floor(Math.random()*explodeChrapnelSizeFudge) - explodeChrapnelSizeFudge/2;
        div.classList.add("explodeNode");
        if(useRandomColor)
            div.style = `color: ${getRandomColor()};font-size:${explodeChrapnelSize + rand}px;`;
        else
            div.style = `color: ${color};font-size:${explodeChrapnelSize + rand}px;`;
        div.style.left = x + dx;
        div.style.top = y + dy;
        body.appendChild(div);
        setTimeout(()=>{body.removeChild(div);},explodeClearLag);
        setTimeout(()=>{updateExplodeNode(x+dx,y+dy,dx,dy,i+1)},explodeLag);
    }
}

function mouseClickFX(e){
    mouseLeft = e.clientX;
    mouseTop = e.clientY;
    for(let i = 0; i < explodeArms; i++){
        let dx = Math.random()*explodeSpeed - explodeSpeed/2;
        let dy = Math.random()*explodeSpeed - explodeSpeed/2;
        setTimeout(()=>{updateExplodeNode(mouseLeft,mouseTop,dx,dy,0)},explodeLag);
    }
}
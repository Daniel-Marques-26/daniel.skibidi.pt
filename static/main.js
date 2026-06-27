import kaplay from "https://unpkg.com/kaplay@3001.0.19/dist/kaplay.mjs";

kaplay({
    scale: 2,
    background: [100, 100, 100]
});

const socket = io("http://192.168.1.190:3000");

const otherPlayers = {}

const player = add([
    sprite("player"),
    pos(200, 200),
    scale(2),
    area(),
    "player"
])

socket.on("connect", () => {
    socket.emit("nick", "Dan_Tuff")
})

socket.on("currentPlayers", (players) => {
    for (const id in players) {

        console.log(players[id])

        otherPlayers[id] = add([
            sprite("player"),
            anchor("center"),
            scale(2),
            area(),
            pos(players[id].x, players[id].y),
            color(Math.floor(Math.random() * 255 + 1), Math.floor(Math.random() * 255 + 1), Math.floor(Math.random() * 255 + 1))
        ])
        console.log(otherPlayers[id])

        otherPlayers[id].add([
            text(players[id].nick, {size: 7}),
            anchor("center"),
            pos(0, -12)
        ])
    }
});

socket.on("newPlayer", (p) => {
    console.log(p)
    otherPlayers[p.id] = add([
        sprite("player"),
        scale(2),
        area(),
        pos(p.x, p.y),
        color(Math.floor(Math.random() * 255 + 1), Math.floor(Math.random() * 255 + 1), Math.floor(Math.random() * 255 + 1))
    ])


})

socket.on("playerMoved", (p) => {
    if (otherPlayers[p.id]) {
        otherPlayers[p.id].pos = vec2(p.x, p.y);
    }
})

socket.on("playerLeft", (inf) => {
    if (otherPlayers[inf]) {
        destroy(otherPlayers[inf])
        delete otherPlayers[inf]
    }
})

function moving() {
    socket.emit("move", {
        x: player.pos.x,
        y: player.pos.y
    })
}

function shoot() {
    socket.emit("shoot", {
        id: socket.id,
        player: player.pos,
        mouse: mousePos()
    })
}

function tp() {
    let r = Math.floor(Math.random() * Object.keys(otherPlayers).length)
    let key = Object.keys(otherPlayers)[r]
    player.pos = vec2(otherPlayers[key].pos.x + Math.floor(Math.random() * 31 - 15), otherPlayers[key].pos.y + Math.floor(Math.random() * 31 - 15))
    moving()
}

loadSprite("player", "/static/Sprites/Sprite-player.png");
loadSprite("block", "/statics/Sprites/Sprite-block.png");
loadSprite("heart", "/static/Sprites/Sprite-heart.png");
loadSprite("bullet", "/static/Sprites/Sprite-bullet.png");

onKeyDown("right", () => {
    player.move(200, 0)
    moving()
})

onKeyDown("left", () => {
    player.move(-200, 0)
    moving()
})

onKeyDown("up", () => {
    player.move(0, -200)
    moving()
})

onKeyDown("down", () => {
    player.move(0, 200)
    moving()
})

onKeyPress("t", () => {
    tp()
})

onKeyPress("f", () => {
    shoot()
})

let surrouding = false

onKeyPress("s", () => {
    surrouding = true
})


onUpdate(() => {
    if (player.pos.x <= 0)
    {
        player.pos.x = 0;
    }

    if (player.pos.x + player.width*player.scale.x >= width())
    {
        player.pos.x = width() - player.width*player.scale.x;
    }

    if (player.pos.y <= 0)
    {
        player.pos.y = 0;
    }

    if (player.pos.y + player.height*player.scale.y >= height())
    {
        player.pos.y = height() - player.height*player.scale.y;
    }

    if (surrouding)
    {
        let r_player = Math.floor(Math.random() * otherPlayers.lenght);
        player.pos = otherPlayers[r_player].pos
    }
})
import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js';


class Player {
    constructor(scene, player) {
        this.id = player.id;
        this.name = player.name;

        this.color = player.color;

        this.position = player.position;

        this.velocityVector = player.velocityVector;

        this.velocity = player.velocity;

        this.inventory = player.inventory;

        this.mesh = new THREE.BoxGeometry(1,1,1);
        this.material = new THREE.MeshBasicMaterial({ color: this.color });
        this.cube = new THREE.Mesh(this.mesh, this.material);
        this.cube.position.set(this.position.x, this.position.y, this.position.z);

        scene.add(this.cube);
    }

    set_position(position) {
        this.position = position;
    }

    update_position() {
        this.cube.position.set(this.position.x, this.position.y, this.position.z);
    }
    
    get_position() {
        return this.position; 
    }

    set_velocityVec_x(x) { this.velocityVector.x += x; }
    set_velocityVec_y(y) { this.velocityVector.y += y; }
    set_velocityVec_z(z) { this.velocityVector.z += z; }
}

class PlayerSelf extends Player {
    constructor(scene, camera, player) {
        super(scene, player);

        this.camera = camera;

        this.cam_offsetY = 10;
        this.cam_offsetZ = 10;
    }

    set_position(position) {
        this.position = position;
    }

    update_position() {
        this.cube.position.set(this.position.x, this.position.y, this.position.z);
        this.camera.position.set(this.position.x, this.position.y + this.cam_offsetY, this.position.z + this.cam_offsetZ);
        this.camera.lookAt(this.position.x, this.position.y, this.position.z);
    }

    move() {
        socket.emit('move', { id: this.id, direction: { x: this.velocityVector.x, y: this.velocityVector.y, z: this.velocityVector.z } });
    }

    get_camera_position() {
        return this.camera.position;
    }
}


const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 70);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('canvas')
});

renderer.setSize(window.innerWidth, window.innerHeight);

window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});

let world = {}

let players = {}
let player = null;

const socket = io();

/// INIT WORLD AND PLAYER
socket.on('init_world', (world_data) => {

    world = world_data.world;

    console.log("World data:", world);

    generate_world(scene, world);
});

socket.on('player_connected_you', (player_data) => {
    console.log(player_data);
    console.log("Player position:", player_data.position);

    if (player_data.position === undefined) {
        return;
    } else {
        
        player = new PlayerSelf(scene, camera, player_data);
        run = true;
    }
});
////////////////////////

socket.on('player_update', (data) => {
    //response time
    response_time = Date.now() - time_2_response;
    //
    player.set_position(data.position);
});

socket.on('other_player_update', (data) => {
    for (const player_ of Object.keys(data)) {
        if (player_ !== player.id) {
            if (players[player_]) { // If player exists
                players[player_].set_position(data[player_].position);
            } else {
                players[player_] = new Player(scene, data[player_]);
            }
        }
    }
});

//
let run = false;

// FPS

let time = Date.now();
let fps = 0;
let fps_low = 1000;

// Response Time

let time_2_response = Date.now();
let response_time = 0;

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
    
    console.log("Socket ",socket.connected)
    console.log("Player",player)

    if (socket.connected) {  // Check if player is not null
        console.log("Player position: ", player.get_position());

        player.move();
        time_2_response = Date.now();  // Response time

        player.update_position();
        update_map(world, player);

        // FPS
        let deltaTime = Date.now() - time;
        let new_fps = 1000 / deltaTime;

        if (new_fps < fps_low && new_fps > 4) {
            fps_low = new_fps;
        }

        fps = new_fps;
        time = Date.now();

        document.getElementById('fps').innerText = `FPS: ${fps.toFixed(2)} | FPS Low: ${fps_low.toFixed(2)} | Response Time: ${response_time}ms`;
    }
}


animate();



/// movement controls

document.addEventListener('keydown', (event) => {
    if (!player) return;  // Check if player is null

    if (event.key === 'w') {
        player.set_velocityVec_z(-1);
    }
    if (event.key === 's') {
        player.set_velocityVec_z(1);
    }
    if (event.key === 'a') {
        player.set_velocityVec_x(-1);
    }
    if (event.key === 'd') {
        player.set_velocityVec_x(1);
    }

    console.log("Velocity Vector: ", player.velocityVector);
});

document.addEventListener('keyup', (event) => {
    if (!player) return;  // Check if player is null

    if (event.key === 'w' || event.key === 's') {
        player.set_velocityVec_z(0);
    }
    if (event.key === 'a' || event.key === 'd') {
        player.set_velocityVec_x(0);
    }
});


function update_map(world, player) {
    const map = document.getElementById('map');
    map.innerHTML = ''; // Leert die Map für eine frische Darstellung

    const world_size = 225;

    // Skalierungsfaktor der Karte basierend auf der Weltgröße und der Kartengröße
    const scale_factor = map.offsetWidth / world_size;

    // Spieler auf der Karte darstellen
    const player_dot = document.createElement('div');
    player_dot.classList.add('player-dot');
    player_dot.style.left = (player.position.x * scale_factor) + 'px';
    player_dot.style.top = (player.position.z * scale_factor) + 'px';
    map.appendChild(player_dot);

    // Andere Spieler auf der Karte darstellen
    Object.keys(players).forEach(player_ => {
        const other_player_dot = document.createElement('div');
        other_player_dot.classList.add('other-player-dot');
        other_player_dot.style.left = (players[player_].position.x * scale_factor) + 'px';
        other_player_dot.style.top = (players[player_].position.z * scale_factor) + 'px';
        map.appendChild(other_player_dot);
    });

    // Bäume auf der Karte darstellen
    world.trees.forEach(tree => {
        const tree_dot = document.createElement('div');
        tree_dot.classList.add('tree-dot');
        tree_dot.style.left = (tree.position.x * scale_factor) + 'px';
        tree_dot.style.top = (tree.position.z * scale_factor) + 'px';
        map.appendChild(tree_dot);
    });

    // Steine auf der Karte darstellen
    world.rocks.forEach(rock => {
        const rock_dot = document.createElement('div');
        rock_dot.classList.add('rock-dot');
        rock_dot.style.left = (rock.position.x * scale_factor) + 'px';
        rock_dot.style.top = (rock.position.z * scale_factor) + 'px';
        map.appendChild(rock_dot);
    });
}



//// world_generator.js
function generate_world(scene, world) {

    const world_size = world.size;

    const geometry = new THREE.PlaneGeometry(1000, 1000);
    
    const material = new THREE.MeshBasicMaterial({ color: 0x3b4929, side: THREE.DoubleSide });

    const plane = new THREE.Mesh(geometry, material);
    plane.rotation.x = -Math.PI / 2;
    scene.add(plane);

    for (const tree of world.trees) {
        const tree_mesh = make_tree(tree);
        scene.add(tree_mesh);
    }

    for (const rock of world.rocks) {
        const rock_mesh = make_rock(rock);
        scene.add(rock_mesh);
    }
    
}


//// tree_generator.js
function make_tree(tree_) {
    const { x, y, z } = tree_.position;
    const height = tree_.height;

    const tree = new THREE.Group();

    const trunk_geometry = new THREE.CylinderGeometry(2, 2, height);
    const trunk_material = new THREE.MeshBasicMaterial({ color: 0x8B4513 });
    const trunk = new THREE.Mesh(trunk_geometry, trunk_material);
    tree.add(trunk);

    let color_leaves = 0x00ff00;

    let leaves_geometry = new THREE.SphereGeometry(8);

    if (tree_.type === 'oak') {
        color_leaves = 0x00ff00;
        leaves_geometry = new THREE.SphereGeometry(8);
    } else if (tree_.type === 'pine') {
        color_leaves = 0x069460;
        leaves_geometry = new THREE.ConeGeometry(8, 16, 8);
    } else if (tree_.type === 'birch') {
        color_leaves = 0x8fa277;
        leaves_geometry = new THREE.SphereGeometry(8);
    }

    const leaves_material = new THREE.MeshBasicMaterial({ color: color_leaves });
    const leaves = new THREE.Mesh(leaves_geometry, leaves_material);
    leaves.position.y = height / 2 + 8;
    tree.add(leaves);

    tree.position.set(x, y, z);  // Set tree position
    return tree;
}

function make_rock(rock_) {
    const { x, y, z } = rock_.position;

    const rock = new THREE.Group();

    const rock_geometry = new THREE.SphereGeometry(4);
    const rock_material = new THREE.MeshBasicMaterial({ color: 0x696969 });
    const rock_mesh = new THREE.Mesh(rock_geometry, rock_material);
    rock.add(rock_mesh);

    rock.position.set(x, y, z);  // Set rock position
    return rock;
}
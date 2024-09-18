import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js';
import { Player, PlayerSelf } from './player.js';
import { generate_world } from './world_generator.js';
import { update_map } from './map_utils.js'; // If you have separate file for update_map function

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

socket.on('adamah', (data) => {
    world = data;
    generate_world(scene, world);
});

socket.on('adameva', (player_data) => {
    console.log(player_data);
    console.log("Player data:", player_data.position);

    if (player_data.position === undefined) {
        return;
    } else {
        player = new PlayerSelf(scene, camera, player_data);
        run = true;
    }
});

socket.on('player_update', (data) => {
    response_time = Date.now() - time_2_response;
    player.set_position(data.position);
});

socket.on('other_player_update', (data) => {
    for (const player_ of Object.keys(data)) {
        if (player_ !== player.id) {
            if (players[player_]) { 
                players[player_].set_position(data[player_].position);
            } else {
                players[player_] = new Player(scene, data[player_]);
            }
        }
    }
});

let run = false;
let time = Date.now();
let fps = 0;
let fps_low = 1000;
let time_2_response = Date.now();
let response_time = 0;

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);

    if (socket.connected && player) {  
        player.move();
        time_2_response = Date.now();  

        player.update_position();
        update_map(world, player);

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

document.addEventListener('keydown', (event) => {
    if (!player) return;

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
});

document.addEventListener('keyup', (event) => {
    if (!player) return;

    if (event.key === 'w' || event.key === 's') {
        player.set_velocityVec_z(0);
    }
    if (event.key === 'a' || event.key === 'd') {
        player.set_velocityVec_x(0);
    }
});

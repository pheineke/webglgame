import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js';


class Player {
    constructor(scene, player) {
        this.id = player.id;
        this.name = player.name;

        this.color = player.color;

        this.position = player.position;

        this.velocity = player.velocity;

        this.inventory = player.inventory;

        this.mesh = new THREE.BoxGeometry(1,1,1);
        this.material = new THREE.MeshBasicMaterial({ color: this.color });
        this.cube = new THREE.Mesh(this.mesh, this.material);
        this.cube.position.set(this.position.x, this.position.y, this.position.z);

        scene.add(this.cube);

    }

    set_position(position) {

        const { x, y, z } = this.position;

        this.position = position;

        this.cube.position.set(this.position.x, this.position.y, this.position.z);
    }
    
    get_position() {
        return this.position; 
    }
}

class PlayerSelf extends Player {
    constructor(scene, camera, player) {
        super(scene, player);

        this.camera = camera;
    }

    set_position(position) {
        const cam_offsetY = 10;
        const cam_offsetZ = 10;

        const { x, y, z } = this.position;

        this.position = position;

        this.cube.position.set(this.position.x, this.position.y, this.position.z);

        this.camera.position.set(this.position.x, this.position.y + cam_offsetY, this.position.z + cam_offsetZ);
        this.camera.lookAt(this.position.x, this.position.y, this.position.z);

    }

    move(vectorX, vectorY, vectorZ) {
        socket.emit('move', { id: this.id, direction: { vectorX: vectorX, vectorY: vectorY, vectorZ: vectorZ } });
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
socket.on('adamah', (data) => {
    console.log('adamah:', data);
    world = data;

    generate_world(scene, world);
});

socket.on('adameva', (data) => {
    console.log('adameva:', data);
    console.log('data:', data);
    player = new PlayerSelf(scene, camera, data);
    console.log('Player:', player);

});
////////////////////////

socket.on('player_update', (data) => {
    console.log('player_update:', data);
    player.set_position(data.position);
});

socket.on('other_player_update', (data) => {
    console.log('other_player_update:', data);

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

function animate() {
    requestAnimationFrame(animate);

    renderer.render(scene, camera);
}

animate();



/// movement controls

document.addEventListener('keydown', (event) => {
    let vectorX = 0;
    let vectorZ = 0;

    if (event.key === 'w') {
        vectorZ -= 1;
    }
    if (event.key === 's') {
        vectorZ += 1;
    }
    if (event.key === 'a') {
        vectorX -= 1;
    }
    if (event.key === 'd') {
        vectorX += 1;
    }

    player.move(vectorX, 0, vectorZ);

    console.log('Camera position:', player.get_camera_position());
});




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

    const trunk_geometry = new THREE.CylinderGeometry(0.5, 0.5, height);
    const trunk_material = new THREE.MeshBasicMaterial({ color: 0x8B4513 });
    const trunk = new THREE.Mesh(trunk_geometry, trunk_material);
    tree.add(trunk);

    let color_leaves = 0x00ff00;

    let leaves_geometry = new THREE.SphereGeometry(2);

    if (tree_.type === 'oak') {
        color_leaves = 0x00ff00;
        leaves_geometry = new THREE.SphereGeometry(2);
    } else if (tree_.type === 'pine') {
        color_leaves = 0x069460;
        leaves_geometry = new THREE.ConeGeometry(2, 4);
    } else if (tree_.type === 'birch') {
        color_leaves = 0x8fa277;
        leaves_geometry = new THREE.SphereGeometry(2);
    }

    const leaves_material = new THREE.MeshBasicMaterial({ color: color_leaves });
    const leaves = new THREE.Mesh(leaves_geometry, leaves_material);
    leaves.position.y = 3;
    tree.add(leaves);

    tree.position.set(x, y, z);  // Set tree position
    return tree;
}

function make_rock(rock_) {
    const { x, y, z } = rock_.position;

    const rock = new THREE.Group();

    const rock_geometry = new THREE.SphereGeometry(2);
    const rock_material = new THREE.MeshBasicMaterial({ color: 0x696969 });
    const rock_mesh = new THREE.Mesh(rock_geometry, rock_material);
    rock.add(rock_mesh);

    rock.position.set(x, y, z);  // Set rock position
    return rock;
}
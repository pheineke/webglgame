import { make_tree, make_rock } from './tree_generator.js';

export function generate_world(scene, world) {
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

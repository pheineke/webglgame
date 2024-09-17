import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js';

function make_tree(tree) {
    const { x, y, z } = tree_.position;

    const tree = new THREE.Group();

    const trunk_geometry = new THREE.CylinderGeometry(0.5, 0.5, 5);
    const trunk_material = new THREE.MeshBasicMaterial({ color: 0x8B4513 });
    const trunk = new THREE.Mesh(trunk_geometry, trunk_material);
    tree.add(trunk);

    let color_leaves = 0x00ff00;

    const leaves_geometry = new THREE.SphereGeometry(2);

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

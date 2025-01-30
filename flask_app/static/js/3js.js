import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// シーン、カメラ、レンダラーの初期化
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// ライトの設定
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(1, 1, 1).normalize();
scene.add(light);

// GLTFモデルをロード
const loader = new GLTFLoader();
loader.load(
    './path_to_your_model/model.glb', // モデルファイルのパス
    (gltf) => {
        const model = gltf.scene;
        scene.add(model);

        // モデルをアニメーションさせる例
        model.rotation.y = Math.PI / 2;

        // アニメーションループ
        function animate() {
            requestAnimationFrame(animate);
            model.rotation.y += 0.01; // 回転を追加
            renderer.render(scene, camera);
        }

        animate();
    },
    undefined,
    (error) => {
        console.error('An error occurred:', error);
    }
);

// カメラ位置を設定
camera.position.z = 5;

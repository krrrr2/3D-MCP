// hahaliu1029/house-3d 의 장면(같은 평면도를 GPT-6 / Fable 이 각각 만든 three.js 앱)을 GLB 로 내보낸다.
// 앱 코드의 빌더 함수를 그대로 호출하고, 형상만 필요하므로 텍스처는 버린다(가짜 캔버스).
//
// 사용: node export_house3d.mjs <house-3d 경로> <fable|gpt6> <french|italian|modern|song> <out.glb>
// 준비: 각 앱 폴더에 three 만 설치하면 된다
//   (cd house-3d/fable && npm install three@0.185.1 --no-save --registry=https://registry.npmjs.org)
//   (cd house-3d/gpt6  && npm install three@0.180.0 --no-save --registry=https://registry.npmjs.org)
//   package-lock 은 중국 미러(registry.npmmirror.com)를 가리키므로 npm ci 대신 위처럼 설치.
import './stubs.mjs';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [root, app, style = 'modern', out] = process.argv.slice(2);
if (!root || !['fable', 'gpt6'].includes(app) || !out) {
  console.error('usage: node export_house3d.mjs <house-3d> <fable|gpt6> <style> <out.glb>');
  process.exit(2);
}
const appDir = resolve(root, app);
const load = (p) => import(pathToFileURL(resolve(appDir, p)).href);
// 앱이 쓰는 것과 같은 three 인스턴스 (심볼릭 링크도 실제 경로로 합쳐짐)
const THREE = await load('node_modules/three/build/three.module.js');
const { GLTFExporter } = await load('node_modules/three/examples/jsm/exporters/GLTFExporter.js');
const { GLTFLoader } = await load('node_modules/three/examples/jsm/loaders/GLTFLoader.js');
GLTFLoader.prototype.loadAsync = async function (url) {           // 가구 GLB 를 fetch 대신 파일에서
  const b = readFileSync(resolve(appDir, 'public', String(url).replace(/^.*?models\//, 'models/')));
  return this.parseAsync(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength), '');
};

const scene = new THREE.Group();
scene.name = 'export';
if (app === 'fable') {
  const { makeMaterials } = await load('src/materials.js');
  const { buildHouse } = await load('src/house.js');
  const { buildFurnishings } = await load('src/furnishings.js');
  const { STYLES } = await load('src/styles.js');
  const { OPENINGS } = await load('src/plan.js');
  const M = makeMaterials();
  const built = buildHouse(M, STYLES[style]);
  built.ceilings.visible = true;
  // 앱 데이터의 열림부 종류(door/window/arch)를 role 로 넘김 → glTF extras → Blender 커스텀 속성 obj["role"]
  const byId = Object.fromEntries(OPENINGS.map((o) => [o.id, o.type]));
  for (const g of built.openings.children) {
    const t = byId[g.name.replace(/^opening-/, '')];
    if (t) g.userData.role = t === 'arch' ? 'trim' : t;
  }
  scene.add(built.house, await buildFurnishings(M, STYLES[style]));
} else {
  // GPT-6 판은 이름(중국어)만으로 역할을 알 수 있어 role 을 따로 넣지 않는다
  const { createMaterials } = await load('src/materials.js');
  const { buildArchitecture } = await load('src/architecture.js');
  const { buildFurniture } = await load('src/furniture.js');
  const { mats } = createMaterials(style);
  for (const [name, m] of Object.entries(mats)) m.name ||= name;
  const arch = buildArchitecture(THREE, mats, style);
  arch.setCeiling(true);
  arch.setCutaway(false);
  scene.add(arch.group, buildFurniture(THREE, mats, style).group);
}
let meshes = 0;
scene.traverse((o) => {
  if (!o.isMesh) return;
  meshes++;
  const name = Array.isArray(o.material) ? o.material.map((m) => m?.name || '').join('+') : (o.material?.name || '');
  o.material = new THREE.MeshStandardMaterial({ name });           // 재질 이름만 남김 (유리 판정용)
});
const glb = await new GLTFExporter().parseAsync(scene, { binary: true, onlyVisible: true });
writeFileSync(out, Buffer.from(glb));
console.log(`exported ${app}/${style}: ${meshes} meshes → ${out}`);

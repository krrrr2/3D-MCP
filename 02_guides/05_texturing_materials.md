# 텍스처링·재질 가이드: AI + MCP로 PBR 재질 제대로 만들기

> 기준일: 2026-09-27 · 재질은 AI에게 "만들게" 하기 전에 "고르게" 하세요. CC0 스캔 라이브러리 → 검증된 절차 레시피 → AI 메시 텍스처링(PBR 켜고 조명 제거) 순서로 쓰고, PBR 수치 규칙을 프롬프트에 박아 두고, 게임·glTF로 보낼 때는 반드시 베이크합니다.

## 핵심 요약

- **소싱 순서가 품질을 정합니다.** ① Poly Haven·ambientCG 같은 CC0 스캔 라이브러리 → ② Infinigen·Substance Designer 레시피 같은 검증된 절차 재질 → ③ 형상 고유 디테일이 필요할 때만 AI 메시 텍스처링. NVIDIA Material Agent도 VLM(비전-언어 모델)이 렌더를 보고 **라이브러리에서 고르는** 방식을 기본으로 씁니다.
- **PBR 규칙은 숫자로 줘야 지켜집니다.** Metallic은 0 또는 1, 금속 Base Color는 밝게(실측값 대부분 linear 0.5~1.0), 비금속 albedo는 조명·그림자 없이 linear 0.02(숯)~0.85(눈), Roughness는 0 금지(0.02 이상), 컬러 맵만 sRGB. LLM은 "반짝이는 금속 = metallic 0.7" 같은 값을 자주 씁니다.
- **ahujasid MCP for Blender(구 blender-mcp)의 Poly Haven 연동은 2026-09-21 이전 버전에 버그가 있었습니다.** normal/displacement 맵을 받아 놓고 연결하지 않는 경로가 있었고, Mapping 노드가 TEXTURE 모드라 타일링이 뒤집혔습니다(2m 텍스처가 4m 면에서 1.993회가 아니라 0.509회 반복). Poly Haven의 Greg Zaal이 [PR #367](https://github.com/ahujasid/blender-mcp/pull/367)로 고쳤습니다. 최신 버전을 쓰고, 도구가 "성공"을 반환해도 연결 상태를 스크립트로 확인하세요(3.2절).
- **절차 셰이더는 검증된 레시피를 따라 하게 하세요.** Infinigen(BSD-3) 소스는 수치가 구체적인 좋은 참고서지만 metallic 0.37 같은 비물리 값이 섞여 있고, Blender 4.1에서 제거된 Musgrave 노드도 씁니다. 이 문서의 대리석·나무·브러시드 메탈·패브릭·엣지 마모 코드는 **Blender 4.2.23 LTS와 5.0.1**(pip `bpy`, 헤드리스)에서 동작을 확인했습니다.
- **웨더링 마스크는 렌더러를 탑니다.** Pointiness와 Bevel 노드는 Cycles 전용입니다(EEVEE에서 pointiness는 상수 0.5, bevel은 효과 없음). AO 노드는 EEVEE에서도 돌지만 화면 공간 방식입니다. EEVEE·게임엔진·glTF가 목표면 Cycles로 구워야 합니다.
- **절차 재질을 그대로 GLB로 내보내면 거의 다 사라집니다.** 이 문서 테스트에서 대리석 절차 재질은 GLB에 `metallicFactor: 0`과 `KHR_materials_specular`만 남았습니다(색·거칠기·요철 소실). 베이크 → ORM(R=AO, G=Roughness, B=Metallic) 팩킹 → AO는 `glTF Material Output` 노드 그룹의 `Occlusion` 입력으로 연결하세요. 활성 이미지 노드가 없는 재질 슬롯은 **오류 없이 건너뜁니다**.
- **AI 텍스처 생성의 3대 실패**는 albedo에 구워진 조명, 뷰 간 불일치·이음새, 이미지 모델이 지어낸 노멀·러프니스 맵입니다. Meshy는 `enable_pbr=true`를 명시해야 하고(기본 false), PBR 맵은 텍스처 해상도 설정과 무관하게 2K입니다. 데이터 맵은 이미지 모델에게 그리게 하지 말고 전용 추정기나 베이크로 만드세요.
- **[한국 사용자] Tencent Hunyuan3D(2.0/2.1, Paint 포함) 라이선스는 한국·EU·영국을 적용 지역에서 빼고 출력물 사용도 제한합니다.** 한국에서 로컬로 쓰면 라이선스 범위 밖입니다. "MIT·Apache라서 안전"에도 단서가 붙습니다. TRELLIS.2는 비상업 nvdiffrast에 의존하고, Step1X-3D 텍스처 모듈에는 Hunyuan 라이선스 헤더가 남은 코드가 있고, Material Anything은 비상업 Text2Tex 설정을 쓰고, PartUV의 PartField 전처리는 비상업입니다. CHORD는 연구 전용입니다.
- **텍스처 전용 MCP**: Substance 3D Painter MCP(커뮤니티, 도구 79개), Substance Designer MCP(레시피 79개), RTX Remix Toolkit 내장 공식 MCP, ComfyUI 공식 `comfy-mcp`, Meshy 공식 MCP가 쓸 만합니다. Adobe 공식 Substance MCP, BlenderKit·Megascans 공식 MCP는 없습니다.
- **"AAA급"은 도구 하나로 나오지 않습니다.** 독립적으로 검증된 AI+MCP의 AAA 재질 결과물은 찾지 못했습니다. 현실적인 경로는 [라이브러리·생성 + 에이전트 조립 + Cycles 렌더 비평 루프 + 사람의 마무리(특히 Painter 스마트 마스크 웨더링)]입니다.

---

## 1. 전체 작업 흐름

```text
[스펙]   부위별 재질 목록 (예: 좌판=화이트오크 오일 마감, 다리=브러시드 스틸, 쿠션=울 패브릭)
  ↓
[소싱]   ① CC0 스캔 라이브러리 검색 → 없으면 ② 절차 레시피 → 형상 고유 디테일이면 ③ AI 메시 텍스처링
  ↓
[규칙 감사] PBR 수치·컬러스페이스 자동 검사 (4.7절 audit_materials)
  ↓
[시각 검증] 중립 조명 + 회색 배경 Cycles 렌더 → VLM이 레퍼런스와 비교 → 수정 (후보 N개 중 선택)
  ↓
[웨더링] 베이스 + 개체별 변화 + 마모 + 오염
  ↓
[UV·텍셀 밀도] 씬 전체에서 통일
  ↓
[베이크] BaseColor / Roughness / Metallic / Normal / AO → ORM 팩킹
  ↓
[내보내기] glTF·FBX → "만든 맵 vs 파일에 실제로 들어간 슬롯" 감사
```

| 상황 | 1순위 | 2순위 | 피할 것 |
|---|---|---|---|
| 바닥·벽·돌·금속판처럼 반복되는 재질 | Poly Haven·ambientCG 스캔 텍스처 (`set_texture`) | Substance Designer MCP 레시피, 절차 레시피 → 베이크 | 이미지 모델에게 PBR 맵 4장을 각각 그리게 하기 |
| 가구(부위마다 재질이 다름) | 부위 분류 → 부위별 라이브러리 재질 할당 | 절차 레시피(나무·패브릭·금속) | AI 재텍스처 한 번으로 끝내기 |
| 형상 고유 무늬(도자기 그림, 조각상 파티나, 라벨) | AI 메시 텍스처링(PBR·조명 제거) → 베이크 | 트림 시트 + 데칼 | 조명이 구워진 albedo를 그대로 사용 |
| 게임 에셋 웨더링 | Substance Painter MCP 스마트 머티리얼·마스크 | Blender Cycles 마스크 → 베이크 | EEVEE 스크린샷만 보고 마모 값 조정 |
| 구형 게임 텍스처 리마스터 | PBRify + RTX Remix(내장 MCP) | — | — |
| 레퍼런스 사진을 편집 가능한 재질로 | Designer MCP 레시피 조정, 후보-비교 루프(4.8절) | VLMaterial(연구용, 데이터 비상업) | 노드 그래프를 한 번에 생성하고 끝내기 |

---

## 2. AI에게 줘야 할 PBR 규칙 (수치)

### 2.1 규칙표

| 항목 | 규칙 | 수치 | 이유·근거 |
|---|---|---|---|
| Metallic | 0 또는 1만. 중간값은 칠 벗겨진 경계 같은 전환부와 안티앨리어싱 픽셀에만 | {0, 1} | 중간 metallic은 현실에 없는 재질이라 뿌옇고 싸 보임. 커뮤니티 스킬 [cc-blender-skill](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-materials/SKILL.md)의 표현으로는 "Metallic is a switch, not a slider" |
| 금속 Base Color | 밝게. "어두운 금속"은 대부분 roughness나 오염 문제 | 실측 linear: 은 0.991, 알루미늄 0.916, 스테인리스 (0.669, 0.639, 0.598), 크롬 0.654, 철 0.53. 예외: 티타늄 0.441 | [physicallybased.info materials.json](https://raw.githubusercontent.com/AntonPalmqvist/physically-based-api/main/deploy/v2/materials.json)(CC0). 흔히 인용되는 가이드 기준 "sRGB 180~255(≈linear 0.46 이상)"는 원문 미확인 |
| 비금속 albedo | 조명·그림자·하이라이트 없음 | linear 0.02(숯)~0.85(눈). 콘크리트 0.51, 흰 달걀껍질 0.61 | physicallybased.info. "sRGB 50~240(엄격)/30~240(허용)" 가이드는 원문 미확인 |
| Roughness | 정확히 0은 쓰지 않음 | 0.02 이상(크롬 0.02, 광택 금 0.05는 cc-blender-skill 값) | DB의 roughness 0은 연마면 기준값. 실제 에셋은 미세한 변화가 있어야 CG 티가 덜 남 |
| Specular(비금속) | 기본값 유지 | IOR 1.5, Specular IOR Level 0.5(=IOR 그대로, 반사율 약 4%) | [Principled BSDF 소스](https://raw.githubusercontent.com/blender/blender/main/source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc) |
| 컬러스페이스 | Base Color·Emission 이미지만 sRGB. roughness·metallic·normal·height·AO·ORM은 Non-Color | `'Non-Color'` → 없으면 `'Linear Rec.709'` → `'Linear'` 순서로 시도 | 데이터 맵을 sRGB로 읽으면 노멀이 휘고 roughness가 밝아짐(너무 매트). [ahujasid addon.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py)도 같은 규칙 |
| 노멀맵 | Image(Non-Color) → Normal Map 노드(Tangent Space) → Principled `Normal` | Blender·glTF는 OpenGL 규약(Y+, Poly Haven `nor_gl`). DirectX(`nor_dx`, Y−) 맵은 G 채널 반전 | 잘못 고르면 음각·양각이 뒤집힘. glTF는 Tangent Space만 지원([glTF-Blender-IO 문서](https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst)) |
| Displacement | 오프라인 렌더용. 게임·glTF로는 나가지 않음 | 게임용이면 normal로 베이크 | 8장 |
| 재질 개수 | 재질 하나에 Material Output 1개, Principled 1개 | — | 중복되면 뷰포트는 맞는데 렌더가 회색이 되는 비결정적 셰이딩([#190](https://github.com/ahujasid/blender-mcp/issues/190)) |

### 2.2 실측 기준값 (physicallybased.info, CC0)

에이전트가 색을 "추측"하지 않게 이 값을 프롬프트나 도구 결과로 넣으세요. API는 `https://api.physicallybased.info/v2`, 저장소는 [AntonPalmqvist/physically-based-api](https://github.com/AntonPalmqvist/physically-based-api)입니다(v2 materials.json, 재질 116종, 2026-09 검증 시점 기준).

- 값은 **linear sRGB**입니다. Blender의 RGB 입력 칸도 linear라서 그대로 넣으면 됩니다. Hex 칸은 sRGB이니 섞어 쓰지 마세요.
- DB의 roughness는 대표값입니다(금속 0은 연마면 기준). 제작할 때는 2.1절 규칙대로 조정하세요.

| 분류 | 재질 | Base Color (linear) | Metallic | Roughness(DB) | 비고 |
|---|---|---|---|---|---|
| 금속 | 은 Silver | (0.991, 0.985, 0.974) | 1 | 0 | |
| 금속 | 알루미늄 Aluminum | (0.916, 0.923, 0.924) | 1 | 0 | |
| 금속 | 구리 Copper | (0.932, 0.623, 0.522) | 1 | 0 | |
| 금속 | 황동 Brass | (0.91, 0.778, 0.423) | 1 | 0 | |
| 금속 | 금 Gold | (1.059, 0.773, 0.307) | 1 | 0 | R이 1을 넘음. 텍스처에는 1로 잘라 넣기 |
| 금속 | 크롬 Chromium | (0.654, 0.685, 0.701) | 1 | 0 | |
| 금속 | 스테인리스 Stainless Steel | (0.669, 0.639, 0.598) | 1 | 0 | 이 문서 브러시드 메탈 기본값 |
| 금속 | 철 Iron | (0.53, 0.513, 0.494) | 1 | 0 | |
| 금속 | 아연 Zinc | (0.808, 0.844, 0.865) | 1 | 0 | 아연도금 |
| 금속 | 티타늄 Titanium | (0.441, 0.4, 0.361) | 1 | 0 | 금속 중 어두운 편 |
| 건축 | 콘크리트 Concrete | (0.51, 0.51, 0.51) | 0 | 0.5 | |
| 건축 | 벽돌 Brick | (0.262, 0.095, 0.061) | 0 | 1.0 | |
| 건축 | 아스팔트(새것) | (0.0429, 0.0414, 0.0401) | 0 | 0.5 | |
| 건축 | 테라코타 Terracotta | (0.555, 0.212, 0.11) | 0 | 1.0 | |
| 건축 | 녹 Rust | (0.181, 0.057, 0.017) | 0 | 1.0 | 녹은 **비금속**. 녹슨 부위는 Metallic 0 |
| 소품 | 대리석 Marble | (0.83, 0.791, 0.753) | 0 | 0 | SSS 데이터 있음 |
| 소품 | 도자기 Porcelain | (0.745, 0.745, 0.723) | 0 | 0 | |
| 소품 | 사무용지 Office Paper | (0.794, 0.834, 0.884) | 0 | 0.8 | |
| 소품 | 골판지 Cardboard | (0.351, 0.208, 0.11) | 0 | 0.5 | |
| 소품 | 타이어 Tire | (0.023, 0.023, 0.023) | 0 | 0.7 | |
| 소품 | 칠판 Blackboard / 화이트보드 | 0.039 / (0.869, 0.867, 0.771) | 0 | 0.9 / 0 | |
| 기준 | 그레이카드 Gray Card | (0.18, 0.18, 0.18) | 0 | 0.9 | 노출 기준 |
| 극단 | 숯 Charcoal / 눈 Snow | 0.02 / 0.85 | 0 | 1.0 / 0.5 | 비금속 albedo 범위의 양 끝 |
| 투명 | 소다석회 유리 / 아크릴 / PC | 약 1.0 | 0 | 0 | IOR 1.52 / 1.4905 / 1.5848, transmission 1 |
| 액체 | 물 Water | (0.969, 0.996, 0.997) | 0 | 0 | IOR 1.3325 |

나무와 패브릭은 이 DB에 없습니다. 4장의 레시피 값을 출발점으로 쓰고 레퍼런스 사진과 렌더를 비교해 맞추세요.

### 2.3 커뮤니티 스킬 레시피 값 (cc-blender-skill, 교차검증 필요)

[RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill)(현재 v1.3.0, Claude Code 스킬 **30종**)의 `blender-materials` 스킬 값입니다. 검증 에이전트가 원문과 일치함을 확인했지만, 스킬 자체는 작성자가 자체 검증만 한 커뮤니티 자료입니다. 특히 금속 기준 "≥0.5 sRGB"는 linear로 약 0.21이라 2.1절 기준보다 느슨하니 그대로 쓰지 마세요.

| 재질 | 값 |
|---|---|
| 브러시드 스틸 | Base (0.56, 0.57, 0.58), Metallic 1, Roughness 0.25 |
| 광택 금 | Base (1.022, 0.782, 0.344), Roughness 0.05 |
| 크롬 | Roughness 0.02 |
| 간유리(Frosted) | Transmission 1, IOR 1.5, Roughness 0.3 |
| 짙은 녹색 와인병 | Volume Absorption (0.05, 0.32, 0.10), Density 80 |
| 옅은 색 유리병(Pale tinted vial) | (0.10, 0.45, 0.18), Density 15. 스킬의 유리병 코드 예시는 같은 색에 Density 30 |
| 유리 공통 | Light Paths의 transmission bounces 16 이상 |
| 래커 플라스틱 | Coat Weight 0.8, Coat Roughness 0.05 |
| 피부 | Subsurface Weight 1, Radius (1, 0.2, 0.1) |
| 벨벳 | Sheen Weight 0.5 |
| 나무 | Wave(Scale 5, Distortion 4) + Noise(Scale 8) → ColorRamp (0.15, 0.07, 0.03)~(0.6, 0.35, 0.18) |

> 이전 조사 요약의 "스킬 10종", "녹색 유리병 (0.10, 0.45, 0.18) Density 80"은 검증에서 틀린 것으로 확인돼 위처럼 바로잡았습니다.

### 2.4 복사해서 쓰는 규칙 블록

프로젝트의 `CLAUDE.md`·`AGENTS.md`([템플릿](../03_playbooks/templates/CLAUDE.md))나 시스템 프롬프트에 그대로 넣으세요.

```text
## 재질 규칙 (PBR)
- 재질 하나 = Material Output 1개 + Principled BSDF 1개. 재질 코드는 항상 노드를 비우고 다시 만든다(반복 실행해도 같은 결과).
- Metallic은 0 또는 1. 칠 벗겨짐 같은 전환부만 마스크로 섞는다.
- Base Color는 physicallybased.info 값(linear)을 쓴다. 예: Concrete 0.51, Aluminum 0.916, Copper (0.932,0.623,0.522), Stainless (0.669,0.639,0.598).
  금속 Base Color는 밝게(대부분 0.5 이상). 비금속 albedo는 0.02~0.85, 조명·그림자·하이라이트를 넣지 않는다.
- Roughness는 0 금지, 최소 0.02. 한 재질 안에서도 결·마모·얼룩으로 변화를 준다.
- 이미지 컬러스페이스: Base Color·Emission만 sRGB, 나머지는 Non-Color.
- 노멀맵은 Normal Map 노드(Tangent) 경유. Poly Haven은 nor_gl을 쓴다.
- 노드·소켓 이름은 추측하지 말고 describe_node_type / bpy_api_lookup으로 먼저 조회한다(4.0 이후 이름: Specular IOR Level, Coat Weight, Transmission Weight, Emission Color, Sheen Weight, Subsurface Weight).
- 노드는 이름이 아니라 type으로 찾는다(한국어 UI에서 이름이 번역될 수 있음). Musgrave Texture는 없다(4.1 제거) → Noise Texture의 noise_type.
- 라이브러리 재질(Poly Haven set_texture)을 먼저 시도하고, 노드를 손으로 짜는 것은 그다음이다.
- 작업이 끝나면 재질별 Base Color/Metallic/Roughness 표를 출력하고 audit_materials()를 돌려 위반을 스스로 고친다.
- 검증 렌더는 Cycles로 한다(EEVEE에서는 Pointiness·Bevel 마스크가 안 보인다). 변경 전후 스크린샷을 비교한다.
- 게임·glTF로 내보내기 전에는 반드시 베이크하고, 내보낸 파일의 재질 슬롯을 감사한다.
```

### 2.5 재질 코드에서 LLM이 틀리는 Blender 버전 함정

전체 목록은 [Blender MCP 가이드 11절](02_blender_mcp.md)에 있습니다. 재질과 관련된 것만 추렸습니다. "테스트"는 이 문서 작성 중 pip `bpy` 4.2.23 LTS·5.0.1로 직접 확인한 것입니다.

| 버전 | 틀리는 코드 | 올바른 코드 | 근거 |
|---|---|---|---|
| 4.0 | `inputs['Specular']`, `'Clearcoat'`, `'Transmission'`, `'Emission'`, `'Sheen'`, `'Subsurface'` | `'Specular IOR Level'`, `'Coat Weight'`, `'Transmission Weight'`, `'Emission Color'`, `'Sheen Weight'`, `'Subsurface Weight'` | 소스·테스트 |
| 4.1 | `nodes.new('ShaderNodeTexMusgrave')` | `ShaderNodeTexNoise` + `noise_type`(`FBM`, `MULTIFRACTAL`, `RIDGED_MULTIFRACTAL`, `HYBRID_MULTIFRACTAL`, `HETERO_TERRAIN`) | 4.2·5.0 모두 "Node type ShaderNodeTexMusgrave undefined"(테스트). [v4.0.0 소스에는 존재](https://raw.githubusercontent.com/blender/blender/v4.0.0/source/blender/nodes/shader/nodes/node_shader_tex_musgrave.cc), [v4.1.0 versioning](https://raw.githubusercontent.com/blender/blender/v4.1.0/source/blender/blenloader/intern/versioning_400.cc)에 변환 함수 |
| 5.0 | 4.2 소켓 목록을 그대로 가정 | 5.0 Principled에는 `Diffuse Roughness` 입력이 추가됨(4.2에는 없음) | 테스트 |
| 5.0 | `mat.use_nodes = True`를 무조건 호출 | `if mat.node_tree is None: mat.use_nodes = True` (5.0에서 폐기 예고) | [Blender MCP 가이드](02_blender_mcp.md) |
| 4.2 | `uv.unwrap(method='MINIMUM_STRETCH')` | 4.2 LTS에는 없음(`ANGLE_BASED`, `CONFORMAL`만). 5.0.1에는 있음 | 테스트 |
| 공통 | `nodes['Principled BSDF']` | `next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')` | 한국어 등 현지화 UI에서 새 노드 이름이 번역될 수 있음([Blender MCP 가이드 12절](02_blender_mcp.md)) |

**Musgrave → Noise 변환 요령**: 이미 저장된 .blend는 4.1이 열 때 자동으로 Noise로 바뀌므로, 깨지는 것은 `ShaderNodeTexMusgrave`를 **새로 만드는** 스크립트와 애드온입니다. `musgrave_type`은 같은 이름의 `noise_type`으로, `musgrave_dimensions`는 `noise_dimensions`로 옮기고, `Dimension` 입력 자리는 `Roughness`를 씁니다(값이 1:1로 대응한다고 가정하지 말고 렌더로 확인). Infinigen main 브랜치의 `table_marble.py`·`wood.py`도 아직 `Nodes.MusgraveTexture`를 참조합니다.

---

## 3. 재질 소싱: 어디서 가져오나

### 3.1 라이브러리와 MCP 경로

| 소스 | 규모 | 라이선스 | MCP 경로 (2026-09) | 주의 |
|---|---|---|---|---|
| [Poly Haven](https://github.com/Poly-Haven/Public-API) | 에셋 약 2,400개(텍스처 약 860개), 1k~8k, 실측 크기 메타데이터 | CC0. API 무료(개인·상업) | ahujasid MCP for Blender 내장 도구 6개(`get_polyhaven_categories`, `search_polyhaven_assets`, `get_polyhaven_asset_preview`, `download_polyhaven_asset`, `set_texture`, `get_polyhaven_status`) | 다운로드가 Blender 메인 스레드에서 돌아 고해상도는 멈춤(해상도 한 단계마다 용량 약 4배). 텍스처 860개 중 114개는 매핑 테이블에 없는 맵을 참조 |
| ambientCG | Poly Haven에 없는 재질(포장재·타일 등) 보완 | CC0 | [dcc-asset-ambientcg](https://github.com/dcc-mcp/dcc-asset-ambientcg)(`search_ambientcg_assets`, `list_ambientcg_downloads`, `download_ambientcg_asset`) **(미검증: 별 0~1개, 일괄 생성된 조직)** | API 명세 원문 미확인 |
| [BlenderKit](https://github.com/BlenderKit/BlenderKit) | 무료 모델 1만+, 머티리얼 1만, HDRI 1천+ / Full Plan 모델 2.7만+ | 무료 + 구독 | 전용 MCP 없음(GitHub 검색 0건). `execute_blender_code`로 애드온 오퍼레이터 호출은 비공식 | 절차 재질이 많아 내보내기 전 베이크 필요 |
| Quixel Megascans / Fab | — | Fab 라이선스([에셋·라이선스 가이드](10_assets_pipeline_licensing.md)) | 공식 MCP 없음. [Quartermaster](https://github.com/Tanshaydar/Quartermaster)(MIT, 별 2개)가 **이미 보유한** Fab/Megascans 카탈로그를 텍셀 밀도·맵 목록까지 로컬 인덱싱해 MCP로 검색. [dcc-mcp-epic](https://github.com/dcc-mcp/dcc-mcp-epic)은 Fab 쪽만, 로그인·구매·라이선스 수락은 자동화하지 않음 | 조사 요약의 "dcc-mcp-epic이 Megascans 미지원을 명시"는 원문에 없는 표현(검증에서 정정) |
| physicallybased.info | 대표값 116종 | CC0 | API/JSON을 프롬프트나 도구 결과로 | 텍스처가 아니라 값 |
| 사내 라이브러리 | — | — | NVIDIA Material Agent처럼 `materials.yaml` 목록에서 VLM이 고르게(3.4절) | 가장 일관된 룩 |

### 3.2 Poly Haven via MCP: 과거 버그와 수정 (PR #367)

**무엇이 잘못됐나** — Poly Haven 운영자 Greg Zaal이 2026-09-14에 [issue #361](https://github.com/ahujasid/blender-mcp/issues/361)로 버그 6개를 보고했고, 2026-09-21 병합된 [PR #367](https://github.com/ahujasid/blender-mcp/pull/367)로 고쳤습니다(Blender 5.2.1에서 E2E 테스트, 테스트 248개 추가).

| 문제 (수정 전) | 결과 | 수정 (PR #367) |
|---|---|---|
| 맵 이름 매칭이 `normal`을 찾는데 API 이름은 `nor_gl`/`nor_dx` | normal·displacement를 받아 놓고 연결하지 않음 → 요철 없는 평면 | Poly Haven 자체 머티리얼 구조를 참조하는 단일 매핑 테이블 |
| Mapping 노드가 `TEXTURE` 모드 | 스케일이 역수로 적용. 2m 텍스처가 4m 면에서 1.993회가 아니라 **0.509회** 반복 | `POINT` 모드 (glTF `KHR_texture_transform`의 권장 타입도 Point) |
| 모든 맵을 다운로드 | 1k 텍스처 하나에 7.4MB(필요량 1.9MB) | 필요한 맵만. 860개 1k 텍스처 기준 4,150MB → 2,100MB(49% 감소) |
| 검색 결과를 관련도가 아니라 slug 순으로 20개에서 자름 | 엉뚱한 텍스처 선택 | 검색 개선 |
| HDRI를 패킹하지 않음 | 파일을 옮기면 HDRI 누락 | 패킹 |
| 모델을 변환 포맷으로 import | 머티리얼 노드 그룹 손실 | `.blend` 원본으로 import해 노드 그룹 보존 |

- **정확히 말하면**(검증 결과): 연결 누락은 "다운로드하면서 머티리얼을 만드는" 경로의 버그였고, `set_texture` 경로에는 `'nor_gl'`을 `'gl'`로 잘못 파싱하는 별도 버그가 있었습니다. blender-kiln이 수정 전 `set_texture`로 측정했을 때는 normal이 GLB에 남았으므로 "모든 경로에서 항상 평평했다"는 표현은 과장입니다.
- 저장소 이름은 현재 `ahujasid/mcp-for-blender`로 바뀌었고(약 29.4k stars, MIT), PyPI 최신은 `mcp-for-blender` 2.1.0(2026-09-25)입니다. 2.1.0은 병합 이후 배포판이지만 릴리스 노트로 수정 포함 여부를 직접 확인하지는 못했습니다. `uvx blender-mcp`는 호환 래퍼로 여전히 이 커뮤니티 서버를 실행합니다.
- 설치·보안 설정(`DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1`은 샌드박스가 아님, 포트 9876 충돌)은 [Blender MCP 가이드](02_blender_mcp.md)와 [빠른 시작](../03_playbooks/01_quickstart_setup.md)을 보세요.

**권장 호출 순서** (인자 이름은 버전마다 다를 수 있으니 도구 스키마를 먼저 확인)

```text
get_polyhaven_status
→ search_polyhaven_assets(asset_type="textures", 키워드 "oak floor")
→ get_polyhaven_asset_preview 로 후보 3개 비교 (VLM이 레퍼런스와 대조)
→ download_polyhaven_asset(해상도 "1k" 또는 "2k"; 카메라 가까운 히어로 에셋만 "4k")
→ set_texture(대상 오브젝트)            ← 노드를 손으로 짜지 말 것
→ 아래 점검 스니펫 실행 → get_viewport_screenshot 으로 반복 패턴·스케일 확인
```

**타일 크기 맞추기**: `POINT` 모드에서 Mapping Scale = 표면 크기 ÷ 텍스처 실측 크기입니다(UV가 면 전체를 0~1로 덮는다고 가정). 바닥 6m에 2m짜리 텍스처면 Scale 3입니다. 수정판은 실측 크기 메타데이터(`polyhaven_scale_mm`)를 저장합니다(저장 위치는 버전별로 확인). UV가 실측 비율이 아니면 6.3절 텍셀 밀도 방식으로 맞추세요.

**연결 상태 점검 스니펫** (`execute_blender_code`로 실행. 4.2·5.0 테스트)

```python
import bpy
obj = bpy.data.objects["Floor"]   # 대상 오브젝트 이름
for slot in obj.material_slots:
    nt = slot.material.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    linked = {s.name: s.is_linked for s in bsdf.inputs if s.name in ("Base Color", "Roughness", "Metallic", "Normal")}
    maps = [n.vector_type for n in nt.nodes if n.type == "MAPPING"]            # 'POINT'이어야 정상
    cs = {n.image.name: n.image.colorspace_settings.name for n in nt.nodes if n.type == "TEX_IMAGE" and n.image}
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output)
    print(slot.material.name, linked, "Mapping:", maps, cs, "Displacement 연결:", out.inputs["Displacement"].is_linked)
```

`Normal`이 `False`이거나 Mapping이 `TEXTURE`이면 구버전 동작입니다. 컬러스페이스는 `Diffuse`만 sRGB여야 합니다.

### 3.3 Poly Haven API 이용 조건

[ToS 원문(master 브랜치)](https://raw.githubusercontent.com/Poly-Haven/Public-API/master/ToS.md) 기준입니다.

- API는 개인·상업 모두 무료입니다. 에셋은 CC0라서 귀속 표시가 필요 없습니다.
- **live API를 쓰는 소프트웨어**는 가벼운 크레딧 표기("Powered by Poly Haven" 수준)를 요청받습니다(2.5절).
- 요청에는 소프트웨어 이름과 일치하는 **고유한 Referer 또는 User-Agent**를 붙입니다(2.4절). 버전 번호가 꼭 들어갈 필요는 없습니다.
- API 저장소 코드는 AGPL-3.0입니다(에셋 라이선스와 별개).

### 3.4 '생성보다 선택' 패턴: 부위를 나누고 라이브러리에서 고르기

**NVIDIA usd-content-agents Material Agent** ([저장소](https://github.com/NVIDIA-Omniverse/usd-content-agents), [Material Agent README](https://raw.githubusercontent.com/NVIDIA-Omniverse/usd-content-agents/main/apps/material_agent/README.md), Apache-2.0, 2026, Beta, Linux/WSL2 전용)
- VLM(NIM/OpenAI/Anthropic/Gemini)이 렌더 뷰를 보고 MDL·UsdPreviewSurface·OpenPBR 라이브러리(`materials.yaml`)에서 부위별 재질을 **고릅니다**.
- 10단계: USD 최적화 → 프리뷰 렌더 → 레퍼런스 이미지 → 부위별 렌더 데이터셋 → 기술 문서에서 재질 정보 추출 → VLM 예측 → 이름 검증·수리 → 반복 인스턴스 조화 → 적용 → 최종 비교 렌더.
- 설계 원칙: **시각 증거가 우선이고, 기술 문서 텍스트는 VLM 판단을 보조할 뿐 뒤집지 못합니다.** 에이전트 하네스는 Codex SDK(기본) 또는 Claude Agent SDK입니다.
- [Texture Agent](https://raw.githubusercontent.com/NVIDIA-Omniverse/usd-content-agents/main/apps/texture_agent/README.md)(Research Preview)는 UV 준비 상태를 먼저 검사(`uv_report.json`)한 뒤 albedo·roughness·metalness·normal을 생성합니다. "UV 검사 → 생성" 순서를 그대로 따라 하세요.

**Blender에서 흉내 내기**: 면 노멀과 높이로 부위를 나눈 뒤 부위별로 라이브러리를 검색합니다. blender-kiln의 분류 규칙 **(미검증 주장, 신뢰도 낮은 출처)**: `abs(n.z) > 0.7`이면서 위쪽 절반 → 좌판·상판, `abs(n.z) < 0.3`이면서 아래 1/4 → 다리, 수직이면서 위쪽 → 등받이. 부위를 처음부터 별도 오브젝트·재질 슬롯으로 모델링하는 편이 더 확실합니다([모델링 가이드](07_modeling_objects_furniture_sculpture.md)).

```text
프롬프트 예: "의자를 부위별로 나눠라(좌판·다리·등받이·쿠션). 부위마다 Poly Haven에서 후보 3개를 검색해 프리뷰를
레퍼런스 사진과 비교하고 가장 가까운 것을 set_texture로 적용하라. 후보가 없으면 그 부위만 절차 레시피를 쓴다.
선택 이유를 부위별 한 줄로 남기고, Cycles 렌더 전후를 비교하라."
```

---

## 4. 절차적 셰이더 레시피 (Blender 4.2 LTS·5.0 테스트)

### 4.1 공통 규칙

1. **idempotent 리셋**: 재질 코드는 항상 `nodes.clear()` → Output 1개(`is_active_output=True`) + Principled 1개로 시작합니다. 같은 스크립트를 두 번 돌려도 노드가 쌓이지 않아야 합니다([#190](https://github.com/ahujasid/blender-mcp/issues/190) 사례).
2. **이름 대신 type·소켓**: 노드는 `n.type`으로 찾고, 소켓은 `inputs["이름"]`으로만 접근합니다(인덱스 접근 금지. 단 Mix 노드처럼 같은 이름 소켓이 여러 개인 노드는 예외적으로 인덱스).
3. **Musgrave 금지**: Noise Texture의 `noise_type`을 씁니다(2.5절).
4. **비물리 값 교정**: Infinigen은 연구용 랜덤화 때문에 `edge_wear`의 마모 금속층 Metallic 0.3745, 긁힘 광택층 0.3855 같은 값을 씁니다. 가져올 때 Metallic을 0/1 마스크로 다시 짭니다.
5. **좌표계**: 가구처럼 UV가 불확실하면 `Texture Coordinate > Object`(미터 단위)를 쓰고, 패브릭처럼 직조 방향이 UV를 따라야 하면 UV를 씁니다. 베이크하려면 어차피 UV가 필요합니다.

### 4.2 원본 레시피 요약 (출처 수치)

| 재질 | 핵심 구성 | 원본 수치 | 출처 |
|---|---|---|---|
| 대리석 | Object 좌표 → Noise(4D)로 왜곡 → Noise로 2차 왜곡 → Voronoi `DISTANCE_TO_EDGE` → 아주 좁은 ColorRamp로 맥 | Noise Scale 3(4D, Detail 15) → Noise Scale 8(Detail 15) → Voronoi 4D Scale 3, W 1.64 → ColorRamp 0.0 흰색 → 0.03 검정. 맥 강약 Noise Scale 4 → Map Range 0.48~0.6. 바탕 ColorRamp 0.3~0.9. Roughness 0.1, Specular IOR Level 0.6, Displacement Scale 0.02 | [Infinigen table_marble.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/table_marble.py) |
| 나무 | 결 방향으로 좌표를 크게 늘림 + 연륜 + 결 | Mapping Scale (5, 100, 100)과 (0.15, 1, 0.15). Roughness `uniform(0, 0.4)` + 노이즈로 최대 +0.8. Coat Weight `clip(uniform(0, 1.4), 0, 1)`. **Musgrave 사용 → 변환 필요** | [Infinigen wood.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wood/wood.py) |
| 브러시드 메탈 | 한 축을 압축한 Noise 2개를 DARKEN → Map Range로 roughness | Mapping (0.2, 0.2, 5)와 (1, 1, 20)(저주파 노이즈로 20% 왜곡). Noise Scale = 100 × scale, Detail 15, Roughness 0.4 / 0.6, Distortion 0.1. Map Range 0.4~0.6 → Roughness 0.2~0.3, 명도 0.8~1.2. Metallic 1, Specular IOR Level 0 | [Infinigen brushed_metal.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/metal/brushed_metal.py) |
| 소파 패브릭 | UV 기반 Brick 텍스처로 미세 직조 + Sheen | Brick Scale 276.98, Mortar Size 0.01, Mortar Smooth 1, Bias 0.5, Row Height 0.1, offset 0.5479. Roughness 0.8624, Sheen Weight 1.0. Displacement(Height=Brick Fac) Scale 0.005~0.01 | [Infinigen sofa_fabric.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/fabric/sofa_fabric.py) |
| 엣지 마모 | Bevel 노멀 − 기하 노멀 → 마스크 × 노이즈 | Bevel samples 20, Radius 0.005~0.01(칠 벗겨짐) / 0.01~0.03(긁힘). ColorRamp 0.069 → 0.156. 마스크 노이즈 Scale 2.5~3, Detail 1 | [Infinigen edge_wear.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wear_tear/edge_wear.py) |
| 긁힘 | 한 축을 25배 늘린 Noise | Mapping (25, 1, 1), Noise Scale 5~80, Detail 15, Roughness 0, Distortion 22.8. 마스크 Noise Scale 5~40 → ColorRamp 0.41. 얕은 변위 | [Infinigen scratches.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wear_tear/scratches.py) |

Infinigen([저장소](https://github.com/princeton-vl/infinigen), BSD-3, 일부 CC-0)에는 이 밖에도 ceramic, fabric(velvet, leather 등), metal(galvanized, hammered 등), wood 14종, tiles가 있고, `node_transpiler`로 노드를 코드로 바꿀 수 있습니다. **LLM에게 "해당 파일의 노드 구성과 수치를 참고해 bpy로 재현하라"고 시키면 환각보다 훨씬 안정적입니다.**

### 4.3 대리석

- **핵심**: "노이즈 하나 대리석"은 구름처럼 보입니다. Voronoi 엣지 거리 + 0.03 이하의 좁은 램프를 써야 가늘고 날카로운 맥이 나옵니다.
- **이 문서의 튜닝 관찰** (Cycles 테스트 렌더, 개인 테스트, n=1):
  - Infinigen 원본 값(2차 왜곡 Noise Scale 8, Detail 15)은 1m 판에서 잘게 부서진 **잔금** 느낌입니다.
  - 2차 왜곡을 Scale 2, Detail 3으로 낮추면 굵고 흐르는 **주맥**이 됩니다.
  - 좌표를 한 축으로 늘리면(Mapping Scale (0.35, 1, 1)) 셀 모양 윤곽이 줄고 맥이 한 방향으로 흐릅니다.
  - 그래서 코드(4.7절)는 주맥(굵게) + Infinigen 원본 잔맥(35% 세기) 두 층으로 구성했습니다. 맥 밀도는 `vein_scale`(2~4)로 조절합니다.
- 바탕 색은 physicallybased 대리석 (0.83, 0.791, 0.753), Roughness 0.1(광택 연마), 맥 부분은 +0.05.

### 4.4 나무

- **핵심**: 등방성 노이즈는 나무가 아니라 얼룩처럼 보입니다. **결 방향 스트레치**와 **코트층**이 "가구다운" 느낌을 만듭니다.
- **이 문서 테스트에서 확인한 것** (개인 테스트, n=1): Infinigen의 Mapping (5, 100, 100)을 Noise로 그대로 옮기면 무늬가 너무 잘아서 1m 판에서 거의 단색이 됩니다. Wave Texture를 `RINGS` + `rings_direction='X'`로 쓰고 **링 축을 판재 면에 대해 몇 도 기울이면**(Rotation Y 약 6°, Location Z 약 0.2) 판재 윗면에 산 모양(cathedral) 무늬가 나타납니다. 결 방향으로 50배 늘린 Noise(Mapping X 0.02)를 곱하면 기공·결이 생깁니다.
- 색은 어두운 결 (0.20, 0.10, 0.045) ~ 밝은 결 (0.55, 0.33, 0.17)(cc-blender-skill 값 근처에서 조정), Roughness 0.40~0.55(어두운 결이 더 거칠게), Coat Weight는 오일 마감 0.1~0.3 / 래커 0.5~1.0, Coat Roughness 0.05.
- 결 방향은 오브젝트 로컬 X축입니다. 다리·상판처럼 결 방향이 다른 부품은 오브젝트를 회전하거나 Mapping Rotation을 바꾸세요.

### 4.5 브러시드 메탈

- **핵심**: 금속의 사실감은 roughness의 **방향성 변동**에서 나옵니다. 단색 roughness는 CG처럼 보입니다.
- Infinigen 구성을 그대로 옮겼습니다. 결 방향은 Mapping Scale (0.2, 0.2, 5)가 정합니다(Z를 압축 → 결이 XY 평면을 따라 늘어남). 방향을 바꾸려면 압축 축을 바꿉니다.
- Noise Scale이 `100 × scale`이라는 점이 중요합니다. 오브젝트 좌표(미터) 기준으로 약 1cm보다 가는 결이 나옵니다. 작은 소품이면 scale을 올리세요.
- Base Color는 스테인리스 실측값 (0.669, 0.639, 0.598), Metallic 1, Roughness 0.2~0.3.

### 4.6 패브릭·벨벳

- **핵심**: 패브릭은 **미세 직조 + Sheen**이 사실감을 결정합니다.
- 소파 패브릭은 UV 좌표 위 Brick Texture(Scale 276.98)를 직조 패턴으로 쓰고, 같은 값을 Displacement(재질 기본 설정인 Bump Only에서 범프로 동작) Scale 0.005~0.01로 줍니다. **UV가 있어야** 하고, UV 스케일이 제각각이면 직조 크기도 제각각이 됩니다(6.3절).
- Roughness 0.86, Sheen Weight 1.0. 벨벳은 cc-blender-skill 값 Sheen Weight 0.5부터 시작합니다.
- 패브릭은 스캔 텍스처(Poly Haven·ambientCG)가 절차 재질보다 나은 경우가 많습니다. 절차 패브릭은 "먼 거리용"으로 생각하세요.

### 4.7 코드 (테스트 완료)

아래 세 파일은 이 문서 작성 중 **pip `bpy` 4.2.23 LTS와 5.0.1**에서 다음을 확인한 코드입니다: 다섯 재질 생성, 같은 이름으로 다시 만들어도 Principled·Output이 1개씩만 남음(idempotent), Cycles 렌더, 베이크(7장), ORM 팩킹, glTF 내보내기 후 슬롯 확인(8장), 규칙 위반 감지. 노드를 이름이 아니라 type과 소켓으로만 다루므로 한국어 UI에서도 안전합니다.

**사용법**: 파일로 저장해 `sys.path`에 추가하고 import하거나(MCP의 `execute_blender_code`는 호출마다 새 네임스페이스), 헤드리스로 `blender -b scene.blend --python build.py`처럼 실행합니다. `BLENDER_MCP_SAFE_MODE=1`은 `open()`·`os` 같은 직접 파일 I/O, 프로세스, 네트워크를 막습니다(bpy 오퍼레이터를 통한 .blend 저장·열기, import/export, 렌더는 허용). `sys.path`에 추가한 모듈을 import할 수 있는지는 확인하지 못했으니, 막히면 내용을 붙여 넣으세요([보조 스크립트 README](../03_playbooks/scripts/README.md)와 같은 방식). `pbr_bake.py`는 `os.makedirs`를 쓰므로 safe mode에서는 헤드리스(7.4절)로 돌리세요.

<details>
<summary><b>pbr_recipes.py</b> — 공통 헬퍼 + 대리석·브러시드 메탈·나무·소파 패브릭·엣지 마모 도장 금속 (약 210줄)</summary>

```python
# pbr_recipes.py — Blender 4.2 LTS / 5.0 에서 테스트. 노드는 이름이 아니라 type·소켓으로만 다룸(한국어 UI 안전)
import bpy

def new_clean_material(name):
    """같은 이름의 재질을 Output 1개 + Principled 1개 상태로 초기화(idempotent)."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if mat.node_tree is None:        # 4.x 호환. 5.0+는 노드 트리가 기본(use_nodes 폐기 예고)
        mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.is_active_output = True
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat, nt, bsdf, out

def ramp(nt, fac_socket, stops):
    """ColorRamp. stops = [(pos, (r,g,b)), ...] 2개 이상"""
    r = nt.nodes.new("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    while len(els) < len(stops):
        els.new(0.5)
    for el, (pos, rgb) in zip(els, stops):
        el.position = pos
        el.color = (*rgb, 1.0)
    nt.links.new(fac_socket, r.inputs["Fac"])
    return r

def noise(nt, vec, scale, detail=15.0, rough=0.5, distortion=0.0, dims="3D", ntype="FBM", w=0.0):
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.noise_dimensions = dims
    n.noise_type = ntype          # 4.1+ (Musgrave 대체): FBM / MULTIFRACTAL / RIDGED_MULTIFRACTAL / HYBRID_MULTIFRACTAL / HETERO_TERRAIN
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    n.inputs["Distortion"].default_value = distortion
    if dims == "4D":
        n.inputs["W"].default_value = w
    if vec is not None:
        nt.links.new(vec, n.inputs["Vector"])
    return n

def map_range(nt, val, a, b, c, d):
    m = nt.nodes.new("ShaderNodeMapRange")
    m.inputs["From Min"].default_value = a; m.inputs["From Max"].default_value = b
    m.inputs["To Min"].default_value = c;   m.inputs["To Max"].default_value = d
    nt.links.new(val, m.inputs["Value"])
    return m

def _set_or_link(nt, sock, v):
    if isinstance(v, (int, float)): sock.default_value = v
    elif isinstance(v, tuple): sock.default_value = (*v, 1.0) if len(v) == 3 else v
    else: nt.links.new(v, sock)

def mix_rgb(nt, fac, a, b, blend="MIX"):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = blend
    _set_or_link(nt, m.inputs[0], fac)   # Factor
    _set_or_link(nt, m.inputs[6], a)     # A (Color)
    _set_or_link(nt, m.inputs[7], b)     # B (Color)
    return m                             # 결과 = m.outputs[2]

# ---------------- 대리석 (Infinigen table_marble 구조 + 맥 방향성 보정, 4.1+) ----------------
def _vein_layer(nt, vec, warp_scale, warp2_scale, warp2_detail, cell_scale, width, w=1.64):
    n1 = noise(nt, vec, warp_scale, dims="4D")                       # 1차 좌표 왜곡
    n2 = noise(nt, n1.outputs["Color"], warp2_scale, detail=warp2_detail)  # 2차 왜곡
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.voronoi_dimensions = "4D"; vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = cell_scale; vor.inputs["W"].default_value = w
    nt.links.new(n2.outputs["Color"], vor.inputs["Vector"])
    return ramp(nt, vor.outputs["Distance"], [(0.0, (1, 1, 1)), (width, (0, 0, 0))]), n1  # width ≤ 0.03 = 가는 맥

def make_marble(name="MAT_Marble", base=(0.83, 0.79, 0.75), vein=(0.06, 0.055, 0.05),
                stretch=(0.35, 1.0, 1.0), vein_scale=3.0, fine_amount=0.35):
    mat, nt, bsdf, out = new_clean_material(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = stretch  # 한 축을 늘려 '흐르는' 맥
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    main, n1 = _vein_layer(nt, mp.outputs["Vector"], 2.0, 2.0, 3.0, vein_scale, 0.015)   # 굵은 주맥
    fine, _ = _vein_layer(nt, mp.outputs["Vector"], 3.0, 8.0, 15.0, 3.0, 0.03, w=0.5)   # Infinigen 원본 값 = 잔맥
    fw = nt.nodes.new("ShaderNodeMath"); fw.operation = "MULTIPLY"; fw.inputs[1].default_value = fine_amount
    nt.links.new(fine.outputs["Color"], fw.inputs[0])
    vmask = nt.nodes.new("ShaderNodeMath"); vmask.operation = "MAXIMUM"
    nt.links.new(main.outputs["Color"], vmask.inputs[0]); nt.links.new(fw.outputs["Value"], vmask.inputs[1])
    cloud = ramp(nt, n1.outputs["Fac"], [(0.3, base), (0.9, tuple(c * 0.8 for c in base))])  # 바탕 얼룩
    col = mix_rgb(nt, vmask.outputs["Value"], cloud.outputs["Color"], vein)
    nt.links.new(col.outputs[2], bsdf.inputs["Base Color"])
    rough = map_range(nt, vmask.outputs["Value"], 0, 1, 0.10, 0.15)  # 광택 대리석 0.1, 맥 +0.05
    nt.links.new(rough.outputs["Result"], bsdf.inputs["Roughness"])
    bsdf.inputs["Specular IOR Level"].default_value = 0.6            # Infinigen 값
    disp = nt.nodes.new("ShaderNodeDisplacement")
    disp.inputs["Midlevel"].default_value = 0.0; disp.inputs["Scale"].default_value = 0.002
    nt.links.new(vmask.outputs["Value"], disp.inputs["Height"])
    nt.links.new(disp.outputs["Displacement"], out.inputs["Displacement"])
    return mat

# ---------------- 브러시드 메탈 (Infinigen brushed_metal) ----------------
def make_brushed_metal(name="MAT_BrushedSteel", base=(0.67, 0.64, 0.60), scale=1.0):
    mat, nt, bsdf, out = new_clean_material(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    m1 = nt.nodes.new("ShaderNodeMapping"); m1.inputs["Scale"].default_value = (0.2, 0.2, 5.0)
    nt.links.new(tc.outputs["Object"], m1.inputs["Vector"])
    na = noise(nt, m1.outputs["Vector"], 100 * scale, 15, 0.4, 0.1, dims="4D")
    m2 = nt.nodes.new("ShaderNodeMapping"); m2.inputs["Scale"].default_value = (1.0, 1.0, 20.0)
    nt.links.new(tc.outputs["Object"], m2.inputs["Vector"])
    nlow = noise(nt, tc.outputs["Object"], 0.1, 15, 0.0, dims="4D")
    warp = mix_rgb(nt, 0.2, m2.outputs["Vector"], nlow.outputs["Color"])
    nb = noise(nt, warp.outputs[2], 100 * scale, 15, 0.6, 0.1, dims="4D")
    dark = mix_rgb(nt, 1.0, na.outputs["Fac"], nb.outputs["Fac"], blend="DARKEN")
    r = map_range(nt, dark.outputs[2], 0.4, 0.6, 0.2, 0.3)           # roughness 0.2~0.3 방향성 변동
    nt.links.new(r.outputs["Result"], bsdf.inputs["Roughness"])
    v = map_range(nt, dark.outputs[2], 0.4, 0.6, 0.8, 1.2)
    hsv = nt.nodes.new("ShaderNodeHueSaturation"); hsv.inputs["Color"].default_value = (*base, 1)
    nt.links.new(v.outputs["Result"], hsv.inputs["Value"])
    nt.links.new(hsv.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.0   # Infinigen 값(금속은 Metallic=1이면 영향 작음)
    return mat

# ---------------- 나무 (판재 무늬: 링 + 결 방향 기공. Musgrave 없이 4.1+) ----------------
def make_wood(name="MAT_Oak", dark=(0.20, 0.10, 0.045), light=(0.55, 0.33, 0.17),
              ring_scale=3.0, tilt_deg=6.0, offset=0.2, coat=0.5):
    """결 방향 = 오브젝트 X축. 판재 윗면(Z)에 산 모양 무늬가 나오게 링 축을 살짝 기울인다."""
    import math
    mat, nt, bsdf, out = new_clean_material(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Location"].default_value = (0, 0, offset)
    mp.inputs["Rotation"].default_value = (0, math.radians(tilt_deg), math.radians(2))
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    wave = nt.nodes.new("ShaderNodeTexWave"); wave.wave_type = "RINGS"; wave.rings_direction = "X"
    for k, v in {"Scale": ring_scale, "Distortion": 3.0, "Detail": 4.0, "Detail Scale": 1.5}.items():
        wave.inputs[k].default_value = v
    nt.links.new(mp.outputs["Vector"], wave.inputs["Vector"])
    rings = ramp(nt, wave.outputs["Fac"], [(0.35, (1, 1, 1)), (0.85, (0, 0, 0))])
    st = nt.nodes.new("ShaderNodeMapping"); st.inputs["Scale"].default_value = (0.02, 1.0, 1.0)  # X로 50배 늘린 기공
    nt.links.new(tc.outputs["Object"], st.inputs["Vector"])
    pores = noise(nt, st.outputs["Vector"], 60.0, detail=8.0, rough=0.6)
    pr = ramp(nt, pores.outputs["Fac"], [(0.4, (1, 1, 1)), (0.7, (0, 0, 0))])
    grain = mix_rgb(nt, 0.35, rings.outputs["Color"], pr.outputs["Color"], blend="MULTIPLY")
    col = mix_rgb(nt, grain.outputs[2], dark, light)
    nt.links.new(col.outputs[2], bsdf.inputs["Base Color"])
    r = map_range(nt, grain.outputs[2], 0, 1, 0.55, 0.40)            # 어두운 결이 더 거칠게
    nt.links.new(r.outputs["Result"], bsdf.inputs["Roughness"])
    bsdf.inputs["Coat Weight"].default_value = coat                  # 오일 마감 0.1~0.3, 래커 0.5~1.0
    bsdf.inputs["Coat Roughness"].default_value = 0.05
    return mat

# ---------------- 소파 패브릭 (Infinigen sofa_fabric, UV 필요) ----------------
def make_sofa_fabric(name="MAT_SofaFabric", color=(0.18, 0.2, 0.24), strength=0.008):
    mat, nt, bsdf, out = new_clean_material(name)
    uv = nt.nodes.new("ShaderNodeUVMap")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.5479; br.squash_frequency = 1
    nt.links.new(uv.outputs["UV"], br.inputs["Vector"])
    br.inputs["Color1"].default_value = (*color, 1)
    br.inputs["Color2"].default_value = tuple(c * 0.85 for c in color) + (1,)
    for k, v in {"Scale": 276.98, "Mortar Size": 0.01, "Mortar Smooth": 1.0, "Bias": 0.5, "Row Height": 0.1}.items():
        br.inputs[k].default_value = v
    nt.links.new(br.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.86
    bsdf.inputs["Sheen Weight"].default_value = 1.0
    disp = nt.nodes.new("ShaderNodeDisplacement"); disp.inputs["Scale"].default_value = strength
    nt.links.new(br.outputs["Fac"], disp.inputs["Height"])
    nt.links.new(disp.outputs["Displacement"], out.inputs["Displacement"])
    return mat

# ---------------- 도장 금속 + 엣지 마모 (Bevel 마스크 = Cycles 전용 → 게임용은 베이크) ----------------
def _edge_signal(nt, radius, samples=16):
    """|Bevel 노멀 - 원래 노멀| : 모서리에서 커지는 값(0~약 0.77). 값의 크기는 메시·반경에 따라 크게 달라진다."""
    bev = nt.nodes.new("ShaderNodeBevel"); bev.samples = samples
    bev.inputs["Radius"].default_value = radius
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"
    nt.links.new(bev.outputs["Normal"], sub.inputs[0]); nt.links.new(geo.outputs["Normal"], sub.inputs[1])
    ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    nt.links.new(sub.outputs["Vector"], ln.inputs[0])
    return ln.outputs["Value"]

def measure_edge_signal(obj, radius=0.01, size=256):
    """마스크 값 분포(백분위수)를 굽기로 측정 → make_worn_painted_metal의 edge_lo/edge_hi를 정한다."""
    import numpy as np
    keep = [s.material for s in obj.material_slots]
    mat, nt, bsdf, out = new_clean_material("_EDGE_PROBE")
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(_edge_signal(nt, radius), em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    obj.data.materials.clear(); obj.data.materials.append(mat)
    img = bpy.data.images.new("_edge_probe", size, size, float_buffer=True)
    img.colorspace_settings.name = "Non-Color"
    tn = nt.nodes.new("ShaderNodeTexImage"); tn.image = img; nt.nodes.active = tn
    bpy.context.scene.render.engine = "CYCLES"
    for o in bpy.context.selected_objects: o.select_set(False)
    obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bpy.ops.object.bake(type="EMIT", margin=0, use_clear=True)
    v = np.array(img.pixels[:]).reshape(-1, 4)[:, 0]; v = v[v > 1e-4]
    obj.data.materials.clear()
    for m in keep: obj.data.materials.append(m)
    bpy.data.images.remove(img); bpy.data.materials.remove(mat)
    return {q: round(float(np.percentile(v, q)), 3) for q in (50, 80, 90, 95, 99)}

def make_worn_painted_metal(name="MAT_PaintedSteel_Worn", paint=(0.05, 0.12, 0.25), radius=0.01,
                            edge_lo=0.10, edge_hi=0.20, breakup_scale=40.0, amount=0.5):
    mat, nt, bsdf, out = new_clean_material(name)
    edge = map_range(nt, _edge_signal(nt, radius), edge_lo, edge_hi, 0.0, 1.0)   # 측정값으로 lo/hi 지정
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = noise(nt, tc.outputs["Object"], breakup_scale, detail=10.0)
    m = nt.nodes.new("ShaderNodeMath"); m.operation = "MULTIPLY"
    nt.links.new(edge.outputs["Result"], m.inputs[0]); nt.links.new(br.outputs["Fac"], m.inputs[1])
    mask = ramp(nt, m.outputs["Value"], [(0.0, (0, 0, 0)), (1.0 - amount, (1, 1, 1))])  # amount↑ = 더 닳음
    mask.color_ramp.interpolation = "CONSTANT"              # Metallic 0/1 규칙: 경계를 끊는다
    col = mix_rgb(nt, mask.outputs["Color"], paint, (0.56, 0.57, 0.58))   # 칠 ↔ 맨 금속(밝게)
    nt.links.new(col.outputs[2], bsdf.inputs["Base Color"])
    nt.links.new(mask.outputs["Color"], bsdf.inputs["Metallic"])       # 0 또는 1
    r = map_range(nt, mask.outputs["Color"], 0, 1, 0.45, 0.30)        # 칠 0.45, 닳은 금속 0.30
    nt.links.new(r.outputs["Result"], bsdf.inputs["Roughness"])
    return mat
```

</details>

<details>
<summary><b>pbr_audit.py</b> — PBR 규칙 위반 목록 (metallic 중간값, roughness 0, 어두운 금속, albedo 범위, 데이터 맵 sRGB, 중복 Output)</summary>

```python
# pbr_audit.py — PBR 규칙 위반 목록 (Blender 4.2 LTS / 5.0 테스트)
import bpy

DATA_SOCKETS = {"Metallic", "Roughness", "Normal", "Alpha", "Specular IOR Level", "Coat Weight",
                "Coat Roughness", "Sheen Weight", "Transmission Weight", "Subsurface Weight"}

def _upstream_images(sock, seen=None):
    """소켓 위쪽으로 거슬러 올라가 연결된 Image Texture 노드를 모은다."""
    seen = seen if seen is not None else set()
    out = []
    for link in sock.links:
        n = link.from_node
        if n.as_pointer() in seen: continue
        seen.add(n.as_pointer())
        if n.type == "TEX_IMAGE" and n.image: out.append(n)
        for s in n.inputs:
            if s.is_linked: out += _upstream_images(s, seen)
    return out

def audit_materials(objects=None):
    """PBR 규칙 위반을 목록으로 반환(값이 상수로 들어간 소켓과 이미지 컬러스페이스만 검사)."""
    issues = []
    objs = objects or [o for o in bpy.data.objects if o.type == "MESH"]
    mats = {s.material for o in objs for s in o.material_slots if s.material}
    for mat in mats:
        nt = mat.node_tree
        if nt is None:
            issues.append((mat.name, "노드 트리 없음")); continue
        bsdfs = [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"]
        outs = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"]
        if len(outs) != 1: issues.append((mat.name, f"Material Output {len(outs)}개(1개여야 함)"))
        if len(bsdfs) > 1: issues.append((mat.name, f"Principled {len(bsdfs)}개(중복 여부 확인)"))
        for b in bsdfs:
            m, r, c = b.inputs["Metallic"], b.inputs["Roughness"], b.inputs["Base Color"]
            if not m.is_linked and 0.05 < m.default_value < 0.95:
                issues.append((mat.name, f"Metallic {m.default_value:.2f} (0 또는 1만)"))
            if not r.is_linked and r.default_value < 0.02:
                issues.append((mat.name, f"Roughness {r.default_value:.3f} (0.02 이상 권장)"))
            if not c.is_linked:
                lum = max(c.default_value[:3])
                if not m.is_linked and m.default_value >= 0.95 and lum < 0.4:
                    issues.append((mat.name, f"금속인데 Base Color가 어두움(max {lum:.2f}, linear)"))
                if not m.is_linked and m.default_value <= 0.05 and (lum > 0.9 or lum < 0.015):
                    issues.append((mat.name, f"비금속 albedo 범위 밖(max {lum:.2f}, linear 0.015~0.9)"))
            for s in b.inputs:
                if not s.is_linked: continue
                for img_node in _upstream_images(s):
                    cs = img_node.image.colorspace_settings.name
                    if s.name in DATA_SOCKETS and cs not in ("Non-Color", "Linear Rec.709", "Linear"):
                        issues.append((mat.name, f"{img_node.image.name} → {s.name}: {cs} (Non-Color여야 함)"))
                    if s.name in ("Base Color", "Emission Color") and cs == "Non-Color":
                        issues.append((mat.name, f"{img_node.image.name} → {s.name}: Non-Color (sRGB여야 함)"))
    return issues
```

</details>

테스트에서 일부러 만든 나쁜 재질(Metallic 0.7, Roughness 0, sRGB 이미지를 Normal에 연결, Output 2개)은 4개 위반이 모두 잡혔고, 위 레시피 다섯 개는 위반 0건이었습니다. 이 감사는 **형태·배치 감사**인 [`scene_audit.py`](../03_playbooks/scripts/README.md)(재질 없음·UV 없음도 검사)와 함께 돌리세요.

### 4.8 후보를 여러 개 만들어 고르게 하기 (시각 루프)

[BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial)(ECCV 2024)는 VLM이 재질 노드 스크립트의 편집 후보를 만들고, 다른 VLM이 렌더를 비교해 트리 서치로 목표에 수렴하게 했습니다(예: 나무 재질 → 마블 화강암). "한 번에 생성"보다 "생성 + 시각 평가 반복"이 낫다는 근거입니다. ahujasid 서버의 `asset_creation_strategy` 프롬프트도 `get_viewport_screenshot()`을 변경 **전후**에 찍으라고 지시합니다.

```text
나무 셰이더 후보 3개를 make_wood의 ring_scale(2,3,4)·tilt_deg(3,6,10)를 바꿔 만들어라.
각각 Cycles 64spp, 45도 키라이트, 회색 배경으로 판재를 렌더해 레퍼런스 사진과 비교하라.
결 간격·색 대비·광택이 가장 가까운 것을 고르고, 차이를 세 줄로 설명한 뒤 한 번 더 개선하라.
기술 검사(audit_materials) 통과는 '보기 좋음'이 아니다. 최종 판단은 렌더 비교로 한다.
```

- 검증 렌더는 이 저장소의 [`review_views.py`](../03_playbooks/scripts/README.md)를 `color_mode="materials", engine="CYCLES"`로 쓰면 4방향을 한 번에 얻습니다(기본 `color_mode="random"`은 배치 검사용).
- "기술 검증 통과 ≠ 보기 좋음"을 품질 게이트로 분리한 예: [blender-art-factory](https://github.com/ErikBurdett/blender-art-factory).
- 조명·색관리가 틀리면 재질 판단도 틀립니다. 중립 조명·AgX 설정은 [라이팅·렌더 가이드](06_lighting_rendering_art_direction.md)를 보세요.

---

## 5. 웨더링: 엣지 마모·먼지·개체별 변화

### 5.1 렌더러별로 동작이 다릅니다

| 기법 | Cycles | EEVEE | 게임엔진·glTF | 근거 |
|---|---|---|---|---|
| Geometry `Pointiness` | 동작(메시 밀도에 의존) | **상수 0.5** | 전달 안 됨 | [GPU geometry 셰이더](https://raw.githubusercontent.com/blender/blender/main/source/blender/gpu/shaders/material/gpu_shader_material_geometry.bsl.hh) `pointiness = 0.5f` |
| `Bevel` 노드 | 동작 | 입력 노멀을 그대로 통과(효과 없음) | 전달 안 됨 | [GPU bevel 셰이더](https://raw.githubusercontent.com/blender/blender/main/source/blender/gpu/shaders/material/gpu_shader_material_bevel.bsl.hh) `result = N` |
| `Ambient Occlusion` 노드 | 동작(레이 트레이스) | **동작**(화면 공간, 시점에 따라 달라짐) | 전달 안 됨 → AO 베이크 | [GPU AO 셰이더](https://raw.githubusercontent.com/blender/blender/main/source/blender/gpu/shaders/material/gpu_shader_material_ambient_occlusion.bsl.hh) |
| `Object Info > Random` | 동작 | 동작 | 전달 안 됨(엔진 머티리얼 인스턴스 파라미터로 대체) | — |

> 정정: 조사 초안의 "Pointiness/Bevel/AO 마스크는 Cycles에서만 동작"은 AO 부분이 틀렸습니다(검증 결과). AO 노드는 EEVEE에서도 돌지만, 결과가 Cycles와 다르고 게임엔진으로는 여전히 베이크가 필요합니다.

**흔한 실수**: EEVEE 뷰포트 스크린샷으로 검증하는 에이전트가 "마모가 안 보인다"며 값을 과하게 올립니다. 마모·먼지 검증은 Cycles 렌더로 하세요.

### 5.2 4단 레이어 구성 (값)

AAA 소품은 단일 재질이 아니라 **베이스 + 변화 + 마모 + 오염** 4단으로 쌓습니다. 같은 의자 10개가 완전히 같은 색이면 바로 CG처럼 보입니다. 아래 값은 조사 원자료의 "일반 실무 값"과 Infinigen 수치입니다. 출발점으로만 쓰고 렌더로 맞추세요.

| 층 | 마스크 만드는 법 | 적용 | 값 |
|---|---|---|---|
| 베이스 | — | 4장 레시피 또는 스캔 텍스처 | 2장 규칙 |
| 개체별 변화 | `Object Info > Random` → Hue/Saturation/Value | 색상·명도를 개체마다 조금씩 | Hue 0.48~0.52, Value 0.85~1.15 |
| 엣지 마모 | Bevel 노멀 차이(4.2절) 또는 Pointiness → ColorRamp × 노이즈 → ColorRamp(Constant) | 칠(Metallic 0, R 0.45) ↔ 맨 금속(Metallic 1, Base 0.56~0.6, R 0.25~0.35) | Bevel Radius 0.005~0.02, samples 8~20. Pointiness 램프 0.50→0.56(조밀한 메시 전용). 노이즈 Scale 30~60, Detail 8~15. 임계값 0.45~0.55 |
| 캐비티 먼지 | AO(Distance 0.1~0.5m, Only Local) 반전 × Noise(Scale 5~10) | Base Color에 어두운 갈색 (0.08, 0.06, 0.04) Multiply | 세기 0.3~0.6, roughness +0.15~0.3 |
| 윗면 먼지 | Normal → Separate XYZ의 Z → Map Range(0.6~0.95 → 0~1) × 노이즈 | 밝은 회색 | roughness 0.85 |
| 긁힘 | 한 축으로 늘린 Noise(Infinigen scratches) 또는 Voronoi | 얕은 변위·roughness 변화 | 4.2절 표 |

### 5.3 엣지 마모: 마스크 값을 먼저 재고 임계값을 정하세요

이 문서의 테스트에서 가장 중요한 발견입니다(pip `bpy` 4.2.23·5.0.1, 개인 테스트, n=1). **Bevel 노멀 차이 마스크의 값 크기는 메시마다 크게 다릅니다.** 고정 임계값을 쓰면 어떤 메시에서는 마모가 전혀 안 나오고, 어떤 메시에서는 온통 벗겨집니다.

| 메시 (0.7m 큐브) | Bevel Radius | 마스크 값 백분위수 p80 / p99 | 결과 |
|---|---|---|---|
| 날카로운 모서리(로우폴리) | 0.01 | 0.11 / 0.16 (평면도 샘플 노이즈로 약 0.1) | lo/hi를 p80/p99로 주자 모서리에만 마모가 생김 |
| 3cm 베벨 모디파이어 적용 + 스무스 셰이딩 | 0.04 | 0.036 / 0.10 | 고정값(0.10~0.20)으로는 마모가 거의 안 보임 |

```python
# pbr_recipes.py(4.7절)를 import했다고 가정
obj = bpy.data.objects["Crate"]
st = measure_edge_signal(obj, radius=0.01)        # 예: {50: 0.1, 80: 0.11, 90: 0.115, 95: 0.119, 99: 0.158}
mat = make_worn_painted_metal("MAT_Crate_Worn", radius=0.01, edge_lo=st[80], edge_hi=st[99], amount=0.5)
obj.data.materials.clear(); obj.data.materials.append(mat)
```

- `amount`를 올리면 더 많이 닳습니다. 마모 폭이 **텍셀 2~3개보다 가늘면 베이크에서 사라집니다**(256px 테스트에서는 완전한 metallic 1 픽셀이 하나도 남지 않았습니다). 목표 텍셀 밀도에서 확인하세요.
- 구운 metallic 맵의 모서리 픽셀은 안티앨리어싱 때문에 중간값이 됩니다. 전환부에서만 나오는 중간값이라 괜찮습니다.
- Pointiness 방식은 메시가 조밀할 때만 쓸 만합니다(8꼭짓점 큐브에서는 무의미).

### 5.4 AAA 웨더링은 Substance Painter MCP 쪽이 효율적입니다

스마트 머티리얼·스마트 마스크는 곡률·AO 기반 마모를 업계 표준 품질로 재현합니다. Blender 셰이더로 같은 품질을 내려면 시간이 훨씬 많이 듭니다(조사 원자료의 판단, 정량 비교는 없음).

1. Painter를 `--enable-remote-scripting`으로 실행(포트 60041).
2. 메시 import → 메시 맵 베이크(AO, curvature, thickness) → smart material 적용 → smart mask(엣지 마모, 캐비티 먼지) → 엔진 프리셋으로 export.
3. 매 단계 관찰 이미지(`painter_observe` 등)를 VLM이 검증. 자세한 도구는 10장.

---

## 6. UV·텍셀 밀도·트림 시트

### 6.1 UV 방법 선택

| 대상 | 방법 | 설정 | 주의 |
|---|---|---|---|
| 하드서페이스·가구 | Smart UV Project → Pack Islands | `angle_limit=math.radians(66)`, `island_margin=0.02`, `correct_aspect=True`, `scale_to_bounds=True` → `pack_islands(shape_method='CONCAVE', margin=0.005)` | 하드서페이스 외에는 섬이 많아짐 |
| 유기체·곡면 | Unwrap `MINIMUM_STRETCH`(SLIM) | 5.0.1에 있음 | **4.2 LTS에는 없음**(테스트). SLIM 없이 빌드되면 conformal로 대체 |
| AI 생성 메시(삼각형 수프) | [PartUV](https://github.com/EricWang12/PartUV)(SIGGRAPH Asia 2025) | `python demo/partuv_demo.py --mesh_path mesh.glb --save_visuals`, 팩킹 `--pack_method uvpackmaster` | Python 3.11 + PyTorch 2.7.1. 자기교차·non-manifold 없는 입력 권장. **라이선스 주의**(아래) |
| ComfyUI Hunyuan 래퍼 결과 | 래퍼 내장 xatlas UV | — | [kijai/ComfyUI-Hunyuan3DWrapper](https://github.com/kijai/ComfyUI-Hunyuan3DWrapper). Hunyuan 라이선스는 한국 제외 |

- Smart UV를 AI 생성 메시에 쓰면 섬이 수백 개 생기고, 이음새와 밉맵 번짐이 AI 텍스처와 베이크 품질을 망칩니다. PartUV는 파트 경계에 이음새를 둬 "차트 수와 왜곡을 줄인다"고 주장합니다(벤더 자체 보고, 독립 비교 없음). 약 255 stars, 2026-07 갱신, 커뮤니티 Blender 애드온(UVgami)과 Windows 포트가 있습니다.
- **PartUV 라이선스**: 프로젝트는 Apache-2.0이지만 필수 전처리인 PartField(`preprocess_utils/partfield_official`)는 NVIDIA "non-commercial research and educational purposes only" 라이선스입니다([LICENSE](https://raw.githubusercontent.com/EricWang12/PartUV/main/LICENSE)). UVPackMaster는 유료 애드온입니다.
- 관례 목표(1차 출처 미확인, 신뢰도 낮음): UV 사용률 85% 이상, 섬 여백 2K에 4~8px·4K에 8~16px.

### 6.2 bpy 코드와 함정 (4.2·5.0 테스트)

```python
import bpy, math
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02,   # ← 라디안!
                         correct_aspect=True, scale_to_bounds=True)
bpy.ops.uv.pack_islands(shape_method="CONCAVE", margin=0.005)                # CONCAVE = Exact Shape
bpy.ops.object.mode_set(mode="OBJECT")
```

- **`angle_limit`은 라디안입니다**([소스](https://raw.githubusercontent.com/blender/blender/main/source/blender/editors/uvedit/uvedit_unwrap_ops.cc) 기본값 `DEG2RADF(66)`). `angle_limit=66.0`을 넣어도 **오류 없이** 범위 최댓값으로 잘려 들어가 결과가 달라집니다. Suzanne 테스트에서 섬 개수가 100개(라디안)가 아니라 64개가 됐습니다. blender-kiln의 `uv-materials.md`가 `angle_limit=66.0  # degrees`로 적어 둔 것이 이 실수입니다.
- `pack_islands`의 `shape_method`는 `CONCAVE`(Exact Shape), `CONVEX`, `AABB`이고, `margin` 기본값은 0.001입니다.

### 6.3 텍셀 밀도를 씬 전체에서 통일

에이전트가 에셋마다 제각각 4K를 쓰면 가까운 소품은 흐리고 먼 벽은 과해상도가 됩니다. **선명도가 들쭉날쭉한 것이 "AI 티"의 대표 원인**입니다.

| 목표 | 텍셀 밀도 | 텍스처 해상도 가이드 |
|---|---|---|
| 모바일·웹 | 5.12~10.24 px/cm (512~1024 px/m) | 1K~2K |
| 콘솔·PC | 10.24~20.48 px/cm | BaseColor·Normal 2048~4096, ORM 1024~2048 |
| 시네마틱 | 20.48 px/cm 이상 | — |

위 값은 흔히 쓰는 업계 관례로, 조사에서 1차 출처를 확인하지 못했습니다 **(신뢰도 낮음)**. 1인칭 약 1024px/m, 3인칭 약 512px/m라는 관례도 같은 상태입니다. 프로젝트 안에서 **하나로 통일하는 것**이 숫자 자체보다 중요합니다.

- [Texel Density Checker](https://github.com/mrven/Blender-Texel-Density-Checker)(v2026.1.1, Blender 4.2+ Extensions, 무료): 텍셀 밀도를 측정·설정·전달하고 vertex color로 시각화합니다. 선택한 오브젝트를 목표값(예: 10.24 px/cm)으로 Set한 뒤 베이크하세요. Python 오퍼레이터 이름은 문서에서 확인하지 못했으니 에이전트에게는 `bpy_api_lookup`으로 먼저 찾게 하세요.
- 스캔 텍스처의 실측 크기(3.2절)와 가구 실측 치수([치수 기준표](../03_playbooks/05_reference_dimensions.md))가 맞아야 나뭇결·타일 크기가 자연스럽습니다.

### 6.4 UV가 엉망인 생성 메시: 트라이플래너로 임시 작업

룩뎁 단계에서는 Image Texture 노드의 `projection='BOX'`(트라이플래너), `projection_blend` 0.15~0.3에 `Texture Coordinate > Object`를 연결하면 UV 없이도 늘어짐 없는 매핑을 바로 볼 수 있습니다(일반 실무 설정). BOX 투영은 셰이더 기능이라 glTF로 전달되지 않으니, 납품 전에 깨끗한 UV로 베이크하세요.

```python
tex.projection = "BOX"; tex.projection_blend = 0.2
nt.links.new(texcoord.outputs["Object"], mapping.inputs["Vector"])
nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
```

### 6.5 트림 시트와 데칼

- 모듈러 건축, 몰딩, 가구 테두리는 트림 시트 하나(수평 스트립)에 UV 섬을 정렬하면 적은 메모리로 높은 선명도를 얻습니다. AAA 환경 아트의 표준 기법입니다.
- [Trimmer](https://github.com/LaXHeXLuX/Trimmer)(v0.2.4, Blender 4.2+): 레퍼런스 plane을 트림 영역으로 나눠 등록하고, 선택한 면을 Fit(비율 유지 + 회전) 또는 Fill(늘려 채움)합니다. MCP 통합은 없으니 `execute_blender_code`로 오퍼레이터를 호출합니다.
- 라벨·얼룩·균열은 알파 데칼 plane으로 얹습니다. glTF 알파 모드는 8.1절을 보세요.

---

## 7. 베이크 자동화 (bpy)

### 7.1 먼저 알아야 할 동작 (검증에서 정정된 사실 포함)

| 동작 | 내용 | 근거 |
|---|---|---|
| 대상 이미지 | 재질마다 **활성 + 선택된 Image Texture 노드**가 있어야 그 이미지에 구움 | [object_bake_api.cc](https://raw.githubusercontent.com/blender/blender/main/source/blender/editors/object/object_bake_api.cc) |
| 대상 노드가 없는 슬롯 | **오류가 아니라 Info 메시지만 남기고 그 슬롯을 건너뜀** → 조용히 일부만 구워짐. 반환값은 `{'FINISHED'}` | 검증 결과 + 테스트. 메시지: 5.0.1 "No active and selected image texture node found in material …", 4.2.23 "No active image found in material …" |
| 해상도 | `width/height`(기본 512)는 **외부 파일로 저장할 때만** 쓰임. `IMAGE_TEXTURES` 대상일 때는 이미지 노드의 해상도 | 검증 결과([v4.2.0 소스](https://raw.githubusercontent.com/blender/blender/v4.2.0/source/blender/editors/object/object_bake_api.cc) 포함) |
| 기본값 | 인자로 주지 않은 값은 씬의 Bake 패널(`scene.render.bake`) 값을 씀. RNA 기본값은 margin 16, margin_type EXTEND, normal_space TANGENT | 검증 결과 |
| 렌더 엔진 | Cycles에서만 베이크 | — |

> 조사 초안의 "활성 이미지 노드가 없으면 오류가 난다"는 틀렸습니다. 실제로는 **오류 없이 건너뛰므로 더 위험합니다.** 베이크 뒤에는 항상 모든 슬롯이 구워졌는지 이미지를 확인하세요.

### 7.2 맵별 설정

| 맵 | bake 인자 | 이미지 컬러스페이스 | 메모 |
|---|---|---|---|
| Base Color | `type='DIFFUSE', pass_filter={'COLOR'}` | sRGB | 기본 pass_filter로 구우면 조명이 섞임 |
| Roughness | `type='ROUGHNESS'` | Non-Color | |
| Metallic | 전용 타입 없음 → Metallic 입력을 Emission에 임시 연결 후 `type='EMIT'` | Non-Color | 끝나면 원래 연결 복구 |
| Normal | `type='NORMAL', normal_space='TANGENT'` | Non-Color | glTF는 기본 설정(R +X, G +Y, B +Z) 유지 |
| AO | `type='AO'` | Non-Color | |
| 고폴리 → 로폴리 | `use_selected_to_active=True`, `cage_extrusion`, `max_ray_distance` | — | AI 생성 고폴리 디테일을 로폴리에 옮길 때([AI 3D 생성 가이드](04_ai_3d_generation.md)) |
| margin | 2K에 16px, 4K에 16~32px | — | 일반 실무 값 |

### 7.3 코드 (테스트 완료)

<details>
<summary><b>pbr_bake.py</b> — bake_pbr(5개 맵) · pack_orm · gltf_material (약 120줄)</summary>

```python
# pbr_bake.py — 절차 재질 → PBR 텍스처 베이크, ORM 팩킹, glTF용 재질 (Blender 4.2 LTS / 5.0 테스트)
import os
import bpy
import numpy as np

def _new_image(name, size, data):
    img = bpy.data.images.get(name)
    if img: bpy.data.images.remove(img)
    img = bpy.data.images.new(name, size, size, alpha=False, float_buffer=False)
    img.colorspace_settings.name = "Non-Color" if data else "sRGB"
    return img

def _activate_target(obj, img):
    """모든 재질 슬롯에 대상 Image 노드를 넣고 활성화. 하나라도 빠지면 그 슬롯은 조용히 건너뛰어짐."""
    tmp = []
    for slot in obj.material_slots:
        nt = slot.material.node_tree
        n = nt.nodes.new("ShaderNodeTexImage"); n.image = img; n.name = "_BAKE_TARGET"
        n.select = True; nt.nodes.active = n
        tmp.append((nt, n))
    return tmp

def _cleanup(tmp):
    for nt, n in tmp:
        nt.nodes.remove(n)

def _swap_to_emission(obj, socket_name):
    """Principled의 socket_name 값을 Emission으로 내보내게 임시 연결(메탈릭 등 전용 베이크 타입이 없는 채널용)."""
    undo = []
    for slot in obj.material_slots:
        nt = slot.material.node_tree
        out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output)
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        old = out.inputs["Surface"].links[0].from_socket if out.inputs["Surface"].is_linked else None
        em = nt.nodes.new("ShaderNodeEmission"); em.name = "_BAKE_EMIT"
        src = bsdf.inputs[socket_name]
        if src.is_linked:
            nt.links.new(src.links[0].from_socket, em.inputs["Color"])
        else:
            v = src.default_value; em.inputs["Color"].default_value = (v, v, v, 1)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        undo.append((nt, out, old, em))
    return undo

def _restore(undo):
    for nt, out, old, em in undo:
        nt.nodes.remove(em)
        if old: nt.links.new(old, out.inputs["Surface"])

def bake_pbr(obj, out_dir, size=2048, margin=16, samples=16):
    """절차 재질 → BaseColor/Roughness/Metallic/Normal/AO PNG. obj는 UV가 있어야 함."""
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = samples
    sc.render.bake.margin = margin
    for o in bpy.context.selected_objects: o.select_set(False)
    obj.select_set(True); bpy.context.view_layer.objects.active = obj
    os.makedirs(out_dir, exist_ok=True)
    jobs = [  # (파일 이름, 데이터 맵?, bake 인자, 이미션 우회 소켓)
        ("BaseColor", False, dict(type="DIFFUSE", pass_filter={"COLOR"}), None),  # 조명 없는 albedo
        ("Roughness", True, dict(type="ROUGHNESS"), None),
        ("Metallic", True, dict(type="EMIT"), "Metallic"),
        ("Normal", True, dict(type="NORMAL", normal_space="TANGENT"), None),       # glTF = OpenGL(+Y)
        ("AO", True, dict(type="AO"), None),
    ]
    paths = {}
    for name, data, kw, emit_socket in jobs:
        img = _new_image(f"T_{obj.name}_{name}", size, data)
        tmp = _activate_target(obj, img)
        undo = _swap_to_emission(obj, emit_socket) if emit_socket else []
        try:
            bpy.ops.object.bake(margin=margin, use_clear=True, **kw)
        finally:
            _restore(undo); _cleanup(tmp)
        p = os.path.join(out_dir, f"T_{obj.name}_{name}.png")
        img.filepath_raw = p; img.file_format = "PNG"; img.save()
        paths[name] = p
    return paths

def pack_orm(ao_path, rough_path, metal_path, out_path):
    """glTF/Unreal ORM: R=AO, G=Roughness, B=Metallic"""
    imgs = [bpy.data.images.load(p, check_existing=False) for p in (ao_path, rough_path, metal_path)]
    for im in imgs: im.colorspace_settings.name = "Non-Color"
    w, h = imgs[0].size
    px = [np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4) for im in imgs]
    orm = np.ones((h, w, 4), dtype=np.float32)
    orm[..., 0], orm[..., 1], orm[..., 2] = px[0][..., 0], px[1][..., 0], px[2][..., 0]
    out = bpy.data.images.new(os.path.basename(out_path), w, h, alpha=False)
    out.colorspace_settings.name = "Non-Color"
    out.pixels[:] = orm.ravel()
    out.filepath_raw = out_path; out.file_format = "PNG"; out.save()
    for im in imgs: bpy.data.images.remove(im)
    return out_path

def gltf_material(name, basecolor_path, orm_path, normal_path):
    """구운 텍스처로 glTF 내보내기용 재질 구성(AO는 'glTF Material Output' 그룹의 Occlusion으로)."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if mat.node_tree is None: mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.is_active_output = True
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    def tex(path, data):
        n = nt.nodes.new("ShaderNodeTexImage")
        n.image = bpy.data.images.load(path, check_existing=True)
        n.image.colorspace_settings.name = "Non-Color" if data else "sRGB"
        return n
    bc = tex(basecolor_path, False); nt.links.new(bc.outputs["Color"], bsdf.inputs["Base Color"])
    orm = tex(orm_path, True)
    sep = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(orm.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"])
    nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    nm = tex(normal_path, True)
    nmap = nt.nodes.new("ShaderNodeNormalMap")   # 기본 Tangent Space 유지
    nt.links.new(nm.outputs["Color"], nmap.inputs["Color"]); nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    grp = bpy.data.node_groups.get("glTF Material Output")
    if grp is None:
        grp = bpy.data.node_groups.new("glTF Material Output", "ShaderNodeTree")
        grp.interface.new_socket(name="Occlusion", in_out="INPUT", socket_type="NodeSocketFloat")
    g = nt.nodes.new("ShaderNodeGroup"); g.node_tree = grp
    nt.links.new(sep.outputs["Red"], g.inputs["Occlusion"])
    return mat
```

</details>

- 한계: `_swap_to_emission`은 재질마다 Principled가 하나라고 가정합니다(Mix Shader로 재질 두 개를 섞은 구성은 미지원). 4.1절 규칙대로 "재질 하나 = Principled 하나"로 만들고, 섞을 때는 입력 쪽(Mix 노드)에서 섞으세요.
- 베이크 뒤 원래 재질의 Coat·Sheen·Transmission 값은 텍스처에 들어가지 않습니다. 필요하면 `gltf_material`이 만든 재질의 Principled에 같은 값을 다시 넣으세요. 테스트에서 Coat Weight 0.5를 넣자 GLB에 `KHR_materials_clearcoat`가 기록됐습니다.

### 7.4 어디서 돌릴까: MCP 소켓 vs 헤드리스

ahujasid 서버의 소켓 타임아웃은 180초이고, 긴 작업은 Blender GUI를 멈춥니다. 이 문서 테스트에서 1K 맵 5장(16 samples)을 굽는 데 4 vCPU CPU로 **29초**가 걸렸습니다(개인 테스트, n=1). 픽셀 수에 비례한다고 보면 2K는 약 2분, 4K는 약 8분이라 MCP 소켓으로는 타임아웃 위험이 큽니다. **베이크는 헤드리스로 돌리세요.**

```python
# bake_export.py — 실행: blender -b asset.blend --python bake_export.py -- MyProp out
import sys, bpy
sys.path.append("/path/to/helpers")                  # pbr_bake.py를 둔 폴더
from pbr_bake import bake_pbr, pack_orm, gltf_material
name, out = sys.argv[sys.argv.index("--") + 1:][:2]
obj = bpy.data.objects[name]
p = bake_pbr(obj, out, size=2048, margin=16, samples=16)          # 끝나면 obj만 선택된 상태
orm = pack_orm(p["AO"], p["Roughness"], p["Metallic"], f"{out}/T_{name}_ORM.png")
mat = gltf_material(f"MAT_{name}_Baked", p["BaseColor"], orm, p["Normal"])
obj.data.materials.clear(); obj.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath=f"{out}/{name}.glb", export_format="GLB", use_selection=True)
```

(이 드라이버의 본문은 pip `bpy` 4.2.23·5.0.1에서 확인했습니다. pip 모듈에는 `--` 인자가 없어 이름을 직접 넣어 테스트했습니다. 결과 GLB에는 선택한 오브젝트만 들어갔고 baseColor·metallicRoughness·normal·occlusion 슬롯이 모두 채워졌습니다.)

---

## 8. glTF 내보내기 제약

### 8.1 나가는 것과 사라지는 것

[glTF-Blender-IO 공식 문서](https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst) 기준이며, "테스트" 표시는 이 문서에서 직접 확인한 것입니다.

| 항목 | glTF에서 | 방법·주의 |
|---|---|---|
| Base Color | 이미지 또는 상수 | Principled `Base Color` 입력 |
| Metallic·Roughness | **같은 이미지의 B(metallic)·G(roughness) 채널** | ORM 이미지 → Separate Color → G→Roughness, B→Metallic |
| AO | R 채널(ORM과 공유 가능) | `glTF Material Output`이라는 이름의 커스텀 노드 그룹에 `Occlusion` 입력을 만들어 연결. Blender 렌더에는 영향 없음(테스트: `occlusionTexture`가 ORM 이미지를 가리킴) |
| Normal | Tangent Space, +Y up | Normal Map 노드는 기본값(Tangent) 유지 |
| Emission | Image → Emission. 1을 넘으면 `KHR_materials_emissive_strength` | |
| Coat·Sheen·Specular·Transmission·Volume·IOR·Anisotropy·Iridescence 등 | `KHR_materials_*` 확장 | 확장 지원은 엔진마다 다름 |
| Mapping 노드 | `KHR_texture_transform` | **Point 타입 권장**. Location X·Y, Rotation Z, Scale X·Y만. Texture 타입은 균일 스케일만 |
| 알파 | Opaque / Mask(0·1로 반올림) / Blend | Alpha 입력 연결 구성으로 자동 결정. TRELLIS.2 GLB는 OPAQUE로 나오니 알파가 필요하면 DCC에서 직접 연결 |
| 이미지 포맷 | PNG·JPEG | 다른 포맷은 자동 변환(내보내기 느려짐) |
| **Displacement, SSS, 절차 노드(Noise·Voronoi·Wave·Brick…), Bevel·Pointiness·AO 마스크, BOX 투영** | **사라짐** | 베이크. 변위 디테일은 normal로 |

**테스트 결과** (pip `bpy` 4.2.23·5.0.1 동일): 4.7절 대리석 절차 재질을 그대로 GLB로 내보내자 재질에 `pbrMetallicRoughness.metallicFactor: 0`과 `KHR_materials_specular`(Specular IOR Level 0.6 → specularColorFactor 1.2)**만** 남았습니다. 색·거칠기·요철은 모두 빠졌습니다. 베이크 후 `gltf_material`로 다시 연결하자 baseColor·metallicRoughness·normal·occlusion이 모두 들어갔습니다.

**사례**: blender-kiln은 Poly Haven `american_walnut_veneer`의 맵 7개(AO, arm, Diffuse, Displacement, nor_dx, nor_gl, Rough) 중 3개(baseColor, metallicRoughness, normal)만 GLB에 남았다고 기록했습니다([texturing-strategy.md](https://raw.githubusercontent.com/elithril/blender-kiln/main/references/texturing-strategy.md)). 단 이 측정은 모든 맵을 받던 PR #367 **이전** 동작 기준이라 지금 버전에서는 재현되지 않습니다. 또 kiln의 표에는 Metallic도 ✅로 표시돼 있어 "3개"라는 서술과 약간 어긋납니다. kiln 문서의 "AO는 ARM 팩킹 배치에서만 채워진다"는 설명은 공식 문서와 다릅니다(검증 결과).

### 8.2 내보낸 뒤 감사: 만든 맵 vs 들어간 슬롯

Blender 없이 일반 Python으로 돌아갑니다(테스트 완료).

```python
import json, struct
def glb_material_report(path):
    data = open(path, "rb").read()
    n = struct.unpack("<I", data[12:16])[0]          # 첫 청크(JSON) 길이
    js = json.loads(data[20:20 + n])
    rows = []
    for m in js.get("materials", []):
        pbr = m.get("pbrMetallicRoughness", {})
        rows.append((m.get("name"), {
            "baseColor": "baseColorTexture" in pbr,
            "metalRough": "metallicRoughnessTexture" in pbr,
            "normal": "normalTexture" in m,
            "occlusion": "occlusionTexture" in m,
            "emissive": "emissiveTexture" in m,
            "ext": sorted(m.get("extensions", {}))}))
    return rows

print(glb_material_report("out/MyProp.glb"))
# 예: [('MAT_MyProp_Baked', {'baseColor': True, 'metalRough': True, 'normal': True, 'occlusion': True, 'emissive': False, 'ext': []})]
```

에이전트에게 "베이크한 맵 목록과 이 결과를 비교해 빠진 슬롯이 있으면 원인을 찾아 다시 내보내라"고 지시하세요.

### 8.3 엔진으로 보낼 때

- **Blender 노드 셰이더는 Unreal로 넘어가지 않습니다.** 한국 개발자로 추정되는 KINGWONWOO의 [Unreal_MCP_Persona](https://github.com/KINGWONWOO/Unreal_MCP_Persona)(2026-02)는 이 문제로 텍스처 기반 PBR로 바꿨습니다. 엔진 대상이면 처음부터 "베이크된 텍스처"를 산출물로 잡으세요.
- Unreal에서는 ORM 텍스처를 sRGB 해제(Masks 압축)로 import합니다. 노멀맵은 엔진의 녹색 채널 규약을 확인하세요(DirectX 규약 엔진이면 G 반전).
- 최종 머티리얼 인스턴스와 톤 변주는 엔진 조명 아래에서 조정해야 정확합니다. UE 5.8 Epic 공식 실험적 Unreal MCP, 머티리얼 그래프를 다루는 [monolith](https://github.com/tumourlove/monolith)(UE 5.7/5.8, MIT, 316 stars, 세부 기능 미검증)는 [기타 MCP·엔진 가이드](03_other_mcp_dcc_cad_engines.md)를 보세요.
- 파일 경량화(gltf-transform, Draco)와 LOD는 [에셋·파이프라인 가이드](10_assets_pipeline_licensing.md)에 있습니다.

---

## 9. AI 텍스처 생성 도구 비교

### 9.1 상황별 선택

| 상황 | 추천 조합 | 이유 |
|---|---|---|
| 한국, 상업, 로컬 GPU 8~16GB | StableGen(SDXL) → Marigold IID·StableDelight로 PBR 분해 → Bake Textures | 지역 제한 없는 오픈 도구로 Blender 안에서 끝까지. 모델별 라이선스는 따로 확인 |
| 한국, 상업, GPU 24GB 이상 | 위 조합 + TRELLIS.2 texturing(법무 검토 후) | Hunyuan 대체. TRELLIS.2는 nvdiffrast 비상업 의존. Step1X-3D 텍스처 모델은 Apache-2.0으로 배포되지만 Hunyuan 파생 코드·nvdiffrast 의존이 있어 법률 검토 전 보류(9.2 표) |
| GPU 부족 / 빠른 결과 | Meshy retexture(`enable_pbr=true`, `remove_lighting=true`, `enable_original_uv=true`) | 클라우드. 플랜별 결과물 라이선스는 [AI 3D 생성 가이드](04_ai_3d_generation.md) |
| 가구처럼 부위가 뚜렷함 | 3.4절 라이브러리 할당 우선 → 부족하면 Tripo `texture_model(part_names=[...])` | 부위별 텍스처링 |
| 새 타일링 재질 | FLUX 등 + ComfyUI-seamless-tiling → Offset 검사 → PBRify/DeepBump(상업) 또는 CHORD(연구만) | 데이터 맵은 추정기로 |
| 조명이 구워진 기존 텍스처를 PBR로 | StableDelight(하이라이트 제거), Marigold IID, Material Anything(라이선스 확인) | de-lighting |
| 구형 게임 리마스터 | PBRify_Remix + RTX Remix(내장 MCP) | CC0 학습 데이터 |

### 9.2 메시에 직접 텍스처를 입히는 도구

| 도구 | 방식 | PBR 출력 | 요구 사양 | 라이선스·상업 | 한국 | MCP·연동 | 기준 |
|---|---|---|---|---|---|---|---|
| [Meshy](https://github.com/meshy-dev/meshy-mcp-server) retexture | 클라우드. 스타일 입력은 text(최대 600자)·이미지·멀티뷰(1~4장, meshy-7/latest) 중 **정확히 하나** | `enable_pbr=true`일 때만. **PBR 맵은 2K 고정**(`texture_resolution` 2k/4k/8k는 Base Color에만) | 크레딧: 텍스처 2K·4K 10, 8K 15 | 플랜별 | 가능 | 공식 Meshy MCP(도구 24개) | 2026-09 |
| [Tripo](https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/tripo3d/client.py) `texture_model` | 클라우드. `part_names`로 부위별 | `pbr` 기본 True | 크레딧(세부 미확인) | 플랜별(무료 플랜은 비상업) | 가능 | [Python SDK](https://pypi.org/project/tripo3d/)(tripo3d 0.4.2) 직접 호출이 현실적. 공식 [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp)는 마지막 커밋 2025-04-14인 alpha라 추천하지 않음. ahujasid `generate_tripo_model`은 유료 Premium 전용 | — |
| [Scenario Blender plugin](https://github.com/scenario-labs/blender-plugin) | 클라우드(선택 메시용 PBR 맵 생성) | PBR 맵 | Blender 5.0+, CU 과금(생성 전 비용 추정 확인) | 플러그인 GPL-3.0-or-later. 모델 세부 미확인 | 가능 | 로컬 MCP `http://127.0.0.1:9876/mcp`(**blender-mcp와 충돌**), 호스티드 MCP `mcp.scenario.com`. 임의 Python 실행은 별도 opt-in | Experimental, 2026-09 |
| [Hunyuan3D-Paint 2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) | 오픈 웨이트, 멀티뷰 PBR 확산([MaterialMVP](https://github.com/ZebinHe/MaterialMVP) 계열). `Hunyuan3DPaintConfig(max_num_view=6, resolution=512)` | 조명 불변 albedo + metallic-roughness | 텍스처 21GB, 형상+텍스처 29GB | Tencent Community License. MAU(월간 활성 사용자) 100만 조항은 버전 출시일 직전 달을 한 번 보는 조건 | **✗ 라이선스 범위 밖(출력물 포함)** | [ComfyUI 래퍼(kijai)](https://github.com/kijai/ComfyUI-Hunyuan3DWrapper), [3DGenStudio](https://github.com/visualbruno/3DGenStudio) | 2.1 공개 2025-06-13, Paint v2-1(2B) 2025-06-14 |
| ahujasid `texture_mesh_hunyuan3d` ([PR #343](https://github.com/ahujasid/blender-mcp/pull/343)) | 기존 메시를 GLB로 로컬 Hunyuan3D-2 서버 `/generate(texture=True)`에 보내 재텍스처, 원본은 숨김 | Hunyuan3D-2 페인트(2.1 PBR 아님) | 로컬 GPU 서버. `LOCAL_API` 전용 | Hunyuan3D-2 라이선스 | **✗** | MCP 도구(병합 전) | 2026-09-02 오픈, 미병합 |
| [TRELLIS.2](https://github.com/microsoft/TRELLIS.2) texturing | 4B, 기존 형상에 PBR(`example_texturing.py`, `app_texturing.py`) | Base Color·Roughness·Metallic·Opacity | 24GB 이상(A100/H100 검증) | 코드 MIT, 그러나 [nvdiffrast](https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt)는 NVIDIA Source Code License(비상업) → **상업 전 법무 검토** | 지역 제한 없음 | StableGen v0.3.0+, ComfyUI 본체([AI 3D 생성 가이드](04_ai_3d_generation.md)) | GLB는 OPAQUE로 나옴. 예시 `texture_size 4096`, `decimation_target 1000000` |
| [Step1X-3D](https://github.com/stepfun-ai/Step1X-3D) | 3.5B 텍스처 모델, SDXL 기반 멀티뷰 동기화 | PBR 여부 미확인 | [AI 3D 생성 가이드](04_ai_3d_generation.md) 참고 | README·LICENSE는 Apache-2.0. 그러나 텍스처 모듈(`custom_rasterizer`, `differentiable_renderer`)이 Hunyuan3D 2.0 코드를 재사용해 **Tencent Hunyuan 라이선스 헤더**가 남아 있고 nvdiffrast에도 의존([mesh_render.py](https://raw.githubusercontent.com/stepfun-ai/Step1X-3D/main/step1x3d_texture/differentiable_renderer/mesh_render.py)) | **△ 텍스처 단계는 법률 검토 전 보류** | NVIDIA Texture Agent가 백엔드로 언급 | 2025 |
| [StableGen](https://github.com/sakalond/StableGen) | Blender 애드온. ComfyUI 백엔드(SDXL, FLUX.1-dev, FLUX.2 Klein(실험적), Qwen-Image-Edit)로 멀티뷰 투영 → Bake Textures | v0.3.0부터 Marigold IID·StableDelight로 albedo·roughness·metallic·normal·height·emission 분해(AO는 Blender 베이크) | SDXL 8GB, FLUX/Qwen 16GB+, FLUX.2 Klein 약 13GB. 모델 다운로드 7~33GB | 애드온 GPL-3.0, 모델별 별도 | 모델 라이선스에 따름 | MCP로 노출 안 됨(애드온 UI) | [v0.3.1](https://github.com/sakalond/StableGen/releases) 2026-06-12. **Blender 4.2~4.5, 5.1+ 지원, 5.0 미지원**(OSL 문제, 네이티브 Raycast 없음) |
| [MV-Adapter](https://github.com/huanngzh/MV-Adapter) | 형상 조건 멀티뷰(6뷰, 768px), `texture_t2tex`/`texture_i2tex` | **diffuse만** | SD2.1 10GB 미만, SDXL i2mv 약 14GB, 형상 조건 SDXL은 16GB 초과 권장 | 코드 Apache-2.0, 베이스 모델 별도 | 가능 | ComfyUI-MVAdapter | ICCV 2025 |
| [Material Anything](https://github.com/3DTopia/MaterialAnything) | 무텍스처·albedo만·생성·스캔 메시 → PBR. confidence mask, UV 공간 refiner | albedo·roughness·metallic·bump | PyTorch3D 등 설치 까다로움 | 코드 MIT지만 [Text2Tex](https://github.com/daveredrum/Text2Tex)(CC BY-NC-SA 3.0) 설정을 그대로 쓰고 가중치 라이선스 미확인 → **상업 안전 단정 불가** | 조건 확인 | — | CVPR 2025 |

### 9.3 이미지 → PBR 맵·타일링 도구

| 도구 | 하는 일 | 라이선스 | 비고 |
|---|---|---|---|
| [CHORD](https://github.com/ubisoft/ubisoft-laforge-chord) (Ubisoft La Forge) | 텍스처 이미지 → PBR 분해(base color·normal·height·roughness·metalness로 소개됨. 출력 목록은 README에서 미확인) | **Research-Only**. [LICENSE](https://raw.githubusercontent.com/ubisoft/ubisoft-laforge-chord/main/LICENSE) "Commercial use is strictly prohibited" | SIGGRAPH Asia 2025, arXiv 2509.09952. [ComfyUI-Chord](https://github.com/ubisoft/ComfyUI-Chord)(`chord_v1.safetensors`, `chord_image_to_material.json`), HF 로그인 필요 |
| [Marigold IID](https://github.com/prs-eth/Marigold) | Appearance: Albedo·Roughness·Metallicity / Lighting: Albedo·Shading·Residual | 코드 Apache-2.0, 가중치 RAIL++-M(사용 제한 조항 확인) | v1.1, 2025-05-15, diffusers 0.28+. 이미지 공간 추정이라 UV 이음새·뷰 일관성은 별도 처리 |
| [StableDelight](https://github.com/Stable-X/StableDelight) | 스페큘러(하이라이트) 제거 | Apache-2.0 | albedo 오염의 가장 흔한 원인 제거. 그림자(AO 성분) 제거는 제한적 |
| [PBRify_Remix](https://github.com/Kim2091/PBRify_Remix) | 업스케일(DXT1 압축·디더링·헤일로 복원) + normal·roughness·height(height 기본 꺼짐) | **CC0**(ambientCG CC0 데이터로만 학습) | 2026-02 갱신. chaiNNer `.chn` 또는 [ComfyUI-RTX-Remix](https://github.com/NVIDIAGameWorks/ComfyUI-RTX-Remix)(ComfyUI 0.3.48+, WIP)의 `integration_pbrify.json`·`restapi_pbrify(_lowVRAM).json` |
| [DeepBump](https://github.com/HugoTini/DeepBump) | color→normal, normal→height, normal→curvature(엣지 마모 마스크로 활용) | GPL | Blender 애드온(Shader Editor 탭)과 CLI. 가볍지만 정확도는 CHORD·Marigold보다 낮음 |
| [Materialize](https://github.com/BoundingBoxSoftware/Materialize) | 단일 이미지 → height·normal·metallic·smoothness·edge·AO | GPL-3.0 | Unity 기반, 유지보수 사실상 중단 |
| [ComfyUI-seamless-tiling](https://github.com/spinagon/ComfyUI-seamless-tiling) | circular padding으로 이음매 없는 생성(X·Y 독립), `Make Circular VAE`, `Circular VAE Decode`, 검사용 `Offset Image` | GPL-3.0 | FLUX 등 DiT 계열 지원은 미확인 |
| [Dream Textures](https://github.com/carson-katri/dream-textures/releases) | Blender 안 SD 타일링·투영 | 오픈소스 | v0.4.1(2024-08-26) 이후 정체 → 신규 프로젝트는 StableGen |
| Substance 3D Sampler "Image to Material" / Firefly text-to-texture | 사진·AI 이미지 → PBR, 텍스트 → 타일링 텍스처 | Adobe 구독 | Firefly 기반 Sampler Text to Texture 베타는 2024-03-18 출시([Adobe 발표](https://news.adobe.com/news/news-details/2024/adobe-brings-firefly-generative-ai-into-substance-3d-workflows), 보완 검증). 2026년 정식 여부·버전·크레딧 단가는 **(미확인)**. 공식 MCP 없음. Claude의 'Adobe for creativity' 커넥터(2026-04-28)에는 Substance 3D가 없음([기타 MCP 가이드](03_other_mcp_dcc_cad_engines.md)) |

**타일링 재질 파이프라인 예** (albedo만 생성, 데이터 맵은 추정):

```text
FLUX + ComfyUI-seamless-tiling으로 albedo 생성 ("flat lighting, no shadows, top-down, seamless")
→ Offset Image 50%로 이음새 확인
→ StableDelight로 남은 하이라이트 제거
→ Marigold Appearance로 roughness/metal 초안, DeepBump로 normal/height (상업 가능 조합)
   (연구·프로토타입이면 CHORD)
→ Blender에서 2.1절 규칙으로 값 범위 점검 (audit_materials) → 렌더 비교
```

### 9.4 절차 그래프를 만드는 연구

| 연구 | 내용 | 라이선스 | 쓰임 |
|---|---|---|---|
| [VLMaterial](https://github.com/mit-gfx/VLMaterial) (ICLR 2025 Spotlight) | 입력 이미지 → Blender 셰이더 노드 그래프를 Python 프로그램으로 생성(LLaVA-NeXT, LLaMA-3 8B 파인튜닝) + Infinigen 포크 렌더 + MCMC 파라미터 정제 | 코드 MIT, **데이터셋 CC BY-NC 4.0** | 학습에 48GB 이상. 레퍼런스 사진을 편집 가능한 재질로 역설계하는 연구 참고 |
| [BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial) (ECCV 2024) | VLM 편집 생성기 + VLM 상태 평가기의 트리 서치, 텍스트→이미지로 목표를 "상상" | 오픈소스(연구) | 2024-12 이후 정체. 패턴을 MCP 루프에 차용(4.8절) |

### 9.5 Meshy·Tripo 호출 요령

**Meshy** ([postprocessing.ts](https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/schemas/postprocessing.ts), [generation.ts](https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/schemas/generation.ts), [instructions.ts](https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/instructions.ts))

```text
설치: npx add-mcp @meshy-ai/meshy-mcp-server --env MESHY_API_KEY=...

meshy_retexture(
  model = <기존 모델>,
  text_style_prompt = "Scandinavian dining chair in solid white oak, natural matte oil finish,
                       fine straight grain, slightly darker end grain, subtle wear on armrest edges,
                       no baked shadows or highlights, uniform albedo",
  enable_pbr = true,            # 기본 false → 명시하지 않으면 albedo만
  enable_original_uv = true,    # 기본 true. 기존 UV 유지
  remove_lighting = true,       # 기본 true. meshy-6 / latest에서만 지원
  texture_resolution = "4k",    # Base Color에만 적용. PBR 맵은 2K 고정
  ai_model = "latest"           # retexture의 latest = Meshy 7
)
```

- 스타일 입력(text / image / multiview)은 **하나만** 줍니다.
- 서버 지침상 크레딧을 쓰는 호출은 **비용을 먼저 제시하고 사용자 확인**을 받아야 하고, 출력 포맷(`target_formats`)은 생성 시점에 정해야 합니다.
- image-to-3D에서 `latest`와 `remove_lighting`을 함께 쓰면 작업이 Meshy 6으로 처리되고, text-to-3D의 `latest`는 Meshy 6으로 해석됩니다(검증 결과). 크레딧: Meshy 7 image-to-3D 메시만 20, 텍스처 포함 30.
- 텍스처 프롬프트에는 **재질, 마감, 색, 마모 위치, "그림자·하이라이트 없음"**을 넣습니다. 결과 맵의 물리적 정확성은 2.1절 규칙으로 따로 확인하세요.

**Tripo** `texture_model` 파라미터([SDK API.md](https://github.com/VAST-AI-Research/tripo-python-sdk/blob/master/docs/API.md) 기준. 검증에서 API.md의 `smart_lowpoly` 설명이 현행 코드와 다른 것이 확인됐으니, 쓰기 전에 [client.py](https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/tripo3d/client.py)로 인자를 다시 확인하세요. [에셋 가이드 2.7절](10_assets_pipeline_licensing.md) 참고): `texture`(기본 True), `pbr`(기본 True), `texture_quality` `'standard'`(기본)/`'detailed'`, `texture_alignment` `'original_image'`(기본, 참조 이미지 충실)/`'geometry'`(형상 맞춤 디테일), `texture_seed`, `bake`(기본 True), `text_prompt`, `image_prompt`, `style_image`, `part_names`.

```python
texture_model(pbr=True, texture_quality="detailed", texture_alignment="geometry", part_names=["seat", "legs"])
```

### 9.6 로컬 GPU 예산 (README 기준 요구 VRAM)

| VRAM | 쓸 수 있는 것 |
|---|---|
| 8GB | StableGen(SDXL) |
| 10GB 안팎 | MV-Adapter SD2.1 버전(10GB 미만) |
| 12~16GB | StableGen FLUX.2 Klein(약 13GB), MV-Adapter SDXL i2mv(약 14GB), StableGen FLUX/Qwen(16GB 이상) |
| 21~24GB | Hunyuan3D-Paint 2.1 텍스처(21GB, 한국 제외), TRELLIS.2(24GB 이상), TEXGen 추론(24GB) |
| 29GB 이상 | Hunyuan3D 2.1 형상+텍스처(29GB, 한국 제외) |

RTX 4090(24GB)은 TRELLIS.2와 Hunyuan Paint의 경계선입니다. VRAM이 부족하면 해상도를 낮추게 되고 결과가 흐려지니, 차라리 클라우드 API(Meshy·Tripo)나 원격 ComfyUI를 쓰세요.

### 9.7 연구 계보 (원리만 알아 두기)

실무 도구(Hunyuan Paint, StableGen, 상용 서비스)에 흡수된 기법들입니다. 실패 원인과 해법을 이해하는 데 씁니다.

| 연구 | 해결한 문제 |
|---|---|
| [Text2Tex](https://github.com/daveredrum/Text2Tex) (ICCV 2023) | depth-aware 인페인팅 + next-best-view. 백팩 예시 약 500초 + 정제 약 360초, 12GB GPU |
| [SyncMVD](https://github.com/LIU-Yuxin/SyncMVD) | 디노이징 단계마다 뷰 간 정보 공유로 **이음새 제거**(SD1.5 + depth/normal ControlNet, 약 4만 면 이하, 깨끗한 UV 필요) |
| [Paint3D](https://github.com/OpenTexture/Paint3D) (CVPR 2024) | **조명 없는** 2K UV 텍스처, UV 인페인팅으로 가려진 곳 채우기 |
| [TEXGen](https://github.com/CVMI-Lab/TEXGen) (SIGGRAPH Asia 2024) | UV 도메인 feed-forward albedo(테스트 24GB) |
| [RomanTex](https://github.com/oakshy/RomanTex) (ICCV 2025) | 3D-aware RoPE로 멀티뷰 일관성 |
| [MaterialMVP](https://github.com/ZebinHe/MaterialMVP) (ICCV 2025) | 조명 불변 멀티뷰 **PBR**. Hunyuan3D-Paint-v2-1의 기반 |

정리하면 **이음새는 뷰 동기화로, 가려진 곳은 UV 인페인팅으로, 구워진 조명은 de-lighting 학습으로** 해결하는 흐름입니다. 더 많은 논문은 [학술 연구 가이드](11_research_papers.md)에 있습니다.

---

## 10. 텍스처 전용 MCP

### 10.1 비교표 (2026-09)

| MCP | 대상 | 만든 곳 | 기능 | 연결 | 라이선스 | 성숙도 | 판단 |
|---|---|---|---|---|---|---|---|
| ahujasid MCP for Blender — Poly Haven | Blender | 커뮤니티 | Poly Haven 도구 6개, `set_texture`(컬러스페이스 자동), `describe_node_type`, `bpy_api_lookup`, `get_viewport_screenshot` | TCP `localhost:9876` | MIT | 약 29.4k stars, PyPI 2.1.0(2026-09-25) | **1순위.** PR #367 이후 버전 |
| [SubstancePainterMCP](https://github.com/elliezu/SubstancePainterMCP) (elliezu) | Substance 3D Painter | 커뮤니티(Adobe와 무관) | 도구 79개: `create_fill_layer`, `set_fill_channels`, `insert_smart_material`, `apply_smart_mask`, `set_procedural_input`, `set_baking_mesh_inputs`, `apply_baking_preset`, `start_batch_bake`, `export_textures`, `start_mesh_reload`(Auto UV) 등. 원자적 롤백, 임의 Python은 opt-in일 때만 | Painter를 `--enable-remote-scripting`으로 실행 → `localhost:60041` | MIT | v1.0.0, Painter 12.1.1에서 실측 검증, 36 stars, 2026-07-28 | AAA 웨더링에 가장 효율적 |
| [painter-mcp](https://github.com/parodyband/painter-mcp) (parodyband) | Painter 12.1.4 | 커뮤니티 | `painter_status` → `painter_observe`(텍스처·창 이미지) → `painter_run`(배치 + 검증)의 관찰 중심 흐름 | — | MIT | 0 stars | 관찰 루프 설계 참고. 이 밖에도 Painter MCP가 10개 이상 있음([기타 MCP 가이드](03_other_mcp_dcc_cad_engines.md)) |
| [substance-designer-mcp](https://github.com/matthieuhuguet/substance-designer-mcp) | Substance 3D Designer | 커뮤니티 | 도구 16개(`create_graph`, `create_node`, `connect_nodes`, `set_parameter`, `build_material_graph`, `build_heightmap_graph`, `apply_recipe` 등), **레시피 79개**(화강암·강철·나무·콘크리트 등). 편집 가능한 `.sbs` 그래프 산출 | FastMCP 브리지 → TCP `localhost:9881` | MIT | Designer 15.0.3 테스트, 43 stars, 2026-05 | 타일링 PBR 재질. **도구는 한 번에 하나씩 순차 호출**(일부 SD 15.x API는 앱을 멈추고, 잘못된 포트 ID는 크래시) |
| [MaterialPilot](https://github.com/SS-360/materialpilot) | [Material Maker](https://github.com/RodZill4/material-maker) 1.7 + Godot 4.7 | 커뮤니티 | 도구 143개, 노드 디스크립터 392개, dry-run 패치, 스냅샷 기반 원자적 적용·롤백, albedo~emission 채널, Blender 프로파일 PNG/EXR 내보내기(SHA-256 검증) | 로컬 | MaterialPilot Apache-2.0, Material Maker MIT | 0.1.0 preview, 5 stars, 2026-09. README가 Codex(GPT-5.6)를 주 개발 협업자로 명시 | **참고용**(독립 사용 사례 없음) |
| [comfy-mcp](https://github.com/Comfy-Org/comfy-mcp) | ComfyUI | **Comfy-Org 공식** | 로컬 ComfyUI 워크플로 실행 | 로컬 | — | 237 stars, 2026-09 활동 | CHORD·Hunyuan 래퍼·MV-Adapter·PBRify·seamless-tiling·StableGen 백엔드가 모두 ComfyUI 위에서 돎. 커뮤니티 `artokun/comfyui-mcp`는 공식으로 대체되어 2026-10-09 아카이브 예정 |
| RTX Remix Toolkit 내장 MCP ([toolkit-remix](https://github.com/NVIDIAGameWorks/toolkit-remix)) | RTX Remix | **NVIDIA 공식** | REST API를 MCP 도구로. `.agents`/`.claude` 스킬 동봉, 저장소 `.mcp.json`에 `remix` 서버 등록 | Streamable HTTP `http://127.0.0.1:18014/mcp`(사용 중이면 18014~18019) | — | [CHANGELOG](https://raw.githubusercontent.com/NVIDIAGameWorks/toolkit-remix/main/CHANGELOG.md) REMIX-4173·4164 | 구형 게임 리마스터 + PBRify. 조사 초안의 "공식 MCP 미확인"은 틀렸음(검증에서 정정) |
| [Meshy MCP](https://github.com/meshy-dev/meshy-mcp-server) | Meshy 클라우드 | 공식 | 도구 24개, `meshy_retexture` | npx | — | 2026-09 활발 | 9.5절 |
| [Scenario](https://github.com/scenario-labs/blender-plugin) | Scenario | 공식 플러그인 | PBR 맵 생성 | 로컬 `127.0.0.1:9876/mcp` 또는 호스티드 `mcp.scenario.com` | GPL-3.0-or-later | Experimental | 로컬은 9876 충돌 → 호스티드 권장 |
| [Quartermaster](https://github.com/Tanshaydar/Quartermaster) | 보유한 Fab/Megascans 등 | 커뮤니티 | 로컬 인덱싱(텍셀 밀도·맵 목록) → MCP 검색 | 로컬 | MIT | 2 stars | Megascans 공식 경로가 없어서 대안 |
| [dcc-mcp](https://github.com/dcc-mcp) 어댑터 | Poly Haven·ambientCG·Fab·Painter 등 | 커뮤니티 | 스킬 기반 | — | MIT | 0~1 stars, 일괄 생성 | **미검증**. 근거로 쓰지 않음 |
| BlenderKit | — | — | 전용 MCP 없음 | — | — | — | 사람이 UI로 드래그앤드롭 |
| Adobe Substance 공식 MCP | — | — | **없음**(확인 안 됨) | — | — | — | 커뮤니티 서버 사용 |

> 주의: "texture mcp pbr" 검색 상위에 과장된 이름의 AI 생성형 skill 저장소(예: `genpark-realtime-neural-3d-mesh-pbr-texture-generator-skill`)가 보입니다. SEO 성격이라 이 지식베이스에서는 근거로 쓰지 않았습니다.

### 10.2 포트 정리

| 포트 | 누가 쓰나 | 충돌 |
|---|---|---|
| 9876 | Blender Lab 공식 서버, ahujasid MCP for Blender, Scenario 로컬 MCP | **셋 다 Blender 안에서 같은 포트를 바인드** → 한 번에 하나만 |
| 60041 | Substance Painter 원격 스크립팅 | — |
| 9881 | Substance Designer MCP 브리지 | — |
| 18014~18019 | RTX Remix Toolkit MCP | — |

### 10.3 Substance Painter MCP 작업 순서 (예)

```text
1. Painter 실행: "Adobe Substance 3D Painter.exe" --enable-remote-scripting   (포트 60041)
2. 메시 로드 (UV 없으면 start_mesh_reload의 Auto UV)
3. set_baking_mesh_inputs → apply_baking_preset → start_batch_bake   (AO, curvature, thickness 등)
4. insert_smart_material  (부위별: 도장 금속, 오크 등)
5. apply_smart_mask       (엣지 마모, 캐비티 먼지)
6. 매 단계 관찰 이미지를 VLM이 레퍼런스와 비교 → 필요하면 롤백
7. export_textures        (엔진 프리셋: Unreal ORM 등)
8. 엔진·Blender로 가져와 8.2절 슬롯 감사
```

도구 이름과 인자는 서버 버전마다 다를 수 있으니 세션 시작 때 도구 목록을 먼저 조회하게 하세요.

---

## 11. 다른 사람들은 어떻게 했나 (사례)

| 사례 | 누가·언제 | 무엇을·어떻게 | 결과·교훈 |
|---|---|---|---|
| Poly Haven 연동 수정 | Greg Zaal(Poly Haven), 2026-09-14 보고 → 09-21 병합 | [#361](https://github.com/ahujasid/blender-mcp/issues/361)에서 버그 6개 보고, [PR #367](https://github.com/ahujasid/blender-mcp/pull/367)로 단일 매핑 테이블·POINT 매핑·필요한 맵만 다운로드·.blend 원본 import·테스트 248개 | 다운로드 49% 감소. **도구가 "성공"을 반환해도 노드 연결을 렌더나 스크립트로 확인해야 함** |
| 렌더만 회색 | psiQAQ 보고, 2026-08-09 종료 | [#190](https://github.com/ahujasid/blender-mcp/issues/190): `set_texture`가 기존 노드를 지우지 않아 Output·Principled가 여러 개 | `_reset_material_nodes_principled`로 수정. **재질 코드는 idempotent해야 함** |
| blender-kiln | elithril, 2026-08 | Claude Code 플러그인. CONFIG→BRIEF→SOURCE→IMPORT→CLEANUP→TEXTURING→OPTIMIZE→EXPORT 8단계와 규칙 31개, 내보내기 전 "받은 맵 vs 채워진 슬롯" 감사 | **(정정)** 갤러리 15개 에셋(21,879 tris, 1,456.2kB→132.7kB, 91% 감소)은 스킬·MCP 실행 결과가 아니라 `blender --background --python` 스크립트 결과라고 [README](https://raw.githubusercontent.com/elithril/blender-kiln/main/README.md)가 밝힘. 소규모(13 stars)·수치 오류가 있어 **신뢰도 낮음** |
| Unreal_MCP_Persona | KINGWONWOO(한국 개발자로 추정), 2026-02 | Claude MCP(Blender 모델링) + Nano Banana MCP(BaseColor·Normal·Roughness·Metallic 4장을 각각 프롬프트로 생성) + Unreal 브리지 | Blender 노드 셰이더가 Unreal로 안 넘어가 텍스처 기반으로 전환. 이미지 모델이 데이터 맵까지 "그리는" 방식은 물리적 일관성을 검증하기 어려움(조사자 분석) |
| MaterialPilot "Abandoned Industrial Floor" | SS-360, 2026-09 | 카탈로그 조회 → 스냅샷 → 패치 dry-run → 검증 → `.ptex` 저장 → 2048 Blender용 내보내기 → SHA-256 검증 | "아티스트가 계속 편집할 수 있는" 절차 재질. 품질은 독립 확인 없음 |
| NVIDIA Material Agent | NVIDIA Omniverse, 2026 | VLM이 렌더를 보고 라이브러리에서 부위별 재질 선택(3.4절) | "시각 증거 우선, 문서는 보조", "생성보다 선택"의 레퍼런스 |
| PBRify_Remix | Kim2091·NVIDIA, 2025~2026-02 | CC0 데이터로만 학습한 모델로 구형 게임 텍스처 업스케일 + PBR | 학습 데이터 출처가 깨끗한 "윤리적 AI 텍스처" 사례 |
| StableGen 전 과정 | sakalond와 커뮤니티, 2025-10~2026-09 | TRELLIS.2 생성 → Sequential+IPAdapter 멀티뷰 → UV Inpaint → Bake → PBR 분해 | 오픈소스 로컬 도구만으로 끝까지 가능. PBR 분해를 독립 실행하는 버튼 요청([#116](https://github.com/sakalond/StableGen/issues/116), 현재 Closed, 해결 방식 미확인) |
| Infinigen 절차 재질 | Princeton VL, 2023~2026 | 파라미터 랜덤화한 대리석·나무·금속·패브릭·마모 | 수치가 구체적이라 LLM 참고서로 훌륭하지만 metallic 0.37대 비물리 값 → 0/1로 교정 |
| 이 문서의 테스트 | 2026-09-27, pip `bpy` 4.2.23 LTS·5.0.1 | 재질 5종 생성·렌더·베이크·glTF 내보내기·감사 | 절차 재질 GLB 소실, 베이크 슬롯 조용한 건너뜀, `angle_limit` 도 단위 함정, 4.2에 SLIM 없음, 엣지 마스크 값의 메시 의존성, 1K 5장 베이크 29초(4 vCPU) (모두 개인 테스트, n=1) |

더 많은 사례는 [사례 모음](../04_case_studies/01_case_studies.md)에 있습니다.

---

## 12. 어떤 AI 모델을 쓸까 (재질 작업 한정 메모)

- 프런티어 모델(GPT-6 Astra, Claude Fable 5.1, Opus 5.5, Gemini 등)이 셰이더 노드를 만드는 품질을 **정량 비교한 자료는 찾지 못했습니다.** 공개된 모델 비교는 대부분 개인 테스트(n=1)이고 결과가 엇갈립니다.
- 재질 작업은 "코드 작성"보다 **"렌더를 보고 레퍼런스와 비교하는 능력"**이 결과를 가릅니다. Anthropic은 Claude Opus 5.5(2026-09-22)를 "vision과 computer use에 가장 좋은 Opus"라고 소개했습니다(벤더 자체 보고).
- GPT-6 Astra를 Codex로 쓸 때는 reasoning effort가 기본 `low`이므로 비교·실사용 시 effort를 명시하세요.
- 작업 유형별 선택과 비용은 [AI 모델·클라이언트 가이드](01_ai_models_and_clients.md)를, 시각 루프 설계는 [에이전트 워크플로 가이드](09_agent_workflow_prompting.md)를 보세요.

---

## 13. 한국 사용자 체크리스트

- [ ] **Hunyuan3D를 로컬로 쓰지 않는다.** [Hunyuan3D-2.1 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE) 원문: "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA". Territory 정의에서 제외되고, 5(c)항은 **출력물(Output)**도 Territory 밖에서 쓰지 못하게 합니다. 해외 서버에서 생성한 결과를 한국에서 쓰는 경우도 해당합니다. [Hunyuan3D-2(2.0) LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE)도 같아서 ahujasid 서버의 Hunyuan 연동과 PR #343에도 적용됩니다. 정확히는 "법으로 금지"가 아니라 "라이선스가 부여되지 않아 무단 사용이 되는 것"입니다. Tencent Cloud API 약관은 별개이며 원문을 확인하지 못했습니다. Hunyuan3D 2.5는 2025-06-23에 기술 보고서만 공개됐습니다.
- [ ] **대안**: TRELLIS.2(MIT, 단 nvdiffrast 비상업), MV-Adapter(Apache-2.0, diffuse만), StableGen + Marigold/StableDelight, PBRify(CC0), 클라우드 Meshy·Tripo(유료 플랜). Step1X-3D는 Apache-2.0이지만 텍스처 모듈에 Hunyuan 파생 코드가 있어 텍스처 단계는 법률 검토 전 보류합니다.
- [ ] **연구 전용을 상업에 섞지 않는다**: CHORD(Research-Only), VLMaterial 데이터(CC BY-NC), Material Anything(Text2Tex CC BY-NC-SA 설정·가중치 미확인), PartUV의 PartField(비상업).
- [ ] **한국어 UI**: 새로 만든 노드 이름이 번역될 수 있어 `nodes['Principled BSDF']`가 깨집니다. 이 문서 코드처럼 type으로 찾고, 에이전트용 Blender에서는 Preferences > Interface > Translation의 **New Data**를 끄세요(`bpy.context.preferences.view.use_translate_new_dataname = False`). 자세한 내용은 [Blender MCP 가이드 12절](02_blender_mcp.md).
- [ ] **재질·오브젝트 이름은 영어**로(`MAT_Oak`, `GEO_Chair` 등). [`scene_audit.py`](../03_playbooks/scripts/README.md)의 치수 검사도 영어 키워드로 동작합니다.
- [ ] **실측 치수**: 텍스처 스케일은 실제 크기에 맞춰야 자연스럽습니다. 한국 가구·공간 치수는 [치수 기준표](../03_playbooks/05_reference_dimensions.md)를 쓰세요.
- [ ] 한국어 자료는 [한국어 자료 모음](../04_case_studies/02_korean_resources.md)에 있습니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 새 조명에서 그림자가 이중으로 보이거나 얼룩짐 | albedo에 조명·하이라이트가 구워짐 | Meshy `remove_lighting=true`, StableDelight·Marigold로 de-light, 조명 불변 PBR 모델, 또는 라이브러리 재질로 교체 |
| 이음새, 뷰마다 색·디테일이 다름 | 멀티뷰 불일치(StableGen Separate 모드 등) | Sequential + IPAdapter, 가림을 줄이는 카메라 전략(Greedy Occlusion Coverage, Normal-Weighted K-means), `Discard-Over Angle`, UV Inpaint |
| 다리 안쪽·좌판 아래가 비어 있음 | 카메라에 안 보이는 면 | 카메라 추가, UV Inpaint, 베이크 전 확인 |
| 노멀맵이 "그럴듯한 보라색"인데 요철이 모양과 안 맞음 | 이미지 모델이 데이터 맵을 지어냄 | 이미지 모델에는 albedo만. normal·roughness는 추정기(Marigold·PBRify·DeepBump, 연구용 CHORD)나 height 베이크로 |
| 요철이 뒤집혀 보임 | `nor_dx`(DirectX)를 Blender·glTF에 사용 | `nor_gl` 사용 또는 G 채널 반전 |
| Poly Haven 텍스처가 평평하고 반복 크기가 이상함 | PR #367 이전 버전(normal 미연결, Mapping TEXTURE 모드) | 최신 버전 + 3.2절 점검 스니펫 + Mapping Scale = 표면 크기 ÷ 텍스처 실측 크기 |
| 전체가 너무 매트하거나 노멀이 휨 | 데이터 맵을 sRGB로 읽음 | Non-Color(없으면 `Linear Rec.709`) |
| 뷰포트는 맞는데 렌더는 회색 | Material Output·Principled 중복 | `nodes.clear()` 후 재구성(idempotent), `audit_materials()` |
| `KeyError: 'Specular'` 등 | 3.x 시절 소켓 이름 | `describe_node_type`·`bpy_api_lookup`으로 조회, 4.0 이름 사용 |
| `Node type ShaderNodeTexMusgrave undefined` | 4.1에서 제거 | Noise Texture + `noise_type` |
| 금속이 뿌옇고 싸 보임 | Metallic 0.3~0.8 같은 중간값(Infinigen 레시피를 그대로 복사한 경우 포함) | 0/1로 고치고 전환부만 마스크 |
| 금속이 검게 보임 | 금속 Base Color를 어둡게 설정 | physicallybased 값(대부분 linear 0.5 이상) |
| EEVEE에서 마모가 안 보여 값을 과하게 올림 | Pointiness·Bevel은 Cycles 전용 | Cycles 렌더로 검증, 게임용은 베이크 |
| 마모가 전혀 없거나 온통 벗겨짐 | 엣지 마스크 값 범위가 메시마다 다름 | `measure_edge_signal`로 p80/p99를 재서 임계값 지정(5.3절) |
| 베이크가 일부 재질만 됨 | 활성 이미지 노드가 없는 슬롯은 조용히 건너뜀 | 모든 슬롯에 대상 노드 추가(`bake_pbr`), 결과 이미지 확인 |
| 구운 albedo에 조명이 섞임 | `DIFFUSE`를 기본 pass_filter로 구움 | `pass_filter={'COLOR'}` |
| GLB에서 재질이 흰색·회색 | 절차 노드는 glTF로 안 나감 | 베이크 → `gltf_material` → 8.2절 감사 |
| GLB에 AO가 없음 | `glTF Material Output` 그룹이 없음 | 그룹을 만들고 `Occlusion` 입력에 ORM R 연결 |
| smart_project 결과가 이상함 | `angle_limit`을 도(66.0)로 넣음(오류 없이 잘림) | `math.radians(66)` |
| 4.2 LTS에서 `MINIMUM_STRETCH` 오류 | 4.2에는 SLIM이 없음 | `ANGLE_BASED`·`CONFORMAL`을 쓰거나 5.x 사용 |
| AI 생성 메시에 Smart UV → 섬 수백 개 | 삼각형 수프 | PartUV(라이선스 확인)·SLIM, 룩뎁은 트라이플래너 |
| 텍스처 선명도가 에셋마다 다름 | 텍셀 밀도 불일치 | Texel Density Checker로 통일(6.3절) |
| 같은 의자 10개가 똑같음 | 개체별 변화 없음 | `Object Info > Random` → HSV 변화 |
| MCP 180초 타임아웃, Blender 멈춤 | 고해상도 Poly Haven 다운로드·베이크를 소켓으로 실행 | 1k/2k로 받기, 베이크는 헤드리스(7.4절) |
| Meshy 결과에 albedo만 있음 | `enable_pbr` 기본 false | `enable_pbr=true` |
| Meshy를 8K로 했는데 roughness가 흐림 | PBR 맵은 2K 고정 | 히어로 에셋은 Painter 등에서 보강하거나 2K 기준으로 텍셀 밀도 설계 |
| Blender MCP가 연결되지 않거나 엉뚱한 서버에 연결 | 9876 포트 충돌(공식·ahujasid·Scenario) | 한 번에 하나만. Scenario는 호스티드 MCP |
| Substance Designer가 멈춤·크래시 | 병렬 도구 호출, 잘못된 포트 ID | 순차 호출, 레시피에서 시작해 파라미터만 조정 |
| 한국에서 Hunyuan 텍스처를 상업 에셋에 사용 | 라이선스 지역 제외(출력물 포함) | 13장 대안 사용 |

---

## 관련 문서

- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [교차검증 로그](../01_research/verification_log.md)
- [AI 모델·클라이언트](01_ai_models_and_clients.md): 작업 유형별 모델 선택, 비용
- [Blender MCP 생태계](02_blender_mcp.md): 공식 Blender Lab 서버 vs ahujasid, 보안·텔레메트리, 4.x→5.x API 함정(11절), 한국어 UI(12절)
- [기타 DCC·CAD·엔진 MCP](03_other_mcp_dcc_cad_engines.md): Substance Painter/Designer MCP 설치, RTX Remix, Unreal·Unity 머티리얼
- [AI 3D 생성](04_ai_3d_generation.md): 생성기 비교, 결과물 라이선스, 후처리·고폴리→로폴리 베이크
- [라이팅·렌더·아트디렉션](06_lighting_rendering_art_direction.md): 재질을 판단할 중립 조명, 색관리
- [모델링: 오브젝트·가구·조형](07_modeling_objects_furniture_sculpture.md): 부품 분리(재질 슬롯), 베벨
- [배치·레이아웃](08_scene_layout_placement.md)
- [에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 렌더→비평 루프, 스킬·CLAUDE.md
- [에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md): CC0·Fab·Megascans 조건, glTF 최적화, 한국 법규
- [학술 연구](11_research_papers.md)
- 플레이북: [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수표](../03_playbooks/05_reference_dimensions.md)
- 템플릿: [CLAUDE.md](../03_playbooks/templates/CLAUDE.md) · [스킬 blender-aaa-scene](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- 스크립트: [scene_audit.py · placement_utils.py · review_views.py](../03_playbooks/scripts/README.md)(Blender 4.2.23 LTS·5.0.1 테스트 통과)
- 사례: [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- `01_research/raw/06_texturing-materials.research.json` — 조사 결과(항목 37, 노하우 26, 사례 10, 출처 83)
- `01_research/raw/06_texturing-materials.verify.json` — 독립 검증(판정 25, 항목 점검 23, 신뢰도 낮은 출처 6, 누락 항목 8)
- 검증 반영 요약: 반박 2건(RTX Remix 공식 MCP 존재, blender-kiln 갤러리는 MCP 결과가 아님), 부분 정정 9건(베이크 동작, 텔레메트리 기본값, cc-blender-skill 수치·스킬 수, Hunyuan 2.5 공개 범위, Megascans 표현, Material Anything·PartUV·TRELLIS.2 라이선스 단서, 비금속 albedo 상한, EEVEE AO), 누락 보완 8건(comfy-mcp, RTX Remix MCP, monolith, Step1X-3D, Quartermaster, SAFE_MODE·DISABLE_TELEMETRY, Scenario 호스티드 MCP, Poly Haven ToS)
- 교차 반영: `01_research/raw/12_assets-pipeline-licensing.verify.json`(Step1X-3D 텍스처 모듈의 Hunyuan 헤더·nvdiffrast 의존, Tripo SDK `docs/API.md`와 현행 코드 불일치), `01_research/raw/05_ai-3d-generation.verify.json`(tripo-mcp 마지막 커밋 2025-04-14), `01_research/raw/10_agent-workflow.verify.json`(SAFE_MODE 차단·허용 범위), `01_research/raw/G4_licensing_pricing.verify.json`(Substance Sampler 2024-03-18)
- 신뢰도 낮은 출처로 표시한 것: blender-kiln, cc-blender-skill SKILL.md(값은 교차확인해 사용), dcc-mcp 조직, MaterialPilot. GitHub 이슈 검색 페이지는 근거에서 빼고 Blender 소스로 대체
- 이 문서의 코드·수치 중 "테스트"로 표시한 것은 2026-09-27 pip `bpy` 4.2.23 LTS·5.0.1(헤드리스, Cycles CPU)에서 직접 실행한 결과(개인 테스트, n=1)

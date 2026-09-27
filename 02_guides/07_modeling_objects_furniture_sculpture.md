# 오브젝트·가구·조형물 모델링 가이드: 스펙 우선으로 '맞는 형태' 만들기

> 기준일: 2026-09-27 · AI가 만든 가구가 그럴듯해 보이는지는 모델보다 순서에서 갈립니다. 치수 스펙(JSON) → 부품 코드 → 숫자 검사 → 렌더 검사 순서로 만들고, 부품 분해·모디파이어 스택·조립 방식은 프로젝트 규칙 파일에 고정하세요.

> [!IMPORTANT]
> **한국 사용자가 먼저 확인할 것**
>
> - **치수는 지역 프리셋으로 넣으세요.** 한국 아파트 천장고는 구축 2,300 mm, 2020년대 신축 2,400~2,500 mm입니다. 싱크대 높이는 850 mm(최근 900 mm 권장도 있음)이고 미국은 914 mm입니다. 매트리스 'K'는 한국 1,600~1,670 mm, 미국 King 1,930 mm, 영국 King 1,500 mm로 나라마다 다릅니다. 그래서 AI에게는 이름 대신 **mm 값**을 주세요. 한국 방문 900×2100은 **문틀 기준**이고 문짝은 약 60 mm 작습니다. 공동주택 공용계단은 높이 **2 m 이내마다 계단참**을 둬야 합니다(3 m가 아님). 자세한 값은 [치수 기준표](../03_playbooks/05_reference_dimensions.md)에 있습니다.
> - **파트 생성 모델 라이선스를 확인하세요.** [Hunyuan3D-Part 라이선스](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-Part/main/LICENSE)는 "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"라고 명시합니다. 한국에서 로컬로 쓰면 라이선스 범위 밖이고, 출력물 사용도 제한됩니다. 검증 에이전트는 ahujasid MCP for Blender의 Hunyuan3D 연동도 같은 문제를 안고 있다고 봤습니다. Tencent Cloud API 약관은 별개이며 (미확인)입니다. [PartPacker](https://raw.githubusercontent.com/NVlabs/PartPacker/main/license.md)는 비상업 연구 전용입니다. 이 문서에 나오는 연구 코드(LL3M, CAD-Recode, Text2CAD, LLaMA-Mesh, ShapeAssembly)도 **상업 사용이 금지**되어 있습니다([8장](#8-연구에서-얻은-교훈)).
> - **한국어 UI에서는 이름으로 찾는 코드가 깨질 수 있습니다.** 현지화 UI에서는 새로 만든 노드 이름이 번역됩니다(일본어 UI 실패 사례가 확인됨). 노드는 `type`으로 찾고, 오브젝트 이름은 만들 때 영어로 직접 지정하세요. [scene_audit.py](../03_playbooks/scripts/README.md)의 치수 규칙은 `chair`, `table` 같은 **영어 이름 키워드**로 동작합니다.

## 핵심 요약

- **품질은 파이프라인이 좌우합니다.** 먼저 부품별 치수 명세(JSON)를 만들고, 부품 단위 코드로 짓고, 결정적 검사(치수·접촉·관입·manifold)를 통과시킨 다음, 마지막에 렌더로 눈 검사를 합니다. [build123d-mcp 프롬프트](https://raw.githubusercontent.com/pzfreo/build123d-mcp/main/default_prompt.md)는 이 순서를 "deterministic checks before visual"로 규칙화했고, [blender-image-to-3d 스킬](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/SKILL.md)은 "Render evidence at every gate"를 규칙으로 둡니다.
- **씬 규약을 먼저 고정하세요.** 1 unit = 1 m, Z-up, 앞면 -Y, 원점은 바닥 접점, 스케일·회전 적용, 영어 부품 이름(`chair_leg_FL`)을 씁니다. 스케일을 적용하지 않으면 bevel·solidify 폭이 축마다 달라집니다.
- **접근법은 대상에 맞춰 고르세요.** 일반 가구는 bpy 프리미티브·bmesh와 모디파이어로 만듭니다. 조인트·하드웨어처럼 mm 정밀도가 필요하면 build123d, CadQuery, OpenSCAD를 MCP로 씁니다. 변형이 많이 필요하면 Infinigen, Archimesh, Geometry Nodes를 씁니다. 유기 조형은 SDF·메타볼·볼륨이나 AI image-to-3D로 만든 뒤 remesh합니다. 배경 소품은 에셋 라이브러리에서 가져오세요.
- **부품을 빼먹지 않으려면 부품 어휘를 주세요.** [PartNet 계층](https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Chair-hier.txt)(chair_back / chair_seat / chair_base → leg, bar_stretcher, runner…)을 체크리스트로 주면 스트레처, 에이프런, 등받이 연결재 같은 부품의 누락이 줄어듭니다. 두께도 숫자로 줍니다. 예를 들어 판재는 18 mm, 뒤판은 3~6 mm, 문·서랍 틈은 2~3 mm입니다.
- **'분해된 의자'는 조립 규칙으로 막습니다.** [ProfRino Assembly Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill)의 규칙은 다음과 같습니다. 코드를 쓰기 전에 연결 맵을 만들고, 큐브는 `size=2`로 만들어 scale이 half-extent와 같게 하고, 두 점을 잇는 부재는 Euler 회전 대신 bmesh로 만들고, 연결부는 최소 5 mm 겹칩니다. 이 문서의 [검사 코드](#24-결정적-검사-숫자가-먼저)는 연결 맵을 받아 틈(GAP), 계획에 없는 관통, 바닥과 이어지지 않은 부품(DETACHED)을 잡습니다. Blender 4.2.23 LTS와 5.0.1에서 동작을 확인했습니다.
- **모디파이어 순서.** transform apply → Mirror → Array → (Solidify) → Boolean → Bevel → (SubSurf) → Weighted Normal(맨 끝) 순서입니다. 제조 모서리에는 bevel을 반드시 넣습니다. 폭은 원목 1~3 mm이고, 크기를 모르면 최대 치수의 0.5%로 둡니다. **Boolean solver 이름이 버전마다 다릅니다**(4.2는 `FAST/EXACT`, 5.0은 `FLOAT/EXACT/MANIFOLD`). 이 문서를 쓰면서 직접 확인했으므로, 런타임에 enum을 읽어서 고르세요.
- **조형물은 버텍스를 직접 만지지 마세요.** SDF smooth union, 메타볼, Mesh to Volume으로 형태를 잡고 voxel remesh(0.003~0.01 m) → Multires/Displace → Decimate → bake 순서로 마감합니다. 받침대처럼 제작된 부재는 하드서피스로 따로 만듭니다.
- **연구에서 나온 공통 교훈.** 코드는 편집 가능한 3D 표현이고, 렌더 기반 VLM 검증 루프가 정확도를 올리며, 생성과 검증을 분리하고 검증에 연산을 더 쓰면 좋아집니다(LL3M, CADCodeVerify, CADFusion, BlenderGym, Procedura). 메시를 텍스트로 직접 뽑는 방식(LLaMA-Mesh 등)은 아직 저폴리 수준입니다.
- **2026-09 사례는 대부분 작성자 자기 보고입니다.** kitchen-twin(GPT-6 Astra, 에셋 32개·조인트 138개), IKEA 의자 한 장 → 분해도·조립, Tom Krcha 기관차(오브젝트 3,295개)가 대표 사례입니다. 저자들 스스로 "얇고 반짝이는 것은 아직 약하다", "순진한 프롬프트는 실패하고 전문가가 쓴 체계적 프롬프트가 성공한다"고 적었습니다. 독립적으로 검증된 'AAA급' AI+MCP 가구 결과물은 찾지 못했습니다. 현실적인 목표는 [스펙 + 코드 + 검사 루프 + 사람의 마무리]입니다.

---

## 1. 왜 AI 가구는 '어딘가 이상해' 보이나

원자료에서 반복해서 나온 실패는 여섯 종류로 묶입니다. 모두 모델을 바꾸는 것보다 규칙과 검사로 잡는 편이 쌉니다.

| 증상 | 대표 원인 | 이 문서의 대응 |
|---|---|---|
| 스케일·비율이 틀림(의자가 식탁보다 높음, 소파 깊이 2.5 m) | LLM이 절대 치수와 관계 치수를 추측함 | 치수 스펙 + 관계식 + [scene_audit.py](../03_playbooks/scripts/README.md) 치수 규칙 (2.2절) |
| 부품이 떠 있거나 서로 파고듦("분해된 의자") | 코드 안에서 좌표를 즉흥 계산, 큐브 크기 규약 혼동, 실린더 회전 오류 | 연결 맵 + 조립 헬퍼 + `check_assembly()` (2.4절, 6장) |
| 부품 누락(스트레처·에이프런·뒤판 없음) | 부품 어휘가 없음 | PartNet 계층 체크리스트 (5장) |
| 판이 종이처럼 얇거나 각재가 너무 굵음 | 두께를 지정하지 않음 | 현실적인 두께 표 (5.2절) |
| 모서리가 칼날 같아 CG 티가 남 | bevel 누락, 스케일 미적용 상태의 bevel | 모디파이어 스택 (4장) |
| 형태가 울퉁불퉁하거나 깨짐(조형물) | 버텍스를 직접 조작 | SDF·볼륨·remesh 경로 (7장) |

---

## 2. 스펙 우선 파이프라인

```text
[0 규약] → [1 치수 스펙] → [2 부품 스펙 JSON] ─(사람 승인)→ [3 부품 코드]
      → [4 결정적 검사: check_assembly + scene_audit] ─FAIL→ 3으로
      → [5 렌더 검사: 4방향 렌더 + 인체 더미 + 예/아니오 질문 + (레퍼런스가 있으면) IoU] ─결함→ 결함 원장 → 3으로
      → [6 마감: 재질·UV·베이크] → [7 익스포트 검사]
```

| 단계 | 산출물 | 통과 기준 | 도구·근거 |
|---|---|---|---|
| 0 규약 | CLAUDE.md/AGENTS.md 규칙 | 단위·축·원점·이름 규칙이 문서화됨 | [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) |
| 1 치수 스펙 | 전체 bbox와 관계 치수 | 지역 기준표 범위 안 | [Holodeck 프롬프트](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py)의 "[L, W, H] cm 먼저" 패턴, [치수 기준표](../03_playbooks/05_reference_dimensions.md) |
| 2 부품 스펙 | parts / connections / checks JSON | PartNet 계층 대비 누락 이유 기록, 사람 승인 | [PartNet](https://github.com/daerduoCarey/partnet_dataset), [ShapeAssembly](https://github.com/rkjones4/ShapeAssembly)의 cuboid + attach 발상 |
| 3 부품 코드 | 부품당 오브젝트 1개 | 호출 1회 = 부품 1개, 재실행해도 결과 같음 | 아래 헬퍼, [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) `execute_blender_code` |
| 4 결정적 검사 | 문제 목록 | `check_assembly()` 빈 목록, scene_audit에서 형태 관련 issue 0 | 2.4절, [scene_audit.py](../03_playbooks/scripts/README.md) |
| 5 렌더 검사 | top/front/side/persp 렌더 | 예/아니오 질문 전부 "예", 결함 원장 해결 | [review_views.py](../03_playbooks/scripts/README.md), [CADCodeVerify](https://github.com/Kamel773/CAD_Code_Generation) 방식 |
| 6~7 마감·익스포트 | 재질·UV·LOD | [품질 체크리스트](../03_playbooks/04_quality_checklists.md) | [05 텍스처링](05_texturing_materials.md), [10 파이프라인](10_assets_pipeline_licensing.md) |

### 2.1 씬 규약 (프로젝트 규칙 파일에 고정)

- `scene.unit_settings.system='METRIC'`, `scale_length=1.0`. 1 unit = 1 m이고 Z-up입니다.
- 가구 **앞면은 -Y**입니다. 이 저장소 스크립트(`placement_utils.face_towards`)와 [blender-image-to-3d 스킬](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/SKILL.md)(-Y forward)이 같은 규약을 씁니다.
- 가구 하나는 **Empty 루트 하나 아래에 부품을 자식으로** 둡니다(`dining_chair_ROOT`). 루트 원점은 바닥 중심입니다. scene_audit.py는 최상위 부모를 한 '유닛'으로 봅니다. 부모 없이 부품이 흩어져 있으면 좌판이 "떠 있음"으로 나옵니다.
- 부품 이름은 `<category>_<part>_<pos>` 형식입니다(`chair_leg_FL`, `table_apron_front`). 컬렉션은 GEO / CUTTERS / REF로 나누고, 커터와 레퍼런스는 렌더와 뷰포트에서 모두 숨깁니다. [validate.py](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/scripts/validate.py)는 `.001` 같은 숫자 접미사에 경고를 냅니다.
- 모델링이 끝나면 `bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)`를 실행합니다. 음수 스케일을 적용한 뒤에는 노멀을 다시 계산합니다.
- 세션을 시작할 때 `bpy.app.version_string`을 확인하고 버전을 프롬프트에 적습니다. `use_auto_smooth`는 4.1에서 제거됐고 Boolean solver 이름은 5.0에서 바뀌었습니다([02 Blender MCP](02_blender_mcp.md)의 API 함정 표 참고).

### 2.2 치수 스펙: 전체 크기 → 관계 → 부품

1. **전체 bbox부터 답하게 합니다.** Holodeck은 LLM에게 오브젝트 크기를 `[length, width, height]` cm로 먼저 적게 합니다(예: sofa [200, 100, 80]). 이 값을 기준표로 검사한 다음 모델링 코드에 넘깁니다.
2. **관계 치수로 묶습니다.** 가구를 따로따로 만들면 서로 어울리지 않는 조합이 나옵니다.
   - 좌판 높이 = 식탁 상판 높이 − 250~305 mm
   - 스툴 좌판 = 카운터 높이 − 250~300 mm (한국 850 mm 조리대라면 약 550~620 mm, 계산값)
   - 협탁 상단 ≈ 매트리스 윗면 ± 50 mm
   - 커피테이블 ≈ 소파 좌판 − 25~50 mm
   - 팔걸이 의자는 팔걸이 윗면이 에이프런 아래로 들어가는지 확인합니다.
3. **범위로 저장하고 조금씩 흔듭니다.** 모든 의자를 정확히 450 mm로 만들면 오히려 CG처럼 보입니다. 430~480 mm처럼 범위를 저장하고 그 안에서 값을 약간씩 다르게 줍니다.

**핵심 수치 요약** (mm, 상세와 출처는 [치수 기준표](../03_playbooks/05_reference_dimensions.md))

| 항목 | 한국 | 미국/글로벌 | 메모 |
|---|---|---|---|
| 식탁 상판 높이 | 720~750 | 711~762 (28~30 in) | 상판−좌판 250~305가 가장 중요한 관계식 |
| 식탁 의자 좌판 높이 | 430~460 | 430~480 | [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions) 등 |
| 사무용 책상 | 720 (KS G 4203 관행) | 737~762 | |
| 조리대(싱크대) | 850 (신규 900 권장도 있음) | 914 (36 in) | 한국 주방 모듈 850 + 700 + 750 ≈ 2,300 ([LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596)) |
| 상하부장 간격 | 650~750 | 457 (18 in) | 지역을 섞으면 한 공간 안에서 모순이 생깁니다 |
| 천장고 | 구축 2,300 / 신축 2,400~2,500 | 2,438 (8 ft)가 흔함 | 신축이 높아지는 추세([서울경제TV](https://www.sentv.co.kr/article/view/sentv202209140082)) |
| 매트리스 폭×길이 | S 1000·SS 1100·Q 1500 × 2000, K 1600~1670 × 2000~2075, LK 1700~1800 × 2000~2075 | Queen 1524×2032, King 1930×2032 | K 이상은 브랜드마다 다릅니다([소비자가 만드는 신문](https://www.consumernews.co.kr/news/articleView.html?idxno=520936)) |
| 방문 | 900×2100 (문틀 기준, 문짝은 약 60 작음) | 813×2032 (미확인 관행) | DIN 18101 문짝 860×1985이면 벽 개구부는 약 885×2010([BauNetz Wissen](https://www.baunetzwissen.de/fenster-und-tueren/fachwissen/konstruktion-funktion/tuerblattgroessen-nach-din-18101-155263)). 벽 boolean에는 **개구부 치수**를 씁니다 |
| 계단 | 공동주택 공용: 단높이 ≤180, 단너비 ≥260, 유효폭 ≥1,200, **2 m 이내마다 계단참** | IRC: 단높이 ≤197, 디딤판 ≥254 (보완 검증에서 재확인하지 못함) | 2R+T = 620~640이 편안함([FreeCAD ArchStairs](https://raw.githubusercontent.com/FreeCAD/FreeCAD/main/src/Mod/BIM/ArchStairs.py)). 한국 근거: [주택건설기준 등에 관한 규정](https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=268503) |
| 책장·옷장 | — | IKEA [BILLY](https://www.ikea.com/us/en/cat/billy-series-28102/) 깊이 280(유리문 300), [PAX](https://www.ikea.com/gb/en/customer-service/knowledge/articles/4dc0cd26-geg1-487c-gee0-43g399373g9f.html) 깊이 580(또는 350) | PAX 높이 2,360은 한국 구축 천장고 2,300에 들어가지 않습니다(신축 2,400 이상이면 가능) |
| 인체 더미 | 남 1,725 / 여 1,596 | — | [사이즈코리아 제8차](https://sizekorea2022.kr/8th_results/)(2022-03 발표, 20~69세 6,839명) |

> [!CAUTION]
> **Infinigen 치수를 "표준"으로 쓰지 마세요.** [Infinigen ChairFactory](https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/seating/chairs/chair.py)는 leg_height를 0.45~0.5에서 샘플링합니다. 그런데 좌판이 두께 중앙 기준으로 놓이기 때문에 **좌판 윗면은 약 0.47~0.54 m**가 되어 표준 좌면(0.43~0.46 m)보다 높습니다. 식탁 높이 범위(0.65~0.85)도 넓습니다. 이 값들은 실측 데이터가 아니라 설계자가 정한 랜덤 범위입니다. **부품 구조의 참고로만** 쓰세요(검증 결과 반영).

### 2.3 부품 스펙 JSON (코드보다 먼저, 사람이 승인)

LLM이 좌표를 코드 안에서 즉흥적으로 계산하면 부품이 떠 있거나 파고드는 일이 잦습니다. 명세 단계에서 치수표 검사와 부품 누락 검사를 먼저 하면 코드 단계 오류가 줄어듭니다. Holodeck의 "크기 먼저", ShapeAssembly의 cuboid + attach, kitchen-twin의 "작은 Blender 모델링 언어"가 같은 원리입니다.

아래 스펙은 한국 식탁 의자 예시입니다. 좌판 윗면 0.45 m, 전체 높이 0.84 m입니다. `connections`가 **연결 맵**이고, 설계상 붙어 있어야 하는 부품 쌍을 적습니다. 이 JSON은 2.4절 코드로 그대로 빌드하고 검사할 수 있습니다.

```json
{
  "name": "dining_chair_ROOT", "region": "KR", "units": "m", "up": "Z", "front": "-Y",
  "parts": [
    {"name": "chair_seat", "type": "box", "size": [0.44, 0.42, 0.03], "center": [0, 0, 0.435]},
    {"name": "chair_leg_FL", "type": "box", "size": [0.035, 0.035, 0.42], "center": [-0.2025, -0.1925, 0.21]},
    {"name": "chair_leg_FR", "type": "box", "size": [0.035, 0.035, 0.42], "center": [0.2025, -0.1925, 0.21]},
    {"name": "chair_leg_BL", "type": "box", "size": [0.035, 0.035, 0.42], "center": [-0.2025, 0.1925, 0.21]},
    {"name": "chair_leg_BR", "type": "box", "size": [0.035, 0.035, 0.42], "center": [0.2025, 0.1925, 0.21]},
    {"name": "chair_back_post_L", "type": "box", "size": [0.035, 0.035, 0.39], "center": [-0.2025, 0.1925, 0.645]},
    {"name": "chair_back_post_R", "type": "box", "size": [0.035, 0.035, 0.39], "center": [0.2025, 0.1925, 0.645]},
    {"name": "chair_back_rail", "type": "box", "size": [0.37, 0.02, 0.08], "center": [0, 0.1925, 0.80]},
    {"name": "chair_stretcher_L", "type": "rod", "p0": [-0.2025, -0.18, 0.15], "p1": [-0.2025, 0.18, 0.15], "radius": 0.01},
    {"name": "chair_stretcher_R", "type": "rod", "p0": [0.2025, -0.18, 0.15], "p1": [0.2025, 0.18, 0.15], "radius": 0.01}
  ],
  "connections": [
    ["chair_seat", "chair_leg_FL"], ["chair_seat", "chair_leg_FR"], ["chair_seat", "chair_leg_BL"], ["chair_seat", "chair_leg_BR"],
    ["chair_seat", "chair_back_post_L"], ["chair_seat", "chair_back_post_R"],
    ["chair_back_post_L", "chair_back_rail"], ["chair_back_post_R", "chair_back_rail"],
    ["chair_leg_FL", "chair_stretcher_L"], ["chair_leg_BL", "chair_stretcher_L"],
    ["chair_leg_FR", "chair_stretcher_R"], ["chair_leg_BR", "chair_stretcher_R"]
  ],
  "checks": {"seat_top_z": [0.43, 0.46], "overall_z": [0.80, 0.95]},
  "omitted": {"chair_arm": "식탁 의자라 생략", "chair_back_connector": "등받이 기둥이 가로대를 직접 받침"}
}
```

- 스트레처(`rod`)는 다리 안쪽 면에서 **5 mm 안으로** 들어가도록 끝점을 잡았습니다(다리 안쪽 면 y = ±0.175, 끝점 y = ±0.18). 계획된 겹침입니다.
- 스펙을 만들 때 AI에게 "PartNet 계층 중 무엇을 쓰고 무엇을 생략했는지 이유와 함께 적으라"고 시키세요(`omitted`). 그리고 **사람이 승인한 다음에** 코드를 쓰게 합니다.

### 2.4 결정적 검사: 숫자가 먼저

[build123d-mcp 규칙](https://raw.githubusercontent.com/pzfreo/build123d-mcp/main/default_prompt.md)은 "(1) execute() 후마다 measure(), (2) 조립 위치를 잡은 뒤 compare(), (3) 둘 다 통과한 뒤에만 render_view()" 순서를 씁니다. VLM의 시각 판단은 mm 단위 오류와 숨은 관입을 놓치기 때문입니다.

이 저장소의 검사는 두 층으로 나뉩니다.

| 층 | 도구 | 잡는 것 | 못 잡는 것 |
|---|---|---|---|
| **부품 단위**(가구 하나 안) | 아래 `check_assembly()` (이 문서 전용) | 연결 맵 기준 틈(GAP), 과도한 겹침(TOO_DEEP), 계획에 없는 관통, 바닥과 이어지지 않은 부품(DETACHED) | 모서리끼리만 스치는 접촉(정점-면 거리 기반), 완전 내포 |
| **유닛 단위**(가구끼리, 가구와 바닥) | [scene_audit.py](../03_playbooks/scripts/README.md) (테스트 완료) | 떠 있음(바닥 근처 5점 레이), 바닥 아래로 박힘, 유닛 간 관통, 스케일 미적용·음수, non-manifold, 재질·UV 없음, 이름 키워드별 치수 범위 이탈 | 같은 유닛 안의 부품끼리 관통(설계상 의도한 결합과 구분할 수 없으므로 일부러 제외) |

> 원자료의 50줄 검사 예시는 bbox 중심에서 아래로 레이를 한 줄만 쏩니다. 그래서 다리 위의 좌판이나 상판처럼 **중심 아래가 비어 있는 부품을 거의 항상 FLOATING으로 오탐**합니다(검증에서 지적됨). 이 저장소는 대신 두 가지 방식을 씁니다. scene_audit.py는 유닛을 묶어 여러 점에서 레이를 쏘고, `check_assembly()`는 BVH 최소 거리와 연결 그래프로 판정합니다. `BVHTree.overlap`이 한 물체가 다른 물체 안에 완전히 들어간 경우를 못 잡는다는 한계는 두 방식 모두에 남아 있습니다.

**코드 A. 조립 헬퍼 + 스펙 빌드 + 연결 맵 검사.** 이 문서를 쓰면서 Blender 4.2.23 LTS와 5.0.1(pip `bpy`, 헤드리스)에서 실행해 확인했습니다. `asm_helpers.py`로 저장해서 쓰세요.

```python
import bpy, bmesh
from itertools import combinations
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree


def _link(ob, parent):
    bpy.context.scene.collection.objects.link(ob)
    if parent is not None:
        ob.parent = parent  # 부모 Empty는 원점·무회전·스케일 1로 둔다


def box(name, size, center, parent=None):
    """size=(x, y, z) 전체 치수(m). 치수는 메시에 굽고 오브젝트 scale은 1로 유지한다."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_cube(bm, size=1.0, calc_uvs=True)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = center
    _link(ob, parent)
    return ob


def rod(name, p0, p1, radius, segments=16, parent=None):
    """두 점 사이 원기둥. Euler 회전 없이 정점을 직접 방향에 맞춘다."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, calc_uvs=True,
                          radius1=radius, radius2=radius, depth=d.length)
    rot = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation((p0 + p1) / 2) @ rot, verts=bm.verts)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    _link(ob, parent)
    return ob


def build_from_spec(spec):
    root = bpy.data.objects.new(spec["name"], None)  # Empty = 유닛 루트(바닥 중심)
    bpy.context.scene.collection.objects.link(root)
    for p in spec["parts"]:
        if p["type"] == "box":
            box(p["name"], p["size"], p["center"], root)
        elif p["type"] == "rod":
            rod(p["name"], p["p0"], p["p1"], p["radius"], parent=root)
    return root


def check_assembly(root, connections, floor_z=0.0, contact_tol=0.001, max_overlap=0.015):
    """connections: 설계상 붙어야 하는 부품 쌍 [(a, b), ...] = connection map."""
    dg = bpy.context.evaluated_depsgraph_get()
    parts = [o for o in root.children_recursive if o.type == 'MESH']
    T, P, BB = {}, {}, {}
    for o in parts:
        bm = bmesh.new()
        bm.from_object(o, dg)
        bm.transform(o.matrix_world)
        T[o.name] = BVHTree.FromBMesh(bm)
        P[o.name] = [v.co.copy() for v in bm.verts]
        BB[o.name] = (Vector([min(v[i] for v in P[o.name]) for i in range(3)]),
                      Vector([max(v[i] for v in P[o.name]) for i in range(3)]))
        bm.free()

    def relation(a, b):
        (amin, amax), (bmin, bmax) = BB[a], BB[b]
        depth = min(min(amax[i], bmax[i]) - max(amin[i], bmin[i]) for i in range(3))
        if depth < -0.05:
            return "far", -depth
        if T[a].overlap(T[b]):
            return "overlap", max(depth, 0.0)
        g = min(min(T[b].find_nearest(p)[3] for p in P[a]),
                min(T[a].find_nearest(p)[3] for p in P[b]))
        return ("contact", g) if g <= contact_tol else ("gap", g)

    names = [o.name for o in parts]
    planned = {frozenset(c) for c in connections}
    rel = {frozenset((a, b)): relation(a, b) for a, b in combinations(names, 2)}
    problems = []
    for key in planned:
        kind, v = rel[key]
        a, b = sorted(key)
        if kind in ("gap", "far"):
            problems.append(f"GAP {a}-{b} {v * 1000:.1f}mm")
        elif kind == "overlap" and v > max_overlap:
            problems.append(f"TOO_DEEP {a}-{b} {v * 1000:.1f}mm")
    for key, (kind, v) in rel.items():
        if kind == "overlap" and key not in planned:
            a, b = sorted(key)
            problems.append(f"UNPLANNED_PENETRATION {a}-{b}")
    # 바닥에 닿은 부품에서 출발해 '실제로 붙은' 연결만 따라가며 도달 여부 확인
    linked = {n: set() for n in names}
    for key, (kind, v) in rel.items():
        if kind in ("contact", "overlap"):
            a, b = tuple(key)
            linked[a].add(b)
            linked[b].add(a)
    seen = [n for n in names if BB[n][0].z <= floor_z + contact_tol]
    stack = list(seen)
    while stack:
        for m in linked[stack.pop()]:
            if m not in seen:
                seen.append(m)
                stack.append(m)
    problems += [f"DETACHED {n}" for n in names if n not in seen]
    return problems
```

**사용 예(MCP 또는 헤드리스).** `execute_blender_code`는 호출할 때마다 새 네임스페이스에서 실행되므로 파일을 import하는 방식이 편합니다([scripts README](../03_playbooks/scripts/README.md)와 같은 방식).

```python
import sys, json, importlib
import bpy
from mathutils import Vector
sys.path.append(r"C:\path\to\helpers")                      # asm_helpers.py 저장 위치
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")
import asm_helpers as A, scene_audit
importlib.reload(A)

SPEC = json.load(open(r"C:\path\to\dining_chair.spec.json", encoding="utf-8"))
root = A.build_from_spec(SPEC)
print(A.check_assembly(root, SPEC["connections"]))           # [] 이면 통과
seat = bpy.data.objects["chair_seat"]
top = max((seat.matrix_world @ Vector(c)).z for c in seat.bound_box)
lo, hi = SPEC["checks"]["seat_top_z"]
print("seat_top", round(top, 3), lo <= top <= hi)
print(scene_audit.audit_scene(floor_z=0.0)["summary"])
```

- 확인한 결과는 다음과 같습니다. 위 스펙으로는 `[]`가 나옵니다. 좌판 윗면은 0.45로 범위 안이고, scene_audit에서는 유닛 1개(0.44×0.42×0.84 m)가 바닥에 지지된 것으로 나오며 issue는 `no_material`뿐입니다. 등받이 가로대를 앞으로 4 cm 옮기면 `['GAP chair_back_post_L-chair_back_rail 12.5mm', 'GAP chair_back_post_R-chair_back_rail 12.5mm', 'DETACHED chair_back_rail']`가 나옵니다. 좌판을 20 mm 내리면 다리 4개가 `TOO_DEEP ... 20.0mm`로 잡힙니다. 연결 맵에 없는 쌍이 겹치면(예: 쿠션이 등받이 기둥을 뚫음) `UNPLANNED_PENETRATION`이 나옵니다.
- `BLENDER_MCP_SAFE_MODE=1`은 `open()`·`os` 같은 **직접** 파일 I/O를 막으므로 `json.load(open(...))`가 차단되고, `sys.path` 추가 후 import가 되는지는 (미확인)입니다(bpy를 통한 저장·렌더·import/export는 허용). 그 경우 코드 A와 SPEC dict를 그대로 붙여 넣으세요. blend-ai는 샌드박스가 `os`, `sys`, `pathlib`, `open`, `eval` 등 25개 import와 builtin을 막으므로 파일 import 방식은 동작하지 않습니다. 붙여 넣기 방식이 그 샌드박스에서 동작하는지는 (미확인)입니다.
- 원자료의 다른 검사 로직도 재사용할 수 있습니다. [3D Print Toolbox](https://raw.githubusercontent.com/blender/blender-addons/main/object_print3d_utils/mesh_helpers.py)의 기본값은 thickness_min 0.001, threshold_zero 0.0001, 왜곡 45°, 날카로움 160°, 오버행 45°입니다. 가구에서는 **thickness_min을 0.005~0.01로 올리면** 종이처럼 얇은 판을 잡을 수 있습니다. 두께 검사는 노멀이 올바르다는 전제가 필요합니다. [blender-image-to-3d validate.py](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/scripts/validate.py)는 음수 스케일·tri budget·UV 누락을 **FAIL**로, 미적용 scale/rotation(1e-4 초과)은 **WARN**으로 처리합니다. 원자료 요약은 "미적용 스케일도 실패"라고 적었지만 검증에서 WARN으로 정정됐습니다.

### 2.5 렌더 검사: 눈은 숫자 다음

1. **4방향 렌더.** [review_views.py](../03_playbooks/scripts/README.md)로 위·정면·측면 정사영과 3/4 원근을 렌더합니다. 오브젝트마다 다른 색이 칠해져 틈과 겹침이 잘 보입니다. 한국 기준 인체 더미(1.725 m / 1.596 m)와 문틀(2.1 m)을 임시로 넣고, 최종 렌더 전에 숨깁니다.
2. **예/아니오 질문으로 비평시킵니다([CADCodeVerify](https://github.com/Kamel773/CAD_Code_Generation), ICLR 2025).** "잘 됐는지 봐 줘"라고 하면 VLM이 관대하게 통과시킵니다. 질문을 먼저 만들게 하고, 각 질문에 근거와 함께 답하게 한 뒤, "아니오" 항목만 수치가 들어간 수정 지시로 바꿉니다(프롬프트는 [13장](#13-프롬프트-예시)).
3. **레퍼런스 사진이 있으면 실루엣을 수치로 비교합니다.** [blender-image-to-3d](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/SKILL.md)의 게이트는 블록아웃 단계 IoU ≥ 0.85·폭 오차 ±0.05·비율 오차 5% 이내, 형태 단계 IoU ≥ 0.90·±0.03·2% 이내입니다. [world_gate.py](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/scripts/world_gate.py)는 10개 밴드의 폭 프로파일과 ref_only(누락)·render_only(여분) 비율을 계산해서, "3 cm 짧음"이나 "축에서 2 cm 벗어남"도 IoU 손실로 드러나게 합니다. [cc-blender-skill reference-analysis-validator](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/reference-analysis-validator/SKILL.md)는 강체 IoU ≥ 0.90, bbox 크기 드리프트 ≤ 3%, 주요 부품 수 정확히 일치를 기준으로 둡니다. 같은 종류끼리만 비교하세요. 와이어프레임 마스크와 셰이딩 렌더를 비교하면 IoU가 낮게 나옵니다.
4. **사진에서 스케일을 잡을 때는 카메라부터 맞춥니다.** [blender-production](https://raw.githubusercontent.com/per-simmons/blender-production/master/SKILL.md)의 규칙은 "Solve camera/lens before deforming geometry to fit a photograph"입니다. 문 높이 같은 알려진 치수 하나를 앵커로 삼고, 불확실한 치수는 `[uncertain]`으로 표시합니다.

### 2.6 결함 원장: 한 번에 하나만 고칩니다

[blender-production](https://raw.githubusercontent.com/per-simmons/blender-production/master/SKILL.md)은 위치/뷰, 결함, 증거, 추정 원인, 변경, 검증의 6개 필드를 가진 작은 원장을 쓰게 하고, "Do not claim ... completion without evidence"를 규칙으로 둡니다. 결함을 조명이나 재질로 가리지 말고 원인을 고친 다음 **같은 카메라**로 다시 렌더해 비교합니다.

| # | view | defect | evidence | cause | change | verify |
|---|---|---|---|---|---|---|
| 1 | side | 등받이 가로대가 기둥에서 떨어져 있음 | `GAP chair_back_post_L-chair_back_rail 12.5mm` | center.y 계산 오류 | y = 기둥 중심 y | check_assembly `[]`, 같은 카메라로 재렌더 |

---

## 3. 접근법 선택

### 3.1 대상별 선택표

| 대상 | 1순위 | 대안 | 고르는 이유 | 주의 |
|---|---|---|---|---|
| 일반 가구(각재·판재: 의자, 식탁, 책장) | bpy/bmesh 부품 + 모디파이어 스택 (MCP 또는 헤드리스) | Infinigen 생성 결과를 구조 참고로 | 편집 가능하고, 파라미터만 바꿔 반복 수정 가능 | 스케일 적용 후 bevel, 연결 맵 필수 |
| 조인트·하드웨어·기구(장부, 도브테일, 레일, 힌지) | build123d + [build123d-mcp](https://github.com/pzfreo/build123d-mcp) | CadQuery, OpenSCAD + BOSL2 | mm 정확도와 간섭 검사가 도구에 들어 있음 | 기본 단위 mm. Blender로 가져와 bevel·UV·재질 |
| 변형이 많은 세트·건축 요소(문, 창, 계단, 주방) | [Archimesh](https://github.com/blender/blender-addons/tree/main/archimesh), [Infinigen](https://github.com/princeton-vl/infinigen) | Geometry Nodes, [Sverchok](https://github.com/nortikin/sverchok) | 규칙 기반 형태를 빠르게, 올바른 스케일로 | 기본값의 지역 차이(Archimesh 상판 약 0.88 m) |
| 곡면 제품(소파 쿠션, 플라스틱 하우징) | 저폴리 베이스 + crease/support loop + SubSurf | Nova3D 초안, AI 생성 후 재모델링 | 셰이딩 품질과 형태 제어 | 핀칭(Bevel↔SubSurf 순서) |
| 조형물·유기 형상 | SDF([fogleman/sdf](https://github.com/fogleman/sdf)), 메타볼, Mesh to Volume → remesh | AI image-to-3D → remesh | 블렌딩이 자연스럽고 manifold 보장 | UV 없음. 리토폴·베이크 필요 (7장) |
| 레퍼런스 사진이 있는 특정 제품 | 파트 단위 image-to-3D를 **레퍼런스로** 쓰고 코드로 재모델링 | 실루엣 IoU 게이트로 직접 보정 | 통짜 메시는 편집 불가, 대칭·두께가 틀림 | 모델 라이선스(한국 제외, 비상업) |
| 배경 소품 | 에셋 라이브러리 | AI 생성 | 가장 싸고 품질이 안정적 | 라이선스·스케일 정규화 ([10 파이프라인](10_assets_pipeline_licensing.md)) |

### 3.2 도구별 요약

| 도구 | 상태(확인일) | 라이선스 | 강점 | 약점·주의 |
|---|---|---|---|---|
| bpy + 모디파이어 (Blender 5.2.2 안정판, 4.5·4.2 LTS) | 2026-09 | GPL | 비파괴라 LLM이 파라미터만 바꿔 반복할 수 있음 | 버전별 API 차이. 스케일 미적용 시 bevel 왜곡 |
| [build123d](https://raw.githubusercontent.com/gumyr/build123d/dev/README.md) | 0.13.0 (2026-09-21), Python 3.11~3.14 | Apache-2.0 | OCCT BREP, [조인트](https://github.com/gumyr/build123d/blob/dev/docs/joints.rst)(Rigid/Revolute/Linear/Cylindrical/Ball + `connect_to`)로 틈 없이 조립 | 유기 형상·텍스처에 약함 |
| [build123d-mcp](https://github.com/pzfreo/build123d-mcp) | PyPI 0.3.90 (2026-09-25) | Apache-2.0 | execute / measure / compare(fit·interference) / validate / design_audit / snapshot / render_view / STEP·STL export | 성능 수치는 도구 저자의 자체 보고 |
| [AgentCAD](https://github.com/jdilla1277/agentcad) | 0.6.0 (2026-09-11) | Apache-2.0 | run / measure / check-spec / inspect / parts / diff, A/B view, 턴테이블 GIF | **Python 3.10~3.12 전용**. 기계 부품 중심 |
| [CadQuery](https://github.com/CadQuery/cadquery) | 2026-09 | Apache-2.0 | 연구(CAD-Recode, CADCodeVerify)의 코드 표현이라 LLM에 친숙 | 설치 의존성이 무거움(conda 권장) |
| OpenSCAD + [BOSL2](https://github.com/BelfrySCAD/BOSL2) | BOSL2 베타 | BSD-2 / GPL | `attach(BOT)` 같은 앵커 배치로 **접촉이 구조적으로 보장**됨 | CSG 메시 품질, UV 없음 |
| OpenSCAD MCP: [RobertCoop/openscad-mcp](https://github.com/RobertCoop/openscad-mcp) (142★), [jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server) (197★) | 2026-09 | MIT | RobertCoop은 조립 간섭·클리어런스 검사 포함(이 주제에 특히 유용). jhacksman은 4방향 PNG | codeofaxel/Kiln은 3D 프린팅 오케스트레이션(AGPL)이라 같은 분류가 아님 |
| [Infinigen](https://github.com/princeton-vl/infinigen) v1 (indoors-stable) | PyPI 안정판 1.15.5 | BSD-3 | 의자·식탁·책상·소파·침대·주방 캐비닛 factory. 부품 구조가 코드로 공개됨 | 설치가 무거움. 단일 방 coarse 단계 CPU 약 8~13분. 치수는 랜덤 범위 |
| [Infinigen 2.0](https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/Infinigen2.md) | 2.0.0a2 (2026-08-27 pre-release), **Python 3.11 전용** | BSD-3 | V2 의자(사무용·원목 식탁), 손잡이 4종(lever/bar-pull/knob/curved-pull), 1~5 패널 문, 렌더 검증 | 실내 오브젝트 일부만 지원. crease + subsurf 재구성은 **테이블 다리·램프·천장등·손잡이에 한정**([CHANGELOG](https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/CHANGELOG.md)) |
| [Archimesh](https://github.com/blender/blender-addons/tree/main/archimesh) | 저장소 2025-05-09 보관(archived) | GPL | 방·문·창·계단·주방·선반 등. 기본값 자체가 치수 참고 | 스타일이 오래됨. 4.2+ Extensions 배포 여부 (미확인) |
| [Archipack](https://github.com/s-leger/archipack) | GitHub 공개판은 2.78/2.79용 | GPL-3.0 | 벽·계단·창호 규칙 기반 | 최신 Blender 호환판 (미확인) (신뢰도 낮음) |
| [Sverchok](https://github.com/nortikin/sverchok) | 5.1 / 4.5 / 3.6 / 2.8 지원 표기 | GPL3 | 600개 이상의 노드. 격자 스크린, 파라메트릭 파빌리온, 트위스트 조형 | LLM이 노드 트리를 코드로 조립하면 장황해짐 |
| [Nova3D](https://github.com/RareSense/Nova3D) | 2026-08, 약 721★ | 클라이언트 MIT, 백엔드 비공개 | 텍스트·이미지 → Blender 코드 → 이름·계층·조인트 피벗·PBR이 있는 GLB | 품질 독립 검증 없음. 가격 비공개 |

**Python 버전 충돌에 주의하세요.** PyPI `bpy` 5.1+는 Python 3.13 전용이고, 5.0은 3.11입니다. AgentCAD는 3.13 미만이 필요하고, Infinigen 2.0은 3.11 전용이며, build123d는 3.11~3.14를 지원합니다. 한 venv에 모두 넣지 말고 도구마다 venv를 따로 만드세요.

### 3.3 하이브리드 레시피

**A. 정밀 부품은 build123d로 만들고 Blender에서 마감합니다.**

```json
{"mcpServers": {"build123d-mcp": {"command": "uv", "args": ["tool", "run", "--python", "3.12", "build123d-mcp@latest"]}}}
```

1. build123d-mcp에서 부품을 만듭니다(reset → execute → `measure()`).
2. 장부와 장부 구멍 같은 결합을 `compare(a='tenon', b='mortise', kind='fit')`로 간섭 검사합니다. 이어서 `validate()`를 실행하고, 통과하면 STL이나 STEP으로 내보냅니다.
3. Blender로 가져올 때 **mm → m 변환을 위해 scale 0.001을 적용한 뒤 Apply**합니다. 그다음 bevel, UV, 재질을 입힙니다.
4. 조립 위치는 build123d `RigidJoint.connect_to`로 계산합니다.
5. 프롬프트 예: "Build incrementally, render after main features, measure final dimensions, run validate(), export STEP if it passes."
6. 재현성이 필요하면 `@latest` 대신 버전을 고정하세요. CADGenBench 제출에서는 0.3.79~0.3.83을 고정해서 썼습니다.

**B. AI가 만든 메시는 '레퍼런스'로만 쓰고 코드로 다시 만듭니다.**

1. 이미지에서 파트 단위 메시를 받습니다(PartCrafter는 최대 16파트).
2. 각 파트의 bbox와 주축을 뽑습니다.
3. 표준 치수로 스냅합니다(다리 0.04, 좌면 0.445 등).
4. `box()` / `rod()`로 다시 만들고 bevel을 넣습니다.
5. 원본 AI 메시는 숨겨 두고 IoU 비교에만 씁니다.
6. 다른 길로는 [MeshCoder](https://github.com/InternRobotics/MeshCoder)(MIT)가 있습니다. 점군을 부품이 나뉜 Blender 코드로 역변환하므로, 코드의 치수를 표준값으로 고쳐 다시 생성할 수 있습니다. 학습 카테고리 밖에서는 일반화가 제한적입니다.

**C. 절차적 생성기를 '형태와 비율의 교사'로 씁니다.**

- Infinigen v1 단일 에셋 생성: `python -m infinigen_examples.generate_individual_assets --output_folder outputs/x -f ChairFactory -n 4 --save_blend`([문서](https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/GeneratingIndividualAssets.md))
- Infinigen 2.0: `uv venv --python 3.11 && uv pip install "infinigen==2.0.0a2"` 후 `uv run infinigen sofa_rand object_demo render_cycles --seed 0`
- 프롬프트 예: "ChairFactory의 부품 구조(leg_type 4종, back_type whole / partial / horizontal-bar / vertical-bar)를 선택지로 삼아, 미드센추리 스타일에 맞는 조합을 고르고 이유를 적어라. 치수는 치수 기준표(KR)를 따른다."

---

## 4. 모디파이어 스택 레시피

### 4.1 하드서피스 가구의 표준 순서

| 순서 | 단계 | 권장값 | 근거·메모 |
|---|---|---|---|
| 0 | 치수대로 만들고 **transform apply** | `transform_apply(rotation=True, scale=True)` | 스케일을 적용하지 않으면 bevel·solidify 폭이 축마다 왜곡됨 |
| 1 | Mirror | X축, Clipping 켬 | 좌우 대칭 부품 |
| 2 | Array | 슬랫, 서랍, 선반 반복 | 개수를 스펙에 명시 |
| 3 | Solidify (판재만) | thickness 0.018, `use_even_offset=True` | 평면으로 만든 판에 두께 부여 |
| 4 | Boolean | 4.x `EXACT`, 5.0+ `MANIFOLD`(또는 `EXACT`). 커터는 렌더·뷰포트 모두 숨김 | 손잡이 홈, 서랍 핑거 홀, 도브테일. 입력이 manifold여야 함. [MOD_boolean.cc](https://raw.githubusercontent.com/blender/blender/main/source/blender/modifiers/intern/MOD_boolean.cc) |
| 5 | Bevel | width는 재질별(아래 표). 크기를 모르면 **최대 치수의 0.5%**. segments 렌더 3 / 게임 1~2. `limit_method='ANGLE'`, 30°, Harden Normals, Miter Outer Arc | [scenario hard-surface 스킬](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-hard-surface/SKILL.md). 0.5%는 튜토리얼 출처가 아니라 스킬 저자가 덧붙인 기본값입니다 |
| 6 | Subdivision Surface (곡면 부품만) | levels 2 / render 3, crease 또는 holding loop | **Bevel을 SubSurf 앞에** 둡니다. 순서가 바뀌면 핀칭이 생깁니다([cc-blender-skill modeling](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-modeling/SKILL.md)) |
| 7 | Weighted Normal | mode `FACE_AREA`, `keep_sharp=True` | **스택 맨 끝** |

- `Mesh.use_auto_smooth`는 **4.1에서 제거**됐습니다. Smooth by Angle 모디파이어나 Shade Smooth by Angle을 쓰세요.
- 소스마다 순서가 조금씩 다릅니다. cc-blender-skill은 Mirror → Array → Solidify → Bevel → SubSurf → Boolean 순서를 씁니다. 이 문서는 **잘린 모서리에도 bevel이 걸리도록 Boolean을 Bevel 앞에** 둡니다(원자료 08 조사 순서). 커터가 곡면을 자르면 결과를 눈으로 비교해 보고 고르세요.
- cc-blender-skill의 기본 bevel 폭 **0.02 m(2 cm)는 가구 부품에는 너무 큽니다.** 두께 3 cm 좌판이 뭉개집니다. 가구에는 아래 표의 폭을 쓰세요.

### 4.2 재질별 bevel 폭 (경험치, 원문 검증 안 됨)

| 재질 | 폭 | 메모 |
|---|---|---|
| 원목 | 1~3 mm | 식탁 상판 가장자리, 의자 좌판 앞 모서리는 R 5 mm 정도로 더 둥글게 |
| 도장 MDF | 0.5~1.5 mm | |
| 금속 | 0.3~1 mm | 각파이프는 모서리 R이 있음 |
| 석재 | 2~5 mm | 조형물 받침대 3 mm |
| 사출 플라스틱 | 0.5~2 mm | |
| 패브릭 쿠션 모서리 | 10~30 mm | 또는 SubSurf + cloth |

"Plausible mesh bevels provide real highlight surfaces on manufactured edges"([blender-production realism.md](https://raw.githubusercontent.com/per-simmons/blender-production/master/references/realism.md)). 완전히 날카로운 90° 모서리는 실제로 없기 때문에 CG 티가 납니다. 렌더 전용이라면 Bevel 셰이더 노드도 쓸 수 있지만 Cycles 전용이라 게임으로 내보내기 전에 베이크해야 합니다([06 라이팅·렌더](06_lighting_rendering_art_direction.md)).

### 4.3 곡면·쿠션·판재

- **곡면 제품**: 저폴리 베이스 + SubSurf(levels 2, render 3)로 만듭니다. 날카로워야 할 에지는 crease 1.0을 주거나(4.x 이상은 에지 속성 `crease_edge`), 에지 양쪽에 에지 길이의 약 2~5% 간격으로 holding loop를 넣습니다. Infinigen 2.0도 테이블 다리, 램프, 손잡이를 "low base polycount with edge creasing and subsurf"로 다시 만들었습니다.
- **소파 쿠션**: box에 SubSurf 2를 걸고 가운데 loop를 살짝 부풀립니다. 파이핑은 커브 bevel 0.004로 표현합니다.
- **판재 가구**: 평면 + Solidify(0.018, even offset)로 만들거나, `box()`로 두께를 가진 판을 만듭니다. 뒤판은 3~6 mm입니다.

### 4.4 코드 B: 스택 헬퍼 (4.2.23 LTS·5.0.1에서 확인)

```python
import math

def hard_surface_stack(ob, width=0.002, segments=3, angle_deg=30):
    """제조 모서리용 Bevel + Weighted Normal(스택 맨 끝). 스케일을 적용한 뒤 호출."""
    bev = ob.modifiers.new("Bevel", 'BEVEL')
    bev.width = width
    bev.segments = segments
    bev.limit_method = 'ANGLE'
    bev.angle_limit = math.radians(angle_deg)
    bev.harden_normals = True
    wn = ob.modifiers.new("WeightedNormal", 'WEIGHTED_NORMAL')
    wn.mode = 'FACE_AREA'
    wn.keep_sharp = True
    return bev, wn


def boolean_cut(ob, cutter):
    """Boolean을 Bevel 앞에 넣어 잘린 모서리에도 bevel이 걸리게 한다."""
    b = ob.modifiers.new("Cut", 'BOOLEAN')
    b.operation = 'DIFFERENCE'
    ids = [e.identifier for e in b.bl_rna.properties['solver'].enum_items]
    b.solver = 'MANIFOLD' if 'MANIFOLD' in ids else 'EXACT'  # 4.2: FAST/EXACT, 5.0: FLOAT/EXACT/MANIFOLD
    b.object = cutter
    cutter.hide_render = True
    cutter.hide_set(True)  # 뷰포트에서도 숨겨야 scene_audit가 커터를 별도 물체로 세지 않는다
    bevel_idx = next((i for i, m in enumerate(ob.modifiers) if m.type == 'BEVEL'), None)
    if bevel_idx is not None:
        ob.modifiers.move(len(ob.modifiers) - 1, bevel_idx)
    return b
```

- 서랍 앞판(0.40×0.018×0.16 m)에 핑거 홀을 뚫어 확인했습니다. 스택이 `BOOLEAN → BEVEL → WEIGHTED_NORMAL` 순서로 정렬되고, 평가된 메시의 non-manifold 에지는 0이며, scene_audit에는 앞판만 유닛으로 나옵니다(커터는 제외).
- **버전 함정(직접 확인)**: 4.2.23의 solver enum은 `['FAST', 'EXACT']`, 5.0.1은 `['FLOAT', 'EXACT', 'MANIFOLD']`입니다. 4.x용 코드의 `solver='FAST'`는 5.0에서 `enum "FAST" not found` 오류가 납니다. `EXACT`는 두 버전 모두에서 됩니다. Manifold solver가 4.5 LTS에서 들어왔다는 말은 릴리스 노트로 확인하지 못했습니다 (미확인).

---

## 5. 부품 분해 체크리스트

### 5.1 PartNet 계층을 체크리스트로

[PartNet](https://github.com/daerduoCarey/partnet_dataset)(CVPR 2019, 주석 MIT)은 26,671개 모델, 573,585개 파트 인스턴스, 24개 카테고리의 계층형 파트 주석입니다. 실제 가구 수만 개에서 나온 부품 어휘라서 누락 부품을 줄여 줍니다.

- **Chair** ([Chair-hier.txt](https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Chair-hier.txt))
  - `chair_back`: back_surface(vertical_bar / horizontal_bar), back_connector, back_support, back_frame
  - `chair_seat`: seat_support, seat_frame(seat_frame_bar), seat_surface
  - `chair_base`: regular_leg_base(leg, bar_stretcher, runner, foot, rocker) / star_leg_base / pedestal_base
  - `chair_arm`, `chair_head`, `footrest`
- **Table** ([Table-hier.txt](https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Table-hier.txt)): tabletop, 여러 종류의 base(leg + stretcher, pedestal, drawer_base → drawer_box 등)

프롬프트에는 "다음 계층의 각 leaf 부품이 있는지 스펙에서 확인하고, 생략했다면 이유를 적어라"라고 넣습니다. 이름을 이 계층에 맞추면(`chair_base_leg_FL`) 검사 스크립트가 부품 존재 여부를 자동으로 확인할 수 있습니다. PartNet에는 치수 정보가 없고 구조만 있습니다.

### 5.2 유형별 부품·두께·관계

아래 표의 두께 값은 세 종류의 출처가 섞여 있습니다. Infinigen·Archimesh 값은 **코드로 확인한 값**, 나머지는 원자료가 정리한 **목공 경험치(원문 검증 안 됨)**, 관계 치수는 [치수 기준표](../03_playbooks/05_reference_dimensions.md)의 값입니다.

| 유형 | 필수 부품 | 자주 빠지는 부품 | 현실적인 두께·치수 | 핵심 관계 |
|---|---|---|---|---|
| **식탁 의자** | 좌판, 다리 4, 등받이(기둥 + 가로대/슬랫) | 사이드 스트레처, 좌판 프레임(에이프런), 등받이 연결재 | 다리 35~45 mm 각재, 좌판 20~35 mm(쿠션이면 50~100), 슬랫 15~20 mm, 스트레처 20×30 mm(바닥에서 100~200) | 좌판 윗면 430~460(KR), 상판−좌판 250~305. 뒷다리가 등받이까지 이어지는 일체형이면 약 8° 뒤로 기울임 |
| **식탁** | 상판, 다리 4 | **에이프런**(상판 가장자리에서 30~50 mm 안쪽), 스트레처 | 상판 25~40 mm(Infinigen 랜덤 범위 30~60), 에이프런 높이 70~100 × 두께 20~25, 다리 40~70 각재(Infinigen straight 지름 50~70) | 상판 720~750(KR). 1인당 폭 610. 팔걸이 의자라면 팔걸이가 에이프런 아래로 들어가는지 확인 |
| **소파** | 베이스 프레임, 좌 쿠션, 등 쿠션, 팔걸이, 다리/받침 | 파이핑, 쿠션 사이 틈, 스티칭 | 쿠션 모서리 bevel 10~30 mm, 파이핑 커브 bevel 0.004 m | 좌판 높이 430~480, 좌판 깊이 510~610(딥시트 760까지), 전체 깊이 810~1,020, 3인용 폭 1,830~2,440(흔한 값 2,130). 한국 로우형은 더 낮다는 말이 있으나 (미확인) |
| **수납장**(책장, 옷장, 주방장) | 측판 2, 상·하판, 선반, 뒤판, 걸레받이 | 뒤판, 문·서랍 틈, 경첩, 손잡이, 선반 받침 | 판재 18 mm(Archimesh board 0.018, Infinigen 측판 0.02), 뒤판 3~6 mm, 문·서랍 틈 2~3 mm, 18 mm 판의 무지지 스팬 0.8 m 이하(경험치) | 책장 깊이 250~350(BILLY 280), 옷장 550~650(PAX 580), 주방 하부장 깊이 580~600(KR 상판 깊이 600~650) |
| **주방 하부장**(Archimesh 기본값) | 본체, 걸레받이, 상판 | 상판 돌출, 걸레받이 | 걸레받이 0.16 + 본체 0.70 + 상판 0.02 = 상판 윗면 **약 0.88 m**, 상판 돌출 0.03, 상부장 깊이 0.35(바닥에서 1.5 m) | 한국 850 / 미국 914에 맞게 **기본값을 바꿔서** 쓰세요 ([achm_kitchen_maker.py](https://raw.githubusercontent.com/blender/blender-addons/main/archimesh/achm_kitchen_maker.py)) |
| **침대** | 프레임(측면 레일, 헤드보드, 풋보드), 매트리스 받침(슬랫), 매트리스, 다리 | 슬랫, 매트리스와 프레임 사이 여유, 침구 | Infinigen bedframe: 폭 1.4~2.4, 길이 2.0~2.4, 다리 높이 0.2~0.6, 헤드보드 0.5~1.3(랜덤 범위) | 매트리스는 **mm 값**으로(KR Q 1500×2000). 매트리스 윗면 500~650(미국 약 635). 협탁 = 매트리스 윗면 ±50 |
| **금속 프레임 가구** | 프레임, 상판/좌판, 발 | 용접부, 캡, 수평 조절발 | 각파이프 20×20~40×40, 두께 1.2~2 mm(경험치) | 얇은 금속은 스펙큘러 플레어가 잘 생김(cc-blender-skill 저자가 한계로 명시) |

**연결 규칙:** 의도한 결합(장부 등)만 겹침을 허용하고, 그 쌍을 스펙의 `connections`에 적습니다. 겹침 깊이는 5~15 mm 안에서 정합니다. ProfRino는 최소 5 mm, cc-blender-skill은 5~15 mm를 권장합니다. `check_assembly()`의 `max_overlap=0.015`가 이 상한입니다.

### 5.3 디테일 계층 (macro / meso / micro)

[blender-production realism.md](https://raw.githubusercontent.com/per-simmons/blender-production/master/references/realism.md)는 디테일을 세 층으로 나눕니다. 형태와 비율이 통과한 **다음에** 추가하세요.

- **macro**: 형태, 패널 분할, 부품 비율
- **meso**: 이음새, 나사·경첩, 손잡이, 쿠션 파이핑, 스티칭, 모서리 마모
- **micro**: 결, 거칠기 변화(재질 단계, [05 텍스처링](05_texturing_materials.md))

---

## 6. 조립 스킬: '분해된 의자' 막기 (ProfRino)

[ProfRino/Blender-MCP-Assembly-Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill)(약 72★)은 Blender MCP로 만든 의자가 흩어져 보이는 문제를 직접 다루는 스킬입니다. 의자 조립 Before/After 예시가 있습니다. 정량 평가나 테스트한 모델 정보는 없습니다. **LICENSE 파일이 없으므로** 내용을 참고해 자기 규칙으로 다시 쓰는 편이 안전합니다.

| 규칙 | 내용 | 왜 |
|---|---|---|
| 연결 맵 먼저 | 코드를 쓰기 전에 부품마다 무엇과, 어느 면으로, 얼마나 겹쳐서 붙는지 적음 | 조립 논리를 명시해야 "폭발한" 모델이 줄어듦 |
| 큐브는 `size=2` | `primitive_cube_add(size=2)`로 만들면 scale 값 = half-extent | LLM의 대표 버그: `size=1` 큐브에 half-extent를 scale로 주면 **치수가 절반**이 됨 |
| 방향성 부재에 Euler 금지 | 다리, 레일, 파이프, 보처럼 두 점을 잇는 부재는 bmesh로 두 점 사이에 직접 만듦 | 실린더 Euler 회전 축·순서 오류가 흔함 |
| 스케일 직후 transform apply | 특히 루프 안에서 | 엉뚱한 오브젝트에 적용되는 위험을 줄임 |
| 측정해서 파생 | `verify_bounds()`, `verify_overlap()`로 월드 bbox를 재고, 새 치수는 측정값에서 계산 | 추측으로 쌓인 오차 방지 |
| 마무리 감사 | `finalize()`, `audit_all()`로 transform 적용, 원점, 스무딩, 회전·스케일 확인 | 최종 상태를 보장 |

**직접 확인한 큐브 크기 버그**(4.2.23 LTS·5.0.1 동일): 좌판 0.44×0.42×0.03 m를 half-extent (0.22, 0.21, 0.015)로 scale하면, `size=2` 큐브는 (0.44, 0.42, 0.03)이 되지만 `size=1` 큐브는 **(0.22, 0.21, 0.015)**가 됩니다. 이 문서의 `box()`는 규약 혼동을 아예 없애는 방식입니다. 전체 치수를 메시 정점에 굽고 오브젝트 scale은 1로 둡니다. `rod()`는 방향을 정점에 직접 굽기 때문에 오브젝트 회전이 (0, 0, 0)으로 남습니다. 수직, 역방향, X축, 대각선 막대로 bbox를 확인했습니다.

**원자료 간 충돌과 이 문서의 정리:** 원자료 08의 검사 예시는 "관입은 `JOINT_` 접두사만 허용"이라고 했고, ProfRino는 "연결부 최소 5 mm 겹침"을 요구합니다. 두 규칙은 서로 충돌합니다(검증에서 지적됨). 이 문서는 **연결 맵에 적은 쌍만 5~15 mm 겹침을 허용하고, 나머지 겹침은 모두 실패**로 처리하는 것으로 정리했습니다.

비슷한 목적의 다른 스킬도 있습니다. [Gaius114/blender-claude-mcp](https://github.com/Gaius114/blender-claude-mcp)는 형상을 만들기 전에 `plan_validator.py`와 `assembly_kernel.py`로 분해 계획을 검증하고, blender-space 스킬로 월드 bbox 기준 배치를 합니다. 자체 서버를 쓰고, 라이선스는 (미확인)입니다.

---

## 7. 조형물·유기 형상

LLM이 bpy로 버텍스를 직접 움직여 유기 곡면을 만들면 울퉁불퉁하거나 깨집니다. 암시적 표면(SDF, 메타볼, 볼륨)은 블렌딩이 자연스럽고 manifold가 보장됩니다.

### 7.1 방법 선택

| 방법 | 어떻게 | 설정값(원자료 제안값) | 맞는 대상 | 약점 |
|---|---|---|---|---|
| **A. 코드 SDF** ([fogleman/sdf](https://github.com/fogleman/sdf), MIT) | `sphere(0.3).k(0.05)`처럼 smooth union(k=0.03~0.08)으로 조합 → `f.save('sculpt.stl')` → Blender | union·difference·intersection, rounded_box, capsule, twist, bend | 추상 조형, 유기적 손잡이, 매끈한 블렌딩 | marching cubes 메시라 토폴로지가 거칠고 UV가 없음 |
| **B1. 메타볼** | Metaball → Convert to Mesh → Remesh | resolution 0.02 | 블롭, 물방울, 부드러운 덩어리 | 세부 제어가 어려움 |
| **B2. 볼륨** | Geometry Nodes Mesh to Volume → Volume to Mesh | voxel 0.005 | 여러 형태를 하나로 녹여 붙이기 | GN 전용 bevel·SDF grid 노드는 (미확인) |
| **B3. 커브·스킨** | Curve to Mesh + radius 프로파일 / Skin modifier | — | 가지, 관, 크리처 골격 | 결합부 토폴로지 정리가 필요 |
| **C. AI image-to-3D** | 생성 → QuadriFlow 또는 voxel remesh | 생성기 선택은 [04 AI 3D 생성](04_ai_3d_generation.md) | 레퍼런스가 있는 복잡한 조형 | 치수·대칭 보장 없음. **Hunyuan 계열 오픈웨이트는 한국 제외** |
| **D. 스컬프트 브러시** | 사람이 직접 | — | 최종 디테일 | 에이전트가 sculpt 브러시로 고품질 조형을 만든 검증 사례는 이번 조사에서 찾지 못했습니다 |

### 7.2 마감 순서 (공통)

1. 형태를 확정합니다(A~C 가운데 하나).
2. Blender에서 **voxel remesh**를 합니다(voxel size 0.003~0.01 m, 크기에 비례).
3. 표면 디테일은 **Multires 2~3** 또는 **Displace**(노이즈 strength 0.002~0.005)로 넣습니다.
4. 게임·실시간용이면 **Decimate**나 리토폴로지 후 normal·AO를 **bake**합니다([05 텍스처링](05_texturing_materials.md)의 bake 절 참고).
5. **받침대와 설치 부재는 하드서피스로 따로** 만듭니다. 예: 석재 받침 0.4×0.4×0.9 m, bevel 3 mm. 이렇게 하면 제작된 것과 조각된 것의 대비가 살아납니다.
6. scene_audit로 non-manifold와 바닥 접지를 확인합니다. 조형물은 받침대가 있는 하나의 유닛으로 묶습니다.

### 7.3 한계 (저자들이 직접 밝힌 것)

- [cc-blender-skill](https://github.com/RobLe3/cc-blender-skill)(v1.3.0, MIT) 저자는 곡면 가구, 프로파일 컷, 실루엣 같은 미적 완성도를 범위 밖으로 두었습니다. 얼굴은 추상 아바타 수준이고, 얇은 금속에는 스펙큘러 플레어가 생긴다고 밝혔습니다. 이 스킬은 Blender 5.1.1에서 의자를 포함한 6종을 끝까지 검증했고 실패 렌더도 공개했습니다.
- kitchen-twin 저자는 "thin and shiny things are still weak"라고 적었습니다(12장).
- 조형물의 '아름다움'은 수치 게이트로 판정하기 어렵습니다. 형태 확정은 사람이 하고, 에이전트에게는 remesh, 받침대, 배치, 조명 같은 반복 작업을 맡기는 분담이 현실적입니다.

---

## 8. 연구에서 얻은 교훈

**라이선스 먼저**: 아래 표에서 상업 사용이 막힌 연구 코드는 **아이디어만 가져오고 코드와 가중치는 상업 파이프라인에 넣지 마세요.** 전체 연구 정리는 [11 학술 연구](11_research_papers.md)에 있습니다.

| 연구 | 무엇 | 실무 교훈 | 라이선스·상태 |
|---|---|---|---|
| [LL3M](https://github.com/threedle/ll3m) (UChicago, 2025) | planner / retriever(BlenderRAG) / coder / debugger / refiner 멀티 에이전트가 Blender 코드로 에셋 생성 | 역할을 나누고, **현재 Blender 버전의 API 문서를 주입**하면 없는 속성을 호출하는 오류가 줄어듦 | [비상업 학술·평가 라이선스](https://raw.githubusercontent.com/threedle/ll3m/main/LICENSE). 저장소는 클라이언트·애드온뿐이고 파이프라인 코드는 비공개. 사용 모델 Claude Sonnet 3.7이 retire되어(2026-02-19) **서버 중단**. 모델에 의존하는 서비스는 수명 위험이 있음 |
| [BlenderLLM](https://github.com/FreedomIntelligence/BlenderLLM) (2024-12) | Qwen2.5-Coder-7B 파인튜닝. CADBench-Sim 0.748 vs GPT-4o 0.565, 문법 오류율 3.4% vs 21.4% | CADBench의 평가 축(속성, 공간 관계, 지시 준수)을 자체 검수 체크리스트로 차용 | Apache-2.0. GPT-4o가 채점자(LLM-as-judge)라는 한계, 2024년 비교라 최신 모델 대비 우위는 불확실 |
| [MeshCoder](https://github.com/InternRobotics/MeshCoder) (NeurIPS 2025) | 점군 → 부품이 나뉜 편집 가능 Blender 코드. 41개 카테고리 100만 쌍으로 학습 | 통짜 메시를 코드로 되돌리는 경로 | MIT. 2025-11-11에 코드·체크포인트·데이터 10만 쌍 공개 |
| [CAD-Recode](https://github.com/filaPro/cad-recode) (ICCV 2025) | Qwen2-1.5B + 선형층 1개로 점군 → CadQuery | 정밀 부품 역설계, "코드를 CadQuery로 표현하라"는 선택의 근거 | [CC BY-NC 4.0](https://raw.githubusercontent.com/filaPro/cad-recode/main/LICENSE.md) (**비상업**) |
| [Text2CAD](https://github.com/SadilKhan/Text2CAD) (NeurIPS 2024 Spotlight) | 초급~전문가 수준 프롬프트 → sketch-extrude 시퀀스 | 형용사 대신 **치수와 연산 순서**를 쓴 전문가 수준 프롬프트일수록 정확 | [CC BY-NC-SA 4.0](https://raw.githubusercontent.com/SadilKhan/Text2CAD/main/LICENSE) (**비상업**) |
| [CADCodeVerify](https://github.com/Kamel773/CAD_Code_Generation) (ICLR 2025) | VLM이 렌더를 보고 검증 질문을 스스로 만들어 답한 뒤 CadQuery 코드를 반복 수정 | 예/아니오 질문 8~12개 → 4방향 렌더로 답 → "아니오"만 수정 지시로 | 라이선스 (미확인). 수치 결과는 원문 차단으로 확인 못 함 |
| [CADFusion](https://github.com/microsoft/CADFusion) (ICML 2025) | 순차 학습과 시각 피드백 학습을 번갈아 진행 | 렌더 기반 피드백이 텍스트만으로 한 학습보다 형상 품질을 높임 → 렌더 비평 단계는 필수 | MIT |
| [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open) (CVPR 2025 Highlight) | VLM의 Blender 편집 벤치마크(procedural geometry, lighting, material, blend shape, placement) | 생성기와 검증기를 분리하고 **검증에 연산을 더 쓰면** 성능이 오름. 최적 비율은 총 예산에 따라 달라짐(0.33 / 0.62 / 0.73만 실험) | 공개. VLM 검증기와 인간의 일치율(Claude-3.5-Sonnet 0.66, 인간끼리 0.79)을 보면 VLM 판정만 믿으면 안 됨 |
| [ShapeAssembly](https://github.com/rkjones4/ShapeAssembly) (SIGGRAPH Asia 2020) | Cuboid 프록시를 attach / squeeze / reflect로 계층 조립하는 DSL | 블록아웃을 "Cuboid + attach"로 먼저 짜면 떠 있는 부품이 문법상 생기지 않음 | [Brown 대학 라이선스](https://raw.githubusercontent.com/rkjones4/ShapeAssembly/master/LICENSE), **상업 제품 포함 금지** |
| L3GO (NAACL 2025 Demo) | 언어 에이전트가 부품을 하나씩 만들며 부착·겹침 피드백으로 수정 | 부품 하나마다 "부모와 닿았나, 겹쳤나"를 확인하고 다음으로 | 공개 저장소는 비어 있음. 세부는 (미확인) (신뢰도 낮음) |
| [LLaMA-Mesh](https://github.com/nv-tlabs/LLaMA-Mesh) / [MeshLLM](https://github.com/Fangkang515/MeshLLM) | OBJ 정점·면을 텍스트 토큰으로 생성 | 면 수와 컨텍스트 한계로 저폴리에 머묾 → **코드 생성 경로가 현실적** | LLaMA-Mesh는 [NVIDIA 비상업](https://raw.githubusercontent.com/nv-tlabs/LLaMA-Mesh/main/LICENSE), MeshLLM은 Apache-2.0 |
| [ShapeLLM-Omni](https://github.com/JAMESYJL/ShapeLLM-Omni) (NeurIPS 2025 Spotlight) | 3D VQVAE 토크나이저를 붙인 네이티브 3D MLLM(생성·편집·이해) | "등받이를 더 높게" 같은 대화형 편집 실험용. 정밀 치수는 코드 경로가 우선 | MIT. TRELLIS 기반 해상도 한계 |
| [PartCrafter](https://github.com/wgsxm/PartCrafter) (NeurIPS 2025) | 이미지 한 장 → 최대 16파트 메시. 장면용 PartCrafter-Scene도 있음 | 통짜 메시 대신 파트로 받아 부품별 재질·리메시 | MIT, TripoSG 기반, VRAM 8 GB 이상 |
| [OmniPart](https://github.com/HKU-MMLab/OmniPart) / [PartPacker](https://github.com/NVlabs/PartPacker) / [Hunyuan3D-Part](https://github.com/Tencent-Hunyuan/Hunyuan3D-Part) | 파트 인식 생성 | 같은 목적 | OmniPart MIT(2D 파트 마스크 입력). PartPacker **비상업**(약 10 GB). Hunyuan3D-Part는 입력이 **메시**(P3-SAM 분할 → X-Part), light 버전만 공개, **한국 제외** |
| [Procedura](https://arxiv.org/abs/2608.26238) (arXiv 2608.26238, 2026-08) | 에이전트가 부품을 파라메트릭 프로그램으로 만들고 **typed mate(기계적으로 검증 가능한 결합) + 솔버**로 조립. mate 게이트가 떠 있거나 파고드는 파트를 측정해 거부. 파트별 PBR 할당, material critic, 관절화 | 가구를 '제대로' 만드는 문제에 가장 직접적인 2026 연구. 이 문서의 연결 맵 + `check_assembly()`는 같은 발상을 가볍게 구현한 것 | Gemini 3.7 Flash / GPT-5.6-sol 구성, MechBench-36. arXiv 본문은 차단으로 직접 열람하지 못했고 프로젝트 페이지 소스로 확인(검증 에이전트) |
| [CADGenBench](https://github.com/huggingface/cadgenbench) | 공학 도면 → 3D 부품 생성과 STEP 편집. validity, shape similarity, interface match, topology(Betti)를 CAD Score로 종합 | 모델만 보지 말고 **모델 + MCP + 프롬프트 시스템 단위로** 평가 | Apache-2.0. 기계 부품 중심이라 미적 품질은 측정하지 않음 |

**연구에서 나온 합의와 이 문서의 대응**

| 합의 | 이 문서에서 |
|---|---|
| 렌더 → 비평 폐루프 | 2.5절 렌더 검사, 13장 질문 프롬프트 |
| 좌표는 솔버, LLM은 관계와 제약 | 스펙의 `connections`, OpenSCAD `attach`, build123d 조인트, Procedura의 typed mate |
| 처음부터 만들기보다 검색·재사용 | 3.1절 에셋 라이브러리, Infinigen·Archimesh 활용 |
| 파라메트릭 부품 코드 | `box()` / `rod()` / 스펙 빌드, build123d |
| 검증에 연산 투자 | 결정적 검사를 매 반복 실행, 생성기와 검증기 분리 |

---

## 9. 실패 모드와 자동 검사

| 실패 | 원인 | 자동 검사 | 처방 |
|---|---|---|---|
| 부품이 떠 있음("분해된 의자") | 좌표 즉흥 계산, 큐브 규약 혼동 | `check_assembly()` → `GAP`, `DETACHED` / scene_audit(유닛 단위) → `floating_or_wall_mounted` | 부모 부품의 면에 스냅. 연결 맵 재작성. 벽걸이·천장등은 의도한 부유인지 확인 |
| 부품 관입 | 계획에 없는 겹침 | `UNPLANNED_PENETRATION` / scene_audit `interpenetrations`(유닛 간) | 접촉 면까지 이동. 의도한 결합이면 연결 맵에 추가(5~15 mm) |
| 결합이 너무 깊음 | 장부를 과하게 박음 | `TOO_DEEP` | 겹침 5~15 mm로 조정 |
| 치수가 절반 또는 두 배 | `size=1` 큐브에 half-extent scale | 스펙 대비 `obj.dimensions` 비교, scene_audit `size_out_of_range` | `box()`처럼 치수를 메시에 굽거나 `size=2` 규칙 |
| 실린더 방향 틀림 | Euler 축·순서 오류 | bbox가 스펙의 두 점과 맞는지 비교 | `rod()`로 두 점 사이 생성 |
| 스케일 미적용·음수 스케일 | apply 누락, 미러링을 음수 스케일로 처리 | scene_audit `unapplied_scale`, `negative_scale` | transform apply 후 bevel 다시 적용. 음수 스케일을 적용한 뒤 노멀 재계산 |
| 뒤집힌 노멀 | 음수 스케일, boolean | validate.py flipped normal 검사(scene_audit는 검사하지 않음) | `bmesh.ops.recalc_face_normals` 또는 `normals_make_consistent(inside=False)` |
| non-manifold | 겹친 정점, 열린 구멍, 잘못된 boolean 입력 | scene_audit `non_manifold_edges` | merge by distance(1e-4), fill holes. boolean 전후로 개수 비교 |
| Z-fighting | 같은 평면에서 겹침 | 렌더 확인 | 0.1~0.5 mm 오프셋 또는 union |
| 비율 오류 | 스펙에서 벗어남, 레퍼런스 무시 | 스펙 `checks`, scene_audit 치수 규칙, 실루엣 IoU | 스펙 값으로 되돌리고 IoU 재측정 |
| CG 느낌(칼날 모서리) | bevel 누락 | 클로즈업 렌더 | 4장 스택 |
| 디테일 부족 | 하드웨어·이음새·두께 없음 | 5.3절 체크리스트 | meso 디테일 추가 |
| 없는 API 호출 | 버전 차이(`use_auto_smooth` 4.1 제거, Boolean `FAST`→`FLOAT` 5.0, EEVEE 식별자) | 오류 메시지 | 버전 명시, enum을 런타임에 읽기, API 조회 도구 사용 |
| 한국어 UI에서 이름 기반 코드 실패 | 노드·새 데이터 이름 번역 | KeyError/None | 노드는 `type`으로 찾기(예: `BSDF_PRINCIPLED`). Preferences > Interface > Translation에서 'New Data' 끄기([hideki711014 규칙](https://github.com/hideki711014/roo-blendermcp-jp-rules)). 오브젝트 이름은 코드에서 영어로 직접 지정 |

**자동 수정 매핑을 에이전트 규칙으로 주세요.** 증상마다 표준 처방이 정해져 있으므로 에이전트가 원인을 보고 바로 고칠 수 있습니다. 조명이나 재질로 결함을 가리는 것은 금지합니다. 물리적으로 말이 되는지 확인하는 QA 목록(떠 있는 쿠션, 받침 없는 조명, 바닥에서 뜬 가구, 구멍, 빛 샘, Z-fighting)은 [Unreal Home Wizard](https://raw.githubusercontent.com/amirmushichge/unreal-home-wizard/main/skills/unreal-home-wizard/SKILL.md)가 잘 정리해 두었습니다. 원칙은 "사용자는 1차 버그 탐지자가 아니다"입니다.

---

## 10. MCP·스킬 추천 (이 주제 관점)

| 이름 | 용도 | 상태 | 주의 |
|---|---|---|---|
| [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) (ahujasid, 구 blender-mcp) | 코드 실행으로 부품을 만들고 검사 스크립트를 실행, 뷰포트 캡처 | PyPI `mcp-for-blender` 2.1.0(2026-09-25), 약 29.4k★, MIT, 36개 tool. `uvx blender-mcp`도 호환 래퍼로 동작 | `execute_code` 전에 저장, 작업을 작게 나누기, 소켓 타임아웃 180초. 익명 텔레메트리 기본 ON(`DISABLE_TELEMETRY=true`). `BLENDER_MCP_SAFE_MODE=1`은 샌드박스가 아님. Tripo는 유료 Premium 전용. Hunyuan3D 연동은 한국 라이선스 제외 |
| Claude 공식 Blender 커넥터(Blender Lab) | 같은 용도의 공식 MCP | 커넥터 v1.0.1, 애드온 `blender_version_min` 5.1.0, GPL-3.0-or-later | **5.1 미만 불가.** 공식·커뮤니티 모두 localhost:9876을 써서 **동시에 켜면 충돌** ([02 Blender MCP](02_blender_mcp.md)) |
| [blend-ai](https://github.com/HoldMyBeer-gg/blend-ai) | 도구 186개, mesh 품질 분석(non-manifold, loose vertex, zero-area face, duplicate vertex) 내장 | Blender 4.2+(5.1에서 테스트), 148★ | **AGPL-3.0-or-later**. 샌드박스가 파일 쓰기를 막음. 도구가 많아 컨텍스트를 많이 씀 |
| [build123d-mcp](https://github.com/pzfreo/build123d-mcp) | 정밀 부품, fit·간섭 검사 | 0.3.90 | 단위 mm |
| [AgentCAD](https://github.com/jdilla1277/agentcad) | CAD 버전 관리, A/B diff, check-spec | 0.6.0 | Python ≤3.12 |
| [RobertCoop/openscad-mcp](https://github.com/RobertCoop/openscad-mcp) | 조립 간섭·클리어런스 검사 | MIT | CSG 메시는 Blender 후처리 필요 |
| [ProfRino Assembly Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill) | 조립 규칙(6장) | 약 72★ | LICENSE 없음 |
| [blender-image-to-3d](https://github.com/majidmanzarpour/blender-game-skills) | 컨셉 아트 → 게임 에셋, 11단계(0~10) 게이트, IoU·비율 게이트, validate.py | MIT, 2026-09-24 커밋 1개, 90★. Blender 4.2~5.2 표기 | 커뮤니티 검증 이력이 없는 새 저장소(Claude 공동 커밋). 규칙은 참고용. init_master의 문틀 1.0×2.2 m는 한국 2.1 m로 조정 |
| [blender-production](https://github.com/per-simmons/blender-production) | 빌드 순서, 증거 기반 QA, 결함 원장, macro/meso/micro | MIT, Blender 5.1.2+, 커밋 1개, 0★ | 성숙도가 낮음. 건축·렌더 중심 |
| [cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) | Claude Code용 30개 스킬, 치수 참조표(7개 카테고리), 품질 개선 자동 루프 | v1.3.0, MIT, Blender 5.1.1 E2E 검증 | Sonnet 4.6 / Opus 4.7 / Haiku 4.5 시절 기준. bevel 기본 0.02 m는 가구에 큼 |
| 이 저장소 [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md) | 스펙 → 빌드 → 감사 → 검토 루프 | — | [scene_audit.py / placement_utils.py / review_views.py](../03_playbooks/scripts/README.md)와 연결 |

설치와 보안 설정은 [빠른 시작](../03_playbooks/01_quickstart_setup.md)을 보세요.

---

## 11. 모델 선택 (이 주제 관점, 요약)

자세한 비교와 가격은 [01 AI 모델·클라이언트](01_ai_models_and_clients.md)에 있습니다. 가구 모델링에 한정한 요점만 적습니다.

- **절대 순위는 없습니다.** GPT-6 Astra, Claude Fable 5.1, Opus 5.5를 **같은 가구 과제**로 비교한 공개 벤치마크는 찾지 못했습니다. 공개된 비교는 대부분 개인 테스트(n=1)이고 결과가 엇갈립니다. 한 예로 속도·토큰은 Astra, 제품 비율·디테일은 Opus 5.5, 기획·코드는 Fable을 선호한다는 보고가 있습니다([사례 모음](https://github.com/yangqiong/gpt6-astra-3d), 개인 테스트, n=1).
- **시스템 단위로 A/B 하세요.** 같은 스펙, 같은 MCP, 같은 검사 스크립트로 두 모델을 돌리고 FAIL 수, 반복 횟수, 비용을 비교합니다. 도구와 검증 루프의 효과가 모델 차이보다 큰 경우가 많습니다. build123d-mcp README는 도구만으로 한 모델의 CADGenBench 점수가 0.360에서 0.457로, validity가 88%에서 100%로 올랐다고 보고합니다(도구 저자 자체 보고, 모델명 미공개).
- **CADGenBench 비교는 공정한 모델 비교가 아닙니다.** [build123d-mcp 저자의 비교 문서](https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md)(2026-07~09, 81 fixture)에서 Opus 5(xhigh) 0.6771, GPT-5.6 Sol 0.5319, Gemini 3.7 Flash 0.5078이었고, 셋 다 80/81 valid였습니다. 그런데 Opus 값은 여러 제출 중 'best' 제출이고, MCP 버전(0.3.79~0.3.83), 하네스, 실행 시기가 모두 다르며, 비교한 사람이 도구 저자 본인입니다(도구 저자 자체 평가). GPT-6 Astra와 Fable 5.1은 포함되지 않았습니다.
- **effort를 명시하세요.** Codex에서 GPT-6 Astra의 기본 reasoning effort는 `low`입니다. 부품 수가 많은 조립이나 검증 단계에서는 명시적으로 올리세요. Opus 5.5의 기본 effort는 medium입니다. Anthropic은 Opus 5.5를 "vision과 computer use에 가장 좋은 Opus"라고 소개하므로, 렌더 비평 역할의 후보로 고려할 만합니다.
- **역할을 나누면 쌉니다.** cc-blender-skill 저자는 테스트는 Haiku, 패치는 Opus로 나눠 약 10배 저렴하게 운용했다고 보고합니다(작성자 보고).

---

## 12. 2026 사례

| 사례 | 누가·언제·모델 | 어떻게 | 결과·한계 | 신뢰도 |
|---|---|---|---|---|
| [kitchen-twin](https://github.com/Frank-ZY-Dou/kitchen-twin) | Zhiyang (Frank) Dou, 2026-09-11, GPT-6 Astra | 휴대폰 워크스루 → metric scan → 인스턴스 분할 → 에셋별 치수 측정 → Astra가 **작은 Blender 모델링 언어**로 에셋마다 코드 작성 → **독립 verifier 세션**이 프레임·스캔과 대조("must justify every complaint with a frame") | 에셋 32개, 작동 조인트 138개, scene.glb 약 15 MB. 저자가 밝힌 한계: "thin and shiny things are still weak, a few objects are drafts, the room shell needs another pass". 파이프라인 비공개 | 결과물은 README로 확인. 방법은 재현 불가. DSL 구조를 "parts / joints / dimensions"로 적은 원자료 요약은 각색이라 쓰지 않음 |
| [IKEA 의자 사진 1장 → 인터랙티브 제품 모델](https://www.linkedin.com/posts/doron-taussy_i-gave-astra-one-photo-of-an-ikea-chair-and-activity-7503069971481182209-ay6a) | Doron Taussy, 2026-09-08, GPT-6 Astra | 사진 한 장으로 치수, 재질 전환, 부품 검사, 분해도, flat-pack, 자가 조립까지 | 가구 부품 분해 주제에 가장 직접적인 사례 | 작성자 자기 보고 |
| Tom Krcha 연작 ([주택](https://x.com/tomkrcha/status/2095598645190291775), [기관차](https://x.com/tomkrcha/status/2095756085890310311)) | 2026-09-03~09, GPT-6 Astra | 집 사진 한 장 → 가구·가전·장난감이 각각 분리된 편집 가능 씬. 증기기관차 그림 → 이름 붙은 기계 어셈블리. "primarily MCP, with occasional computer-use checks" | 기관차는 오브젝트 3,295개. Porsche 서브디비전 실험(2026-09-09)의 교훈: **"Naive prompts will fail, refined systematic prompts written by an expert succeed"** | 작성자 주장. X 원문은 큐레이션 목록 경유로만 확인. 치수 정확도는 검증되지 않음 |
| [Unreal Home Wizard](https://github.com/amirmushichge/unreal-home-wizard) | AmirMušić, 2026-09-21, Codex용 스킬(사례 목록상 GPT-6 Astra) | 매물 사진 20장 + 파노라마 → UE 5.8 워크스루. 사진 재현 모드(임의 재디자인 금지). 보이는 모든 오브젝트의 지지·고정·배치를 개별 검증 | 러프 레이아웃과 최종 뷰의 2단계 승인. 스케일 앵커는 천장고나 문 폭 같은 알려진 치수 하나 | 저장소로 확인. Sol·Opus 5.5 언급은 원문에 없음(정정) |
| [Realsee 스캔 복원](https://github.com/realsee-developer/realsee-astra-blender) | realsee-developer, 2026-09-15, GPT-6 Astra(Codex), Blender 5.2.1 | 공개 프롬프트: 공간 연결 이해 → 구조 → 주요 가구 → 소품. 근거 없는 방은 만들지 않고 불확실한 곳은 기록. 저장 후 다시 열어 벽·문이 실제로 편집되는지 확인 | 입력 396개 파일(5.66 GiB)과 프롬프트 공개. 스크립트는 공간 전용 | 높음(코드 MIT, 데이터 권리 별도) |
| [retriever](https://github.com/openretriever/retriever) | Linfeng Zhao | Stanford 주방 영상 → MuJoCo 씬(작동 서랍) | 런타임 코드 공개. kitchen-twin과 같은 계열 | 저장소 공개 |
| [blender-production](https://github.com/per-simmons/blender-production) Fallingwater | Pat Simmons, 2026-09 | 세션 확인 → 브리프를 검사 기준으로 변환 → 의존 순서대로 빌드 → 렌더 벤치마크 → 증거 기반 QA와 결함 원장 | 사례 목록에 "54 hours of unattended compute"라는 인용이 있음 | 수치는 저자 주장. 저장소 성숙도 낮음 |
| [CADGenBench 제출](https://github.com/pzfreo/cadgenbench-build123d) | pzfreo, 2026-07~09 | 과제 유형별 범용 프롬프트(checkpoint-first, validity-as-invariant) → MCP로 증분 빌드, measure, compare, validate. fixture별 튜닝 금지 | 11장 참고 | 도구 저자 자체 평가 |
| [평면도 → 가구가 있는 2층 주택](https://x.com/uncle_render/status/2103080046537904576) / [새 침대가 아이 방에 맞는지 확인](https://x.com/scheemunai/status/2103059885361598633) | 2026-09-24, Claude Opus 5.5 | Claude Code로 모델·뷰어 생성 / 가구 배치·치수 확인 | 세부 공정은 (미확인) | 낮음(원문 미열람) |
| [GPU 워크스테이션 사진 4장 → Blender 모델](https://x.com/superalesha/status/2096706133121540436) | Alexey Fateev, 2026-09-06, GPT-6 Astra와 Fable 5.1 | 같은 Blender MCP로 두 모델 비교 | 세부 결과 (미확인) | 개인 테스트, n=1 |
| [생성형 CAD 현황 노트](https://www.linkedin.com/posts/adammichaelkeating_astra-is-far-better-at-understanding-geometry-activity-7503061853816696832-7CRf) | Adam Keating, 2026-09-08 | 실무자 평가 | "looks like the thing you want"는 쉬워졌지만 **"The gap remains in the last mile - particularly in manufacturing"** | 개인 의견 |

**사례에서 반복되는 교훈**

1. **치수 기반 중간 표현과 독립 검증 세션**이 정확한 가구·수납 재현의 핵심입니다(kitchen-twin). 검증자에게는 "불만마다 프레임 증거를 대라"는 규칙을 줍니다.
2. **구조 → 주요 가구 → 소품** 순서로 만들고, 근거 없는 것은 지어내지 않고 기록합니다(Realsee).
3. **프롬프트는 전문가가 쓴 체계적인 스펙이어야 합니다**(Tom Krcha). 이 문서의 스펙 우선 방식이 같은 이야기입니다.
4. **얇고 반짝이는 부품, 제조 수준의 마지막 정밀도**는 아직 사람 몫입니다(kitchen-twin 저자, Adam Keating).
5. 공개 사례 가운데 수치로 독립 검증된 'AAA급' 가구 결과물은 없습니다. 목표는 [스펙 + 코드 + 검사 루프 + 사람의 마무리]입니다.

더 많은 사례는 [사례 모음](../04_case_studies/01_case_studies.md)에 있습니다.

---

## 13. 프롬프트 예시

재사용 템플릿 전체는 [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md)에 있습니다.

**A. 스펙 우선 킥오프 (한국 아파트 4인 식탁 세트)**

```text
너는 Blender {bpy.app.version_string} bpy로 가구를 만드는 시니어 하드서피스 모델러다.
규약: 단위 m, Z-up, 앞면 -Y, 가구마다 Empty 루트(바닥 중심) 아래에 부품을 자식으로, 부품 이름은 영어 <category>_<part>_<pos>.
지역: KR. 치수는 03_playbooks/05_reference_dimensions.md의 KR 값을 따른다(식탁 상판 0.72~0.75, 의자 좌판 윗면 0.43~0.46, 상판−좌판 0.25~0.305).

1단계(코드 금지): 식탁 1개와 의자 4개의 JSON 스펙만 출력해.
 - parts: name, type(box|rod), size 또는 p0/p1/radius, center
 - connections: 설계상 붙어야 하는 부품 쌍(연결 맵). 결합부 겹침은 5~15 mm로만.
 - checks: 좌판 윗면, 상판 높이, 전체 높이 범위
 - omitted: PartNet 계층(chair_back / chair_seat / chair_base(leg, bar_stretcher) / chair_arm, tabletop / leg / apron / stretcher) 중 생략한 것과 이유
 - 두께: 상판 0.03 오크, 에이프런 0.08×0.022(상판 가장자리에서 0.04 안쪽), 다리 0.055 각재, 의자 다리 0.035, 좌판 0.03
내가 승인하면 2단계로 간다.

2단계: 부품 하나에 호출 하나로 빌드(get-or-create, 재실행해도 결과 동일). 스케일은 메시에 굽고 오브젝트 scale=1.
큐브를 쓸 거면 size=2 + half-extent 규칙, 두 점을 잇는 부재는 Euler 회전 대신 두 점 사이 bmesh.
3단계: check_assembly()와 scene_audit.audit_scene(floor_z=0)를 실행해 결과를 그대로 보여 줘. 빈 목록이 될 때까지 고쳐.
4단계: 그다음에만 bevel(원목 2 mm, 3 seg, 30°, harden normals) + Weighted Normal. 의자는 식탁 아래로 0.10 넣어 배치.
5단계: review_views로 top/front/side/persp를 렌더하고 인체 더미(1.725 m)와 함께 제출. 결함은 원장에 기록하고 한 번에 하나만 고쳐.
숫자가 통과해도 이미지가 틀리면 실패다. 증거 없이 완료를 주장하지 마.
```

**B. VLM 검수 질문 (CADCodeVerify 방식)**

```text
원래 요청: <요청 원문>. 스펙: <JSON>.
1) 먼저 이 요청의 충족 여부를 판정할 예/아니오 질문 10개를 만들어라.
   구조, 부품 수, 접촉, 비율, 대칭, 두께, 모서리, 재질 경계를 반드시 포함한다.
2) 첨부한 Image 1: top, Image 2: front, Image 3: side, Image 4: persp를 보고
   각 질문에 [예 | 아니오 | 불확실] + 근거(어느 이미지의 어느 위치)로 답하라.
3) "아니오"만 우선순위순으로 수정 지시로 바꿔라. 지시에는 부품 이름과 수치(m)를 넣는다.
관대하게 판정하지 마라. 확신이 없으면 "불확실"로 답하고, 확인하려면 어떤 추가 뷰가 필요한지 적어라.
```

**C. 정점 직접 입력 금지 규칙 (프로젝트 규칙 파일에)**

```text
정점 좌표를 직접 나열하지 말고 primitive, modifier, bmesh 연산으로 구성하라.
정점을 직접 다루는 것은 프로파일 커브(단면 폴리라인 20점 이하)에만 허용한다.
유기 형상은 SDF / metaball / Mesh to Volume으로 만들고 remesh하라.
```

---

## 흔한 실수와 해결

| 실수 | 결과 | 해결 |
|---|---|---|
| 코드부터 쓰게 함 | 좌표 즉흥 계산으로 부품이 떠 있거나 파고듦 | 스펙 JSON → 승인 → 코드 (2.3절) |
| 스케일을 적용하기 전에 bevel·solidify를 검 | 축마다 폭이 달라짐 | transform apply 후 스택 적용 |
| 부품을 부모 없이 흩어 놓음 | scene_audit가 좌판을 "떠 있음"으로 판정 | Empty 루트 아래 자식으로 |
| 커터를 뷰포트에 보이게 둠 | scene_audit가 커터를 별도 물체로 셈 | `hide_set(True)` + `hide_render=True` |
| 매트리스·침대를 이름으로 지정("King") | 지역이 섞임(한국 1,600 vs 미국 1,930) | mm 값으로 지정 |
| 한국 씬에 미국 기본값(천장 2,438, 조리대 914, 상하부장 간격 457)을 씀 | "한국 집 같지 않은" 비율 | 지역 프리셋 분리(KR 구축·신축 / US) |
| Infinigen·Archimesh 기본값을 표준으로 씀 | 좌면이 0.47~0.54 m로 높음, 조리대 0.88 m | 구조만 참고하고 치수는 기준표 |
| 문짝 치수로 벽을 자름 | 문틀이 들어갈 자리가 없음 | 벽 boolean은 개구부(문틀 외곽) 치수 |
| 4.x 코드의 `solver='FAST'`를 5.0에서 실행 | enum 오류 | 런타임 enum 조회(코드 B) |
| cc-blender-skill의 bevel 0.02 m를 가구에 적용 | 얇은 판이 뭉개짐 | 재질별 폭(4.2절) |
| VLM에게 "괜찮아 보여?"라고 물음 | 관대한 통과 | 결정적 검사 먼저, 예/아니오 질문 |
| 여러 결함을 한 번에 고침 | 회귀 | 결함 원장, 하나씩, 같은 카메라로 재렌더 |
| 비상업 연구 코드(LL3M, CAD-Recode, Text2CAD, LLaMA-Mesh, ShapeAssembly, PartPacker)를 상업 파이프라인에 넣음 | 라이선스 위반 | 아이디어만 차용 |
| 한국에서 Hunyuan3D-Part·Hunyuan3D 로컬 가중치로 조형물 생성 | 라이선스 범위 밖, 출력물 사용도 제한 | [04 AI 3D 생성](04_ai_3d_generation.md)의 한국용 조합 |
| 공식 Blender 커넥터와 ahujasid 서버를 동시에 켬 | 둘 다 9876 포트라 충돌 | 하나만 켜기 |
| 도구마다 Python 버전 요구가 다른데 한 venv에 설치 | 설치 실패 | 도구별 venv(bpy 5.1+ 3.13, AgentCAD ≤3.12, Infinigen 2.0 3.11) |

---

## 관련 문서

- [컴퓨터 유즈 vs MCP vs 스크립트](12_computer_use_and_other_methods.md): 스컬프트·유기체를 컴퓨터 유즈로 할 수 있나
- [00 목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [01 AI 모델·클라이언트](01_ai_models_and_clients.md): 모델별 역할, effort, 비용
- [02 Blender MCP](02_blender_mcp.md): 공식 vs ahujasid, 보안, 버전별 API 함정
- [03 기타 DCC·CAD·엔진 MCP](03_other_mcp_dcc_cad_engines.md): Fusion, SketchUp, FreeCAD, 엔진 쪽 모델링
- [04 AI 3D 생성](04_ai_3d_generation.md): 파트 생성, 생성기 선택, 한국 라이선스
- [05 텍스처링·재질](05_texturing_materials.md): 부품별 재질, UV, bake
- [06 라이팅·렌더·아트디렉션](06_lighting_rendering_art_direction.md): 마이크로 bevel과 하이라이트, 렌더 검사
- [08 배치·레이아웃](08_scene_layout_placement.md): 만든 가구를 방에 놓기, 간격 규칙
- [09 에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 스킬, 비용
- [10 에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md): 에셋 라이브러리, 익스포트, 법규
- [11 학술 연구](11_research_papers.md): LL3M·CAD 코드 생성·레이아웃 연구 전체
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [치수 기준표](../03_playbooks/05_reference_dimensions.md)
- [보조 스크립트](../03_playbooks/scripts/README.md)(`scene_audit.py`, `placement_utils.py`, `review_views.py`) · [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- `01_research/raw/08_modeling-objects.research.json`: 치수 표준, 모델링 접근법, 모디파이어, 부품 분해, 유기 조형, 연구, 실패 모드, 사례 조사
- `01_research/raw/08_modeling-objects.verify.json`: 독립 검증. Infinigen 좌면 높이 해석 정정, FLOATING 오탐, validate.py WARN/FAIL 정정, 연구 코드 비상업 라이선스(LL3M·CAD-Recode·Text2CAD·LLaMA-Mesh·ShapeAssembly·PartPacker), Hunyuan3D-Part 한국 제외, CADGenBench 비교의 한계, kitchen-twin DSL 각색 지적. 누락 항목(ProfRino, IKEA 의자, Tom Krcha 교훈, Adam Keating, retriever, realsee, PartCrafter-Scene, cc-blender-skill)
- `01_research/raw/G1_dimensions.gap.json`: 실측 치수 약 136행(KR/US/EU)과 치수 노하우
- `01_research/raw/G1_dimensions.verify.json`: 치수 검증. 공동주택 계단참 2 m 정정, 천장고 신축 2.4~2.5 m, 매트리스 K/LK 브랜드 편차, 문틀·문짝 구분, DIN 18101, NKBA 식탁 뒤 여유 3단계
- 보조로 참고한 원자료
  - `02_blender-mcp.research.json`: 노드를 type으로 찾는 규칙, cc-blender-skill 스택
  - `07_aaa-rendering-lighting.research.json`, `07_aaa-rendering-lighting.verify.json`: 마이크로 bevel 0.5% 규칙
  - `10_agent-workflow.research.json`, `10_agent-workflow.verify.json`: 모디파이어 순서, 겹침 5~15 mm, 현지화 UI, reference-analysis-validator 기준
  - `11_case-studies.research.json`, `11_case-studies.verify.json`: ProfRino, Realsee, Tom Krcha, cc-blender-skill
  - `13_research-papers.research.json`, `13_research-papers.verify.json`: Procedura, LL3M 라이선스·retire, BlenderGym 정정
- 이 문서의 코드 A·B와 수치 결과는 작성 중에 Blender 4.2.23 LTS와 5.0.1(pip `bpy`, 헤드리스)에서 직접 실행해 확인했습니다(2026-09-27).

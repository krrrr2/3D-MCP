# 인체·유기물·건물 전용 도구 가이드

> 기준일: 2026-09-27 · 원자료: [`G9_human_character`](../01_research/raw/G9_human_character.gap.json), [`G10_organic_nature`](../01_research/raw/G10_organic_nature.gap.json), [`G11_architecture`](../01_research/raw/G11_architecture.gap.json), [`G12_tool_safety`](../01_research/raw/G12_tool_safety.gap.json)과 각 `.verify.json`(원문 대조)
> 조사는 읽기 전용으로만 했습니다. 파일을 받거나 설치·실행하지 않았습니다. GitHub·PyPI는 직접 확인했고, 차단된 사이트(extensions.blender.org, Superhive, arXiv, Hugging Face, 벤더 사이트)의 내용은 **(검색 요약)**으로 표시했습니다. 날짜·라이선스 일부는 git 메타데이터와 LICENSE 원문으로 다시 확인했습니다(각 `.verify.json`).

## 핵심 요약

- **세 분야 모두 같은 결론입니다. AI에게 형태를 "직접 빚게" 하지 말고, 검증된 생성기를 "호출"하게 하세요.**
  - 인체는 **파라메트릭 인체 모델**, 나무는 **파라메트릭 나무 생성기**, 유기 조형은 **SDF**, 건물은 **의미 객체(IFC)나 건축 애드온**으로 만듭니다.
  - 에이전트는 파라미터를 고르고, 결과를 **숫자로 검사**합니다.
  - 실사용 평가에서도 같은 결과가 나왔습니다. 에이전트는 서랍장·나선 계단은 잘 만들지만 옹이 진 그루터기나 제대로 리깅된 인물은 어렵습니다(검색 요약).
- **인체** 👤
  - 무료 1순위는 **MPFB2**입니다(MakeHuman의 Blender 판). GPLv3 코드, 에셋·출력은 별도 조항이고, 2026-09-26까지 커밋이 이어졌습니다. bpy로 부를 수 있습니다.
  - 새로 나온 상업 친화 인체 모델은 **Anny**(NAVER, Apache-2.0, 0.6.0 2026-08)와 **MHR**(Meta, Apache-2.0)입니다.
  - **SMPL-X는 비상업 라이선스**이니 상업 작업에는 빼세요.
- **유기물** 🌿
  - **Blender 5.0부터 SDF 노드가 기본으로 들어 있습니다**(직접 확인). 5.0.1에 30종, 5.2.2에 37종이 있고, 대표적인 것은 Mesh to SDF Grid, SDF Grid Boolean/Fillet/Offset, Grid to Mesh입니다. 애드온 없이 매끄러운 유기 조형을 만들 수 있습니다.
  - 나무는 Sapling·Modular Tree(무료), The Grove(유료) 같은 생성기에 맡기세요.
- **건물** 🏠
  - **생성기보다 검증기가 중요합니다.** IFC 편집 벤치마크(BIM-Edit, 2026-06)에서 최고 모델 평균이 49.48%였습니다(검색 요약). 성과를 낸 사례는 모두 **규칙 검사기와 반복 수정 루프**를 붙였습니다.
  - Blender 쪽 최선의 오픈 조합은 **Bonsai + IfcOpenShell**입니다. IfcOpenShell은 **공식 MCP 서버**(PyPI `ifcopenshell-mcp` 0.8.5)도 냅니다.
- **떠 있는 부품이 1순위 실패입니다.** 나무·바위·가구·부품 모두 같습니다.
  - 표면 위에만 분포시키고, 배치 뒤 **레이캐스트로 접촉을 검사**하세요.
  - 한 사례에서는 나무가 떠 보인 원인이 두께 0인 지면의 착시였고, 이를 측정으로 가려냈습니다(검색 요약).
- **한국 사용자 라이선스 주의**
  - **Hunyuan3D 2.1·Omni** 라이선스는 한국에 적용되지 않습니다(LICENSE 원문). 이를 입력으로 쓰는 파생 파이프라인(UltraShape 등)도 같습니다.
  - 대안은 TRELLIS.2(MIT), TripoSG(MIT), Direct3D-S2(MIT), Step1X-3D(Apache-2.0)입니다.
- **보안**
  - 이 분야 유료 애드온의 **크랙판이 검색 상위에 넘칩니다.** Human Generator, Auto-Rig Pro, Quad Remesher, SDF.R, Botaniq, Archipack, SceneCity 등입니다.
  - GitHub에는 **README 링크가 모두 한 zip으로 가는 가짜 "Blender MCP" 저장소**도 있습니다.
  - 공식 스토어·원 저장소에서만 받고, [설치 안전 가이드](14_tool_install_safety.md)의 점검표를 따르세요.

---

## 0. 공통 작업 원칙

| 원칙 | 인체 | 유기물 | 건물 |
|---|---|---|---|
| 형태는 생성기로 | MPFB2·Anny·HumGen3D 베이스 → 매크로(나이·성별·키·체중·근육) 조정 | 나무 생성기, Infinigen 팩토리, SDF 노드 | Bonsai(IFC)·Home Builder 5·Building Tools, 또는 도면 입력 |
| 에이전트의 역할 | 설명 → 파라미터 번역, 의상·디테일 | 수종·지형 서술 → 파라미터 번역 | 방 연결 그래프 + 면적 JSON 작성 |
| 숫자 검사 | 비례(양팔 폭 ≈ 키), 리그·가중치 규칙, 자기교차 | 지면 접촉(레이캐스트), 겹침(최소 간격) | 방 도달 가능성(그래프), 문–벽 관계, 계단·통로 규칙 |
| 사람 승인 | 형상(4방향) → 리토폴 → 텍스처 → 5포즈 변형 테스트 | 실루엣·밀도 | 평면(2D) 승인 후 3D화 |

이 저장소의 [`scene_audit.py`](../03_playbooks/scripts/README.md)(부유·관통), [`building_audit.py`](../03_playbooks/scripts/README.md)(건축 상식), [`review_views.py`](../03_playbooks/scripts/README.md)(4방향 렌더)는 세 분야 모두에 그대로 쓸 수 있습니다.

---

## 1. 인체·캐릭터

### 1.1 파라메트릭 인체 베이스 (여기서 시작)

| 도구 | 라이선스·상업 이용 | 최신성 | 에이전트 사용 | 안전 신호 |
|---|---|---|---|---|
| [MPFB2](https://github.com/makehumancommunity/mpfb2) | 코드 GPLv3, 에셋·출력은 별도 조항(에셋 CC0, 출력은 사용자 소유, 조사 요약) | v2.0.17(2026-07-22), 마지막 커밋 2026-09-26(확인) | 공식 스크립트 샘플 `HumanService.create_human()`, `TargetService.load_target()`. 확장 설치 위치에 따라 import 경로가 달라지므로 샘플의 동적 import 방식을 그대로 씀 | 양호 |
| [Anny](https://github.com/naver/anny) (NAVER LABS Europe) | Apache-2.0(LICENSE 확인), MakeHuman 유래 에셋 CC0 | PyPI 0.6.0(2026-08-07, 확인) | 영유아~노인, WHO 통계로 보정된 파라메트릭 인체. Python 패키지 | 양호 |
| [MHR](https://github.com/facebookresearch/MHR) (Meta) | Apache-2.0(확인) | 2026-09 커밋(확인) | 인체 리그 모델. 아래 SAM 3D Body의 출력 형식 | 양호 |
| [HumGen3D](https://github.com/OliverJPost/HumGen3D) (Human Generator) | 애드온 코드 GPL-3.0, 에셋 팩은 유료 | 2026 갱신(검색 요약) | 파이썬 API가 있음 | 양호. **크랙판 주의** |
| [CharMorph](https://github.com/Upliner/CharMorph) | 코드 AGPL/GPL 혼재, 캐릭터별 에셋 라이선스 | 마지막 커밋 2024-10(확인) → 사실상 정체 | 가능 | 주의(정체) |
| [SMPL/SMPL-X](https://github.com/Meshcapade/SMPL_blender_addon) | **비상업 학술 라이선스**(검색 요약). Epic의 Meshcapade 인수(2026-02) 뒤 상업 경로 불투명(검색 요약) | 애드온 GitHub판 2023 이후 중단 | 연구에 널리 쓰임 | 라이선스 위험 |

- **상업 작업에서 뺄 것**: SMPL-X에 의존하는 도구입니다(LHM, PSHuman, VPoser, GVHMR 경로). 대신 MPFB2, Anny, MHR + SAM 3D Body 조합을 쓰세요.
- **다른 생태계에서 가져오기**:
  - MetaHuman: UE 5.6부터 표준 UE EULA(검색 요약). [Character DNA 애드온](https://github.com/poly-hammer/meta-human-dna-addon)으로 Blender에서 편집
  - Character Creator: [CC/iC Blender Tools](https://github.com/soupday/cc_blender_tools)
  - VRoid: [VRM 애드온](https://github.com/saturday06/VRM-Addon-for-Blender)
  - Daz: [Daz to Blender](https://github.com/daz3d/DazToBlender)

  모두 원 저장소·공식 사이트에서 받으세요.

### 1.2 사진·텍스트 → 인체

| 도구 | 설명 | 라이선스 |
|---|---|---|
| [SAM 3D Body](https://github.com/facebookresearch/sam-3d-body) (Meta, 2025-11) | 사진 한 장 → MHR 인체. 현재 가장 실용적 | SAM License(2025-11-19판, 확인). 상업 허용, 일부 용도 금지(조사 요약) |
| [SOMA-X](https://github.com/NVlabs/SOMA-X) (NVIDIA) | SMPL·MHR·Anny·MANO를 한 토폴로지·리그로 묶음 | Apache-2.0(확인). 선택 백엔드는 각자 라이선스 |
| 상용: Tripo 3.x, Meshy 6, Rodin Gen-2/2.5 | T/A 포즈 강제, 자동 리깅, 애니메이션 프리셋(검색 요약). 공식 MCP 있음([Meshy MCP](https://github.com/meshy-dev/meshy-mcp-server), [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp)) | 서비스 약관 |
| [TRELLIS.2](https://github.com/microsoft/TRELLIS.2) | 오픈 이미지→3D. 한국에서 쓸 수 있는 대안 | MIT |
| [Hunyuan3D 2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) / Omni | 2.1(2025-06), Omni(2025-09). 3.x는 오픈 가중치 없음 | **한국 제외**(LICENSE 원문) |

- AI로 만든 인체는 **얼굴·손·여러 겹 의상에서 반복적으로 실패합니다**(실제 파이프라인 사례: 눈이 둘로 겹침, 코 위치 어긋남, 얇은 수염이 막대로 뭉개짐).
  - 얼굴은 따로 다룹니다. 머리 전용 고해상도 생성을 하거나 파라메트릭 머리로 교체하세요.
  - 텍스처로 얼굴 구조를 그려 넣지 마세요.
- 입력 이미지는 **정면 전신, 중립 조명, T-포즈**를 씁니다. T-포즈가 오토리거와 가장 잘 맞습니다. 어깨 변형이 중요하면 A-포즈를 씁니다.

### 1.3 리깅

| 도구 | 설명 | 라이선스 |
|---|---|---|
| Rigify (Blender 내장) | 실무 기준 | GPL |
| AccuRIG 2 (Reallusion, 무료) | 인체 오토리깅(검색 요약) | 무료, 콘텐츠 EULA |
| Auto-Rig Pro (유료, Superhive) | 여러 겹 의상에 voxel 바인딩 | 상용. **크랙판 주의** |
| [UniRig](https://github.com/VAST-AI-Research/UniRig) (SIGGRAPH 2025) | 학습형, 헤드리스 CLI, 8 GB 이상 GPU | MIT(확인) |
| [SkinTokens](https://github.com/VAST-AI-Research/SkinTokens) (2026) | 학습형 스키닝, GLB 입출력, 14 GB 이상 GPU | MIT(확인) |
| [Puppeteer](https://github.com/Seed3D/Puppeteer) (NeurIPS 2025) | FBX 내보내기 지원 | Apache-2.0 |
| Mixamo | 무료지만 오래 정체, 전용 본 이름이라 리타깃 필요(검색 요약) | Adobe 약관 |

학습형 리거(UniRig, SkinTokens)는 컴파일이 필요한 의존성(flash-attn, spconv)과 큰 GPU가 필요하고, 얼굴 리그는 만들지 않습니다.

### 1.4 인체 검사 (전용 애드온은 없음 → 수치 게이트)

에이전트 저장소들이 실제로 쓰는 검사입니다(blender-kiln, [mixamo-llm-mocap](https://github.com/squall01337/mixamo-llm-mocap), reference-asset-compiler).

1. **비례**: 양팔 폭 ≈ 키. 이 검사 하나로 두개골에 박힌 어깨, 잘못된 본 축, 팔을 반대로 내리는 부호 오류를 잡았다는 보고가 있습니다. 보조 기준도 있습니다: 가랑이 ≈ 키의 절반, 성인 7.5~8등신(일반 캐논, 검색 요약).
2. **리그·가중치 규칙**
   - 아마추어 스케일 1
   - 변형 루트 본 1개
   - 본 이름에 공백·특수문자 없음
   - 버텍스당 영향 본 4개 이하
   - 무가중치 버텍스 0
   - "버텍스 수 ÷ 변형 본 수" 5 이상. 370버텍스 저폴리 인물에 본 160개짜리 Rigify를 씌우자 머리가 떨어졌습니다.
3. **리그 치수 기록**: 상완·전완·대퇴·정강이 길이, 힙·머리 높이를 월드 좌표로 측정해 JSON에 남깁니다. 측정 전에 `view_layer.update()`를 호출합니다.
4. **5포즈 변형 테스트 + 자기교차 검사**: 포즈를 적용한 메시에 `BVHTree.overlap()`을 써서 부위 간 교차를 셉니다.
5. **내보내기**
   - Rigify는 포징 전에 팔다리의 IK_FK 속성을 1.0으로 둡니다. 기본값이 IK라 FK 컨트롤이 무반응입니다.
   - 레스트 포즈를 적용한 뒤 내보냅니다.
   - glTF는 변형 본만 내보냅니다. 한 사례에서 조인트가 865개에서 319개로 줄었습니다.
   - FBX 루트 본에 100배 스케일이 남는 문제를 확인합니다.
6. **여러 겹 의상**: 자동(heat) 가중치를 기대하지 마세요. voxel 바인딩이나 프록시 가중치 전사를 씁니다.

---

## 2. 유기물·자연·조형물

### 2.1 나무·식물

| 도구 | 가격·라이선스 | 비고 | 안전 |
|---|---|---|---|
| Sapling Tree Gen | 무료, 공식 Extension(GPL, 검색 요약) | 순수 Python, 스크립트로 호출 쉬움 | 양호(공식 확장에서만 받기) |
| [Modular Tree](https://github.com/GoodPie/modular_tree) | 무료, 애드온 GPLv3 / 코어 MIT | 노드 기반, **C++ 네이티브 코어 포함** | 주의: 이름 비슷한 포크 다수 → 원 저장소 릴리스만 |
| [Spacetree](https://github.com/varkenvarken/spacetree) | 무료(공간 식민 알고리즘) | Extension 등록(검색 요약) | 양호 |
| The Grove 2.3 | 유료(2026-03, Blender 5 지원, 검색 요약) | 성장 시뮬레이션 기반 고품질 | 공식 판매처만 |
| SpeedTree | Unity 구독(Learning판 무료·export 불가, 검색 요약) | 업계 표준 | 공식만 |
| [Infinigen](https://github.com/princeton-vl/infinigen) 자연 팩토리 | BSD-3 | 나무·바위·산호·생물·지형. **`nature-stable` 태그(bpy 3.6)** 버전으로 안내됨. 전용 환경에서 OBJ/USD/FBX로 뽑아 가져오는 "에셋 공장" 방식이 현실적 | 양호(환경 격리) |

에이전트에게는 "원기둥을 쌓아 나무를 만들라"가 아니라 **"수종 설명을 생성기 파라미터로 옮기라"**고 시키세요(Foliager 방식).

### 2.2 유기 조형·생물: SDF가 기본

- **Blender 5.x 내장 SDF 노드**(확인)로 비파괴 유기 조형을 만듭니다.
  - 순서: Mesh/Points to SDF Grid → **SDF Grid Boolean**(합치기) → **SDF Grid Fillet/Offset**(이음매 둥글게) → Mean/Median(다듬기) → **Grid to Mesh** → 리토폴로지
  - [07 모델링 가이드 7절](07_modeling_objects_furniture_sculpture.md)의 "스무스 유니온 → 복셀 리메시" 순서를 지오메트리 노드 안으로 옮긴 것입니다.
- 유료 SDF 애드온(SDF.R, Chisel)은 강력하지만 폐쇄형 네이티브 바이너리이고 **크랙판이 넘칩니다**. 쓰려면 Superhive 정품만 쓰세요.
- 메타볼은 빠른 덩어리 스케치용으로만 쓰고, 결국 SDF나 리메시로 넘깁니다.
- 큰 지오메트리 노드 그래프를 에이전트가 처음부터 짜게 하지 마세요. 노드가 몇 개를 넘으면 연결 오류가 흔합니다(검색 요약). 검증된 노드 그룹을 append하고 입력만 바꾸게 하세요. 노드 이름은 공식 Blender MCP의 API·매뉴얼 검색으로 확인시킵니다.

### 2.3 지형·스캐터

| 도구 | 비고 |
|---|---|
| A.N.T. Landscape (무료, Extension) | Blender 안에서 지형 + 침식 |
| Gaea 2.x / World Creator 2026 | 전용 지형 툴(유료, 무료판은 비상업·export 제한, 검색 요약). heightmap과 침식 마스크(flow·slope)를 스캐터 밀도·재질 블렌드에 재사용 |
| Blender 5.0 기본 **Scatter on Surface** 에셋 | 에이전트용 기본 분포로 충분 |
| Geo-Scatter 5.6(유료) + Biome-Reader(무료), Botaniq(유료) | 생태 규칙(경사·고도·충돌) 내장. **Botaniq 크랙판 주의** |
| [OpenScatter](https://github.com/GitMay3D/OpenScatter) | 무료였으나 **2026-08 보관(유지보수 중단)**(조사 기록) |

스캐터 규칙은 다섯 가지입니다.
1. 표면 분포로만 만듭니다(공중 좌표 금지).
2. 법선에 맞춰 세웁니다.
3. 뿌리를 지면 아래로 살짝 묻습니다.
4. 큰 것(나무·바위)을 먼저 놓고 그 주변을 밀도에서 뺍니다.
5. 최소 간격(Poisson)을 지킵니다.

배치 뒤에는 모든 인스턴스에서 아래로 레이캐스트해 접촉 거리를 표로 확인합니다.

### 2.4 이미지→3D (유기물)

- **한국에서 쓸 수 있는 오픈 모델**
  - [TRELLIS.2](https://github.com/microsoft/TRELLIS.2)(MIT, 큰 GPU 필요)
  - [TripoSG](https://github.com/VAST-AI-Research/TripoSG)(MIT)
  - [Direct3D-S2](https://github.com/DreamTechAI/Direct3D-S2)(MIT)
  - Step1X-3D(Apache-2.0)
- **상용 서비스**: Rodin Gen-2.5(2026-05, 초고밀도 원본·쿼드 출력), Meshy-6, Tripo 3.1(모두 검색 요약). 공개 순위표는 방법론과 벤더에 따라 크게 흔들립니다.
- AI가 만든 유기 메시는 "원본"일 뿐입니다. 데시메이트 → 쿼드 리토폴로지(Quad Remesher 정품, 무료 [QRemeshify](https://github.com/ksami/QRemeshify)는 2024-10 이후 정체) → UV → 베이크를 거칩니다.

---

## 3. 건물·건축·평면·도시

### 3.1 가장 중요한 것: 평면을 먼저 검증하고 나서 3D로

2026년 연구와 실사례가 같은 방향을 가리킵니다.

1. 에이전트가 **방 연결 그래프(버블 다이어그램) + 방별 목표 면적 JSON**을 먼저 냅니다.
2. 방 폴리곤(미터)으로 구체화합니다.
3. **결정적으로 검사합니다.** 겹침, 면적 오차, **문을 통한 연결**, 외곽 경계를 봅니다.
4. 통과한 것만 3D(벽·문·창)로 세웁니다.

근거는 다음과 같습니다.
- 평면 생성 연구가 "검증 가능한 규칙을 보상으로" 쓰는 방식으로 옮겨 가고 있습니다(ACL 2026 RLVR 논문, CVPR 2026 FMLM, 검색 요약).
- 텍스트만으로 Claude에게 큰 평면을 만들게 한 테스트에서는 문 누락, 끊긴 방, 갑자기 생긴 계단이 반복됐습니다. 공식 SketchUp 커넥터 결과도 같았습니다(RoomSketcher·MindStudio, 검색 요약).
- 반대로 **기존 도면을 입력으로 주고** Claude Code + Blender로 3D화한 사례는 여러 번 수정해 이틀 만에 워크스루까지 갔습니다(검색 요약).

이 저장소의 [`building_audit.py`](../03_playbooks/scripts/README.md)는 4단계 뒤의 3D 검사(문·창·방 연결·동선·문 여는 방향)를 맡습니다.

### 3.2 Blender 건물 애드온

| 도구 | 라이선스 | 최신성 | 비고 |
|---|---|---|---|
| [Home Builder 5](https://github.com/CreativeDesigner3D/home_builder_5) | GPL-3.0 | 마지막 커밋 2026-09-26(확인) | Blender 5+ 전용으로 재작성. 벽·문·창·계단·평면도, 문 스윙. **2026년 가장 활발**. 무료인데도 "FULL 다운로드" 재배포 사이트가 있으니 공식만 |
| [Building Tools](https://github.com/ranjian0/building_tools) | MIT | 마지막 커밋 2025-05-16(확인) | 외관 생성에 강함. 공식 호환 표기는 Blender 4.0까지 |
| [Bonsai](https://extensions.blender.org/add-ons/bonsai/) (구 BlenderBIM) | GPL-3.0+ | 일일 빌드 계속(검색 요약) | **IFC 네이티브**. 벽·문·창·공간이 의미 객체로 생김 |
| Archipack 2.x | 유료(€49, 검색 요약) | 2.8.5, Blender 5.x 대응 주장 | **크랙판 주의** |
| [HiFi Architecture Builder](https://extensions.blender.org/add-ons/hifi-builder/) | 확장 페이지 GPL / GitHub MIT로 표기 불일치 | 2026(검색 요약) | 공식 확장판만 |
| Archimesh | GPL | 확장 플랫폼 "제한 지원" | 노후. 치수 기본값 참고용([치수표](../03_playbooks/05_reference_dimensions.md)) |

### 3.3 IFC로 만들면 검사가 쉬워진다

- 벽·문·창·방을 메시가 아니라 **IFC 의미 객체**(IfcWall, IfcDoor, IfcSpace, IfcStair)로 만들면 좋은 점이 있습니다. "문이 벽에 있는가"를 기하로 추정하지 않고 **개구부 관계로 직접** 확인할 수 있습니다.
- [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell)(LGPL)이 제공하는 도구:
  - **ifctester**: IDS 규칙 파일로 "모든 문에 폭·높이, 모든 공간에 용도"가 있는지 계약처럼 검사
  - **ifcclash**: 충돌 검사
  - **공식 MCP 서버 [ifcmcp](https://docs.ifcopenshell.org/ifcmcp.html)**: PyPI `ifcopenshell-mcp` 0.8.5, 2026-04-01(확인). 이름이 같은 제3자 패키지가 있으니 IfcOpenShell 조직 것인지 확인하세요.
- 검증 도구
  - [buildingSMART Validation Service](https://github.com/buildingSMART/validate)(MIT): 온라인 서비스는 파일이 외부로 전송되므로 민감한 프로젝트는 로컬로 돌리세요.
  - [TopologicPy](https://github.com/wassimj/topologicpy): 방·문 **도달 가능성 그래프**. 현관에서 모든 방에 갈 수 있는지, 침실을 거쳐야만 가는 욕실은 없는지 봅니다.
  - [JuPedSim](https://github.com/PedestrianDynamics/jupedsim): 피난 시뮬레이션.
- Blender + Bonsai용 MCP: [MCP4IFC](https://github.com/Show2Instruct/ifc-bonsai-mcp)(MIT), [Bonsai_mcp](https://github.com/JotaDeRodriguez/Bonsai_mcp)(MIT). 둘 다 코드 실행 도구가 있으니 로컬 전용으로 쓰고 작업 전에 저장합니다.
  - MCP4IFC 연구의 결론은 "IFC 생성은 가능하지만 의미적으로 견고하지 않다"입니다(검색 요약).
  - 에이전트에게는 임의 코드보다 `create_wall(시작, 끝, 두께)`, `create_door(호스트 벽, 오프셋, 폭, 스윙)` 같은 **고수준 도구**를 주는 편이 안정적입니다.

### 3.4 건축 MCP 공식판 현황 (2026-09)

| 제품 | 상태 |
|---|---|
| Autodesk Revit | Revit 2027 Public MCP **테크 프리뷰, 읽기 전용**(검색 요약) → 생성 결과를 **검사**하는 데 좋음 |
| McNeel Rhino | [RhinoAI](https://github.com/mcneel/rhinoai) 공식(Grasshopper 포함, 마지막 커밋 2026-09-26 확인) |
| Trimble SketchUp | Claude 공식 커넥터(원격, 2026-04) |
| Graphisoft Archicad | 공식판 "진행 중". 커뮤니티판만 있음 |

쓰기가 되는 Revit·Archicad MCP는 커뮤니티 제품뿐입니다. **커뮤니티 Revit MCP의 한 포크는 서명 없는 사전 빌드 DLL zip을 받게 안내하니** 소스 빌드나 공식판을 쓰세요.

### 3.5 도시·단지 배치

- 절차적으로 지어내기보다 **실제 OSM 건물 윤곽 + 지형(DEM)**에서 시작하는 것이 가장 그럴듯합니다.
  - [blosm](https://github.com/vvoovv/blosm)과 [BlenderGIS](https://github.com/domlysz/BlenderGIS)를 씁니다. BlenderGIS는 2025-12에 Blender 5용 수정이 들어갔습니다(확인).
  - blendergis.com은 저장소가 링크하지 않은 도메인이니 GitHub에서 받으세요.
- **경사지 건물**: 윤곽 꼭짓점 아래 지형 높이를 레이캐스트로 잽니다. 바닥은 입구 쪽 높이에 맞추고, 높이 차만큼 기단을 내려 뜨거나 파묻히지 않게 합니다.
- 절차적 도로·필지 분할의 표준은 CityEngine입니다(유료, 검색 요약). 오픈소스 대안은 연구용이거나 노후했습니다.

### 3.6 평면 데이터셋 라이선스

| 데이터 | 라이선스 |
|---|---|
| [ResPlan](https://github.com/m-agour/ResPlan) (17k 주거 평면, 2025) | **CC BY 4.0**(상업 가능), 코드 MIT. 문 연결 그래프 포함. 배포 형식이 pickle이라 격리 환경에서 한 번만 불러와 JSON으로 변환 |
| RPLAN | 연구 전용(검색 요약) |
| Tell2Design | 데이터 CC BY-NC 4.0 |
| MSD, CubiCasa5k | 미확인 |

대부분의 평면 생성 모델(HouseDiffusion, GSDiff 등)이 RPLAN으로 학습됐고, 가중치는 구글 드라이브의 pickle로 배포됩니다. 상업 이용은 법률 검토를 거치고, 불러오기는 격리 환경에서 하세요.

---

## 4. 보안 요약 (이 분야에서 본 것)

| 위험 | 내용 | 대응 |
|---|---|---|
| **크랙판 유료 애드온** | 인체(Human Generator, Auto-Rig Pro), 리토폴(Quad Remesher), 유기물(SDF.R, Chisel, Botaniq, Nature Generator), 건물(Archipack, SceneCity, HiFi)의 "무료/FULL" 재배포 사이트가 검색 상위에 뜸 | 공식 스토어·원 저장소만. 무료 애드온(Home Builder 5 등)도 재배포 사이트에 올라 있으니 "무료니까 아무 데서나"도 금지 |
| **가짜 "Blender MCP" 저장소** | README의 모든 링크(배지 포함)가 저장소 안 zip 하나로 가는 저장소(예: `Immunogenic-prismspectroscope589/Blender_mcp`)는 전형적인 악성 배포 패턴 | 링크를 누르지 않음. 원 저장소(ahujasid/mcp-for-blender, Blender Lab)만 |
| **폐쇄형 컴파일 번들** | 커밋 3개에 별 93개, Nuitka로 컴파일된 비공개 코드(ai-forge-mcp) | 소스 없는 번들은 격리 환경에서만 |
| **네이티브 바이너리 포함 무료 도구** | Modular Tree(C++ 코어), QRemeshify(QuadWild), 학습형 리거의 컴파일 의존성 | 원 저장소 릴리스만. 포크 배포본 금지 |
| **pickle 가중치·데이터** | 연구 가중치(HouseDiffusion, GSDiff), 데이터(ResPlan) | 격리 환경에서 로드 후 변환 |
| **제3자 링크로 라이선스 파일 받기** | PSHuman이 SMPL-X 파일을 제3자 OneDrive 링크로 안내 | 공식 배포처에서 등록 후 받기 |

자세한 점검표와 사건 목록은 [설치 안전 가이드](14_tool_install_safety.md)를 보세요.

## 5. 확인하지 못한 것

- extensions.blender.org·Superhive의 평점과 다운로드 수. 차단돼서 "평가 좋은"의 근거는 GitHub 활동, 공식 채널 등록, 업계 언론 언급으로 대신했습니다.
- 3D Arena 등 공개 순위표의 실시간 순위
- The Grove, Botaniq, Geo-Scatter에 컴파일된 바이너리가 들어 있는지
- Revit 2027 MCP, BIM-Edit, 평면 LLM 논문의 세부 수치(검색 요약)
- SMPL-X 상업 라이선스의 현재 상태(Meshcapade 인수 이후)
- GPT-6 Astra로 건물·인체를 만든 사례(검색 한도 소진)

## 관련 문서

- [배치·조형 보조 도구 한눈에 보기](../03_playbooks/06_placement_structure_helpers.md) · [설치 안전 가이드](14_tool_install_safety.md)
- [07 오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md) · [08 배치·레이아웃](08_scene_layout_placement.md) · [04 AI 3D 생성](04_ai_3d_generation.md) · [10 에셋·라이선스](10_assets_pipeline_licensing.md)
- [보조 스크립트](../03_playbooks/scripts/README.md): `scene_audit.py`, `building_audit.py`, `review_views.py` · [실측 치수표](../03_playbooks/05_reference_dimensions.md)

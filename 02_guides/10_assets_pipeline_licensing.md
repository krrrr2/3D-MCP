# 에셋 소스 · 게임레디 파이프라인 · 라이선스와 법규

> 기준일: 2026-09-27 · 에셋은 새로 만들기 전에 먼저 찾아 쓰고(CC0 우선), 생성 메시는 정해진 순서대로 게임레디로 바꾼 뒤 결정적 검사로 통과시키세요. 에셋마다 출처·플랜·사람이 수정한 이력을 남기고, 한국 사용자는 Hunyuan 계열 오픈웨이트를 쓰지 않습니다.

## 핵심 요약

- **소스 우선순위**: 이미 가진 에셋과 CC0 라이브러리(Poly Haven, ambientCG, Kenney, Quaternius)를 먼저 쓰고, 그다음 CC-BY(표기 자동화), 그다음 **상업권이 있는 유료 플랜**의 생성 서비스, 마지막으로 로컬 오픈 모델(의존성 라이선스 검토 후) 순서입니다. "처음부터 만들기보다 검색·재사용"은 연구 쪽 합의와도 같습니다([11 연구 가이드](11_research_papers.md)).
- **MCP로 바로 가져오기**: 커뮤니티 표준 ahujasid **MCP for Blender**(PyPI `mcp-for-blender` 2.1.0, 2026-09-25)에 Poly Haven(키 불필요), Sketchfab·Poly Pizza(키 필요)가 들어 있고, 가져온 에셋의 id·URL·저자·라이선스를 Blender 커스텀 프로퍼티로 남깁니다. dcc-mcp 에셋 스킬, Quartermaster 같은 나머지 도구는 별 0~2개 수준의 초기 프로젝트입니다.
- **게임레디 순서**: 정리 → **voxel remesh 먼저, decimate 나중** → (필요하면) 쿼드 리메시 → UV 재전개·텍셀 밀도 통일 → 하이→로우 베이크 → ORM 패킹 → LOD/Nanite·콜리전 → 익스포트 → 검증. 생성 원본을 곧바로 decimate하면 의자 다리나 난간 같은 얇은 부분이 부서집니다.
- **수치 기준**: Khronos 3D Commerce 가이드 1.0은 삼각형 10만 개 이하, 파일 5MB 이하, 텍스처 1K~2K(Normal 2K), OpenGL 노멀 + MikkTSpace, ORM(R=AO, G=Roughness, B=Metal), 1 unit = 1 m, +Y up, 정면 +Z입니다. "원점은 바닥 중앙"은 v2.0(2025-08) 기준입니다. Meshy 가이드는 모바일 소품 1K~5K, PC/콘솔 전경 5K~50K tris를 권장합니다.
- **이 문서 작성 중 직접 확인한 함정**: `gltfpack` 기본값은 노드 이름과 extras(= provenance 메타데이터)를 지우고 양자화 확장을 붙입니다. 엔진용이면 `-kn -km -ke -noq`를 붙이세요. 노멀이 면마다 갈라진 메시는 `-sp` 없이는 거의 줄지 않습니다. glTF-Transform `simplify`의 기본 오차(0.0001)로는 목표 비율에 못 미치고, `optimize`는 기본으로 메시를 단순화합니다. `npx gltf-validator`는 실행되지 않으니 `gltf-transform validate`나 Node 스크립트를 쓰세요(2.5·2.6절).
- **한국 사용자 라이선스 함정**: Hunyuan3D 2.0/2.1/Omni/Part, HunyuanWorld·HY-World, HY-Motion, BPT의 라이선스는 적용 지역에서 EU·영국·대한민국을 빼고, **출력물 사용도** 그 지역 밖에서는 금지합니다. "MIT"라고 적혀 있어도 TRELLIS.2(nvdiffrast 비상업, DINOv3, 배경 제거 가중치), Step1X-3D(텍스처 코드에 Hunyuan 헤더), TripoSG(RMBG-1.4 자동 다운로드)는 의존성까지 봐야 합니다.
- **생성 서비스는 플랜이 곧 라이선스입니다**: Meshy Free = CC BY 4.0(Meshy 표기), Tripo Free = 비상업, World Labs Marble Free·Standard = 상업권 없음, Rodin 무료·체험 키 = 미확인이므로 비상업으로 취급하세요.
- **소유권 ≠ 저작권 ≠ 비침해**: Anthropic 약관은 출력물을 고객 소유로 두고 권리를 양도합니다(원문 확인). OpenAI도 양도 구조로 알려져 있지만 원문은 열람하지 못했고, Google Gemini API는 "소유권을 주장하지 않는다"는 수준입니다. 미국 저작권청(2025-01-29)과 한국 등록 안내서(2025-06)는 모두 **사람의 창작적 기여만** 보호합니다.
- **공개·표시 의무**: 한국 인공지능기본법 2026-01-22 시행(제31조 표시 의무, 계도기간은 법적 유예가 아닌 행정 운영 방침), EU AI Act 제50조 2026-08-02 적용, Steam 공개 규정 2026-01-16 개정(pre-generated / live-generated), Sketchfab은 2025-12-11부터 모든 AI 모델에 CreatedWithAI 표시, Fab은 Created with AI 자가 신고가 의무입니다.
- **provenance**: 에셋마다 소스·모델 버전·플랜·날짜·입력·라이선스·사람 수정 이력을 남기세요. Blender 커스텀 프로퍼티 → glTF extras → credits.csv 흐름을 이 문서에서 테스트했습니다(5장).

> **한국 사용자: 먼저 확인할 세 가지**
>
> 1. **Hunyuan 계열은 로컬 가중치, 제3자 호스팅 API, MCP 통합 옵션을 모두 끄세요.** 라이선스 머리말부터 "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"입니다. Output 정의에 "Hosted Service를 통한 것"이 들어 있어서, 누군가 호스팅한 2.x 가중치를 API로 불러 써도 같은 제약을 받는다고 보는 편이 안전합니다. image-to-3dlab의 PBR 리페인트 단계(Hunyuan 2.1)나 BPT 리토폴로지도 같은 문제입니다.
> 2. **Tencent Cloud의 Hunyuan 3D 3.0/3.1 API**는 오픈웨이트 라이선스와 별개의 서비스 약관을 따릅니다. 한국 계정에서 쓸 수 있는지, 지역 조항이 있는지는 **(미확인)** 입니다. 확인하기 전에는 상업 프로젝트에 쓰지 마세요.
> 3. **인공지능기본법 제31조**는 이미 발효되었습니다. 게임이나 앱이 사용자에게 AI 생성 기능을 제공하면 결과물 표시를 설계해야 합니다(10.1절).

---

## 1. 에셋은 어디서 가져오나

### 1.1 우선순위

| 순서 | 소스 | 쓰는 이유 | 조건 |
|---|---|---|---|
| 1 | 이미 가진 에셋, CC0 라이브러리 | 라이선스 사고가 없고 품질이 일정합니다. 에이전트가 자동으로 조합해도 안전합니다 | 원본 URL만 기록 |
| 2 | CC-BY 에셋(Poly Pizza, Sketchfab, Google Scanned Objects 등) | 표기만 하면 상업 이용 가능 | 크레딧 문구 자동 수집 필수 |
| 3 | 상용 생성 서비스(Meshy, Tripo, Rodin 등) | 원하는 형태를 직접 만들 수 있음 | **상업권이 있는 유료 플랜**, 모델 버전·생성 날짜 기록 |
| 4 | 로컬 오픈 모델(TRELLIS.2 등) | 크레딧 비용 없음 | 의존성 라이선스 검토(7장) |
| 쓰지 않음 | NC(비상업)·ND(변경 금지), NoAI 태그, 라이선스 불명, 한국 제외 라이선스 | — | 배포 빌드에서 제거 |

### 1.2 에셋 라이브러리 비교 (2026-09)

| 소스 | 라이선스 | 규모·내용 | MCP·API 접근 | 주의 | 신뢰도 |
|---|---|---|---|---|---|
| **Poly Haven** | 에셋 CC0(표기 불필요). API는 개인·상업 모두 무료. API 저장소 코드는 AGPL-3.0 | HDRI·PBR 텍스처·모델 약 2,400개(MCP for Blender README 기준) | MCP for Blender `search_polyhaven_assets` / `download_polyhaven_asset`(키 불필요). 공개 API 엔드포인트 `/types`, `/assets`, `/info/{id}`, `/files/{id}`, `/categories/{type}`, `/author/{id}` | 모델 수가 적어 가구·소품 다양성이 부족합니다. **live API를 앱에 넣어 사용자에게 보여 주면** "Powered by Poly Haven" 수준의 크레딧이 필요하고, 호출마다 앱 이름과 일치하는 고유 Referer 또는 User-Agent를 붙여야 합니다(ToS 2.4조). Poly Haven이 만들거나 보증한 것처럼 보이면 안 됩니다. 기업용으로 서명된 Provenance Attestation 매니페스트를 선택 제공합니다(2.7조) — [Public API](https://github.com/Poly-Haven/Public-API), [ToS](https://github.com/Poly-Haven/Public-API/blob/master/ToS.md), [License](https://polyhaven.com/license) | 높음 |
| **ambientCG** | CC0 | PBR 재질·HDRI, 1K~8K JPG/PNG | [dcc-asset-ambientcg](https://github.com/dcc-mcp/dcc-asset-ambientcg)(`search_ambientcg_assets`, `list_ambientcg_downloads`, `download_ambientcg_asset`) | 게임용이면 2K JPG(Color, NormalGL, Roughness, AO)를 받아 ORM으로 패킹. 공식 라이선스 페이지는 직접 열람하지 못했고 2차 자료로 확인([Cinevva 가이드](https://app.cinevva.com/guides/game-asset-licenses)) | 중간 |
| **Kenney** | CC0(표기 선택) | 로우폴리 게임 에셋. 흔히 인용되는 "6만 개 이상"은 유료 올인원 번들 수치라서 무료 CC0 수로 쓰면 안 됩니다 | [dcc-asset-kenney](https://github.com/dcc-mcp/dcc-asset-kenney)(zip, 출처 URL, CC0 정보를 `asset_descriptor`로 반환) | 사실적 AAA 스타일에는 맞지 않습니다. 블록아웃·배치 테스트 프록시나 스타일라이즈드 프로젝트용. Kenney 로고는 공식 프로젝트 전용 | 중간 |
| **Quaternius** | CC0 | 로우폴리 모델 팩 | [dcc-asset-quaternius](https://github.com/dcc-mcp/dcc-asset-quaternius)(우회 다운로드 없이 공식 팩 페이지 링크만 반환) | Kenney와 같음 | 중간 |
| **Poly Pizza** | CC0 + CC-BY 혼합(약 69%가 CC-BY) | 무료 로우폴리 약 10,600개(구 Google Poly 아카이브 포함) | MCP for Blender `search_polypizza_models` / `download_polypizza_model`(무료 API 키). `polypizza_attribution`에 완성된 크레딧 문구가 저장됩니다([README](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/README.md)) | 표기 부담을 줄이려면 CC0만 필터링. 품질 편차가 큼 | 높음 |
| **BlenderKit** | 에셋마다 Royalty-Free 또는 CC0. RF는 상업 이용 가능하지만 **원본 파일 재배포·재판매 불가**. 애드온은 GPL-2.0 | 무료(로그인 없이): 모델 1만+, 재질 1만+, 씬 250+, HDRI 1,000+, 브러시 300+. Full Plan: 모델 2.7만+, 씬 750+, HDRI 1,500+, 브러시 850+ | 전용 MCP 없음(GitHub 검색 0건). `execute_blender_code`로 애드온 API를 부르는 방법은 검증되지 않음 — [BlenderKit](https://github.com/BlenderKit/BlenderKit) | RF 원본을 공개 저장소나 에셋 팩에 넣지 마세요. AI 사용 조항 원문은 미확인 | 중간 |
| **Sketchfab** | 모델마다 다름(CC0, CC-BY, CC-BY-SA, CC-BY-NC, ND 등, 또는 Standard/Editorial) | 사용자 업로드 모델이 방대함. downloadable 모델은 glTF/GLB/USDZ/원본으로 받음 | [gregkop/sketchfab-mcp-server](https://github.com/gregkop/sketchfab-mcp-server)(ISC, 도구 3개, 결과 1~24개, 별 40개 소규모), [dcc-asset-sketchfab](https://github.com/dcc-mcp/dcc-asset-sketchfab)(검색은 토큰 불필요, 다운로드는 `SKETCHFAB_TOKEN` OAuth), MCP for Blender(`BLENDERMCP_SKETCHFAB_API_KEY`) | Store는 문을 닫고 거래는 Fab으로 이전(2024-10-22 발표). Sketchfab은 뷰어·쇼케이스로 남음. **2025-12-11부터 판매 여부와 관계없이 모든 AI 생성 모델에 CreatedWithAI 표시 의무**([Game Developer](https://www.gamedeveloper.com/business/sketchfab-to-require-mandatory-ai-disclosure-epic-games-accounts-for-users)). 신규 가입은 Epic 계정으로 하게 되었다는 보도가 있지만, 기존 사용자까지 강제하는지는 불명확. 받은 뒤 스케일·원점 정규화, 리토폴·리베이크 필요 | 중간 |
| **Fab / Quixel Megascans** | Fab Standard License. Personal·Professional 어느 가격 티어로 샀든 모든 엔진·툴에서 사용 가능 | AAA 품질 스캔 재질·오브젝트(텍셀 밀도 정보 포함) | 공식 MCP 없음. [Quartermaster](https://github.com/Tanshaydar/Quartermaster)가 **보유한** 에셋을 로컬 색인해 MCP로 노출하지만, 비공개 API·세션 재생으로 수집하므로 스토어 약관 위반 위험이 큽니다(패턴 참고용) | **Megascans는 2024-12-31까지만 전부 무료**였습니다. 2025년부터는 유료가 기본(개별 에셋 $0.99~, 절차적 키트 $4.99~, 팩 $24.99~)이고, 인기 에셋 1,500개 이상의 무료 스타터 팩은 계속 제공됩니다([Fab 전환 FAQ](https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US), [CG Channel](https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/)). "UE 사용자는 무료"라는 옛 정보는 버리세요. **NoAI** 메타 태그 = 생성형 AI 데이터로 쓰지 말라는 표시([Fab 지원 문서](https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration?language=en_US)). Personal/Professional을 나누는 매출 기준은 미확인 | 중간 |
| **Objaverse 1.0 / Objaverse-XL** | 데이터셋 전체 ODC-By v1.0, **객체마다 개별 라이선스**. 코드는 Apache-2.0. Polycam 데이터는 학술·비상업(신청·승인 필요) | 1.0 약 80만 개(Sketchfab 기반), XL 1,000만 개 이상. LVIS 카테고리 주석 | pip `objaverse` 0.1.7(2023-11)의 `load_annotations()`에 license 필드. MCP로는 [dcc-asset-objaverse](https://github.com/dcc-mcp/dcc-asset-objaverse) — [objaverse-xl](https://github.com/allenai/objaverse-xl), [PyPI](https://pypi.org/project/objaverse/) | 품질 편차가 매우 큽니다. 상업용이면 license 필드로 CC0/CC-BY만 남기고 저작자 표기를 보관. 레퍼런스·배치 연구용으로 적합 | 높음 |
| **Smithsonian Open Access** | 메타데이터 CC0(1,100만 건 이상, AWS Open Data). 3D 모델은 에셋마다 다름(미확인) | 조각상·유물 스캔 | GitHub 저장소는 2026-05-21 아카이브(읽기 전용) — [OpenAccess](https://github.com/Smithsonian/OpenAccess) | 조형물 레퍼런스로 좋지만 스캔 메시라 리토폴·리베이크 필수 | 중간 |
| **Google Scanned Objects** | CC-BY 4.0 | 가정용품 스캔 1,030개(OBJ+PNG), 실측 스케일 | MuJoCo 변환본 [mujoco_scanned_objects](https://github.com/kevinzakka/mujoco_scanned_objects)로 받기 쉬움 | CC-BY 표기 필요, 스캔 메시 | 중간 |
| **상용 마켓**(Poliigon, TurboSquid, CGTrader, Textures.com) | 유료 royalty-free(세부 미확인) | 고품질 가구·소품 | 공식 MCP·공개 API 미확인. 구매한 에셋을 로컬 폴더로 두고 경로를 에이전트에게 넘기는 방식 | AI 학습·입력 금지 조항, AI 생성물 업로드 정책을 **전혀 확인하지 못했습니다**. 구매 전 약관에서 "AI", "machine learning" 조항을 확인하세요 | 낮음 |

### 1.3 MCP·API로 에셋을 가져오는 경로

| 경로 | 무엇을 가져오나 | 라이선스 메타데이터 | 성숙도·주의 |
|---|---|---|---|
| **ahujasid MCP for Blender**([GitHub](https://github.com/ahujasid/blender-mcp), [PyPI](https://pypi.org/project/mcp-for-blender/)) | Poly Haven, Sketchfab, Poly Pizza + 생성(Hyper3D Rodin, Hunyuan3D via Tencent Cloud). 2026-09-25부터 유료 **Premium**(자기 키 없이 Hunyuan3D·Tripo·Rodin, Tripo는 Premium 전용) | 커스텀 프로퍼티: `polyhaven_id`, `polyhaven_url`, `polyhaven_authors`, `polyhaven_resolution`, `polyhaven_licence`, `polypizza_attribution`, `polypizza_id`, `polypizza_licence` | 약 29.4k stars, 2026년 9월에만 릴리스 6회(2.0.0은 9/16). Hunyuan3D의 Tencent Cloud 모드는 본토 계정(ai3d, ap-guangzhou)과 국제 계정(hunyuan, ap-singapore)의 엔드포인트가 다릅니다. **한국에서는 Hunyuan 옵션과 Premium의 Hunyuan을 끄세요.** 공식 Blender Lab 커넥터와의 차이는 [02 가이드](02_blender_mcp.md) |
| **Meshy 공식 MCP**([meshy-mcp-server](https://github.com/meshy-dev/meshy-mcp-server)) | 생성 + remesh, UV unwrap, retexture, rig, convert(24 tools) | 플랜에 따라 결과물 라이선스가 달라짐(6장) | MIT, npm 0.5.2(2026-09-22). **Pro 플랜 이상 API 키** 필요 → MCP로 만든 결과물은 기본적으로 유료 플랜 산출물 |
| **Tripo**: [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp)(공식 조직), [trident-mcp](https://raw.githubusercontent.com/mordor-forge/trident-mcp/main/docs/MCP_TOOLS.md)(제3자, Go) | 생성, smart low-poly, 포맷 변환(GLTF, FBX, OBJ, STL, USDZ, 3MF) | 플랜별(6장) | tripo-mcp는 MIT, 알파, Tripo Blender 애드온 필수, 별 206개·커밋 8개 |
| **dcc-mcp 에셋 스킬**([조직](https://github.com/dcc-mcp)) | Poly Haven, ambientCG, NASA 3D, Smithsonian, Kenney, Quaternius, Objaverse, Sketchfab | `license_name`, `license_url`, `usage_notice`, 저작자 표기 반환 | 래퍼 MIT. 대부분 별 0~1개인 초기 프로젝트라 성숙한 도구처럼 믿으면 안 됩니다 |
| **Quartermaster** | 본인이 구매한 Fab·Megascans·Unity Asset Store·Gumroad 에셋 색인(FTS5 + ONNX + CLIP, 오프라인) | 스토어 메타 | 별 2개. 비공개 GraphQL·세션 재생 방식이라 **약관 위반 위험**. README도 "약관 준수는 사용자 책임"이라고 경고합니다. "이미 산 에셋부터 찾게 한다"는 **패턴**만 참고하세요 |

### 1.4 에이전트 규칙 블록 (CLAUDE.md·AGENTS.md에 그대로 붙이기)

```markdown
## 에셋·라이선스 규칙
- 새로 생성하기 전에 먼저 찾는다: 프로젝트 라이브러리 → Poly Haven / ambientCG(CC0) → Poly Pizza(CC0 필터) → Sketchfab.
- Sketchfab·Objaverse는 downloadable이고 license가 CC0 또는 CC-BY인 것만 받는다.
  CC-BY-SA는 사람이 승인한 경우만. NC·ND·라이선스 없음·NoAI 태그는 받지 않는다.
- 받은 에셋마다 원본 URL, 저자, 라이선스를 커스텀 프로퍼티(prov_*)와 credits.csv에 기록한다.
- Hunyuan3D 계열(로컬, Tencent Cloud, Premium 경유)은 호출하지 않는다.
- 생성 서비스는 상업권이 있는 유료 플랜 키로만 호출하고, 모델 버전을 명시한다(SDK 기본값 금지).
- 라이선스를 확인할 수 없는 에셋은 배포 빌드에 넣지 않는다.
```

> CC-BY-SA는 수정본에도 같은 라이선스 조건이 따라붙을 수 있어 상업 게임에서는 신중히 다루세요. 조사 원자료는 CC0, CC-BY, CC-BY-SA를 허용 목록으로 제안했지만, 위 블록에서는 SA를 사람 승인 항목으로 한 단계 낮췄습니다. 전체 템플릿은 [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md)에 있습니다.

---

## 2. 게임레디 변환 파이프라인

생성 원본은 보통 삼각형 약 100만 개에 비정형 토폴로지이고, watertight·manifold가 보장되지 않습니다. **디테일은 베이크로 보존하고 메시는 가볍게 다시 만든다**가 정석입니다. 생성 단계 자체와 품질 수치(asset-studio 프리셋 등)는 [04 AI 3D 생성 가이드 7장](04_ai_3d_generation.md#7-필수-후처리-게임렌더에-쓸-수-있게-만들기)을 함께 보세요.

### 2.1 전체 순서

| 단계 | 할 일 | 도구·설정 | 합격 기준 |
|---|---|---|---|
| 0. 원본 보관 | 생성 원본을 `_gen`(또는 `_HP`)으로 보관 | 파일 버전 | 베이크 소스·저작권 증빙으로 재사용 |
| 1. 정리·정규화 | 부유 조각·퇴화면 제거, 중복 정점 병합, 노멀 재계산. **1 unit = 1 m, 원점 바닥 중앙, 트랜스폼 적용** | Blender([04 가이드 6.2절 코드](04_ai_3d_generation.md#62-생성-후-정규화-blender-코드-테스트-완료)), `placement_utils.snap_to_floor()`, Tripo `pivot_to_center_bottom`, glTF-Transform `center --pivot below` | [`scene_audit.py`](../03_playbooks/scripts/README.md)에서 스케일 미적용·떠 있음·관통 0 |
| 2. Voxel Remesh | 수밀화·균일화. 얇은 형상(의자 다리, 난간, 조형물의 가는 부분)을 지키려면 **decimate보다 먼저** | Blender Voxel Remesh. 라이브러리 수준에서는 meshoptimizer v1.3의 voxel remeshing([releases](https://github.com/zeux/meshoptimizer/releases)) | 구멍·조각 없음 |
| 3. 감량 / 리토폴 | 예산까지 decimate, 쿼드가 필요하면 리메셔(2.2절) | 예: [image-to-3dlab](https://github.com/Bingeljell/image-to-3dlab) 약 90만 → 4만 면 | 3장 예산 이하 |
| 4. UV | 재전개·패킹, **텍셀 밀도 통일** | xatlas(padding 4~8px@2K, `texelsPerUnit` 고정), Blender Smart UV + Pack Islands(margin), [Texel Density Checker](https://github.com/mrven/Blender-Texel-Density-Checker), glTF-Transform `unwrap`, Meshy `meshy_uv_unwrap`, Tripo `pack_uv=True` | 겹침 0, 씬 전체 같은 px/m |
| 5. 베이크 | 원본(하이)에서 로우로 Normal·AO(+ color, roughness, metallic) | Blender Cycles 베이크([05 가이드 7장](05_texturing_materials.md#7-베이크-자동화-bpy)) | 노멀 뒤집힘·번짐 없음 |
| 6. ORM 패킹 | R=AO, G=Roughness, B=Metallic. BaseColor·Emissive만 sRGB, 나머지는 Linear(Non-Color) | 05 가이드 `pack_orm` | glTF Asset Auditor PBR safe color 30~243, 금속도는 0 또는 1 |
| 7. LOD·Nanite·콜리전 | LOD1 50%, LOD2 25% 같은 체인, UCX 볼록 콜리전 | gltfpack·glTF-Transform(2.5절), Blender Decimate + [4.1절 헬퍼](#41-unreal-engine) | LOD 전환 시 실루엣 유지 |
| 8. 익스포트 | glTF(extras 포함) / FBX / USD | Blender glTF 익스포터(2.4절) | 엔진용 원본은 압축하지 않음 |
| 9. 검증 | 스펙 검증 오류 0, 예산·텍스처 규칙, 씬 감사, 4방향 렌더 비평, 엔진 임포트 테스트 | 2.6절 | 모두 통과해야 다음 에셋으로 |

**실제 예 (image-to-3dlab, 2026-09)**: `python scripts/retopo_repaint.py generated.glb source.png finished.glb --faces 40000 --skip-paint`는 voxel remesh → 4만 면 decimate → JPEG 2048 재인코딩을 거쳐 32MB 파일을 5MB 미만으로 만듭니다([README](https://raw.githubusercontent.com/Bingeljell/image-to-3dlab/main/README.md)). 이 도구의 선택적 PBR 리페인트는 **Hunyuan 2.1**을 쓰므로 한국에서는 `--skip-paint`를 유지하세요.

**MCP 프롬프트 예 (정리·리토폴)**:

```text
선택한 생성 메시를 SM_Chair_Oak_01_gen으로 복제해 숨겨 두고(원본 보관), 작업본에서:
1) Separate by Loose Parts → 면 100개 미만 조각(부유물) 삭제 → 나머지를 다시 Join
2) Voxel Remesh(voxel size 5mm) → Decimate로 3만~8만 tris
3) QRemeshify 실행(Symmetry X). 서랍·손잡이처럼 떨어진 부품은 따로 분리한 채로 실행
   결과는 SM_Chair_Oak_01로 이름 변경
4) 바운딩 박스 최저점을 z=0, 원점을 바닥 중앙으로, 실측 높이 0.9m로 균등 스케일 후 Apply Scale
5) scene_audit.py를 돌려 issues가 빈 목록인지 보고
```

voxel size와 QRemeshify 설정값은 예시입니다. 치수 기준은 [실측 치수표](../03_playbooks/05_reference_dimensions.md)를 쓰세요.

### 2.2 리토폴로지 도구 고르기

| 도구 | 라이선스 | 특징·설정 | 한국 상업 사용 |
|---|---|---|---|
| Blender Voxel Remesh + Decimate | Blender 내장 | 가장 단순. 소품은 이것만으로 충분한 경우가 많음 | 가능 |
| QuadriFlow | Blender Remesh 연산자에 내장 | MCP가 Blender Python으로 호출 | 가능 |
| [QRemeshify](https://github.com/ksami/QRemeshify) | GPL-3.0, Blender 4.2+, 별 1.2k, 최종 갱신 2024-10 | QuadWild + Bi-MDF. 설정: Sharp Angle Threshold, Symmetry, Preprocess, Smoothing. **입력은 1천~10만 tris, 삼각형 분포 균일, loose part는 분리**(README). 하드서피스 특징선 보존이 좋고 옷 주름처럼 복잡한 디테일에서는 느림. Windows 외 플랫폼은 테스트 중 | 가능 |
| [Instant Meshes](https://github.com/wjakob/instant-meshes) | BSD-3, 별 6.2k | field-aligned 쿼드. Modo 10.2 이후 자동 리토폴에 같은 알고리즘. 유지보수 뜸 | 가능 |
| [AutoRemesher](https://github.com/huxingyi/autoremesher) | MIT, 별 3.5k, 최근 커밋 2026-09-03 | CLI `--target-quads`, `--edge-scaling`, `--sharp-edge`, `--adaptivity`, `--anisotropy`. 헤드리스 일괄 처리에 적합 | 가능 |
| Quad Remesher(Exoside) | 상용 | 최신 버전·가격 1차 출처 미확인 | 라이선스 구매 |
| [meshoptimizer](https://github.com/zeux/meshoptimizer) v1.3 | MIT | `meshopt_simplify`(target_index_count, target_error, LockBorder/Regularize/Permissive/ErrorClamped), `simplifyWithAttributes`(노멀·UV 가중), `simplifySloppy`, `clusterlod.h`(Nanite식 클러스터 LOD), voxel remeshing | 가능 |
| Meshy `meshy_remesh` | 크레딧(5) | `topology` quad/triangle, `target_polycount`, `should_remesh`, `decimation_mode`, `target_formats` | 유료 플랜 |
| Tripo `smart_lowpoly` | 크레딧 | 2.7절 | 유료 플랜 |
| MeshAnything V1/V2 | **S-Lab License 1.0(비상업)**, 상업은 별도 문의 | V1 800면, V2 1,600면 상한. +Y up, `--mc` 전처리([V2](https://github.com/buaacyw/MeshAnythingV2), [LICENSE](https://raw.githubusercontent.com/buaacyw/MeshAnything/main/LICENSE.txt)) | 불가 |
| BPT(Tencent) | **Tencent Hunyuan 3D 2.0 Community License**([License](https://raw.githubusercontent.com/Tencent-Hunyuan/bpt/main/License)) | 8,000면 이상, fp16 약 12GB, 약 2분(CVPR'25) | **불가(한국 제외)** |
| [MeshRipple](https://github.com/MayMhappy/MeshRipple) | **LICENSE 파일 없음** → 모든 권리 유보로 봐야 함 | 10k면(Full Attention), 20k면(NSA), CVPR 2026 highlight | 불가 |

- 목표 쿼드 수는 최종 삼각형 예산의 약 절반으로 잡습니다(쿼드 1개 = 삼각형 2개).
- 캐릭터 관절의 에지 루프는 자동 리메셔가 수작업 품질에 못 미칩니다. 정적 소품·가구·조형물은 자동으로 충분한 경우가 많습니다.

### 2.3 UV와 텍셀 밀도

- AI 생성 메시의 UV는 조각이 많고 밀도가 제각각입니다. 같은 방 안의 가구끼리 선명도가 달라 보이면 "AI 티"가 납니다. **항상 재전개하고 씬 전체의 px/m를 하나로 맞추세요.**
- [xatlas](https://github.com/jpcy/xatlas)(MIT, Godot·Filament·ArmorPaint·Bakery가 사용, 파이썬 바인딩 xatlas-python): `padding`, `texelsPerUnit`, `resolution`, `bruteForce`, `maxChartSize`. glTF-Transform `unwrap`도 내부적으로 xatlas를 씁니다(기존 UV가 있으면 `--overwrite` 없이는 덮어쓰지 않는 것으로 보임).
- 관례값(1인칭 약 1024px/m, 3인칭 약 512px/m)은 1차 출처를 찾지 못했습니다 **(신뢰도 낮음)**. 숫자보다 **통일**이 중요합니다. 세부 표는 [05 가이드 6.3절](05_texturing_materials.md#63-텍셀-밀도를-씬-전체에서-통일).

### 2.4 베이크·ORM·노멀 규약과 glTF 익스포트

| 항목 | glTF / Blender | Unreal Engine | 근거 |
|---|---|---|---|
| 탄젠트 노멀 규약 | OpenGL(red right, **green up**), MikkTSpace | DirectX(green down) 규약으로 알려져 있음 **(1차 문서 미확인)** → 텍스처의 Flip Green Channel을 켜거나 DirectX용으로 베이크 | [Khronos 가이드 1.0](https://raw.githubusercontent.com/KhronosGroup/3DC-Asset-Creation/main/asset-creation-guidelines-1.0/RealtimeAssetCreationGuidelines.md) |
| ORM 채널 | R=AO, G=Roughness, B=Metal | `T_*_ORM`으로 패킹해 사용(sRGB 해제) | 같은 문서 |
| 색 공간 | BaseColor·Emissive = sRGB, 나머지 = Linear | 같음 | 같은 문서 |
| 금속도 | 0 또는 1. 회색은 안티에일리어싱용으로만 | 같음 | [Khronos 가이드 v2.0](https://raw.githubusercontent.com/KhronosGroup/3DC-Asset-Creation/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md) |

**Blender glTF 익스포터가 읽는 방식**([glTF-Blender-IO 문서](https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst)):

- 재질은 Principled BSDF에서 읽습니다. 이미지로 연결하면 metallic = **B 채널**, roughness = **G 채널**입니다.
- 오클루전은 `glTF Material Output`이라는 이름의 노드 그룹에서 **R 채널**로 읽습니다. 한국어 UI에서 "새 데이터 번역"을 켜 두면 새로 만든 데이터 이름이 번역될 수 있으므로, 이 노드 그룹은 스크립트에서 정확한 영어 이름으로 만드세요. 노드는 이름 대신 `type`으로 찾게 하세요([05 가이드](05_texturing_materials.md)).
- 노멀맵은 Normal Map 노드를 거쳐야 하고 이미지는 Non-Color여야 합니다.
- 쿼드·n-gon은 자동 삼각화됩니다. **절차적 텍스처는 베이크하지 않으면 사라집니다.**
- 지원 확장: transmission, clearcoat, sheen, specular, volume, IOR, anisotropy, emissive strength.
- 권장 옵션: +Y up, Apply Modifiers, UV·Normals·Tangents 포함, 이미지 PNG(품질) 또는 JPEG/WebP(용량), **Custom Properties를 extras로 내보내기**(라이선스 메타 보존, 5장).
- pip `bpy` 4.2.23에서 내보낼 때 Draco 라이브러리를 찾지 못한다는 오류 메시지가 나왔습니다(이 문서 테스트, 내보내기는 정상 완료). 헤드리스에서 Draco 압축이 필요하면 glTF-Transform `draco`를 쓰세요.

### 2.5 LOD·단순화·압축 (이 문서에서 직접 테스트)

**테스트 조건 (2026-09-27)**: `npx gltfpack@1.3.0`(gltfpack 1.3), `npx @gltf-transform/cli@4.5.0`, npm `gltf-validator` 2.0.0-dev.3.10. 입력은 Blender 5.0.1(pip `bpy`)에서 내보낸 UV 구 16,128 tris(스무스 셰이딩판과 플랫 셰이딩판 두 가지)에 커스텀 프로퍼티를 extras로 실은 GLB입니다.

| 명령 | 결과 | 의미 |
|---|---|---|
| `gltfpack -si 0.5` (기본) | 노드 이름 **삭제**, extras **삭제**, `KHR_mesh_quantization` 추가 | UE 네이밍(`SM_`, `UCX_`, `_LOD0`)과 provenance가 사라짐 |
| `gltfpack -si 0.5 -kn -km` | 이름은 남지만 extras는 여전히 삭제, 양자화 유지 | `-ke` 필요 |
| `gltfpack -si 0.5 -kn -km -ke -noq` | 이름·extras 유지, 확장 없음 | **엔진 임포트용 LOD는 이 조합** |
| 스무스 메시 `-si 0.5 / 0.25 / 0.1` | 8,064 / 4,032 / 1,612 tris | 목표대로 줄어듦 |
| 플랫 셰이딩 메시 `-si 0.5` | 15,736 tris(양자화) / 16,128 tris(`-noq`) | **노멀이 면마다 갈라져 있으면 거의 안 줄어듦** |
| 플랫 셰이딩 메시 `-si 0.5 -sp` | 8,064 tris | `-sp`(속성 경계를 넘는 단순화 허용)로 해결 |
| `gltf-transform simplify --ratio 0.5` (기본 `--error 0.0001`) | 14,698 tris | 목표 미달. 오차 한도에서 멈춤 |
| `gltf-transform simplify --ratio 0.5 --error 0.01` | 8,064 tris | 목표 도달 |
| 플랫 메시 `weld` 후 `simplify --error 0.01` | 16,128 tris(변화 없음) | weld로는 노멀이 다른 정점이 합쳐지지 않음 → 스무스 셰이딩 후 내보내거나 gltfpack `-sp` |
| `gltf-transform optimize` (기본) | 14,698 tris + `EXT_meshopt_compression` + 양자화 | **기본으로 메시를 단순화함**. 엔진 원본에는 쓰지 말거나 `--simplify false` |
| `gltf-transform center --pivot below` | 바닥 중앙이 원점이 되도록 노드 이동 | 피벗 정규화 |
| `gltf-transform draco` | 366KB → 32KB, `KHR_draco_mesh_compression` | gltfpack은 Draco 미지원 |
| glTF-Transform 명령 전반(weld, simplify, center, tangents, unwrap, draco, optimize) | 노드 extras 유지 | provenance가 보존됨 |

**복사해서 쓰는 명령**:

```bash
# 엔진(UE/Unity)용 LOD 체인: 이름·재질·extras 유지, 양자화 끔
npx gltfpack@1.3.0 -i SM_Chair.glb -o SM_Chair_LOD1.glb -si 0.5  -kn -km -ke -noq
npx gltfpack@1.3.0 -i SM_Chair.glb -o SM_Chair_LOD2.glb -si 0.25 -kn -km -ke -noq
# 하드 엣지가 많은 소품(상자, 기계)은 -sp 추가
npx gltfpack@1.3.0 -i SM_Crate.glb -o SM_Crate_LOD1.glb -si 0.5 -sp -kn -km -ke -noq

# glTF-Transform: 오차 한도를 반드시 지정
npx @gltf-transform/cli@4.5.0 weld     in.glb welded.glb
npx @gltf-transform/cli@4.5.0 simplify welded.glb out.glb --ratio 0.5 --error 0.01
npx @gltf-transform/cli@4.5.0 center   in.glb out.glb --pivot below
npx @gltf-transform/cli@4.5.0 tangents in.glb out.glb        # MikkTSpace 탄젠트

# 웹·모바일 배포본 (gltfpack README 기준, 텍스처 압축은 이 문서에서 미테스트)
npx gltfpack@1.3.0 -i SM_Chair.glb -o web/SM_Chair.glb -cc -tc -kn -ke
```

- gltfpack 플래그 정리([README](https://raw.githubusercontent.com/zeux/meshoptimizer/master/gltf/README.md)): `-c`/`-cc` = `EXT_meshopt_compression`, `-cz` 또는 `-ce khr` = 새 `KHR_meshopt_compression`, `-tc` = KTX2(BasisU), `-tw` = WebP, `-mi` = 인스턴싱, `-se` = 단순화 오차 한도(기본 0.01), `-sa` = 품질 무시하고 목표 비율 강제, `-slb` = 경계 정점 고정. **Draco는 지원하지 않습니다.**
- glTF-Transform([GitHub](https://github.com/donmccurdy/glTF-Transform), [CLI 소스](https://raw.githubusercontent.com/donmccurdy/glTF-Transform/main/packages/cli/src/cli.ts))에는 `ktx2`라는 명령이 없습니다. KTX2는 `uastc` / `etc1s`로 만듭니다. 그 밖에 `dedup`, `prune`, `resize`, `webp`, `meshopt`, `instance`, `flatten`, `join`, `palette`, `xmp`, `validate`가 있습니다.
- meshopt·KTX2 확장은 모든 임포터가 지원하지 않습니다. **UE·Unity로 보내는 원본은 압축하지 않은 GLB/FBX**로 두고, 압축은 웹 배포본에만 하세요.

### 2.6 검증 게이트 (에이전트 루프의 마지막 단계)

렌더 이미지를 눈으로 보고 판단하면 치수·겹침·스케일 오류를 놓치기 쉽습니다. **결정적 검사로 먼저 거르고, 그다음 렌더로 눈 검사**하세요.

| 검사 | 도구 | 설정·합격 기준 |
|---|---|---|
| glTF 스펙 | [glTF-Validator](https://github.com/KhronosGroup/glTF-Validator)(Apache-2.0). npm 최신 2.0.0-dev.3.10(2024-10-22)로 릴리스가 느림 | 오류 0. JSON 구조, 참조, 접근자 NaN·min/max, 2의 거듭제곱 경고, KHR/EXT 확장 검사 |
| 에셋 규칙 | [glTF Asset Auditor](https://github.com/KhronosGroup/glTF-Asset-Auditor)(Apache-2.0, 별 27개) | JSON 프로파일. 기본값: 텍스처 512~2048, 2의 거듭제곱, PBR safe color 30~243, 삼각형 최대 100,000, 파일 최대 5,120KB, UV 0~1·뒤집힘·겹침·거터·텍셀 밀도. 끄려면 -1 또는 false. 고폴리 메시는 1분 넘게 걸릴 수 있고 엔진 고유 규칙(콜리전, 네이밍)은 검사하지 않음 |
| 씬 감사 | [`scene_audit.py`](../03_playbooks/scripts/README.md)(이 저장소, Blender 4.2.23 LTS·5.0.1 테스트) | 떠 있음·바닥 관통·유닛 간 관통·스케일 미적용·non-manifold·재질/UV 없음·치수 범위 이탈 0 |
| 슬롯 확인 | [05 가이드 8.2절 `glb_material_report`](05_texturing_materials.md#82-내보낸-뒤-감사-만든-맵-vs-들어간-슬롯) | 베이크한 맵이 GLB 슬롯에 모두 들어갔는지 |
| 눈 검사 | [`review_views.py`](../03_playbooks/scripts/README.md) 4방향 렌더 → AI 비평 | 실루엣·비율·재질 |
| 엔진 | UE/Unity/Godot 임포트 테스트 | 스케일·축·재질 연결 |

**주의: `npx gltf-validator out.glb`는 동작하지 않습니다.** npm의 `gltf-validator`는 CLI가 아니라 라이브러리라서 "could not determine executable to run" 오류가 납니다(이 문서 테스트). 둘 중 하나를 쓰세요.

```bash
# (a) glTF-Transform CLI: 오류가 있으면 종료 코드 1 (테스트 완료)
npx @gltf-transform/cli@4.5.0 validate out.glb
```

```js
// (b) validate.mjs — 사용: npm i gltf-validator && node validate.mjs out.glb (테스트 완료)
import fs from 'fs';
import validator from 'gltf-validator';
const file = process.argv[2];
const report = await validator.validateBytes(new Uint8Array(fs.readFileSync(file)));
const { numErrors, numWarnings, messages } = report.issues;
console.log(JSON.stringify({ file, numErrors, numWarnings,
  top: messages.filter(m => m.severity <= 1).slice(0, 20) }, null, 1));
process.exit(numErrors > 0 ? 1 : 0);
```

테스트에서 accessor count를 일부러 망가뜨린 GLB는 `ACCESSOR_TOO_LONG`, `MESH_PRIMITIVE_UNEQUAL_ACCESSOR_COUNT` 오류 3건과 종료 코드 1을 냈고, 정상 파일은 오류 0·종료 코드 0이었습니다. 에이전트에게는 "종료 코드가 0이 될 때까지 고쳐서 다시 내보내라"고 지시하면 됩니다.

### 2.7 생성 서비스 API에서 바로 게임레디로 받기

**Tripo** — 기준은 문서가 아니라 현행 SDK 소스입니다. `docs/API.md`는 코드와 맞지 않으니 근거로 쓰지 마세요([client.py](https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/tripo3d/client.py), [tripo3d 0.4.2, 2026-07-01](https://pypi.org/project/tripo3d/)).

| 함수 | 현행 값 (client.py) | 주의 |
|---|---|---|
| 생성(`text_to_model`, `image_to_model`) | `model_version` 목록: `P1-20260311`(저폴리 전용), `Turbo-v1.0-20250506`, `v3.1-20260211`, `v3.0-20250812`, `v2.5-20250123`, `v2.0-20240919`, `v1.4-20240625`. 인자: `face_limit`, `quad`, `smart_low_poly`, `generate_parts`, `pbr`, `texture_quality`·`geometry_quality`(standard/detailed), `auto_size`, `export_uv`(기본 True), `image_to_model`만 `orientation`(default/align_image) | **기본값이 여전히 v2.5-20250123**이므로 반드시 지정 |
| `smart_lowpoly` | `model_version`은 `P-v2.0-20251226`만 허용(기본값 동일), `face_limit` 기본값 None, `quad`(기본 False), `bake`(기본 True), `part_names` | 옛 문서의 "P-v1.0, 기본 4000면"은 낡은 정보. face_limit을 직접 지정 |
| `convert_model` | `format`(GLTF/USDZ/FBX/OBJ/STL/3MF), `quad`, `force_symmetry`, `face_limit`(기본 None), `flatten_bottom`, `texture_size`(기본 4096), `texture_format`(기본 JPEG), `scale_factor`(기본 1.0), `pivot_to_center_bottom`(기본 False), `pack_uv`(기본 False), `bake`(기본 True), `fbx_preset`(blender/mixamo/3dsmax, 기본 blender), `export_orientation`(+x/+y/-x/-y, 기본 +x), `export_vertex_colors`, `with_animation`(기본 True) | 엔진용이면 texture_size 2048, pivot_to_center_bottom·pack_uv를 켬 |

```python
# 시그니처는 client.py(tripo3d 0.4.2) 기준. API 키·크레딧이 필요해 이 문서에서 실제 호출은 하지 않았습니다.
import asyncio
from tripo3d import TripoClient            # 환경변수 TRIPO_API_KEY(tsk_로 시작)

async def main():
    async with TripoClient() as c:
        t = await c.image_to_model(image="chair_front.png", model_version="v3.1-20260211",
                                   texture_quality="detailed")
        await c.wait_for_task(t)
        lp = await c.smart_lowpoly(t, face_limit=4000, quad=True)      # P-v2.0-20251226
        await c.wait_for_task(lp)
        cv = await c.convert_model(lp, format="FBX", fbx_preset="blender",
                                   pivot_to_center_bottom=True, texture_size=2048,
                                   pack_uv=True, flatten_bottom=True)
        task = await c.wait_for_task(cv)
        print(await c.download_task_models(task, "out"))

asyncio.run(main())
```

각 함수는 task id(문자열)를 돌려주므로 `wait_for_task`로 끝날 때까지 기다린 뒤 다음 단계에 넘깁니다. 처음부터 저폴리가 필요하면 생성 단계에서 `model_version="P1-20260311"`을 쓰는 방법도 있습니다.

**Meshy** — 공식 MCP의 `meshy_remesh`(`topology` quad/triangle, `target_polycount`, `should_remesh`, `decimation_mode`, `target_formats`, 5 credits), `meshy_uv_unwrap`(5 credits), `meshy_convert`(1 credit). 출력 범위는 1K~300K tris입니다([meshy-mcp-server](https://github.com/meshy-dev/meshy-mcp-server), [game-asset-pipeline](https://github.com/meshy-dev/game-asset-pipeline)). 생성 모델·텍스처 옵션은 [04 가이드](04_ai_3d_generation.md)를 보세요.

---

## 3. 수치 기준

### 3.1 Khronos 3D Commerce 실시간 에셋 가이드라인

| 항목 | v1.0 (2020-10) | v2.0 (2025-08) |
|---|---|---|
| 삼각형 | 100,000개 이하 | — |
| 파일 크기 | 5MB 이하("Ideally") | 단일 `.glb` 선호 |
| 텍스처 | BaseColor·ORM·Emissive 1K~2K, Normal 2K 권장, 2의 거듭제곱(정사각형은 필수 아님) | png / jpg / webp / ktx2 |
| 노멀 | OpenGL(red right, green up) + MikkTSpace | 같음 |
| ORM | R=AO, G=Roughness, B=Metal | 금속도는 0 또는 1(회색은 안티에일리어싱에만) |
| 색 공간 | BaseColor·Emissive sRGB, 나머지 Linear | 같음 |
| 좌표 | +Y up, 정면 +Z, 1 unit = 1 m | **원점은 제품 바닥 중앙(0,0,0)** |
| 파일명 | — | a-z, 0-9, `_`, `-` |

출처: [3DC-Asset-Creation](https://github.com/KhronosGroup/3DC-Asset-Creation), [v1.0](https://raw.githubusercontent.com/KhronosGroup/3DC-Asset-Creation/main/asset-creation-guidelines-1.0/RealtimeAssetCreationGuidelines.md), [v2.0](https://raw.githubusercontent.com/KhronosGroup/3DC-Asset-Creation/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md) (둘 다 CC BY 4.0 문서). 웹·AR 커머스 기준이라 AAA 게임의 히어로 에셋 예산보다 보수적입니다. 대신 "합의하기 쉬운 표준 수치"라는 장점이 있습니다.

### 3.2 폴리곤·텍스처 예산

| 대상 | 삼각형 | 텍스처 | 출처 |
|---|---|---|---|
| 모바일 소품 | 1K~5K | — | Meshy game-asset-pipeline (벤더 가이드) |
| PC/콘솔 전경 소품 | 5K~50K | 최대 4K PBR | 같음 |
| 웹·AR 커머스 | 100K 이하, 5MB 이하 | 1K~2K | Khronos 1.0 |
| Auditor 기본 프로파일 | 최대 100,000 | 512~2048 | glTF Asset Auditor |
| 스타일 프리셋·감량 실측 예 | [04 가이드 7.2절](04_ai_3d_generation.md#72-qa-기준-수치) | | asset-studio(개인 프로젝트 보고) |

### 3.3 프롬프트에는 "게임레디"가 아니라 숫자를 넣으세요

"게임레디로 만들어 줘"라고만 하면 모델마다 결과가 다릅니다. 숫자는 `face_limit`, `target_polycount` 같은 API 인자로 바로 옮겨집니다.

```text
이 의자는 PC 3인칭 배경 소품이다.
- LOD0 6,000 tris 이하, LOD1 50%, LOD2 25%
- 텍스처 2K 한 세트: BaseColor(sRGB), Normal(OpenGL, MikkTSpace), ORM(R=AO, G=Roughness, B=Metal)
- 실측 높이 0.9m, 좌면 0.45m, 1 unit = 1 m, 원점 바닥 중앙, 정면 -Y(Blender)
- 이름: SM_Chair_Oak_01, 콜리전 UCX_SM_Chair_Oak_01_00
- 완료 조건: gltf-transform validate 종료 코드 0, scene_audit issues 없음
```

"정면 -Y"는 이 저장소 [스크립트 규약](../03_playbooks/scripts/README.md)(Blender Z-up)입니다. glTF로 내보내면 +Y up / 정면 +Z로 바뀝니다. 한국 가구 치수는 [실측 치수표](../03_playbooks/05_reference_dimensions.md)를 쓰세요.

---

## 4. 엔진 네이밍·임포트

### 4.1 Unreal Engine

**네이밍** — 커뮤니티 표준 [Allar UE5 Style Guide](https://github.com/Allar/ue5-style-guide)(Epic 공식 아님, **main 브랜치는 UE4용이고 UE5용은 v2 브랜치**): `Prefix_BaseAssetName_Variant_Suffix`.

| 에셋 | 이름 예 | 비고 |
|---|---|---|
| 정적 메시 | `SM_Chair_Oak_01`(가이드 표기는 `S_`, `SM_` 병기) | |
| 스켈레탈 메시 | `SK_Knight_01` | |
| 머티리얼 / 인스턴스 | `M_Wood_Master` / `MI_Chair_Oak_01` | |
| 텍스처 | `T_Chair_Oak_01_D`, `_N`, `_ORM` | 접미사 `_D/_N/_R/_M/_O/_E/_A`. 패킹 텍스처는 글자를 이어 붙임(`_ORM`). `_M`이 Mask와 Metallic에 겹치니 프로젝트에서 하나로 정하세요 |
| 물리 에셋 | `PHYS_` | |

**콜리전·LOD·소켓** — Epic의 Send to Unreal 문서([static-mesh.md](https://raw.githubusercontent.com/EpicGamesExt/BlenderTools/main/docs/send2ue/asset-types/static-mesh.md), [BlenderTools](https://github.com/EpicGamesExt/BlenderTools), MIT):

| 규칙 | 형식 |
|---|---|
| 볼록 콜리전 | `UCX_[RenderMeshName]_##` |
| 박스 / 캡슐 / 구 | `UBX_`, `UCP_`, `USP_`(구는 8세그먼트 정도) |
| LOD | `_LOD0`, `_LOD1` … (`_LOD0` 접미사는 자동 제거) |
| 소켓 | `SOCKET_` 접두사를 단 자식 |

**Blender 헬퍼: UCX 콜리전과 LOD 이름 만들기** (pip `bpy` 4.2.23 LTS·5.0.1에서 테스트: 구 3,968 tris → UCX 202 tris, 볼록성·manifold 확인, LOD 3,968 / 1,984 / 992 tris)

```python
import bpy, bmesh

def make_ucx(obj, index=0, max_tris=200):
    """렌더 메시 obj로 볼록 콜리전 UCX_<obj 이름>_NN 을 만든다(Send to Unreal 이름 규칙).
    점이 많으면 Decimate한 복사본의 점만으로 볼록 껍질을 만든다(껍질 삼각형 ≤ 2V-4).
    트랜스폼을 먼저 Apply한 뒤 쓰는 것을 전제로 한다."""
    max_verts = max_tris // 2 + 2
    tmp = obj.copy(); tmp.data = obj.data.copy()
    obj.users_collection[0].objects.link(tmp)
    nv = len(tmp.data.vertices)
    if nv > max_verts:
        tmp.modifiers.new("dec", "DECIMATE").ratio = max_verts / nv
    ev = tmp.evaluated_get(bpy.context.evaluated_depsgraph_get())
    pts = [obj.matrix_world @ v.co for v in ev.to_mesh().vertices]   # 점만 사용
    ev.to_mesh_clear(); bpy.data.objects.remove(tmp)
    bm = bmesh.new()
    for p in pts:
        bm.verts.new(p)
    res = bmesh.ops.convex_hull(bm, input=bm.verts)
    bmesh.ops.delete(bm, geom=res["geom_interior"] + res["geom_unused"], context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(f"UCX_{obj.name}_{index:02d}")
    bm.to_mesh(me); bm.free()
    col = bpy.data.objects.new(me.name, me)
    obj.users_collection[0].objects.link(col)
    col.display_type = "WIRE"
    return col

def make_lods(obj, ratios=(0.5, 0.25)):
    """obj 이름에 _LOD0을 붙이고, Decimate 비율별 _LOD1, _LOD2 … 복제본을 만든다."""
    base = obj.name
    obj.name = f"{base}_LOD0"
    lods = [obj]
    for i, r in enumerate(ratios, start=1):
        dup = obj.copy(); dup.data = obj.data.copy(); dup.name = f"{base}_LOD{i}"
        obj.users_collection[0].objects.link(dup)
        dup.modifiers.new("Decimate", "DECIMATE").ratio = r
        lods.append(dup)
    return lods

# 사용: 콜리전을 먼저 만들고(렌더 메시 이름 기준), 그다음 LOD 이름을 붙인다
# ucx = make_ucx(bpy.data.objects["SM_Chair_Oak_01"]); make_lods(bpy.data.objects["SM_Chair_Oak_01"])
```

- 의자처럼 오목한 물체는 볼록 껍질 하나로 덮으면 좌판 아래가 막힙니다. 부위(좌판, 등받이, 다리)별 오브젝트마다 `make_ucx(part, index=0/1/2…)`로 여러 개를 만드세요.
- LOD를 함께 쓸 때 콜리전 이름이 `_LOD0`이 붙은 이름을 따라야 하는지는 Send to Unreal 문서에서 확인하지 못했습니다. 임포트 후 UE에서 콜리전이 붙었는지 확인하세요.

**Nanite** — 불투명 정적 소품과 고밀도 스캔에는 켭니다(Meshy 가이드). 반투명·스켈레탈·모바일/저사양 타깃은 기존 LOD를 유지하라는 것이 조사 당시의 학습 지식이지만, UE 5.5 이후 Nanite 스켈레탈(실험) 등 지원 범위가 바뀌었을 수 있습니다 **(미확인, Epic 문서 차단)**. Nanite 메시도 UV와 노멀맵은 필요합니다. UE 5.8의 Epic 공식 실험적 Unreal MCP는 [03 가이드](03_other_mcp_dcc_cad_engines.md)를 보세요.

### 4.2 Unity

- glTF는 공식 패키지 [glTFast](https://github.com/Unity-Technologies/com.unity.cloud.gltfast)(`com.unity.cloud.gltfast`, Apache-2.0)로 가져오고 내보냅니다.
- Meshy FBX처럼 cm 단위로 내보낸 파일이 100배로 들어오면 **Scale Factor 0.01**을 씁니다(Meshy 가이드). GLB는 재질이 자동 할당되고, FBX는 URP/HDRP Lit에 텍스처를 수동 연결합니다. 휴머노이드는 Rig를 Humanoid로 둡니다.
- Blender는 미터 단위로 두고, FBX 익스포트에서 Apply Transform과 스케일 옵션을 맞춘 뒤 Unity에서 Bake Axis Conversion과 Scale Factor를 점검하세요. Unity 기본값과 Unity 6.x 자동 Mesh LOD 기능 여부는 **(미확인, Unity 문서 차단)**. LOD Group으로 LOD0~2를 연결합니다.

### 4.3 Godot·웹

- Godot은 glTF를 그대로 임포트합니다. 실제 사례로 Paper Ember Duel(Godot 4.7.2)이 있습니다(12장).
- 웹 배포본만 meshopt/Draco·KTX2/WebP로 압축하세요(2.5절).

---

## 5. Provenance(출처 기록)

### 5.1 왜 필요한가

같은 기록이 다섯 군데에 쓰입니다.

1. **플랜별 상업권 증명**: Meshy 무료 = CC BY 4.0, Tripo 상업권은 "구독이 활성화된 기간에 생성한 모델"에만 적용.
2. **크레딧 표기**: Poly Pizza·Sketchfab·Google Scanned Objects의 CC-BY.
3. **플랫폼 공개**: Steam 콘텐츠 설문, Fab·Sketchfab AI 태그.
4. **저작권 등록·분쟁**: 사람이 기여한 부분을 따로 증명해야 함(9장).
5. **규제 대응**: 한국 인공지능기본법·EU AI Act 표시 의무(10장).

### 5.2 필드

```json
{
  "asset_id": "SM_Chair_Oak_01",
  "source_type": "generated",
  "generator": "Tripo P1-20260311",
  "plan": "Professional (구독 활성 기간 내 생성)",
  "generated_at": "2026-09-10",
  "inputs": ["ref/chair_front.png (직접 촬영)"],
  "input_hash": "sha256:…",
  "params": {"face_limit": 6000, "quad": true},
  "components": {"matting": "사용자 제작 알파 PNG", "texture": "Blender 베이크"},
  "license": "commercial-private",
  "attribution": "",
  "human_edits": ["Blender 리토폴로지·UV 재작업", "좌판 쿠션 스컬팅", "패브릭 텍스처 핸드페인팅"],
  "files": ["SM_Chair_Oak_01_gen.blend", "SM_Chair_Oak_01_retopo.blend", "SM_Chair_Oak_01_final.blend"],
  "disclosure": {"steam": "pre-generated", "fab": "Created with AI"}
}
```

- 라이브러리 에셋은 `source_type: "library"`, `source_url`, `author`, `license`만 있어도 됩니다.
- image-to-3dlab은 `.provenance.json`에 입력 해시, 백엔드, 파라미터, **컴포넌트별 라이선스**를 남깁니다. 배경 제거기·텍스트→이미지 모델처럼 중간 단계 모델의 라이선스까지 적는 방식이 좋습니다(같은 README에 따르면 텍스트→이미지에 쓴 Qwen-Image 2.1 가중치는 비상업이라 그 경로의 결과물은 비상업으로 분류됩니다).

### 5.3 어디에 실을까

| 방법 | 장점 | 단점 | 이 문서 테스트 |
|---|---|---|---|
| Blender 커스텀 프로퍼티 → glTF **extras** | 에셋과 함께 이동. MCP for Blender가 이미 `polyhaven_*`, `polypizza_*`를 씀 | gltfpack 기본값이 extras를 지움(`-ke` 필요). 엔진이 extras를 읽는지는 엔진마다 다름(미확인) | 4.2.23·5.0.1에서 노드 extras로 들어감 확인 |
| 사이드카 `*.provenance.json` | 사람이 읽기 쉽고 필드 제한 없음 | 파일이 떨어지기 쉬움 | — |
| `credits.csv` | 크레딧 화면·스토어 페이지로 바로 사용 | 요약본일 뿐 | 아래 코드로 생성 확인 |
| glTF **XMP**(`KHR_xmp_json_ld`) | glTF 표준 메타데이터. 제목·저작자·출처·이용 조건 | JSON-LD 작성 필요 | glTF-Transform `xmp --packet`로 추가, validator 오류 0 확인 |
| Poly Haven Provenance Attestation | 서명된 매니페스트(기업 대상 선택 사항, ToS 2.7조) | Poly Haven 에셋 한정 | — |

### 5.4 코드: 커스텀 프로퍼티 → credits.csv → GLB extras (테스트 완료)

pip `bpy` 4.2.23 LTS·5.0.1에서 같은 결과를 확인했습니다. 라이선스가 없는 메시 오브젝트는 목록으로 돌려주므로, 빈 목록이 아니면 배포를 멈추게 하세요.

```python
import bpy, csv, json

def set_provenance(obj, **fields):
    """obj(오브젝트·재질·이미지 등 ID)에 prov_* 커스텀 프로퍼티로 출처를 기록한다."""
    for k, v in fields.items():
        obj[f"prov_{k}"] = v if isinstance(v, (str, int, float)) else json.dumps(v, ensure_ascii=False)

def build_credits(path):
    """prov_* 와 MCP for Blender가 남긴 polyhaven_*/polypizza_* 값을 모아 credits.csv를 만든다.
    메시 오브젝트는 전부 검사하고, 재질·이미지·월드(HDRI)는 라이선스 값이 있는 것만 싣는다.
    반환값: 라이선스를 알 수 없는 메시 오브젝트 이름 목록(비어 있어야 통과)."""
    rows, unknown = [], []
    blocks = [("object", o) for o in bpy.data.objects if o.type == "MESH"]
    blocks += [(kind, b) for kind, coll in (("material", bpy.data.materials),
               ("image", bpy.data.images), ("world", bpy.data.worlds)) for b in coll]
    for kind, b in blocks:
        lic = b.get("prov_license") or b.get("polyhaven_licence") or b.get("polypizza_licence")
        if lic is None:
            if kind == "object":
                unknown.append(b.name)
            continue
        src = b.get("prov_source") or b.get("polyhaven_url") or b.get("polypizza_id") or ""
        att = b.get("prov_attribution") or b.get("polypizza_attribution") or ""
        rows.append((kind, b.name, src, lic, att))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kind", "name", "source", "license", "attribution"])
        w.writerows(rows)
    return unknown

def export_glb_with_provenance(path):
    """커스텀 프로퍼티를 glTF extras로 실어 내보낸다."""
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB",
                              export_extras=True, export_yup=True, export_apply=True)

# 사용 예
chair = bpy.data.objects["SM_Chair_Oak_01"]
set_provenance(chair, source="Tripo P1-20260311", plan="Professional", generated_at="2026-09-10",
               license="commercial-private", human_edits=["retopo", "uv", "handpaint"])
missing = build_credits(bpy.path.abspath("//credits.csv"))    # .blend를 저장한 폴더 기준
assert not missing, f"라이선스 불명 에셋: {missing}"
export_glb_with_provenance(bpy.path.abspath("//SM_Chair_Oak_01.glb"))
```

테스트 결과(요약): 노드 `SM_Chair_Oak_01`의 extras에 `prov_source`, `prov_plan`, `prov_generated_at`, `prov_license`, `prov_human_edits`(JSON 문자열)가 들어갔고, `polypizza_*` 값을 가진 오브젝트와 `polyhaven_*` 값을 가진 재질은 CSV에 실렸으며, 값이 없는 메시 오브젝트는 `missing`으로 잡혔습니다. `//`로 시작하는 경로는 .blend 파일이 저장된 상태를 전제로 합니다(저장 전이면 절대 경로를 쓰세요).

**XMP로 싣기** (glTF-Transform 4.5.0 테스트, 결과 GLB의 validator 오류 0):

```bash
npx @gltf-transform/cli@4.5.0 xmp SM_Chair_Oak_01.glb out.glb --packet provenance.jsonld
```

```json
{
  "@context": {"dc": "http://purl.org/dc/elements/1.1/", "xmpRights": "http://ns.adobe.com/xap/1.0/rights/"},
  "dc:title": {"@type": "rdf:Alt", "rdf:_1": {"@language": "x-default", "@value": "SM_Chair_Oak_01"}},
  "dc:creator": {"@list": ["Studio Name"]},
  "dc:source": "Tripo P1-20260311 (Professional, 2026-09-10) + human retopo/handpaint",
  "xmpRights:UsageTerms": {"@type": "rdf:Alt", "rdf:_1": {"@language": "x-default", "@value": "Commercial, private. See provenance.json"}}
}
```

`--packet` 없이 실행하면 대화형으로 필드를 물어봅니다. `@context`의 두 주소는 Dublin Core·XMP 네임스페이스 식별자입니다.

---

## 6. AI 3D 생성 서비스: 약관·가격 (2026-09)

가격은 대부분 애그리게이터 요약입니다. **가격표를 코드나 CLAUDE.md에 고정하지 말고** 도입 직전에 공식 페이지를 확인하세요.

| 서비스 | 무료 플랜 결과물 | 상업권이 생기는 조건 | 가격 (보고 기준) | 신뢰도 |
|---|---|---|---|---|
| **Meshy** | **CC BY 4.0** — 상업 이용 가능하지만 "Meshy" 표기 필요, 공개될 수 있음 | 유료 플랜 = 비공개 소유(표기 불필요). 조건 두 가지: **Meshy Community에 공개하지 않을 것**, 업로드한 입력(참조 이미지 등)이 타인 권리를 침해하지 않을 것([Help Center](https://help.meshy.ai/en/articles/9992001-can-i-use-my-generated-assets-for-commercial-projects), [소유권 FAQ](https://help.meshy.ai/en/articles/10137554-what-is-the-ownership-of-the-generated-models), [Meshy-guide](https://github.com/meshy-dev/Meshy-guide)) | 공식 가격 페이지 제목은 Free/Pro/Studio/Enterprise. 애그리게이터의 6개 플랜·가격 목록은 **(미확인)**. 무료 크레딧은 공식 GitHub 가이드 기준 월 200, 애그리게이터 기준 월 100으로 서로 다름. MCP는 Pro 이상 필요 | 라이선스 높음 / 가격 낮음 |
| **Tripo** | 공개 모델, **비상업** | Professional 이상. **구독이 활성화된 기간에 생성한 모델**에 상업권 | Free 약 200 credits(표준 생성 1회 약 25 credits → 약 8개 안팎). Professional $19.90/월 3,000 credits(약 120개), 동시 작업 10개, 비공개. Max $89.9/월(월 결제로 보임), Team $109.9/월(보고). API 단가 **(미확인)** — [가격](https://www.tripo3d.ai/pricing), [costbench](https://costbench.com/software/ai-3d-generation/tripo-ai/) | 중간 |
| **Hyper3D Rodin** | **(미확인)** → 비상업으로 취급 | "모든 플랜에 상업권"이라는 애그리게이터 요약은 근거를 찾지 못함. Business에는 API 전체 접근, High-Poly Quad, ChatAvatar 상업 라이선스 혜택 | Creator $30/월, Business $120/월, 크레딧 직접 구매 $1.5/credit(월 결제 기준 여러 출처 일치) — [가격](https://hyper3d.ai/pricing) | 가격 중간 / 상업권 미확인 |
| **World Labs Marble** | 상업권 없음 | **Pro·Max만** 상업권 | Free 4회, Standard $20(12회, 상업권 없음), Pro $35(25회), Max $95(75회). 2025-11-12 출시 당시 가격 — [billing 문서](https://docs.worldlabs.ai/marble/support/account-billing), [TechCrunch](https://techcrunch.com/2025/11/12/fei-fei-lis-world-labs-speeds-up-the-world-model-race-with-marble-its-first-commercial-product/) | 중간 |
| **Tencent Hunyuan 3D 3.0/3.1**(클라우드 전용, 가중치 비공개) | 신규 크리에이터 하루 20회 무료(플랫폼) | **한국에 적용되는 약관 (미확인)**. 실명 인증 필요 | 3.0은 2025-09-16 발표([VoxelMatters](https://www.voxelmatters.com/tencent-launches-updated-hunyuan-3d-3-0-platform-for-3d-model-generation/)), 3.1 글로벌 제공 2026-01-28([Tencent HY](https://x.com/TencentHunyuan/status/2016449283428659599)). Tencent Cloud는 크레딧 과금(단가 미확인) | 낮음 |
| Hitem3D(Hi3D로 리브랜딩 언급) | 미확인 | 미확인 | Free / PRO $19.9 / MAX $39.9(월, 단일 비교 사이트) | 낮음 |
| Kaedim | — | 계약서의 IP 양도 조항 확인 | 영업 문의형, 사람 검수 방식. 리뷰상 $150부터 | 낮음 |
| Adobe Substance 3D(Firefly) | — | Adobe 플랜·생성형 크레딧 | Sampler Text to Texture·Stager Generative Background 베타가 2024-03-18 출시([Adobe](https://news.adobe.com/news/news-details/2024/adobe-brings-firefly-generative-ai-into-substance-3d-workflows)). 2026년 기능 범위·크레딧 단가 미확인. Claude의 "Adobe for creativity" 커넥터(2026-04-28)에는 **Substance 3D가 없습니다**([Adobe 블로그](https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector)) | 중간 |

**운영 규칙**

- 프로토타입은 무료 플랜으로 만들어도 되지만, **출시할 에셋은 상업권이 있는 플랜에서 다시 생성**하세요. 나중에 유료로 바꿔도 과거 무료 결과물의 조건이 바뀐다는 보장은 없습니다(약관 원문 미확인).
- 결제 영수증과 **생성 당시 약관 캡처**를 provenance와 함께 보관하세요.
- MCP for Blender Premium(자기 키 없이 생성)은 누구의 계정·플랜으로 생성되는지, 어떤 약관이 적용되는지 이 조사에서 확인하지 못했습니다. 상업 프로젝트는 **본인 유료 키(BYOK)** 경로를 쓰세요.

---

## 7. 오픈웨이트·오픈소스 라이선스 함정

"코드 라이선스"와 "실제로 돌아가는 파이프라인 전체의 라이선스"는 다릅니다. 가중치, 배경 제거기, 래스터라이저, 이미지 인코더까지 봐야 합니다.

| 대상 | 함정 | 한국 상업 사용 | 근거 |
|---|---|---|---|
| **Tencent Hunyuan3D 2.0 / 2.1 / Omni / Part, HunyuanWorld 1.0 / HY-World 2.0, HY-Motion 1.0, BPT** | Territory = "EU·영국·한국을 제외한 전 세계". 머리말부터 "DOES NOT APPLY IN … SOUTH KOREA". **5(c)** Territory 밖에서 Works·Output의 사용·복제·수정·배포·전시 금지. **5(b)** 출력물로 다른 AI 모델 개선 금지. Output 정의에 "Hosted Service를 통한 것" 포함. 라이선스 대상에 가중치뿐 아니라 **추론 코드·소프트웨어**도 포함. MAU 100만 조항은 **각 버전 출시일(2.0: 2025-01-21, 2.1: 2025-06-13) 직전 달 MAU를 한 번 보는 조건**(계속 적용되는 한도가 아님). Territory 안에서는 "Tencent claims no rights in Outputs" | **불가** | [2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE), [2.0](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE), [Omni](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-Omni/main/License.txt)(2025-09-26), [Part](https://github.com/Tencent-Hunyuan/Hunyuan3D-Part/blob/main/LICENSE), [HY-World 2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0/blob/main/License.txt), [HY-Motion 1.0](https://github.com/Tencent-Hunyuan/HY-Motion-1.0), [BPT](https://raw.githubusercontent.com/Tencent-Hunyuan/bpt/main/License). 공개 직후 개발자 반발: [Hacker News](https://news.ycombinator.com/item?id=42786403), [이슈 #50](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/50) |
| **Hunyuan 파생 코드가 섞인 저장소** | Hunyuan3D-2의 `custom_rasterizer`, `differentiable_renderer`를 재사용한 코드에도 같은 라이선스가 따라옴 | 코드 단위 확인 | 아래 Step1X-3D 참고 |
| **Microsoft TRELLIS.2** | 코드는 MIT, 지역 제한 없음. 하지만 공식 GLB 익스포트 `o_voxel.postprocess.to_glb`와 텍스처링 파이프라인이 **nvdiffrast**를 import해 텍스처를 베이크합니다. nvdiffrast·nvdiffrec의 NVIDIA Source Code License **3.3조: "non-commercially (research or evaluation purposes only)"**. 이 문제를 묻는 이슈 #22는 메인테이너 답변 없이 열려 있음. 이미지 인코더 DINOv3는 Meta DINOv3 License(상업 이용 허용, 군사 용도·제재 대상 금지, 재배포 시 라이선스 첨부). 불투명 입력의 배경 제거 가중치는 조사마다 RMBG-2.0(PR #175) / BiRefNet으로 다르게 보고됨 → 쓰는 버전에서 직접 확인. `to_glb` 기본값은 decimation_target 1,000,000, texture_size 2048(4096은 README 예시값) | **조건부**: 상업 납품 전 nvdiffrast 대체 경로 또는 NVIDIA 상업 라이선스, DINOv3 약관, 배경 제거기 검토 | [TRELLIS.2](https://github.com/microsoft/TRELLIS.2), [postprocess.py](https://raw.githubusercontent.com/microsoft/TRELLIS.2/main/o-voxel/o_voxel/postprocess.py), [nvdiffrast LICENSE](https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt), [nvdiffrec LICENSE](https://github.com/NVlabs/nvdiffrec/blob/main/LICENSE.txt), [이슈 #22](https://github.com/microsoft/TRELLIS.2/issues/22), [PR #175](https://github.com/microsoft/TRELLIS.2/issues/175), [DINOv3 License](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md) |
| **Step1X-3D** | README·LICENSE는 Apache-2.0(2025-05-13 가중치 공개). 그런데 텍스처 파이프라인 `step1x3d_texture/custom_rasterizer`, `differentiable_renderer`는 Hunyuan3D 2.0 코드를 재사용했고 파일 헤더에 **"TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT"**가 남아 있음. requirements에 nvdiffrast도 있음 | **형상 단계만** 검토 대상. 텍스처 단계는 법률 검토 전 사용 보류 | [mesh_render.py 헤더](https://raw.githubusercontent.com/stepfun-ai/Step1X-3D/main/step1x3d_texture/differentiable_renderer/mesh_render.py), [requirements.txt](https://raw.githubusercontent.com/stepfun-ai/Step1X-3D/main/requirements.txt) |
| **TripoSG** | MIT, 1.5B, 형상만, 약 8GB VRAM, `--faces 5000`처럼 면 수 제한. 추론 스크립트가 **briaai/RMBG-1.4**를 자동으로 내려받음(BRIA 비상업 라이선스로 알려짐, 원문 미확인) | **조건부**: 알파 있는 RGBA 입력을 쓰거나 배경 제거 단계를 교체 | [TripoSG](https://github.com/VAST-AI-Research/TripoSG) |
| **Stable Fast 3D** | Stability AI Community License(2024-07-05): 본인과 계열사를 합친 **전체 연매출** 100만 달러 미만이면 무료 상업 이용. **상업 이용 시 `stability.ai/community-license`에 등록 필수**. 배포 시 Notice 파일과 "Powered by Stability AI" 표시. 출력물로 파운데이션 생성 모델을 만들거나 개선 금지. 출력물 소유는 "적용법이 허용하는 범위에서". 리메시 none/triangle/quad, 약 6GB VRAM | **조건부**: 등록·매출 기준 기록 | [LICENSE](https://raw.githubusercontent.com/Stability-AI/stable-fast-3d/main/LICENSE.md), [저장소](https://github.com/Stability-AI/stable-fast-3d) |
| MeshAnything V1/V2 | S-Lab License 1.0 비상업 | 불가 | 2.2절 |
| MeshRipple | LICENSE 없음 | 불가 | 2.2절 |
| BRIA RMBG-2.0 | 비상업 조건, Hugging Face 게이트. image-to-3dlab은 라이선스 문제로 기본 비활성화하고 알파 RGBA 입력만 받음 | 불가(교체) | [image-to-3dlab README](https://raw.githubusercontent.com/Bingeljell/image-to-3dlab/main/README.md) |
| Qwen-Image 2.1(텍스트→이미지) | image-to-3dlab README에 "Those weights are non-commercial"로 명시 → 이 단계를 거친 결과물은 비상업 | 불가(다른 모델로) | 같은 README |
| Objaverse의 Polycam 데이터 | 학술·비상업(신청·승인) | 불가 | [objaverse-xl](https://github.com/allenai/objaverse-xl) |

**한국에서 로컬 파이프라인을 짠다면**: 상업 SaaS(유료 플랜)와 로컬 모델을 섞고, 로컬 모델은 위 표의 "조건부" 항목을 하나씩 지워 나가세요. 모델별 품질·VRAM 비교와 Pixal3D 같은 다른 선택지는 [04 가이드 2.3절](04_ai_3d_generation.md#23-오픈웨이트-로컬-실행)과 [9장](04_ai_3d_generation.md#9-상업-파이프라인-함정)에 있습니다.

---

## 8. LLM 출력물 소유권 (Claude · GPT · Gemini)

MCP로 Claude나 GPT가 쓴 Blender 스크립트, 배치 데이터, 텍스처 프롬프트의 결과물에 해당합니다.

| 회사·약관 | 출력물 권리 | 학습 사용 | IP 면책 | 확인 수준 |
|---|---|---|---|---|
| **Anthropic Commercial Terms**(2025-06-17 발효, API·Team·Enterprise 등) | "Customer … owns its Outputs", "Anthropic hereby assigns to Customer its right, title and interest (if any) in and to Outputs" | 고객 콘텐츠로 학습하지 않음 | 유료 사용 중 생성한 출력물의 제3자 IP 침해에 면책. **예외**: 수정, 비Anthropic 기술과의 결합, 상업적 상표 사용, 고객이 제공한 Inputs·데이터, 타인 권리를 침해하는 방식의 사용, Output 안의 특허 발명 실시 | 원문 확인([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)) |
| **Anthropic Consumer Terms**(2025-10-08 발효, 개인 요금제) | 약관 준수를 조건으로 권리 양도("if any") | 옵트아웃하지 않으면 학습에 쓰일 수 있음. **옵트아웃해도 Feedback 제출분과 안전 검토 대상으로 플래그된 자료는 쓰일 수 있음** | — | 원문 확인([Consumer Terms](https://www.anthropic.com/legal/consumer-terms)). 경쟁 제품·모델 개발 목적 이용 금지 |
| **OpenAI Terms of Use** | 사용자가 Output을 소유하고 OpenAI가 권리를 양도. 비슷한 출력이 다른 사용자에게도 나올 수 있다는 단서 | — | 소비자 요금제는 제한적(요약 기준) | **원문 미열람**(openai.com 차단, 2차 자료). GPT-6 Astra에 별도 상업 조건이 있는지 **(미확인)** — [ROW Terms](https://openai.com/policies/row-terms-of-use/) |
| **Google Gemini API Additional Terms** | Google이 생성 콘텐츠의 소유권을 **주장하지 않음**(명시적 양도는 아님) | 무료 티어는 입력·출력이 품질 개선에 쓰일 수 있음(원문 확인 필요) | Vertex AI(엔터프라이즈)에서 면책 제공(요약 기준) | 원문 미열람 — [Gemini API Terms](https://ai.google.dev/gemini-api/terms) |

- 상업 프로젝트에서는 Commercial Terms가 적용되는 경로(API, Team/Enterprise)로 Claude(Opus 5.5, Sonnet 5 등)를 MCP에 연결하고, 개인 요금제를 쓴다면 학습 옵트아웃을 켜세요. 모델·요금 선택은 [01 AI 모델 가이드](01_ai_models_and_clients.md).
- **소유권 조항은 AI 회사와 사용자 사이의 관계만 정합니다.** 저작권이 생긴다는 뜻도, 제3자 권리를 침해하지 않는다는 뜻도 아닙니다. 유명 IP 캐릭터, 브랜드 로고, 실존 디자이너 가구(상표·디자인권 대상일 수 있음)를 복제하라고 프롬프트하지 마세요. 예: "임스 라운지 체어" 대신 "1950년대 미드센추리 합판 곡면 라운지 체어, 오리지널 디자인".

---

## 9. 저작권: AI 산출물은 어디까지 보호되나

| 관할 | 문서 | 요지 |
|---|---|---|
| 미국 | 저작권청 「Copyright and AI Part 2: Copyrightability」(2025-01-29)([NewsNet](https://www.copyright.gov/newsnet/2025/1060.html), [Crowell 해설](https://www.crowell.com/en/insights/client-alerts/us-copyright-office-releases-part-2-of-artificial-intelligence-report-clarifying-copyrightability-of-generative-ai-outputs)) | 순수 AI 생성물은 보호되지 않음. **프롬프트만으로는 상세하더라도 저작자성 불인정**(현재 기술 수준 기준). 사람이 AI 출력물을 창작적으로 수정하거나 선택·배열한 부분, 사람이 만든 입력이 출력에 그대로 드러나는 부분은 사안별로 보호 가능. 섞인 작품은 사람 기여분만 보호. Thaler의 "A Recent Entrance to Paradise" 등록 거절 사례 인용. Thaler v. Perlmutter(D.C. Cir., 2025-03)도 인간 저작자 요건을 유지했다는 것이 조사 당시 학습 지식이며, 대법원 상고 결과는 **(미확인)** |
| 한국 | 「생성형 AI 저작권 안내서」(2023-12) | AI 학습·산출 과정의 침해 예방 |
| 한국 | 문체부·한국저작권위원회 「생성형 AI 활용 저작물의 저작권 등록 안내서」(2025-06)([한국저작권위원회](https://www.copyright.or.kr/information-materials/publication/research-report/view.do?brdctsno=54253), [전자신문](https://www.etnews.com/20250701000303)) | **인간의 창작적 기여 부분만 등록 가능**. 등록 시 AI가 만든 부분과 사람이 만든 부분(수정·보완, 선택·배열, 편집)을 구분해 기재. 법적 구속력은 없는 가이드라인 |
| 한국 | 「생성형 인공지능의 저작물 학습에 대한 저작권법상 '공정이용' 안내서」(2026-02-26)([법률신문](https://www.lawtimes.co.kr/news/articleView.html?idxno=217415)) | AI 개발사의 **학습 데이터 이용**에 관한 안내. 크리에이터의 출력물 이용 안내가 아니니 혼동하지 마세요 |

**실무**: AI 원본 메시·텍스처는 보호되지 않는다고 전제하고, 사람의 기여를 **의도적으로 추가하고 기록**하세요.

- 파일 버전: `_gen`(AI 원본) → `_retopo` → `_sculpt` → `_final`, 커밋 메시지에 수정 내용.
- 기여 예: 리토폴로지, 스컬팅 수정(쿠션 주름 직접 조각), 핸드페인팅 텍스처, 조합·배치·레벨 디자인.
- 타임랩스·스크린샷 보관. 미국 등록 시 AI 생성 부분은 제외하고 신고. 한국 등록 시 게임·영상 전체는 편집저작물·2차적저작물 관점에서 사람 기여를 중심으로 신청.
- 순수 AI 결과물은 경쟁사가 복제해도 대응이 약할 수 있다는 점을 사업 판단에 넣으세요.

---

## 10. 법규·플랫폼 공개 의무

### 10.1 한국 인공지능기본법

「인공지능 발전과 신뢰 기반 조성 등에 관한 기본법」은 2025-01-21 공포, **2026-01-22 시행**입니다([정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148958380)). 조문은 제3자 조문 데이터([nfa-bigdata](https://raw.githubusercontent.com/nfa-bigdata/ai-law-clause-search-set5-2026/main/%EC%A1%B0%ED%95%AD%EB%8D%B0%EC%9D%B4%ED%84%B0.json))로 확인했으며, 국가법령정보센터 원문과 직접 대조하지는 못했습니다.

| 조항 | 내용 | 게임·3D 창작자에게 의미 |
|---|---|---|
| 제31조 ①항 | 사전고지 의무 | 과태료가 붙는 유일한 항목(제43조, 3천만 원 이하) |
| 제31조 ②항 | "인공지능사업자는 생성형 인공지능 또는 이를 이용한 제품 또는 서비스를 제공하는 경우 그 결과물이 생성형 인공지능에 의하여 생성되었다는 사실을 표시하여야 한다" | 게임이 **런타임에 AI로 생성**하거나 사용자에게 AI 3D 생성 기능을 제공하면 표시 설계 필요 |
| 제31조 ③항 | 실제와 구분하기 어려운 가상의 음향·이미지·영상은 명확히 고지. 단 **예술적·창의적 표현물**이면 전시·향유를 저해하지 않는 방식으로 가능 | 게임은 예술적·창의적 표현물에 해당할 수 있어 완화된 표시 방식이 적용될 여지 |
| 제31조 ④항 | 방법·예외를 대통령령에 위임 | 시행령·가이드라인 원문 확인 필요 |
| 계도기간 | 과태료 부과에 **최소 1년 이상**, 이 기간 사실조사도 원칙적 유예(인명 피해·중대한 인권 침해·국가적 피해 우려는 예외) | **법적 유예가 아니라 행정 운영 방침**입니다. 의무 자체는 2026-01-22부터 발생 |

- 의무 주체는 "인공지능사업자"(개발·이용사업자)입니다. **AI를 도구로만 쓴 개인 크리에이터나, 개발 중에 미리 생성한 에셋에 이 조항이 어떻게 적용되는지는 (미확인)** 입니다.
- 시행령의 과태료 세부 기준(1회 500만 원, 2회 1,000만 원, 3회 이상 1,500만 원)은 단일 출처라 **(미확인)**, 시행령 국무회의 의결일(2026-01-20)도 **(미확인)** 입니다.
- 실무 예: 런타임에 AI로 인테리어를 생성하는 모드라면 UI에 "AI 생성" 배지를 달고, 내보내는 glTF의 extras에 generator 메타데이터를 남기세요(5장). 표시 방식 해설: [법무법인 해설](https://bh-law.kr/ko/news/column/ai-content-labeling-obligation-guide), [신앤김 뉴스레터](https://www.shinkim.com/kor/media/newsletter/3114).

### 10.2 EU AI Act 제50조 (EU에 출시한다면)

- **2026-08-02부터 적용**. AI와 직접 상호작용하는 시스템 고지, AI 생성 콘텐츠의 **기계 판독 가능한 표시**(제공자), 딥페이크 등 공개(배포자).
- 워터마킹 유예(2026-12-02까지)는 **2026-08-02 이전에 시장에 나온 생성형 AI 시스템에만** 적용됩니다. 그 뒤에 출시하는 게임·앱의 런타임 생성 기능은 출시 즉시 표시해야 합니다. 챗봇 고지·딥페이크 표시는 유예 없이 바로 적용([CSA 노트](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article50-watermarking-deadline/), [EU 요약](https://digital-strategy.ec.europa.eu/en/factpages/quick-facts-transparency-rules-ai-systems)).
- 위반 시 최대 1,500만 유로 또는 전 세계 연매출 3% 중 높은 금액([Cooley](https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026)). 준수 경로로 자율 [실천강령](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)이 있습니다.
- 사전 제작된 정적 3D 에셋 자체에는 주로 플랫폼 공개 규정(Steam 등)이 적용됩니다.

### 10.3 Steam (2026-01-16 개정)

[Game Developer 보도](https://www.gamedeveloper.com/business/valve-tweaks-and-clarifies-ai-disclosure-rules-for-steam) 등 요약 기준이며 Steamworks 원문은 열람하지 못했습니다.

| 구분 | 공개 대상 | 해야 할 일 |
|---|---|---|
| **Pre-Generated** | 게임 파일에 포함되어 출시되는 AI 제작 에셋(텍스처, 캐릭터 아트, 음성, LLM이 쓴 로어 등) | Content Survey에 AI로 만든 메시·텍스처 등을 구체적으로 기재. 불법·권리 침해가 없음을 보증 |
| **Live-Generated** | 플레이 중 AI가 만드는 콘텐츠 | 불법·유해 콘텐츠를 막는 **가드레일**과 그 설명 |
| **면제** | 코드 어시스턴트·디버깅 같은 개발 효율화 도구, **아이디어 구상에만 쓰고 출시물에 넣지 않은 콘셉트 아트** | MCP로 에디터 작업만 자동화하고 최종 에셋은 사람이 만들었다면 면제에 해당하는지 판단 근거를 기록 |

- 스토어 페이지·마케팅 자료가 공개 대상에 포함된다는 요약이 있으나 원문 문구는 **(미확인)**. 콘셉트 아트는 출시물이나 스토어·마케팅에 **실제로 쓰인 경우**만 공개하면 됩니다.
- 공개 문구 예: "일부 가구 3D 모델의 초안은 AI 3D 생성 도구로 만들었고, 모든 모델은 아티스트가 수정했습니다."
- "Steam 게임의 약 20%가 AI 사용을 공개"라는 수치는 단일 SEO 성격 출처이고 분모가 불명확합니다 **(신뢰도 낮음)**.

### 10.4 Fab · Sketchfab 태그

- **Sketchfab**: 2025-12-11 약관 개정으로 판매·다운로드 여부와 관계없이 **모든 AI 생성 모델에 CreatedWithAI** 표시(전에는 판매·다운로드 가능한 모델만). 사이트가 AI 생성을 감지하면 라벨을 자동으로 붙일 수 있습니다. 포트폴리오로 올릴 때도 해당합니다.
- **Fab**: AI 생성 콘텐츠를 배포하려면 **Created with AI 자가 신고** 의무. 신고 누락은 약관 위반으로 보고 자동 탐지 도구도 추가되었습니다([UE 포럼 공지](https://forums.unrealengine.com/t/update-on-products-generated-with-ai/2523501), [80.lv](https://80.lv/articles/epic-games-adresses-ai-generated-content-plaguing-fab)).
- **NoAI 태그**가 붙은 에셋은 AI 파이프라인(image-to-3D 레퍼런스, 학습, 스타일 참조)에 넣지 마세요.
- 참고로 NoAI·CreatedWithAI 태그는 Fab의 AI 범람 대응으로 생긴 것이 아니라 Sketchfab이 2023년 2월에 도입했습니다([Sketchfab 블로그](https://sketchfab.com/blogs/community/introducing-the-noai-createdwithai-tags/)). ArtStation의 NoAI는 2022년 12월입니다.

### 10.5 판단 흐름

```text
[AI를 어디에 썼나?]
 ├─ 에디터 자동화(MCP로 배치·코드 작성)만, 출시물에 AI 생성 콘텐츠 없음
 │    → Steam 면제 가능성. 판단 근거를 기록
 ├─ 개발 중 미리 생성한 에셋이 출시물·스토어·마케팅에 포함 (pre-generated)
 │    → Steam 공개, Fab/Sketchfab 태그, provenance·사람 기여 기록
 │    → 한국 AI기본법 적용 여부 (미확인): 법률 검토 권장
 └─ 게임·앱이 실행 중에 AI로 생성 (live-generated / 사용자에게 생성 기능 제공)
      → Steam 가드레일 설명
      → 한국 AI기본법 제31조 표시 설계(예술·창작물 완화 방식 검토)
      → EU 출시라면 제50조 기계 판독 표시(2026-08-02 이후 출시는 유예 없음)
```

---

## 11. 한국 창작자용 컴플라이언스 체크리스트

**도구 선택**

- [ ] Hunyuan 계열(2.0/2.1/Omni/Part, HunyuanWorld·HY-World, HY-Motion, BPT)을 로컬·제3자 API·MCP 옵션에서 모두 뺐다
- [ ] Tencent Cloud Hunyuan 3.x, MCP for Blender Premium은 약관 확인 전까지 상업 프로젝트에서 쓰지 않는다
- [ ] 로컬 모델은 코드뿐 아니라 가중치·배경 제거기·래스터라이저(nvdiffrast)·인코더(DINOv3)·텍스트→이미지 모델 라이선스까지 확인했다
- [ ] 연구 전용 모델(MeshAnything, MeshRipple 등)은 출시 에셋 경로에 없다
- [ ] Stable Fast 3D를 상업적으로 쓴다면 Stability 커뮤니티 라이선스에 등록했고 매출 기준을 기록했다

**생성**

- [ ] 출시할 에셋은 상업권이 있는 유료 플랜(Meshy 유료, Tripo Professional 이상, Marble Pro 이상)에서 생성했다
- [ ] Rodin 무료·체험 키로 만든 결과물은 비상업으로 분류했다
- [ ] Meshy 유료 에셋을 Meshy Community에 공개하지 않았다
- [ ] 모델 버전을 명시했다(Tripo SDK 기본값 v2.5 금지)
- [ ] 결제 영수증과 생성 당시 약관 캡처를 보관했다

**에셋 수집**

- [ ] 라이브러리 에셋은 CC0 우선, CC-BY는 credits.csv에 자동 수집된다
- [ ] NC·ND·NoAI·라이선스 불명 에셋이 빌드에 없다(`build_credits()`의 반환값이 빈 목록)
- [ ] BlenderKit RF·Fab 유료 에셋 원본을 공개 저장소에 커밋하지 않았다(`.gitignore`)
- [ ] Megascans·Fab 에셋은 "2024년 무료 획득분"과 "구매분"을 구분해 기록했다

**제작**

- [ ] 에셋마다 provenance(소스·버전·플랜·날짜·입력·라이선스·사람 수정 이력)가 있다
- [ ] `_gen` → `_retopo` → `_sculpt` → `_final` 버전 파일과 타임랩스로 사람 기여를 남겼다
- [ ] 유명 IP·상표·실존 디자이너 제품을 복제하라고 프롬프트하지 않았다
- [ ] 상업 프로젝트의 LLM은 Commercial Terms 경로(API/Team/Enterprise)로 쓰고, 개인 요금제라면 학습 옵트아웃을 켰다

**출시**

- [ ] Steam Content Survey에 pre-generated / live-generated를 구체적으로 기재했다
- [ ] Fab 판매 시 Created with AI, Sketchfab 게시 시 CreatedWithAI를 달았다
- [ ] 런타임 생성 기능이 있으면 AI기본법 제31조 표시(가시 라벨 또는 메타데이터)를 설계했다
- [ ] EU에 출시한다면 제50조 기계 판독 표시를 넣었다
- [ ] 한국저작권위원회에 등록한다면 AI 생성 부분과 사람 창작 부분을 구분해 적었다

---

## 12. 다른 사람들은 어떻게 했나

| 사례 | 누가·언제 | 무엇을 어떻게 | 교훈 |
|---|---|---|---|
| [image-to-3dlab](https://github.com/Bingeljell/image-to-3dlab) | Bingeljell, 2026-09(별 약 136개) | 로컬(Apple Silicon 32GB 또는 NVIDIA 24GB)에서 이미지·텍스트 → 게임레디 PBR GLB. 백엔드 Pixal3D, Hunyuan3D-MLX, TRELLIS.2(M5 MacBook에서 15~35분), SF3D 중 선택. Finish = voxel remesh → decimate(90만 → 4만) → (선택) Hunyuan 2.1 PBR 리페인트(약 6분) → JPEG 2048(32MB → 5MB 미만). 결과마다 `.provenance.json` | **컴포넌트별 라이선스 게이트**의 좋은 예: Hunyuan은 "EU/UK/한국 불가", TRELLIS.2·Pixal3D는 DINOv3 때문에 "commercial-conditional", RMBG-2.0은 기본 비활성화, Qwen-Image 2.1 경로는 비상업. 저장소 코드는 Apache-2.0 |
| [Paper Ember Duel](https://github.com/AIWHOS/paper-ember-duel) | AIWHOS, 2026-09-10~13 | GPT-6/Codex로 기획·코드, Hyper3D Rodin MCP로 "Gen-2.5 Medium / Raw" 백만 면급 원본 생성(웹의 Extreme-High는 일부러 피함), BANG으로 캐릭터를 메시 부품 8개로 분해, Blender에서 메시 연결·감면·스킨 웨이트·무기 그립을 수작업 보정, Godot 4.7.2 임포트 | 고폴리 원본은 엔진 투입 전 감면이 필수. README에 "코드·아트에 통일된 오픈소스 라이선스 없음, 상업적 재사용 불허" — 남의 결과물을 에셋으로 가져다 쓰면 안 됩니다 |
| [rodin-via-blender](https://github.com/KaelNebula/rodin-via-blender) | KaelNebula, 2026-05 | 쇼핑몰 설치용 FRP 캐릭터 조형물(높이 1.1/1.5/1.8/2.0m). 4면 레퍼런스 → Rodin v2(bbox·tier 지정, 유료 키 권장) → Blender MCP로 Voxel/QuadriFlow/Subsurf 정리, Shrinkwrap·Boolean으로 부조 데칼 → 수밀성·스케일·셸 두께·언더컷 검증 → OBJ/STL/GLB + 도색 사양서. Claude Code 스킬 | 실물 조형물 제작에도 같은 리메시·검증 원칙이 통합니다 |
| [Meshy game-asset-pipeline](https://github.com/meshy-dev/game-asset-pipeline) | Meshy 공식, 2026-05 | art_style 선택 → preview(약 30초) → refine(약 2분) → Remesh 1K~300K → 최대 4K PBR → GLB/FBX/OBJ/USDZ/BLEND. Unity Scale 0.01·URP/HDRP Lit, UE5 정적 소품 Nanite·캐릭터 IK Retargeter | 플랜별 라이선스(무료 CC BY 4.0, 유료 비공개)를 명시한 1차 자료 |
| [Quartermaster](https://github.com/Tanshaydar/Quartermaster) | Tanshaydar, 2026-09 | 보유 에셋을 로컬 SQLite에 색인해 MCP `search_owned_assets`, `validate_stack`, `import_asset_to_project`, `audit_project`로 노출 | "생성보다 먼저 이미 산 에셋을 찾게 한다"는 패턴. 단 수집 방식이 약관 위반 위험이 크고(Unity 구매 목록 페이지는 2026-08 이후 404), 별 2개 수준 |
| MCP for Blender 에셋 통합 | Siddharth Ahuja 외, 2026-09 | Poly Haven·Sketchfab·Poly Pizza·Hyper3D·Hunyuan3D를 한 MCP로. 가져온 에셋에 라이선스·저작자 커스텀 프로퍼티 | 라이선스 메타데이터를 **가져오는 순간** 남기는 설계가 핵심 |

더 많은 사례는 [사례 모음](../04_case_studies/01_case_studies.md)에 있습니다.

---

## 흔한 실수와 해결

| 실수 | 증상 | 해결 |
|---|---|---|
| 생성 원본을 바로 Decimate | 의자 다리·난간이 끊어지고 구멍이 생김 | Voxel Remesh → Decimate 순서 |
| gltfpack 기본값으로 LOD 생성 | UE에서 이름 규칙(UCX_, _LOD)이 인식되지 않고 provenance가 사라짐. 일부 임포터에서 양자화 확장 문제 | `-kn -km -ke -noq` |
| 하드 엣지 많은 메시에 `-si 0.5` | 삼각형 수가 거의 그대로 | `-sp` 추가, 또는 스무스 셰이딩 후 내보내기 |
| glTF-Transform `simplify`에 오차 한도 미지정 | 목표 비율 미달(테스트: 50% 목표에 91% 남음) | `--error 0.01` 등 명시 |
| 엔진 원본에 `gltf-transform optimize` | 모르는 사이 메시가 단순화·양자화·meshopt 압축됨 | 원본은 비압축으로 두고, `optimize`는 웹 배포본에만(`--simplify false` 검토) |
| `npx gltf-validator out.glb`로 검사 | "could not determine executable to run" | `gltf-transform validate` 또는 2.6절 Node 스크립트 |
| Tripo SDK 기본값·옛 문서 값 사용 | 구버전 모델(v2.5)로 생성되거나 smart_lowpoly가 거부됨 | `model_version` 명시, smart_lowpoly는 `P-v2.0-20251226` |
| 소스마다 스케일·피벗이 다름 | 가구가 떠 있거나 파묻힘, 배치 좌표 오류 누적 | 임포트 직후 1 m 단위·원점 바닥 중앙·Apply Scale, `scene_audit.py`로 확인. 배치는 [08 가이드](08_scene_layout_placement.md) |
| 소품마다 텍스처 해상도를 제각각 4K로 | 같은 방 안에서 선명도가 들쭉날쭉 | 텍셀 밀도 통일(2.3절) |
| UE에 OpenGL 노멀맵 그대로 | 요철이 뒤집혀 보임 | Flip Green Channel 또는 DirectX용 베이크(UE 규약은 1차 문서로 재확인) |
| "MIT니까 상업 OK" | 의존성(nvdiffrast 등)의 비상업 조항 위반 | 7장 표로 파이프라인 전체 점검 |
| 무료 플랜으로 만든 에셋을 그대로 출시 | Tripo 무료는 비상업, Meshy 무료는 표기 누락 시 위반 | 유료 플랜에서 재생성 + provenance에 플랜 기록 |
| Meshy 유료 에셋을 커뮤니티에 공개 | 비공개 소유 조건이 깨짐 | 공개 갤러리에 올리지 않기 |
| Sketchfab에서 NC·ND 모델 사용 | 상업 배포 불가, 리토폴 같은 수정도 불가(ND) | 라이선스 화이트리스트를 에이전트 규칙으로 강제(1.4절) |
| AI 원본만으로 저작권 주장 | 보호 대상 아님 | 사람의 수정 이력·버전 파일·타임랩스 보관 |
| 계도기간이니 AI기본법은 나중에 | 의무는 이미 발효 | 런타임 생성 기능이 있으면 지금 표시 설계 |

---

## 관련 문서

- [README](../README.md) — 저장소 개요와 읽는 순서
- [00 목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [01 AI 모델·클라이언트·비용](01_ai_models_and_clients.md) — 상업 경로(API/Team/Enterprise) 선택
- [02 Blender MCP](02_blender_mcp.md) — 공식 Blender Lab 커넥터 vs ahujasid MCP for Blender, 보안·API 함정
- [03 기타 MCP·엔진](03_other_mcp_dcc_cad_engines.md) — UE 5.8 공식 실험적 Unreal MCP, Unity·Godot MCP
- [04 AI 3D 생성](04_ai_3d_generation.md) — 생성기 비교, 후처리 7장, 상업 파이프라인 함정 9장
- [05 텍스처링·재질](05_texturing_materials.md) — 베이크 코드, ORM, glTF 슬롯 감사, 텍셀 밀도
- [07 모델링](07_modeling_objects_furniture_sculpture.md) · [08 배치](08_scene_layout_placement.md)
- [09 에이전트 워크플로](09_agent_workflow_prompting.md) — 검증 루프, CLAUDE.md·스킬
- [11 연구 논문](11_research_papers.md) — 검색·재사용 기반 생성 연구
- [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수표](../03_playbooks/05_reference_dimensions.md)
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [blender-aaa-scene 스킬](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [보조 스크립트](../03_playbooks/scripts/README.md) — `scene_audit.py`, `placement_utils.py`, `review_views.py`
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- `01_research/raw/12_assets-pipeline-licensing.research.json` — 에셋 소스, 게임레디 파이프라인, 라이선스·법률 1차 조사
- `01_research/raw/12_assets-pipeline-licensing.verify.json` — 독립 검증(TRELLIS.2 nvdiffrast 비상업, Step1X-3D Hunyuan 헤더, BPT 라이선스, Tripo SDK 현행값, gltfpack `-noq`/`-ke`, AI기본법 ③④항 등 정정·누락 반영)
- `01_research/raw/G4_licensing_pricing.gap.json` — 상용 약관·가격·플랫폼 공개 규정·저작권·표시 의무 보완 조사
- `01_research/raw/G4_licensing_pricing.verify.json` — 보완 검증(Meshy 유료 소유 조건, Tripo·Rodin 가격 정정, Hunyuan MAU 조건, EU 유예 범위, Steam 면제 범위, Anthropic 약관 예외 등)
- Hunyuan3D-Part·HY-World 2.0·HY-Motion 라이선스 링크는 `01_research/raw/05_ai-3d-generation.verify.json`에서 가져왔습니다.
- 이 문서 작성 중 추가 테스트(2026-09-27): pip `bpy` 4.2.23 LTS·5.0.1(provenance → glTF extras, UCX·LOD 헬퍼), `gltfpack` 1.3, `@gltf-transform/cli` 4.5.0, npm `gltf-validator` 2.0.0-dev.3.10. 결과는 2.5·2.6·4.1·5.4절에 적었습니다.

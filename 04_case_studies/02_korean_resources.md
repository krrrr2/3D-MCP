# 한국어 자료 모음: AI + MCP 3D 제작

> 기준일: 2026-09-27 · 한국어 유튜브·블로그·강의·커뮤니티·뉴스와 한국(추정) GitHub 사례를 신뢰도와 함께 정리하고, 한국 사용자만 겪는 함정(라이선스 지역 제외, 한국어 UI, 한국 치수)을 모았습니다.

## 핵심 요약

- 한국어 자료는 **설치·연결 가이드와 뉴스가 대부분**입니다. AAA 품질, 가구 배치·레이아웃, 리토폴로지·UV·베이크 자동화를 다룬 한국어 자료는 거의 없습니다. 이 부분은 영어권 사례([사례 모음](./01_case_studies.md))와 이 저장소의 가이드로 채워야 합니다.
- 원문을 직접 열어 본 한국 자료는 **GitHub 저장소 4개**(octopus7, openerai, tahooki, Aryeon0228)뿐입니다. 나머지 한국어 웹 자료(유튜브, 블로그, 클리앙, 뉴스)는 조사 환경에서 접속이 막혀 **검색 결과의 제목·요약으로만** 확인했습니다. 한국어 보완 조사(G2)는 별도의 독립 검증도 거치지 않았습니다.
- 한국(추정) 사례의 핵심은 두 건입니다. [octopus7/astra-blender-forest](https://github.com/octopus7/astra-blender-forest)는 채팅만으로 만든 Blender Python 패키지로 나무 3,800그루, 인스턴스 16,573개를 배치하고 UE HISM으로 내보냅니다. [openerai/blender-previz-video](https://github.com/openerai/blender-previz-video)는 그레이박스 프리비즈를 AI 영상으로 바꾸는 한국어 Claude Code 스킬입니다. 둘 다 '한국 사례'라는 판단 자체가 추정입니다.
- 블렌더 MCP를 정면으로 다루는 한국어 유료 강의는 패스트캠퍼스 강의 1개뿐입니다. 언리얼·유니티 MCP 전용 한국어 강의는 찾지 못했습니다.
- 국내 커뮤니티의 평가는 영어권과 같습니다. "속도는 매우 빠르지만 고급 모델러 수준에는 못 미치고, 며칠 만에 만든 결과는 인디 프로토타입 수준"이라는 것입니다. AI에게는 블록아웃·반복 작업·배치를 맡기고, 최종 품질은 PBR·라이팅·리토폴로지 같은 전통 기법과 사람의 마무리로 끌어올려야 합니다.
- 국내 기업 사례로는 NC AI '바르코 3D'가 있습니다(리니지M 배경 작업 2~3주 → 약 1주. '4주→3분'은 홍보 문구). 다만 MCP 기반이 아니고, MCP로 3D 파이프라인을 운영한다고 공개한 국내 게임사는 없습니다.
- "10분", "50분 만에 영상", "4주→3분" 같은 헤드라인 수치는 전부 개인 주장이거나 홍보 문구입니다. 독립적으로 검증된 'AAA급' AI+MCP 결과물은 국내외 어디서도 찾지 못했습니다.
- **한국 사용자가 꼭 알아야 할 세 가지**: ① Hunyuan3D 계열 오픈웨이트는 라이선스 적용 지역에서 한국이 빠져 있고 출력물 사용도 제한됩니다(한국어 소개 글에는 이 경고가 거의 없습니다). ② 한국어 UI에서는 노드 이름이 번역되어 에이전트 코드가 깨질 수 있습니다. ③ 가구·주거 치수는 한국 값을 mm로 지정합니다.
- 한국어 가이드는 공식 Blender 커넥터(Blender Lab)와 커뮤니티 서버(ahujasid MCP for Blender)를 구분하지 않고 설명하는 경우가 많아 보입니다(검색 요약 기준 추정). 둘 다 `localhost:9876`을 쓰므로 한 번에 하나만 켜야 합니다.

## 이 문서 읽는 법

| 표시 | 뜻 |
|---|---|
| **높음** | 원문(주로 GitHub)을 직접 열어 확인했거나, 여러 매체의 보도 내용이 서로 일치 |
| **중간** | 검색 결과로 내용 요지를 확인. 원문은 읽지 못함 |
| **낮음** | 단일 SNS, 큐레이션·번역·제휴 콘텐츠, 또는 제목만 확인 |
| **검색 요약** | 원문을 열지 못하고 검색 결과의 제목·요약으로만 확인한 항목. 조사 환경에서 유튜브, 네이버, velog, 클리앙, 뉴스 사이트 등이 차단됐기 때문입니다([조사 방법](../01_research/research_method.md) 4절) |
| **원문 확인** | 페이지를 직접 열어 내용을 확인 |
| (추정) / (미확인) | 원자료에 근거가 약하거나 확인하지 못한 값 |

- 채널명, 게시일, 가격은 대부분 확인하지 못했습니다. 빈칸 대신 '미확인'으로 적었습니다.
- 목록은 "무엇이 있는지"를 알려 주는 용도입니다. 내용을 인용하거나 따라 하기 전에 원문 날짜와 버전을 직접 확인하세요. 이 분야는 매주 바뀝니다.

## 1. 목적별 바로가기

| 하고 싶은 일 | 먼저 볼 한국어 자료 | 이어서 볼 이 저장소 문서 |
|---|---|---|
| Claude와 Blender 처음 연결 | 패스트캠퍼스 미디어 입문 가이드, Threads @dddesign.io(공식 커넥터), brunch(Mac) | [빠른 시작](../03_playbooks/01_quickstart_setup.md), [Blender MCP](../02_guides/02_blender_mcp.md) |
| MCP의 동작 원리와 한계를 팀에 설명 | tali.kr, 박재홍의 실리콘밸리 | [에이전트 워크플로](../02_guides/09_agent_workflow_prompting.md) |
| GPT-6 Astra로 Blender 작업 | 다나와 DPG, 유튜브 2편, 클리앙 Astra 글 | [AI 모델 선택](../02_guides/01_ai_models_and_clients.md), [사례 모음](./01_case_studies.md) |
| 작업별 모델 고르기 | AI타임스 Opus 5.5 비교, AI매터스 Astra 대 Fable 5.1 | [AI 모델 선택](../02_guides/01_ai_models_and_clients.md) |
| Unreal 연동 | 게임뷰 전·후편, velog UE5 세팅, tahooki/unreal-blender-mcp | [기타 DCC·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md) |
| Unity 연동 | duplicat.kr, kiweb, Apidog 한국어, 유튜브 연동 영상 | [기타 DCC·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md) |
| SketchUp·건축·인테리어 | 뽁숑이, 긱톡, brunch '스케치업이냐, 라이노냐' | [기타 DCC·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md), [배치](../02_guides/08_scene_layout_placement.md) |
| 대규모 야외 배치(숲·도시) | octopus7/astra-blender-forest | [배치](../02_guides/08_scene_layout_placement.md) 7절 |
| 시네마틱 영상(프리비즈) | openerai/blender-previz-video | [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md) |
| 재질·라이팅 기초 | 유정통 3D, iRender 한국어, 아키스케치, Substance 한국어 튜토리얼 | [텍스처링](../02_guides/05_texturing_materials.md), [라이팅](../02_guides/06_lighting_rendering_art_direction.md) |
| 가구 형태를 제대로 | blender.pe.kr, 가구·집 모델링 유튜브 강좌 | [모델링](../02_guides/07_modeling_objects_furniture_sculpture.md), [치수 기준표](../03_playbooks/05_reference_dimensions.md) |
| 이미지·텍스트로 3D 생성 | 인프런 Meshy 클립(Hunyuan3D 자료는 라이선스 주의) | [AI 3D 생성](../02_guides/04_ai_3d_generation.md) |

## 2. 한국 사용자 주의사항 (요약)

| 주의 | 무엇이 문제인가 | 할 일 | 자세히 |
|---|---|---|---|
| **Hunyuan3D 계열 라이선스** | Tencent Hunyuan3D 2.0·2.1·Omni·Part, HY-World, HY-Motion, BPT의 오픈웨이트 라이선스는 적용 지역에서 EU·영국·**대한민국**을 뺍니다. 2.0·2.1 라이선스는 머리말부터 "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"입니다. 지역 밖에서는 **출력물의 사용·배포·전시도 금지**됩니다(5(c)항). 한국어 소개 글(파이토치 한국 사용자 모임, secondbrush, 출시 기사)은 이 점을 다루지 않습니다 | 로컬 가중치, 제3자가 호스팅한 가중치 API, MCP for Blender의 Hunyuan3D 연동을 모두 끕니다. Tencent Cloud API 약관은 별개이며 원문을 확인하지 못했습니다(미확인) | [2.0 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE), [2.1 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE), [AI 3D 생성](../02_guides/04_ai_3d_generation.md), [라이선스](../02_guides/10_assets_pipeline_licensing.md) 7절 |
| 'MIT'라도 의존성 확인 | [TRELLIS.2](https://github.com/microsoft/TRELLIS.2) 코드는 MIT지만, 텍스처링과 GLB 후처리가 비상업 조건의 [nvdiffrast](https://github.com/NVlabs/nvdiffrast/blob/main/LICENSE.txt)를 씁니다 | 상업 프로덕션이면 의존성 라이선스까지 검토 | [라이선스](../02_guides/10_assets_pipeline_licensing.md) 7절 |
| **한국어 UI 노드 이름** | UI를 현지화하면 새로 만든 노드 이름이 번역될 수 있어 `nodes['Principled BSDF']` 같은 코드가 깨집니다. 일본어 UI에서 실패한 사례가 [문서화](https://github.com/hideki711014/roo-blendermcp-jp-rules)되어 있고, 한국어 UI도 원리가 같습니다(추정. 한국어 UI로 직접 재현하지는 못했습니다) | ① 노드는 이름이 아니라 type으로 찾게 합니다(`n.type == 'BSDF_PRINCIPLED'`). ② 에이전트가 조작하는 Blender는 영어 UI를 쓰거나 New Data 번역을 끕니다(`bpy.context.preferences.view.use_translate_new_dataname = False`. 이 속성이 있다는 것은 bpy 4.2.23·5.0.1에서 확인했지만, 번역 동작 자체는 확인하지 못했습니다). ③ 오브젝트 이름은 영어로 붙입니다. 이 저장소의 `scene_audit.py`는 이름 속 영어 단어(`dining_table_01`, `SM_Armchair_A`처럼 snake_case·CamelCase 모두 인식)로 치수 규칙을 고르고, `building_audit.py`는 `Floor_living`, `Door_...`, `Window_...` 같은 이름으로 방·문·창을 찾습니다. 한국어 이름은 둘 다 인식하지 않습니다(`building_audit.py`는 `obj["role"] = "door"`, `obj["room_type"] = "living"` 같은 커스텀 프로퍼티로 대신 지정 가능) | [Blender MCP](../02_guides/02_blender_mcp.md) 12절, [워크플로](../02_guides/09_agent_workflow_prompting.md), [보조 스크립트](../03_playbooks/scripts/README.md) |
| **한국 치수** | '킹', '표준 방문' 같은 이름은 나라마다 크기가 다릅니다. 한국 K 매트리스 폭은 1600 mm(표준표 기준)이고 미국 King은 1930 mm입니다 | AI에게는 이름 대신 mm 값을 넘깁니다. 아래 표 참고 | [치수 기준표](../03_playbooks/05_reference_dimensions.md), [배치](../02_guides/08_scene_layout_placement.md) 6절 |
| **공식 커넥터와 커뮤니티 서버 혼동** | 한국어 가이드 상당수(패스트캠퍼스 미디어, brunch)는 uv 설치와 BlenderMCP 탭의 Start/Connect 버튼을 쓰는 커뮤니티 서버 기준으로 보입니다(추정). Threads @dddesign.io 글은 공식 커넥터 기준입니다. 두 서버 모두 `localhost:9876`을 씁니다 | 한 번에 하나만 켭니다. 공식 커넥터 애드온은 Blender 5.1.0 이상이 필요하고(manifest 기준), Edit > Preferences에서 Allow Online Access가 켜져 있어야 시작된다는 보고가 있습니다. 커뮤니티 서버는 익명 텔레메트리가 기본으로 켜져 있으니 `DISABLE_TELEMETRY=true`로 끕니다 | [빠른 시작](../03_playbooks/01_quickstart_setup.md), [Blender MCP](../02_guides/02_blender_mcp.md) 2·10절 |
| **오래된 한국어 강좌** | 무료 한국어 기초 강좌는 Blender 3.0 전후 자료가 많습니다. 5.x에서는 `Material/World.use_nodes` 폐기가 예고됐고, EEVEE 식별자도 `'BLENDER_EEVEE'`입니다(4.2~4.x는 `'BLENDER_EEVEE_NEXT'`) | 강좌에서는 개념만 가져오고, 에이전트에게는 쓰는 버전을 명시합니다(2026-09 기준 최신 안정판은 5.2 LTS 계열의 5.2.2, 이전 LTS 4.5·4.2도 유지 중) | [Blender MCP](../02_guides/02_blender_mcp.md) 11절 |
| **인공지능기본법** | 2026-01-22에 시행됐습니다. 제31조의 생성형 AI 결과물 표시 의무는 이미 발생했고, 계도기간은 법적 유예가 아니라 행정 운영 방침입니다 | 게임·앱에 런타임 AI 생성 기능이 있으면 표시 방식을 설계합니다. 저작권 등록은 사람의 창작적 기여 부분만 가능합니다(문체부·한국저작권위원회 2025-06 안내서) | [라이선스](../02_guides/10_assets_pipeline_licensing.md) 10·11절 |

### 한국 주거·가구 치수 빠른 참고 (mm)

| 항목 | 한국 값 | 주의 |
|---|---|---|
| 아파트 천장고 | 2300(구축·표준 설계), 2400~2500(2020년대 신축 추세) | 층고 2800~2850. 연식별로 프리셋을 나눕니다 |
| 매트리스 Q | 1500×2000 | 조사한 6개사 모두 같음 |
| 매트리스 K / LK | 표준표는 1600 / 1800 × 2000. 브랜드별로 K 1600~1670, LK 1700~1800, 길이 2000~2075 | 미국 King은 폭 1930. 이름 대신 mm로 지정 |
| 싱크대(조리대) 높이 | 850(오래된 산업 표준), 최근 900 권장도 있음 | 미국은 914. 독립 재검증은 하지 못함 |
| 방문 | 900×2100(**문틀 기준**). 문짝은 약 60 mm 작음 | 벽 개구부는 문틀 외곽 치수로 뚫습니다 |
| 공동주택 공용계단 | 단높이 180 이하, 단너비 260 이상. 높이 2 m를 넘으면 2 m 이내마다 계단참(너비 1200 이상) | 층고 2800을 직통 16단으로 만들면 안 됩니다(예: 8단 + 계단참 + 8단) |

근거와 전체 표는 [치수 기준표](../03_playbooks/05_reference_dimensions.md)에 있습니다. 매트리스 근거: [퀸 규격 6개사 비교](https://www.consumernews.co.kr/news/articleView.html?idxno=713641), [킹·라지킹 브랜드별 차이](https://www.consumernews.co.kr/news/articleView.html?idxno=520936)(소비자가만드는신문).

## 3. 한국 사례

### 3.1 GitHub에 공개된 한국(추정) 프로젝트

| 제목 | 작성자 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| astra-blender-forest | octopus7 | 2026-09-13~14 | ChatGPT 채팅(Codex 아님)으로 생성한 Blender Python 패키지. 300×300 m 로우폴리 호수 숲(나무 3,800그루, 랜드마크 포함 3,839), 배치 인스턴스 16,573개, 재사용 메시 127개, 랜드마크 영역 12곳. UE HISM 내보내기·임포트 스크립트 포함 | 대규모 야외 배치를 메시 공유, 인스턴싱, 고정 seed로 처리하는 실제 코드. 순수 Python 테스트 30개 | [GitHub](https://github.com/octopus7/astra-blender-forest) | 높음 · 원문 확인(수치와 MIT 라이선스 검증됨). 단 '한국 사례'는 README_KO(영·한·일 중 하나)만 근거라 추정, 모델 'Astra'도 저장소 이름에만 나와 추정 |
| blender-previz-video | openerai | 2026-09-08 | 한국어 Claude Code 스킬. Blender 그레이박스로 카메라·컷·타이밍·동선을 먼저 고정하고, 뷰포트 렌더를 Seedance 2.5에 video-to-video로 넣음. Higgsfield Bridge 커넥터와 Blender 플러그인(bl_* MCP 도구) 사용. Blender 5.0 이상 | 프롬프트 규칙 13개. '블로킹과 텍스트가 충돌하면 블로킹이 이긴다' 규칙은 다른 영상 워크플로에도 그대로 쓸 수 있음 | [GitHub](https://github.com/openerai/blender-previz-video) | 높음 · 원문 확인. 원래 방법론은 Higgsfield 블로그의 @adilinthewild 글(2026-08-28)이고 이 저장소는 그것을 한국어 스킬로 재구성한 것. LICENSE 파일은 없고 README에 '문서 텍스트는 MIT'라고만 적혀 있음. 최종 결과물은 3D 렌더가 아니라 AI 영상 |
| unreal-blender-mcp (한국어 Project-document) | tahooki | 미확인 | blender-mcp를 확장해 Unreal과 Blender를 한 MCP 서버로 제어. 허브앤스포크 구조: 중앙 MCP 서버(8300, SSE), Blender 애드온(8400), Unreal 플러그인(8500). Blender 쪽은 씬·오브젝트·머티리얼·PolyHaven·Hyper3D, Unreal 쪽은 레벨 생성·에셋 임포트·Python 실행, LangChain 기반 메모리 | Blender에서 만든 에셋을 Unreal 레벨에 배치하는 통합 파이프라인 설계를 한국어로 볼 수 있음 | [설계 문서](https://github.com/tahooki/unreal-blender-mcp/blob/main/Project-document.md) | 높음 · 원문 확인. 라이선스와 유지보수 상태는 미확인 |
| BlenderMCP (한국어 README) | Aryeon0228 | 미확인(Blender 5.0.1 기준이라 2026 추정) | ahujasid 서버 파생판. Blender를 띄워 둔 채 소켓으로 명령을 보냄. 뷰포트 스크린샷, 오브젝트·머티리얼 조작, bpy 실행. Windows 10, Python 3.8 이상, Blender 5.0.1 이상 | 명령당 0.1~1초로, 명령마다 Blender를 새로 띄우는 서브프로세스 방식(10~15초)보다 약 100배 빠르다고 주장. 비교 대상은 ahujasid 서버가 아니라 서브프로세스 방식이라는 점에 주의 | [GitHub](https://github.com/Aryeon0228/BlenderMCP), [glama](https://glama.ai/mcp/servers/@Aryeon0228/BlenderMCP) | 높음 · 원문 확인. 속도 수치는 저자 자체 주장. MIT. Windows 한정, 기본 프리미티브 위주 |
| unreal_bp_mcp 클라이언트 설정 가이드(한국어) | BestDev | 미확인 | 언리얼 블루프린트용 MCP 서버의 한국어 클라이언트 설정 문서(glama 미러) | 블루프린트 조작 MCP를 붙일 때 참고 | [glama](https://glama.ai/mcp/servers/@BestDev/unreal_bp_mcp/blob/fab6d0f35a553450a8cdf90bf3762dfa443582e8/docs/MCP_CLIENT_SETUP.md) | 낮음 · 검색 요약 |

### 3.2 octopus7/astra-blender-forest는 어떻게 했나

근거: [저장소](https://github.com/octopus7/astra-blender-forest). 모든 항목은 README 기준이며, 검증 에이전트가 수치를 다시 확인했습니다.

1. **요청 방식**: Codex 같은 코딩 에이전트가 아니라 ChatGPT 대화에서 "실행 가능한 Python 패키지" 형태로 받았습니다. LLM이 좌표를 하나씩 찍지 않고, 규칙과 seed로 좌표를 계산하는 코드를 만들게 한 것이 핵심입니다.
2. **결정적 생성**: 지형을 50×50 m 셀 36개로 나누고 seed 42로 생성합니다. 같은 seed면 같은 숲이 나옵니다.
3. **메시 공유**: 반복되는 오브젝트는 메시 데이터블록 127개를 공유합니다. 인스턴스 16,573개가 메시 127개로 표현됩니다.
4. **실행 순서**: Blender 4.2 이상에서 `01_build_scene.py` → `02_export_unreal.py`(셀·에셋 ID별 FBX와 배치 매니페스트 생성) → Unreal에서 `03_import_unreal.py`.
5. **엔진 변환 규칙**: 반복 에셋은 셀·에셋 ID별 HISM(Hierarchical Instanced Static Mesh)으로, 고유 오브젝트는 Static Mesh Actor로 보냅니다.
6. **테스트**: 지오메트리, 배치, 결정성, Blender→UE 변환을 검사하는 순수 Python 테스트 30개가 있습니다.
7. **한계**: 콜리전, LOD, World Partition은 범위 밖입니다. Blender와 UE에서 실제로 실행한 기록은 검증 자료에 없습니다.

**배울 점**: 채팅만으로도 결과물을 "코드 패키지"로 요구하면 대규모 배치를 재현할 수 있게 만들 수 있습니다. 이 저장소의 [배치 가이드](../02_guides/08_scene_layout_placement.md) 7절(야외 산포)과 같은 원리입니다.

따라 할 때의 요청 예시(이 문서가 작성한 예시이며 원 저장소의 프롬프트가 아닙니다):

```text
Blender 4.2 이상에서 실행할 Python 패키지를 만들어 줘. 300×300 m 로우폴리 숲 장면이다.
- 1 unit = 1 m, Z-up. 50×50 m 셀로 나누고 seed를 인자로 받아 결과가 항상 같게 할 것
- 나무·바위는 종류별 메시 1개를 만들고 나머지는 같은 메시 데이터를 공유하는 인스턴스로 배치
- 호수·길 위에는 나무를 두지 말 것(마스크로 제외). 나무끼리 최소 간격 규칙을 둘 것
- 배치 결과를 JSON 매니페스트(에셋 ID, 위치, 회전, 스케일)로도 저장
- 순수 Python으로 돌아가는 테스트(개수, 겹침, 결정성)를 함께 작성
```

### 3.3 openerai/blender-previz-video는 어떻게 했나

근거: [저장소](https://github.com/openerai/blender-previz-video) README.

1. **설치**: `~/.claude/skills/`에 클론한 뒤 Claude Code에서 `/blender-previz-video`로 호출합니다.
2. **흐름**: 인테이크 → 샷 설계 → 블로킹 브리프 → Blender 실행 → 뷰포트 렌더 → 레퍼런스 정리 → 4블록 생성 프롬프트 → 리비전. MCP가 연결되지 않았으면 핸드오프 모드로 바꿉니다.
3. **도구**: Higgsfield Bridge 커넥터와 Blender 플러그인의 `bl_*` MCP 도구를 씁니다. `bl_get_skill`로 `blender-greybox`, `blender-lighting-camera` 같은 모듈을 불러옵니다.
4. **역할 분리 규칙**: 블로킹 영상은 카메라 궤적, 컷, 타이밍, 동선을 맡고, 텍스트 프롬프트는 재질, 조명, 그레이딩, 의상을 맡습니다. 둘이 충돌하면 블로킹이 이긴다고 프롬프트에 명시합니다.
5. **재사용**: 구조(블로킹 마스터)는 그대로 두고 스타일만 바꿔 실사, 2D 애니메이션, 스톱모션으로 뽑을 수 있습니다.
6. **한계**: 최종 화면은 AI 영상이라 게임이나 실시간 3D 에셋으로는 쓸 수 없습니다. Higgsfield는 유료입니다. SNS에서 '포토리얼 3D'로 보이는 결과물 중 상당수가 이런 방식이니, 실제 3D 렌더와 구분해서 보세요.

### 3.4 한국어로 소개된 제작 사례 한눈에 보기

| 사례 | 누가 | AI·도구 | 어떻게 | 결과·한계 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| GPT-6 Astra로 Blender 'Backrooms' 영상과 도시 게임 | 국내외 사용자 사례를 다나와 DPG가 정리(2026-09) | GPT-6 Astra, Blender, Codex, Computer Use | 프롬프트 약 5개로 모델링·연출 30분, 내보내기 20분. 이미지를 Codex에 올려 Blender 파일로 바꾸는 흐름도 소개 | '50분 만에 유튜브 영상', '5일짜리 도시 게임'이라는 헤드라인. 품질 검증 없음 | [다나와 DPG](https://dpg.danawa.com/news/view?boardSeq=60&listSeq=6058609), [promppy](https://www.promppy.com/item/1433678) | 낮음(수치는 개인 주장, 출처 1곳) · 검색 요약 |
| 2D 로봇 그림 → 3D → 랜딩 페이지 | 한국어 유튜버(채널명 미확인) | Claude, Blender MCP | 2D 이미지를 레퍼런스로 3D 모델을 만들고 웹 랜딩 페이지에 적용 | '완전 자동화'를 내세움. 스타일라이즈드 수준으로 추정 | [YouTube](https://www.youtube.com/watch?v=I5rtlgAvoV4) | 중간 · 검색 요약 |
| SketchUp 자동 모델링 + AI 렌더 | 건축·인테리어 유튜버 뽁숑이(2026 추정) | Claude 커넥터(MCP), SketchUp, AI 렌더러 | 매스 모델을 자동 생성한 뒤 AI 렌더러로 시각화. 연결 방법은 쇼츠로 공개 | 실무 관점 워크플로 시연 | [YouTube](https://www.youtube.com/watch?v=GOaWRhrsQC0), [쇼츠](https://www.youtube.com/shorts/WyzHiIZ1J3I?cbrd=1) | 중간 · 검색 요약 |
| Unity 드리프트 게임 프로토타입 30분 | Threads @secret_canada_(2025~2026) | Claude Code, [CoderGamester/mcp-unity](https://github.com/CoderGamester/mcp-unity), 무료 에셋 | Unity 설치 → Claude Code 실행 → mcp-unity 연결 → 무료 에셋으로 약 30분 워밍업 | "캐주얼 게임이라면 며칠이면 된다"는 평가 | [Threads](https://www.threads.com/@secret_canada_/post/DTCjtmzjJPD/video-%EC%9D%B4%EC%A0%A0-unity3d-mcp-%EB%A1%9C-%ED%81%B4%EB%A1%9C%EB%93%9C-%EC%BD%94%EB%93%9C-%EB%B6%99%EC%97%AC%EC%84%9C-%EA%B2%8C%EC%9E%84%EB%A7%8C%EB%93%9C%EB%8A%94%EA%B2%8C%EA%B0%80%EB%8A%A5%ED%95%B4%EC%A7%90-%EC%98%A4%EB%8A%98-%EC%B2%98%EC%9D%8C-30%EB%B6%84-%EC%A0%95%EB%8F%84-%EC%9B%8C%EB%B0%8D%EC%97%85-%EC%9C%BC%EB%A1%9C-%EB%93%9C%EB%A6%AC%ED%94%84%ED%8A%B8-%EA%B2%8C%EC%9E%84-%EC%9D%84-%EB%A7%8C%EB%93%A4%EC%96%B4-%EB%B3%B4%EA%B3%A0%EC%8B%B6%EC%96%B4%EC%84%9C-%EB%AC%B4?hl=ko) | 중간(개인 테스트, n=1) · 검색 요약 |
| UE 5.8 MCP로 게임 개발 | 게임뷰 기사(개발자 사례 소개. '글로벌 핫 이슈' 섹션이라 해외 사례일 수 있음) | LLM 에이전트(모델 미확인), UE 5.8 Unreal MCP, UMG, Niagara | 에이전트가 에디터를 실시간으로 조작하고 화면을 읽음. 이해하기 어려운 머티리얼 수식에 어노테이션을 달아 질문 | "MCP로 현재 상황을 인식하게 된 것이 핵심 개선"이라는 평가 | [전편](https://www.gamevu.co.kr/news/articleView.html?idxno=60827), [후편](https://www.gamevu.co.kr/news/articleView.html?idxno=60830) | 중간 · 검색 요약 |
| Meshy로 모델러 없이 게임 에셋 | 인프런 클립 강사(이름 미확인) | Meshy | 생성 직후 100만 폴리곤 이상 → 리메시로 약 1만 폴리곤 → 엔진 임포트 | 프로토타입 속도에 큰 도움 | [인프런 클립](https://www.inflearn.com/clip/570) | 중간 · 검색 요약 |
| NC AI 바르코 3D로 리니지M 배경 작업 단축 | 엔씨소프트, NC AI(2025~2026) | VARCO 3D(자체 모델), 바르코 스튜디오 | 리니지M 배경 원화팀이 파이프라인에 도입 | 팀 사례는 2~3주 → 약 1주. 제품 홍보는 '3D 애셋 제작 4주 → 3분'. 두 수치는 맥락이 다름. MCP 기반 아님 | [시사저널e](https://www.sisajournal-e.com/news/articleView.html?idxno=417470), [아주경제](https://www.ajunews.com/view/20260714153538647), [NCSOFT](https://about.ncsoft.com/news/article/gameai_01_260424) | 중간(홍보 수치 포함) · 검색 요약 |
| Opus 5.5·Fable 5.1·GPT-5.6 3D 코딩 비교 | AI타임스(2026) | Claude Opus 5.5, Claude Fable 5.1, GPT-5.6 | 같은 프롬프트(물고기 떼, 소용돌이, 폭풍 속의 배, 쓰나미, 관람차·제어실)로 결과 비교 | 카메라 앵글·노을 안개·텍스트 레이아웃 같은 연출 디테일은 Opus 5.5, 비용·속도는 GPT-5.6이 우세. Fable 5.1은 최종 연출의 정교함이 떨어짐. GPT-6 Astra는 비교 대상이 아님 | [AI타임스](https://www.aitimes.com/news/articleView.html?idxno=215618) | 중간(여러 비교가 섞인 요약, 표본 적음) · 검색 요약 |
| 휴대폰 사진 몇 장 → Blender 건물 재구성 | Bad Decisions Studio 사례를 AI매터스가 소개(2026-09) | GPT-6 Astra, Blender | 휴대폰 사진을 참조 이미지로 넣고 모델링 | 30분 이내 완료(작성자 자기 보고). 사진 재구성에서 원본에 없는 요소를 지어내는 문제가 함께 지적됨 | [AI매터스](https://aimatters.co.kr/news-report/51830/) | 중간 · 검색 요약 |

## 4. 유튜브

모두 검색 결과의 영상 제목과 요약으로만 확인했습니다. 채널명과 게시일은 대부분 확인하지 못했습니다.

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| 블렌더(Blender) MCP를 활용해서 3D 모델링 업무 자동화하기 | 미확인 | 미확인(2025~2026 추정) | 블렌더 MCP로 반복 모델링 업무를 자동화하는 과정 | 설치 직후 '업무 자동화' 관점을 잡기 좋음 | [YouTube](https://www.youtube.com/watch?v=UU_iqziC6mE) | 중간 · 검색 요약 |
| Claude가 내 2D 로봇을 3D 모델로 만들었다 \| Blender MCP 완전 자동화 | 미확인 | 미확인 | 2D 로봇 이미지 → 3D 모델 → 웹 랜딩 페이지 적용 | 결과물을 실제 제품에 넣는 과정까지 보여 줌 | [YouTube](https://www.youtube.com/watch?v=I5rtlgAvoV4) | 중간 · 검색 요약. AAA보다는 스타일라이즈드 쪽으로 추정 |
| 클로드 AI 커넥터(MCP)로 스케치업 자동 모델링 + AI 렌더링 하는 법 | 뽁숑이 | 2026 추정 | SketchUp MCP 자동 모델링 → AI 렌더링. 연결 방법 쇼츠 별도 | 건축·인테리어 실무 관점의 한국어 자료는 드묾 | [YouTube](https://www.youtube.com/watch?v=GOaWRhrsQC0), [쇼츠](https://www.youtube.com/shorts/WyzHiIZ1J3I?cbrd=1) | 중간 · 검색 요약. 게임 AAA 파이프라인과는 거리가 있음 |
| GPT 6 x 블렌더 3D = 이제는 바이브 모델링 시대 | 미확인 | 2026-09(Astra 공개 이후) | GPT-6 Astra로 블렌더를 조작하는 '바이브 모델링' | Astra의 Computer Use와 블렌더 조작 능력을 빠르게 훑어볼 수 있음 | [YouTube](https://www.youtube.com/watch?v=_S4SaiNBlRk) | 중간 · 제목만 확인. 과장된 프레이밍일 수 있음 |
| GPT 6 아스트라 x 블렌더 (바이브 모델링 & 애니메이션) | 미확인 | 2026-09 | Astra로 모델링과 애니메이션까지 | 애니메이션 자동화 가능성 확인 | [YouTube](https://www.youtube.com/watch?v=JT9kgRePJ-E) | 중간 · 제목만 확인 |
| Claude Code + Unity MCP 연동하기 | 미확인 | 미확인 | Claude Code와 Unity MCP 서버 연결 튜토리얼 | 설치 과정을 영상으로 따라 할 수 있음 | [YouTube](https://www.youtube.com/watch?v=XauWsKw7nco) | 중간 · 검색 요약. 품질보다 연동 자체에 초점 |
| 클로드 오퍼스5 압도적 성능 + 미친반값효율 (페이블5 완벽대체) | 미확인 | 2026 | Claude Opus 5와 Fable 5의 성능·가격 비교. 3D 전용 아님 | 모델 비용 감각. 단, 이전 세대 비교라 지금은 Opus 5.5($4/$20)와 Fable 5.1($10/$50) 기준으로 다시 봐야 함 | [YouTube](https://www.youtube.com/watch?v=bfyvRM7VcH0) | 낮음 · 제목만 확인 |
| [Blender 3.0+ 초보 강좌] 8강. Texturing - 2 (PBR Texturing, Node Editor) | 미확인 | 2022 전후 | PBR 텍스처 적용과 노드 에디터 | Base Color·Roughness·Normal 연결 기초를 무료로 | [YouTube](https://www.youtube.com/watch?v=rDLb0xizzrU) | 중간 · 검색 요약. 버전이 오래됨 |
| 블렌더 유저라면 꼭 알아야 하는 무료 이미지 & 텍스처 사이트 Poly Haven | 미확인 | 미확인 | Poly Haven(무료 HDRI, 텍스처, 모델) 소개 | MCP for Blender의 Poly Haven 연동과 함께 쓰면 사실적인 HDRI와 PBR 재질을 쉽게 확보 | [YouTube](https://www.youtube.com/watch?v=AqtYMdZqo4g) | 중간 · 검색 요약 |
| 가구·집 모델링 무료 강좌: 쿠션 의자 만들기 1강 / 집 모델링 / 블렌더 기초·3D 재생목록 | 미확인 | 미확인 | 의자·집 모델링과 블렌더 기초 | AI 결과물을 직접 고칠 수 있는 기초 역량 | [의자](https://www.youtube.com/watch?v=19jGvcYle1I), [집](https://www.youtube.com/watch?v=App-xLPworM), [재생목록 1](https://www.youtube.com/playlist?list=PLqf2JB4ViQO4dXIJykSyCM-k5a50eJC_P), [재생목록 2](https://www.youtube.com/playlist?list=PLZMaMcWE_6r8Mo2yhWELYWwx0QZx_a2Lc) | 중간 · 검색 요약 |

## 5. 블로그·가이드

### 5.1 Blender MCP 설치·원리

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| Claude AI와 블렌더 MCP로 3D 모델링 시작하기! 입문자 완전 정복 가이드 | 패스트캠퍼스 미디어(인사이트) | 2025~2026 | MCP 애드온 설치, uv로 통신 환경 구성, Claude Desktop 연결. 활용 분야(건축 시각화, 제품 렌더, 썸네일 소품) | 가장 체계적인 한국어 입문 설치 가이드. "반복적이고 규칙적인 작업에서 효과가 크다"는 실용 조언 | [패스트캠퍼스 미디어](https://media.fastcampus.co.kr/insight/ai_creative/blendermcp/) | 중간 · 검색 요약. 강의 판매용 입문 콘텐츠. 커뮤니티 서버 기준으로 보임(추정) |
| Mac에서 생성형 AI 클로드와 블랜더 MCP로 연결하기 | brunch @soonkyujang | 미확인 | macOS 연결 과정, BlenderMCP 탭의 Start/Connect MCP Server 버튼 | Mac에서 연결이 막혔을 때 | [brunch](https://brunch.co.kr/@soonkyujang/221) | 중간 · 검색 요약. 개인 기록이라 버전 차이 가능 |
| 블렌더 MCP 연결 원리, AI가 3D 게임 에셋 만드는 법 | tali.kr | 2026 추정 | MCP 구조(로컬 Blender 안에서 여는 서버에 AI가 접속)와 게임 에셋 제작 흐름. 며칠 만든 결과물은 인디 프로토타입 수준이라는 한계 | 원리와 한계를 균형 있게 설명. 팀 설명용 | [tali.kr](https://tali.kr/blender-mcp-assets) | 중간 · 검색 요약 |
| 블렌더 MCP 연결 완전 정복: AI가 직접 3D 작업하는 시대 | MKCGI 블로그 | 2026-05 | 크리에이티브 커넥터 이후의 블렌더 MCP 연결 가이드 | 한국어 가이드 중 날짜가 최신 | [MKCGI](https://www.mkcgi.net/2026/05/mcp-ai-3d.html) | 중간 · 검색 요약. 세부 미확인 |
| LLM 인공지능과 BlenderMCP 사용 자연어로 3D 모델 만들기 | IoThingsMaker | 2025 추정 | 자연어 3D 모델링 실습 | 3D 프린팅·메이커 용도 | [IoThingsMaker](https://iothingsmaker.com/llm-%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EA%B3%BC-blendermcp%EC%82%AC%EC%9A%A9-%EC%9E%90%EC%97%B0%EC%96%B4%EB%A1%9C-3d-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0/) | 중간 · 검색 요약. 초기 blender-mcp 기준일 수 있음 |
| MCP로 버튜버 캐릭터 만들기 | velog @w0729 | 미확인 | MCP로 버튜버 캐릭터를 만든 개발 기록 | 캐릭터 제작에 에이전트를 쓴 구체적 시도 | [velog](https://velog.io/@w0729/MCP%EB%A1%9C-%EB%B2%84%ED%8A%9C%EB%B2%84-%EC%BA%90%EB%A6%AD%ED%84%B0-%EB%A7%8C%EB%93%A4%EA%B8%B0) | 낮음 · 검색 요약 |
| GPT-6 Astra 활용 Blender 3D 환경 구현 사례 / 이미지에서 Blender 파일로 / Claude Opus 5.5의 3D 모델링 및 시각화 능력 활용 | promppy | 2026 | Astra로 이미지를 Codex에 올려 Blender 파일로 바꾸는 흐름, Opus 5.5 3D 활용법 | 모델별 프롬프트 예시 수집 | [1](https://www.promppy.com/item/1433678), [2](https://www.promppy.com/item/1563417), [3](https://www.promppy.com/item/1864060) | 낮음 · 큐레이션 요약 사이트라 1차 출처가 아님 |

### 5.2 Unreal·Unity MCP

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| UE5 + Claude Code + MCP 1. 환경 세팅: AI Agent로 언리얼 엔진 연동하기 | velog @miniminichip | 미확인(2025~2026) | Claude Code로 UE5를 제어하는 환경 세팅 시리즈 1편 | 단계별로 따라 하기 좋음 | [velog](https://velog.io/@miniminichip/UE5-Claude-Code-MCP-1) | 중간 · 검색 요약. UE 5.8 공식 플러그인 이전 방식일 수 있음 |
| 언리얼 에디터 안에 들어온 MCP 서버: AI 에이전트가 게임 엔진을 직접 조종하는 시대 | 박재홍의 실리콘밸리(위키독스) | 2026 추정 | UE 5.8 Unreal MCP의 의미 해설 | 업계 맥락을 한국어로 설명할 때 인용 | [위키독스](https://wikidocs.net/blog/@jaehong/20632/) | 중간 · 검색 요약. 실습 없음 |
| 유니티 MCP 서버: 클로드와 함께 AI를 사용하여 유니티 프로젝트 제어하기 | Apidog 한국어 블로그 | 2025 추정 | 에셋 가져오기, 프리팹 인스턴스화·생성, 씬 열기·저장·수정, 게임 오브젝트 조작 | Unity MCP로 할 수 있는 일을 한눈에 | [Apidog](https://apidog.com/kr/blog/unity-mcp-server-kr/) | 중간 · 검색 요약. 벤더 블로그 번역 성격 |
| vscode 클로드코드 확장에서 유니티mcp사용하기 / [Unity] 유니티 mcp 사용하기 / Unity와 AI로만 게임 만들기 (2) | duplicat.kr / kiweb develog / kiweb ai-labs | 미확인(2025~2026) | 에셋스토어의 MCP for Unity 설치 → Python·uv 설치 → 모든 상태가 초록불인지 확인 → Unity·Claude 재시작 → Allow → `/mcp`로 연결 확인 | 실제 설치 체크리스트로 쓰기 좋음 | [duplicat.kr](https://duplicat.kr/1175), [kiweb develog](https://develog.kiweb.or.kr/@user_1777093328305/unity-%EC%9C%A0%EB%8B%88%ED%8B%B0-mcp-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0), [kiweb ai-labs](https://ai-labs.kiweb.or.kr/creative/post/unitywa-airoman-geim-mandeulgi-baibeu-kodingyi-haegsim-gaideu-2-TukBzx1xFLd3A5H) | 중간 · 검색 요약. 대표 구현은 [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)(v10.0.0, 2026-06-30)이지만 글에서 다룬 버전은 미확인 |

### 5.3 MCP 일반·커넥터 해설

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| 클로드 MCP 설치 및 추천 7종 가이드 (2026) / Claude MCP 사용법 완벽 정리 | 골든래빗 / 이랜서 블로그 | 2026 | Claude Code와 Desktop의 MCP 연결, 추천 서버 | 블렌더 외 MCP를 함께 쓰려는 초심자용. 3D 특화 아님 | [골든래빗](https://goldenrabbit.co.kr/articles/ugC8rmSLpFfoJPnnRVUZ), [이랜서](https://www.elancer.co.kr/blog/detail/1123) | 중간 · 검색 요약 |
| 앤트로픽의 새 무기, 클로드 커넥터: 달라진 창작의 방식? | 마소캠퍼스 GEN AI 인사이트 | 2026-04~05 추정 | 크리에이티브 커넥터가 창작 워크플로를 바꾸는 방식 | 비개발 크리에이터에게 커넥터를 설명할 때 | [마소캠퍼스](https://www.masocampus.com/anthropic-claude-connector-creative/) | 중간 · 검색 요약. 실습은 제한적 |

### 5.4 AI 3D 생성 도구

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| Hunyuan3D 소개 / #550 Tencent Hunyuan 3D 사용해보기 / GeekNews 토픽 | 파이토치 한국 사용자 모임 / secondbrush / GeekNews | 2024-11~2025(GeekNews 2025-01-23) | Hunyuan3D(텍스트·이미지·스케치로 3D, 멀티뷰 최대 4장 입력) 소개와 사용기. 웹에서 브라우저 번역을 켜고 쓰는 요령 | 이미지→3D의 멀티뷰 입력 원리 이해 | [파이토치 KR](https://discuss.pytorch.kr/t/hunyuan3d-tencent-3d/5451), [secondbrush](https://blog.secondbrush.co.kr/dailyprompt-550/), [GeekNews](https://news.hada.io/topic?id=18861) | 중간 · 검색 요약. GeekNews 토픽은 제목·내용 미확인. **한국에서는 오픈웨이트 라이선스 범위 밖**(2절) |
| 트리포 3D AI 리뷰: 뛰어난 점과 아쉬운 점 / Tripo·Meshy 리뷰 | see3d.art 한국어 / unite.ai | 2025~2026 | Tripo(Smart Mesh 토폴로지, PBR, Unity·Unreal 원클릭 내보내기)와 Meshy의 장단점 | 생성 도구 비교의 출발점 | [see3d.art](https://see3d.art/ko/blog/detail/Tripo-3D-AI-Review-What-It-s-Great-At-and-Not-b6180d62aa21/), [unite.ai Tripo](https://www.unite.ai/tripo-review/), [unite.ai Meshy](https://www.unite.ai/meshy-ai-review/) | 낮음 · 번역(기계번역 추정)·제휴 콘텐츠일 수 있음 |

### 5.5 AAA 품질 기초 (재질·라이팅·렌더·인테리어·가구)

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| 블렌더 재질·텍스처 완벽 가이드(PBR과 노드 랭글러) / 라이팅 독학 가이드 / F12 렌더가 까맣게 나오는 이유 | 유정통 3D | 2025~2026 추정 | Node Wrangler로 PBR 맵 한 번에 연결, 월드 배경색을 조금 올려 암부 살리기, 렌더가 검게 나올 때 해결 | AI가 만든 씬의 재질·조명 보정 체크리스트. 에이전트 규칙으로 옮기기 좋음 | [PBR](https://yujungtong.com/%EB%B8%94%EB%A0%8C%EB%8D%94-%EC%9E%85%EB%AC%B8%EC%9E%90-%ED%95%84%EB%8F%85-pbr-%ED%85%8D%EC%8A%A4%EC%B2%98-%EC%A0%81%EC%9A%A9-%ED%95%B5%EC%8B%AC/), [라이팅](https://yujungtong.com/blender-lighting-and-color/), [검은 렌더](https://yujungtong.com/blender-rendering-black-screen-fix-guide/) | 중간 · 검색 요약. 입문자 수준 |
| 블렌더 렌더링 설정 마스터하기 / Cycles 렌더링 빠르게 하는 방법 | iRender 한국어 블로그 | 미확인 | 샘플링, 라이트 패스, 컬러 매니지먼트가 조명·그림자·반사에 주는 영향 | 에이전트가 렌더 설정을 잡을 때 기준값 정리 | [설정](https://irendering.net/%EB%B8%94%EB%A0%8C%EB%8D%94-%EB%A0%8C%EB%8D%94%EB%A7%81-%EC%84%A4%EC%A0%95-%EB%A7%88%EC%8A%A4%ED%84%B0%ED%95%98%EA%B8%B0-%EA%B3%A0%ED%92%88%EC%A7%88-%EB%A0%8C%EB%8D%94%EB%A7%81%EC%9D%84-%EB%8D%94/), [Cycles 속도](https://irendering.net/blender-cycles-%EB%A0%8C%EB%8D%94%EB%A7%81-%EB%B9%A0%EB%A5%B4%EA%B2%8C-%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95/) | 중간 · 검색 요약. 렌더팜 업체 마케팅 성격 |
| 인테리어 렌더링 퀄리티를 향상시키는 7가지 필수 팁 | 아키스케치 | 2025 추정 | 인테리어 렌더링 품질 팁 | 인테리어 씬 사실감 체크리스트 | [아키스케치](https://www.archisketch.com/en/blog/67ce4dcab7dabf0012869791) | 낮음 · 검색 요약. URL은 /en/ 경로 |
| 의자 만들기 / 소파 모델링 / Architecture 카테고리 | blender.pe.kr | 미확인 | 의자·소파 같은 가구와 건축 요소 모델링 | 가구의 구조(다리, 프레임, 쿠션)를 에이전트 프롬프트나 검수 기준으로 옮길 때 | [의자](https://blender.pe.kr/870), [소파](https://blender.pe.kr/874), [건축](https://blender.pe.kr/category/Blender/Architecture) | 중간 · 검색 요약. 오래된 버전일 수 있음 |
| 블렌더 기본 라이팅과 렌더링 / 블렌더 알파 텍스처 적용 | 포스타입 @ijuhamnida123 / godhasdone.com | 미확인 | 라이팅 기초, 알파 텍스처(잎사귀·커튼) | 알파 마스크가 필요한 소품 | [포스타입](https://www.postype.com/@ijuhamnida123/post/14722869), [godhasdone](https://www.godhasdone.com/21) | 낮음 · 검색 요약 |
| 스케치업이냐, 라이노냐? 3D 모델링 프로그램에 대해서 | brunch | 미확인 | 건축 실무 관점의 SketchUp과 Rhino 비교("SketchUp으로 되는 건 Rhino로 다 되지만 반대는 아니다") | SketchUp MCP와 Rhino MCP 중 선택할 때 | [brunch](https://brunch.co.kr/@ratm820309n85i/198) | 중간 · 검색 요약. AI는 다루지 않음 |

## 6. 강의·책·공식 문서

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| Red Dot 수상자에게 배우는 AI 3D 모델링 (ft. 블렌더 MCP) | 패스트캠퍼스 | 2026 | 레드닷 수상 디자이너의 블렌더 MCP 기반 AI 3D 모델링 유료 강의(사전예약 뒤 순차 공개) | MCP를 정면으로 다루는 거의 유일한 국내 유료 강의 | [패스트캠퍼스](https://fastcampus.co.kr/dgn_online_reddot) | 중간 · 검색 요약. 가격·커리큘럼·품질 미확인 |
| 3D 캐릭터 아티스트 채디의 블렌더와 AI로 연출하는 매력적인 캐릭터 모델링 | 콜로소 | 미확인 | 블렌더 캐릭터 모델링 + Midjourney 같은 AI 이미지 레퍼런스, 스컬핑, 툰셰이딩 | 'AI 이미지 레퍼런스 + 사람의 고품질 모델링' 하이브리드. MCP는 다루지 않음 | [콜로소](https://coloso.co.kr/products/3ddesign-chedy) | 중간 · 검색 요약 |
| 모델러 없는 개발자가 AI로 3D 에셋 자급자족하는 법 (ft. Meshy) | 인프런 클립 | 미확인 | Meshy 생성 메시 100만 폴리곤 이상 → 리메시 약 1만 폴리곤 | 게임용 폴리곤 수 감각. 구체적 수치 | [인프런](https://www.inflearn.com/clip/570) | 중간 · 검색 요약. 무료 또는 저가(추정) |
| 블렌더 3.0에서 인테리어 디자인 하기 | 인프런 | 2022 전후 | 인테리어 모델링 필수 기능, 애드온, 재질 | AI가 만든 인테리어 씬을 검수·보정할 기초 | [인프런](https://www.inflearn.com/course/%EB%B8%94%EB%A0%8C%EB%8D%94-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4-%EB%94%94%EC%9E%90%EC%9D%B8) | 중간 · 검색 요약. 버전이 오래됨 |
| 블렌더 입문·캐릭터·게임그래픽 강의 모음 | 콜로소 / 클래스101(메이커척, 김렌더, 호야초) / Udemy 한글자막 | 2022~2023 전후 | 블렌더 기초부터 캐릭터·애니메이션 | AI 결과물을 직접 고칠 기본기. AI·MCP는 다루지 않음 | [콜로소 입문](https://coloso.co.kr/products/blender-basiccourse-100refundchallenge202307), [콜로소 게임그래픽](https://coloso.co.kr/products/gamegraphic_blender_class), [클래스101 ①](https://class101.net/en/products/639bfc01fd25ce000fb59ec9), [②](https://class101.net/en/products/62d1aee723c860000e396615), [③](https://class101.net/en/products/645dea176a6491000f917784), [Udemy](https://www.udemy.com/course/blender-tutorial-korean/) | 중간 · 검색 요약 |
| 건축/인테리어 실무에서 쓰이는 스케치업 (모델링/렌더링) | 클래스101 | 미확인 | SketchUp 실무 모델링·렌더링 | SketchUp MCP 결과를 실무 수준으로 다듬는 기초 | [클래스101](https://class101.net/en/products/5f434c3699b841001331f602) | 중간 · 검색 요약 |
| 책 『서브스턴스 디자이너 시작하기』 | 안원철, 비엘북스 | 2018 전후(추정) | Substance Designer로 PBR 타일링 텍스처 10종을 노드로 제작 | 절차적 PBR 원리를 익혀 AI 텍스처를 평가·보정 | [예스24](https://www.yes24.com/product/goods/64372727), [교보문고](http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9791186573266) | 중간 · 검색 요약. 버전이 오래됨 |
| Adobe Substance 3D Painter / Sampler 한국어 튜토리얼 | Adobe(공식) | 상시 | PBR 페인팅, 스캔 기반 머티리얼 제작 | 공식 자료. Adobe 크리에이티브 커넥터와도 연결됨 | [Painter](https://helpx.adobe.com/kr/ko/substance-3d-painter/tutorials.html), [Sampler](https://helpx.adobe.com/kr/ko/substance-3d-sampler/tutorials.html) | 중간 · 검색 요약. AI 워크플로는 다루지 않음 |

## 7. 커뮤니티

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| [클로드 블렌더 커넥터 사용법] 공식 가이드가 불친절해서 만듬 | Threads @dddesign.io | 2026-04 이후 | 공식 커넥터 설치: Claude Desktop 커넥터에서 blender 검색 → Enable → 공식 링크에서 MCP 파일 다운로드 → Blender 창에 드래그(반드시 2번) → Edit > Preferences에서 확인 | 공식 문서에 없는 실전 팁('2번 드래그', 독립 검증은 못 함) | [Threads](https://www.threads.com/@dddesign.io/post/DXsWAspka7F/%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%B8%94%EB%A0%8C%EB%93%9C-%EC%BB%A4%ED%85%8D%ED%84%B0-%EC%82%AC%EC%9A%A9%EB%B2%95%EA%B3%B5%EC%8B%9D-%EA%B0%80%EC%9D%B4%EB%93%9C%EA%B0%80-%EB%B6%88%EC%B9%9C%EC%A0%88%ED%95%B4%EC%84%9C-%EB%A7%8C%EB%93%AC1-claude-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%B8%ED%8C%85-%EC%BB%A4%EB%84%A5%ED%84%B0-%EC%9D%B4%EB%8F%992-blender-%EA%B2%80%EC%83%89-%EC%84%A0%ED%83%9D3-enbaled-%EB%88%84?hl=ko) | 중간 · 검색 요약. SNS라 버전마다 달라질 수 있음 |
| AI로 모델링 이젠 수준급 바이브모델링 10분도 안걸려 / 이젠 AI에이전트의 시대 클로드를 자비스로 만들고 있어요 / Astra(GPT-6)로 만든 결과물 | 클리앙 모두의공원 | 2026(Astra 글은 2026-09) | 바이브 모델링 체험(10분 이내), Claude 에이전트 구성 경험, GPT-6 Astra 결과물 | 한국 사용자의 체감 품질과 댓글의 비판적 의견 | [①](https://www.clien.net/service/board/park/19015735), [②](https://www.clien.net/service/board/park/19037225), [③](https://www.clien.net/service/board/park/19258409) | 중간 · 검색 요약. 본문 미확인, 일화적(개인 테스트, n=1) |
| 이제는 바이브 모델링 시대? / Unreal-MCP 등장 / Unity3D MCP로 클로드 코드 붙여서 게임 만들기 | Threads @choi.openai / @unclejobs.ai / @secret_canada_ | 2025~2026 | blender-mcp 초기 바이럴, 커뮤니티판 Unreal-MCP 소개, mcp-unity와 Claude Code로 30분 만에 드리프트 게임 | 국내 확산 흐름과 빠른 체험담 | [@choi.openai](https://www.threads.com/@choi.openai/post/DHFQXYoPAoo), [@unclejobs.ai](https://www.threads.com/@unclejobs.ai/post/DH2Sok7JBzf/video-%EC%99%80-%EC%9D%B4%EA%B2%8C-%EB%90%98%EB%84%A4%EC%9A%94%EC%9D%B4%EC%A0%9C-%EC%96%B8%EB%A6%AC%EC%96%BC-%EC%97%94%EC%A7%84%EB%8F%84-mcp%EB%A1%9C-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%A0-%EC%88%98-%EC%9E%88%EA%B2%8C-%EB%90%90%EC%8A%B5%EB%8B%88%EB%8B%A4x%EC%9D%98-%EC%9C%A0%EC%A0%80%EA%B0%80-%EC%A7%81%EC%A0%91-%EB%A7%8C%EB%93%A0-unreal-mcp%EA%B0%80-%EB%93%B1%EC%9E%A5%ED%96%88%EC%8A%B5%EB%8B%88%EB%8B%A4%EC%9D%B4%EC%A0%9C-3d-%EA%B2%8C%EC%9E%84%EB%8F%84-%EB%B0%94?hl=ko), [@secret_canada_](https://www.threads.com/@secret_canada_/post/DTCjtmzjJPD/video-%EC%9D%B4%EC%A0%A0-unity3d-mcp-%EB%A1%9C-%ED%81%B4%EB%A1%9C%EB%93%9C-%EC%BD%94%EB%93%9C-%EB%B6%99%EC%97%AC%EC%84%9C-%EA%B2%8C%EC%9E%84%EB%A7%8C%EB%93%9C%EB%8A%94%EA%B2%8C%EA%B0%80%EB%8A%A5%ED%95%B4%EC%A7%90-%EC%98%A4%EB%8A%98-%EC%B2%98%EC%9D%8C-30%EB%B6%84-%EC%A0%95%EB%8F%84-%EC%9B%8C%EB%B0%8D%EC%97%85-%EC%9C%BC%EB%A1%9C-%EB%93%9C%EB%A6%AC%ED%94%84%ED%8A%B8-%EA%B2%8C%EC%9E%84-%EC%9D%84-%EB%A7%8C%EB%93%A4%EC%96%B4-%EB%B3%B4%EA%B3%A0%EC%8B%B6%EC%96%B4%EC%84%9C-%EB%AC%B4?hl=ko) | 중간 · 검색 요약. 깊이가 얕고 과장이 섞일 수 있음 |
| 스케치업이 자동으로 모델링 해준다? 한줄이면? (MCP+클로드 AI 연동 실험) | 긱톡 | 2026 추정 | SketchUp MCP와 Claude 연동 실험 | 건축 모델링 자동화가 어디까지 되는지 | [긱톡](https://www.gigtalk.co.kr/post/719891) | 낮음 · 검색 요약 |
| 블렌더 첫 공간 모델링 후기 / 두 번째 모델링 후기 | 디시인사이드 블렌더 마이너 갤러리 | 미확인 | 입문자의 공간(인테리어) 모델링 후기와 갤러리 이용자 피드백 | 사람이 공간 모델링에서 하는 실수를 AI 결과물 검수 기준으로 옮기기 | [①](https://gall.dcinside.com/mgallery/board/view/?id=blender&no=42368), [모바일](https://m.dcinside.com/board/blender/42368), [②](https://gall.dcinside.com/mgallery/board/view/?id=blender&no=43908) | 낮음 · 검색 요약. AI와 무관 |
| 크래프톤·NC·클로드… 게임 제작 AI 원톱은? / Blender 강의 추천 스레드 | 디시 게임와이 갤러리 / 침하하 | 2026 추정 | 게임 제작 AI 비교 게시글, 블렌더 강의 추천 | 커뮤니티 여론과 추천 강의 | [디시](https://gall.dcinside.com/board/view/?id=gamey&no=14768), [침하하](https://chimhaha.net/recommend_comics/435126) | 낮음 · 검색 요약 |

## 8. 뉴스

| 제목 | 작성자/채널 | 날짜 | 다루는 내용 | 왜 유용한가 | 링크 | 신뢰도 |
|---|---|---|---|---|---|---|
| 앤트로픽 크리에이티브 커넥터 9종 보도 | AI매터스, AI타임스, 디지털인사이트, 월간디자인, 디자인DB, KITPA, 디지털포커스 | 2026-04-28~05 | 2026-04-28 출시된 Claude 크리에이티브 커넥터 9종. 블렌더 커넥터로 씬 전체 분석, 커스텀 스크립트 작성, 인터페이스에 새 도구 추가. 한국어 보도에는 'Adobe 50개 이상 앱 지원'으로 나오지만, 발표 원문은 Creative Cloud 여러 앱에 걸친 '도구 50개 이상'이고 현재 커넥터 도구는 67개입니다([기타 DCC·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md)) | 출시일과 지원 범위를 한국어로 인용할 때 | [AI매터스 ①](https://aimatters.co.kr/news-report/41239/), [②](https://aimatters.co.kr/news-report/41315/), [AI타임스](https://www.aitimes.com/news/articleView.html?idxno=209904), [디지털인사이트](https://ditoday.com/%ED%81%B4%EB%A1%9C%EB%93%9C%EC%97%90%EC%84%9C-%ED%8F%AC%ED%86%A0%EC%83%B5-%EC%93%B4%EB%8B%A4-%EC%95%A4%ED%8A%B8%EB%A1%9C%ED%94%BD-%ED%81%AC%EB%A6%AC%EC%97%90%EC%9D%B4%ED%8B%B0%EB%B8%8C-%EC%86%8C/), [월간디자인](https://design.co.kr/article/163859/), [KITPA](https://kitpa.org/news/1460), [디지털포커스](https://www.digitalfocus.news/news/articleView.html?idxno=20533) | 높음(출시일과 9종 구성이 여러 매체에서 일치) · 검색 요약. 대부분 보도자료 수준 |
| GPT-6 아스트라 활용법 총정리, 50분 만에 유튜브 영상부터 5일짜리 도시 게임까지 | 다나와 DPG | 2026-09 | GPT-6 Astra(9월 3일 공개)의 Computer Use와 블렌더 3D 사례: 집 사진에서 편집 가능한 3D 씬, 그림에서 대량 오브젝트 생성, 렌더를 보고 스스로 수정, Unreal·Unity·CAD 내보내기 | Astra 3D 사례를 한국어로 빠르게 파악 | [다나와 DPG](https://dpg.danawa.com/news/view?boardSeq=60&listSeq=6058609) | 중간 · 검색 요약. 사례 수치는 개별 사용자 주장 |
| GPT-6 아스트라 vs 클로드 페이블 5.1, 성능표만 보면 놓치는 차이 | AI매터스 | 2026-09 | 컴퓨터 사용 성공률의 의미, 사진 재구성 시 환각 문제 | 벤치마크 수치를 실제 3D 작업으로 옮겨 읽는 법 | [AI매터스](https://aimatters.co.kr/news-report/51830/) | 중간 · 검색 요약 |
| 3D 코딩 대결... 클로드 오퍼스 5.5 "디테일" vs GPT-5.6 "비용·속도" / 클로드 오퍼스 5.5 공개(가격 40% 인하) | AI타임스 | 2026(Opus 5.5 출시 2026-09-22 전후) | Opus 5.5의 3D 생성 능력 비교(3.4절 표 참고), Opus 5.5 출시와 가격. '40% 인하'는 기사 제목 표현이고, Anthropic 발표는 'Opus 5 대비 일반 작업 비용 40% 절감'(단가 입력/출력 $4/$20 per 1M) | 모델별 3D 강약점을 한국어로 인용 | [비교](https://www.aitimes.com/news/articleView.html?idxno=215618), [출시](https://www.aitimes.com/news/articleView.html?idxno=215583) | 중간 · 검색 요약. 세부는 원문 확인 필요 |
| '제미나이'에 인터랙티브 3D 모델·시뮬레이션 생성 기능 추가 / 제미나이3 활용법: 게임·3D·웹앱 제작 사례 13가지 + 실전 프롬프트 | AI타임스 / AI매터스 | 2025-11~2026 | Gemini 앱의 인터랙티브 3D·시뮬레이션 생성(Pro 모델에서 '시각화해 줘'), Gemini 3 게임·3D 사례 | Gemini를 다룬 드문 한국어 3D 자료. 블렌더 MCP 연동은 없음 | [AI타임스](https://www.aitimes.com/news/articleView.html?idxno=209099), [AI매터스](https://aimatters.co.kr/ai-tool/ai-tool-how-to/34188/) | 중간 · 검색 요약 |
| 언리얼 엔진을 직접 다루는 AI, UE5.8 MCP 활용 게임 개발기 [전편]·[후편] | 게임뷰 | 2026 추정 | UE 5.8 MCP로 에이전트가 에디터를 실시간 조작한 개발기. UMG, 나이아가라, 월드 비주얼, 에디터 어노테이션 활용 | 언리얼 MCP 실전 사례와 한계(3.4절 표 참고) | [전편](https://www.gamevu.co.kr/news/articleView.html?idxno=60827), [후편](https://www.gamevu.co.kr/news/articleView.html?idxno=60830) | 중간 · 검색 요약. 해외 사례 소개일 수 있음 |
| 텐센트 '훈위안 3D' 글로벌 출시 | 캐드앤그래픽스, GTT코리아, 한국클라우드신문, 글로벌이코노믹 | 2025(글로벌이코노믹 2025-07-28) | 훈위안 3D 글로벌 버전(텍스트·이미지·스케치 → 3D), '3D 월드' 생성 확장 | AI 3D 생성 동향 인용 | [캐드앤그래픽스](https://www.cadgraphics.co.kr/newsview.php?pages=news&sub=new01&catecode=2&num=77635), [GTT코리아](https://www.gttkorea.com/news/articleView.html?idxno=22862), [한국클라우드신문](https://www.kcloudnews.co.kr/news/articleView.html?idxno=15709), [글로벌이코노믹](https://www.g-enews.com/article/ICT/2025/07/202507280826165223c5fa75ef86_1) | 중간 · 검색 요약. 보도자료 성격. **오픈웨이트는 한국에서 라이선스 범위 밖**, 호스팅 서비스 약관은 미확인 |
| NC AI '바르코 3D'와 국내 게임사 AI 활용 | 시사저널e, 아주경제, 게임플, 다음, NCSOFT 공식 블로그 | 2025-12~2026-07 | 바르코 3D('4주→3분'), 리니지M 배경 작업 단축, NC·크래프톤·넥슨의 AI 현황, 3D 모델링 자동화로 경쟁 축이 '내러티브'로 옮겨 간다는 분석 | 국내 기업 사례와 산업 맥락 | [시사저널e](https://www.sisajournal-e.com/news/articleView.html?idxno=417470), [아주경제](https://www.ajunews.com/view/20260714153538647), [게임플](https://www.gameple.co.kr/news/articleView.html?idxno=209527), [다음](https://v.daum.net/v/20251207161025106), [NCSOFT](https://about.ncsoft.com/news/article/gameai_01_260424) | 중간 · 검색 요약. 홍보성 수치이고 MCP 기반 아님 |

## 9. 한국어 자료에서 뽑은 노하우 (보완·주의 포함)

한국어 자료에 나온 팁을 모으고, 다른 조사 결과로 보완하거나 주의점을 붙였습니다.

| # | 노하우 | 한국어 근거 | 보완·주의 |
|---|---|---|---|
| 1 | 공식 Claude 블렌더 커넥터는 설치 링크를 Blender 창에 **두 번** 드래그하고, Edit > Preferences에서 활성화됐는지 확인합니다(**미검증** 팁) | [Threads @dddesign.io](https://www.threads.com/@dddesign.io/post/DXsWAspka7F/%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%B8%94%EB%A0%8C%EB%93%9C-%EC%BB%A4%ED%85%8D%ED%84%B0-%EC%82%AC%EC%9A%A9%EB%B2%95%EA%B3%B5%EC%8B%9D-%EA%B0%80%EC%9D%B4%EB%93%9C%EA%B0%80-%EB%B6%88%EC%B9%9C%EC%A0%88%ED%95%B4%EC%84%9C-%EB%A7%8C%EB%93%AC1-claude-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%B8%ED%8C%85-%EC%BB%A4%EB%84%A5%ED%84%B0-%EC%9D%B4%EB%8F%992-blender-%EA%B2%80%EC%83%89-%EC%84%A0%ED%83%9D3-enbaled-%EB%88%84?hl=ko) | blender.org 공식 설치 페이지의 검색 요약에도 '1회차에 Lab 확장 저장소 추가, 2회차에 애드온 설치'로 나오지만, 원문이 차단돼 독립 검증에서 확인하지 못했습니다. 반대로 드래그 설치와 수동 설치를 둘 다 하면 같은 애드온이 두 번 설치된다는 경고(stefancrm 설정 키트)가 있으니 한 경로만 씁니다. 애드온은 Blender 5.1.0 이상이고, Allow Online Access를 켜야 시작된다는 보고가 있습니다 → [Blender MCP](../02_guides/02_blender_mcp.md) 4절 |
| 2 | 커뮤니티 blender-mcp는 로컬 Blender, uv 준비 후 BlenderMCP 탭에서 Start/Connect MCP Server를 누르고, 버튼이 Disconnect로 바뀌면 연결된 것입니다 | [brunch](https://brunch.co.kr/@soonkyujang/221), [패스트캠퍼스 미디어](https://media.fastcampus.co.kr/insight/ai_creative/blendermcp/), [tali.kr](https://tali.kr/blender-mcp-assets) | 현재 이름은 MCP for Blender(PyPI `mcp-for-blender` 2.1.0, 2026-09-25). `uvx blender-mcp`는 호환 래퍼로 같은 커뮤니티 서버를 실행합니다. 텔레메트리 기본 ON(`DISABLE_TELEMETRY=true`), 공식 커넥터와 동시 실행 금지(9876) |
| 3 | MCP 자동화는 반복적이고 규칙적인 작업(건축 시각화, 제품 렌더, 썸네일 소품, 에셋 배치)부터 쓰고, 히어로 에셋은 사람이 마무리합니다 | [패스트캠퍼스 미디어](https://media.fastcampus.co.kr/insight/ai_creative/blendermcp/), [tali.kr](https://tali.kr/blender-mcp-assets), [클리앙](https://www.clien.net/service/board/park/19015735) | 영어권 결론(AI는 감독이 필요한 협업자)과 같습니다 → [AAA 플레이북](../03_playbooks/02_aaa_production_playbook.md) |
| 4 | 생성형 3D 결과물은 반드시 리메시·리토폴로지를 거칩니다(Meshy 100만 폴리곤 이상 → 약 1만) | [인프런 클립](https://www.inflearn.com/clip/570) | 스케일·축도 확인합니다. 영어권 사례에서는 FBX가 100배로 들어오는 문제(Unity 2 m 로봇이 200 m)가 반복됐고, 이미지→3D 결과가 작게 들어온다는 보고(TRELLIS "just small", 조사 요약에는 약 1.4 m·Y-up)도 있습니다. 임포트 직후 bounds로 실측하고, Blender에서 FBX로 내보낼 때는 `apply_scale_options='FBX_SCALE_UNITS'`를 줍니다 → [AI 3D 생성](../02_guides/04_ai_3d_generation.md) 7절 |
| 5 | UE 5.8 MCP는 에디터에 어노테이션(코멘트)을 달아 두고, 에이전트에게 현재 화면을 보고 다음 할 일을 묻는 식으로 씁니다 | [게임뷰 전편](https://www.gamevu.co.kr/news/articleView.html?idxno=60827), [후편](https://www.gamevu.co.kr/news/articleView.html?idxno=60830) | Epic 공식 Unreal MCP는 **실험적** 플러그인입니다. 기본 주소는 `http://127.0.0.1:8000/mcp`, AllToolsets가 필요합니다. [한 해외 사례](https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/AGENTIC-GAMEDEV-GUIDE.md)는 서버가 자동으로 뜨지 않았고(bAutoStartServer=false), 8000 포트 충돌로 8123으로 바꿨으며, AllToolsets와 PythonScriptPlugin을 켜야 했다고 기록했습니다 → [기타 DCC·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md) |
| 6 | Blender와 Unreal을 함께 쓰는 파이프라인은 중앙 MCP 허브 하나에 도구별 플러그인을 포트를 나눠 붙입니다 | [tahooki 설계 문서](https://github.com/tahooki/unreal-blender-mcp/blob/main/Project-document.md) | 8300/8400/8500을 씁니다. 다른 Blender MCP(9876)와는 포트가 겹치지 않지만, 한 Blender에 여러 애드온을 켜면 무엇이 명령을 받는지 헷갈리니 하나만 켭니다 |
| 7 | 렌더 → 스크린샷 → 수정 루프는 Blender를 띄워 둔 채 소켓으로 명령을 보내는 방식이 명령마다 Blender를 실행하는 방식보다 훨씬 빠릅니다 | [Aryeon0228/BlenderMCP](https://github.com/Aryeon0228/BlenderMCP) | 저자 주장(0.1~1초 대 10~15초). 검토용 4방향 렌더는 이 저장소의 `review_views.py`를 쓰면 됩니다 → [보조 스크립트](../03_playbooks/scripts/README.md) |
| 8 | PBR 맵은 Node Wrangler 자동 연결로 한 번에 연결하고, 무료 HDRI와 텍스처는 Poly Haven에서 가져옵니다 | [유정통 3D](https://yujungtong.com/%EB%B8%94%EB%A0%8C%EB%8D%94-%EC%9E%85%EB%AC%B8%EC%9E%90-%ED%95%84%EB%8F%85-pbr-%ED%85%8D%EC%8A%A4%EC%B2%98-%EC%A0%81%EC%9A%A9-%ED%95%B5%EC%8B%AC/), [Poly Haven 소개 영상](https://www.youtube.com/watch?v=AqtYMdZqo4g) | 에이전트가 코드로 연결할 때는 Normal·Roughness 맵의 색공간을 Non-Color로 두는지 확인합니다. MCP for Blender의 Poly Haven 연동은 무료 기능입니다 → [텍스처링](../02_guides/05_texturing_materials.md) |
| 9 | 인테리어 씬은 월드 배경색이나 HDRI 강도를 조금 올려 암부에 기초광을 두고, 샘플링·라이트 패스·컬러 매니지먼트를 함께 맞춥니다 | [유정통 라이팅](https://yujungtong.com/blender-lighting-and-color/), [iRender](https://irendering.net/%EB%B8%94%EB%A0%8C%EB%8D%94-%EB%A0%8C%EB%8D%94%EB%A7%81-%EC%84%A4%EC%A0%95-%EB%A7%88%EC%8A%A4%ED%84%B0%ED%95%98%EA%B8%B0-%EA%B3%A0%ED%92%88%EC%A7%88-%EB%A0%8C%EB%8D%94%EB%A7%81%EC%9D%84-%EB%8D%94/), [아키스케치](https://www.archisketch.com/en/blog/67ce4dcab7dabf0012869791) | 수치 기준과 색관리는 [라이팅·렌더](../02_guides/06_lighting_rendering_art_direction.md) 문서를 따릅니다 |
| 10 | Unity MCP는 Python과 uv 설치 → MCP for Unity 창에서 모든 상태가 초록불인지 확인 → Unity와 Claude 재시작 → Allow → `/mcp`로 연결 확인 순서로 합니다 | [duplicat.kr](https://duplicat.kr/1175), [kiweb develog](https://develog.kiweb.or.kr/@user_1777093328305/unity-%EC%9C%A0%EB%8B%88%ED%8B%B0-mcp-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0), [Apidog](https://apidog.com/kr/blog/unity-mcp-server-kr/) | 설치 실패의 흔한 원인은 의존성 누락과 재시작 누락입니다 |
| 11 | 이미지로 3D를 만들 때는 단일 이미지보다 멀티뷰 이미지를 넣습니다(Hunyuan3D 최대 4장) | [캐드앤그래픽스](https://www.cadgraphics.co.kr/newsview.php?pages=news&sub=new01&catecode=2&num=77635), [GTT코리아](https://www.gttkorea.com/news/articleView.html?idxno=22862) | **Hunyuan3D 오픈웨이트는 한국에서 쓰지 마세요**(2절). 멀티뷰 원칙은 다른 도구에도 그대로 통합니다 → [AI 3D 생성](../02_guides/04_ai_3d_generation.md) 5절 |
| 12 | GPT-6 Astra로 컨셉을 3D로 옮길 때는 이미지를 먼저 준비해 Codex에 올리고 'Blender 파일로 변환'을 지시하는 2단계로 합니다 | [다나와 DPG](https://dpg.danawa.com/news/view?boardSeq=60&listSeq=6058609), [promppy](https://www.promppy.com/item/1563417) | Codex의 Astra 기본 reasoning effort는 low입니다(단계 low/medium/high/xhigh/max/ultra). 품질을 비교하거나 최종 작업을 할 때는 effort를 명시합니다 → [AI 모델 선택](../02_guides/01_ai_models_and_clients.md) |

## 10. 한국어 자료가 비어 있는 곳

| 빈 곳 | 대신 볼 곳 |
|---|---|
| AI로 가구를 배치하거나 레이아웃 타당성을 검사하는 한국어 자료가 거의 없음 | [배치 가이드](../02_guides/08_scene_layout_placement.md), `placement_utils.py`·`scene_audit.py`(가구 배치·관통), `building_audit.py`(문·창·방 연결이 상식적인지, 백룸처럼 기묘한지)([보조 스크립트](../03_playbooks/scripts/README.md)) |
| 리토폴로지·UV·텍스처 베이크 자동화를 다룬 한국어 자료가 거의 없음. 기존 한국어 기초 자료는 대부분 입문자용이고 AI를 다루지 않음 | [텍스처링](../02_guides/05_texturing_materials.md), [사례 모음](./01_case_studies.md)(UV 재베이크 프롬프트) |
| Claude Fable 5.1, Sonnet 5, Gemini를 블렌더·언리얼 MCP와 함께 쓴 한국어 실전 글이 드묾. 모델 비교 기사(AI타임스)와 Gemini 앱 3D 기사 정도만 있음 | [AI 모델 선택](../02_guides/01_ai_models_and_clients.md) |
| 언리얼·유니티 MCP 전용 한국어 유료 강의는 확인하지 못함. 블렌더 MCP도 패스트캠퍼스 1개뿐 | [기타 DCC·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md), [빠른 시작](../03_playbooks/01_quickstart_setup.md) |
| MCP나 에이전트로 3D 파이프라인을 운영한다고 공개한 국내 게임사(NC, 크래프톤, 넥슨) 사례 없음 | [사례 모음](./01_case_studies.md) |
| Meshy, Tripo, Rodin(Hyper3D) 한국어 후기는 번역·제휴 콘텐츠가 많고, 국내 실무자의 독립 비교는 부족 | [AI 3D 생성](../02_guides/04_ai_3d_generation.md) |
| GeekNews에서는 블렌더 MCP 글을 찾지 못함(Hunyuan3D 추정 토픽 1건). 네이버 블렌더 카페, 네이버 블로그, 디스콰이엇, 요즘IT는 미국 기반 검색에 거의 잡히지 않음 | 국내 검색 엔진으로 별도 조사 필요 → [인수인계](../05_handoff/status_and_next_steps.md) |
| 패스트캠퍼스 강의 커리큘럼·가격, 클리앙 본문, 게임뷰 기사 세부는 검색 한도로 교차 확인하지 못함 | 원문을 직접 확인 |

## 흔한 실수와 해결

| 실수 | 증상 | 해결 |
|---|---|---|
| 여러 한국어 가이드를 섞어 따라 함(공식 커넥터와 커뮤니티 서버를 같이 설치) | 연결 실패, 어느 서버가 응답하는지 불분명 | 둘 다 `localhost:9876`을 씁니다. 하나만 고르세요 → [빠른 시작](../03_playbooks/01_quickstart_setup.md) |
| 공식 커넥터 애드온이 설치되지 않거나 서버가 시작되지 않음 | Preferences에 애드온이 보이지 않거나, 커넥터는 켜졌는데 도구가 응답하지 않음 | Blender 5.1.0 이상인지, Edit > Preferences에서 Allow Online Access가 켜져 있는지 확인합니다. 드래그 설치가 안 되면 한 번 더 드래그해 봅니다(후기 기준 팁). 드래그 설치와 수동 설치를 섞어 중복 설치하지 않습니다 → [빠른 시작](../03_playbooks/01_quickstart_setup.md) |
| 한국어 UI Blender에서 에이전트가 쓴 재질 코드가 실패 | `nodes['Principled BSDF']`가 None이거나 KeyError | 노드를 type으로 찾게 하고, 영어 UI를 쓰거나 New Data 번역을 끕니다 → [Blender MCP](../02_guides/02_blender_mcp.md) 12절 |
| 오브젝트 이름을 한글로 지음(예: '의자', '거실 바닥') | `scene_audit.py` 치수 검사(영어 키워드 기준)가 적용되지 않음 | 가구는 영어 이름(`chair_01`, `dining_table`)을 쓰게 합니다. 방·문·창은 `building_audit.py`가 **끝 단어 기준으로 한국어·중국어도 인식**합니다(`거실_바닥`, `현관문`, `거실_창문`; `창가_소파`는 소파로 봄). 애매하면 `obj["role"]`을 넣습니다 → [보조 스크립트](../03_playbooks/scripts/README.md) |
| MCP for Blender의 Hunyuan3D 연동을 그대로 사용 | 출력물이 라이선스 범위 밖 | 연동을 끄고 약관을 확인한 다른 생성 도구를 씁니다 → [AI 3D 생성](../02_guides/04_ai_3d_generation.md) |
| Blender 3.0 시절 한국어 강좌 코드를 에이전트에게 그대로 줌 | 5.x에서 경고나 오류(`use_nodes` 폐기 예고, EEVEE 식별자 변경) | Blender 버전을 프롬프트에 명시하고 API 함정 표를 확인합니다 → [Blender MCP](../02_guides/02_blender_mcp.md) 11절 |
| 헤드라인 수치('10분', '50분', '4주→3분')를 기대치로 삼음 | 실제로는 수정 반복이 수십 번 필요 | 개인·홍보 주장입니다. 영어권의 정직한 기록(10시간·21회 수정, 리뷰어 점수 6~7/10)을 기준으로 일정을 잡습니다 → [사례 모음](./01_case_studies.md) |
| '킹 침대', '표준 문'처럼 이름으로 지시 | 지역마다 크기가 달라 비율이 어색함 | mm 값으로 지정합니다(한국 K 1600 대 미국 King 1930) → [치수 기준표](../03_playbooks/05_reference_dimensions.md) |
| 한국 아파트를 미국식 천장고로 만듦 | 공간이 한국 집처럼 보이지 않고, 키 큰 가구가 천장을 뚫음 | 구축 2300, 신축 2400~2500 mm로 둡니다. `scene_audit.audit_scene(ceiling_z=2.30)`으로 천장을 뚫는 가구(예: 높이 236 cm 옷장)를 잡습니다 |
| 유튜브 '바이브 모델링' 결과를 모델 비교 근거로 삼음 | effort 설정이 달라 비교가 왜곡됨 | Astra는 Codex 기본 effort가 low이고, Opus 5.5는 기본 medium입니다. 비교할 때는 effort와 하네스를 맞춥니다 → [AI 모델 선택](../02_guides/01_ai_models_and_clients.md) |
| 생성형 3D 메시를 그대로 엔진에 넣음 | 100만 폴리곤 이상, 스케일·축 오류 | 리메시·리토폴로지 후 bounds로 실측합니다 → [AI 3D 생성](../02_guides/04_ai_3d_generation.md) 7절 |

## 관련 문서

- [목적·요구사항·범위](../00_purpose/purpose_and_scope.md)
- [조사 방법·한계·신뢰도 정책](../01_research/research_method.md): 한국어 도메인 차단 등 조사 환경의 한계
- [출처 카탈로그](../01_research/sources_catalog.md), [교차검증 로그](../01_research/verification_log.md)
- [사례 모음](./01_case_studies.md): 영어권·일본·중국 사례와 교훈
- [AI 모델 비교·선택](../02_guides/01_ai_models_and_clients.md)
- [Blender MCP 생태계](../02_guides/02_blender_mcp.md): 12절 한국어 UI 현지화
- [기타 DCC·CAD·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md)
- [AI 3D 생성](../02_guides/04_ai_3d_generation.md): Hunyuan 계열 한국 제외
- [텍스처링·재질](../02_guides/05_texturing_materials.md)
- [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md)
- [오브젝트·가구·조형 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md)
- [배치·레이아웃](../02_guides/08_scene_layout_placement.md)
- [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md)
- [에셋·파이프라인·라이선스](../02_guides/10_assets_pipeline_licensing.md): 한국 라이선스·인공지능기본법
- [빠른 시작](../03_playbooks/01_quickstart_setup.md)
- [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md)
- [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md): 한국/미국/유럽
- [보조 스크립트](../03_playbooks/scripts/README.md): `scene_audit.py`, `placement_utils.py`, `review_views.py`, `building_audit.py`(Blender 4.2.23 LTS·5.0.1 테스트 통과)
- [진행 상태·다음 작업](../05_handoff/status_and_next_steps.md)

## 원자료

- [`01_research/raw/G2_korean_resources.gap.json`](../01_research/raw/G2_korean_resources.gap.json): 한국어 자료 보완 조사(이 문서의 주 원자료. 별도 검증 파일 없음)
- [`01_research/raw/11_case-studies.research.json`](../01_research/raw/11_case-studies.research.json): octopus7, openerai 사례와 UE 5.8 MCP 설정 함정
- [`01_research/raw/11_case-studies.verify.json`](../01_research/raw/11_case-studies.verify.json): octopus7·openerai 정정(한국 사례 여부 추정, 원출처 Higgsfield, 라이선스), Hunyuan3D 한국 제외 누락 지적
- [`01_research/raw/G1_dimensions.gap.json`](../01_research/raw/G1_dimensions.gap.json), [`G1_dimensions.verify.json`](../01_research/raw/G1_dimensions.verify.json): 한국 주거·가구 치수와 정정(계단참 2 m, 매트리스 K/LK 브랜드 차이, 신축 천장고, 문틀 기준)
- [`01_research/raw/G4_licensing_pricing.gap.json`](../01_research/raw/G4_licensing_pricing.gap.json), [`G4_licensing_pricing.verify.json`](../01_research/raw/G4_licensing_pricing.verify.json): Hunyuan3D 라이선스, TRELLIS.2 의존성, 인공지능기본법, 저작권 등록 안내서
- [`01_research/raw/10_agent-workflow.research.json`](../01_research/raw/10_agent-workflow.research.json), [`10_agent-workflow.verify.json`](../01_research/raw/10_agent-workflow.verify.json): 현지화 UI 노드 이름 문제, `use_translate_new_dataname` 확인
- [`01_research/raw/01_ai-models.research.json`](../01_research/raw/01_ai-models.research.json): AI매터스 Astra 대 Fable 5.1 기사, 사진 재구성 사례
- [`01_research/raw/04_engine-mcp.research.json`](../01_research/raw/04_engine-mcp.research.json): CoplayDev/unity-mcp, CoderGamester/mcp-unity
- [`01_research/raw/02_blender-mcp.verify.json`](../01_research/raw/02_blender-mcp.verify.json): 공식 애드온 manifest(`blender_version_min` 5.1.0), '2번 드래그' 미검증, Allow Online Access, `blender-mcp` 2.0.0 호환 래퍼. [`03_dcc-cad-mcp.verify.json`](../01_research/raw/03_dcc-cad-mcp.verify.json): Adobe 커넥터 도구 수(발표 50+ → 현재 67). [`G6_benchmarks_models.gap.json`](../01_research/raw/G6_benchmarks_models.gap.json): Opus 5.5 단가와 'Opus 5 대비 40% 절감' 문구

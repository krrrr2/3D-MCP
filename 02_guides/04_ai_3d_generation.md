# AI 3D 생성 가이드: Text/Image-to-3D · 파트 생성 · 월드 생성

> 기준일: 2026-09-27 · 생성 모델은 "형태 초안 공장"입니다. 좋은 레퍼런스 이미지 → 치수 제약을 건 생성 → 파트 분리 → 리토폴로지·UV·베이크·LOD → 검증까지 거쳐야 쓸 수 있는 에셋이 되고, 한국 사용자는 모델 라이선스부터 확인해야 합니다.

> [!WARNING]
> **한국 사용자 라이선스 경고: 가장 먼저 확인하세요**
>
> - **Tencent Hunyuan 계열 오픈웨이트는 한국에서 쓸 수 없습니다.** Hunyuan3D 2.0(2mv·2mini·Turbo 포함), 2.1, Omni, Part, HunyuanWorld 1.0, HY-World 2.0, HY-Motion 1.0(다른 조사 기준으로 BPT도 포함)의 Community License는 모두 적용 지역(Territory)을 "EU·영국·대한민국을 제외한 전 세계"로 정의합니다. 2.0·2.1 라이선스는 머리말에 아예 "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"라고 적어 두었습니다. **모델만이 아니라 출력물(Output)도** Territory 밖에서 사용·복제·수정·배포·전시하면 안 됩니다(5(c)항). Output 정의에 "Hosted Service를 통한 것"이 들어 있으므로, **제3자가 호스팅한 2.x 가중치 API를 불러 쓰는 것도 같은 제약을 받는다고 보는 편이 안전합니다.** 근거: [2.1 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE) · [2.0 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE) · [Omni](https://github.com/Tencent-Hunyuan/Hunyuan3D-Omni/blob/main/License.txt) · [Part](https://github.com/Tencent-Hunyuan/Hunyuan3D-Part/blob/main/LICENSE) · [HY-World 2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0/blob/main/License.txt) · [HY-Motion 1.0](https://github.com/Tencent-Hunyuan/HY-Motion-1.0)
> - Tencent Cloud의 **Hunyuan 3D 3.0/3.1 API**(가중치 비공개)는 오픈웨이트 라이선스와 별개인 서비스 약관을 따릅니다. 한국 계정으로 쓸 수 있는지, 지역 조항이 있는지는 **(미확인)** 입니다. 확인하기 전에는 상업 프로젝트에 쓰지 마세요.
> - **"MIT라서 안전하다"도 절반만 맞습니다.** TRELLIS.2 코드는 MIT이지만, 텍스처링 파이프라인과 GLB 후처리가 **비상업 전용 라이선스인 nvdiffrast**를 import합니다. 이미지 인코더는 DINOv3 License를 따르고, 파이프라인 기본 배경 제거기는 **비상업 RMBG-2.0**으로 보고됩니다. 상업 프로젝트라면 [9장](#9-상업-파이프라인-함정)을 먼저 보세요.
> - **SaaS는 "어느 플랜으로 생성했는가"가 곧 라이선스입니다.** Tripo 무료 플랜은 비상업, World Labs Marble은 Free·Standard에 상업권 없음, Meshy 무료 플랜은 CC BY 4.0(출처 표기 필요)입니다. Rodin 무료·체험 키로 만든 결과물은 상업권이 **(미확인)** 이니 비상업으로 취급하세요.

## 핵심 요약

- **역할 분담부터 정리하세요.** GPT-6 Astra, Claude Fable 5.1, Opus 5.5 같은 LLM은 3D 메시를 직접 "생성"하지 않습니다. MCP로 생성기를 호출하고, 스키마를 확인하고, 후처리 코드를 짜고, 결과를 검증하는 **감독** 역할입니다. 메시는 Rodin·Tripo·Meshy·TRELLIS.2 같은 3D 생성 모델이 만듭니다. Scenario 문서에 나오는 "GPT-6 Astra 3D"는 Scenario가 자체적으로 붙인 파이프라인 이름으로 보이며, OpenAI가 내놓은 3D 제품이라는 근거는 없습니다.
- **최신 버전(2026-09 기준).** 상용 서비스는 Rodin Gen-2.5, Tripo v3.1·P1·P2(P2는 2026-09-15), Meshy 7·7.1(7.1은 2026-09-20), Tencent Hunyuan 3D 3.1, Hitem3D v2.0(Sparc3D 2.1)입니다. 오픈 모델 최상위권은 Microsoft **TRELLIS.2**(4B)와 TencentARC **Pixal3D**(SIGGRAPH 2026)이고, ComfyUI 본체가 2026-08-21부터 둘 다 네이티브로 지원합니다.
- **한국 사용자 기본 조합.** 클라우드는 Rodin, Meshy, Tripo를 **유료 플랜**으로 쓰세요. 로컬에서 쓸 때는 TRELLIS.2나 Pixal3D가 맞고, 상업 목적이면 의존성 라이선스를 검토해야 합니다. Hunyuan 로컬 가중치는 쓰지 않습니다.
- **용도별로 생성기를 고르세요.** 가구·하드서피스는 Rodin Gen-2.5 Low + bbox, Tripo P1/P2, Meshy smart-topology가 맞습니다. 조형물처럼 디테일이 높은 대상은 Rodin Extreme-High, TRELLIS.2·Pixal3D 1536, Hitem3D 1536pro를 씁니다. 캐릭터는 Rodin TAPose, Meshy A-pose와 리깅을 조합하고, 월드는 Marble(Pro 이상)의 splat을 collider mesh로 변환합니다.
- **품질의 절반은 입력 이미지에서 갈립니다.** 오브젝트 하나를 화면 중앙에 두고, 단색이나 투명 배경, 3/4 뷰, 부드러운 조명, 글자 없음을 지키세요. 텍스트로 바로 3D를 만들기보다 텍스트→이미지→3D 두 단계로 나누는 편이 낫습니다. 멀티뷰 입력 순서는 모델마다 다릅니다.
- **치수는 생성 단계에서 지정하세요.** Rodin `bbox_condition [W,H,L]`과 `height`(cm), Tripo `auto_size`, Scenario `autoSize`(m 단위)를 씁니다. 생성 후에는 실측 높이로 정규화하고(아래 코드는 Blender 4.2.23 LTS·5.0.1에서 테스트함) [scene_audit.py](../03_playbooks/scripts/README.md)로 확인합니다.
- **파트는 분리해서 받으세요.** Rodin BANG, Tripo `generate_parts`, Meshy smart-topology(t2), 로컬에서는 PartCrafter와 OmniPart(MIT)를 씁니다. 한 덩어리 메시로는 서랍 열기, 재질 분리, 부분 수정을 할 수 없습니다.
- **후처리는 선택이 아니라 필수입니다.** 생성 원본은 보통 100만 삼각형 안팎이고, watertight나 manifold를 보장하지 않습니다. master(최대 1M tri, 4K)를 만든 뒤 voxel remesh→decimate→새 UV→bake→LOD(50%/25%)→collision→glTF 검증 순서로 내립니다. 공개 사례(asset-studio, 개인 프로젝트 보고)에서는 상자 에셋 하나(954,901→7,998 tri)가 RTX 5090 한 장에서 11.1분 걸렸습니다.
- **비용은 몇 가지 레버로 조절합니다.** 형태를 싸게 먼저 확정하고 텍스처는 나중에 입힙니다(Meshy는 mesh만 20 credits, 텍스처까지 30). Rodin은 0.5 credit 티어로 탐색하고 최종본만 1.0에 HighPack을 붙입니다. 타임아웃이 나도 재실행하지 말고, 모델 버전은 반드시 고정하세요.
- **"AAA급"이라고 독립 검증된 생성 결과는 찾지 못했습니다.** 생성물은 초안입니다. 품질을 끌어올리는 것도, 저작권 보호를 받는 것도 사람이 리토폴로지·텍스처·배치에 기여한 부분에서 나옵니다.

---

## 1. 먼저 알아 둘 것: LLM과 3D 생성기는 하는 일이 다릅니다

| 층 | 예 | 하는 일 | 이 문서에서 다루는 곳 |
|---|---|---|---|
| 에이전트(LLM) | GPT-6 Astra(Codex), Claude Fable 5.1, Opus 5.5 | 프롬프트 재작성, 생성기 선택, 스키마 확인, 비동기 작업 관리, Blender 후처리 코드 작성, 스크린샷·렌더 비평 | [01 모델 가이드](01_ai_models_and_clients.md), [09 워크플로](09_agent_workflow_prompting.md) |
| 연결(MCP) | ahujasid MCP for Blender, Meshy MCP, Scenario MCP, Rodin skill/CLI | 생성 요청, 결과 다운로드, DCC로 가져오기 | 3장 |
| 3D 생성기 | Rodin, Tripo, Meshy, Hunyuan 3.x(클라우드), TRELLIS.2, Pixal3D | 이미지·텍스트 → 메시 + 텍스처 | 2장 |
| 후처리·검증 | Blender, meshoptimizer, gltf-transform, 이 저장소 스크립트 | 스케일·원점·리토폴·UV·베이크·LOD·검사 | 7장 |

- 실제 사례도 이 분담을 보여 줍니다. 멀티벤더 3D 스킬 저장소 [scenario-labs/skills](https://github.com/scenario-labs/skills)를 보면 [AGENTS.md](https://github.com/scenario-labs/skills/blob/main/AGENTS.md)에 `gpt-6-astra`가 OpenAI Codex 모델명으로 나오고, 커밋 공동 작성자(Co-Authored-By)로 Claude Fable 5.1이 등장합니다(예: [커밋 75d8a7a](https://github.com/scenario-labs/skills/commit/75d8a7a)). LLM 에이전트가 3D 생성 도구를 다루는 스킬 문서를 직접 쓰고 고치는 셈입니다.
- 이런 이유로 LLM을 "3D 품질"로 비교하는 것은 핵심이 아닙니다. 봐야 할 것은 **오케스트레이션, 코드 품질, 이미지 비평 능력**입니다. Codex에서 GPT-6 Astra의 기본 reasoning effort는 `low`이므로, 파이프라인을 감독하게 할 때는 effort를 명시하세요(자세한 내용은 [01 모델 가이드](01_ai_models_and_clients.md)).

---

## 2. 모델·서비스 비교

### 2.1 상용 API·서비스: 기능

| 서비스 (최신 버전·날짜) | 입력 | 출력·토폴로지·폴리곤 제어 | 텍스처·PBR | 파트·치수·포즈 | 속도(보고값) |
|---|---|---|---|---|---|
| **Hyper3D Rodin Gen-2.5** (Deemos, ComfyUI 노드 2026-05-22, CLI 0.2.0 2026-09-23) | 텍스트, 이미지 1~5장(512~4096px, 16MB 이하 JPEG/PNG/WebP) | `mesh_mode` Raw 500~1,000,000(기본 500k) / Quad 1,000~50,000(기본 18k). 티어별 면 수(Raw/Quad): High 1M/50k, Medium 500k/18k, Low 60k/8k, Extra-low 20k/4k. **Gen-2.5는 Raw 권장**, Quad는 legacy 티어에 적합 | material PBR/Shaded/All/None, HighPack(4K), `--texture-delight` | `bbox_condition [W,H,L]`, `height`(cm), TAPose(인간형 T/A 포즈), BANG 파트 분리(strength 1~12, 기본 5), seed 0~65535 | (미확인) |
| **Tripo** (VAST) v3.1-20260211 · P1-20260311 · P2(ComfyUI 2026-09-15) | 텍스트, 이미지, 멀티뷰 2~4장(front/left/back/right 순) | `face_limit`(-1=적응형, 최대 2M. **quad는 150,000에서 조용히 잘린다**는 ComfyUI 주석), `quad=True`면 FBX, `smart_low_poly` 500~20K(quad 500~10K). **P2**: low-poly clean topology, 삼각 GLB 또는 quad-dominant FBX(quad는 선택, 기본 off), face 48~50,000(quad 48~25,000), meshopt 압축 옵션 | `pbr=True`, `texture_quality` standard/detailed/extreme(ComfyUI 기준 2K/4K/8K), P2는 none도 가능, `texture_seed` | `generate_parts`, segmentation, `auto_size`, `orientation='align_image'`, 리깅·retarget, stylize(LEGO/voxel) | H3.1 약 150초, P1 약 76초(서드파티 [trident-mcp](https://github.com/mordor-forge/trident-mcp/blob/main/docs/MCP_TOOLS.md) 실측) |
| **Meshy 7 / 7.1** (7은 2026-08, 7.1은 ComfyUI 2026-09-20) | 텍스트, 이미지, 멀티 이미지. "an image beats text": 이미지 입력이 텍스트보다 우선 | `topology` quad/triangle, `target_polycount` 100~300,000(ComfyUI 기본 300,000), `should_remesh`, smart-topology `meshy-t1/t2`(파트 분리 메시) | `enable_pbr`(**ComfyUI 기본 false이므로 반드시 켤 것**), 2k/4k/8k, `ultra_mode`(4k ultra_resolution은 ComfyUI 기준 7.1/latest 전용), multi-view retexture | `pose_mode` A-pose/T-pose, `symmetry_mode` auto/on/off, rig 또는 animate(순차가 아니라 둘 중 선택) | (미확인) |
| **Tencent Hunyuan 3D 3.0 / 3.1** (클라우드 전용, 3.0 2025-09-16 발표, 3.1 글로벌 제공 2026-01-28) | 텍스트, 이미지, 스케치 | `face_count` 3,000~1,500,000(기본 500,000), `polygon_type` triangle/quadrilateral, `generate_type` Normal/LowPoly/Geometry/Sketch(**LowPoly는 3.1에서 불가**), SmartTopology, 결과 포맷 STL/USDZ/FBX | `enable_pbr`(metallic/normal/roughness), UV 생성(ModelTo3DUV), TextureEdit | 3DPart | (미확인) |
| **Hitem3D v2.0 / Sparc3D 2.0·2.1** (Math Magic) | **이미지만**(텍스트 프롬프트 없음), 4뷰 front/back/left/right(장당 20MB 이하) | 해상도 512³/1024³(권장)/1536³/1536pro, face 100K~2M(커뮤니티 래퍼 기준, 기본 1M. Scenario 경유 시 500K~2M, Sparc3D 2.0은 옵션 없음), OBJ/GLB/STL/FBX | geometry_only / texture_only / both | Base 라인(소품), Portrait 라인(두상·흉상) | **중앙값 17~21분** |
| **Scenario "GPT-6 Astra 3D"** (2026-09-21 문서 추가) | 사진·렌더 1~8장 | `faceBudget`(게임용 10k~50k. 기본값은 고디테일이라 게임용이 아님), `buildEffort`, `refineSteps` | 파트별 PBR | named parts, `autoSize`(m) | (미확인) |

- Rodin 파라미터 출처: [rodin3d-skills SKILL.md](https://github.com/DeemosTech/rodin3d-skills/blob/main/skills/rodin3d-skill/SKILL.md), [hyper3d-cli README](https://raw.githubusercontent.com/DeemosTech/hyper3d-cli/main/README.md), [ComfyUI nodes_rodin.py](https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/comfy_api_nodes/nodes_rodin.py). ComfyUI 폴리곤 프리셋은 Quad 4K/8K/18K/50K/200K, Triangle 2K/20K/150K/200K/500K/1M입니다.
- Tripo: [SDK client.py](https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/tripo3d/client.py), [ComfyUI nodes_tripo.py](https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/comfy_api_nodes/nodes_tripo.py). **Python SDK(tripo3d 0.4.2, 2026-07-01)의 기본 모델은 아직 `v2.5-20250123`입니다.** `model_version`을 반드시 지정하세요. P2를 "quad 전용 모델"로 소개하는 글이 있는데 부정확합니다.
- Meshy: [meshy-mcp-server](https://github.com/meshy-dev/meshy-mcp-server), [ComfyUI nodes_meshy.py](https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/comfy_api_nodes/nodes_meshy.py). MCP README에는 "text-to-3D는 meshy-6까지"라고 되어 있지만, ComfyUI 공식 파트너 노드는 text-to-3D에서도 meshy-7(2026-08-24)과 7.1(2026-09-20)을 선택할 수 있게 해 둡니다. 서로 어긋나므로 **공식 API 문서로 다시 확인하세요.**
- Hunyuan 3.x: [ComfyUI nodes_hunyuan3d.py](https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/comfy_api_nodes/nodes_hunyuan3d.py), [dcc-ai-hunyuan3d tools.yaml](https://raw.githubusercontent.com/dcc-mcp/dcc-ai-hunyuan3d/main/skill/hunyuan3d/tools.yaml). 둘 다 서드파티 래퍼라서 Tencent Cloud 공식 문서로는 확인하지 못했습니다.
- Hitem3D/Sparc3D: [Scenario sparc3d skill](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-sparc3d/SKILL.md)을 기준으로 삼았습니다. 커뮤니티 ComfyUI 래퍼는 비공식이라 1차 근거로 쓰지 않았습니다.
- Scenario Astra 3D: 출처가 [Scenario scenario-3d SKILL.md](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-3d/SKILL.md) 한 곳뿐입니다. "props and hard-surface subjects, not characters"라는 설명과 성능 주장은 **벤더 자체 설명이며 독립 검증은 없습니다.**
- **기타(미확인)**: CSM, Kaedim(사람이 검수하는 게임용 토폴로지, 견적제), Autodesk Wonder 3D/Project Bernini, NVIDIA Edify 3D, ByteDance Seed3D는 공식 사이트가 차단되어 2026년 현황을 확인하지 못했습니다. "Seed3D 2.0"은 SEO성 저장소에서만 보여 실재 여부도 확인하지 못했습니다.

### 2.2 상용 API·서비스: 비용·상업 조건·연동

| 서비스 | 비용 (확인 수준) | 상업 이용 조건 | MCP·Blender 연동 경로 (2026-09) |
|---|---|---|---|
| **Rodin** | Gen-2.5 생성 1회에 0.5 credit(Extreme-High만 1.0), HighPack(4K 텍스처) +1 credit. 구독은 Creator $30/월, Business $120/월(API 전체 접근, High-Poly Quad 포함). 크레딧 직접 구매 시 1 credit = $1.5 | 유료 플랜은 상업권이 있다고 보고됩니다. **무료 플랜과 체험 키는 (미확인)이므로 비상업으로 취급하세요.** ahujasid 애드온에 들어 있는 체험 키 `vibecoding`도 마찬가지입니다 | ahujasid MCP for Blender 내장(자기 키 BYOK 가능), 공식 [rodin3d-skills](https://github.com/DeemosTech/rodin3d-skills)(Claude plugin), [@hyper3d/cli](https://www.npmjs.com/package/@hyper3d/cli), ComfyUI, [DeemosTech](https://github.com/DeemosTech)의 UE RodinBridge(2026-07-17)·Godot 플러그인. [rodin-api-mcp](https://github.com/DeemosTech/rodin-api-mcp)는 마지막 커밋이 2025-04-22라 **추천하지 않음** |
| **Tripo** | H3.1 약 50 credits, P1 약 40 credits(서드파티 실측). P2는 ComfyUI 가격 배지 기준 100~130 Comfy credits(약 $1.00~1.30). Free는 월 약 200 credits(약 8개 모델), Professional은 $19.90/월에 3,000 credits(1회 25 credits 기준 약 120개). Max $89.9/월, Team $109.9/월(월 결제, 보고값). API 100 credits당 $1은 **(미확인)** | **Free는 공개 모델에 비상업.** Professional 이상에서는 **구독이 활성화된 기간에 생성한 모델**에 상업권과 비공개가 적용됩니다 | ahujasid에서는 **유료 Premium 전용**(2026-09-25부터, 자기 키로는 불가). 공식 [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp)는 마지막 커밋이 2025-04-14인 alpha라 **추천하지 않음**. 대안은 커뮤니티 [trident-mcp](https://github.com/mordor-forge/trident-mcp/blob/main/docs/MCP_TOOLS.md)(Go), [SDK](https://pypi.org/project/tripo3d/), ComfyUI 노드 |
| **Meshy** | meshy-7/6 기준 mesh 20, +texture 30, +8K 35 credits. smart-topology t2는 5/15/20, meshy-5는 5/15, ultra_mode +5, remesh 5, rig 5, animate 3, uv-unwrap 5. **플랜 이름과 달러 가격은 (미확인)**(공식 가격 페이지 제목은 Free/Pro/Studio/Enterprise) | **Free는 CC BY 4.0**이라 "Meshy" 출처를 표기하면 상업 이용이 가능합니다. 유료 플랜은 비공개 소유인데, Meshy Community에 공개하지 않고 업로드한 입력(참조 이미지 등)이 타인 권리를 침해하지 않는다는 조건이 붙습니다([Help Center](https://help.meshy.ai/en/articles/9992001-can-i-use-my-generated-assets-for-commercial-projects)) | 공식 [@meshy-ai/meshy-mcp-server](https://www.npmjs.com/package/@meshy-ai/meshy-mcp-server) 0.5.2(2026-09-22, 24 tools: remesh·retexture·UV unwrap·rig·animate·프린트 검증). Claude Code, Claude Desktop, Cursor, Codex, VS Code 지원. ComfyUI |
| **Hunyuan 3D 3.x (Tencent Cloud)** | 종량 과금(단가 미확인). 자체 플랫폼은 **신규 크리에이터**에게 하루 20회 무료 | **한국에 적용되는 약관은 (미확인).** 확인 전 상업 사용 보류 | ahujasid(Tencent Cloud SecretId/SecretKey, 본토 ap-guangzhou / 국제 ap-singapore), [dcc-ai-hunyuan3d](https://github.com/dcc-mcp/dcc-ai-hunyuan3d)(2026-08-25), ComfyUI |
| **Hitem3D** | Free / PRO $19.9 / MAX $39.9 per month(비교 사이트 한 곳 기준, 신뢰도 낮음). "Hi3D"로 리브랜딩했다는 언급이 있음 | (미확인) | Scenario MCP, 비공식 ComfyUI 래퍼 |
| **Scenario** (멀티벤더) | 구독 + credit(금액 미확인) | 벤더별 조건 + Scenario 약관(미확인) | Scenario MCP(OAuth·API 키) + [scenario-labs/skills](https://github.com/scenario-labs/skills)(0.48.0, 2026-09-26). Meshy·Rodin·Sparc3D·Hunyuan·Tripo·Trellis·Astra 3D·Marble·HY World·TripoSplat을 한 MCP로 제공. Blender 5.2, Maya 2027, UE 5.8용 DCC 전문가 스킬 포함 |

- 가격 출처는 대부분 애그리게이터 요약입니다. **가격표를 코드나 CLAUDE.md에 고정하지 말고**, 도입 직전에 공식 페이지를 확인하세요: [Meshy](https://www.meshy.ai/pricing), [Tripo](https://www.tripo3d.ai/pricing), [Hyper3D](https://hyper3d.ai/pricing), [Marble](https://docs.worldlabs.ai/marble/support/account-billing).
- **Scenario 경유 Hunyuan에 주의하세요.** Scenario의 3D Worlds 스킬에는 "HY World members carried a geo restriction tag"라고 적혀 있습니다([scenario-3d-worlds](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-3d-worlds/SKILL.md)). 중개 서비스를 거쳐도 지역 제한은 사라지지 않습니다. Scenario에서 제공하는 Hunyuan 모델이 어떤 버전인지, 어떤 약관을 따르는지 확인하기 전에는 한국에서 쓰지 마세요.

### 2.3 오픈웨이트 (로컬 실행)

| 모델 (공개일) | 라이선스 / 한국 | 출력 | 텍스처 | VRAM · 속도 | 비고·연동 |
|---|---|---|---|---|---|
| **Microsoft TRELLIS.2-4B** (2025-12-16, 학습 코드 2026-01-10, 마지막 커밋 2026-06-05) | 코드 MIT. 지역 제한은 없습니다. **단, 상업 사용은 의존성 검토가 필요합니다**(nvdiffrast 비상업, DINOv3 License, 배경 제거 가중치) | GLB. O-Voxel 512³/1024³/1536³ cascade. open surface, non-manifold, 내부 구조까지 표현 | base color, roughness, metallic, opacity. **normal 맵은 출력하지 않음**(bake 필요). 알파는 텍스처에 남지만 OPAQUE로 export | **24GB 이상**(A100·H100에서 검증), Linux. H100 기준 512³ 약 3초, 1024³ 약 17초, 1536³ 약 60초(벤더 자체 보고) | 텍스처 전용 `Trellis2TexturingPipeline`(메시+이미지) 제공. ComfyUI 네이티브([nodes_trellis2.py](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_trellis2.py)), [trellis_blender](https://github.com/FishWoWater/trellis_blender), trellis2_mcp, [asset-studio](https://github.com/zorrobyte/asset-studio). [저장소](https://github.com/microsoft/TRELLIS.2) |
| **TencentARC Pixal3D** (SIGGRAPH 2026, 2026-05 코드, 2026-09-01 multi-view) | MIT. TencentARC 소속이라 **Hunyuan 라이선스가 아니고 한국 제외 조항이 없음**. 다만 DINOv3를 불러옴(NOTICE에는 dinov2만 기재) | PBR GLB(UV 텍스처) | PBR | 기본 1536, `--low_vram` 또는 `--resolution 1024`. C++ 포트 [pixal3d.cpp](https://github.com/raven38/pixal3d.cpp)는 1024 cascade 기준 16GB 카드에서 동작 | 개선판은 TRELLIS.2 backbone(main 브랜치), 원 논문판은 Direct3D-S2 기반. `python inference.py --image in.png --output out.glb`, 멀티뷰는 `python inference_mv.py --views_dir <dir>`. 알파가 없으면 자동으로 배경 제거. 정량 벤치마크 없음. [저장소](https://github.com/TencentARC/Pixal3D) |
| **DreamTech Direct3D-S2** (2025-05-30) | MIT | OBJ, **형상만** | 없음 | 512는 10GB, 1024는 약 24GB | 텍스처는 TRELLIS.2 texturing이나 Meshy retexture로 입힘. [저장소](https://github.com/DreamTechAI/Direct3D-S2) |
| **StepFun Step1X-3D** (2025-05-13) | Apache-2.0 | GLB(watertight TSDF) | 3.5B 텍스처 모델 | 27~29GB, 50 step에 약 152초(벤더 자체 보고) | LoRA 파인튜닝. 독립 비교는 없음. [저장소](https://github.com/stepfun-ai/Step1X-3D) |
| **Meta SAM 3D Objects** (2025-11-19) | SAM License. 상업 허용, ITAR·군사·제재 대상 사용과 역공학은 금지 | Gaussian splat `.ply` + mesh `.glb`, **여러 객체의 위치·자세 포함** | 텍스처(게임용 PBR은 아님) | **NVIDIA 32GB 이상**([setup.md](https://github.com/facebookresearch/sam-3d-objects/blob/main/doc/setup.md)). 24GB 카드로는 부족 | 가림이 있는 실사진에서 가구 여러 개를 동시에 복원해 배치 참고용으로 씀. [저장소](https://github.com/facebookresearch/sam-3d-objects) |
| **Stability SPAR3D / Stable Fast 3D** (2025년 초) | Stability Community License(연매출 100만 달러 미만이면 상업 가능) | UV 펼친 메시 | material 예측 | 10.5GB(low VRAM 모드 약 7GB) | 매우 빠르고 point cloud를 편집해 뒷면을 고칠 수 있음. 충실도는 낮아 프리비즈용. [LICENSE](https://github.com/Stability-AI/stable-point-aware-3d/blob/main/LICENSE.md) |
| **PartCrafter** (NeurIPS 2025) | MIT | 파트별·객체별 메시 | 없음 | 8GB 이상 | 파트 수를 직접 지정하거나 VLM에게 추천받음. [저장소](https://github.com/wgsxm/PartCrafter) |
| **OmniPart** (2025-10) | MIT | 파트 분리 3D(2D 파트 mask `.exr` 조건) | TRELLIS 1세대 수준 | 미명시 | mask를 고쳐 파트 경계를 직접 정함. [저장소](https://github.com/HKU-MMLab/OmniPart) |
| **NVIDIA PartPacker** | **NVIDIA Source Code License, 비상업**([license.md](https://github.com/NVlabs/PartPacker/blob/main/license.md)) | GLB(파트) | 없음 | 약 10GB(fp16) | 연구·참고용 |
| **PhysX-Anything** (CVPR 2026) | S-Lab License(일반적으로 비상업) | URDF, MJCF, PLY(관절·물리 속성) | — | — | 서랍·문 관절 구조 추정 참고. [저장소](https://github.com/ziangcao0312/PhysX-Anything) |
| **SceneGen** (3DV 2026) | MIT | 사진 한 장 → 배치가 포함된 다중 에셋 GLB | TRELLIS 1세대 수준 | — | 배치 초안용. [저장소](https://github.com/Mengmouxu/SceneGen) |
| **Roblox Cube 3D v0.5 / CubePart** (2025-07 / 2026-05) | **연구 전용**(CUBE3D RESEARCH-ONLY RAIL-MS). CubePart도 같은 라이선스 | `.obj`, 형상만 | 없음 | 16GB(`--fast-inference`는 24GB) | `--bounding-box-xyz`로 비율 제어, CubePart는 파트 스키마 기반. [저장소](https://github.com/Roblox/cube) |
| **Meta SAM 3D Body** | (미확인) | 사진 한 장 → 전신 인체 메시(MHR 파라메트릭 리그) | — | — | 캐릭터 포즈·체형 레퍼런스용. ComfyUI 네이티브 지원(2026-08-22). [저장소](https://github.com/facebookresearch/sam-3d-body) |
| **Hunyuan3D 2.0/2.1/Omni/Part** | **한국 제외, 사용 금지** | — | — | (참고: 2.1은 shape 10GB, paint 21GB) | Omni의 bbox/point/voxel/pose 제어는 개념적으로 가구에 가장 적합하지만 한국에서는 쓸 수 없음 |

- 2025년 모델(Step1X-3D, Direct3D-S2, PartCrafter 등)은 TRELLIS.2나 Pixal3D보다 디테일이 떨어질 가능성이 큽니다. 다만 같은 입력으로 비교한 독립 벤치마크는 찾지 못했습니다.
- **연구 동향만 보면 되는 것**: Hunyuan3D-Buffalo 1.0(3D 생성·이해·편집 통합)과 WorldClaw(에이전트 기반 오픈월드)는 논문만 공개된 상태입니다(2026-08). 코드·가중치 공개 여부와 라이선스는 명시되지 않았습니다([Tencent-Hunyuan 3D 저장소 목록](https://github.com/orgs/Tencent-Hunyuan/repositories?q=3d)).

### 2.4 월드 생성기

| 이름 | 출력 | 한국·상업 조건 | 쓸 곳과 주의 |
|---|---|---|---|
| **World Labs Marble** (2025-11-12 출시. Scenario 기준 1.0 Draft, 1.1, 1.1 Plus) | 3D Gaussian splat `.spz`가 기본이고 triangle·collider mesh로 export 가능 | 출시 당시 가격 기준 Free 4회, Standard $20(12회, 상업권 없음), **Pro $35(25회, 상업권)**, **Max $95(75회, 상업권)** | 입력은 텍스트, 이미지(평면·360°), 사진 2~8장, 영상입니다(이미지와 영상은 동시에 넣을 수 없음). 같은 seed면 Draft에서 상위 티어로 올려도 같은 월드가 나옵니다. 렌더링은 [Spark](https://github.com/sparkjsdev/spark)(three.js, SPZ/PLY/SOG), 연동은 [worldlabs-api-python](https://github.com/worldlabsai/worldlabs-api-python)과 커뮤니티 [worldlabs-mcp](https://github.com/sandraschi/worldlabs-mcp)(21 tools, Blender/Unity export). 게임 메시로 쓰려면 변환과 retopo가 필요합니다 |
| **HunyuanWorld 1.0 / HY-World 2.0 / 2.1 / WorldMirror** | 1.0: 360° 파노라마 + layered mesh. 2.0(2026-04-16): 텍스트·이미지·멀티뷰·영상을 mesh·3DGS·point cloud로 | **오픈웨이트는 한국 제외.** HY World 2.1(2026-07, 제품) 약관은 (미확인) | 구성 모델이 매우 큽니다(HY-Pano-2 약 80B, WorldStereo-2 약 17B). 한국에서는 쓰지 않습니다. [HY-World 2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0) |
| **NVIDIA Lyra 2.0** (2026-04-15, GUI·학습 코드 2026-07-20) | 영상을 생성한 뒤 3DGS로 재구성해 `reconstructed_scene.ply` 출력 | 코드 Apache-2.0, 모델 라이선스는 버전별로 다름 | 1×H100 80GB 기준 약 9분(DMD 사용 시 약 35초, 벤더 자체 보고)으로 **개인 GPU용이 아닙니다**. [Lyra-2](https://github.com/nv-tlabs/lyra/tree/main/Lyra-2) |
| **Google DeepMind Genie 3** | 인터랙티브 **비디오 프레임**(메시·splat 파일이 아님) | (미확인) | 콘셉트나 무드 탐색용 레퍼런스 영상·스크린샷만 만들 수 있습니다. 2026년 현황은 1차 출처로 확인하지 못했습니다 |
| **ComfyUI TripoSplat / Gaussian splat 노드** (2026-06-01 / 2026-05-31) | 단일 객체 사진 → splat | (미확인) | 로컬 splat 워크플로. [nodes_triposplat.py](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_triposplat.py) |
| **SAM 3D Objects · SceneGen** | 실사진 → 다중 객체와 배치 | 상업 가능 / MIT | 방 사진에서 가구 배치를 뽑는 참고용. 배치 방법은 [08 배치 가이드](08_scene_layout_placement.md) |

---

## 3. MCP·에이전트 연동 경로

### 3.1 추천 조합 (한국 사용자 기준)

| 조합 | 구성 | 장점 | 주의 |
|---|---|---|---|
| **A. 가장 간단한 클라우드** | ahujasid MCP for Blender + Rodin 자기 키(BYOK) → Blender에서 정리·검증 | 생성, import, 배치, 스크린샷 검증을 에이전트 하나로 처리. 서버 프롬프트도 먼저 통합 상태를 확인하고 변경 전후에 `get_viewport_screenshot()`을 찍으라고 권장 | 생성기 파라미터 노출이 제한적입니다(세부 quality, mesh_mode 등). 세밀하게 제어하려면 B나 C를 함께 쓰세요. Hunyuan 통합은 끄세요 |
| **B. 파라미터를 세밀하게** | 공식 Meshy MCP 또는 Rodin 공식 skill + `hyper3d` CLI(`--output json`) → 파일로 받아 Blender MCP로 import | quad·polycount·bbox·delight·BANG을 모두 제어 | 결과 URL 만료(Rodin은 10분), 비동기 폴링 규칙이 필요 |
| **C. 로컬·무료** | ComfyUI 네이티브 TRELLIS.2/Pixal3D(+ Paint Mesh, Bake Texture From Voxel 최대 8192) 또는 asset-studio MCP → Blender | 크레딧이 들지 않고, 지역 제한 없는 오픈 모델이라 한국에서 가장 쉽게 시작 | TRELLIS.2는 24GB 이상 GPU 필요(pixal3d.cpp는 1024 cascade를 16GB에서 실행). **상업 납품에는 9장의 의존성 라이선스 검토 필수** |
| **D. 멀티벤더 비교** | Scenario MCP + skills | 벤더 교체와 A/B 비교가 쉽고, 모델 비교 절차가 스킬로 정리됨 | 중개 비용이 붙음. Hunyuan·HY World 항목 주의 |

### 3.2 연동 도구별 요점

- **ahujasid MCP for Blender**([README](https://github.com/ahujasid/blender-mcp/blob/main/README.md), [server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py))
  - 생성 tool: `generate_hyper3d_model_via_text`, `generate_hyper3d_model_via_images`, `poll_rodin_job_status`, `import_generated_asset`, `generate_hunyuan3d_model`, `generate_tripo_model`.
  - 환경변수: `BLENDERMCP_HYPER3D_API_KEY`, `BLENDERMCP_HUNYUAN3D_SECRET_ID` / `_SECRET_KEY` / `_API_URL`, `BLENDERMCP_SKETCHFAB_API_KEY`, `BLENDERMCP_POLYPIZZA_API_KEY`.
  - 2026-09-25부터 유료 **Premium**이 생겼습니다. 자기 키 없이 Hunyuan3D·Tripo·Rodin을 생성할 수 있고, **Tripo는 Premium에서만** 쓸 수 있습니다. Premium의 Hunyuan이 어느 버전인지는 확인하지 못했으므로 한국에서는 쓰지 마세요.
  - 로컬 Hunyuan 모드의 기본 URL은 `http://localhost:8081`인데, Hunyuan3D-2 `api_server.py` 예시는 8080 포트입니다. 한국에서는 이 모드 자체를 쓰지 않습니다.
  - 보안(임의 Python 실행, `BLENDER_MCP_SAFE_MODE`), 텔레메트리, 공식 Blender Lab 서버와의 포트 충돌(9876)은 [02 Blender MCP 가이드](02_blender_mcp.md)를 보세요.
- **Meshy 공식 MCP**: `npx add-mcp @meshy-ai/meshy-mcp-server --env MESHY_API_KEY=msy_...`. 0.5.0은 npm에 없고 0.5.1(2026-08-27), 0.5.2(2026-09-22)가 배포되어 있습니다.
- **Rodin**: `npm install --global @hyper3d/cli@latest`. 에이전트가 `--output json`으로 호출하게 하면 스크립트로 다루기 쉽습니다. Claude Code에서는 [rodin3d-skills](https://github.com/DeemosTech/rodin3d-skills)를 플러그인으로 설치합니다. 공식 스킬에 티어별 용도와 면 수 매핑이 정리되어 있습니다.
- **Tripo**: ahujasid에서는 Premium 전용이고 공식 tripo-mcp는 방치 상태입니다. 따라서 [SDK](https://pypi.org/project/tripo3d/)나 ComfyUI 노드, 커뮤니티 trident-mcp를 쓰는 편이 현실적입니다. ([02 가이드](02_blender_mcp.md)는 tripo-mcp를 대안으로 소개하지만, 이번 검증에서 2025-04-14 이후 커밋이 없는 것을 확인했습니다.)
- **TRELLIS.2 / Pixal3D**: ComfyUI 본체에서 2026-08-21(PR #14718)부터 커스텀 노드 없이 돌아갑니다. [asset-studio](https://github.com/zorrobyte/asset-studio)는 Claude Code용 MCP tool(`generate`, `status`, `artifacts`, `retry`, `open_in_blender`)을 제공합니다. [trellis_blender](https://github.com/FishWoWater/trellis_blender)의 기본값은 sampling steps 12, CFG 7.5, simplify 0.95, texture 1024/2048, bake mode fast|opt입니다.
- **Scenario MCP 표준 절차**: `recommend`로 모델을 찾고 → `model_schema_get` → `model_run(wait=false)` → `jobs_wait` → `asset_display`(직접 눈으로 확인) → `asset_download` 순서입니다. 모델 ID는 하드코딩하지 말고 매번 `recommend`와 `model_schema_get`으로 확인하세요. 카탈로그에서 빠지는 모델에는 `deprecated:<replacement_id>` 태그가 붙습니다. 흔한 실수로 스키마를 보지 않고 실행하기, 로컬 경로를 그대로 넘기기, 모델 ID 하드코딩이 문서에 정리되어 있습니다.
- **ComfyUI Partner(API) Nodes**: Rodin, Tripo, Meshy, Hunyuan 3.x 노드가 본체에 들어 있어서 **최신 모델이 가장 빨리 반영되고**, 한 워크플로에서 벤더끼리 A/B 비교를 할 수 있습니다([comfy_api_nodes](https://github.com/comfyanonymous/ComfyUI/tree/master/comfy_api_nodes)). 벤더마다 파라미터 이름이 조금씩 다르게 매핑되니 주의하세요.

### 3.3 에이전트에게 줄 비동기 작업 규칙 (CLAUDE.md·스킬에 그대로 넣기)

```markdown
## 3D 생성 작업 규칙
- 생성 전: 모델 버전을 명시한다(Tripo model_version, Meshy ai_model). "latest"나 SDK 기본값에 맡기지 않는다.
- 생성 전: 스키마를 조회한다(Scenario model_schema_get 등). 멀티뷰 순서와 장수는 모델마다 다르다.
- 생성 전: 유료 생성은 사용자 승인을 받는다. 예상 크레딧과 pass/fail 기준을 먼저 적는다.
- 제출 후: 타임아웃이 나도 같은 작업을 다시 제출하지 않는다. job id로 상태를 조회한다(jobs_wait, poll_rodin_job_status).
- 완료 즉시: 결과 파일을 로컬에 저장한다(Rodin 다운로드 링크는 10분 뒤 만료).
- import 후: 스케일·원점·트랜스폼을 정규화하고, scene_audit.py와 검토 렌더로 확인한 다음에 다음 단계로 간다.
- 기록: 에셋마다 provenance(도구·모델 버전·플랜·날짜·입력 이미지·라이선스·사람이 수정한 내역)를 남긴다.
```

---

## 4. 용도별 선택 가이드

| 용도 | 1순위 | 대안 | 핵심 설정 | 주의 |
|---|---|---|---|---|
| **가구·하드서피스 소품** (게임용) | Rodin Gen-2.5 **Low**("Clean assets, small hardsurface props") + `bbox_condition` | Tripo **P1/P2**(game-ready low-poly), Meshy smart-topology t2, Scenario Astra 3D(named parts, 벤더 설명) | Low는 Raw 60k / Quad 8k. Tripo `smart_low_poly` 500~20K. 삼각형 예산은 7.2절 참고 | 단순한 형태(책상, 선반, 상자)는 생성보다 **코드 모델링**이 토폴로지와 치수 모두 정확합니다([07 모델링 가이드](07_modeling_objects_furniture_sculpture.md)) |
| **비율이 중요한 가구** (의자·식탁·침대) | Rodin `bbox_condition` + `height` | Tripo `auto_size`, Scenario `autoSize` | 치수는 [05 치수표](../03_playbooks/05_reference_dimensions.md)에서 가져옵니다 | 이미지 한 장으로는 깊이가 모호합니다. 생성 후 반드시 정규화하고 `scene_audit.py`로 확인하세요 |
| **서랍·문이 있는 가구** | 파트 분리(Rodin BANG, Tripo `generate_parts`, Meshy t2) 후 Blender에서 피벗 설정 | PartCrafter/OmniPart(MIT, 로컬) | BANG `--strength 5 --instruction "separate ..."` | 관절 자동 추정 모델 PhysX-Anything은 비상업이라 참고용으로만 씁니다 |
| **조형물·부조·고디테일** | Rodin **Extreme-High**("High-frequency detail reproduction") | TRELLIS.2 1536 cascade, Pixal3D 1536, Hitem3D 1536pro(최대 2M faces) | 원본은 고폴리로 받고 7장처럼 bake | 느리고(Hitem3D 17~21분) 고폴리라 retopo가 필수입니다 |
| **스타일라이즈** | Rodin legacy **Smooth**("clear edges and stylized") | Tripo stylize(LEGO/voxel 등) | — | 플랫·벡터 스타일 그림을 TRELLIS.2에 넣으면 색이 크게 틀어진다는 보고가 있습니다 |
| **캐릭터** | Rodin **TAPose** | Meshy `pose_mode="A-pose"` + rig 또는 animate, Tripo 리깅·retarget | T/A 포즈로 생성해야 리깅이 쉽습니다 | Scenario Astra 3D는 캐릭터용이 아닙니다. 체형·포즈 레퍼런스에는 SAM 3D Body. HY-Motion(텍스트→모션)은 한국 제외 |
| **두상·흉상** | Sparc3D/Hitem3D **Portrait** 라인 | Rodin 고티어 | 4뷰 front/back/left/right | 비용과 시간이 큽니다 |
| **실사진 → 가구 배치 참고** | SAM 3D Objects(32GB+) | SceneGen(MIT) | 객체 mask(SAM) | 에셋 품질은 게임용 수준이 아닙니다. 위치와 자세만 참고하세요 |
| **월드·배경** | Marble **Pro 이상**(상업권) | Lyra 2(H100), 에셋 라이브러리 조립 | Draft로 탐색하고 같은 seed로 상위 티어 | splat은 게임 메시가 아닙니다. collider mesh export 후 retopo가 필요합니다. 근경 오브젝트는 따로 만드세요 |
| **빠른 프리비즈** | Stable Fast 3D / SPAR3D | TRELLIS.2 512³(약 3초) | — | 연매출 100만 달러 이상이면 Stability Enterprise 라이선스가 필요합니다 |

> 이 표는 각 벤더 문서의 용도 설명과 커뮤니티 정성 평가에 근거합니다. 가구·하드서피스·조형물을 같은 입력으로 비교한 **정량 벤치마크는 찾지 못했습니다.** 중요한 에셋은 후보 2~3개를 같은 레퍼런스로 돌려 직접 비교하세요.

---

## 5. 레퍼런스 이미지 준비 규칙

### 5.1 체크리스트

| 규칙 | 이유 | 근거 |
|---|---|---|
| 한 이미지에 **오브젝트 하나**, 화면 중앙 | 여러 객체가 있으면 matting과 형태가 무너짐 | asset-studio, Scenario("a single centered subject on a plain background") |
| **단색 또는 투명(알파) 배경** | TRELLIS.2는 배경이 있으면 "severe artifacts and missing geometry (holes)"가 생김 | [TRELLIS.2 이슈 #65](https://github.com/microsoft/TRELLIS.2/issues/65) |
| **3/4 뷰**, 부드럽고 고른 스튜디오 조명 | 앞면과 옆면 정보를 동시에 담고, 그림자가 형태로 오인되지 않게 함 | asset-studio 프롬프트 재작성 규칙 |
| 글자, 로고, 소품 없음 | 글자는 형태를 망가뜨리고 상표 문제도 생김 | asset-studio |
| **사실적인 셰이딩**(플랫·벡터 일러스트 피하기) | "TRELLIS.2 can get colours badly wrong on flat or vector-style art" | [image-to-3dlab](https://raw.githubusercontent.com/Bingeljell/image-to-3dlab/main/docs/info_and_credits.md) |
| 반사나 강한 조명이 있으면 **delight** 켜기 | 텍스처에 그림자·하이라이트가 구워지면 엔진 조명과 겹쳐 이중 음영이 생김 | Rodin `--texture-delight`("for highly reflective reference"), Scenario `delight: true` |
| 해상도·용량 제한 지키기 | 규격을 벗어나면 거부되거나 품질이 떨어짐 | Rodin 512~4096px·16MB 이하 JPEG/PNG/WebP, Hitem3D 장당 20MB 이하 |
| 유명 디자인이나 IP 복제 금지 | 출력 소유권 양도가 제3자 권리 침해까지 막아 주지는 않음 | 9장 |
| `NoAI` 태그가 붙은 에셋은 입력으로 쓰지 않기 | 창작자가 생성형 AI 사용을 거부한 표시 | [10 에셋·라이선스 가이드](10_assets_pipeline_licensing.md) |

### 5.2 텍스트 → 이미지 → 3D 두 단계로

텍스트에서 바로 3D를 만들기보다, 이미지 모델로 레퍼런스를 먼저 만들고 사람이 확인한 뒤 image-to-3D로 넘기세요. [asset-studio](https://github.com/zorrobyte/asset-studio)는 모든 프롬프트를 아래 조건으로 자동 재작성합니다.

```text
a mid-century oak lounge chair, single object, centered, plain light-grey background,
three-quarter view, soft even studio lighting, no text, no props
```

한국어로 요청받았다면 에이전트에게 이렇게 시키세요.

```text
사용자 설명을 영어 이미지 프롬프트로 바꿔라. 반드시 다음을 포함한다:
single object, centered, plain light-grey background, three-quarter view,
soft even studio lighting, realistic shading, no text, no logo, no props.
실존 브랜드나 디자이너 이름은 쓰지 말고 형태·재료·시대 스타일로만 묘사한다
(예: "Eames lounge chair" 대신 "1950s mid-century molded plywood lounge chair, original design").
결과 이미지를 보여 주고 승인을 받은 뒤에만 3D 생성을 호출한다.
```

| 레퍼런스용 이미지 모델 (asset-studio·image-to-3dlab 기준) | 특징 | 라이선스 |
|---|---|---|
| Qwen-Image-2512 Lightning | 8 step, 1328², 약 8초 | Apache-2.0 |
| FLUX.2 Klein 4B | 약 2.5초 | 사용 전 확인 |
| Z-Image Turbo | 실루엣이 가장 깨끗함 | 사용 전 확인 |
| Qwen-Image 2.1 | 로컬 M 시리즈 Mac에서 약 4.5분 | **Research License(비상업)** |
| FLUX.2 Klein 9B | — | **비상업** |

### 5.3 멀티뷰 입력 순서 (모델마다 다름)

| 모델 | 장수 | 순서 |
|---|---|---|
| Tripo multiview | 2~4 | front, left, back, right |
| Hitem3D / Sparc3D | 4 | front, back, left, right |
| Rodin | 1~5 | (스키마 확인) |
| Scenario Astra 3D | 1~8 | (스키마 확인) |
| Pixal3D multi-view | 폴더 | 카메라 파라미터 포함(`inference_mv.py --views_dir`) |

순서를 틀리면 앞뒤가 뒤바뀐 형상이 나옵니다. Scenario 문서도 "the count and the ordering vary per model"이라며 스키마부터 조회하라고 강조합니다.

### 5.4 배경 제거는 품질과 라이선스를 같이 봐야 합니다

- TRELLIS.2 코드는 BiRefNet 구조로 배경을 제거합니다. 커뮤니티 파이프라인 두 곳(asset-studio, image-to-3dlab)에 따르면 TRELLIS.2·Pixal3D 파이프라인의 **기본 가중치는 gated·비상업 라이선스인 `briaai/RMBG-2.0`** 입니다(HF 설정 파일은 직접 확인하지 못함). image-to-3dlab은 이 때문에 RMBG-2.0을 패치로 꺼 둡니다.
- **권장 대응**: 알파 PNG를 직접 만들어 넣으세요(투명 배경으로 렌더하거나 편집). 또는 라이선스가 허용되는 matting(예: rembg u2net, MIT 가중치의 BiRefNet)으로 바꾸고 `.provenance.json`에 기록하세요.

---

## 6. 치수·비율 제어와 파트 분리

### 6.1 생성 단계에서 치수 지정

| 도구 | 파라미터 | 단위·동작 | 비고 |
|---|---|---|---|
| Rodin | `bbox_condition [W, H, L]`, `height` | height는 cm | `geometry_instruct_mode`(기본 `faithful`)와 함께 사용 |
| Tripo | `auto_size=True`, `orientation='align_image'` | 실제 크기 추정 | P2도 `auto_size` 지원 |
| Scenario | `autoSize: true` | 실제 m 단위(기본 off) | — |
| Roblox Cube v0.5 | `--bounding-box-xyz` | 비율 | 연구 전용 |
| Hunyuan3D-Omni | `--control_type bbox` | 비율 | **한국 제외** |

### 6.2 생성 후 정규화: Blender 코드 (테스트 완료)

생성기가 치수를 지원하더라도 import한 뒤에는 **실측 높이로 스케일을 맞추고, 원점을 바닥 중앙에 두고, 트랜스폼을 적용**하세요(asset-studio도 `height_m` 기준으로 같은 처리를 합니다). 아래 두 함수는 이 문서를 쓰면서 pip `bpy` **4.2.23 LTS와 5.0.1**에서 헤드리스로 테스트했습니다. glTF를 export한 뒤 다시 import하고, 부모·회전·스케일이 섞인 상태에서 돌려 확인했습니다. `bmesh`와 `mathutils`만 써서 Blender MCP의 `execute_blender_code`에서도 그대로 동작합니다.

```python
import bpy, bmesh
from mathutils import Matrix

def normalize_generated(obj, target_height_m):
    """생성 메시를 실측 높이로 맞추고 원점=바닥 중앙, 변환 적용(단위 행렬) 상태로 만든다."""
    if obj.parent:                                  # 부모(Empty 등)가 있으면 월드 위치를 유지한 채 분리
        mw = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = mw
    me = obj.data
    me.transform(obj.matrix_basis)                  # 위치·회전·스케일을 메시에 굽기
    obj.matrix_basis = Matrix.Identity(4)
    zs = [v.co.z for v in me.vertices]
    s = target_height_m / (max(zs) - min(zs))       # 높이 기준 균일 스케일(비율 유지)
    me.transform(Matrix.Scale(s, 4))
    xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
    me.transform(Matrix.Translation((-(min(xs) + max(xs)) / 2, -(min(ys) + max(ys)) / 2, -min(zs))))
    me.update()
    dims = [max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)]
    return {"scale": round(s, 4), "dims_m": [round(d, 3) for d in dims]}

def basic_cleanup(obj, merge_dist=1e-5):
    """중복 정점 병합 + 노멀 재계산 + 열린 경계/비다양체 에지·삼각형 수 보고."""
    me = obj.data
    bm = bmesh.new(); bm.from_mesh(me)
    n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    rep = {
        "merged_verts": n0 - len(bm.verts),
        "open_boundary_edges": sum(e.is_boundary for e in bm.edges),
        "non_manifold_edges": sum((not e.is_manifold) and (not e.is_boundary) for e in bm.edges),
        "tris": sum(len(f.verts) - 2 for f in bm.faces),
    }
    rep["watertight"] = rep["open_boundary_edges"] == 0 and rep["non_manifold_edges"] == 0
    bm.to_mesh(me); bm.free(); me.update()
    return rep

obj = bpy.data.objects["chair_gen"]      # 이름에 chair/table/sofa 같은 영어 키워드를 넣어야 scene_audit 치수 검사가 동작
print(normalize_generated(obj, 0.80))    # 0.80은 예시값. 실제 값은 05_reference_dimensions.md에서
print(basic_cleanup(obj))                # 정규화 뒤에 실행해야 병합 거리(1e-5)가 m 단위가 되고, 음수 스케일로 뒤집힌 노멀도 바로잡힘
```

- 위아래가 뒤집히거나 옆으로 누운 채 들어오면(생성기마다 up축이 다름) **회전부터 바로잡은 뒤** `normalize_generated`를 호출하세요. 이 함수는 현재 Z축을 높이로 봅니다.
- 부모 Empty가 Z축으로 돌아가 있으면 그 회전도 메시에 구워지므로, 가로·세로 치수는 회전된 상자의 AABB가 됩니다. 앞면을 -Y로 맞춘 다음 실행하세요(이 저장소 스크립트의 규약).
- 한 GLB에 메시가 여러 개 들어 있으면 먼저 하나로 합치거나, 파트로 유지할 경우 부모 Empty 아래 자식으로 묶고 부모 기준으로 스케일하세요.
- 그다음 [placement_utils.py](../03_playbooks/scripts/README.md)의 `snap_to_floor()`와 `drop_to_surface()`로 배치하고, `scene_audit.audit_scene()`으로 떠 있음, 관통, 스케일 미적용, non-manifold, 재질·UV 없음, 이름 기준 치수 범위(예: `chair` 높이 0.70~1.20 m)를 확인합니다.

### 6.3 파트 분리 생성

| 방법 | 입력·제어 | 결과 | 비용·라이선스 |
|---|---|---|---|
| **Rodin BANG** | 완성된 모델 + `--strength 1~12`(기본 5) + `--instruction "separate seat, backrest, four legs"` | 파트별 분리 | Rodin credit |
| **Tripo** | `generate_parts=True`, Smart Segment | 파트 메시 | Tripo credit |
| **Meshy smart-topology** | `model_type='smart-topology'`(meshy-t2) | 파트가 분리된 geometry와 설정 가능한 polycount | mesh 5 credits(t2) |
| **Tencent 3DPart** | 클라우드 노드 | 파트 분할 | 한국 약관 미확인 |
| **Scenario Astra 3D** | 1~8장 | named parts와 파트별 PBR | 벤더 설명, 미검증 |
| **PartCrafter** (로컬) | 이미지 + 파트 수(직접 지정 또는 VLM 추천). 토큰은 객체당 기본 1024, 장면은 2048 | 파트별 메시(텍스처 없음) | MIT, 8GB 이상 |
| **OmniPart** (로컬) | 이미지 + 2D 파트 mask(`.exr` part ID) | 경계를 사용자가 정한 파트 | MIT |
| PartPacker / CubePart / PhysX-Anything | — | 파트·관절 | **비상업·연구 전용** |
| Hunyuan3D-Part (P3-SAM + X-Part) | 메시 → 파트 | 파트 | **한국 제외** |

분리 후 Blender에서 할 일:
1. 파트 이름을 영어로 짓습니다(`chair_seat`, `chair_leg_fl` 등).
2. 파트를 하나의 부모 Empty 아래에 묶습니다. `scene_audit.py`는 최상위 부모를 "유닛"으로 보기 때문에, 부모 없이 흩어진 좌판은 "떠 있음"으로 잡힙니다.
3. 서랍과 문은 회전·이동 피벗을 경첩이나 레일 위치에 둡니다.
4. 재질 슬롯을 파트별로 나눕니다(목재/금속/패브릭). 자세한 규칙은 [05 텍스처링 가이드](05_texturing_materials.md)를 보세요.

---

## 7. 필수 후처리: 게임·렌더에 쓸 수 있게 만들기

생성 원본은 대개 **삼각형 100만 개 안팎에 비정형 토폴로지**이고, watertight나 manifold가 보장되지 않습니다. TRELLIS.2는 열린 면과 non-manifold 구조를 일부러 표현하는 방식입니다. 디테일은 normal·텍스처 bake로 보존하고 메시는 가볍게 다시 만드는 것이 정석입니다.

### 7.1 표준 순서 (asset-studio 방식 기준)

| 단계 | 할 일 | 설정·수치 |
|---|---|---|
| 0. master 확보 | 고해상도로 생성하고 원본을 보관 | 최대 1M tri, 4096² PBR. TRELLIS.2는 `mesh.simplify(16777216)`(nvdiffrast 한계) 후 `to_glb(decimation_target=1000000, texture_size=4096, remesh=True, remesh_band=1, remesh_project=0)` |
| 1. import·정규화 | 스케일, 원점, 트랜스폼 적용, 중복 정점 병합, 노멀 재계산 | 6.2절 코드 |
| 2. 감량 | **voxel remesh 후 decimate 순서**("order matters") | 예: image-to-3dlab `--faces 40000`. 텍스처를 다시 입힐 예정이면 그 전에 줄여 둡니다(참고로 Hunyuan paint는 약 500k faces가 넘으면 멈춘다는 보고가 있음) |
| 3. 리토폴로지 | 캐릭터·조형물은 예를 들어 Quadriflow 리메시 후 Subdivision Surface, 게임 소품은 decimate나 전용 low-poly 모델(Tripo P1/P2, Meshy quad) | Rodin Gen-2.5는 Raw로 받은 뒤 직접 retopo |
| 4. UV | 새로 펼칩니다. 생성기 UV는 retopo를 거치면 깨집니다 | Meshy·Hunyuan 클라우드에도 UV 생성 기능이 있음 |
| 5. 텍스처 | **(a) master에서 bake**: color, metallic-roughness, normal. 또는 **(b) 깨끗한 메시에 텍스처만 다시 생성** | (b) TRELLIS.2 `Trellis2TexturingPipeline`, Meshy retexture(2k/4k/8k), Tencent TextureEdit + ModelTo3DUV, Tripo `texture_model`. ComfyUI Bake Texture From Voxel은 최대 8192 |
| 6. LOD·충돌 | LOD1 50%, LOD2 25%, convex hull collision | LOD가 8k tri 아래로 내려가면 UV 보존 제약 때문에 목표치에 못 미칠 수 있음 |
| 7. export | procedural 셰이더는 bake(glTF가 버리는 노드 감사), 텍스처 압축 | gltf-transform, gltfpack. 재인코딩으로 약 32MB → 5MB 미만(image-to-3dlab). TRELLIS.2 GLB는 알파가 있어도 OPAQUE로 나오므로 투명 재질은 blend mode를 직접 켜야 함 |
| 8. 검증 | Khronos glTF validator 오류 0, `scene_audit.py`, [review_views.py](../03_playbooks/scripts/README.md) 4방향 렌더를 AI에게 비평시키기, 엔진 import 테스트 | asset-studio는 validator 통과와 Godot 4.7.2 import를 확인함 |

- **예산만 바꿀 때는 다시 생성하지 마세요.** 최적화 단계만 다시 돌리면 됩니다. asset-studio는 `retry --from-stage blender`로 약 80초가 걸립니다.
- **[한국어 UI 주의]** bake용 노드를 스크립트로 구성할 때 `nodes['Principled BSDF']`처럼 이름으로 찾으면 한국어 UI의 "New Data" 번역 설정에 따라 깨질 수 있습니다. 노드는 `type`으로 찾게 하세요(이 저장소 스크립트도 그렇게 합니다. 자세한 내용은 [02 가이드](02_blender_mcp.md)).
- 재질·bake의 세부 규칙은 [05 텍스처링 가이드](05_texturing_materials.md), 전체 게이트는 [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md)과 [품질 체크리스트](../03_playbooks/04_quality_checklists.md)를 보세요.

### 7.2 QA 기준 수치

| 항목 | 기준 | 출처·비고 |
|---|---|---|
| 삼각형 예산 | 모바일 소품 3k~8k, 일반 게임 에셋 10k~50k, 기계 디테일 보존은 20k 이상 | asset-studio, Scenario(`faceBudget` 10k~50k) |
| asset-studio 스타일 프리셋 (tri / 텍스처) | mobile_factory 20k/2048, stylized_generic 30k/2048, realistic 40k/2048, lowpoly 6k/1024 | [asset-studio](https://github.com/zorrobyte/asset-studio) |
| 감량 결과 예시 | crate 954,901 → 7,998 tri(오차 1.4%, 소요 11.1분), pump 997,520 → 19,803 tri(오차 2.3%, 소요 15.6분). RTX 5090 1장 | asset-studio README(개인 프로젝트 보고) |
| 형상 무결성 | 열린 경계 0, 비다양체 에지 0 (6.2절 `basic_cleanup` 보고값) | 콜리전, boolean, 3D 프린트, 조형물 제작용이면 필수. 렌더 전용이면 눈에 띄는 구멍만 없으면 됨 |
| 스케일·트랜스폼 | 1 unit = 1 m, 트랜스폼 적용, 원점은 바닥 중앙 | `scene_audit.py` 규약 |
| glTF | Khronos validator 오류 0 | asset-studio |
| 텍스처 | 프리셋 기준 2048(lowpoly 1024), master 4096. 투명 재질은 blend mode 확인 | 위 프리셋 |

> **인용 주의**: "TRELLIS.2 출력의 91.1%가 non-watertight, 14.9%가 non-manifold"라는 수치가 돌아다닙니다. 이 수치는 수리 도구 벤더(Topoheal)가 올린 초기 측정치(TRELLIS.2 표본 n=101)이고, 원저자가 2026-09-01 **철회**했습니다. 인용하지 마세요. 해당 벤더의 `3dqa` 패키지는 오픈소스가 아니라 source-available·재배포 금지 라이선스입니다([PyPI](https://pypi.org/project/3dqa/)). 자체 검사는 6.2절 코드와 `scene_audit.py`로 충분합니다.

---

## 8. 비용 레버

| 레버 | 방법 | 효과 (근거) |
|---|---|---|
| **형태 먼저, 텍스처는 나중** | Scenario `texture: false`로 bare mesh만 받기. Meshy는 mesh만 20 credits로 형태를 확정한 뒤 retexture | 텍스처와 8K 옵션이 비용의 대부분입니다. 형태가 틀리면 텍스처 비용이 통째로 버려집니다 |
| **싼 티어로 탐색** | Rodin Gen-2.5 Medium(0.5 credit)으로 후보를 뽑고, 최종본만 Extreme-High(1.0) + HighPack(+1, 4K) | 최종본 1회에 2 credit(직접 구매 단가 $1.5를 적용하면 약 $3, 추정) |
| **저비용 모델 활용** | Meshy smart-topology t2는 mesh 5 credits, meshy-5는 5/15 | 게임용 저폴리에 적합 |
| **seed 분리** | `seed`와 `textureSeed`(Tripo는 `texture_seed`)를 따로 고정 | 형태를 고정한 채 텍스처만 바꿔 볼 수 있음 |
| **재실행 금지** | 타임아웃이 나면 job id로 조회만 합니다. Sparc3D/Hitem3D는 중앙값 17~21분이라 "never re-run the job" 규칙이 필요 | credit이 두 번 나가는 것을 막음 |
| **버전 고정** | Tripo `model_version='v3.1-20260211'` 또는 `'P1-20260311'`, Meshy `ai_model='meshy-7'` | 구버전 기본값(Tripo SDK v2.5)으로 생성해 돈을 버리는 일을 막음 |
| **최적화 단계만 재실행** | 삼각형 예산을 바꿀 때 재생성 대신 decimate·bake만 | asset-studio 약 80초 |
| **승인 게이트** | 레퍼런스 이미지와 멀티뷰를 사람이 승인한 뒤에만 유료 호출. pass/fail 기준을 생성 전에 적음("a result is scored, not admired") | 잘못된 레퍼런스로 유료 생성을 반복하는 것이 가장 큰 낭비 |
| **로컬로 탐색** | TRELLIS.2/Pixal3D로 형태를 탐색하고, 최종본만 상업권이 있는 유료 SaaS로 | GPU만 있으면 추가 비용 없음(상업 납품은 9장 참고) |
| **최종본은 유료 플랜에서** | 무료 플랜 결과물은 라이선스가 다릅니다. 나중에 유료로 바꿔도 과거 무료 출력물의 조건은 바뀌지 않을 수 있음 | 프로토타입은 무료로, 출시 에셋은 유료 플랜에서 다시 생성 |

---

## 9. 상업 파이프라인 함정

| 함정 | 무엇이 문제인가 | 대응 |
|---|---|---|
| **Hunyuan 오픈웨이트 (한국)** | Territory에서 한국 제외. 출력물도 Territory 밖 사용 금지(5(c)), 호스팅 서비스 경유 출력도 Output에 포함, 출력물로 다른 AI 모델 개선 금지(5(b)). MAU 100만 조항은 **각 버전 출시일(2.0은 2025-01-21, 2.1은 2025-06-13) 기준 직전 달 MAU를 한 번 보는 조건**입니다 | 로컬 가중치, 서드파티 호스팅 2.x API, ahujasid 로컬 모드, blender-kiln 같은 파이프라인의 Hunyuan 기본값을 모두 끄고 다른 생성기로 바꾸세요 |
| **TRELLIS.2의 숨은 의존성** | 코드는 MIT지만 텍스처링(`trellis2_texturing.py`)과 GLB 후처리(`o_voxel/postprocess.py`)가 **nvdiffrast**를 import합니다. nvdiffrast·nvdiffrec의 NVIDIA Source Code License 3.3항은 "non-commercially(research or evaluation purposes only)"입니다([nvdiffrast LICENSE](https://github.com/NVlabs/nvdiffrast/blob/main/LICENSE.txt)). 이미지 인코더 `facebook/dinov3-vitl16`은 Meta DINOv3 License를 따릅니다 | 상업 납품 전에 nvdiffrast를 대체할 경로가 있는지, NVIDIA 상업 라이선스가 필요한지, DINOv3 약관을 검토하세요. Pixal3D도 TRELLIS.2 backbone과 DINOv3를 쓰므로 같은 검토가 필요합니다(Pixal3D의 nvdiffrast 사용 여부는 미확인) |
| **배경 제거기 RMBG-2.0** | TRELLIS.2·Pixal3D 파이프라인의 기본 matting 가중치로 보고됨. gated·비상업 | 알파 PNG를 직접 넣거나 허용 라이선스 matting으로 교체 (5.4절) |
| **레퍼런스 이미지 모델** | Qwen-Image 2.1은 Research License, FLUX.2 Klein 9B는 비상업 | 상업이면 Qwen-Image-2512(Apache-2.0)처럼 라이선스를 확인한 모델을 쓰세요 |
| **연구 전용 모델** | Roblox Cube·CubePart(RAIL-MS 연구 전용), PartPacker(NVIDIA SCL 비상업), PhysX-Anything(S-Lab) | 아이디어와 레퍼런스용으로만. 출시 에셋 경로에 넣지 마세요 |
| **Stability Community License** | 연매출 100만 달러를 넘으면 Enterprise 라이선스 필요 | 매출 기준을 기록해 두세요 |
| **SaaS 무료 플랜** | Tripo Free는 비상업, Marble Free·Standard는 상업권 없음, Meshy Free는 CC BY 4.0(출처 표기), Rodin 무료·체험 키는 미확인 | 출시 에셋은 상업권이 있는 플랜에서 생성하고, 결제 영수증과 당시 약관 캡처를 보관 |
| **Tripo 상업권의 범위** | "구독이 활성화된 기간에 생성한 모델"에 적용 | 생성 날짜와 구독 기간을 provenance에 기록 |
| **Meshy 유료 소유권의 조건** | Community에 공개하면 비공개 소유 조건이 깨짐. 입력 이미지가 타인 권리를 침해하면 안 됨 | 에셋을 공개 갤러리에 올리지 말 것 |
| **Tencent Cloud 3.x·HY World 2.1 제품** | 한국 약관 미확인. 실명 인증 필요 | 원문을 확인하기 전에는 상업 프로젝트에서 제외 |
| **소유권 ≠ 저작권** | 미국 저작권청 Part 2 보고서(2025-01-29)와 한국 「생성형 AI 활용 저작물의 저작권 등록 안내서」(2025-06)는 모두 AI 생성분 자체는 보호하지 않고 **사람의 창작적 기여만** 보호합니다([US Copyright Office](https://www.copyright.gov/newsnet/2025/1060.html), [한국저작권위원회](https://www.copyright.or.kr/information-materials/publication/research-report/view.do?brdctsno=54253)) | 리토폴로지, 스컬팅 수정, 핸드페인팅, 배치 같은 사람의 기여를 버전 이력과 타임랩스로 남기세요 |
| **플랫폼 AI 공개 의무** | Steam(2026-01-16 개정: 게임에 포함된 pre-generated와 live-generated 콘텐츠 공개, 출시물에 쓰지 않은 구상용 콘셉트 아트는 면제), Sketchfab(2025-12-11부터 모든 AI 모델에 CreatedWithAI), Fab("Created with AI" 자가 신고) | 생성 에셋은 기본적으로 공개 대상으로 관리하세요. 자세한 내용은 [10 에셋·라이선스 가이드](10_assets_pipeline_licensing.md) |
| **런타임 생성 기능** | 한국 인공지능기본법(2026-01-22 시행, 표시 의무. 계도기간은 법적 유예가 아니라 행정 운영 방침), EU AI Act 제50조(2026-08-02 적용. 2026-12-02까지의 워터마크 유예는 그 전에 출시된 시스템에만 해당) | 게임이나 앱이 사용자에게 3D 생성 기능을 제공하면 결과물 표시를 설계하세요([10 가이드](10_assets_pipeline_licensing.md)) |

**provenance 기록 예시** (image-to-3dlab의 `.provenance.json` 방식):

```json
{
  "asset_id": "chair_012",
  "generator": "Tripo P1-20260311",
  "plan": "Professional (구독 활성 기간 내 생성)",
  "generated_at": "2026-09-10",
  "inputs": ["ref/chair_012_front.png (Qwen-Image-2512, Apache-2.0)"],
  "matting": "사용자 제작 알파 PNG",
  "license_notes": "상업 가능, 비공개",
  "human_edits": ["Blender 리토폴로지·UV 재작업", "좌판 쿠션 스컬팅", "패브릭 텍스처 핸드페인팅"],
  "disclosure": "Steam pre-generated"
}
```

---

## 10. 실제 사례에서 배운 것

| 사례 | 파이프라인 | 결과 | 신뢰도 |
|---|---|---|---|
| [zorrobyte/asset-studio](https://github.com/zorrobyte/asset-studio) (0BSD, 2026-09) | 프롬프트 재작성 → Qwen-Image-2512 Lightning → Pixal3D/TRELLIS.2(1024 또는 1536 cascade, 후보 2개) → Blender(meshoptimizer, 새 UV, bake, LOD 50/25%, convex hull) → Khronos validator. Claude Code MCP 제공 | 7장 수치 참고. Godot 4.7.2 import 확인 | 높음(README 수치 확인) |
| [Bingeljell/image-to-3dlab](https://github.com/Bingeljell/image-to-3dlab) | 같은 입력으로 로컬 백엔드 5종 비교 → voxel remesh→decimate → 텍스처 재압축 → `.provenance.json` | Pixal3D는 "Best results we have; one pass, no repaint needed". TRELLIS.2는 충실도가 가장 높지만 Mac에서 15~35분이 걸리고 플랫 아트에서 색이 틀림. Hunyuan MLX는 형상이 가장 깨끗하지만 한국·EU·영국은 라이선스 문제 | 중간(개인 테스트, 정성 비교) |
| [Scenario 보물상자 Worked Example](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-3d/SKILL.md) | recommend → 콘셉트 이미지 → image-to-3D 스키마 확인 → 비동기 실행 → display → download | 벤더와 무관한 표준 절차와 흔한 실수 목록 | 중간(벤더 문서) |
| [img2threejs](https://github.com/img2threejs/img2threejs) (Apache-2.0, 약 16.9k stars) | 메시 생성 대신 에이전트가 Three.js factory 코드를 작성. blockout부터 optimization까지 8단계마다 렌더와 레퍼런스를 비교하는 quality gate | 생성형 메시의 대안. 기계적인 검증은 Python이 맡고 모델 토큰은 시각 판단에만 씀 | 중간 |
| [elithril/blender-kiln](https://github.com/elithril/blender-kiln) (2026-08) | Claude Code 스킬 8단계(CONFIG→BRIEF→SOURCE→IMPORT→CLEANUP→TEXTURING→OPTIMIZE→EXPORT), glTF에서 사라지는 노드 감사 | **기본 소스가 Hunyuan3D 2.x라 한국에서는 소스를 바꿔야 함** | 중간 |
| rodin-via-blender, sketch-to-3d-codex, blender-ai-3d-setup | 4뷰 → Rodin → Quadriflow로 FRP 조형물 / 스케치 Design Lock → 승인 게이트 → Rodin / Gemini → Hitem3D → 교실 가구 배치 | 셋 다 커밋 1개짜리 저장소입니다. sketch-to-3d-codex는 README에 실제 생성을 테스트하지 않았다고 직접 적혀 있음 | **낮음. 아이디어 참고용** |

더 많은 사례와 "누가·어떻게·결과" 정리는 [사례 모음](../04_case_studies/01_case_studies.md)에 있습니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 구멍과 찌꺼기가 많은 메시(TRELLIS.2) | 배경이 있는 입력 | 알파 PNG를 넣으세요. Pixal3D는 알파가 없으면 자동으로 배경을 제거합니다 |
| 색이 크게 틀림 | 플랫·벡터 스타일 레퍼런스 | 사실적인 셰이딩으로 레퍼런스를 다시 만드세요 |
| 앞뒤가 뒤바뀐 형상 | 멀티뷰 순서 오류 | 모델별 순서(5.3절)를 지키고 스키마를 조회하세요 |
| 텍스처에 그림자·반사가 구워짐 | 조명이 강한 레퍼런스 | delight 옵션, 부드러운 조명 레퍼런스 |
| 크기가 엉뚱하거나 바닥 아래에 묻힘 | 생성기가 임의 스케일로 출력 | bbox/auto-size + 6.2절 정규화 + `scene_audit.py` |
| 생각보다 품질이 낮음(Tripo) | SDK 기본값 `v2.5-20250123`으로 생성 | `model_version` 명시 |
| 같은 작업에 credit이 두 번 나감 | 타임아웃 후 재제출 | job id로 조회만(`jobs_wait`, `poll_rodin_job_status`) |
| 결과 다운로드 실패 | Rodin 링크 10분 만료 | 완료 즉시 저장 |
| quad 면 수가 지정값보다 적음(Tripo) | quad는 150,000에서 잘림(ComfyUI 주석) | quad 예산은 그 이하로. P2 quad는 최대 25,000 |
| PBR 맵이 없음(Meshy, ComfyUI) | `enable_pbr` 기본 false | 켜세요 |
| 투명해야 할 부분이 불투명 | TRELLIS.2 GLB가 OPAQUE로 export | DCC에서 blend mode 설정 |
| 텍스처 단계가 멈춤 | 면 수가 너무 많음(Hunyuan paint 약 500k) | 텍스처 전에 decimate |
| ahujasid에서 Tripo가 안 됨 | 2026-09-25부터 Premium 전용 | Tripo SDK, ComfyUI, trident-mcp |
| glTF에서 재질이 사라짐 | Blender procedural 노드는 glTF로 export되지 않음 | bake 후 export(blender-kiln 방식) |
| LOD 목표치에 못 미침 | 8k tri 미만에서는 UV 보존 제약 | 목표를 조정하거나 UV seam을 줄이세요 |
| 한국어 UI에서 bake 스크립트가 깨짐 | 노드 이름 번역 | 노드를 `type`으로 찾기, New Data 번역 끄기 |
| "latest"가 endpoint마다 다름(Meshy) | image-to-3D에서는 7, text-to-3D에서는 다르게 해석될 수 있음 | `ai_model`을 명시 |

---

## 관련 문서

- [00 목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [01 AI 모델·클라이언트](01_ai_models_and_clients.md): 감독 역할을 맡을 LLM 고르기, effort 설정, 비용
- [02 Blender MCP](02_blender_mcp.md): ahujasid 생성 통합, Premium, 보안·텔레메트리, 포트 충돌
- [03 기타 DCC·CAD·엔진 MCP](03_other_mcp_dcc_cad_engines.md): 생성 에셋을 Unreal·Unity·Godot으로 가져가기
- [05 텍스처링·재질](05_texturing_materials.md): 재텍스처링, PBR 규칙, bake
- [06 라이팅·렌더·아트디렉션](06_lighting_rendering_art_direction.md): 생성 에셋을 "싸구려 CG"로 보이지 않게 하기
- [07 오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md): 생성과 코드 모델링 중 무엇을 고를지
- [08 배치·레이아웃](08_scene_layout_placement.md): 생성 에셋 배치, 충돌·부유 검사
- [09 에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 스킬
- [10 에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md): 라이선스·법규(한국 포함) 전체
- [11 학술 연구](11_research_papers.md): 파트 생성·레이아웃 연구
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [치수 기준표](../03_playbooks/05_reference_dimensions.md)
- [보조 스크립트](../03_playbooks/scripts/README.md)(`scene_audit.py`, `placement_utils.py`, `review_views.py`) · [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- `01_research/raw/05_ai-3d-generation.research.json`: 생성 모델·서비스·MCP 연동·노하우·사례 조사
- `01_research/raw/05_ai-3d-generation.verify.json`: 독립 검증. TRELLIS.2 최근 커밋 정정, 3DQA 수치 철회, Tripo P2 정정, tripo-mcp·rodin-api-mcp 방치, SAM 3D 32GB, PartPacker 비상업, RMBG-2.0 함정, ComfyUI 네이티브 지원 등 누락 항목
- `01_research/raw/G4_licensing_pricing.gap.json`: 가격·상업 조건·라이선스·법규 보완 조사
- `01_research/raw/G4_licensing_pricing.verify.json`: 보완 검증. TRELLIS.2 nvdiffrast 비상업 의존성, Hunyuan MAU 조항 해석, Tripo·Meshy 가격 정정, Rodin 전 플랜 상업권 미확인, EU 워터마크 유예 범위

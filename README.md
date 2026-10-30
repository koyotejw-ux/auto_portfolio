# Auto Portfolio Studio (자동화 포트폴리오 스튜디오)

> **Enterprise-Grade UX/UI Case Study Deck & 60fps Live Interactive Prototyping Hub**  
> 복잡한 도메인 지식을 정량적 데이터 시각화와 고해상도 12슬라이드 Behance 케이스 스터디, 그리고 60fps 라이브 인터랙티브 프로토타입으로 완성하는 포트폴리오 관리 허브입니다.

---

## 📁 디렉터리 아키텍처

```text
auto_portfolio/
├── index.html                    # 🌟 마스터 포트폴리오 스튜디오 허브 (전체 프로젝트 쇼케이스 대시보드)
├── style.css                     # 마스터 허브 모던 다크 럭셔리 스타일시트
├── README.md                     # 포트폴리오 아키텍처 및 자동화 가이드
│
├── smart_dca/                    # 📊 Project 01: 스마트 물타기 계산기 (Smart DCA Calculator)
│   ├── index.html                # 12슬라이드 Behance 프론트페이지 케이스 스터디 뷰어
│   ├── prototype.html            # 60fps 라이브 모바일 시뮬레이터 (반응형 높이 스케일링)
│   ├── style.css                 # 핀테크/퀀트 테마 스타일시트
│   ├── behance_slides/           # 1920x1080 고해상도 슬라이드 01 ~ 12
│   ├── iphone_mockups/           # 티타늄 아이폰 플래그십 실물 목업
│   ├── app/                      # 실제 인터랙티브 웹 앱 엔진
│   └── Smart_DCA_Portfolio.pdf   # 12슬라이드 통합 고해상도 PDF
│
└── ftmt/                         # 🔮 Project 02: 포춘매치 (FortuneMatch)
    ├── index.html                # 12슬라이드 Behance 프론트페이지 케이스 스터디 뷰어 (코스믹 럭셔리)
    ├── prototype.html            # 60fps 라이브 모바일 시뮬레이터 (44px 스테이터스 바 & 오토 리사이징)
    ├── style.css                 # 코스믹 럭셔리 (Obsidian/Gold/Aurora Violet) 스타일시트
    ├── behance_slides/           # 1920x1080 고해상도 슬라이드 01 ~ 12
    ├── build_ftmt_mockups.py     # 실물 기기 스크린샷 기반 아이폰 목업 자동 생성기
    ├── generate_ftmt_slides.py   # 12슬라이드 Python Pillow 고해상도 자동 생성기
    ├── assets/                   # 원본 스크린샷, 앱 아이콘, 타로 카드 자산
    └── app/                      # 실제 인터랙티브 웹 앱 엔진
```

---

## 🚀 로컬 실행 방법

포트폴리오 스튜디오는 표준 정적 웹 규격으로 구축되어 있어, 로컬 웹 서버(예: Python `http.server` 또는 VS Code Live Server)로 즉시 구동 가능합니다.

```bash
# auto_portfolio 디렉터리에서 로컬 서버 실행 (포트 8080)
cd d:\097.flutter_project\auto_portfolio
python -m http.server 8080
```

- **마스터 허브**: `http://localhost:8080/index.html`
- **스마트 물타기 계산기 케이스 스터디**: `http://localhost:8080/smart_dca/index.html`
- **스마트 물타기 계산기 60fps 프로토타입**: `http://localhost:8080/smart_dca/prototype.html`
- **포춘매치 케이스 스터디**: `http://localhost:8080/ftmt/index.html`
- **포춘매치 60fps 프로토타입**: `http://localhost:8080/ftmt/prototype.html`

---

## 🎨 새로운 앱 포트폴리오 추가 가이드 (Extending to New Apps)

새로운 Flutter 앱(예: `Pingo`, `TalkClear`, `Vent & Burn Diary` 등)에 대한 포트폴리오를 추가하려면:

1. `auto_portfolio/<new_app>/` 폴더 생성
2. 앱의 원본 스크린샷을 `assets/raw/`에 복사
3. `build_mockups.py`를 실행하여 4개 코어 화면(Hub, Core Feature 1, Core Feature 2, Settings)을 티타늄 아이폰 목업으로 렌더링
4. `generate_slides.py`에서 앱의 브랜드 컬러와 12개 슬라이드 스토리(Overview -> Problem -> Persona -> IA -> Flow -> Wireframe -> Design System -> Deep Dive 1 & 2 -> UI Screens -> Retrospective -> Live Prototype) 구성 후 실행
5. `index.html`과 `prototype.html`을 복사하여 브랜드 테마와 4-Flow 탭 연결
6. 마스터 허브 `auto_portfolio/index.html`에 프로젝트 카드 추가

---

## 🏆 합격 기준 및 품질 표준 (Enterprise Standard Compliance)

- **100% UX/UI 중심**: 불필요한 개발 프레임워크 명칭 배제, 기획 의도와 디자인 시스템에 집중
- **정량적 비즈니스 검증**: D1 리텐션, 체류 시간, 전환율 등 측정 지표 및 200자 이상의 STAR 기법 회고 수록
- **반응형 60fps 프로토타입**: 브라우저 창 높이에 따라 자동으로 축소/확대되어 상하 잘림이 없는 반응형 목업 뷰어 탑재

import 'dart:convert';
import 'package:flutter/material.dart';

enum ElementType {
  header,
  text,
  statCard,
  barChart,
  donutChart,
  flowchart,
  designTokens,
  mockupPlaceholder,
  personaMatrix,
  kpiStrip,
  shape,
}

class DeckTextStyle {
  String fontFamily;
  double fontSize;
  FontWeight fontWeight;
  Color color;
  double letterSpacing;
  double height;
  double wordSpacing;

  DeckTextStyle({
    this.fontFamily = 'Pretendard',
    this.fontSize = 16.0,
    this.fontWeight = FontWeight.normal,
    this.color = const Color(0xFF0F172A),
    this.letterSpacing = 0.0,
    this.height = 1.4,
    this.wordSpacing = 0.0,
  });

  TextStyle toTextStyle() {
    return TextStyle(
      fontFamily: fontFamily,
      fontSize: fontSize,
      fontWeight: fontWeight,
      color: color,
      letterSpacing: letterSpacing,
      height: height,
      wordSpacing: wordSpacing,
    );
  }

  Map<String, dynamic> toJson() => {
        'fontFamily': fontFamily,
        'fontSize': fontSize,
        'fontWeight': fontWeight.index,
        'color': color.toARGB32(),
        'letterSpacing': letterSpacing,
        'height': height,
        'wordSpacing': wordSpacing,
      };

  factory DeckTextStyle.fromJson(Map<String, dynamic> json) {
    return DeckTextStyle(
      fontFamily: json['fontFamily'] ?? 'Pretendard',
      fontSize: (json['fontSize'] as num?)?.toDouble() ?? 16.0,
      fontWeight: FontWeight.values[(json['fontWeight'] as int?) ?? 3],
      color: Color((json['color'] as int?) ?? 0xFF0F172A),
      letterSpacing: (json['letterSpacing'] as num?)?.toDouble() ?? 0.0,
      height: (json['height'] as num?)?.toDouble() ?? 1.4,
      wordSpacing: (json['wordSpacing'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

class DeckElement {
  String id;
  ElementType type;
  String name;
  double x;
  double y;
  double width;
  double height;
  DeckTextStyle textStyle;
  Map<String, dynamic> props;

  DeckElement({
    required this.id,
    required this.type,
    required this.name,
    required this.x,
    required this.y,
    required this.width,
    required this.height,
    DeckTextStyle? textStyle,
    required this.props,
  }) : textStyle = textStyle ?? DeckTextStyle();

  Map<String, dynamic> toJson() => {
        'id': id,
        'type': type.name,
        'name': name,
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'textStyle': textStyle.toJson(),
        'props': props,
      };

  factory DeckElement.fromJson(Map<String, dynamic> json) {
    return DeckElement(
      id: json['id'],
      type: ElementType.values.firstWhere(
        (e) => e.name == json['type'],
        orElse: () => ElementType.text,
      ),
      name: json['name'] ?? 'Element',
      x: (json['x'] as num).toDouble(),
      y: (json['y'] as num).toDouble(),
      width: (json['width'] as num).toDouble(),
      height: (json['height'] as num).toDouble(),
      textStyle: json['textStyle'] != null
          ? DeckTextStyle.fromJson(json['textStyle'])
          : DeckTextStyle(),
      props: Map<String, dynamic>.from(json['props'] ?? {}),
    );
  }
}

class DeckSlide {
  String id;
  String title;
  int pageNumber;
  Color backgroundColor;
  List<DeckElement> elements;

  DeckSlide({
    required this.id,
    required this.title,
    required this.pageNumber,
    this.backgroundColor = const Color(0xFFF8FAFC),
    List<DeckElement>? elements,
  }) : elements = elements ?? [];

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'pageNumber': pageNumber,
        'backgroundColor': backgroundColor.toARGB32(),
        'elements': elements.map((e) => e.toJson()).toList(),
      };

  factory DeckSlide.fromJson(Map<String, dynamic> json) {
    return DeckSlide(
      id: json['id'],
      title: json['title'] ?? 'Slide',
      pageNumber: json['pageNumber'] ?? 1,
      backgroundColor: Color(json['backgroundColor'] ?? 0xFFF8FAFC),
      elements: (json['elements'] as List? ?? [])
          .map((e) => DeckElement.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
    );
  }
}

class PortfolioProject {
  String title;
  String author;
  List<DeckSlide> slides;

  PortfolioProject({
    required this.title,
    required this.author,
    List<DeckSlide>? slides,
  }) : slides = slides ?? [];

  String toJsonString() {
    return jsonEncode({
      'title': title,
      'author': author,
      'slides': slides.map((s) => s.toJson()).toList(),
    });
  }

  factory PortfolioProject.fromJsonString(String str) {
    final map = jsonDecode(str);
    return PortfolioProject(
      title: map['title'] ?? 'Portfolio',
      author: map['author'] ?? 'Designer',
      slides: (map['slides'] as List? ?? [])
          .map((s) => DeckSlide.fromJson(Map<String, dynamic>.from(s)))
          .toList(),
    );
  }

  /// 12대 전체 엔터프라이즈 포트폴리오 섹션 템플릿 완벽 탑재
  static PortfolioProject createDefaultTemplate() {
    final proj = PortfolioProject(
      title: 'ZeroPass Enterprise UX Case Study',
      author: 'Senior Product Designer',
    );

    // 01. Hero Cover
    proj.slides.add(DeckSlide(
      id: 'slide_1',
      title: '01. Hero Cover & Value Proposition',
      pageNumber: 1,
      backgroundColor: const Color(0xFFFAFCFF),
      elements: [
        DeckElement(
          id: 's1_header',
          type: ElementType.header,
          name: '헤더 인디케이터',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          textStyle: DeckTextStyle(fontSize: 13, fontWeight: FontWeight.w600, letterSpacing: -0.2),
          props: {
            'badge': '2026 CASE STUDY',
            'meta': '서비스 기획 · UI/UX 디자인 · Android Live · Smart Attendance System',
          },
        ),
        DeckElement(
          id: 's1_hero_text',
          type: ElementType.text,
          name: '메인 헤드라인',
          x: 100,
          y: 160,
          width: 820,
          height: 220,
          textStyle: DeckTextStyle(fontSize: 32, fontWeight: FontWeight.w900, letterSpacing: -1.0, height: 1.25),
          props: {
            'category': '체크앤페이 · CHECK & PAY',
            'titleBlack': '1초 원터치 출결, ',
            'titleBlue': '완벽한 수납 자동화.',
            'subtitle': '학원·교습소 원장님의 반복되는 출결 체크와 미수금 스트레스를\n단 한 번의 터치와 오프라인 안심 저장으로 해결하는 모바일 솔루션',
          },
        ),
        DeckElement(
          id: 's1_flowchart',
          type: ElementType.flowchart,
          name: '4대 핵심 기능 리스트',
          x: 100,
          y: 360,
          width: 780,
          height: 440,
          props: {
            'items': [
              {'num': '01', 'tag': '출결 마찰 제로', 'title': '1초 원터치 키오스크 UI', 'desc': '번호 뒤 4자리 터치 즉시 0.8초 등하원 인증 및 대기 줄 완전 제거'},
              {'num': '02', 'tag': '수납 누수 차단', 'title': '스마트 D-Day 수납 장부', 'desc': '정기 결제일과 잔여 회차 기반 만료 7일 전 3단계 색상 직관 분류'},
              {'num': '03', 'tag': '감정 소모 해소', 'title': '원클릭 모바일 청구서', 'desc': '계좌번호 및 청구 금액이 자동 치환된 정중한 카톡 청구서 즉시 발송'},
              {'num': '04', 'tag': '안심 프라이버시', 'title': '100% 로컬 오프라인 볼트', 'desc': '서버 없이 기기 내부 로컬 암호화 보관으로 월 유지비 0원 및 프라이버시 완결'},
            ]
          },
        ),
        DeckElement(
          id: 's1_mockup',
          type: ElementType.mockupPlaceholder,
          name: '3D 스마트폰 목업 & 캐릭터',
          x: 960,
          y: 140,
          width: 860,
          height: 660,
          props: {
            'mockupType': 'phone_3d',
            'imagePath': 'zeropass/assets/iphone_mockups/clean_android_upright_mockup.png',
            'mascotPath': 'zeropass/assets/mascot_poses/passy_active_jump_wink_3d.png',
            'screenTitle': '체크앤페이 출결 체크',
            'showMascot': true,
          },
        ),
        DeckElement(
          id: 's1_kpi_strip',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '담당 역할', 'val': '서비스 기획 100% · UI/UX 100%', 'sub': '소상공인 리서치, IA, 와이어프레임, UI 디자인'},
              {'title': '진행 기간', 'val': '2026.08 - 현재 (v1.0 상용)', 'sub': '실제 현장 인터뷰 기반 설계 및 라이브 고도화'},
              {'title': '디자인 시스템', 'val': '신뢰 기반 토큰 & 컴포넌트', 'sub': '8pt 그리드, Electric Blue, 라이트 고대비 12.8:1'},
              {'title': '출시 및 배포', 'val': 'Android 상용 출시 & 60fps 프로토타입', 'sub': '안심 로컬 보관 아키텍처 탑재'},
            ]
          },
        ),
      ],
    ));

    // 02. Problem Study & Market Research
    proj.slides.add(DeckSlide(
      id: 'slide_2',
      title: '02. Market Research & Pain Point Analysis',
      pageNumber: 2,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's2_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '02 PROBLEM STUDY & RESEARCH',
            'meta': 'Market Gap Analysis · Stakeholder Interview Matrix',
          },
        ),
        DeckElement(
          id: 's2_title',
          type: ElementType.text,
          name: '연구 배경 및 핵심 페인포인트',
          x: 100,
          y: 150,
          width: 1000,
          height: 130,
          props: {
            'titleBlack': '학원 원장님의 ',
            'titleBlue': '숨겨진 3대 운영 비효율성',
            'subtitle': '매일 반복되는 출결 태그 지연, 미수금 독촉에 따른 학부모 감정 마찰,\n월 5~10만원에 달하는 고정 SaaS 비용 문제를 분석했습니다.',
          },
        ),
        DeckElement(
          id: 's2_flowchart',
          type: ElementType.flowchart,
          name: '3대 페인포인트 비교 카드',
          x: 100,
          y: 300,
          width: 1720,
          height: 500,
          props: {
            'items': [
              {'num': 'PAIN 01', 'tag': '출결 병목', 'title': '카드 분실 및 등원 태그 대기열 (평균 45초 소요)', 'desc': '바쁜 등교/등원 시간대 원생들이 카드를 찾지 못해 입구에서 긴 대기열 발생'},
              {'num': 'PAIN 02', 'tag': '미수금 누수', 'title': '수기 장부와 결제일 불일치로 인한 회수 지연', 'desc': '회차권과 월정액이 혼재되어 언제 청구해야 할지 실시간 파악이 불가능'},
              {'num': 'PAIN 03', 'tag': '비용 부담', 'title': '월정액 클라우드 SaaS 비용 및 외부 서버 보안 불안', 'desc': '영세 학원에 부담스러운 고정 비용과 학생 개인정보 외부 유출 우려'},
            ]
          },
        ),
      ],
    ));

    // 03. Target & Persona Matrix
    proj.slides.add(DeckSlide(
      id: 'slide_3',
      title: '03. Target & Persona Matrix',
      pageNumber: 3,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's3_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '03 TARGET & PERSONA ARCHITECTURE',
            'meta': 'Primary User Archetypes & Needs Alignment',
          },
        ),
        DeckElement(
          id: 's3_persona',
          type: ElementType.personaMatrix,
          name: '원장님 & 학부모 페르소나 매트릭스',
          x: 100,
          y: 160,
          width: 1720,
          height: 640,
          props: {
            'personas': [
              {
                'role': '원장님 (김선영, 42세)',
                'tag': '1인 피아노 학원 운영 8년차',
                'needs': '강의 도중 수납 장부 정리 시간을 줄이고, 학부모 대면 미수금 독촉을 스마트하게 해결하고 싶음.',
                'solution': '1초 키오스크 무인 출결 & 카카오 알림톡 원클릭 청구서',
              },
              {
                'role': '학부모 (이지은, 38세)',
                'tag': '초등 2학년 학부모',
                'needs': '아이가 학원에 안전하게 도착했는지 실시간으로 확인하고, 수업료 결제를 카톡으로 편리하게 처리하고 싶음.',
                'solution': '0.8초 등원 안심 알림톡 & 계좌번호 자동 치환 모바일 청구서',
              },
            ]
          },
        ),
      ],
    ));

    // 04. Information Architecture (IA)
    proj.slides.add(DeckSlide(
      id: 'slide_4',
      title: '04. Information Architecture (IA)',
      pageNumber: 4,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's4_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '04 INFORMATION ARCHITECTURE | DEPTH HIERARCHY',
            'meta': 'Complete Structural Sitemap & Data Flow',
          },
        ),
        DeckElement(
          id: 's4_ia_tree',
          type: ElementType.flowchart,
          name: '4대 메인 트리 구조',
          x: 100,
          y: 200,
          width: 1720,
          height: 600,
          props: {
            'items': [
              {'num': 'TAB 1', 'tag': '출결 체크', 'title': '1초 출결 대시보드 / 태블릿 키오스크 연동', 'desc': '실시간 출석 인원 카운터, 미출석 안심 케어, 원터치 체크인'},
              {'num': 'TAB 2', 'tag': '청구·수납', 'title': 'D-Day 스마트 수납 장부 & 위험도 분류', 'desc': '만료 임박 알림톡, 미납 순차 발송, 카톡 모바일 청구서'},
              {'num': 'TAB 3', 'tag': '회원 관리', 'title': '원생 프로필 & 회차권/월정액 내역 관리', 'desc': '잔여 회차 충전, 수강 이력 트래킹, 보호자 연락처 연동'},
              {'num': 'TAB 4', 'tag': '보안 볼트', 'title': '100% 로컬 SQLite 데이터 백업 및 복원', 'desc': '기기 내부 로컬 암호화, 오프라인 무결성 보장, 엑셀 내보내기'},
            ]
          },
        ),
      ],
    ));

    // 05. User Flow & Task Flow
    proj.slides.add(DeckSlide(
      id: 'slide_5',
      title: '05. 5-Stage Interactive User Flowchart',
      pageNumber: 5,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's5_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '05 USER FLOW & UX FLOWCHART | TASK ARCHITECTURE',
            'meta': '5-Stage Full Lifecycle Architecture',
          },
        ),
        DeckElement(
          id: 's5_flowchart',
          type: ElementType.flowchart,
          name: '5단계 서비스 핵심 플로우',
          x: 100,
          y: 200,
          width: 1720,
          height: 600,
          props: {
            'items': [
              {'num': '01단계', 'tag': '인증', 'title': '키오스크 등원 인증', 'desc': '원생 번호 뒤 4자리 터치 즉시 0.8초 고속 출결'},
              {'num': '02단계', 'tag': '차감', 'title': '출결 데이터 자동 차감', 'desc': '잔여 회차 및 출석 일자 로컬 DB 즉시 갱신'},
              {'num': '03단계', 'tag': '분류', 'title': '수납 장부 D-Day 정렬', 'desc': '만료 7일 전부터 3단계 색상 위험도 자동 분류'},
              {'num': '04단계', 'tag': '발송', 'title': '원클릭 청구서 발송', 'desc': '정중한 카카오톡 알림톡 템플릿 즉시 전송'},
              {'num': '05단계', 'tag': '보존', 'title': '보안 볼트 & 백업', 'desc': '기기 내부 안전 암호화 보관 및 월 유지비 0원'},
            ]
          },
        ),
      ],
    ));

    // 06. Wireframe & Ergonomics
    proj.slides.add(DeckSlide(
      id: 'slide_6',
      title: '06. Wireframe & Ergonomics',
      pageNumber: 6,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's6_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '06 WIREFRAME & ERGONOMICS | THUMB-ZONE ARCHITECTURE',
            'meta': 'High-Fidelity Wireframes & Reachability Heatmap',
          },
        ),
        DeckElement(
          id: 's6_mockup',
          type: ElementType.mockupPlaceholder,
          name: '4단 와이어프레임 & 엄지 영역 도식',
          x: 100,
          y: 180,
          width: 1720,
          height: 620,
          props: {
            'screenTitle': '체크앤페이 와이어프레임 & 썸존 설계',
            'showMascot': false,
          },
        ),
      ],
    ));

    // 07. Visual Design System
    proj.slides.add(DeckSlide(
      id: 'slide_7',
      title: '07. Visual Design System & Brand Tokens',
      pageNumber: 7,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's7_header',
          type: ElementType.header,
          name: '디자인 시스템 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '07 VISUAL DESIGN SYSTEM & BRAND TOKENS',
            'meta': 'Design Foundations · Keyline Drafting · 24dp Iconography · Component Tokens',
          },
        ),
        DeckElement(
          id: 's7_tokens',
          type: ElementType.designTokens,
          name: '컬러 팔레트 및 타이포그래피 토큰',
          x: 100,
          y: 150,
          width: 820,
          height: 660,
          props: {
            'colors': [
              {'name': 'Brand Electric Blue', 'hex': '#0052FF', 'role': 'Primary Action & Hero Accent'},
              {'name': 'Cyan Accent', 'hex': '#06B6D4', 'role': 'Secondary Glow & Active States'},
              {'name': 'Obsidian Dark', 'hex': '#0F172A', 'role': 'Title Black & Kiosk Surface'},
              {'name': 'Success Emerald', 'hex': '#10B981', 'role': 'Attendance Success & Verified'},
              {'name': 'Warning Amber', 'hex': '#F59E0B', 'role': 'D-Day Expiring Soon Alert'},
              {'name': 'Pure White Clean', 'hex': '#FFFFFF', 'role': 'Card Surface & Elevated Light'},
            ],
            'typography': [
              {'level': 'Hero Display', 'size': '56px Black', 'sample': '1초 원터치 출결'},
              {'level': 'Section Title', 'size': '32px ExtraBold', 'sample': '스마트 D-Day 수납 장부'},
              {'level': 'Card Headline', 'size': '18px Bold', 'sample': '출결 마찰 제로 키오스크'},
              {'level': 'Body Regular', 'size': '14px Regular', 'sample': '단 한 번의 터치로 완결되는 경험'},
            ]
          },
        ),
        DeckElement(
          id: 's7_charts',
          type: ElementType.donutChart,
          name: '컴포넌트 완성도 & 도넛 차트',
          x: 960,
          y: 150,
          width: 860,
          height: 660,
          props: {
            'title': '디자인 시스템 토큰 규격 준수율',
            'percentage': 98.4,
            'stat1': '24dp 아이콘 64종',
            'stat2': 'WCAG AAA 12.8:1 고대비',
            'stat3': '8pt 그리드 100% 준수',
          },
        ),
      ],
    ));

    // 08. Tablet Kiosk Attendance & Mobile Sync
    proj.slides.add(DeckSlide(
      id: 'slide_8',
      title: '08. Tablet Kiosk Attendance & Mobile Sync',
      pageNumber: 8,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's8_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '08 CORE FEATURE | 0.8S TABLET KIOSK ATTENDANCE & MOBILE SYNC',
            'meta': 'Kiosk Engine & Real-Time Sync Interaction Architecture',
          },
        ),
        DeckElement(
          id: 's8_title',
          type: ElementType.text,
          name: '기능 타이틀 & 설명',
          x: 100,
          y: 114,
          width: 1200,
          height: 110,
          textStyle: DeckTextStyle(fontSize: 30, fontWeight: FontWeight.w900, letterSpacing: -0.8, height: 1.25),
          props: {
            'titleBlack': '원생 4자리 번호 터치부터 ',
            'titleBlue': '원장님 메인 출결 동기화까지,',
            'subtitle': '원생이 10인치 태블릿에서 입력하는 즉시 0.8초 초고속 인증과 회차 자동 차감이 완결되며\n원장님 모바일 출결 체크 화면의 카운터에 실시간 100% 무선 동기화되어 즉각 반영됩니다.',
          },
        ),
        DeckElement(
          id: 's8_flowchart',
          type: ElementType.flowchart,
          name: '3단계 키오스크 프로세스 & 모바일 인터랙션',
          x: 100,
          y: 244,
          width: 1720,
          height: 570,
          props: {
            'isKioskCarousel': true,
            'stages': [
              {
                'step': 'STEP 01',
                'badge': '무인 대기 모드',
                'title': '대기 및 진입 (Standby Engine)',
                'sub': '원생 진입 감지 & 실시간 디지털 클록 연동',
                'features': ['옵시디언 다크 테마 시인성 100%', '스튜디오 브랜드 & 실시간 시계 연동', '10인치 태블릿 가로/세로 반응형'],
                'interaction': '진입 대기: 4자리 입력 박스가 Clear 상태로 원생 터치 대기'
              },
              {
                'step': 'STEP 02',
                'badge': '고속 햅틱 입력',
                'title': '인체공학 터치 다이얼 (Dialing)',
                'sub': '116dp 대형 텐키패드 & 10ms 고속 트리거',
                'features': ['116dp 대형 그리드로 오터치 원천 차단', '네온 글로우 햅틱 피드백 즉각 반응', '4자리 입력 즉시 로컬 인덱스 매칭'],
                'interaction': '입력 파이프라인: 4자리 터치 완료 시 10ms 내 로컬 원생 식별 가동'
              },
              {
                'step': 'STEP 03',
                'badge': '출결 및 차감 완결',
                'title': '0.8초 완결 & 메인 동기화 (Sync)',
                'sub': '원생 식별 · 잔여 회차 즉시 차감 · 모바일 실시간 반영',
                'features': ['강지훈 원생 즉각 식별 및 잔여 회차 차감', '학부모 안심 알림톡 백그라운드 발송', '원장님 모바일 출결 체크 헤더 카운터 자동 갱신'],
                'interaction': '상태 인터랙션: 태블릿 완료 즉시 모바일 메인 카운터 +1 반영'
              },
            ]
          },
        ),
        DeckElement(
          id: 's8_kpis',
          type: ElementType.kpiStrip,
          name: '실시간 측정 성능 지표 스트립',
          x: 100,
          y: 832,
          width: 1720,
          height: 140,
          props: {
            'header': '키오스크 출결 엔진 & 메인 동기화 실측 지표',
            'items': [
              {'title': '출결 완결 속도', 'val': '0.8초', 'sub': '기존 45초 대비 98% 단축'},
              {'title': '메인 실시간 동기화', 'val': '< 10ms', 'sub': '로컬 이벤트 버스 즉각 반영'},
              {'title': '오프라인 보존율', 'val': '100%', 'sub': '무손실 SQLite 볼트 저장'},
              {'title': 'UI 렌더링 무지연', 'val': '60 fps', 'sub': 'Flutter 프레임 드랍 0%'},
            ]
          },
        ),
      ],
    ));

    // 09. Smart D-Day Billing Ledger
    proj.slides.add(DeckSlide(
      id: 'slide_9',
      title: '09. Smart D-Day Billing Ledger',
      pageNumber: 9,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's9_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '09 CORE FEATURE | SMART D-DAY BILLING LEDGER',
            'meta': 'Automated Ledger Priority & Mobile Billing Invoice',
          },
        ),
        DeckElement(
          id: 's9_mockup',
          type: ElementType.mockupPlaceholder,
          name: '수납 장부 목업 화면',
          x: 960,
          y: 160,
          width: 860,
          height: 640,
          props: {
            'screenTitle': '스마트 D-Day 청구·수납 장부',
            'showMascot': true,
          },
        ),
      ],
    ));

    // 10. Mobile Screens (Figma & Flutter)
    proj.slides.add(DeckSlide(
      id: 'slide_10',
      title: '10. Mobile Production Screens (Figma & Flutter)',
      pageNumber: 10,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's10_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '10 PRODUCTION SCREENS | FIGMA & FLUTTER IMPLEMENTATION',
            'meta': '6 Core Mobile App Views · Pixel-Perfect 8pt Grid',
          },
        ),
        DeckElement(
          id: 's10_screens',
          type: ElementType.mockupPlaceholder,
          name: '6종 모바일 화면 그리드',
          x: 100,
          y: 180,
          width: 1720,
          height: 620,
          props: {
            'screenTitle': '체크앤페이 6대 모바일 핵심 뷰',
            'showMascot': false,
          },
        ),
      ],
    ));

    // 11. Business Impact & Retrospective
    proj.slides.add(DeckSlide(
      id: 'slide_11',
      title: '11. Business Impact & Retrospective (STAR)',
      pageNumber: 11,
      backgroundColor: const Color(0xFFF8FAFC),
      elements: [
        DeckElement(
          id: 's11_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '11 BUSINESS IMPACT & STRATEGIC RETROSPECTIVE',
            'meta': 'Quantitative Results · STAR Methodology Evaluation',
          },
        ),
        DeckElement(
          id: 's11_kpis',
          type: ElementType.kpiStrip,
          name: '비즈니스 정량 지표',
          x: 100,
          y: 160,
          width: 1720,
          height: 140,
          props: {
            'header': '체크앤페이 런칭 후 핵심 운영 성과',
            'items': [
              {'title': '출결 대기 시간', 'val': '-98%', 'sub': '45초 -> 0.8초 단축'},
              {'title': '미수금 회수율', 'val': '99.4%', 'sub': '수납 누수 완전 차단'},
              {'title': '월 운영비 절감', 'val': '0원', 'sub': '외부 유료 서버 탈피'},
              {'title': '원장 만족도', 'val': '4.9 / 5.0', 'sub': '대면 독촉 스트레스 해소'},
            ]
          },
        ),
        DeckElement(
          id: 's11_star',
          type: ElementType.flowchart,
          name: 'STAR 방법론 기반 회고',
          x: 100,
          y: 330,
          width: 1720,
          height: 480,
          props: {
            'items': [
              {'num': 'S', 'tag': 'Situation', 'title': '소상공인 학원 운영의 비효율과 미수금 스트레스', 'desc': '바쁜 강의 일정 중 출결 태그 지연과 학부모 수납 독촉으로 인한 감정 소모 심화'},
              {'num': 'T', 'tag': 'Task', 'title': '카드 없는 1초 출결과 D-Day 수납 자동화 시스템 설계', 'desc': '영세 학원도 월 고정비 부담 없이 안전하게 쓸 수 있는 로컬 온디바이스 아키텍처 수립'},
              {'num': 'A', 'tag': 'Action', 'title': '10인치 태블릿 키오스크 및 정중한 카톡 청구서 템플릿 구현', 'desc': '원생 4자리 다이얼 즉시 식별 알고리즘과 카카오톡 자동 치환 발송 체계 구축'},
              {'num': 'R', 'tag': 'Result', 'title': '출결 마찰 제로화 및 미수금 99.4% 회수, Play스토어 상용 배포', 'desc': '안정적인 60fps 프레임 유지와 소상공인 원장님들의 열렬한 호평 확보'},
            ]
          },
        ),
      ],
    ));

    // 12. Interactive Finale
    proj.slides.add(DeckSlide(
      id: 'slide_12',
      title: '12. Live Interactive Prototype & Obsidian Finale',
      pageNumber: 12,
      backgroundColor: const Color(0xFF0F172A),
      elements: [
        DeckElement(
          id: 's12_header',
          type: ElementType.header,
          name: '상단 헤더',
          x: 100,
          y: 70,
          width: 1720,
          height: 60,
          props: {
            'badge': '12 LIVE INTERACTIVE PROTOTYPE & EXPERIENCE HUB',
            'meta': 'Interactive Web Simulation · ZeroPass Obsidian Finale',
          },
        ),
        DeckElement(
          id: 's12_text',
          type: ElementType.text,
          name: '피날레 메시지',
          x: 100,
          y: 180,
          width: 1000,
          height: 200,
          textStyle: DeckTextStyle(fontSize: 34, fontWeight: FontWeight.w900, color: Colors.white, height: 1.3),
          props: {
            'titleBlack': '단순한 관리를 넘어, ',
            'titleBlue': '원장님의 일상에 온전한 여유를 드립니다.',
            'subtitle': '체크앤페이(ZeroPass)는 현장의 고충을 기술로 풀어낸 엔터프라이즈 포트폴리오입니다.',
          },
        ),
      ],
    ));

    return proj;
  }
}

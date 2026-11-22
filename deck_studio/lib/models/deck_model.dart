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
  double letterSpacing; // 자간 (Letter spacing)
  double height; // 행간 / 줄간격 (Line height multiplier)
  double wordSpacing; // 어간 (Word spacing)

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

  static PortfolioProject createDefaultTemplate() {
    final proj = PortfolioProject(
      title: 'ZeroPass Enterprise Case Study',
      author: 'UI/UX & Product Design',
    );

    // Slide 1: Hero Cover
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
          textStyle: DeckTextStyle(
            fontFamily: 'Pretendard',
            fontSize: 13,
            fontWeight: FontWeight.w600,
            letterSpacing: -0.2,
          ),
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
          textStyle: DeckTextStyle(
            fontFamily: 'Pretendard',
            fontSize: 32,
            fontWeight: FontWeight.w900,
            letterSpacing: -1.0,
            height: 1.25,
          ),
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
          textStyle: DeckTextStyle(
            fontFamily: 'Pretendard',
            fontSize: 13,
            fontWeight: FontWeight.bold,
            letterSpacing: -0.3,
            height: 1.4,
          ),
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
            'screenTitle': '체크앤페이 출결 체크',
            'showMascot': true,
            'mascotName': 'Passy (패시)',
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

    // Slide 2: Kiosk Attendance Engine
    proj.slides.add(DeckSlide(
      id: 'slide_2',
      title: '08. Tablet Kiosk Attendance & Mobile Sync',
      pageNumber: 8,
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
            'badge': '08 CORE FEATURE | 0.8S TABLET KIOSK ATTENDANCE & MOBILE SYNC',
            'meta': 'Kiosk Engine & Real-Time Sync Interaction Architecture',
          },
        ),
        DeckElement(
          id: 's2_title',
          type: ElementType.text,
          name: '기능 타이틀 & 설명',
          x: 100,
          y: 114,
          width: 1200,
          height: 110,
          textStyle: DeckTextStyle(
            fontFamily: 'Pretendard',
            fontSize: 30,
            fontWeight: FontWeight.w900,
            letterSpacing: -0.8,
            height: 1.25,
          ),
          props: {
            'titleBlack': '원생 4자리 번호 터치부터 ',
            'titleBlue': '원장님 메인 출결 동기화까지,',
            'subtitle': '원생이 10인치 태블릿에서 입력하는 즉시 0.8초 초고속 인증과 회차 자동 차감이 완결되며\n원장님 모바일 출결 체크 화면의 카운터에 실시간 100% 무선 동기화되어 즉각 반영됩니다.',
          },
        ),
        DeckElement(
          id: 's2_flowchart',
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
          id: 's2_kpis',
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

    return proj;
  }
}

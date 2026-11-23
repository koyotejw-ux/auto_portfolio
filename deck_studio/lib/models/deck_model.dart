import 'dart:convert';
import 'package:flutter/material.dart';

enum ElementType {
  header,
  text,
  button,
  badge,
  statCard,
  barChart,
  donutChart,
  flowchart,
  designTokens,
  mockupPlaceholder,
  personaMatrix,
  kpiStrip,
  shape,
  group, // Figma Group / AutoLayout Frame
}

enum AutoLayoutDirection { none, horizontal, vertical }
enum AutoLayoutAlignment { start, center, end, spaceBetween }

enum TextAlignOption { left, center, right }

class DeckTextStyle {
  String fontFamily;
  double fontSize;
  FontWeight fontWeight;
  Color color;
  double letterSpacing; // 자간
  double height; // 행간
  double wordSpacing; // 장평/어간
  TextAlignOption textAlign;

  DeckTextStyle({
    this.fontFamily = 'Pretendard',
    this.fontSize = 16.0,
    this.fontWeight = FontWeight.normal,
    this.color = const Color(0xFF0F172A),
    this.letterSpacing = 0.0,
    this.height = 1.4,
    this.wordSpacing = 0.0,
    this.textAlign = TextAlignOption.left,
  });

  TextAlign get flutterTextAlign {
    switch (textAlign) {
      case TextAlignOption.center:
        return TextAlign.center;
      case TextAlignOption.right:
        return TextAlign.right;
      default:
        return TextAlign.left;
    }
  }

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
        'textAlign': textAlign.name,
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
      textAlign: TextAlignOption.values.firstWhere(
        (t) => t.name == json['textAlign'],
        orElse: () => TextAlignOption.left,
      ),
    );
  }
}

class DeckBoxStyle {
  Color backgroundColor;
  Color borderColor;
  double borderWidth;
  double borderRadius;
  double padding;
  bool hasShadow;

  DeckBoxStyle({
    this.backgroundColor = Colors.white,
    this.borderColor = const Color(0xFFE2E8F0),
    this.borderWidth = 1.0,
    this.borderRadius = 16.0,
    this.padding = 16.0,
    this.hasShadow = true,
  });

  BoxDecoration toDecoration() {
    return BoxDecoration(
      color: backgroundColor,
      borderRadius: BorderRadius.circular(borderRadius),
      border: borderWidth > 0 ? Border.all(color: borderColor, width: borderWidth) : null,
      boxShadow: hasShadow
          ? [
              BoxShadow(
                color: const Color(0xFF0F172A).withValues(alpha: 0.04),
                blurRadius: 16,
                offset: const Offset(0, 4),
              ),
            ]
          : null,
    );
  }

  Map<String, dynamic> toJson() => {
        'backgroundColor': backgroundColor.toARGB32(),
        'borderColor': borderColor.toARGB32(),
        'borderWidth': borderWidth,
        'borderRadius': borderRadius,
        'padding': padding,
        'hasShadow': hasShadow,
      };

  factory DeckBoxStyle.fromJson(Map<String, dynamic> json) {
    return DeckBoxStyle(
      backgroundColor: Color((json['backgroundColor'] as int?) ?? 0xFFFFFFFF),
      borderColor: Color((json['borderColor'] as int?) ?? 0xFFE2E8F0),
      borderWidth: (json['borderWidth'] as num?)?.toDouble() ?? 1.0,
      borderRadius: (json['borderRadius'] as num?)?.toDouble() ?? 16.0,
      padding: (json['padding'] as num?)?.toDouble() ?? 16.0,
      hasShadow: json['hasShadow'] ?? true,
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
  DeckBoxStyle boxStyle;
  String iconName; // e.g., 'check_circle', 'phone', 'tune', 'star'
  Map<String, dynamic> props;

  // Figma Layer & AutoLayout Features
  bool isLocked;
  bool isVisible;
  AutoLayoutDirection autoLayoutDirection;
  double autoLayoutSpacing;
  double autoLayoutPadding;
  AutoLayoutAlignment autoLayoutAlignment;
  List<DeckElement> children;

  DeckElement({
    required this.id,
    required this.type,
    required this.name,
    required this.x,
    required this.y,
    required this.width,
    required this.height,
    DeckTextStyle? textStyle,
    DeckBoxStyle? boxStyle,
    this.iconName = '',
    required this.props,
    this.isLocked = false,
    this.isVisible = true,
    this.autoLayoutDirection = AutoLayoutDirection.none,
    this.autoLayoutSpacing = 16.0,
    this.autoLayoutPadding = 16.0,
    this.autoLayoutAlignment = AutoLayoutAlignment.start,
    List<DeckElement>? children,
  })  : textStyle = textStyle ?? DeckTextStyle(),
        boxStyle = boxStyle ?? DeckBoxStyle(),
        children = children ?? [];

  /// Helper to trigger AutoLayout re-positioning of children
  void applyAutoLayout() {
    if (autoLayoutDirection == AutoLayoutDirection.none || children.isEmpty) return;

    if (autoLayoutDirection == AutoLayoutDirection.horizontal) {
      double curX = autoLayoutPadding;
      for (final child in children) {
        child.x = curX;
        child.y = autoLayoutPadding;
        curX += child.width + autoLayoutSpacing;
      }
      width = curX - autoLayoutSpacing + autoLayoutPadding;
    } else if (autoLayoutDirection == AutoLayoutDirection.vertical) {
      double curY = autoLayoutPadding;
      for (final child in children) {
        child.x = autoLayoutPadding;
        child.y = curY;
        curY += child.height + autoLayoutSpacing;
      }
      height = curY - autoLayoutSpacing + autoLayoutPadding;
    }
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'type': type.name,
        'name': name,
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'textStyle': textStyle.toJson(),
        'boxStyle': boxStyle.toJson(),
        'iconName': iconName,
        'props': props,
        'isLocked': isLocked,
        'isVisible': isVisible,
        'autoLayoutDirection': autoLayoutDirection.name,
        'autoLayoutSpacing': autoLayoutSpacing,
        'autoLayoutPadding': autoLayoutPadding,
        'autoLayoutAlignment': autoLayoutAlignment.name,
        'children': children.map((c) => c.toJson()).toList(),
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
      boxStyle: json['boxStyle'] != null
          ? DeckBoxStyle.fromJson(json['boxStyle'])
          : DeckBoxStyle(),
      iconName: json['iconName'] ?? '',
      props: Map<String, dynamic>.from(json['props'] ?? {}),
      isLocked: json['isLocked'] ?? false,
      isVisible: json['isVisible'] ?? true,
      autoLayoutDirection: AutoLayoutDirection.values.firstWhere(
        (d) => d.name == json['autoLayoutDirection'],
        orElse: () => AutoLayoutDirection.none,
      ),
      autoLayoutSpacing: (json['autoLayoutSpacing'] as num?)?.toDouble() ?? 16.0,
      autoLayoutPadding: (json['autoLayoutPadding'] as num?)?.toDouble() ?? 16.0,
      autoLayoutAlignment: AutoLayoutAlignment.values.firstWhere(
        (a) => a.name == json['autoLayoutAlignment'],
        orElse: () => AutoLayoutAlignment.start,
      ),
      children: (json['children'] as List? ?? [])
          .map((c) => DeckElement.fromJson(Map<String, dynamic>.from(c)))
          .toList(),
    );
  }

  /// Deep-clone element with new unique IDs for entire children tree
  DeckElement deepClone({double deltaX = 24.0, double deltaY = 24.0}) {
    final rawJson = toJson();
    _reassignIds(rawJson);
    final cloned = DeckElement.fromJson(rawJson);
    cloned.x += deltaX;
    cloned.y += deltaY;
    cloned.name = '$name (복제)';
    return cloned;
  }

  static void _reassignIds(Map<String, dynamic> map) {
    map['id'] = 'elem_${DateTime.now().microsecondsSinceEpoch}';
    if (map['children'] is List) {
      for (final child in map['children']) {
        if (child is Map<String, dynamic>) {
          _reassignIds(child);
        }
      }
    }
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

  Map<String, dynamic> toJson() => {
        'title': title,
        'author': author,
        'slides': slides.map((s) => s.toJson()).toList(),
      };

  factory PortfolioProject.fromJson(Map<String, dynamic> map) {
    return PortfolioProject(
      title: map['title'] ?? 'Portfolio',
      author: map['author'] ?? 'Designer',
      slides: (map['slides'] as List? ?? [])
          .map((s) => DeckSlide.fromJson(Map<String, dynamic>.from(s)))
          .toList(),
    );
  }

  String toJsonString() {
    return jsonEncode(toJson());
  }

  factory PortfolioProject.fromJsonString(String str) {
    return PortfolioProject.fromJson(jsonDecode(str));
  }

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
          iconName: 'fact_check',
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
          iconName: 'phone_android',
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

    return proj;
  }
}

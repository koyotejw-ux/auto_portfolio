import 'package:flutter/services.dart';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'models/deck_model.dart';
import 'models/multagi_template.dart';
import 'widgets/canvas_editor.dart';
import 'widgets/inspector_panel.dart';
import 'widgets/figma_toolbar.dart';
import 'widgets/element_library_modal.dart';
import 'widgets/design_system_library_modal.dart';
import 'widgets/fullscreen_export_modal.dart';
import 'widgets/figma_layers_panel.dart';
import 'widgets/figma_assets_panel.dart';
import 'widgets/icon_drawing_modal.dart';

void main() {
  runApp(const DeckStudioApp());
}

class DeckStudioApp extends StatelessWidget {
  const DeckStudioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DeckStudio - Portfolio Deck Builder',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0052FF),
          primary: const Color(0xFF0052FF),
        ),
        fontFamily: 'Pretendard',
        scaffoldBackgroundColor: const Color(0xFFF1F5F9),
        useMaterial3: true,
      ),
      home: const DeckStudioHomeScreen(),
    );
  }
}

class DeckStudioHomeScreen extends StatefulWidget {
  const DeckStudioHomeScreen({super.key});

  @override
  State<DeckStudioHomeScreen> createState() => _DeckStudioHomeScreenState();
}

class _DeckStudioHomeScreenState extends State<DeckStudioHomeScreen> {
  late PortfolioProject _project;
  int _activeSlideIndex = 0;
  DeckElement? _selectedElement;

  // Figma Toolbar Mode & Undo/Redo Stacks
  FigmaToolMode _currentToolMode = FigmaToolMode.select;
  final List<String> _undoStack = [];
  final List<String> _redoStack = [];
  double _zoomScale = 0.55;
  DeckElement? _clipboardElement;
  final FocusNode _keyboardFocusNode = FocusNode();
  bool _showLayoutGrid = false;
  int _leftSidebarTabIndex = 0; // 0: Layers, 1: Assets (Design System)
  bool _isPagesExpanded = true; // Figma-style collapsible Pages header in Layers tab

  @override
  void initState() {
    super.initState();
    // Default load Smart DCA (물타기 계산기) 12-slide full portfolio deck
    _project = MultagiProjectTemplate.createSmartDcaProject();
  }

  DeckSlide get _currentSlide => _project.slides[_activeSlideIndex];

  void _recordUndoState() {
    try {
      final jsonState = jsonEncode(_project.toJson());
      _undoStack.add(jsonState);
      if (_undoStack.length > 30) {
        _undoStack.removeAt(0);
      }
      _redoStack.clear();
    } catch (_) {}
  }

  void _undo() {
    if (_undoStack.isEmpty) return;
    try {
      final currentState = jsonEncode(_project.toJson());
      _redoStack.add(currentState);
      final lastState = _undoStack.removeLast();
      setState(() {
        _project = PortfolioProject.fromJson(jsonDecode(lastState));
        if (_activeSlideIndex >= _project.slides.length) {
          _activeSlideIndex = _project.slides.length - 1;
        }
        _selectedElement = null;
      });
    } catch (_) {}
  }

  void _redo() {
    if (_redoStack.isEmpty) return;
    try {
      final currentState = jsonEncode(_project.toJson());
      _undoStack.add(currentState);
      final nextState = _redoStack.removeLast();
      setState(() {
        _project = PortfolioProject.fromJson(jsonDecode(nextState));
        if (_activeSlideIndex >= _project.slides.length) {
          _activeSlideIndex = _project.slides.length - 1;
        }
        _selectedElement = null;
      });
    } catch (_) {}
  }

  void _addNewSlide() {
    _recordUndoState();
    setState(() {
      final newPageNum = _project.slides.length + 1;
      _project.slides.add(DeckSlide(
        id: 'slide_$newPageNum',
        title: '$newPageNum. Custom Section',
        pageNumber: newPageNum,
        backgroundColor: const Color(0xFFF8FAFC),
        elements: [
          DeckElement(
            id: 'header_$newPageNum',
            type: ElementType.header,
            name: '상단 헤더',
            x: 100,
            y: 70,
            width: 1720,
            height: 60,
            props: {
              'badge': '0$newPageNum CORE FEATURE',
              'meta': 'Portfolio Architecture · Custom Section Spec',
            },
          ),
          DeckElement(
            id: 'title_$newPageNum',
            type: ElementType.text,
            name: '타이틀 텍스트',
            x: 100,
            y: 150,
            width: 1000,
            height: 120,
            props: {
              'titleBlack': '사용자 경험을 혁신하는 ',
              'titleBlue': '새로운 기능 섹션',
              'subtitle': '포트폴리오의 논리와 디자인 의도를 자유롭게 정의하고 커스텀하세요.',
            },
          ),
        ],
      ));
      _activeSlideIndex = _project.slides.length - 1;
      _selectedElement = null;
    });
  }

  void _showProjectSwitchDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF0F172A),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Text('포트폴리오 프로젝트 전환', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              tileColor: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              leading: const Icon(Icons.calculate, color: Color(0xFF0052FF)),
              title: const Text('스마트 DCA (물타기 계산기) 12개 전 섹션', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
              subtitle: const Text('리서치, 페르소나, IA, 플로우차트, 와이어프레임, 디자인시스템, 0.2s 음성도크, 퀀트역산, 6대화면, 비즈니스임팩트, 라이브허브', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 10)),
              onTap: () {
                _recordUndoState();
                setState(() {
                  _project = MultagiProjectTemplate.createSmartDcaProject();
                  _activeSlideIndex = 0;
                  _selectedElement = null;
                });
                Navigator.pop(ctx);
              },
            ),
            const SizedBox(height: 12),
            ListTile(
              tileColor: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              leading: const Icon(Icons.qr_code_scanner, color: Color(0xFF06B6D4)),
              title: const Text('ZeroPass / 체크앤페이 엔터프라이즈 케이스스터디', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
              subtitle: const Text('1초 원터치 키오스크 UI, D-Day 수납, 3D 마스코트 패시 덱', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 10)),
              onTap: () {
                _recordUndoState();
                setState(() {
                  _project = PortfolioProject.createDefaultTemplate();
                  _activeSlideIndex = 0;
                  _selectedElement = null;
                });
                Navigator.pop(ctx);
              },
            ),
          ],
        ),
      ),
    );
  }

  void _openElementLibrary() {
    showDialog(
      context: context,
      builder: (ctx) => ElementLibraryModal(
        onSelectType: (type) {
          Navigator.pop(ctx);
          _insertElement(type);
        },
      ),
    );
  }

  void _insertElement(ElementType type) {
    _recordUndoState();
    setState(() {
      final id = 'elem_${DateTime.now().millisecondsSinceEpoch}';
      late DeckElement newElem;

      switch (type) {
        case ElementType.text:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '텍스트 레이블',
            x: 200,
            y: 200,
            width: 480,
            height: 100,
            props: {
              'category': 'HIGHLIGHT',
              'titleBlack': '핵심 가치 제안 ',
              'titleBlue': '강조 포인트',
              'subtitle': '상세한 UX 기획 배경 및 문제 해결 과정을 서술합니다.',
            },
          );
          break;
        case ElementType.shape:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '컨테이너 / 카드',
            x: 240,
            y: 240,
            width: 460,
            height: 260,
            boxStyle: DeckBoxStyle(
              backgroundColor: Colors.white,
              borderColor: const Color(0xFFE2E8F0),
              borderWidth: 1.0,
              borderRadius: 16.0,
              padding: 20.0,
            ),
            props: {
              'title': '카드 컴포넌트',
              'desc': 'Figma처럼 자유롭게 스타일과 규격을 변경할 수 있는 다목적 카드 컨테이너입니다.',
            },
          );
          break;
        case ElementType.flowchart:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '플로우차트 / 프로세스',
            x: 100,
            y: 360,
            width: 780,
            height: 440,
            props: {
              'items': [
                {'num': '01', 'tag': '원터치', 'title': '진입 및 탐색', 'desc': '직관적인 시작 단계'},
                {'num': '02', 'tag': '자동화', 'title': '핵심 작업 수행', 'desc': '마찰 없는 빠른 완결'},
                {'num': '03', 'tag': '안심 보관', 'title': '결과 동기화', 'desc': '실시간 메인 화면 반영'},
              ]
            },
          );
          break;
        case ElementType.kpiStrip:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '하단 규격 바',
            x: 100,
            y: 840,
            width: 1720,
            height: 120,
            props: {
              'items': [
                {'title': '측정 지표 1', 'val': '0.8초', 'sub': '속도 혁신'},
                {'title': '측정 지표 2', 'val': '100%', 'sub': '무손실 안전성'},
                {'title': '측정 지표 3', 'val': '60 fps', 'sub': '무지연 렌더링'},
                {'title': '측정 지표 4', 'val': 'AAA', 'sub': '글로벌 표준'},
              ]
            },
          );
          break;
        case ElementType.donutChart:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '도넛 차트 / 완성도 게이지',
            x: 960,
            y: 200,
            width: 500,
            height: 480,
            props: {
              'title': '시스템 완성도 지표',
              'percentage': 96.5,
              'stat1': '가이드라인 준수',
              'stat2': '고대비 최적화',
            },
          );
          break;
        case ElementType.designTokens:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '디자인 토큰 시스템',
            x: 100,
            y: 200,
            width: 820,
            height: 580,
            props: {
              'colors': [
                {'name': 'Primary Blue', 'hex': '#0052FF'},
                {'name': 'Cyan Accent', 'hex': '#06B6D4'},
                {'name': 'Dark Obsidian', 'hex': '#0F172A'},
              ],
              'typography': [
                {'level': 'Display', 'size': '56px', 'sample': '헤드라인'},
                {'level': 'Body', 'size': '14px', 'sample': '본문 텍스트'},
              ]
            },
          );
          break;
        case ElementType.mockupPlaceholder:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '목업 플레이스홀더',
            x: 960,
            y: 180,
            width: 800,
            height: 600,
            props: {
              'screenTitle': '모바일 앱 화면',
              'showMascot': false,
            },
          );
          break;
        default:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '새 요소',
            x: 200,
            y: 200,
            width: 400,
            height: 200,
            props: {},
          );
      }

      _currentSlide.elements.add(newElem);
      _selectedElement = newElem;
    });
  }

  // --- Quick Figma Actions ---
  void _copySelected() {
    if (_selectedElement == null) return;
    _clipboardElement = _selectedElement!.deepClone(deltaX: 0, deltaY: 0);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.check_circle, color: Colors.white, size: 16),
            const SizedBox(width: 8),
            Text(
              '컴포넌트 [${_selectedElement!.name}] 및 하위 요소(${_selectedElement!.children.length}개)가 클립보드에 복사되었습니다. (Ctrl+V로 붙여넣기)',
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        backgroundColor: const Color(0xFF0052FF),
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
    setState(() {});
  }

  void _pasteClipboard() {
    if (_clipboardElement == null) return;
    _recordUndoState();
    setState(() {
      final pasted = _clipboardElement!.deepClone(deltaX: 32.0, deltaY: 32.0);
      _currentSlide.elements.add(pasted);
      _selectedElement = pasted;
      _clipboardElement = pasted.deepClone(deltaX: 0, deltaY: 0);
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          '컴포넌트 [${_selectedElement!.name}] 붙여넣기 완료!',
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
        ),
        backgroundColor: const Color(0xFF0052FF),
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _duplicateSelected() {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      final duplicated = _selectedElement!.deepClone(deltaX: 24.0, deltaY: 24.0);
      _currentSlide.elements.add(duplicated);
      _selectedElement = duplicated;
    });
  }

  void _deleteSelected() {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      _currentSlide.elements.removeWhere((e) => e.id == _selectedElement!.id);
      _selectedElement = null;
    });
  }

  void _bringToFront() {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      final elem = _selectedElement!;
      _currentSlide.elements.removeWhere((e) => e.id == elem.id);
      _currentSlide.elements.add(elem);
    });
  }

  void _sendToBack() {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      final elem = _selectedElement!;
      _currentSlide.elements.removeWhere((e) => e.id == elem.id);
      _currentSlide.elements.insert(0, elem);
    });
  }

  void _groupSelected() {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      final elem = _selectedElement!;
      final index = _currentSlide.elements.indexOf(elem);
      if (index == -1) return;

      final group = DeckElement(
        id: 'group_${DateTime.now().millisecondsSinceEpoch}',
        type: ElementType.group,
        name: 'Frame · ${elem.name}',
        x: elem.x,
        y: elem.y,
        width: elem.width,
        height: elem.height,
        boxStyle: DeckBoxStyle(
          backgroundColor: Colors.transparent,
          borderColor: const Color(0xFF38BDF8),
          borderWidth: 1.0,
          borderRadius: 8.0,
        ),
        props: {},
        autoLayoutDirection: AutoLayoutDirection.none,
        children: [elem],
      );

      _currentSlide.elements[index] = group;
      _selectedElement = group;
    });
  }

  void _toggleAutoLayout() {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      final elem = _selectedElement!;
      if (elem.autoLayoutDirection == AutoLayoutDirection.none) {
        elem.autoLayoutDirection = AutoLayoutDirection.horizontal;
        elem.type = ElementType.group;
        elem.name = elem.name.startsWith('AutoLayout') ? elem.name : 'AutoLayout · ${elem.name}';
        elem.applyAutoLayout();
      } else if (elem.autoLayoutDirection == AutoLayoutDirection.horizontal) {
        elem.autoLayoutDirection = AutoLayoutDirection.vertical;
        elem.applyAutoLayout();
      } else {
        elem.autoLayoutDirection = AutoLayoutDirection.none;
      }
    });
  }

  void _ungroupSelected() {
    if (_selectedElement == null) return;
    final parent = _selectedElement!;

    // Check if it's a Figma Group with children
    if (parent.children.isNotEmpty) {
      _recordUndoState();
      setState(() {
        final index = _currentSlide.elements.indexOf(parent);
        for (final child in parent.children) {
          child.x = parent.x + child.x;
          child.y = parent.y + child.y;
        }
        if (index != -1) {
          _currentSlide.elements.removeAt(index);
          _currentSlide.elements.insertAll(index, parent.children);
          _selectedElement = parent.children.first;
        }
      });
      return;
    }

    // Check legacy composite items
    final items = parent.props['items'];
    if (items is! List || items.isEmpty) return;

    _recordUndoState();
    setState(() {
      final index = _currentSlide.elements.indexOf(parent);
      final newElements = <DeckElement>[];

      if (parent.type == ElementType.kpiStrip) {
        final count = items.length;
        const totalW = 1720.0;
        final cardW = (totalW - (count - 1) * 16.0) / count;
        final cardH = parent.height;

        for (int i = 0; i < count; i++) {
          final item = Map<String, dynamic>.from(items[i]);
          final newX = parent.x + i * (cardW + 16.0);
          final newY = parent.y;

          newElements.add(DeckElement(
            id: 'kpi_${DateTime.now().millisecondsSinceEpoch}_$i',
            type: ElementType.statCard,
            name: '${item['title'] ?? '메트릭 ${i + 1}'}',
            x: newX,
            y: newY,
            width: cardW,
            height: cardH,
            boxStyle: DeckBoxStyle(
              backgroundColor: parent.boxStyle.backgroundColor,
              borderColor: parent.boxStyle.borderColor,
            ),
            props: {
              'title': item['title'] ?? '',
              'val': item['val'] ?? '',
              'sub': item['sub'] ?? '',
            },
          ));
        }
      } else {
        // Flowchart or list items
        final count = items.length;
        final itemH = (parent.height - (count - 1) * 14.0) / count;
        final itemW = parent.width;

        for (int i = 0; i < count; i++) {
          final item = Map<String, dynamic>.from(items[i]);
          final newX = parent.x;
          final newY = parent.y + i * (itemH + 14.0);

          newElements.add(DeckElement(
            id: 'card_${DateTime.now().millisecondsSinceEpoch}_$i',
            type: ElementType.shape,
            name: '${item['tag'] ?? item['title'] ?? '카드 ${i + 1}'}',
            x: newX,
            y: newY,
            width: itemW,
            height: itemH,
            boxStyle: DeckBoxStyle(
              backgroundColor: Colors.white,
              borderColor: const Color(0xFFE2E8F0),
            ),
            props: {
              'num': item['num'] ?? '0${i + 1}',
              'tag': item['tag'] ?? '',
              'title': item['title'] ?? '',
              'desc': item['desc'] ?? '',
            },
          ));
        }
      }

      if (index != -1) {
        _currentSlide.elements.removeAt(index);
        _currentSlide.elements.insertAll(index, newElements);
        _selectedElement = newElements.isNotEmpty ? newElements.first : null;
      }
    });
  }

  void _alignSelected(String alignType) {
    if (_selectedElement == null) return;
    _recordUndoState();
    setState(() {
      final elem = _selectedElement!;
      const canvasW = 1920.0;
      const canvasH = 1080.0;

      switch (alignType) {
        case 'left':
          elem.x = 100.0;
          break;
        case 'center_h':
          elem.x = (canvasW - elem.width) / 2;
          break;
        case 'right':
          elem.x = canvasW - elem.width - 100.0;
          break;
        case 'top':
          elem.y = 80.0;
          break;
        case 'center_v':
          elem.y = (canvasH - elem.height) / 2;
          break;
        case 'bottom':
          elem.y = canvasH - elem.height - 80.0;
          break;
      }
    });
  }

  void _showShortcutsDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E1E),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: Color(0xFF333333))),
        title: const Row(
          children: [
            Icon(Icons.keyboard, color: Color(0xFF0052FF), size: 20),
            SizedBox(width: 8),
            Text('Figma 완전 단축키 치트시트 (Figma Keyboard Shortcuts)', style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
          ],
        ),
        content: SizedBox(
          width: 580,
          height: 440,
          child: ListView(
            children: const [
              _ShortcutGroup(title: '도구 선택 (Tools)', items: [
                _ShortcutItem(keys: 'V', desc: '선택 및 이동 도구 (Move Tool)'),
                _ShortcutItem(keys: 'T', desc: '텍스트 레이어 추가 (Text Tool)'),
                _ShortcutItem(keys: 'R', desc: '사각형 / 카드 박스 (Rectangle)'),
                _ShortcutItem(keys: 'F', desc: '새 프레임 / 섹션 (Frame)'),
                _ShortcutItem(keys: 'H / Space', desc: '핸드 이동 툴 (Hand Tool)'),
              ]),
              _ShortcutGroup(title: '객체 탐색 & 포커싱 (Focus & Selection)', items: [
                _ShortcutItem(keys: 'Tab', desc: '다음 레이어로 순차 포커스 이동 (Cycle Next)'),
                _ShortcutItem(keys: 'Esc', desc: '선택 해제 (Deselect)'),
                _ShortcutItem(keys: 'Ctrl + A', desc: '전체 객체 탐색 활성화 (Select All)'),
                _ShortcutItem(keys: '더블 클릭 (Double Tap)', desc: '텍스트 제자리 인라인 편집 (Edit Text)'),
              ]),
              _ShortcutGroup(title: '그리드 & 가이드 (View & Grid)', items: [
                _ShortcutItem(keys: 'Ctrl + \' (or Ctrl+Shift+4)', desc: '피그마 12컬럼 / 8pt 레이아웃 그리드 토글'),
                _ShortcutItem(keys: 'Ctrl + + / Ctrl + -', desc: '화면 확대 / 축소 (Zoom In/Out)'),
                _ShortcutItem(keys: 'Shift + 1 (or 0)', desc: '캔버스 100% 핏 맞춤 (Zoom to Fit)'),
              ]),
              _ShortcutGroup(title: '정밀 이동 & 변형 (Nudge & Layout)', items: [
                _ShortcutItem(keys: '방향키 (↑/↓/←/→)', desc: '1px 정밀 미세 이동 (Nudge)'),
                _ShortcutItem(keys: 'Shift + 방향키', desc: '10px 고속 이동 (Big Nudge)'),
                _ShortcutItem(keys: 'Shift + A', desc: '오토레이아웃 토글 (AutoLayout H/V/None)'),
                _ShortcutItem(keys: 'Ctrl + G / Ctrl + Shift + G', desc: '그룹화 (Group) / 그룹 해제 (Ungroup)'),
              ]),
              _ShortcutGroup(title: '레이어 & 편집 (Edit & Hierarchy)', items: [
                _ShortcutItem(keys: 'Ctrl + C / Ctrl + V', desc: '하위 트리 포함 컴포넌트 복사 & 붙여넣기'),
                _ShortcutItem(keys: 'Ctrl + D', desc: '제자리 오프셋 복제 (Duplicate)'),
                _ShortcutItem(keys: 'Ctrl + Z / Ctrl + Y', desc: '실행 취소 (Undo) / 다시 실행 (Redo)'),
                _ShortcutItem(keys: '] / [', desc: '맨 앞으로 가져오기 / 맨 뒤로 보내기'),
                _ShortcutItem(keys: 'Ctrl + Shift + L', desc: '선택 요소 잠금 / 해제 토글 (Lock/Unlock)'),
                _ShortcutItem(keys: 'Ctrl + Shift + H', desc: '선택 요소 숨김 / 보이기 토글 (Hide/Show)'),
                _ShortcutItem(keys: 'Delete / Backspace', desc: '선택 요소 삭제 (Delete)'),
              ]),
            ],
          ),
        ),
        actions: [
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0052FF), foregroundColor: Colors.white),
            onPressed: () => Navigator.pop(ctx),
            child: const Text('닫기'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Focus(
        focusNode: _keyboardFocusNode,
        autofocus: true,
        onKeyEvent: (node, event) {
          if (event is KeyDownEvent) {
            final isCtrl = HardwareKeyboard.instance.isControlPressed ||
                HardwareKeyboard.instance.isMetaPressed;
            final isShift = HardwareKeyboard.instance.isShiftPressed;
            final isAlt = HardwareKeyboard.instance.isAltPressed;

            // 1. Copy / Paste / Duplicate
            if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyC) {
              if (_selectedElement != null) {
                _copySelected();
                return KeyEventResult.handled;
              }
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyV) {
              if (_clipboardElement != null) {
                _pasteClipboard();
                return KeyEventResult.handled;
              }
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyD) {
              if (_selectedElement != null) {
                _duplicateSelected();
                return KeyEventResult.handled;
              }
            // 2. Undo / Redo
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyZ) {
              if (isShift) {
                _redo();
              } else {
                _undo();
              }
              return KeyEventResult.handled;
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyY) {
              _redo();
              return KeyEventResult.handled;
            // 3. Group / Ungroup
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyG) {
              if (isShift) {
                _ungroupSelected();
              } else {
                _groupSelected();
              }
              return KeyEventResult.handled;
            // 4. AutoLayout Toggle (Shift + A)
            } else if (isShift && event.logicalKey == LogicalKeyboardKey.keyA) {
              _toggleAutoLayout();
              return KeyEventResult.handled;
            // 5. Delete (Delete or Backspace)
            } else if (event.logicalKey == LogicalKeyboardKey.delete || event.logicalKey == LogicalKeyboardKey.backspace) {
              if (_selectedElement != null) {
                _deleteSelected();
                return KeyEventResult.handled;
              }
            // 5.1 Select All (Ctrl + A)
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyA) {
              if (_currentSlide.elements.isNotEmpty) {
                setState(() => _selectedElement = _currentSlide.elements.first);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('전체 객체 탐색 활성화 (Tab 키로 순회 선택 가능)'),
                    duration: Duration(seconds: 1),
                  ),
                );
                return KeyEventResult.handled;
              }
            // 5.2 Layout Grid Toggle (Ctrl + Shift + 4 or Ctrl + ')
            } else if ((isCtrl && isShift && event.logicalKey == LogicalKeyboardKey.digit4) ||
                       (isCtrl && event.logicalKey == LogicalKeyboardKey.quote)) {
              setState(() => _showLayoutGrid = !_showLayoutGrid);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(_showLayoutGrid ? 'Figma 레이아웃 그리드 (12컬럼 / 8pt 그리드) 켜짐' : '레이아웃 그리드 꺼짐'),
                  duration: const Duration(seconds: 1),
                  backgroundColor: const Color(0xFF0052FF),
                ),
              );
              return KeyEventResult.handled;
            // 5.3 Lock / Unlock Selected (Ctrl + Shift + L)
            } else if (isCtrl && isShift && event.logicalKey == LogicalKeyboardKey.keyL) {
              if (_selectedElement != null) {
                _recordUndoState();
                setState(() => _selectedElement!.isLocked = !_selectedElement!.isLocked);
                return KeyEventResult.handled;
              }
            // 5.4 Hide / Show Selected (Ctrl + Shift + H)
            } else if (isCtrl && isShift && event.logicalKey == LogicalKeyboardKey.keyH) {
              if (_selectedElement != null) {
                _recordUndoState();
                setState(() {
                  _selectedElement!.isVisible = !_selectedElement!.isVisible;
                  if (!_selectedElement!.isVisible) _selectedElement = null;
                });
                return KeyEventResult.handled;
              }
            // 5.5 Show Figma Shortcuts CheatSheet (Ctrl + / or ?)
            } else if (isCtrl && (event.logicalKey == LogicalKeyboardKey.slash || event.logicalKey == LogicalKeyboardKey.question)) {
              _showShortcutsDialog();
              return KeyEventResult.handled;
            // 6. Layer Stacking Order: Bring to Front (]) / Send to Back ([)
            } else if (event.logicalKey == LogicalKeyboardKey.bracketRight) {
              if (_selectedElement != null) {
                _bringToFront();
                return KeyEventResult.handled;
              }
            } else if (event.logicalKey == LogicalKeyboardKey.bracketLeft) {
              if (_selectedElement != null) {
                _sendToBack();
                return KeyEventResult.handled;
              }
            // 7. Figma Zoom Shortcuts (Ctrl + + / Ctrl + - / Shift + 1 / Shift + 2 / Shift + 0)
            } else if (isCtrl && (event.logicalKey == LogicalKeyboardKey.equal || event.logicalKey == LogicalKeyboardKey.numpadAdd)) {
              setState(() {
                if (_zoomScale < 2.0) _zoomScale += 0.05;
              });
              return KeyEventResult.handled;
            } else if (isCtrl && (event.logicalKey == LogicalKeyboardKey.minus || event.logicalKey == LogicalKeyboardKey.numpadSubtract)) {
              setState(() {
                if (_zoomScale > 0.2) _zoomScale -= 0.05;
              });
              return KeyEventResult.handled;
            } else if (isShift && (event.logicalKey == LogicalKeyboardKey.digit1 || event.logicalKey == LogicalKeyboardKey.digit0)) {
              setState(() => _zoomScale = 0.55); // Zoom to Fit
              return KeyEventResult.handled;
            // 8. Tool Mode Shortcuts (V, T, R, F, H)
            } else if (!isCtrl && !isShift && !isAlt) {
              if (event.logicalKey == LogicalKeyboardKey.keyV) {
                setState(() => _currentToolMode = FigmaToolMode.select);
                return KeyEventResult.handled;
              } else if (event.logicalKey == LogicalKeyboardKey.keyT) {
                _insertElement(ElementType.text);
                return KeyEventResult.handled;
              } else if (event.logicalKey == LogicalKeyboardKey.keyR) {
                _insertElement(ElementType.shape);
                return KeyEventResult.handled;
              } else if (event.logicalKey == LogicalKeyboardKey.keyF) {
                _addNewSlide();
                return KeyEventResult.handled;
              } else if (event.logicalKey == LogicalKeyboardKey.keyH) {
                setState(() => _currentToolMode = FigmaToolMode.hand);
                return KeyEventResult.handled;
              } else if (event.logicalKey == LogicalKeyboardKey.escape) {
                setState(() => _selectedElement = null);
                return KeyEventResult.handled;
              // Tab / Shift+Tab to Cycle Elements on Canvas
              } else if (event.logicalKey == LogicalKeyboardKey.tab) {
                if (_currentSlide.elements.isNotEmpty) {
                  final idx = _selectedElement == null ? -1 : _currentSlide.elements.indexOf(_selectedElement!);
                  setState(() {
                    if (idx == -1) {
                      _selectedElement = _currentSlide.elements.first;
                    } else {
                      final nextIdx = (idx + 1) % _currentSlide.elements.length;
                      _selectedElement = _currentSlide.elements[nextIdx];
                    }
                  });
                  return KeyEventResult.handled;
                }
              }
            // 9. Nudge Arrow Keys (1px / 10px)
            } else if (event.logicalKey == LogicalKeyboardKey.arrowLeft ||
                event.logicalKey == LogicalKeyboardKey.arrowRight ||
                event.logicalKey == LogicalKeyboardKey.arrowUp ||
                event.logicalKey == LogicalKeyboardKey.arrowDown) {
              if (_selectedElement != null && !_selectedElement!.isLocked) {
                final delta = isShift ? 10.0 : 1.0;
                _recordUndoState();
                setState(() {
                  if (event.logicalKey == LogicalKeyboardKey.arrowLeft) _selectedElement!.x -= delta;
                  if (event.logicalKey == LogicalKeyboardKey.arrowRight) _selectedElement!.x += delta;
                  if (event.logicalKey == LogicalKeyboardKey.arrowUp) _selectedElement!.y -= delta;
                  if (event.logicalKey == LogicalKeyboardKey.arrowDown) _selectedElement!.y += delta;
                });
                return KeyEventResult.handled;
              }
            }
          }
          return KeyEventResult.ignored;
        },
        child: Column(
          children: [
            // 1. Figma UI3 Global App Top Header
            _buildGlobalAppBar(),

            // 2. Main Workspace: Slide Thumbnails + Figma Layers + Canvas Editor + Inspector Panel
            Expanded(
              child: Row(
                children: [
                  // Unified Left Sidebar: Figma UI3 (Tabs: Layers & Pages / Assets)
                  Container(
                    width: 260,
                    decoration: const BoxDecoration(
                      color: Color(0xFF1E1E1E),
                      border: Border(right: BorderSide(color: Color(0xFF2C2C2C))),
                    ),
                    child: Column(
                      children: [
                        // UI3 Left Sidebar Tabs: Layers / Assets
                        Container(
                          height: 38,
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: const BoxDecoration(
                            border: Border(bottom: BorderSide(color: Color(0xFF2C2C2C))),
                          ),
                          child: Row(
                            children: [
                              Expanded(
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(4),
                                  onTap: () => setState(() => _leftSidebarTabIndex = 0),
                                  child: Container(
                                    alignment: Alignment.center,
                                    decoration: BoxDecoration(
                                      color: _leftSidebarTabIndex == 0 ? const Color(0xFF2C2C2C) : Colors.transparent,
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(
                                          Icons.layers_outlined,
                                          size: 13,
                                          color: _leftSidebarTabIndex == 0 ? const Color(0xFF38BDF8) : const Color(0xFFA3A3A3),
                                        ),
                                        const SizedBox(width: 4),
                                        Text(
                                          'Layers',
                                          style: TextStyle(
                                            color: _leftSidebarTabIndex == 0 ? Colors.white : const Color(0xFFA3A3A3),
                                            fontSize: 11,
                                            fontWeight: _leftSidebarTabIndex == 0 ? FontWeight.bold : FontWeight.normal,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 4),
                              Expanded(
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(4),
                                  onTap: () => setState(() => _leftSidebarTabIndex = 1),
                                  child: Container(
                                    alignment: Alignment.center,
                                    decoration: BoxDecoration(
                                      color: _leftSidebarTabIndex == 1 ? const Color(0xFF2C2C2C) : Colors.transparent,
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(
                                          Icons.widgets_outlined,
                                          size: 13,
                                          color: _leftSidebarTabIndex == 1 ? const Color(0xFF38BDF8) : const Color(0xFFA3A3A3),
                                        ),
                                        const SizedBox(width: 4),
                                        Text(
                                          'Assets',
                                          style: TextStyle(
                                            color: _leftSidebarTabIndex == 1 ? Colors.white : const Color(0xFFA3A3A3),
                                            fontSize: 11,
                                            fontWeight: _leftSidebarTabIndex == 1 ? FontWeight.bold : FontWeight.normal,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        // Tab Content Body
                        Expanded(
                          child: _leftSidebarTabIndex == 0
                              ? Column(
                                  children: [
                                    // 1. Figma Page Dropdown Selector (Compact 1-line bar)
                                    _buildFigmaPageDropdownBar(),

                                    // 2. Figma Objects / Layers Hierarchy Tree
                                    Expanded(
                                      child: FigmaLayersPanel(
                                        slide: _currentSlide,
                                        selectedElement: _selectedElement,
                                        onElementSelected: (elem) {
                                          setState(() => _selectedElement = elem);
                                        },
                                        onSlideModified: () {
                                          _recordUndoState();
                                          setState(() {});
                                        },
                                        onGroupSelected: _groupSelected,
                                        onUngroupSelected: _ungroupSelected,
                                        onCopySelected: _copySelected,
                                        onPasteSelected: _pasteClipboard,
                                        canPaste: _clipboardElement != null,
                                      ),
                                    ),
                                  ],
                                )
                              : FigmaAssetsPanel(
                                  onAddElement: (newElem) {
                                    _recordUndoState();
                                    setState(() {
                                      _currentSlide.elements.add(newElem);
                                      _selectedElement = newElem;
                                    });
                                  },
                                ),
                        ),
                      ],
                    ),
                  ),

                  // Center: 1920x1080 Interactive Canvas with Floating Figma UI3 Bottom Dock Toolbar
                  Expanded(
                    child: Stack(
                      children: [
                        Positioned.fill(
                          child: CanvasEditor(
                            slide: _currentSlide,
                            selectedElement: _selectedElement,
                            showLayoutGrid: _showLayoutGrid,
                            onElementSelected: (elem) {
                              setState(() => _selectedElement = elem);
                            },
                            onSlideModified: () {
                              _recordUndoState();
                              setState(() {});
                            },
                          ),
                        ),

                        // Figma UI3 Floating Pill Bottom Toolbar (Floating Above Canvas)
                        Positioned(
                          left: 0,
                          right: 0,
                          bottom: 20,
                          child: Center(
                            child: FigmaToolbar(
                              activeMode: _currentToolMode,
                              onModeChanged: (mode) {
                                setState(() => _currentToolMode = mode);
                              },
                              selectedElement: _selectedElement,
                              onAddText: () => _insertElement(ElementType.text),
                              onAddCard: () => _insertElement(ElementType.shape),
                              onAddFrame: _addNewSlide,
                              onOpenComponentLibrary: _openElementLibrary,
                              onOpenDesignSystem: () {
                                showDialog(
                                  context: context,
                                  builder: (ctx) => const DesignSystemLibraryModal(),
                                );
                              },
                              onDuplicateSelected: _duplicateSelected,
                              onCopySelected: _copySelected,
                              onPasteSelected: _pasteClipboard,
                              canPaste: _clipboardElement != null,
                              onDeleteSelected: _deleteSelected,
                              onBringToFront: _bringToFront,
                              onSendToBack: _sendToBack,
                              onGroupSelected: _groupSelected,
                              onUngroupSelected: _ungroupSelected,
                              onToggleAutoLayout: _toggleAutoLayout,
                              onAlignSelected: _alignSelected,
                              onUndo: _undo,
                              onRedo: _redo,
                              canUndo: _undoStack.isNotEmpty,
                              canRedo: _redoStack.isNotEmpty,
                              zoomScale: _zoomScale,
                              onZoomIn: () {
                                setState(() {
                                  if (_zoomScale < 1.5) _zoomScale += 0.05;
                                });
                              },
                              onZoomOut: () {
                                setState(() {
                                  if (_zoomScale > 0.25) _zoomScale -= 0.05;
                                });
                              },
                              onZoomFit: () {
                                setState(() {
                                  _zoomScale = 0.55;
                                });
                              },
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Right: Inspector Panel (Width: 380)
                  InspectorPanel(
                    element: _selectedElement,
                    onElementUpdated: () {
                      _recordUndoState();
                      setState(() {});
                    },
                    onElementDeleted: _deleteSelected,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGlobalAppBar() {
    return Container(
      height: 46,
      padding: const EdgeInsets.symmetric(horizontal: 14),
      decoration: const BoxDecoration(
        color: Color(0xFF1E1E1E), // Figma UI3 Dark Slate
        border: Border(bottom: BorderSide(color: Color(0xFF2C2C2C))),
      ),
      child: Row(
        children: [
          // Figma UI3 App Icon & Document Title
          Container(
            padding: const EdgeInsets.all(5),
            decoration: BoxDecoration(
              color: const Color(0xFF2C2C2C),
              borderRadius: BorderRadius.circular(6),
            ),
            child: const Icon(Icons.dashboard_customize, color: Color(0xFF0052FF), size: 15),
          ),
          const SizedBox(width: 10),
          Row(
            children: [
              const Text(
                'DeckStudio (데스크탑 포트폴리오 에디터)',
                style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFF2C2C2C),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: const Text('Drafts', style: TextStyle(color: Color(0xFFA3A3A3), fontSize: 10, fontWeight: FontWeight.w500)),
              ),
            ],
          ),
          const Spacer(),
          ElevatedButton.icon(
            icon: Icon(_showLayoutGrid ? Icons.grid_on : Icons.grid_off, size: 14, color: _showLayoutGrid ? const Color(0xFF38BDF8) : const Color(0xFFA3A3A3)),
            label: Text(_showLayoutGrid ? 'Grid ON' : 'Grid', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: _showLayoutGrid ? const Color(0xFF0038A8) : const Color(0xFF2C2C2C),
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(6),
                side: BorderSide(color: _showLayoutGrid ? const Color(0xFF0052FF) : const Color(0xFF404040)),
              ),
            ),
            onPressed: () {
              setState(() => _showLayoutGrid = !_showLayoutGrid);
            },
          ),
          const SizedBox(width: 6),
          IconButton(
            icon: const Icon(Icons.keyboard, color: Color(0xFFA3A3A3), size: 18),
            tooltip: '피그마 전체 단축키 모음 (Ctrl+/)',
            onPressed: _showShortcutsDialog,
            visualDensity: VisualDensity.compact,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
          ),
          const SizedBox(width: 4),
          ElevatedButton.icon(
            icon: const Icon(Icons.swap_horiz, size: 14),
            label: const Text('프로젝트 전환', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF2C2C2C),
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(6),
                side: const BorderSide(color: Color(0xFF404040)),
              ),
            ),
            onPressed: _showProjectSwitchDialog,
          ),
          const SizedBox(width: 6),
          ElevatedButton.icon(
            icon: const Icon(Icons.tune, size: 14, color: Color(0xFF38BDF8)),
            label: const Text('Variables', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF2C2C2C),
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(6),
                side: const BorderSide(color: Color(0xFF404040)),
              ),
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (ctx) => const DesignSystemLibraryModal(),
              );
            },
          ),
          const SizedBox(width: 6),
          ElevatedButton.icon(
            icon: const Icon(Icons.add_box_outlined, size: 14),
            label: const Text('컴포넌트 삽입', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0052FF),
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
            ),
            onPressed: _openElementLibrary,
          ),
          const SizedBox(width: 6),
          ElevatedButton.icon(
            icon: const Icon(Icons.play_arrow, size: 14, color: Colors.white),
            label: const Text('Present', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF10B981),
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (ctx) => FullscreenExportModal(project: _project),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildFigmaPageDropdownBar() {
    return Container(
      height: 36,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: const BoxDecoration(
        color: Color(0xFF1E1E1E),
        border: Border(bottom: BorderSide(color: Color(0xFF2C2C2C))),
      ),
      child: Row(
        children: [
          const Icon(Icons.description_outlined, color: Color(0xFF38BDF8), size: 13),
          const SizedBox(width: 6),
          Expanded(
            child: DropdownButtonHideUnderline(
              child: DropdownButton<int>(
                value: _activeSlideIndex,
                isExpanded: true,
                dropdownColor: const Color(0xFF262626),
                style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                icon: const Icon(Icons.arrow_drop_down, color: Color(0xFFA3A3A3), size: 16),
                items: _project.slides.asMap().entries.map((entry) {
                  final idx = entry.key;
                  final slide = entry.value;
                  return DropdownMenuItem<int>(
                    value: idx,
                    child: Text(
                      'Page ${idx + 1}: ${slide.title}',
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        fontSize: 11,
                        color: idx == _activeSlideIndex ? const Color(0xFF38BDF8) : Colors.white,
                        fontWeight: idx == _activeSlideIndex ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                  );
                }).toList(),
                onChanged: (newIdx) {
                  if (newIdx != null) {
                    setState(() {
                      _activeSlideIndex = newIdx;
                      _selectedElement = null;
                    });
                  }
                },
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.add, size: 15, color: Color(0xFF38BDF8)),
            onPressed: _addNewSlide,
            tooltip: '새 페이지 추가',
            visualDensity: VisualDensity.compact,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
          ),
        ],
      ),
    );
  }

  Widget _buildSlideNavigator() {
    return Container(
      width: 220,
      decoration: const BoxDecoration(
        color: Color(0xFF1E1E1E), // Figma UI3 Dark Slate
        border: Border(right: BorderSide(color: Color(0xFF2C2C2C))),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Color(0xFF2C2C2C))),
            ),
            child: Row(
              children: [
                const Icon(Icons.description_outlined, color: Color(0xFFA3A3A3), size: 14),
                const SizedBox(width: 6),
                const Expanded(
                  child: Text(
                    'Pages / Frames',
                    style: TextStyle(color: Colors.white, fontSize: 11.5, fontWeight: FontWeight.bold),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.add, size: 16, color: Color(0xFF38BDF8)),
                  onPressed: _addNewSlide,
                  tooltip: '새 페이지 추가',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 22, minHeight: 22),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
              itemCount: _project.slides.length,
              itemBuilder: (context, index) {
                final slide = _project.slides[index];
                final isActive = index == _activeSlideIndex;

                return GestureDetector(
                  onTap: () {
                    setState(() {
                      _activeSlideIndex = index;
                      _selectedElement = null;
                    });
                  },
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 4),
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                    decoration: BoxDecoration(
                      color: isActive ? const Color(0xFF2C2C2C) : Colors.transparent,
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(
                        color: isActive ? const Color(0xFF0052FF) : Colors.transparent,
                        width: 1,
                      ),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          Icons.grid_view,
                          size: 13,
                          color: isActive ? const Color(0xFF0052FF) : const Color(0xFF737373),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            slide.title,
                            style: TextStyle(
                              color: isActive ? Colors.white : const Color(0xFFA3A3A3),
                              fontSize: 11.5,
                              fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        Text(
                          '${slide.elements.length}',
                          style: const TextStyle(color: Color(0xFF525252), fontSize: 10),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _ShortcutGroup extends StatelessWidget {
  final String title;
  final List<_ShortcutItem> items;

  const _ShortcutGroup({required this.title, required this.items});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 12, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 6),
          Container(
            decoration: BoxDecoration(
              color: const Color(0xFF262626),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: const Color(0xFF333333)),
            ),
            child: Column(
              children: items.map<Widget>((item) => Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(item.desc, style: const TextStyle(color: Color(0xFFD4D4D4), fontSize: 11.5)),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: const Color(0xFF171717),
                        borderRadius: BorderRadius.circular(4),
                        border: Border.all(color: const Color(0xFF404040)),
                      ),
                      child: Text(
                        item.keys,
                        style: const TextStyle(color: Color(0xFFE5E5E5), fontSize: 10.5, fontWeight: FontWeight.bold, fontFamily: 'Consolas'),
                      ),
                    ),
                  ],
                ),
              )).toList(),
            ),
          ),
        ],
      ),
    );
  }
}

class _ShortcutItem {
  final String keys;
  final String desc;
  const _ShortcutItem({required this.keys, required this.desc});
}

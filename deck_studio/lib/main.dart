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
              '컴포넌트 [] 및 하위 요소(개)가 클립보드에 복사되었습니다. (Ctrl+V로 붙여넣기)',
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
          '컴포넌트 [] 붙여넣기 완료!',
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
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyZ) {
              _undo();
              return KeyEventResult.handled;
            } else if (isCtrl && event.logicalKey == LogicalKeyboardKey.keyY) {
              _redo();
              return KeyEventResult.handled;
            }
          }
          return KeyEventResult.ignored;
        },
        child: Column(
        children: [
          // 1. Global App Bar
          _buildGlobalAppBar(),

          // 2. Figma-Style Quick Toolbar (추가/수정/삭제/정렬/되돌리기/도구 모음)
          FigmaToolbar(
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

          // 3. Main Workspace: Slide Thumbnails + Figma Layers + Canvas Editor + Inspector Panel
          Expanded(
            child: Row(
              children: [
                // Left 1: Slide Thumbnails Navigator (Width: 200)
                _buildSlideNavigator(),

                // Left 2: Figma Object Layers Tree (Width: 260)
                FigmaLayersPanel(
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

                // Center: 1920x1080 Interactive Canvas
                Expanded(
                  child: CanvasEditor(
                    slide: _currentSlide,
                    selectedElement: _selectedElement,
                    onElementSelected: (elem) {
                      setState(() => _selectedElement = elem);
                    },
                    onSlideModified: () {
                      _recordUndoState();
                      setState(() {});
                    },
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
      height: 52,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: const BoxDecoration(
        color: Color(0xFF0F172A),
        border: Border(bottom: BorderSide(color: Color(0xFF1E293B))),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(7),
            decoration: BoxDecoration(
              color: const Color(0xFF0052FF),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.dashboard_customize, color: Colors.white, size: 16),
          ),
          const SizedBox(width: 12),
          const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'DeckStudio (데스크탑 포트폴리오 에디터)',
                style: TextStyle(color: Colors.white, fontSize: 13.5, fontWeight: FontWeight.bold),
              ),
              Text(
                'Figma 표준 툴바 · 도식/플로우차트/디자인시스템/목업 실시간 커스텀 툴',
                style: TextStyle(color: Color(0xFF94A3B8), fontSize: 10),
              ),
            ],
          ),
          const Spacer(),
          ElevatedButton.icon(
            icon: const Icon(Icons.swap_horiz, size: 15),
            label: const Text('프로젝트 템플릿 전환', style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF334155),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
            ),
            onPressed: () {
              _showProjectSwitchDialog();
            },
          ),
          const SizedBox(width: 8),
          ElevatedButton.icon(
            icon: const Icon(Icons.style, size: 15),
            label: const Text('디자인 시스템 라이브러리', style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0891B2),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (ctx) => const DesignSystemLibraryModal(),
              );
            },
          ),
          const SizedBox(width: 8),
          ElevatedButton.icon(
            icon: const Icon(Icons.add_box_outlined, size: 15),
            label: const Text('컴포넌트 삽입', style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0052FF),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
            ),
            onPressed: _openElementLibrary,
          ),
          const SizedBox(width: 8),
          OutlinedButton.icon(
            icon: const Icon(Icons.file_download_outlined, size: 15, color: Color(0xFF38BDF8)),
            label: const Text('전체화면 HTML / Flutter 웹 / PDF 출력', style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.bold, color: Colors.white)),
            style: OutlinedButton.styleFrom(
              backgroundColor: const Color(0xFF1E293B),
              side: const BorderSide(color: Color(0xFF0052FF)),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
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

  Widget _buildSlideNavigator() {
    return Container(
      width: 190,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(right: BorderSide(color: Color(0xFFE2E8F0))),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Color(0xFFE2E8F0))),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  '슬라이드 목록',
                  style: TextStyle(color: Color(0xFF0F172A), fontSize: 13, fontWeight: FontWeight.bold),
                ),
                IconButton(
                  icon: const Icon(Icons.add, size: 20, color: Color(0xFF0052FF)),
                  onPressed: _addNewSlide,
                  tooltip: '새 슬라이드 추가',
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
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
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: isActive ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                        color: isActive ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
                        width: isActive ? 1.5 : 1,
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: isActive ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                'P.${slide.pageNumber}',
                                style: TextStyle(
                                  color: isActive ? Colors.white : const Color(0xFF64748B),
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            Text(
                              '${slide.elements.length}개 요소',
                              style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          slide.title,
                          style: TextStyle(
                            color: isActive ? const Color(0xFF0052FF) : const Color(0xFF0F172A),
                            fontSize: 11.5,
                            fontWeight: isActive ? FontWeight.bold : FontWeight.w500,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
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

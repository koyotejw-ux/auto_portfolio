import 'package:flutter/material.dart';
import 'models/deck_model.dart';
import 'widgets/canvas_editor.dart';
import 'widgets/inspector_panel.dart';
import 'widgets/element_library_modal.dart';
import 'widgets/design_system_library_modal.dart';

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

  @override
  void initState() {
    super.initState();
    _project = PortfolioProject.createDefaultTemplate();
  }

  DeckSlide get _currentSlide => _project.slides[_activeSlideIndex];

  void _addNewSlide() {
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

  void _openElementLibrary() {
    showDialog(
      context: context,
      builder: (ctx) => ElementLibraryModal(
        onSelectType: (type) {
          _addElementOfType(type);
        },
      ),
    );
  }

  void _addElementOfType(ElementType type) {
    setState(() {
      final id = 'elem_${DateTime.now().millisecondsSinceEpoch}';
      late DeckElement newElem;

      switch (type) {
        case ElementType.header:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '헤더 인디케이터',
            x: 100,
            y: 70,
            width: 1720,
            height: 60,
            props: {
              'badge': '2026 CASE STUDY',
              'meta': '서비스 기획 · UI/UX 디자인 · Android Live',
            },
          );
          break;
        case ElementType.text:
          newElem = DeckElement(
            id: id,
            type: type,
            name: '텍스트 헤드라인',
            x: 100,
            y: 200,
            width: 800,
            height: 140,
            props: {
              'titleBlack': '핵심 타이틀 ',
              'titleBlue': '강조 포인트',
              'subtitle': '상세한 UX 기획 배경 및 문제 해결 과정을 서술합니다.',
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Global App Bar
          _buildGlobalAppBar(),

          // Main Workspace: Slide Thumbnails + Canvas Editor + Inspector Panel
          Expanded(
            child: Row(
              children: [
                // Left: Slide Thumbnails Navigator (Width: 240)
                _buildSlideNavigator(),

                // Center: 1920x1080 Interactive Canvas
                Expanded(
                  child: CanvasEditor(
                    slide: _currentSlide,
                    selectedElement: _selectedElement,
                    onElementSelected: (elem) {
                      setState(() => _selectedElement = elem);
                    },
                    onSlideModified: () {
                      setState(() {});
                    },
                  ),
                ),

                // Right: Inspector Panel (Width: 340)
                InspectorPanel(
                  element: _selectedElement,
                  onElementUpdated: () {
                    setState(() {});
                  },
                  onElementDeleted: () {
                    if (_selectedElement != null) {
                      setState(() {
                        _currentSlide.elements.removeWhere((e) => e.id == _selectedElement!.id);
                        _selectedElement = null;
                      });
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGlobalAppBar() {
    return Container(
      height: 56,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      decoration: const BoxDecoration(
        color: Color(0xFF0F172A),
        border: Border(bottom: BorderSide(color: Color(0xFF1E293B))),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: const Color(0xFF0052FF),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.dashboard_customize, color: Colors.white, size: 18),
          ),
          const SizedBox(width: 12),
          const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'DeckStudio (데스크탑 포트폴리오 에디터)',
                style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
              ),
              Text(
                '도식 · 그래프 · 플로우차트 · 디자인시스템 · 3D 목업 실시간 커스텀 툴',
                style: TextStyle(color: Color(0xFF94A3B8), fontSize: 10),
              ),
            ],
          ),
          const Spacer(),
          ElevatedButton.icon(
            icon: const Icon(Icons.style, size: 16),
            label: const Text('디자인 시스템 라이브러리', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0891B2),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (ctx) => const DesignSystemLibraryModal(),
              );
            },
          ),
          const SizedBox(width: 10),
          ElevatedButton.icon(
            icon: const Icon(Icons.add_box_outlined, size: 16),
            label: const Text('컴포넌트 삽입', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0052FF),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
            onPressed: _openElementLibrary,
          ),
          const SizedBox(width: 10),
          OutlinedButton.icon(
            icon: const Icon(Icons.picture_as_pdf, size: 16),
            label: const Text('Behance 슬라이드 / PDF 내보내기', style: TextStyle(fontSize: 12)),
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.white,
              side: const BorderSide(color: Color(0xFF334155)),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('현재 덱의 모든 슬라이드가 고해상도 1920x1080 규격으로 준비되었습니다.'),
                  backgroundColor: Color(0xFF0052FF),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildSlideNavigator() {
    return Container(
      width: 240,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(right: BorderSide(color: Color(0xFFE2E8F0))),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(16),
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

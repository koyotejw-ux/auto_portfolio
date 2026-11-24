import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../models/deck_model.dart';
import '../utils/flutter_project_parser.dart';

class FlutterProjectLoaderModal extends StatefulWidget {
  final ValueChanged<PortfolioProject> onProjectLoaded;

  const FlutterProjectLoaderModal({super.key, required this.onProjectLoaded});

  @override
  State<FlutterProjectLoaderModal> createState() => _FlutterProjectLoaderModalState();
}

class _FlutterProjectLoaderModalState extends State<FlutterProjectLoaderModal> {
  String? _selectedDirectory;
  bool _isLoading = false;
  List<ParsedFlutterScreen> _parsedScreens = [];
  Set<String> _selectedFiles = {};
  FlutterComponentCategory? _filterCategory; // null = all
  String _statusMessage = '플러터 프로젝트 루트 폴더를 선택해주세요.';

  // Recent sample projects list
  final List<String> _sampleProjects = [
    r'D:\097.flutter_project\average_down_calculator',
    r'D:\097.flutter_project\zeropass',
    r'D:\097.flutter_project\korea_history_quiz',
  ];

  Future<void> _pickDirectory() async {
    final selectedDir = await FilePicker.getDirectoryPath(
      dialogTitle: '로드할 플러터(Flutter) 프로젝트 폴더 선택',
    );
    if (selectedDir != null) {
      _loadDirectory(selectedDir);
    }
  }

  Future<void> _loadDirectory(String path) async {
    setState(() {
      _selectedDirectory = path;
      _isLoading = true;
      _statusMessage = '플러터 전체 소스코드 스캔 및 페이지/모달/바텀시트 분류 중...';
      _parsedScreens = [];
      _selectedFiles = {};
    });

    try {
      final files = await FlutterProjectParser.findScreenFiles(path);
      final parsedList = <ParsedFlutterScreen>[];

      for (final f in files) {
        try {
          final parsed = FlutterProjectParser.parseDartFile(f);
          parsedList.add(parsed);
        } catch (_) {}
      }

      setState(() {
        _isLoading = false;
        _parsedScreens = parsedList;
        _selectedFiles = parsedList.map((s) => s.filePath).toSet();

        final pageCount = parsedList.where((s) => s.category == FlutterComponentCategory.page).length;
        final modalCount = parsedList.where((s) => s.category == FlutterComponentCategory.modal).length;
        final sheetCount = parsedList.where((s) => s.category == FlutterComponentCategory.bottomSheet).length;
        final widgetCount = parsedList.where((s) => s.category == FlutterComponentCategory.widget).length;

        _statusMessage = '총 ${parsedList.length}개 발견 (페이지: $pageCount, 모달: $modalCount, 바텀시트: $sheetCount, 위젯: $widgetCount)';
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _statusMessage = '폴더 분석 중 오류가 발생했습니다: $e';
      });
    }
  }

  void _convertAndImport() {
    if (_selectedFiles.isEmpty) return;

    setState(() => _isLoading = true);

    final selectedScreens = _parsedScreens.where((s) => _selectedFiles.contains(s.filePath)).toList();
    final slides = <DeckSlide>[];

    for (int i = 0; i < selectedScreens.length; i++) {
      final s = selectedScreens[i];
      slides.add(s.toDeckSlide(i + 1));
    }

    if (slides.isEmpty) {
      setState(() {
        _isLoading = false;
        _statusMessage = '선택한 파일에서 UI를 추출하지 못했습니다.';
      });
      return;
    }

    final projName = _selectedDirectory != null
        ? _selectedDirectory!.split(Platform.pathSeparator).last
        : 'Flutter Live UI Project';

    final project = PortfolioProject(
      title: 'Flutter UI: $projName',
      author: 'Flutter Two-Way Sync Engine',
      slides: slides,
    );

    widget.onProjectLoaded(project);
    Navigator.pop(context);
  }

  Color _getCategoryColor(FlutterComponentCategory cat) {
    switch (cat) {
      case FlutterComponentCategory.page:
        return const Color(0xFF0052FF);
      case FlutterComponentCategory.modal:
        return const Color(0xFFA78BFA);
      case FlutterComponentCategory.bottomSheet:
        return const Color(0xFF38BDF8);
      case FlutterComponentCategory.widget:
        return const Color(0xFF10B981);
    }
  }

  IconData _getCategoryIcon(FlutterComponentCategory cat) {
    switch (cat) {
      case FlutterComponentCategory.page:
        return Icons.phone_android;
      case FlutterComponentCategory.modal:
        return Icons.picture_in_picture_alt;
      case FlutterComponentCategory.bottomSheet:
        return Icons.vertical_align_bottom;
      case FlutterComponentCategory.widget:
        return Icons.widgets_outlined;
    }
  }

  @override
  Widget build(BuildContext context) {
    final filteredScreens = _filterCategory == null
        ? _parsedScreens
        : _parsedScreens.where((s) => s.category == _filterCategory).toList();

    return Dialog(
      backgroundColor: const Color(0xFF1E1E1E),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: Color(0xFF333333)),
      ),
      child: Container(
        width: 880,
        height: 680,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Modal Header
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0052FF).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.sync_alt, color: Color(0xFF38BDF8), size: 22),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '플러터(Flutter) 프로젝트 전체 인식 & 양방향 UI 동기화 로더',
                        style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 2),
                      Text(
                        '프로젝트 전체를 인식하여 [페이지], [모달], [바텀시트]별로 캔버스에 생성하며, 수정 후 [저장] 시 Flutter 원본 코드가 실시간 업데이트됩니다.',
                        style: TextStyle(color: Color(0xFFA3A3A3), fontSize: 11),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white70),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Directory Selection Bar
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF141414),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: const Color(0xFF2C2C2C)),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Text(
                      _selectedDirectory ?? '선택된 프로젝트 폴더 없음 (폴더 찾기 버튼을 눌러주세요)',
                      style: TextStyle(
                        color: _selectedDirectory != null ? const Color(0xFF38BDF8) : const Color(0xFF737373),
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  const SizedBox(width: 12),
                  ElevatedButton.icon(
                    icon: const Icon(Icons.folder, size: 16),
                    label: const Text('폴더 찾기', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF0052FF),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    ),
                    onPressed: _isLoading ? null : _pickDirectory,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),

            // Quick Samples Chips
            Row(
              children: [
                const Text('빠른 샘플 로드: ', style: TextStyle(color: Color(0xFF888888), fontSize: 11)),
                const SizedBox(width: 6),
                ..._sampleProjects.map((p) {
                  final name = p.split(Platform.pathSeparator).last;
                  return Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ActionChip(
                      label: Text(name, style: const TextStyle(fontSize: 10, color: Colors.white70)),
                      backgroundColor: const Color(0xFF262626),
                      side: const BorderSide(color: Color(0xFF383838)),
                      visualDensity: VisualDensity.compact,
                      onPressed: _isLoading ? null : () => _loadDirectory(p),
                    ),
                  );
                }),
              ],
            ),
            const SizedBox(height: 12),

            // Category Filter Tabs
            if (_parsedScreens.isNotEmpty)
              Row(
                children: [
                  _buildCategoryFilterChip(null, '전체보기 (${_parsedScreens.length})'),
                  const SizedBox(width: 6),
                  _buildCategoryFilterChip(
                    FlutterComponentCategory.page,
                    '페이지 (${_parsedScreens.where((s) => s.category == FlutterComponentCategory.page).length})',
                  ),
                  const SizedBox(width: 6),
                  _buildCategoryFilterChip(
                    FlutterComponentCategory.modal,
                    '모달 다이얼로그 (${_parsedScreens.where((s) => s.category == FlutterComponentCategory.modal).length})',
                  ),
                  const SizedBox(width: 6),
                  _buildCategoryFilterChip(
                    FlutterComponentCategory.bottomSheet,
                    '바텀시트 (${_parsedScreens.where((s) => s.category == FlutterComponentCategory.bottomSheet).length})',
                  ),
                  const SizedBox(width: 6),
                  _buildCategoryFilterChip(
                    FlutterComponentCategory.widget,
                    '위젯 (${_parsedScreens.where((s) => s.category == FlutterComponentCategory.widget).length})',
                  ),
                ],
              ),
            const SizedBox(height: 10),

            // Content Area: File Selection List
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFF141414),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: const Color(0xFF2C2C2C)),
                ),
                child: _isLoading
                    ? const Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            CircularProgressIndicator(color: Color(0xFF0052FF)),
                            SizedBox(height: 14),
                            Text('Flutter 프로젝트 전체 구조 및 모달/바텀시트 분석 중...', style: TextStyle(color: Colors.white70, fontSize: 12)),
                          ],
                        ),
                      )
                    : _parsedScreens.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.devices, color: Color(0xFF404040), size: 48),
                                const SizedBox(height: 12),
                                Text(_statusMessage, style: const TextStyle(color: Color(0xFFA3A3A3), fontSize: 12)),
                              ],
                            ),
                          )
                        : Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                                decoration: const BoxDecoration(
                                  border: Border(bottom: BorderSide(color: Color(0xFF262626))),
                                ),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      '생성할 캔버스 슬라이드 (${_selectedFiles.length}/${_parsedScreens.length}개 선택됨)',
                                      style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                                    ),
                                    Row(
                                      children: [
                                        TextButton(
                                          onPressed: () {
                                            setState(() => _selectedFiles = _parsedScreens.map((f) => f.filePath).toSet());
                                          },
                                          child: const Text('전체 선택', style: TextStyle(fontSize: 10, color: Color(0xFF38BDF8))),
                                        ),
                                        TextButton(
                                          onPressed: () {
                                            setState(() => _selectedFiles.clear());
                                          },
                                          child: const Text('선택 해제', style: TextStyle(fontSize: 10, color: Color(0xFFEF4444))),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                              Expanded(
                                child: ListView.builder(
                                  itemCount: filteredScreens.length,
                                  itemBuilder: (ctx, idx) {
                                    final screen = filteredScreens[idx];
                                    final isChecked = _selectedFiles.contains(screen.filePath);
                                    final relPath = screen.filePath.replaceAll(r'\', '/');
                                    final catColor = _getCategoryColor(screen.category);
                                    final catIcon = _getCategoryIcon(screen.category);

                                    return CheckboxListTile(
                                      value: isChecked,
                                      dense: true,
                                      activeColor: const Color(0xFF0052FF),
                                      checkColor: Colors.white,
                                      title: Row(
                                        children: [
                                          Container(
                                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                            decoration: BoxDecoration(
                                              color: catColor.withValues(alpha: 0.2),
                                              borderRadius: BorderRadius.circular(4),
                                              border: Border.all(color: catColor, width: 0.8),
                                            ),
                                            child: Text(
                                              screen.categoryLabel,
                                              style: TextStyle(color: catColor, fontSize: 9.5, fontWeight: FontWeight.bold),
                                            ),
                                          ),
                                          const SizedBox(width: 8),
                                          Expanded(
                                            child: Text(
                                              '${screen.screenName} (${screen.fileName})',
                                              style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                                              overflow: TextOverflow.ellipsis,
                                            ),
                                          ),
                                        ],
                                      ),
                                      subtitle: Text(
                                        relPath,
                                        style: const TextStyle(color: Color(0xFF737373), fontSize: 10),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      secondary: Icon(catIcon, color: catColor, size: 18),
                                      onChanged: (val) {
                                        setState(() {
                                          if (val == true) {
                                            _selectedFiles.add(screen.filePath);
                                          } else {
                                            _selectedFiles.remove(screen.filePath);
                                          }
                                        });
                                      },
                                    );
                                  },
                                ),
                              ),
                            ],
                          ),
              ),
            ),
            const SizedBox(height: 16),

            // Bottom Actions
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    _statusMessage,
                    style: const TextStyle(color: Color(0xFF888888), fontSize: 11),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Row(
                  children: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('취소', style: TextStyle(color: Colors.white70)),
                    ),
                    const SizedBox(width: 10),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.sync, size: 16),
                      label: Text(
                        '선택 화면 캔버스 로드 (${_selectedFiles.length}개 화면)',
                        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF0052FF),
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      onPressed: _selectedFiles.isEmpty || _isLoading ? null : _convertAndImport,
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCategoryFilterChip(FlutterComponentCategory? cat, String label) {
    final isSelected = _filterCategory == cat;
    return ActionChip(
      label: Text(
        label,
        style: TextStyle(
          fontSize: 10,
          color: isSelected ? Colors.white : const Color(0xFFA3A3A3),
          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
        ),
      ),
      backgroundColor: isSelected ? const Color(0xFF0052FF) : const Color(0xFF262626),
      side: BorderSide(color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF383838)),
      visualDensity: VisualDensity.compact,
      onPressed: () => setState(() => _filterCategory = cat),
    );
  }
}

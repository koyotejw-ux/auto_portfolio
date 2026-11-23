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
  List<File> _foundFiles = [];
  Set<String> _selectedFiles = {};
  String _statusMessage = '플러터 프로젝트 루트 폴더(또는 lib 폴더)를 선택해주세요.';

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
      _statusMessage = '플러터 Dart 소스코드 및 UI 구조 분석 중...';
      _foundFiles = [];
      _selectedFiles = {};
    });

    try {
      final files = await FlutterProjectParser.findScreenFiles(path);
      // Filter primarily screens and widgets
      final prioritized = files.where((f) {
        final p = f.path.replaceAll(r'\', '/').toLowerCase();
        return p.contains('/screen') || p.contains('/page') || p.contains('/view') || p.contains('/widget') || p.endsWith('main.dart');
      }).toList();

      final displayFiles = prioritized.isNotEmpty ? prioritized : files;

      setState(() {
        _isLoading = false;
        _foundFiles = displayFiles;
        _selectedFiles = displayFiles.map((f) => f.path).toSet();
        _statusMessage = '총 ${displayFiles.length}개의 화면/위젯 파일을 성공적으로 감지했습니다.';
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

    final selectedList = _foundFiles.where((f) => _selectedFiles.contains(f.path)).toList();
    final slides = <DeckSlide>[];

    for (int i = 0; i < selectedList.length; i++) {
      final file = selectedList[i];
      try {
        final parsed = FlutterProjectParser.parseDartFile(file);
        slides.add(parsed.toDeckSlide(i + 1));
      } catch (e) {
        debugPrint('Error parsing ${file.path}: $e');
      }
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
      author: 'Flutter Engine Live Parser',
      slides: slides,
    );

    widget.onProjectLoaded(project);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: const Color(0xFF1E1E1E),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: Color(0xFF333333)),
      ),
      child: Container(
        width: 820,
        height: 640,
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
                  child: const Icon(Icons.folder_open, color: Color(0xFF38BDF8), size: 22),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '플러터(Flutter) 프로젝트 폴더 UI 로더',
                        style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 2),
                      Text(
                        '실제 Flutter 프로젝트의 Dart 소스 코드를 읽어 화면 레이아웃과 컴포넌트 구조를 피그마 캔버스로 즉시 복원합니다.',
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
            const SizedBox(height: 18),

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
            const SizedBox(height: 12),

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
            const SizedBox(height: 14),

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
                            Text('Flutter 프로젝트 UI 구문 분석 중...', style: TextStyle(color: Colors.white70, fontSize: 12)),
                          ],
                        ),
                      )
                    : _foundFiles.isEmpty
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
                                      '불러올 UI 화면 / 위젯 (${_selectedFiles.length}/${_foundFiles.length}개 선택됨)',
                                      style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                                    ),
                                    Row(
                                      children: [
                                        TextButton(
                                          onPressed: () {
                                            setState(() => _selectedFiles = _foundFiles.map((f) => f.path).toSet());
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
                                  itemCount: _foundFiles.length,
                                  itemBuilder: (ctx, idx) {
                                    final file = _foundFiles[idx];
                                    final isChecked = _selectedFiles.contains(file.path);
                                    final fileName = file.uri.pathSegments.last;
                                    final relPath = file.path.replaceAll(r'\', '/');

                                    return CheckboxListTile(
                                      value: isChecked,
                                      dense: true,
                                      activeColor: const Color(0xFF0052FF),
                                      checkColor: Colors.white,
                                      title: Text(
                                        fileName,
                                        style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                                      ),
                                      subtitle: Text(
                                        relPath,
                                        style: const TextStyle(color: Color(0xFF737373), fontSize: 10),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      secondary: const Icon(Icons.phone_android, color: Color(0xFF38BDF8), size: 16),
                                      onChanged: (val) {
                                        setState(() {
                                          if (val == true) {
                                            _selectedFiles.add(file.path);
                                          } else {
                                            _selectedFiles.remove(file.path);
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
                Text(
                  _statusMessage,
                  style: const TextStyle(color: Color(0xFF888888), fontSize: 11),
                ),
                Row(
                  children: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('취소', style: TextStyle(color: Colors.white70)),
                    ),
                    const SizedBox(width: 10),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.download_done, size: 16),
                      label: Text(
                        '캔버스에 UI 복원 및 편집 모드 시작 (${_selectedFiles.length}개 화면)',
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
}

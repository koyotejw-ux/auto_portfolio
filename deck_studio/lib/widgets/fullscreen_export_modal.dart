import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/deck_model.dart';
import '../utils/deck_pdf_exporter.dart';
import '../utils/deck_web_html_exporter.dart';
import '../utils/deck_flutter_web_exporter.dart';

class FullscreenExportModal extends StatefulWidget {
  final PortfolioProject project;

  const FullscreenExportModal({super.key, required this.project});

  @override
  State<FullscreenExportModal> createState() => _FullscreenExportModalState();
}

class _FullscreenExportModalState extends State<FullscreenExportModal> {
  bool _isExporting = false;
  String? _statusMessage;
  String? _lastExportedPath;

  Future<void> _exportPdf() async {
    setState(() {
      _isExporting = true;
      _statusMessage = '고해상도 16:9 PDF 문서를 생성하는 중입니다...';
    });

    try {
      final outDir = Directory('d:/097.flutter_project/auto_portfolio/export_output');
      if (!outDir.existsSync()) outDir.createSync(recursive: true);

      final outPath = '${outDir.path}/SmartDCA_Portfolio_Deck.pdf';
      final file = await DeckPdfExporter.exportProjectToPdf(
        project: widget.project,
        outputPath: outPath,
      );

      setState(() {
        _isExporting = false;
        _lastExportedPath = file.path;
        _statusMessage = 'PDF 문서가 성공적으로 생성되었습니다! (${(file.lengthSync() / 1024 / 1024).toStringAsFixed(2)} MB)';
      });
    } catch (e) {
      setState(() {
        _isExporting = false;
        _statusMessage = 'PDF 출력 중 오류가 발생했습니다: $e';
      });
    }
  }

  Future<void> _exportHtml() async {
    setState(() {
      _isExporting = true;
      _statusMessage = '반응형 풀스크린 HTML 프레젠테이션을 생성하는 중입니다...';
    });

    try {
      final outDir = Directory('d:/097.flutter_project/auto_portfolio/export_output');
      if (!outDir.existsSync()) outDir.createSync(recursive: true);

      final outPath = '${outDir.path}/index_fullscreen.html';
      final file = await DeckWebHtmlExporter.exportProjectToHtml(
        project: widget.project,
        outputPath: outPath,
      );

      setState(() {
        _isExporting = false;
        _lastExportedPath = file.path;
        _statusMessage = '전체화면 HTML 프레젠테이션이 준비되었습니다! 브라우저에서 바로 열 수 있습니다.';
      });
    } catch (e) {
      setState(() {
        _isExporting = false;
        _statusMessage = 'HTML 출력 중 오류가 발생했습니다: $e';
      });
    }
  }

  Future<void> _exportFlutterWeb() async {
    setState(() {
      _isExporting = true;
      _statusMessage = '60fps Flutter Web 엔진 소스코드를 빌드하는 중입니다...';
    });

    try {
      final outDir = Directory('d:/097.flutter_project/auto_portfolio/export_output/flutter_web');
      if (!outDir.existsSync()) outDir.createSync(recursive: true);

      final outPath = '${outDir.path}/deck_presentation_web.dart';
      final file = await DeckFlutterWebExporter.exportProjectToFlutterWeb(
        project: widget.project,
        outputDartPath: outPath,
      );

      setState(() {
        _isExporting = false;
        _lastExportedPath = file.path;
        _statusMessage = 'Flutter Web 독립 실행 엔트리 소스코드가 생성되었습니다!';
      });
    } catch (e) {
      setState(() {
        _isExporting = false;
        _statusMessage = 'Flutter Web 소스 생성 오류: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      backgroundColor: const Color(0xFF0F172A),
      child: Container(
        width: 680,
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Modal Header
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0052FF),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.output_rounded, color: Colors.white, size: 20),
                ),
                const SizedBox(width: 14),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '전체화면 포트폴리오 멀티 포맷 출력 센터',
                      style: TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '${widget.project.title} (${widget.project.slides.length}개 슬라이드 전체)',
                      style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11),
                    ),
                  ],
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.close, color: Color(0xFF94A3B8)),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),

            const SizedBox(height: 24),
            const Text(
              '원하는 출력 포맷을 선택하세요. 16:9 고해상도 규격으로 즉시 렌더링되어 파일로 생성됩니다.',
              style: TextStyle(color: Color(0xFFCBD5E1), fontSize: 13),
            ),
            const SizedBox(height: 20),

            // 3 Format Cards
            Row(
              children: [
                // 1. PDF Document
                Expanded(
                  child: _buildExportCard(
                    icon: Icons.picture_as_pdf,
                    color: const Color(0xFFEF4444),
                    title: 'PDF 문서 출력',
                    desc: '16:9 표준 와이드스크린 규격\n인쇄 및 Behance 업로드용',
                    buttonText: 'PDF 내보내기',
                    onTap: _exportPdf,
                  ),
                ),
                const SizedBox(width: 14),

                // 2. Fullscreen HTML Web
                Expanded(
                  child: _buildExportCard(
                    icon: Icons.html,
                    color: const Color(0xFF06B6D4),
                    title: '전체화면 HTML 웹',
                    desc: '자체 반응형 16:9 뷰포트\n단독 실행 웹 프레젠테이션',
                    buttonText: 'HTML 내보내기',
                    onTap: _exportHtml,
                  ),
                ),
                const SizedBox(width: 14),

                // 3. Flutter Web Engine
                Expanded(
                  child: _buildExportCard(
                    icon: Icons.flutter_dash,
                    color: const Color(0xFF0052FF),
                    title: 'Flutter Web 엔진',
                    desc: '60fps 무지연 인터랙션\n독립 플러터 웹 앱 소스',
                    buttonText: 'Flutter 웹 출력',
                    onTap: _exportFlutterWeb,
                  ),
                ),
              ],
            ),

            if (_isExporting) ...[
              const SizedBox(height: 20),
              const Center(
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF0052FF))),
                    SizedBox(width: 12),
                    Text('문서를 렌더링하고 변환하는 중입니다...', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12)),
                  ],
                ),
              ),
            ],

            if (_statusMessage != null) ...[
              const SizedBox(height: 20),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFF334155)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.check_circle_outline, color: Color(0xFF10B981), size: 18),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        _statusMessage!,
                        style: const TextStyle(color: Color(0xFFE2E8F0), fontSize: 12),
                      ),
                    ),
                    if (_lastExportedPath != null)
                      IconButton(
                        icon: const Icon(Icons.copy, size: 16, color: Color(0xFF38BDF8)),
                        tooltip: '파일 경로 복사',
                        onPressed: () {
                          Clipboard.setData(ClipboardData(text: _lastExportedPath!));
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('경로가 클립보드에 복사되었습니다.')),
                          );
                        },
                      ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildExportCard({
    required IconData icon,
    required Color color,
    required String title,
    required String desc,
    required String buttonText,
    required VoidCallback onTap,
  }) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF334155)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: color, size: 24),
          ),
          const SizedBox(height: 12),
          Text(title, style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
          const SizedBox(height: 6),
          Text(desc, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11, height: 1.4)),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: color,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 10),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
                elevation: 0,
              ),
              onPressed: _isExporting ? null : onTap,
              child: Text(buttonText, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            ),
          ),
        ],
      ),
    );
  }
}


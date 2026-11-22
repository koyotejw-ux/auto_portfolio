import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CodeExportModal extends StatefulWidget {
  final String flutterCode;
  final String htmlCode;
  final String figmaCode;
  final String elementName;

  const CodeExportModal({
    super.key,
    required this.flutterCode,
    required this.htmlCode,
    required this.figmaCode,
    required this.elementName,
  });

  @override
  State<CodeExportModal> createState() => _CodeExportModalState();
}

class _CodeExportModalState extends State<CodeExportModal> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _copyToClipboard(String code, String type) {
    Clipboard.setData(ClipboardData(text: code));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$type 코드가 클립보드에 복사되었습니다! 원하는 곳에 바로 붙여넣으세요.'),
        backgroundColor: const Color(0xFF0052FF),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 820,
        height: 620,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Modal Top Header
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: const Color(0xFFEFF6FF),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.code, color: Color(0xFF0052FF), size: 20),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '원클릭 소스 코드 & 디자인 복사 (${widget.elementName})',
                        style: const TextStyle(
                          color: Color(0xFF0F172A),
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 2),
                      const Text(
                        'Flutter 위젯, HTML/Tailwind, Figma 속성 규격을 복사하여 즉시 개발 및 디자인에 적용하세요.',
                        style: TextStyle(color: Color(0xFF64748B), fontSize: 11),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Tab Bar
            Container(
              decoration: BoxDecoration(
                color: const Color(0xFFF1F5F9),
                borderRadius: BorderRadius.circular(8),
              ),
              child: TabBar(
                controller: _tabController,
                labelColor: const Color(0xFF0052FF),
                unselectedLabelColor: const Color(0xFF64748B),
                indicatorColor: const Color(0xFF0052FF),
                indicatorSize: TabBarIndicatorSize.tab,
                tabs: const [
                  Tab(icon: Icon(Icons.flutter_dash, size: 16), text: 'Flutter 위젯 코드'),
                  Tab(icon: Icon(Icons.html, size: 18), text: 'HTML / Tailwind CSS'),
                  Tab(icon: Icon(Icons.draw, size: 16), text: 'Figma 디자인 스펙 & JSON'),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Tab Views with Code Block & Copy Button
            Expanded(
              child: TabBarView(
                controller: _tabController,
                children: [
                  _buildCodePane(widget.flutterCode, 'Flutter'),
                  _buildCodePane(widget.htmlCode, 'HTML/Tailwind'),
                  _buildCodePane(widget.figmaCode, 'Figma Spec'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCodePane(String code, String type) {
    return Column(
      children: [
        // Action Bar
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '$type 소스 규격 (Ready to Paste)',
              style: const TextStyle(color: Color(0xFF475569), fontSize: 12, fontWeight: FontWeight.bold),
            ),
            ElevatedButton.icon(
              icon: const Icon(Icons.content_copy, size: 14),
              label: Text('$type 코드 복사', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0052FF),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
              onPressed: () => _copyToClipboard(code, type),
            ),
          ],
        ),
        const SizedBox(height: 10),

        // Code Viewer Block
        Expanded(
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFF0F172A),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: const Color(0xFF1E293B)),
            ),
            child: SingleChildScrollView(
              child: SelectableText(
                code,
                style: const TextStyle(
                  fontFamily: 'Consolas',
                  fontSize: 12,
                  color: Color(0xFFE2E8F0),
                  height: 1.45,
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}


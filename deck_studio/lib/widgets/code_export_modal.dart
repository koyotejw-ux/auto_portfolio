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
        content: Row(
          children: [
            const Icon(Icons.check_circle, color: Colors.white, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                '하위 컴포넌트 전체가 포함된 $type 소스 코드가 클립보드에 복사되었습니다! 원하는 디자인 툴이나 코드 에디터에 바로 붙여넣으세요.',
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        backgroundColor: const Color(0xFF0052FF),
        duration: const Duration(seconds: 3),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 860,
        height: 640,
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
                  child: const Icon(Icons.account_tree_outlined, color: Color(0xFF0052FF), size: 20),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Flexible(
                            child: Text(
                              '컴포넌트 단위 소스 코드 복사 · ${widget.elementName}',
                              style: const TextStyle(
                                color: Color(0xFF0F172A),
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: const Color(0xFF0052FF).withOpacity(0.1),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Text(
                              '하위 계층 트리 전체 포함',
                              style: TextStyle(color: Color(0xFF0052FF), fontSize: 10, fontWeight: FontWeight.bold),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 2),
                      const Text(
                        '선택된 프레임 및 하위 자식 요소(AutoLayout, 텍스트, 카드, 뱃지 등) 전체가 결합된 완전한 컴포넌트 단위 소스입니다.',
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
                  Tab(icon: Icon(Icons.draw, size: 16), text: 'Figma 디자인 스펙 & JSON'),
                  Tab(icon: Icon(Icons.flutter_dash, size: 16), text: 'Flutter 계층형 위젯 코드'),
                  Tab(icon: Icon(Icons.html, size: 18), text: 'HTML / Tailwind CSS'),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Tab Views with Code Block & Copy Button
            Expanded(
              child: TabBarView(
                controller: _tabController,
                children: [
                  _buildCodePane(widget.figmaCode, 'Figma 컴포넌트 스펙', 'Figma Inspect 및 Tokens Studio에 붙여넣어 AutoLayout Frame 복원'),
                  _buildCodePane(widget.flutterCode, 'Flutter 컴포넌트 코드', 'Flutter 프로젝트에 바로 붙여넣어 StatelessWidget 컴포넌트로 사용'),
                  _buildCodePane(widget.htmlCode, 'HTML/Tailwind 컴포넌트', '웹 페이지 및 반응형 웹 레이아웃에 직접 붙여넣기'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCodePane(String code, String type, String desc) {
    return Column(
      children: [
        // Action Bar
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: const Color(0xFFE2E8F0)),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$type (하위 자식 요소 트리 포함)',
                      style: const TextStyle(color: Color(0xFF0F172A), fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      desc,
                      style: const TextStyle(color: Color(0xFF64748B), fontSize: 10.5),
                    ),
                  ],
                ),
              ),
              ElevatedButton.icon(
                icon: const Icon(Icons.content_copy, size: 14),
                label: Text('$type 복사', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
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

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../utils/figma_design_system_exporter.dart';

class DesignSystemLibraryModal extends StatefulWidget {
  const DesignSystemLibraryModal({super.key});

  @override
  State<DesignSystemLibraryModal> createState() => _DesignSystemLibraryModalState();
}

class _DesignSystemLibraryModalState extends State<DesignSystemLibraryModal> with SingleTickerProviderStateMixin {
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

  void _copy(String text, String label) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$label 규격이 클립보드에 복사되었습니다! Figma 또는 CSS에 바로 붙여넣으세요.'),
        backgroundColor: const Color(0xFF0052FF),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final fullCss = FigmaDesignSystemExporter.generateFullFigmaDesignSystem();
    final jsonTokens = FigmaDesignSystemExporter.generateFigmaTokensJson();

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 880,
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
                  child: const Icon(Icons.style, color: Color(0xFF0052FF), size: 22),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '디자인 시스템 파운데이션 & 컴포넌트 라이브러리',
                        style: TextStyle(
                          color: Color(0xFF0F172A),
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 2),
                      Text(
                        'Figma 및 프론트엔드 개발에 1초 만에 복사하여 즉시 사용할 수 있는 전체 토큰 & 컴포넌트 셋',
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
                  Tab(icon: Icon(Icons.view_quilt, size: 16), text: '컴포넌트 라이브러리 뷰'),
                  Tab(icon: Icon(Icons.css, size: 18), text: 'Figma / CSS 변수 토큰'),
                  Tab(icon: Icon(Icons.data_object, size: 16), text: 'Figma Tokens JSON'),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Tab Views
            Expanded(
              child: TabBarView(
                controller: _tabController,
                children: [
                  _buildVisualComponentViewer(),
                  _buildCodePane(fullCss, 'Figma / CSS 디자인 시스템'),
                  _buildCodePane(jsonTokens, 'Figma Tokens JSON'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildVisualComponentViewer() {
    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      children: [
        // 1. Color Palette Swatches
        _buildSectionHeader('1. 브랜드 & 시맨틱 컬러 팔레트 (WCAG AAA 12.8:1)'),
        const SizedBox(height: 8),
        Row(
          children: [
            _buildColorSwatch('Primary Blue', '#0052FF', const Color(0xFF0052FF)),
            _buildColorSwatch('Cyber Cyan', '#0891B2', const Color(0xFF0891B2)),
            _buildColorSwatch('Success', '#10B981', const Color(0xFF10B981)),
            _buildColorSwatch('Warning', '#F59E0B', const Color(0xFFF59E0B)),
            _buildColorSwatch('Overdue Red', '#EF4444', const Color(0xFFEF4444)),
            _buildColorSwatch('Obsidian Dark', '#0F172A', const Color(0xFF0F172A)),
          ],
        ),
        const SizedBox(height: 20),

        // 2. Buttons & CTAs
        _buildSectionHeader('2. 아토믹 인터랙티브 컴포넌트 (Buttons & Badges)'),
        const SizedBox(height: 12),
        Wrap(
          spacing: 12,
          runSpacing: 10,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            ElevatedButton.icon(
              icon: const Icon(Icons.check_circle_outline, size: 16),
              label: const Text('0.8초 등원 인증 (Primary)'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0052FF),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              onPressed: () {},
            ),
            OutlinedButton.icon(
              icon: const Icon(Icons.send_outlined, size: 16),
              label: const Text('원클릭 카톡 청구서 (Secondary)'),
              style: OutlinedButton.styleFrom(
                foregroundColor: const Color(0xFF0052FF),
                side: const BorderSide(color: Color(0xFF0052FF)),
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              onPressed: () {},
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: const Color(0xFFFFFBEB),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFFFDE68A)),
              ),
              child: const Text('D-7 만료 임박', style: TextStyle(color: Color(0xFFF59E0B), fontSize: 11, fontWeight: FontWeight.bold)),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: const Color(0xFFECFDF5),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFFA7F3D0)),
              ),
              child: const Text('출결 완료 (12회 완납)', style: TextStyle(color: Color(0xFF10B981), fontSize: 11, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
        const SizedBox(height: 20),

        // 3. Kiosk Tenkey Dial Key
        _buildSectionHeader('3. 10인치 태블릿 키오스크 116dp 텐키 다이얼 버튼'),
        const SizedBox(height: 12),
        Row(
          children: [
            _buildDialKey('1'),
            const SizedBox(width: 12),
            _buildDialKey('2'),
            const SizedBox(width: 12),
            _buildDialKey('3'),
            const SizedBox(width: 20),
            const Expanded(
              child: Text(
                '• 116dp 그리드로 유아/저학년도 오터치 원천 차단\n• 10ms 인덱싱 및 네온 글로우 햅틱 피드백\n• 다크 옵시디언 고대비 테마(시인성 100%)',
                style: TextStyle(color: Color(0xFF64748B), fontSize: 12, height: 1.5),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildSectionHeader(String title) {
    return Text(
      title,
      style: const TextStyle(
        color: Color(0xFF0F172A),
        fontSize: 13,
        fontWeight: FontWeight.bold,
      ),
    );
  }

  Widget _buildColorSwatch(String name, String hex, Color color) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.only(right: 8),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: Colors.black12),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              name,
              style: TextStyle(
                color: color.computeLuminance() > 0.5 ? Colors.black87 : Colors.white,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
              maxLines: 1,
            ),
            const SizedBox(height: 2),
            Text(
              hex,
              style: TextStyle(
                color: color.computeLuminance() > 0.5 ? Colors.black54 : Colors.white70,
                fontSize: 9,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDialKey(String num) {
    return Container(
      width: 60,
      height: 60,
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: Colors.white24),
        boxShadow: const [
          BoxShadow(color: Colors.black26, blurRadius: 8, offset: Offset(0, 4)),
        ],
      ),
      child: Center(
        child: Text(
          num,
          style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w900),
        ),
      ),
    );
  }

  Widget _buildCodePane(String code, String type) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '$type 전체 코드 (Ready to Paste)',
              style: const TextStyle(color: Color(0xFF475569), fontSize: 12, fontWeight: FontWeight.bold),
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
              onPressed: () => _copy(code, type),
            ),
          ],
        ),
        const SizedBox(height: 10),
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
                  fontSize: 11.5,
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


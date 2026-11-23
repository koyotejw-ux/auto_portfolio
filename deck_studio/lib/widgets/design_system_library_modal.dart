import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import '../utils/figma_design_system_exporter.dart';

class DesignSystemVariable {
  String name;
  String group; // 'Colors', 'Spacing', 'Typography', 'Radius'
  String type;  // 'COLOR', 'FLOAT', 'STRING'
  dynamic value;
  String description;

  DesignSystemVariable({
    required this.name,
    required this.group,
    required this.type,
    required this.value,
    this.description = '',
  });
}

class DesignSystemLibraryModal extends StatefulWidget {
  const DesignSystemLibraryModal({super.key});

  @override
  State<DesignSystemLibraryModal> createState() => _DesignSystemLibraryModalState();
}

class _DesignSystemLibraryModalState extends State<DesignSystemLibraryModal> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  String _selectedGroup = 'All';
  String _searchQuery = '';

  // Figma Local Variables State (동적 수정 및 관리 가능)
  final List<DesignSystemVariable> _variables = [
    DesignSystemVariable(name: 'brand.primary', group: 'Colors', type: 'COLOR', value: const Color(0xFF0052FF), description: '시그니처 일렉트릭 블루 (WCAG AAA 12.8:1)'),
    DesignSystemVariable(name: 'brand.primary-light', group: 'Colors', type: 'COLOR', value: const Color(0xFFEFF6FF), description: '블루 연무 서피스'),
    DesignSystemVariable(name: 'brand.primary-border', group: 'Colors', type: 'COLOR', value: const Color(0xFFBFDBFE), description: '포커스 테두리 라인'),
    DesignSystemVariable(name: 'accent.cyber-cyan', group: 'Colors', type: 'COLOR', value: const Color(0xFF0891B2), description: '키오스크 & 프로 하이라이트'),
    DesignSystemVariable(name: 'semantic.success', group: 'Colors', type: 'COLOR', value: const Color(0xFF10B981), description: '출결 완료 및 완납 그린'),
    DesignSystemVariable(name: 'semantic.warning', group: 'Colors', type: 'COLOR', value: const Color(0xFFF59E0B), description: 'D-Day 만료 임박 경고 앰버'),
    DesignSystemVariable(name: 'semantic.danger', group: 'Colors', type: 'COLOR', value: const Color(0xFFEF4444), description: '미수금 연체 독촉 레드'),
    DesignSystemVariable(name: 'surface.obsidian', group: 'Colors', type: 'COLOR', value: const Color(0xFF0F172A), description: '옵시디언 다크 헤더 서피스'),
    DesignSystemVariable(name: 'surface.card', group: 'Colors', type: 'COLOR', value: const Color(0xFFFFFFFF), description: '퓨어 화이트 카드 서피스'),
    DesignSystemVariable(name: 'surface.bg', group: 'Colors', type: 'COLOR', value: const Color(0xFFF8FAFC), description: '뉴트럴 캔버스 배경'),
    DesignSystemVariable(name: 'border.hairline', group: 'Colors', type: 'COLOR', value: const Color(0xFFE2E8F0), description: '헤어라인 보더 컬러'),
    DesignSystemVariable(name: 'text.primary', group: 'Colors', type: 'COLOR', value: const Color(0xFF0F172A), description: '본문 및 타이틀 블랙'),
    DesignSystemVariable(name: 'text.muted', group: 'Colors', type: 'COLOR', value: const Color(0xFF64748B), description: '보조 설명 슬레이트 그레이'),

    DesignSystemVariable(name: 'spacing.xs', group: 'Spacing', type: 'FLOAT', value: 4.0, description: '4pt 극소 간격'),
    DesignSystemVariable(name: 'spacing.sm', group: 'Spacing', type: 'FLOAT', value: 8.0, description: '8pt 기본 간격'),
    DesignSystemVariable(name: 'spacing.md', group: 'Spacing', type: 'FLOAT', value: 16.0, description: '16pt 카드 내부 패딩'),
    DesignSystemVariable(name: 'spacing.lg', group: 'Spacing', type: 'FLOAT', value: 24.0, description: '24pt 섹션 간격'),
    DesignSystemVariable(name: 'spacing.xl', group: 'Spacing', type: 'FLOAT', value: 32.0, description: '32pt 대형 그리드 갭'),

    DesignSystemVariable(name: 'radius.sm', group: 'Radius', type: 'FLOAT', value: 8.0, description: '태그, 뱃지, 다이얼 서브박스'),
    DesignSystemVariable(name: 'radius.md', group: 'Radius', type: 'FLOAT', value: 12.0, description: '버튼, 인풋 필드, 다이얼로그'),
    DesignSystemVariable(name: 'radius.lg', group: 'Radius', type: 'FLOAT', value: 16.0, description: '메인 카드, 수납 장부 서피스'),
    DesignSystemVariable(name: 'radius.xl', group: 'Radius', type: 'FLOAT', value: 24.0, description: '바텀시트, 키오스크 패드'),

    DesignSystemVariable(name: 'font.family', group: 'Typography', type: 'STRING', value: 'Pretendard', description: '글로벌 디스플레이 폰트'),
    DesignSystemVariable(name: 'font.hero.size', group: 'Typography', type: 'FLOAT', value: 56.0, description: '히어로 헤드라인 크기'),
    DesignSystemVariable(name: 'font.title1.size', group: 'Typography', type: 'FLOAT', value: 32.0, description: '타이틀 1 크기'),
    DesignSystemVariable(name: 'font.title2.size', group: 'Typography', type: 'FLOAT', value: 24.0, description: '타이틀 2 크기'),
    DesignSystemVariable(name: 'font.body.size', group: 'Typography', type: 'FLOAT', value: 14.0, description: '본문 텍스트 크기'),
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
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
        content: Text('$label 규격이 클립보드에 복사되었습니다! Figma에 바로 붙여넣으세요.'),
        backgroundColor: const Color(0xFF0052FF),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _addNewVariableDialog() {
    String varName = '';
    String varGroup = 'Colors';
    String varType = 'COLOR';
    dynamic varValue = const Color(0xFF0052FF);
    String varDesc = '';

    showDialog(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          backgroundColor: Colors.white,
          title: const Row(
            children: [
              Icon(Icons.add_circle_outline, color: Color(0xFF0052FF), size: 20),
              SizedBox(width: 8),
              Text('새 Figma 변수 (Variable) 생성', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
            ],
          ),
          content: SingleChildScrollView(
            child: SizedBox(
              width: 400,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('변수 이름 (예: brand.accent)', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Color(0xFF475569))),
                  const SizedBox(height: 6),
                  TextFormField(
                    decoration: const InputDecoration(isDense: true, border: OutlineInputBorder(), hintText: 'component.button.bg'),
                    style: const TextStyle(fontSize: 12),
                    onChanged: (v) => varName = v,
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('컬렉션 / 그룹', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Color(0xFF475569))),
                            const SizedBox(height: 6),
                            DropdownButtonFormField<String>(
                              value: varGroup,
                              isExpanded: true,
                              decoration: const InputDecoration(isDense: true, border: OutlineInputBorder()),
                              items: ['Colors', 'Spacing', 'Radius', 'Typography']
                                  .map((g) => DropdownMenuItem(value: g, child: Text(g, style: const TextStyle(fontSize: 12))))
                                  .toList(),
                              onChanged: (v) {
                                if (v != null) {
                                  setDialogState(() {
                                    varGroup = v;
                                    if (v == 'Colors') {
                                      varType = 'COLOR';
                                      varValue = const Color(0xFF0052FF);
                                    } else if (v == 'Spacing' || v == 'Radius') {
                                      varType = 'FLOAT';
                                      varValue = 16.0;
                                    } else {
                                      varType = 'STRING';
                                      varValue = 'Pretendard';
                                    }
                                  });
                                }
                              },
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('타입', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Color(0xFF475569))),
                            const SizedBox(height: 6),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                              decoration: BoxDecoration(
                                color: const Color(0xFFF1F5F9),
                                borderRadius: BorderRadius.circular(4),
                                border: Border.all(color: const Color(0xFFCBD5E1)),
                              ),
                              child: Text(varType, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF0F172A))),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  const Text('설명 (Description)', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Color(0xFF475569))),
                  const SizedBox(height: 6),
                  TextFormField(
                    decoration: const InputDecoration(isDense: true, border: OutlineInputBorder(), hintText: '용도 및 적용 가이드 서술'),
                    style: const TextStyle(fontSize: 12),
                    onChanged: (v) => varDesc = v,
                  ),
                ],
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('취소'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0052FF), foregroundColor: Colors.white),
              onPressed: () {
                if (varName.trim().isEmpty) return;
                setState(() {
                  _variables.add(DesignSystemVariable(
                    name: varName.trim(),
                    group: varGroup,
                    type: varType,
                    value: varValue,
                    description: varDesc.trim(),
                  ));
                });
                Navigator.pop(ctx);
              },
              child: const Text('생성 완료'),
            ),
          ],
        ),
      ),
    );
  }

  void _editColorVariable(DesignSystemVariable variable) {
    Color pickerColor = variable.value is Color ? variable.value as Color : const Color(0xFF0052FF);
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('${variable.name} 컬러 수정', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
        content: SingleChildScrollView(
          child: ColorPicker(
            pickerColor: pickerColor,
            onColorChanged: (c) => pickerColor = c,
            enableAlpha: false,
            displayThumbColor: true,
          ),
        ),
        actions: [
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0052FF), foregroundColor: Colors.white),
            child: const Text('적용 완료'),
            onPressed: () {
              setState(() => variable.value = pickerColor);
              Navigator.pop(ctx);
            },
          ),
        ],
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
        width: 980,
        height: 700,
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
                    color: const Color(0xFF0F172A),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.tune, color: Color(0xFF38BDF8), size: 20),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Figma Local Variables & 디자인 시스템 관리자',
                        style: TextStyle(
                          color: Color(0xFF0F172A),
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 2),
                      Text(
                        '피그마 표준 로컬 변수(Local Variables), 색상 토큰, 간격, 곡률, 타이포그래피 실시간 직접 입력 및 수정 관리',
                        style: TextStyle(color: Color(0xFF64748B), fontSize: 11),
                      ),
                    ],
                  ),
                ),
                ElevatedButton.icon(
                  icon: const Icon(Icons.add, size: 14),
                  label: const Text('새 변수 추가 (Create Variable)', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0052FF),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  onPressed: _addNewVariableDialog,
                ),
                const SizedBox(width: 8),
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
                  Tab(icon: Icon(Icons.tune, size: 16), text: 'Figma Local Variables (변수 관리)'),
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
                  _buildFigmaVariablesManager(),
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

  Widget _buildFigmaVariablesManager() {
    final filtered = _variables.where((v) {
      final matchesGroup = _selectedGroup == 'All' || v.group == _selectedGroup;
      final matchesQuery = _searchQuery.isEmpty ||
          v.name.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          v.description.toLowerCase().contains(_searchQuery.toLowerCase());
      return matchesGroup && matchesQuery;
    }).toList();

    return Column(
      children: [
        // Filter toolbar
        Row(
          children: [
            // Group chips
            ...['All', 'Colors', 'Spacing', 'Radius', 'Typography'].map((g) {
              final isSel = _selectedGroup == g;
              return Padding(
                padding: const EdgeInsets.only(right: 6),
                child: ChoiceChip(
                  label: Text(g, style: TextStyle(fontSize: 11, fontWeight: isSel ? FontWeight.bold : FontWeight.normal)),
                  selected: isSel,
                  selectedColor: const Color(0xFFEFF6FF),
                  backgroundColor: const Color(0xFFF8FAFC),
                  onSelected: (val) {
                    if (val) setState(() => _selectedGroup = g);
                  },
                ),
              );
            }),
            const Spacer(),
            SizedBox(
              width: 220,
              height: 34,
              child: TextField(
                decoration: InputDecoration(
                  hintText: '변수 검색 (Search tokens)...',
                  hintStyle: const TextStyle(fontSize: 11),
                  prefixIcon: const Icon(Icons.search, size: 16),
                  contentPadding: EdgeInsets.zero,
                  isDense: true,
                  filled: true,
                  fillColor: const Color(0xFFF8FAFC),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(6), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
                ),
                style: const TextStyle(fontSize: 11),
                onChanged: (q) => setState(() => _searchQuery = q),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),

        // Variable Table Header
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: BoxDecoration(
            color: const Color(0xFF0F172A),
            borderRadius: BorderRadius.circular(8),
          ),
          child: const Row(
            children: [
              SizedBox(width: 200, child: Text('변수 이름 (Variable)', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold))),
              SizedBox(width: 100, child: Text('타입', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold))),
              SizedBox(width: 180, child: Text('현재 값 (Value / Color)', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold))),
              Expanded(child: Text('용도 설명 (Description)', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold))),
              SizedBox(width: 50, child: Text('삭제', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold))),
            ],
          ),
        ),
        const SizedBox(height: 6),

        // Variable Table Body
        Expanded(
          child: ListView.separated(
            itemCount: filtered.length,
            separatorBuilder: (ctx, i) => const Divider(height: 1, color: Color(0xFFE2E8F0)),
            itemBuilder: (ctx, i) {
              final v = filtered[i];
              return Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                color: i % 2 == 0 ? Colors.white : const Color(0xFFF8FAFC),
                child: Row(
                  children: [
                    SizedBox(
                      width: 200,
                      child: Row(
                        children: [
                          Icon(
                            v.type == 'COLOR'
                                ? Icons.circle
                                : (v.type == 'FLOAT' ? Icons.straighten : Icons.text_fields),
                            size: 14,
                            color: const Color(0xFF0052FF),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              v.name,
                              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF0F172A)),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(
                      width: 100,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: const Color(0xFFEFF6FF),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(v.type, style: const TextStyle(fontSize: 9.5, fontWeight: FontWeight.bold, color: Color(0xFF0052FF))),
                      ),
                    ),
                    SizedBox(
                      width: 180,
                      child: v.type == 'COLOR' && v.value is Color
                          ? InkWell(
                              onTap: () => _editColorVariable(v),
                              borderRadius: BorderRadius.circular(4),
                              child: Row(
                                children: [
                                  Container(
                                    width: 22,
                                    height: 22,
                                    decoration: BoxDecoration(
                                      color: v.value as Color,
                                      borderRadius: BorderRadius.circular(4),
                                      border: Border.all(color: Colors.black26),
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    '#${(v.value as Color).toARGB32().toRadixString(16).padLeft(8, '0').substring(2).toUpperCase()}',
                                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                  const SizedBox(width: 4),
                                  const Icon(Icons.edit, size: 12, color: Color(0xFF64748B)),
                                ],
                              ),
                            )
                          : TextFormField(
                              initialValue: v.value.toString(),
                              style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                              decoration: const InputDecoration(isDense: true, contentPadding: EdgeInsets.symmetric(horizontal: 6, vertical: 4), border: OutlineInputBorder()),
                              onChanged: (text) {
                                if (v.type == 'FLOAT') {
                                  final parsed = double.tryParse(text);
                                  if (parsed != null) v.value = parsed;
                                } else {
                                  v.value = text;
                                }
                              },
                            ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        v.description,
                        style: const TextStyle(fontSize: 11, color: Color(0xFF64748B)),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    SizedBox(
                      width: 50,
                      child: IconButton(
                        icon: const Icon(Icons.delete_outline, color: Color(0xFFEF4444), size: 16),
                        onPressed: () {
                          setState(() => _variables.remove(v));
                        },
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
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



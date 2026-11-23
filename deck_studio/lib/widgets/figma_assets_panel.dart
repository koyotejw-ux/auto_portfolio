import 'package:flutter/material.dart';
import '../models/deck_model.dart';
import 'icon_drawing_modal.dart';

enum AssetDragType { color, icon, component }

class AssetDragData {
  final AssetDragType type;
  final String title;
  final dynamic payload;

  AssetDragData({required this.type, required this.title, required this.payload});
}

class FigmaAssetsPanel extends StatefulWidget {
  final ValueChanged<DeckElement> onAddElement;

  const FigmaAssetsPanel({super.key, required this.onAddElement});

  @override
  State<FigmaAssetsPanel> createState() => _FigmaAssetsPanelState();
}

class _FigmaAssetsPanelState extends State<FigmaAssetsPanel> {
  String _searchQuery = '';

  final List<Map<String, dynamic>> _designSystemColors = [
    {'name': 'Primary Blue', 'hex': '#0052FF', 'color': const Color(0xFF0052FF), 'token': 'brand.primary'},
    {'name': 'Cyber Cyan', 'hex': '#0891B2', 'color': const Color(0xFF0891B2), 'token': 'accent.cyber-cyan'},
    {'name': 'Success Emerald', 'hex': '#10B981', 'color': const Color(0xFF10B981), 'token': 'semantic.success'},
    {'name': 'Warning Amber', 'hex': '#F59E0B', 'color': const Color(0xFFF59E0B), 'token': 'semantic.warning'},
    {'name': 'Danger Red', 'hex': '#EF4444', 'color': const Color(0xFFEF4444), 'token': 'semantic.danger'},
    {'name': 'Obsidian Dark', 'hex': '#0F172A', 'color': const Color(0xFF0F172A), 'token': 'surface.obsidian'},
    {'name': 'Pure White', 'hex': '#FFFFFF', 'color': const Color(0xFFFFFFFF), 'token': 'surface.card'},
    {'name': 'Soft Gray Bg', 'hex': '#F8FAFC', 'color': const Color(0xFFF8FAFC), 'token': 'surface.bg'},
  ];

  final List<Map<String, dynamic>> _systemIcons = [
    {'name': 'Check Circle', 'icon': Icons.check_circle_outline, 'val': 'check_circle'},
    {'name': 'Attendance Check', 'icon': Icons.fact_check_outlined, 'val': 'fact_check'},
    {'name': 'Smartphone Mockup', 'icon': Icons.phone_android, 'val': 'phone_android'},
    {'name': 'Tablet Kiosk', 'icon': Icons.tablet_mac, 'val': 'tablet_mac'},
    {'name': 'Receipt / Billing', 'icon': Icons.receipt_long, 'val': 'receipt_long'},
    {'name': 'Student Group', 'icon': Icons.groups_outlined, 'val': 'groups'},
    {'name': 'Settings Tune', 'icon': Icons.tune, 'val': 'tune'},
    {'name': 'Security Shield', 'icon': Icons.security, 'val': 'security'},
    {'name': 'Star Highlight', 'icon': Icons.star_border, 'val': 'star'},
  ];

  final List<Map<String, dynamic>> _premadeComponents = [
    {
      'name': 'Primary Action CTA 버튼',
      'type': ElementType.shape,
      'width': 220.0,
      'height': 48.0,
      'boxStyle': DeckBoxStyle(backgroundColor: const Color(0xFF0052FF), borderRadius: 10.0, borderWidth: 0),
      'props': {'title': '0.8초 즉시 인증', 'desc': ''},
    },
    {
      'name': 'D-Day 경고 뱃지 칩',
      'type': ElementType.badge,
      'width': 130.0,
      'height': 34.0,
      'boxStyle': DeckBoxStyle(backgroundColor: const Color(0xFFFFFBEB), borderColor: const Color(0xFFFDE68A), borderRadius: 20.0, borderWidth: 1),
      'props': {'badge': 'D-7 결제 임박'},
    },
    {
      'name': '핵심 지표 스탯 카드',
      'type': ElementType.statCard,
      'width': 340.0,
      'height': 160.0,
      'boxStyle': DeckBoxStyle(backgroundColor: Colors.white, borderColor: const Color(0xFFE2E8F0), borderRadius: 16.0),
      'props': {'title': '출결 도달률', 'val': '99.4%', 'sub': '전월 대비 +14.2% 상승'},
    },
    {
      'name': '10인치 키오스크 다이얼 버튼',
      'type': ElementType.shape,
      'width': 90.0,
      'height': 90.0,
      'boxStyle': DeckBoxStyle(backgroundColor: const Color(0xFF1E293B), borderColor: Colors.white24, borderRadius: 16.0, borderWidth: 1),
      'props': {'title': '1', 'desc': ''},
    },
  ];

  void _openVectorStudio() {
    showDialog(
      context: context,
      builder: (ctx) => IconDrawingModal(
        onSaveComponent: (elem) {
          widget.onAddElement(elem);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('매터리얼 가이드 벡터 아이콘 [${elem.name}] 이(가) 캔버스에 등록되었습니다!'),
              backgroundColor: const Color(0xFF0052FF),
              duration: const Duration(seconds: 2),
            ),
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Color(0xFF1E1E1E), // Figma UI3 Dark Slate
      ),
      child: Column(
        children: [
          // Header & Vector Studio Trigger Button
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Color(0xFF2C2C2C))),
            ),
            child: Row(
              children: [
                const Icon(Icons.category_outlined, color: Color(0xFF38BDF8), size: 15),
                const SizedBox(width: 6),
                const Expanded(
                  child: Text(
                    'Assets & Design System',
                    style: TextStyle(color: Colors.white, fontSize: 11.5, fontWeight: FontWeight.bold),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.gesture, size: 16, color: Color(0xFF38BDF8)),
                  tooltip: '구글 매터리얼 아이콘 그리기 모드',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 22, minHeight: 22),
                  onPressed: _openVectorStudio,
                ),
              ],
            ),
          ),

          // Search Field
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: SizedBox(
              height: 30,
              child: TextField(
                style: const TextStyle(color: Colors.white, fontSize: 11),
                decoration: InputDecoration(
                  hintText: '자산 검색 (드래그하여 배치)...',
                  hintStyle: const TextStyle(color: Color(0xFF737373), fontSize: 11),
                  prefixIcon: const Icon(Icons.search, size: 14, color: Color(0xFF737373)),
                  isDense: true,
                  filled: true,
                  fillColor: const Color(0xFF262626),
                  contentPadding: EdgeInsets.zero,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(6), borderSide: BorderSide.none),
                ),
                onChanged: (q) => setState(() => _searchQuery = q.toLowerCase()),
              ),
            ),
          ),

          // Scrollable Assets Sections
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              children: [
                // 1. Vector Icon Drawing Mode Banner
                InkWell(
                  onTap: _openVectorStudio,
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFF0038A8), Color(0xFF0052FF)],
                      ),
                      borderRadius: BorderRadius.circular(8),
                      boxShadow: const [
                        BoxShadow(color: Color(0x330052FF), blurRadius: 8, offset: Offset(0, 3)),
                      ],
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.gesture, color: Colors.white, size: 18),
                        SizedBox(width: 8),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('아이콘 그리기 모드', style: TextStyle(color: Colors.white, fontSize: 11.5, fontWeight: FontWeight.bold)),
                              Text('Material 24dp 키라인 그리드 드로잉', style: TextStyle(color: Colors.white70, fontSize: 9.5)),
                            ],
                          ),
                        ),
                        Icon(Icons.arrow_forward_ios, color: Colors.white70, size: 10),
                      ],
                    ),
                  ),
                ),

                // 2. Design System Colors Swatches (Draggable)
                _buildSectionHeader('디자인 시스템 색상 (드래그하여 적용)'),
                const SizedBox(height: 6),
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: _designSystemColors.where((c) => c['name'].toString().toLowerCase().contains(_searchQuery)).map((c) {
                    final color = c['color'] as Color;
                    return Draggable<AssetDragData>(
                      data: AssetDragData(type: AssetDragType.color, title: c['name'], payload: color),
                      feedback: Material(
                        color: Colors.transparent,
                        child: Container(
                          width: 32,
                          height: 32,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.white, width: 2),
                            boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 8, offset: Offset(0, 4))],
                          ),
                        ),
                      ),
                      child: Tooltip(
                        message: '${c['name']} (${c['hex']}) - 캔버스나 요소에 드롭',
                        child: Container(
                          width: 24,
                          height: 24,
                          decoration: BoxDecoration(
                            color: color,
                            borderRadius: BorderRadius.circular(4),
                            border: Border.all(color: Colors.white24),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),

                const SizedBox(height: 16),

                // 3. Material Icons (Draggable)
                _buildSectionHeader('머티리얼 아이콘 (드래그하여 배치)'),
                const SizedBox(height: 6),
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: _systemIcons.where((i) => i['name'].toString().toLowerCase().contains(_searchQuery)).map((i) {
                    final iconData = i['icon'] as IconData;
                    final iconVal = i['val'] as String;
                    return Draggable<AssetDragData>(
                      data: AssetDragData(type: AssetDragType.icon, title: i['name'], payload: iconVal),
                      feedback: Material(
                        color: Colors.transparent,
                        child: Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: const Color(0xFF0052FF),
                            borderRadius: BorderRadius.circular(8),
                            boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 10, offset: Offset(0, 4))],
                          ),
                          child: Icon(iconData, color: Colors.white, size: 24),
                        ),
                      ),
                      child: Tooltip(
                        message: '${i['name']} - 캔버스에 드롭하여 추가',
                        child: Container(
                          padding: const EdgeInsets.all(6),
                          decoration: BoxDecoration(
                            color: const Color(0xFF262626),
                            borderRadius: BorderRadius.circular(6),
                            border: Border.all(color: const Color(0xFF333333)),
                          ),
                          child: Icon(iconData, color: const Color(0xFFE5E5E5), size: 16),
                        ),
                      ),
                    );
                  }).toList(),
                ),

                const SizedBox(height: 16),

                // 4. Pre-made Design System Components (Draggable)
                _buildSectionHeader('아토믹 UI 컴포넌트 (드래그하여 배치)'),
                const SizedBox(height: 6),
                ..._premadeComponents.where((c) => c['name'].toString().toLowerCase().contains(_searchQuery)).map((c) {
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 6),
                    child: Draggable<AssetDragData>(
                      data: AssetDragData(
                        type: AssetDragType.component,
                        title: c['name'],
                        payload: c,
                      ),
                      feedback: Material(
                        color: Colors.transparent,
                        child: Opacity(
                          opacity: 0.85,
                          child: Container(
                            width: 180,
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: const Color(0xFF0052FF),
                              borderRadius: BorderRadius.circular(8),
                              boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 12, offset: Offset(0, 6))],
                            ),
                            child: Text(
                              c['name'],
                              style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                            ),
                          ),
                        ),
                      ),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                        decoration: BoxDecoration(
                          color: const Color(0xFF262626),
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(color: const Color(0xFF333333)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.widgets_outlined, size: 14, color: Color(0xFF38BDF8)),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                c['name'],
                                style: const TextStyle(color: Colors.white, fontSize: 11),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            const Icon(Icons.drag_indicator, size: 12, color: Color(0xFF737373)),
                          ],
                        ),
                      ),
                    ),
                  );
                }),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Text(
      title,
      style: const TextStyle(color: Color(0xFFA3A3A3), fontSize: 10.5, fontWeight: FontWeight.bold),
    );
  }
}

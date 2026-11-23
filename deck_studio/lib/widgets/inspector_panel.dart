import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import '../models/deck_model.dart';
import '../utils/code_export_generator.dart';
import 'code_export_modal.dart';

class InspectorPanel extends StatefulWidget {
  final DeckElement? element;
  final VoidCallback onElementUpdated;
  final VoidCallback onElementDeleted;
  final VoidCallback? onToggleMainComponent;
  final VoidCallback? onEditMainComponent;
  final VoidCallback? onDetachInstance;
  final VoidCallback? onPushToComponent;

  const InspectorPanel({
    super.key,
    required this.element,
    required this.onElementUpdated,
    required this.onElementDeleted,
    this.onToggleMainComponent,
    this.onEditMainComponent,
    this.onDetachInstance,
    this.onPushToComponent,
  });

  @override
  State<InspectorPanel> createState() => _InspectorPanelState();
}

class _InspectorPanelState extends State<InspectorPanel> {
  final List<String> _fontFamilies = [
    'Pretendard',
    'Inter',
    'Roboto',
    'Montserrat',
    'Noto Sans KR',
    'SF Pro Display'
  ];

  final List<Map<String, dynamic>> _commonIcons = [
    {'name': '없음', 'val': ''},
    {'name': '체크 완료', 'val': 'check_circle'},
    {'name': '출결 체크', 'val': 'fact_check'},
    {'name': '스마트폰', 'val': 'phone_android'},
    {'name': '태블릿', 'val': 'tablet_mac'},
    {'name': '장부/영수증', 'val': 'receipt_long'},
    {'name': '원생 그룹', 'val': 'groups'},
    {'name': '설정 볼트', 'val': 'tune'},
    {'name': '보안 방패', 'val': 'security'},
    {'name': '별표 강조', 'val': 'star'},
  ];

  void _openCodeExport() {
    if (widget.element == null) return;
    final elem = widget.element!;

    final flutterCode = CodeExportGenerator.generateFlutterCode(elem);
    final htmlCode = CodeExportGenerator.generateHtmlCode(elem);
    final figmaCode = CodeExportGenerator.generateFigmaSpec(elem);

    showDialog(
      context: context,
      builder: (ctx) => CodeExportModal(
        flutterCode: flutterCode,
        htmlCode: htmlCode,
        figmaCode: figmaCode,
        elementName: elem.name,
      ),
    );
  }

  void _pickColor(BuildContext context, Color currentColor, String title, ValueChanged<Color> onColorChanged) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
        content: SingleChildScrollView(
          child: ColorPicker(
            pickerColor: currentColor,
            onColorChanged: onColorChanged,
            enableAlpha: false,
            displayThumbColor: true,
          ),
        ),
        actions: [
          ElevatedButton(
            child: const Text('선택 완료'),
            onPressed: () => Navigator.pop(ctx),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (widget.element == null) {
      return Container(
        width: 380,
        color: const Color(0xFF1E1E1E), // Figma Dark Slate
        padding: const EdgeInsets.all(24),
        child: const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.touch_app_outlined, size: 48, color: Color(0xFF525252)),
              SizedBox(height: 16),
              Text(
                '요소를 선택하면 정렬, 크기, 폰트, 자간/행간,\n아이콘, 색상 및 UI 텍스트를 자유자재로 수정하고\nFlutter/HTML/Figma 소스를 즉시 복붙할 수 있습니다.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xFFA3A3A3), fontSize: 13, height: 1.5),
              ),
            ],
          ),
        ),
      );
    }

    final elem = widget.element!;
    final ts = elem.textStyle;
    final bs = elem.boxStyle;

    return Container(
      width: 380,
      decoration: const BoxDecoration(
        color: Color(0xFF1E1E1E), // Figma Dark
        border: Border(left: BorderSide(color: Color(0xFF2C2C2C))),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Inspector Header
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Color(0xFF2C2C2C))),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: const Color(0xFF2C2C2C),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Icon(Icons.tune, color: Color(0xFF38BDF8), size: 16),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    elem.name,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.delete_outline, color: Color(0xFFEF4444), size: 18),
                  onPressed: widget.onElementDeleted,
                  tooltip: '요소 삭제',
                ),
              ],
            ),
          ),

          // Figma Component & Instance Banner / Actions
          if (elem.isComponent) ...[
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              color: const Color(0xFF7C3AED).withOpacity(0.18),
              child: Row(
                children: [
                  const Icon(Icons.auto_awesome, color: Color(0xFFA78BFA), size: 16),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '메인 컴포넌트 (Main Component)',
                          style: TextStyle(color: Color(0xFFA78BFA), fontSize: 11, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '편집 시 모든 인스턴스에 실시간 일괄 동기화됩니다.',
                          style: TextStyle(color: Color(0xFFC4B5FD), fontSize: 9.5),
                        ),
                      ],
                    ),
                  ),
                  TextButton.icon(
                    icon: const Icon(Icons.sync, size: 12, color: Colors.white),
                    label: const Text('인스턴스 일괄 반영', style: TextStyle(fontSize: 10, color: Colors.white)),
                    style: TextButton.styleFrom(
                      backgroundColor: const Color(0xFF7C3AED),
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      visualDensity: VisualDensity.compact,
                    ),
                    onPressed: widget.onPushToComponent,
                  ),
                ],
              ),
            ),
          ] else if (elem.componentId != null) ...[
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              color: const Color(0xFF0052FF).withOpacity(0.15),
              child: Row(
                children: [
                  const Icon(Icons.diamond_outlined, color: Color(0xFF60A5FA), size: 16),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '컴포넌트 인스턴스 (Instance)',
                          style: TextStyle(color: Color(0xFF60A5FA), fontSize: 11, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '메인 컴포넌트 편집 시 일괄 동기화됩니다.',
                          style: TextStyle(color: Color(0xFF93C5FD), fontSize: 9.5),
                        ),
                      ],
                    ),
                  ),
                  ElevatedButton.icon(
                    icon: const Icon(Icons.edit_note, size: 14),
                    label: const Text('컴포넌트 편집', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF7C3AED),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      visualDensity: VisualDensity.compact,
                    ),
                    onPressed: widget.onEditMainComponent,
                  ),
                  const SizedBox(width: 6),
                  IconButton(
                    icon: const Icon(Icons.link_off, size: 16, color: Color(0xFF94A3B8)),
                    tooltip: '인스턴스 분해 (Detach Instance)',
                    visualDensity: VisualDensity.compact,
                    onPressed: widget.onDetachInstance,
                  ),
                ],
              ),
            ),
          ] else ...[
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              color: const Color(0xFF181818),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('컴포넌트 미지정 요소', style: TextStyle(color: Color(0xFF737373), fontSize: 10)),
                  TextButton.icon(
                    icon: const Icon(Icons.auto_awesome, size: 12, color: Color(0xFFA78BFA)),
                    label: const Text('컴포넌트 만들기 (Ctrl+Alt+K)', style: TextStyle(fontSize: 10, color: Color(0xFFA78BFA))),
                    style: TextButton.styleFrom(visualDensity: VisualDensity.compact),
                    onPressed: widget.onToggleMainComponent,
                  ),
                ],
              ),
            ),
          ],

          // Action Button: 원클릭 코드 내보내기 (Flutter / HTML / Figma)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            color: const Color(0xFF141414),
            child: ElevatedButton.icon(
              icon: const Icon(Icons.copy_all, size: 16),
              label: const Text(
                'Flutter / HTML / Figma 소스 복사',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0052FF),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 10),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
              onPressed: _openCodeExport,
            ),
          ),

          // Scrollable Properties List
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // 1. 레이아웃 위치 & 크기 (Size & Alignment)
                _buildSectionHeader(Icons.aspect_ratio, '위치 및 크기 (Layout & Size)'),
                const SizedBox(height: 8),
                Row(
                  children: [
                    _buildNumField('X 좌표', elem.x, (val) {
                      setState(() => elem.x = val);
                      widget.onElementUpdated();
                    }),
                    const SizedBox(width: 8),
                    _buildNumField('Y 좌표', elem.y, (val) {
                      setState(() => elem.y = val);
                      widget.onElementUpdated();
                    }),
                  ],
                ),
                const SizedBox(height: 8),
                // 너비 / 높이 수치 및 피그마식 Auto (Hug / Fill / Fixed) 리사이징 모드
                Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildFieldLabel('너비 (W)'),
                              _buildSizingModeDropdown(elem.horizontalSizing, (mode) {
                                setState(() {
                                  elem.horizontalSizing = mode;
                                  elem.applyAutoLayout();
                                });
                                widget.onElementUpdated();
                              }),
                            ],
                          ),
                          _buildDimensionInputField(
                            elem.width,
                            elem.horizontalSizing,
                            (val) {
                              setState(() {
                                if (val == -1) {
                                  elem.horizontalSizing = SizingMode.hug;
                                } else {
                                  elem.horizontalSizing = SizingMode.fixed;
                                  elem.width = val;
                                }
                                elem.applyAutoLayout();
                              });
                              widget.onElementUpdated();
                            },
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildFieldLabel('높이 (H)'),
                              _buildSizingModeDropdown(elem.verticalSizing, (mode) {
                                setState(() {
                                  elem.verticalSizing = mode;
                                  elem.applyAutoLayout();
                                });
                                widget.onElementUpdated();
                              }),
                            ],
                          ),
                          _buildDimensionInputField(
                            elem.height,
                            elem.verticalSizing,
                            (val) {
                              setState(() {
                                if (val == -1) {
                                  elem.verticalSizing = SizingMode.hug;
                                } else {
                                  elem.verticalSizing = SizingMode.fixed;
                                  elem.height = val;
                                }
                                elem.applyAutoLayout();
                              });
                              widget.onElementUpdated();
                            },
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 18),

                // 2. UI 정렬 옵션 (Alignment: 수평 & 수직)
                _buildSectionHeader(Icons.format_align_left, '텍스트 정렬 (Text Alignment)'),
                const SizedBox(height: 8),
                // 2.1 수평 정렬
                Row(
                  children: [
                    _buildAlignButton('좌측', TextAlignOption.left, Icons.format_align_left, ts.textAlign),
                    const SizedBox(width: 6),
                    _buildAlignButton('가운데', TextAlignOption.center, Icons.format_align_center, ts.textAlign),
                    const SizedBox(width: 6),
                    _buildAlignButton('우측', TextAlignOption.right, Icons.format_align_right, ts.textAlign),
                  ],
                ),
                const SizedBox(height: 8),
                // 2.2 피그마식 수직 정렬 (Top / Middle / Bottom)
                Row(
                  children: [
                    _buildVerticalAlignButton('상단 (Top)', TextVerticalAlign.top, Icons.vertical_align_top, ts.verticalAlign),
                    const SizedBox(width: 6),
                    _buildVerticalAlignButton('세로 중앙 (Middle)', TextVerticalAlign.middle, Icons.vertical_align_center, ts.verticalAlign),
                    const SizedBox(width: 6),
                    _buildVerticalAlignButton('하단 (Bottom)', TextVerticalAlign.bottom, Icons.vertical_align_bottom, ts.verticalAlign),
                  ],
                ),
                const SizedBox(height: 18),

                // 2.5 오토레이아웃 상위/내부 정렬 (Parent/Self Alignment)
                _buildSectionHeader(Icons.align_horizontal_left, '오토레이아웃 축 정렬 (AutoLayout Align)'),
                const SizedBox(height: 8),
                Row(
                  children: [
                    _buildAutoLayoutAlignBtn('시작 (Start)', AutoLayoutAlignment.start, Icons.align_horizontal_left, elem.autoLayoutAlignment),
                    const SizedBox(width: 6),
                    _buildAutoLayoutAlignBtn('중앙 (Center)', AutoLayoutAlignment.center, Icons.align_horizontal_center, elem.autoLayoutAlignment),
                    const SizedBox(width: 6),
                    _buildAutoLayoutAlignBtn('끝 (End)', AutoLayoutAlignment.end, Icons.align_horizontal_right, elem.autoLayoutAlignment),
                    const SizedBox(width: 6),
                    _buildAutoLayoutAlignBtn('균등 (Between)', AutoLayoutAlignment.spaceBetween, Icons.space_bar, elem.autoLayoutAlignment),
                  ],
                ),
                const SizedBox(height: 18),

                // 3. 아이콘 선택 (Icon Selector)
                _buildSectionHeader(Icons.interests, '아이콘 삽입 및 변경 (Icon Selector)'),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0xFFE2E8F0)),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: _commonIcons.any((i) => i['val'] == elem.iconName) ? elem.iconName : '',
                      isExpanded: true,
                      style: const TextStyle(fontSize: 12, color: Color(0xFF0F172A), fontWeight: FontWeight.bold),
                      items: _commonIcons.map((i) => DropdownMenuItem<String>(
                        value: i['val'] as String,
                        child: Text(i['name'] as String),
                      )).toList(),
                      onChanged: (val) {
                        if (val != null) {
                          setState(() => elem.iconName = val);
                          widget.onElementUpdated();
                        }
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 18),

                // 4. 타이포그래피 (폰트, 자간, 행간, 장평, 컬러)
                _buildSectionHeader(Icons.text_format, '타이포그래피 및 편집 (Typography)'),
                const SizedBox(height: 10),

                // 폰트 패밀리
                _buildFieldLabel('폰트 (Font Family)'),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0xFFE2E8F0)),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: _fontFamilies.contains(ts.fontFamily) ? ts.fontFamily : 'Pretendard',
                      isExpanded: true,
                      style: const TextStyle(fontSize: 12, color: Color(0xFF0F172A), fontWeight: FontWeight.bold),
                      items: _fontFamilies.map((f) => DropdownMenuItem(value: f, child: Text(f))).toList(),
                      onChanged: (val) {
                        if (val != null) {
                          setState(() => ts.fontFamily = val);
                          widget.onElementUpdated();
                        }
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 12),

                // 폰트 크기 및 두께
                Row(
                  children: [
                    _buildNumField('크기(px)', ts.fontSize, (val) {
                      setState(() => ts.fontSize = val);
                      widget.onElementUpdated();
                    }),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildFieldLabel('두께 (Weight)'),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10),
                            decoration: BoxDecoration(
                              color: const Color(0xFFF8FAFC),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: const Color(0xFFE2E8F0)),
                            ),
                            child: DropdownButtonHideUnderline(
                              child: DropdownButton<FontWeight>(
                                value: ts.fontWeight,
                                isExpanded: true,
                                style: const TextStyle(fontSize: 12, color: Color(0xFF0F172A), fontWeight: FontWeight.bold),
                                items: const [
                                  DropdownMenuItem(value: FontWeight.w300, child: Text('Light (300)')),
                                  DropdownMenuItem(value: FontWeight.w400, child: Text('Regular (400)')),
                                  DropdownMenuItem(value: FontWeight.w500, child: Text('Medium (500)')),
                                  DropdownMenuItem(value: FontWeight.w600, child: Text('SemiBold (600)')),
                                  DropdownMenuItem(value: FontWeight.w700, child: Text('Bold (700)')),
                                  DropdownMenuItem(value: FontWeight.w900, child: Text('Black (900)')),
                                ],
                                onChanged: (val) {
                                  if (val != null) {
                                    setState(() => ts.fontWeight = val);
                                    widget.onElementUpdated();
                                  }
                                },
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // 자간 & 행간
                Row(
                  children: [
                    _buildNumField('자간 (Letter)', ts.letterSpacing, (val) {
                      setState(() => ts.letterSpacing = val);
                      widget.onElementUpdated();
                    }, step: 0.1),
                    const SizedBox(width: 8),
                    _buildNumField('행간 (Height)', ts.height, (val) {
                      setState(() => ts.height = val);
                      widget.onElementUpdated();
                    }, step: 0.05),
                  ],
                ),
                const SizedBox(height: 12),

                // 장평/어간 & 텍스트 컬러
                Row(
                  children: [
                    _buildNumField('장평/어간 (Word)', ts.wordSpacing, (val) {
                      setState(() => ts.wordSpacing = val);
                      widget.onElementUpdated();
                    }, step: 0.5),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildFieldLabel('글자 색상 (Color)'),
                          GestureDetector(
                            onTap: () => _pickColor(context, ts.color, '텍스트 컬러 선택', (c) {
                              setState(() => ts.color = c);
                              widget.onElementUpdated();
                            }),
                            child: Container(
                              height: 38,
                              padding: const EdgeInsets.symmetric(horizontal: 10),
                              decoration: BoxDecoration(
                                color: const Color(0xFFF8FAFC),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: const Color(0xFFE2E8F0)),
                              ),
                              child: Row(
                                children: [
                                  Container(
                                    width: 18,
                                    height: 18,
                                    decoration: BoxDecoration(
                                      color: ts.color,
                                      shape: BoxShape.circle,
                                      border: Border.all(color: Colors.black26),
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    '#${(ts.color.r * 255).toInt().toRadixString(16).padLeft(2, '0')}${(ts.color.g * 255).toInt().toRadixString(16).padLeft(2, '0')}${(ts.color.b * 255).toInt().toRadixString(16).padLeft(2, '0')}'
                                        .toUpperCase(),
                                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 18),

                // 5. 박스 및 배경 스타일 (UI Surface & Border)
                _buildSectionHeader(Icons.palette, '박스 서피스 및 테두리 (Box Style)'),
                const SizedBox(height: 10),
                Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildFieldLabel('배경 색상 (Bg Color)'),
                          GestureDetector(
                            onTap: () => _pickColor(context, bs.backgroundColor, '배경 색상 선택', (c) {
                              setState(() => bs.backgroundColor = c);
                              widget.onElementUpdated();
                            }),
                            child: Container(
                              height: 38,
                              padding: const EdgeInsets.symmetric(horizontal: 8),
                              decoration: BoxDecoration(
                                color: const Color(0xFFF8FAFC),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: const Color(0xFFE2E8F0)),
                              ),
                              child: Row(
                                children: [
                                  Container(
                                    width: 16,
                                    height: 16,
                                    decoration: BoxDecoration(
                                      color: bs.backgroundColor,
                                      shape: BoxShape.circle,
                                      border: Border.all(color: Colors.black26),
                                    ),
                                  ),
                                  const SizedBox(width: 6),
                                  Text(
                                    '#${(bs.backgroundColor.r * 255).toInt().toRadixString(16).padLeft(2, '0')}${(bs.backgroundColor.g * 255).toInt().toRadixString(16).padLeft(2, '0')}${(bs.backgroundColor.b * 255).toInt().toRadixString(16).padLeft(2, '0')}'
                                        .toUpperCase(),
                                    style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildFieldLabel('테두리 색상 (Border)'),
                          GestureDetector(
                            onTap: () => _pickColor(context, bs.borderColor, '테두리 색상 선택', (c) {
                              setState(() => bs.borderColor = c);
                              widget.onElementUpdated();
                            }),
                            child: Container(
                              height: 38,
                              padding: const EdgeInsets.symmetric(horizontal: 8),
                              decoration: BoxDecoration(
                                color: const Color(0xFFF8FAFC),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: const Color(0xFFE2E8F0)),
                              ),
                              child: Row(
                                children: [
                                  Container(
                                    width: 16,
                                    height: 16,
                                    decoration: BoxDecoration(
                                      color: bs.borderColor,
                                      shape: BoxShape.circle,
                                      border: Border.all(color: Colors.black26),
                                    ),
                                  ),
                                  const SizedBox(width: 6),
                                  Text(
                                    '#${(bs.borderColor.r * 255).toInt().toRadixString(16).padLeft(2, '0')}${(bs.borderColor.g * 255).toInt().toRadixString(16).padLeft(2, '0')}${(bs.borderColor.b * 255).toInt().toRadixString(16).padLeft(2, '0')}'
                                        .toUpperCase(),
                                    style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    _buildNumField('곡률 (Radius)', bs.borderRadius, (val) {
                      setState(() => bs.borderRadius = val);
                      widget.onElementUpdated();
                    }),
                    const SizedBox(width: 8),
                    _buildNumField('패딩 (Padding)', bs.padding, (val) {
                      setState(() => bs.padding = val);
                      widget.onElementUpdated();
                    }),
                  ],
                ),
                const SizedBox(height: 18),

                // 5.5 Figma AutoLayout Section
                _buildAutoLayoutSection(elem),
                const SizedBox(height: 18),

                // 6. 텍스트 및 UI 콘텐츠 직접 수정
                _buildSectionHeader(Icons.edit_note, 'UI 텍스트 직접 편집 (UI Content)'),
                const SizedBox(height: 10),
                ..._buildCustomProps(elem),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAutoLayoutSection(DeckElement elem) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionHeader(Icons.view_quilt_outlined, 'Figma AutoLayout (오토레이아웃)'),
        const SizedBox(height: 10),
        Row(
          children: [
            _buildAutoLayoutDirBtn('없음', AutoLayoutDirection.none, Icons.close, elem.autoLayoutDirection, () {
              setState(() => elem.autoLayoutDirection = AutoLayoutDirection.none);
              widget.onElementUpdated();
            }),
            const SizedBox(width: 6),
            _buildAutoLayoutDirBtn('가로 (H)', AutoLayoutDirection.horizontal, Icons.view_column, elem.autoLayoutDirection, () {
              setState(() {
                elem.autoLayoutDirection = AutoLayoutDirection.horizontal;
                elem.applyAutoLayout();
              });
              widget.onElementUpdated();
            }),
            const SizedBox(width: 6),
            _buildAutoLayoutDirBtn('세로 (V)', AutoLayoutDirection.vertical, Icons.view_stream, elem.autoLayoutDirection, () {
              setState(() {
                elem.autoLayoutDirection = AutoLayoutDirection.vertical;
                elem.applyAutoLayout();
              });
              widget.onElementUpdated();
            }),
          ],
        ),
        if (elem.autoLayoutDirection != AutoLayoutDirection.none) ...[
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _buildFieldLabel('간격 (Gap)'),
                        InkWell(
                          onTap: () {
                            setState(() {
                              elem.isAutoSpacing = !elem.isAutoSpacing;
                              elem.applyAutoLayout();
                            });
                            widget.onElementUpdated();
                          },
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1.5),
                            decoration: BoxDecoration(
                              color: elem.isAutoSpacing ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              'Auto',
                              style: TextStyle(
                                fontSize: 9.5,
                                fontWeight: FontWeight.bold,
                                color: elem.isAutoSpacing ? Colors.white : const Color(0xFF64748B),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                      decoration: BoxDecoration(
                        color: elem.isAutoSpacing ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: elem.isAutoSpacing ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
                        ),
                      ),
                      child: elem.isAutoSpacing
                          ? const Center(
                              child: Text(
                                'Auto (균등 분배)',
                                style: TextStyle(fontSize: 11.5, color: Color(0xFF0052FF), fontWeight: FontWeight.bold),
                              ),
                            )
                          : TextFormField(
                              key: ValueKey('${elem.id}_gap_${elem.autoLayoutSpacing}'),
                              initialValue: elem.autoLayoutSpacing.toInt().toString(),
                              keyboardType: const TextInputType.numberWithOptions(decimal: true),
                              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                              decoration: const InputDecoration(
                                isDense: true,
                                contentPadding: EdgeInsets.zero,
                                border: InputBorder.none,
                              ),
                              onChanged: (text) {
                                if (text.trim().toLowerCase() == 'auto') {
                                  setState(() {
                                    elem.isAutoSpacing = true;
                                    elem.applyAutoLayout();
                                  });
                                  widget.onElementUpdated();
                                  return;
                                }
                                final parsed = double.tryParse(text);
                                if (parsed != null) {
                                  setState(() {
                                    elem.isAutoSpacing = false;
                                    elem.autoLayoutSpacing = parsed;
                                    elem.applyAutoLayout();
                                  });
                                  widget.onElementUpdated();
                                }
                              },
                            ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              _buildNumField('패딩 (Padding)', elem.autoLayoutPadding, (val) {
                setState(() {
                  elem.autoLayoutPadding = val;
                  elem.applyAutoLayout();
                });
                widget.onElementUpdated();
              }),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            '하위 요소: ${elem.children.length}개 자동 정렬 배치됨 ${elem.isAutoSpacing ? "• Auto Spacing 적용 중" : ""}',
            style: const TextStyle(color: Color(0xFF0052FF), fontSize: 11, fontWeight: FontWeight.bold),
          ),
        ],
      ],
    );
  }

  Widget _buildAutoLayoutDirBtn(String label, AutoLayoutDirection dir, IconData icon, AutoLayoutDirection cur, VoidCallback onTap) {
    final isSelected = cur == dir;
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: isSelected ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
              width: isSelected ? 1.5 : 1,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 14, color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B)),
              const SizedBox(height: 3),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B),
                  fontSize: 10.5,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAutoLayoutAlignBtn(String label, AutoLayoutAlignment align, IconData icon, AutoLayoutAlignment current) {
    final isSelected = current == align;
    return Expanded(
      child: InkWell(
        onTap: () {
          setState(() {
            widget.element!.autoLayoutAlignment = align;
            widget.element!.applyAutoLayout();
          });
          widget.onElementUpdated();
        },
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: isSelected ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
              width: isSelected ? 1.5 : 1,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 14, color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B)),
              const SizedBox(height: 3),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B),
                  fontSize: 9.5,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAlignButton(String label, TextAlignOption opt, IconData icon, TextAlignOption current) {
    final isSelected = current == opt;
    return Expanded(
      child: InkWell(
        onTap: () {
          setState(() => widget.element!.textStyle.textAlign = opt);
          widget.onElementUpdated();
        },
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: isSelected ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
              width: isSelected ? 1.5 : 1,
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 14, color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B)),
              const SizedBox(width: 4),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B),
                  fontSize: 11,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildVerticalAlignButton(String label, TextVerticalAlign opt, IconData icon, TextVerticalAlign current) {
    final isSelected = current == opt;
    return Expanded(
      child: InkWell(
        onTap: () {
          setState(() => widget.element!.textStyle.verticalAlign = opt);
          widget.onElementUpdated();
        },
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: isSelected ? const Color(0xFF0052FF) : const Color(0xFFE2E8F0),
              width: isSelected ? 1.5 : 1,
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 14, color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B)),
              const SizedBox(width: 4),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? const Color(0xFF0052FF) : const Color(0xFF64748B),
                  fontSize: 10,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(IconData icon, String title) {
    return Row(
      children: [
        Icon(icon, size: 14, color: const Color(0xFF0052FF)),
        const SizedBox(width: 6),
        Text(
          title,
          style: const TextStyle(
            color: Color(0xFF64748B),
            fontSize: 11,
            fontWeight: FontWeight.bold,
            letterSpacing: 0.5,
          ),
        ),
      ],
    );
  }

  Widget _buildSizingModeDropdown(SizingMode mode, ValueChanged<SizingMode> onChanged) {
    return Container(
      height: 20,
      padding: const EdgeInsets.symmetric(horizontal: 4),
      decoration: BoxDecoration(
        color: const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(4),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<SizingMode>(
          value: mode,
          isDense: true,
          style: const TextStyle(fontSize: 10, color: Color(0xFF0052FF), fontWeight: FontWeight.bold),
          items: const [
            DropdownMenuItem(value: SizingMode.fixed, child: Text('Fixed')),
            DropdownMenuItem(value: SizingMode.hug, child: Text('Hug (Auto)')),
            DropdownMenuItem(value: SizingMode.fill, child: Text('Fill')),
          ],
          onChanged: (val) {
            if (val != null) onChanged(val);
          },
        ),
      ),
    );
  }

  Widget _buildDimensionInputField(double val, SizingMode mode, ValueChanged<double> onChanged) {
    if (mode == SizingMode.hug) {
      return Container(
        height: 36,
        alignment: Alignment.centerLeft,
        padding: const EdgeInsets.symmetric(horizontal: 10),
        decoration: BoxDecoration(
          color: const Color(0xFFEFF6FF),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: const Color(0xFF0052FF)),
        ),
        child: const Text(
          'Hug (내용 맞춤 Auto)',
          style: TextStyle(fontSize: 11, color: Color(0xFF0052FF), fontWeight: FontWeight.bold),
        ),
      );
    } else if (mode == SizingMode.fill) {
      return Container(
        height: 36,
        alignment: Alignment.centerLeft,
        padding: const EdgeInsets.symmetric(horizontal: 10),
        decoration: BoxDecoration(
          color: const Color(0xFFEFF6FF),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: const Color(0xFF0052FF)),
        ),
        child: const Text(
          'Fill (부모 채움)',
          style: TextStyle(fontSize: 11, color: Color(0xFF0052FF), fontWeight: FontWeight.bold),
        ),
      );
    }

    return Container(
      height: 36,
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF262626),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFF333333)),
      ),
      child: TextFormField(
        key: ValueKey('${widget.element!.id}_dim_$val'),
        initialValue: val.toInt().toString(),
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.white),
        decoration: const InputDecoration(
          isDense: true,
          contentPadding: EdgeInsets.zero,
          border: InputBorder.none,
        ),
        onChanged: (text) {
          final trimmed = text.trim().toLowerCase();
          if (trimmed == 'auto' || trimmed == 'hug') {
            onChanged(-1); // Signal hug
            return;
          }
          final parsed = double.tryParse(text);
          if (parsed != null) onChanged(parsed);
        },
      ),
    );
  }

  Widget _buildFieldLabel(String label) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Text(
        label,
        style: const TextStyle(color: Color(0xFFD4D4D4), fontSize: 11, fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _buildNumField(String label, double val, ValueChanged<double> onChanged, {double step = 1.0}) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildFieldLabel(label),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF262626),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: const Color(0xFF333333)),
            ),
            child: TextFormField(
              key: ValueKey('${widget.element!.id}_${label}_$val'),
              initialValue: step < 1.0 ? val.toStringAsFixed(2) : val.toInt().toString(),
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.white),
              decoration: const InputDecoration(
                isDense: true,
                contentPadding: EdgeInsets.zero,
                border: InputBorder.none,
              ),
              onChanged: (text) {
                final parsed = double.tryParse(text);
                if (parsed != null) onChanged(parsed);
              },
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildCustomProps(DeckElement elem) {
    final widgets = <Widget>[];

    elem.props.forEach((key, value) {
      if (value is String) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                key,
                style: const TextStyle(color: Color(0xFF334155), fontSize: 11, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 6),
              TextFormField(
                key: ValueKey('${elem.id}_$key'),
                initialValue: value,
                maxLines: value.contains('\n') || value.length > 30 ? 3 : 1,
                style: const TextStyle(fontSize: 12),
                decoration: InputDecoration(
                  isDense: true,
                  filled: true,
                  fillColor: const Color(0xFFF8FAFC),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                  ),
                ),
                onChanged: (text) {
                  elem.props[key] = text;
                  widget.onElementUpdated();
                },
              ),
            ],
          ),
        ));
      } else if (value is bool) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(key, style: const TextStyle(color: Color(0xFF334155), fontSize: 12)),
              Switch(
                value: value,
                activeThumbColor: const Color(0xFF0052FF),
                onChanged: (bool newVal) {
                  setState(() => elem.props[key] = newVal);
                  widget.onElementUpdated();
                },
              ),
            ],
          ),
        ));
      } else if (value is List) {
        // Support editing lists of items (Flowcharts, KPI strips, stages)
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '$key (${value.length}개 항목)',
                    style: const TextStyle(color: Color(0xFF0052FF), fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              ...value.asMap().entries.map((entry) {
                final idx = entry.key;
                final item = entry.value;
                if (item is Map) {
                  final mapItem = Map<String, dynamic>.from(item);
                  return Container(
                    margin: const EdgeInsets.only(bottom: 8),
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF8FAFC),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: const Color(0xFFE2E8F0)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: mapItem.entries.map((fEntry) {
                        if (fEntry.value is String) {
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 6),
                            child: Row(
                              children: [
                                SizedBox(
                                  width: 50,
                                  child: Text(
                                    fEntry.key,
                                    style: const TextStyle(fontSize: 10, color: Color(0xFF64748B), fontWeight: FontWeight.bold),
                                  ),
                                ),
                                Expanded(
                                  child: TextFormField(
                                    key: ValueKey('${elem.id}_${key}_${idx}_${fEntry.key}'),
                                    initialValue: fEntry.value as String,
                                    style: const TextStyle(fontSize: 11),
                                    decoration: InputDecoration(
                                      isDense: true,
                                      contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                                      fillColor: Colors.white,
                                      filled: true,
                                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(4), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
                                    ),
                                    onChanged: (newText) {
                                      mapItem[fEntry.key] = newText;
                                      value[idx] = mapItem;
                                      widget.onElementUpdated();
                                    },
                                  ),
                                ),
                              ],
                            ),
                          );
                        }
                        return const SizedBox.shrink();
                      }).toList(),
                    ),
                  );
                }
                return const SizedBox.shrink();
              }),
            ],
          ),
        ));
      }
    });

    return widgets;
  }
}

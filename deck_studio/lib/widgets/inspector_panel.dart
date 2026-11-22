import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import '../models/deck_model.dart';
import '../utils/code_export_generator.dart';
import 'code_export_modal.dart';

class InspectorPanel extends StatefulWidget {
  final DeckElement? element;
  final VoidCallback onElementUpdated;
  final VoidCallback onElementDeleted;

  const InspectorPanel({
    super.key,
    required this.element,
    required this.onElementUpdated,
    required this.onElementDeleted,
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
        color: Colors.white,
        padding: const EdgeInsets.all(24),
        child: const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.touch_app_outlined, size: 48, color: Color(0xFF94A3B8)),
              SizedBox(height: 16),
              Text(
                '요소를 선택하면 정렬, 크기, 폰트, 자간/행간,\n아이콘, 색상 및 UI 텍스트를 자유자재로 수정하고\nFlutter/HTML/Figma 소스를 즉시 복붙할 수 있습니다.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xFF64748B), fontSize: 13, height: 1.5),
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
        color: Colors.white,
        border: Border(left: BorderSide(color: Color(0xFFE2E8F0))),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Inspector Header
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Color(0xFFE2E8F0))),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: const Color(0xFFEFF6FF),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Icon(Icons.tune, color: Color(0xFF0052FF), size: 16),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    elem.name,
                    style: const TextStyle(
                      color: Color(0xFF0F172A),
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

          // Action Button: 원클릭 코드 내보내기 (Flutter / HTML / Figma)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            color: const Color(0xFFF8FAFC),
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
                Row(
                  children: [
                    _buildNumField('너비 (Width)', elem.width, (val) {
                      setState(() => elem.width = val);
                      widget.onElementUpdated();
                    }),
                    const SizedBox(width: 8),
                    _buildNumField('높이 (Height)', elem.height, (val) {
                      setState(() => elem.height = val);
                      widget.onElementUpdated();
                    }),
                  ],
                ),
                const SizedBox(height: 18),

                // 2. UI 정렬 옵션 (Alignment)
                _buildSectionHeader(Icons.format_align_left, '텍스트 및 컨텐츠 정렬 (Alignment)'),
                const SizedBox(height: 8),
                Row(
                  children: [
                    _buildAlignButton('좌측', TextAlignOption.left, Icons.format_align_left, ts.textAlign),
                    const SizedBox(width: 6),
                    _buildAlignButton('중앙', TextAlignOption.center, Icons.format_align_center, ts.textAlign),
                    const SizedBox(width: 6),
                    _buildAlignButton('우측', TextAlignOption.right, Icons.format_align_right, ts.textAlign),
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

  Widget _buildFieldLabel(String label) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Text(
        label,
        style: const TextStyle(color: Color(0xFF334155), fontSize: 11, fontWeight: FontWeight.w600),
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
              color: const Color(0xFFF8FAFC),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: const Color(0xFFE2E8F0)),
            ),
            child: TextFormField(
              key: ValueKey('\${widget.element!.id}_\${label}_\$val'),
              initialValue: step < 1.0 ? val.toStringAsFixed(2) : val.toInt().toString(),
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
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
                key: ValueKey('\${elem.id}_\$key'),
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
                                    key: ValueKey('\${elem.id}_\${key}_\${idx}_\${fEntry.key}'),
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

import 'package:flutter/material.dart';
import '../models/deck_model.dart';

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
  @override
  Widget build(BuildContext context) {
    if (widget.element == null) {
      return Container(
        width: 320,
        color: Colors.white,
        padding: const EdgeInsets.all(24),
        child: const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.touch_app_outlined, size: 48, color: Color(0xFF94A3B8)),
              SizedBox(height: 16),
              Text(
                '요소를 선택하면 세부 속성을\n실시간으로 커스텀할 수 있습니다.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xFF64748B), fontSize: 13, height: 1.5),
              ),
            ],
          ),
        ),
      );
    }

    final elem = widget.element!;

    return Container(
      width: 340,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(left: BorderSide(color: Color(0xFFE2E8F0))),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Inspector Header
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
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
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    elem.name,
                    style: const TextStyle(
                      color: Color(0xFF0F172A),
                      fontSize: 13.5,
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

          // Scrollable Properties List
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildSectionTitle('위치 및 크기 (Layout)'),
                const SizedBox(height: 10),
                Row(
                  children: [
                    _buildCoordField('X', elem.x, (val) {
                      setState(() => elem.x = val);
                      widget.onElementUpdated();
                    }),
                    const SizedBox(width: 8),
                    _buildCoordField('Y', elem.y, (val) {
                      setState(() => elem.y = val);
                      widget.onElementUpdated();
                    }),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    _buildCoordField('Width', elem.width, (val) {
                      setState(() => elem.width = val);
                      widget.onElementUpdated();
                    }),
                    const SizedBox(width: 8),
                    _buildCoordField('Height', elem.height, (val) {
                      setState(() => elem.height = val);
                      widget.onElementUpdated();
                    }),
                  ],
                ),
                const SizedBox(height: 20),
                _buildSectionTitle('텍스트 및 내용 (Content)'),
                const SizedBox(height: 10),
                ..._buildCustomProps(elem),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: const TextStyle(
        color: Color(0xFF64748B),
        fontSize: 11,
        fontWeight: FontWeight.bold,
        letterSpacing: 0.5,
      ),
    );
  }

  Widget _buildCoordField(String label, double val, ValueChanged<double> onChanged) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: const Color(0xFFF8FAFC),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: const Color(0xFFE2E8F0)),
        ),
        child: Row(
          children: [
            Text(label, style: const TextStyle(color: Color(0xFF64748B), fontSize: 11, fontWeight: FontWeight.bold)),
            const SizedBox(width: 8),
            Expanded(
              child: TextFormField(
                initialValue: val.toInt().toString(),
                keyboardType: TextInputType.number,
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
                activeColor: const Color(0xFF0052FF),
                onChanged: (bool newVal) {
                  setState(() => elem.props[key] = newVal);
                  widget.onElementUpdated();
                },
              ),
            ],
          ),
        ));
      }
    });

    return widgets;
  }
}


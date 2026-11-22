import 'package:flutter/material.dart';
import '../models/deck_model.dart';

class FigmaLayersPanel extends StatelessWidget {
  final DeckSlide slide;
  final DeckElement? selectedElement;
  final ValueChanged<DeckElement?> onElementSelected;
  final VoidCallback onSlideModified;
  final VoidCallback onGroupSelected;
  final VoidCallback onUngroupSelected;

  const FigmaLayersPanel({
    super.key,
    required this.slide,
    required this.selectedElement,
    required this.onElementSelected,
    required this.onSlideModified,
    required this.onGroupSelected,
    required this.onUngroupSelected,
  });

  IconData _getElementIcon(ElementType type) {
    switch (type) {
      case ElementType.group:
        return Icons.folder_outlined;
      case ElementType.text:
        return Icons.text_fields;
      case ElementType.header:
        return Icons.subtitles_outlined;
      case ElementType.statCard:
        return Icons.analytics_outlined;
      case ElementType.shape:
        return Icons.crop_square_outlined;
      case ElementType.mockupPlaceholder:
        return Icons.phone_android;
      case ElementType.designTokens:
        return Icons.palette_outlined;
      case ElementType.flowchart:
        return Icons.account_tree_outlined;
      case ElementType.kpiStrip:
        return Icons.view_column_outlined;
      default:
        return Icons.widgets_outlined;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 260,
      decoration: const BoxDecoration(
        color: Color(0xFF1E293B), // Figma dark slate panel
        border: Border(right: BorderSide(color: Color(0xFF334155))),
      ),
      child: Column(
        children: [
          // Header: Layers title + Group / Ungroup buttons
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Color(0xFF334155))),
            ),
            child: Row(
              children: [
                const Icon(Icons.layers, color: Color(0xFF38BDF8), size: 15),
                const SizedBox(width: 6),
                const Expanded(
                  child: Text(
                    'Layers',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                // Group button (Ctrl+G)
                IconButton(
                  icon: const Icon(Icons.folder_open, size: 15, color: Color(0xFF94A3B8)),
                  tooltip: '그룹화 (Ctrl+G)',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 22, minHeight: 22),
                  onPressed: onGroupSelected,
                ),
                // Ungroup button (Ctrl+Shift+G)
                IconButton(
                  icon: const Icon(Icons.call_split, size: 15, color: Color(0xFF94A3B8)),
                  tooltip: '그룹 분해 (Ctrl+Shift+G)',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 22, minHeight: 22),
                  onPressed: onUngroupSelected,
                ),
              ],
            ),
          ),

          // Layer item list (Z-index order from top to bottom)
          Expanded(
            child: slide.elements.isEmpty
                ? const Center(
                    child: Text(
                      '요소 없음',
                      style: TextStyle(color: Color(0xFF64748B), fontSize: 11),
                    ),
                  )
                : ReorderableListView.builder(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    itemCount: slide.elements.length,
                    onReorder: (oldIndex, newIndex) {
                      // Reverse index to map visually: top of list = front of stack
                      final actualOld = slide.elements.length - 1 - oldIndex;
                      var actualNew = slide.elements.length - 1 - newIndex;
                      if (oldIndex < newIndex) {
                        actualNew += 1;
                      }
                      final item = slide.elements.removeAt(actualOld);
                      slide.elements.insert(actualNew.clamp(0, slide.elements.length), item);
                      onSlideModified();
                    },
                    itemBuilder: (context, index) {
                      // Topmost visual item is last element in stack (highest z-index)
                      final actualIndex = slide.elements.length - 1 - index;
                      final elem = slide.elements[actualIndex];
                      final isSelected = selectedElement?.id == elem.id;

                      return _buildLayerItem(elem, isSelected, ValueKey(elem.id));
                    },
                  ),
          ),

          // Bottom summary bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: const BoxDecoration(
              color: Color(0xFF0F172A),
              border: Border(top: BorderSide(color: Color(0xFF334155))),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '${slide.elements.length}개 레이어',
                  style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10.5),
                ),
                Text(
                  selectedElement != null ? '1개 선택됨' : '선택 없음',
                  style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 10.5, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLayerItem(DeckElement elem, bool isSelected, Key key) {
    final isGroup = elem.type == ElementType.group || elem.children.isNotEmpty;
    final isAutoLayout = elem.autoLayoutDirection != AutoLayoutDirection.none;

    return Container(
      key: key,
      margin: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
      decoration: BoxDecoration(
        color: isSelected ? const Color(0xFF0052FF).withOpacity(0.3) : Colors.transparent,
        borderRadius: BorderRadius.circular(6),
        border: isSelected ? Border.all(color: const Color(0xFF0052FF), width: 1) : null,
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(6),
          onTap: () => onElementSelected(elem),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            child: Row(
              children: [
                // Icon
                Icon(
                  isGroup
                      ? (isAutoLayout ? Icons.view_stream : Icons.folder_outlined)
                      : _getElementIcon(elem.type),
                  color: isSelected
                      ? const Color(0xFF38BDF8)
                      : (elem.isVisible ? const Color(0xFF94A3B8) : const Color(0xFF475569)),
                  size: 15,
                ),
                const SizedBox(width: 8),

                // Name & Type badge
                Expanded(
                  child: Row(
                    children: [
                      Flexible(
                        child: Text(
                          elem.name,
                          style: TextStyle(
                            color: elem.isVisible
                                ? (isSelected ? Colors.white : const Color(0xFFE2E8F0))
                                : const Color(0xFF64748B),
                            fontSize: 11.5,
                            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      if (isAutoLayout) ...[
                        const SizedBox(width: 6),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
                          decoration: BoxDecoration(
                            color: const Color(0xFF0284C7).withOpacity(0.3),
                            borderRadius: BorderRadius.circular(3),
                          ),
                          child: Text(
                            elem.autoLayoutDirection == AutoLayoutDirection.horizontal ? 'H' : 'V',
                            style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 9, fontWeight: FontWeight.bold),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),

                // Lock toggle button
                IconButton(
                  icon: Icon(
                    elem.isLocked ? Icons.lock : Icons.lock_open,
                    size: 13,
                    color: elem.isLocked ? const Color(0xFFF59E0B) : const Color(0xFF475569),
                  ),
                  tooltip: elem.isLocked ? '잠금 해제' : '잠금',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
                  onPressed: () {
                    elem.isLocked = !elem.isLocked;
                    onSlideModified();
                  },
                ),

                // Visibility toggle button
                IconButton(
                  icon: Icon(
                    elem.isVisible ? Icons.visibility : Icons.visibility_off,
                    size: 13,
                    color: elem.isVisible ? const Color(0xFF94A3B8) : const Color(0xFF475569),
                  ),
                  tooltip: elem.isVisible ? '숨기기' : '표시하기',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
                  onPressed: () {
                    elem.isVisible = !elem.isVisible;
                    onSlideModified();
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

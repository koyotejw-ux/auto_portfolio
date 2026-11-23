import 'package:flutter/material.dart';
import '../models/deck_model.dart';

class FigmaLayersPanel extends StatefulWidget {
  final DeckSlide slide;
  final DeckElement? selectedElement;
  final ValueChanged<DeckElement?> onElementSelected;
  final VoidCallback onSlideModified;
  final VoidCallback onGroupSelected;
  final VoidCallback onUngroupSelected;
  final VoidCallback? onCopySelected;
  final VoidCallback? onPasteSelected;
  final bool canPaste;

  const FigmaLayersPanel({
    super.key,
    required this.slide,
    required this.selectedElement,
    required this.onElementSelected,
    required this.onSlideModified,
    required this.onGroupSelected,
    required this.onUngroupSelected,
    this.onCopySelected,
    this.onPasteSelected,
    this.canPaste = false,
  });

  @override
  State<FigmaLayersPanel> createState() => _FigmaLayersPanelState();
}

class _FigmaLayersPanelState extends State<FigmaLayersPanel> {
  final Set<String> _expandedGroupIds = {};

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
      width: 270,
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
                    'Layers & Hierarchy',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                // Copy Component (Ctrl+C)
                if (widget.onCopySelected != null)
                  IconButton(
                    icon: const Icon(Icons.copy, size: 14, color: Color(0xFF38BDF8)),
                    tooltip: '선택 컴포넌트 복사 (하위 포함, Ctrl+C)',
                    visualDensity: VisualDensity.compact,
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
                    onPressed: widget.selectedElement != null ? widget.onCopySelected : null,
                  ),
                // Paste Component (Ctrl+V)
                if (widget.onPasteSelected != null)
                  IconButton(
                    icon: Icon(Icons.paste, size: 14, color: widget.canPaste ? const Color(0xFF38BDF8) : const Color(0xFF475569)),
                    tooltip: '컴포넌트 붙여넣기 (Ctrl+V)',
                    visualDensity: VisualDensity.compact,
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
                    onPressed: widget.canPaste ? widget.onPasteSelected : null,
                  ),
                // Group button (Ctrl+G)
                IconButton(
                  icon: const Icon(Icons.folder_open, size: 15, color: Color(0xFF94A3B8)),
                  tooltip: '그룹화 (Ctrl+G)',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
                  onPressed: widget.onGroupSelected,
                ),
                // Ungroup button (Ctrl+Shift+G)
                IconButton(
                  icon: const Icon(Icons.call_split, size: 15, color: Color(0xFF94A3B8)),
                  tooltip: '그룹 분해 (Ctrl+Shift+G)',
                  visualDensity: VisualDensity.compact,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 20, minHeight: 20),
                  onPressed: widget.onUngroupSelected,
                ),
              ],
            ),
          ),

          // Layer item list (Z-index order from top to bottom)
          Expanded(
            child: widget.slide.elements.isEmpty
                ? const Center(
                    child: Text(
                      '요소 없음',
                      style: TextStyle(color: Color(0xFF64748B), fontSize: 11),
                    ),
                  )
                : ListView(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    children: widget.slide.elements.reversed.map((elem) {
                      return _buildElementTreeItem(elem, depth: 0);
                    }).toList(),
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
                  '${widget.slide.elements.length}개 최상위 레이어',
                  style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10.5),
                ),
                Text(
                  widget.selectedElement != null ? widget.selectedElement!.name : '선택 없음',
                  style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 10.5, fontWeight: FontWeight.bold),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildElementTreeItem(DeckElement elem, {int depth = 0}) {
    final hasChildren = elem.children.isNotEmpty;
    final isExpanded = _expandedGroupIds.contains(elem.id) || depth > 0;
    final isSelected = widget.selectedElement?.id == elem.id;
    final isAutoLayout = elem.autoLayoutDirection != AutoLayoutDirection.none;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          margin: EdgeInsets.only(left: 4.0 + (depth * 14.0), right: 4.0, top: 1.0, bottom: 1.0),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFF0052FF).withOpacity(0.3) : Colors.transparent,
            borderRadius: BorderRadius.circular(6),
            border: isSelected ? Border.all(color: const Color(0xFF0052FF), width: 1) : null,
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              borderRadius: BorderRadius.circular(6),
              onTap: () => widget.onElementSelected(elem),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 5),
                child: Row(
                  children: [
                    // Expand/Collapse Chevron for groups
                    if (hasChildren)
                      GestureDetector(
                        onTap: () {
                          setState(() {
                            if (_expandedGroupIds.contains(elem.id)) {
                              _expandedGroupIds.remove(elem.id);
                            } else {
                              _expandedGroupIds.add(elem.id);
                            }
                          });
                        },
                        child: Icon(
                          isExpanded ? Icons.keyboard_arrow_down : Icons.keyboard_arrow_right,
                          color: const Color(0xFF94A3B8),
                          size: 16,
                        ),
                      )
                    else
                      const SizedBox(width: 8),

                    // Icon
                    Icon(
                      hasChildren
                          ? (isAutoLayout ? Icons.view_stream : Icons.folder_outlined)
                          : _getElementIcon(elem.type),
                      color: isSelected
                          ? const Color(0xFF38BDF8)
                          : (elem.isVisible ? const Color(0xFF94A3B8) : const Color(0xFF475569)),
                      size: 14,
                    ),
                    const SizedBox(width: 6),

                    // Name & AutoLayout badge
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
                                fontSize: 11,
                                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (isAutoLayout) ...[
                            const SizedBox(width: 4),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
                              decoration: BoxDecoration(
                                color: const Color(0xFF0284C7).withOpacity(0.3),
                                borderRadius: BorderRadius.circular(3),
                              ),
                              child: Text(
                                elem.autoLayoutDirection == AutoLayoutDirection.horizontal ? 'H' : 'V',
                                style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 8.5, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),

                    // Lock button
                    IconButton(
                      icon: Icon(
                        elem.isLocked ? Icons.lock : Icons.lock_open,
                        size: 12,
                        color: elem.isLocked ? const Color(0xFFF59E0B) : const Color(0xFF475569),
                      ),
                      tooltip: elem.isLocked ? '잠금 해제' : '잠금',
                      visualDensity: VisualDensity.compact,
                      padding: EdgeInsets.zero,
                      constraints: const BoxConstraints(minWidth: 18, minHeight: 18),
                      onPressed: () {
                        elem.isLocked = !elem.isLocked;
                        widget.onSlideModified();
                      },
                    ),

                    // Visibility button
                    IconButton(
                      icon: Icon(
                        elem.isVisible ? Icons.visibility : Icons.visibility_off,
                        size: 12,
                        color: elem.isVisible ? const Color(0xFF94A3B8) : const Color(0xFF475569),
                      ),
                      tooltip: elem.isVisible ? '숨기기' : '표시하기',
                      visualDensity: VisualDensity.compact,
                      padding: EdgeInsets.zero,
                      constraints: const BoxConstraints(minWidth: 18, minHeight: 18),
                      onPressed: () {
                        elem.isVisible = !elem.isVisible;
                        widget.onSlideModified();
                      },
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),

        // Recursive Children rendering if expanded
        if (hasChildren && isExpanded)
          ...elem.children.map((child) => _buildElementTreeItem(child, depth: depth + 1)),
      ],
    );
  }
}

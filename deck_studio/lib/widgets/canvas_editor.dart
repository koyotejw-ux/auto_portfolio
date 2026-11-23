import 'dart:io';
import 'package:flutter/material.dart';
import '../models/deck_model.dart';
import 'figma_assets_panel.dart';

class CanvasEditor extends StatefulWidget {
  final DeckSlide slide;
  final DeckElement? selectedElement;
  final ValueChanged<DeckElement?> onElementSelected;
  final VoidCallback onSlideModified;
  final bool showLayoutGrid;
  final bool showRulers;

  const CanvasEditor({
    super.key,
    required this.slide,
    required this.selectedElement,
    required this.onElementSelected,
    required this.onSlideModified,
    this.showLayoutGrid = false,
    this.showRulers = true,
  });

  @override
  State<CanvasEditor> createState() => _CanvasEditorState();
}

class _CanvasEditorState extends State<CanvasEditor> {
  double _scale = 0.55;
  String? _editingElementId;
  final TextEditingController _inlineTextController = TextEditingController();
  final FocusNode _inlineFocusNode = FocusNode();

  @override
  void dispose() {
    _inlineTextController.dispose();
    _inlineFocusNode.dispose();
    super.dispose();
  }

  void _startEditing(DeckElement elem) {
    final textValue = (elem.props['title'] ??
            elem.props['text'] ??
            (elem.props['titleBlack'] != null || elem.props['titleBlue'] != null
                ? '${elem.props['titleBlack'] ?? ''}${elem.props['titleBlue'] ?? ''}'
                : elem.props['subtitle'] ?? elem.props['badge'] ?? elem.props['num'] ?? elem.props['tag'] ?? elem.name))
        .toString();

    setState(() {
      _editingElementId = elem.id;
      _inlineTextController.text = textValue;
      _inlineTextController.selection = TextSelection(baseOffset: 0, extentOffset: textValue.length);
    });
    widget.onElementSelected(elem);
    _inlineFocusNode.requestFocus();
  }

  void _finishEditing(DeckElement elem) {
    if (_editingElementId != elem.id) return;
    final newText = _inlineTextController.text;
    setState(() {
      _editingElementId = null;
      if (elem.props.containsKey('title') || (!elem.props.containsKey('titleBlack') && !elem.props.containsKey('subtitle'))) {
        elem.props['title'] = newText;
      } else if (elem.props.containsKey('titleBlack') || elem.props.containsKey('titleBlue')) {
        elem.props['titleBlack'] = newText;
        elem.props['titleBlue'] = '';
      } else if (elem.props.containsKey('subtitle')) {
        elem.props['subtitle'] = newText;
      } else {
        elem.name = newText;
      }
    });
    widget.onSlideModified();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Top Toolbar: Zoom Controls & Slide Title
        Container(
          height: 48,
          padding: const EdgeInsets.symmetric(horizontal: 16),
          decoration: const BoxDecoration(
            color: Colors.white,
            border: Border(bottom: BorderSide(color: Color(0xFFE2E8F0))),
          ),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  widget.slide.title,
                  style: const TextStyle(
                    color: Color(0xFF0F172A),
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.zoom_out, size: 20),
                onPressed: () {
                  setState(() {
                    if (_scale > 0.25) _scale -= 0.05;
                  });
                },
                tooltip: '축소',
              ),
              Text(
                '${(_scale * 100).toInt()}%',
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
              ),
              IconButton(
                icon: const Icon(Icons.zoom_in, size: 20),
                onPressed: () {
                  setState(() {
                    if (_scale < 1.0) _scale += 0.05;
                  });
                },
                tooltip: '확대',
              ),
              const SizedBox(width: 8),
              ElevatedButton.icon(
                icon: const Icon(Icons.fit_screen, size: 14),
                label: const Text('핏', style: TextStyle(fontSize: 11)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFF1F5F9),
                  foregroundColor: const Color(0xFF334155),
                  elevation: 0,
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                ),
                onPressed: () {
                  setState(() {
                    _scale = 0.55;
                  });
                },
              ),
            ],
          ),
        ),

        // Scrollable 1920x1080 Canvas Area
        Expanded(
          child: Container(
            color: const Color(0xFFE2E8F0),
            child: InteractiveViewer(
              constrained: false,
              boundaryMargin: const EdgeInsets.all(200),
              minScale: 0.2,
              maxScale: 2.0,
              child: Padding(
                padding: const EdgeInsets.all(40),
                child: Center(
                  child: Container(
                    width: 1920,
                    height: 1080,
                    decoration: BoxDecoration(
                      color: widget.slide.backgroundColor,
                      borderRadius: BorderRadius.circular(8),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.12),
                          blurRadius: 30,
                          offset: const Offset(0, 10),
                        ),
                      ],
                    ),
                    child: Stack(
                      clipBehavior: Clip.none,
                      children: [
                        // Slide Background Click to Deselect & Drop Target from AutoLayout to Canvas & Assets Drop
                        Positioned.fill(
                          child: DragTarget<Object>(
                            onWillAcceptWithDetails: (details) => true,
                            onAcceptWithDetails: (details) {
                              final droppedData = details.data;
                              if (droppedData is DeckElement) {
                                setState(() {
                                  final dropped = droppedData;
                                  final oldParent = _findParentOf(widget.slide.elements, dropped);
                                  if (oldParent != null) {
                                    oldParent.children.removeWhere((c) => c.id == dropped.id);
                                    oldParent.applyAutoLayout();
                                    dropped.x = (oldParent.x + dropped.x).clamp(50.0, 1800.0);
                                    dropped.y = (oldParent.y + dropped.y + 60.0).clamp(50.0, 1000.0);
                                    widget.slide.elements.add(dropped);
                                    widget.onElementSelected(dropped);
                                  }
                                });
                                widget.onSlideModified();
                              } else if (droppedData is AssetDragData) {
                                setState(() {
                                  final renderBox = context.findRenderObject() as RenderBox?;
                                  Offset localPos = const Offset(200, 200);
                                  if (renderBox != null) {
                                    try {
                                      localPos = renderBox.globalToLocal(details.offset);
                                    } catch (_) {}
                                  }

                                  if (droppedData.type == AssetDragType.color) {
                                    widget.slide.backgroundColor = droppedData.payload as Color;
                                  } else if (droppedData.type == AssetDragType.icon) {
                                    final iconVal = droppedData.payload as String;
                                    final newElem = DeckElement(
                                      id: 'icon_${DateTime.now().millisecondsSinceEpoch}',
                                      type: ElementType.shape,
                                      name: droppedData.title,
                                      x: localPos.dx.clamp(50.0, 1750.0),
                                      y: localPos.dy.clamp(50.0, 950.0),
                                      width: 64.0,
                                      height: 64.0,
                                      textStyle: DeckTextStyle(color: const Color(0xFF0052FF), fontSize: 48),
                                      props: {'icon': iconVal, 'title': ''},
                                    );
                                    widget.slide.elements.add(newElem);
                                    widget.onElementSelected(newElem);
                                  } else if (droppedData.type == AssetDragType.component) {
                                    final comp = droppedData.payload as Map<String, dynamic>;
                                    final newElem = DeckElement(
                                      id: 'comp_${DateTime.now().millisecondsSinceEpoch}',
                                      type: comp['type'] as ElementType,
                                      name: droppedData.title,
                                      x: localPos.dx.clamp(50.0, 1600.0),
                                      y: localPos.dy.clamp(50.0, 900.0),
                                      width: comp['width'] as double,
                                      height: comp['height'] as double,
                                      boxStyle: comp['boxStyle'] as DeckBoxStyle?,
                                      props: Map<String, dynamic>.from(comp['props'] ?? {}),
                                    );
                                    widget.slide.elements.add(newElem);
                                    widget.onElementSelected(newElem);
                                  }
                                });
                                widget.onSlideModified();
                              }
                            },
                            builder: (context, candidateData, rejectedData) {
                              return GestureDetector(
                                onTap: () => widget.onElementSelected(null),
                                behavior: HitTestBehavior.opaque,
                                child: const SizedBox.expand(),
                              );
                            },
                          ),
                        ),

                        // Figma Layout Grid Overlay (Ctrl + Shift + 4 or Ctrl + ')
                        if (widget.showLayoutGrid)
                          Positioned.fill(
                            child: IgnorePointer(
                              child: CustomPaint(
                                painter: _FigmaLayoutGridPainter(),
                              ),
                            ),
                          ),

                        // Interactive Elements
                        ...widget.slide.elements.where((elem) => elem.isVisible).map((elem) {
                          final isSelected = widget.selectedElement?.id == elem.id;
                          return Positioned(
                            left: elem.x,
                            top: elem.y,
                            width: elem.width,
                            height: elem.height,
                            child: GestureDetector(
                              onTap: () => widget.onElementSelected(elem),
                              onDoubleTap: () => _startEditing(elem),
                              onPanUpdate: elem.isLocked || _editingElementId == elem.id
                                  ? null
                                  : (details) {
                                      setState(() {
                                        elem.x += details.delta.dx;
                                        elem.y += details.delta.dy;
                                      });
                                      widget.onSlideModified();
                                    },
                              child: Container(
                                decoration: BoxDecoration(
                                  border: isSelected
                                      ? Border.all(color: const Color(0xFF0052FF), width: 2)
                                      : (elem.type == ElementType.group
                                          ? Border.all(color: const Color(0xFF38BDF8).withOpacity(0.3), width: 1)
                                          : null),
                                ),
                                child: Stack(
                                  clipBehavior: Clip.none,
                                  children: [
                                    _buildInnerElement(elem),
                                    if (isSelected)
                                      Positioned(
                                        top: -24,
                                        left: 0,
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                          decoration: BoxDecoration(
                                            color: elem.isLocked ? const Color(0xFFF59E0B) : const Color(0xFF0052FF),
                                            borderRadius: BorderRadius.circular(4),
                                          ),
                                          child: Row(
                                            mainAxisSize: MainAxisSize.min,
                                            children: [
                                              if (elem.isLocked) ...[
                                                const Icon(Icons.lock, color: Colors.white, size: 10),
                                                const SizedBox(width: 4),
                                              ],
                                              Text(
                                                '${elem.name} (${elem.x.toInt()}, ${elem.y.toInt()}) [${elem.width.toInt()}×${elem.height.toInt()}]',
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontSize: 10,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    if (isSelected && !elem.isLocked) ...[
                                      // Top-Left Handle
                                      Positioned(
                                        left: -6,
                                        top: -6,
                                        child: GestureDetector(
                                          onPanUpdate: (details) {
                                            setState(() {
                                              final newW = (elem.width - details.delta.dx).clamp(40.0, 1920.0);
                                              final newH = (elem.height - details.delta.dy).clamp(24.0, 1080.0);
                                              elem.x += (elem.width - newW);
                                              elem.y += (elem.height - newH);
                                              elem.width = newW;
                                              elem.height = newH;
                                              elem.applyAutoLayout();
                                            });
                                            widget.onSlideModified();
                                          },
                                          child: _buildFigmaHandle(),
                                        ),
                                      ),
                                      // Top-Right Handle
                                      Positioned(
                                        right: -6,
                                        top: -6,
                                        child: GestureDetector(
                                          onPanUpdate: (details) {
                                            setState(() {
                                              final newH = (elem.height - details.delta.dy).clamp(24.0, 1080.0);
                                              elem.y += (elem.height - newH);
                                              elem.height = newH;
                                              elem.width = (elem.width + details.delta.dx).clamp(40.0, 1920.0);
                                              elem.applyAutoLayout();
                                            });
                                            widget.onSlideModified();
                                          },
                                          child: _buildFigmaHandle(),
                                        ),
                                      ),
                                      // Bottom-Left Handle
                                      Positioned(
                                        left: -6,
                                        bottom: -6,
                                        child: GestureDetector(
                                          onPanUpdate: (details) {
                                            setState(() {
                                              final newW = (elem.width - details.delta.dx).clamp(40.0, 1920.0);
                                              elem.x += (elem.width - newW);
                                              elem.width = newW;
                                              elem.height = (elem.height + details.delta.dy).clamp(24.0, 1080.0);
                                              elem.applyAutoLayout();
                                            });
                                            widget.onSlideModified();
                                          },
                                          child: _buildFigmaHandle(),
                                        ),
                                      ),
                                      // Bottom-Right Handle
                                      Positioned(
                                        right: -6,
                                        bottom: -6,
                                        child: GestureDetector(
                                          onPanUpdate: (details) {
                                            setState(() {
                                              elem.width = (elem.width + details.delta.dx).clamp(40.0, 1920.0);
                                              elem.height = (elem.height + details.delta.dy).clamp(24.0, 1080.0);
                                              elem.applyAutoLayout();
                                            });
                                            widget.onSlideModified();
                                          },
                                          child: _buildFigmaHandle(),
                                        ),
                                      ),
                                    ],
                                  ],
                                ),
                              ),
                            ),
                          );
                        }),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildFigmaHandle() {
    return Container(
      width: 11,
      height: 11,
      decoration: BoxDecoration(
        color: Colors.white,
        shape: BoxShape.rectangle,
        borderRadius: BorderRadius.circular(2),
        border: Border.all(color: const Color(0xFF0052FF), width: 1.8),
        boxShadow: const [
          BoxShadow(color: Color(0x33000000), blurRadius: 4, offset: Offset(0, 1)),
        ],
      ),
    );
  }

  Widget _buildInnerElement(DeckElement elem) {
    switch (elem.type) {
      case ElementType.header:
        return _buildHeader(elem);
      case ElementType.text:
        return _buildText(elem);
      case ElementType.flowchart:
        return _buildFlowchart(elem);
      case ElementType.kpiStrip:
        return _buildKpiStrip(elem);
      case ElementType.mockupPlaceholder:
        return _buildMockupPlaceholder(elem);
      case ElementType.designTokens:
        return _buildDesignTokens(elem);
      case ElementType.donutChart:
        return _buildDonutChart(elem);
      case ElementType.statCard:
        return _buildStatCard(elem);
      case ElementType.shape:
        return _buildShape(elem);
      case ElementType.group:
        return _buildGroup(elem);
      case ElementType.badge:
        return _buildBadge(elem);
      case ElementType.vectorIcon:
        return _buildVectorIcon(elem);
      default:
        return Container(
          padding: EdgeInsets.all(elem.boxStyle.padding),
          decoration: elem.boxStyle.toDecoration(),
          child: Center(
            child: Text(elem.name, style: const TextStyle(fontSize: 12)),
          ),
        );
    }
  }

  Widget _buildHeader(DeckElement elem) {
    final badge = elem.props['badge'] ?? '2026 CASE STUDY';
    final meta = elem.props['meta'] ?? 'Header Meta';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(height: 1, color: const Color(0xFFE2E8F0)),
        const SizedBox(height: 14),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
              decoration: BoxDecoration(
                color: const Color(0xFFEFF6FF),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFFBFDBFE)),
              ),
              child: Text(
                badge,
                style: const TextStyle(
                  color: Color(0xFF0052FF),
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Text(
              meta,
              style: const TextStyle(
                color: Color(0xFF64748B),
                fontSize: 13,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildText(DeckElement elem) {
    if (_editingElementId == elem.id) {
      final ts = elem.textStyle;
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(4),
          border: Border.all(color: const Color(0xFF0052FF), width: 2),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF0052FF).withValues(alpha: 0.18),
              blurRadius: 8,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: TextField(
          controller: _inlineTextController,
          focusNode: _inlineFocusNode,
          autofocus: true,
          maxLines: null,
          textAlign: ts.flutterTextAlign,
          style: ts.toTextStyle(),
          decoration: const InputDecoration(
            isDense: true,
            contentPadding: EdgeInsets.zero,
            border: InputBorder.none,
          ),
          onSubmitted: (_) => _finishEditing(elem),
          onTapOutside: (_) => _finishEditing(elem),
        ),
      );
    }

    final category = elem.props['category'];
    final titleBlack = elem.props['titleBlack'] ?? '';
    final titleBlue = elem.props['titleBlue'] ?? '';
    final subtitle = elem.props['subtitle'] ?? '';
    final plainTitle = (elem.props['title'] ?? elem.props['text']) as String?;

    final ts = elem.textStyle;
    final align = ts.flutterTextAlign;
    final crossAlign = align == TextAlign.center
        ? CrossAxisAlignment.center
        : (align == TextAlign.right
            ? CrossAxisAlignment.end
            : CrossAxisAlignment.start);

    // If it's a decomposed title component or pure single text element
    if (plainTitle != null && category == null && titleBlack.isEmpty && titleBlue.isEmpty) {
      return Text(
        plainTitle,
        textAlign: align,
        style: ts.toTextStyle(),
      );
    }

    return Column(
      crossAxisAlignment: crossAlign,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (category != null) ...[
          Text(
            category,
            textAlign: align,
            style: TextStyle(
              fontFamily: ts.fontFamily,
              color: const Color(0xFF0052FF),
              fontSize: 14,
              fontWeight: FontWeight.bold,
              letterSpacing: ts.letterSpacing,
            ),
          ),
          const SizedBox(height: 8),
        ],
        if (titleBlack.isNotEmpty || titleBlue.isNotEmpty)
          RichText(
            textAlign: align,
            text: TextSpan(
              children: [
                TextSpan(
                  text: titleBlack,
                  style: TextStyle(
                    fontFamily: ts.fontFamily,
                    color: ts.color,
                    fontSize: ts.fontSize,
                    fontWeight: ts.fontWeight,
                    letterSpacing: ts.letterSpacing,
                    height: ts.height,
                    wordSpacing: ts.wordSpacing,
                  ),
                ),
                TextSpan(
                  text: titleBlue,
                  style: TextStyle(
                    fontFamily: ts.fontFamily,
                    color: const Color(0xFF0052FF),
                    fontSize: ts.fontSize,
                    fontWeight: ts.fontWeight,
                    letterSpacing: ts.letterSpacing,
                    height: ts.height,
                    wordSpacing: ts.wordSpacing,
                  ),
                ),
              ],
            ),
          ),
        if (subtitle.isNotEmpty) ...[
          const SizedBox(height: 8),
          Text(
            subtitle,
            textAlign: align,
            style: TextStyle(
              fontFamily: ts.fontFamily,
              color: const Color(0xFF475569),
              fontSize: 13.5,
              height: 1.5,
              letterSpacing: ts.letterSpacing,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildBadge(DeckElement elem) {
    final num = elem.props['num'] as String?;
    final tag = elem.props['tag'] as String?;
    final badge = elem.props['badge'] as String?;
    final category = elem.props['category'] as String?;
    final title = elem.props['title'] as String? ?? elem.name;
    final ts = elem.textStyle;

    if (num != null && num.isNotEmpty) {
      return Container(
        padding: EdgeInsets.all(elem.boxStyle.padding > 0 ? elem.boxStyle.padding : 4),
        decoration: elem.boxStyle.backgroundColor != Colors.transparent || elem.boxStyle.borderWidth > 0
            ? elem.boxStyle.toDecoration()
            : BoxDecoration(
                color: const Color(0xFFF1F5F9),
                borderRadius: BorderRadius.circular(elem.boxStyle.borderRadius > 0 ? elem.boxStyle.borderRadius : 6),
              ),
        child: Text(
          num,
          style: ts.fontSize != 16.0 || ts.color != const Color(0xFF0F172A)
              ? ts.toTextStyle()
              : const TextStyle(
                  color: Color(0xFF0052FF),
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                ),
        ),
      );
    }

    if (tag != null && tag.isNotEmpty) {
      return Container(
        padding: EdgeInsets.all(elem.boxStyle.padding > 0 ? elem.boxStyle.padding : 4),
        decoration: elem.boxStyle.backgroundColor != Colors.transparent || elem.boxStyle.borderWidth > 0
            ? elem.boxStyle.toDecoration()
            : BoxDecoration(
                color: const Color(0xFFEFF6FF),
                borderRadius: BorderRadius.circular(elem.boxStyle.borderRadius > 0 ? elem.boxStyle.borderRadius : 12),
              ),
        child: Text(
          tag,
          style: ts.fontSize != 16.0 || ts.color != const Color(0xFF0F172A)
              ? ts.toTextStyle()
              : const TextStyle(
                  color: Color(0xFF0052FF),
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
        ),
      );
    }

    if (badge != null && badge.isNotEmpty) {
      return Container(
        padding: EdgeInsets.symmetric(
          horizontal: elem.boxStyle.padding > 0 ? elem.boxStyle.padding : 14,
          vertical: elem.boxStyle.padding > 0 ? elem.boxStyle.padding * 0.4 : 5,
        ),
        decoration: elem.boxStyle.backgroundColor != Colors.transparent || elem.boxStyle.borderWidth > 0
            ? elem.boxStyle.toDecoration()
            : BoxDecoration(
                color: const Color(0xFFEFF6FF),
                borderRadius: BorderRadius.circular(elem.boxStyle.borderRadius > 0 ? elem.boxStyle.borderRadius : 20),
                border: Border.all(color: const Color(0xFFBFDBFE)),
              ),
        child: Text(
          badge,
          style: ts.fontSize != 16.0 || ts.color != const Color(0xFF0F172A)
              ? ts.toTextStyle()
              : const TextStyle(
                  color: Color(0xFF0052FF),
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                ),
        ),
      );
    }

    return Container(
      padding: EdgeInsets.all(elem.boxStyle.padding > 0 ? elem.boxStyle.padding : 4),
      decoration: elem.boxStyle.backgroundColor != Colors.transparent || elem.boxStyle.borderWidth > 0
          ? elem.boxStyle.toDecoration()
          : BoxDecoration(
              color: const Color(0xFFEFF6FF),
              borderRadius: BorderRadius.circular(elem.boxStyle.borderRadius > 0 ? elem.boxStyle.borderRadius : 6),
            ),
      child: Text(
        category ?? title,
        style: ts.fontSize != 16.0 || ts.color != const Color(0xFF0F172A)
            ? ts.toTextStyle()
            : const TextStyle(
                color: Color(0xFF0052FF),
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
      ),
    );
  }

  Widget _buildVectorIcon(DeckElement elem) {
    final rawStrokes = elem.props['iconStrokes'] as List? ?? [];
    final strokeColor = Color(elem.props['strokeColor'] as int? ?? 0xFF0052FF);
    final strokeWidth = (elem.props['strokeWidth'] as num?)?.toDouble() ?? 2.0;
    final isFilled = elem.props['isFilled'] == true;
    final fillColor = Color(elem.props['fillColor'] as int? ?? 0x00000000);

    return Container(
      width: elem.width,
      height: elem.height,
      decoration: elem.boxStyle.backgroundColor != Colors.transparent || elem.boxStyle.borderWidth > 0
          ? elem.boxStyle.toDecoration()
          : null,
      child: CustomPaint(
        size: Size(elem.width, elem.height),
        painter: _VectorIconElementPainter(
          rawStrokes: rawStrokes,
          strokeColor: strokeColor,
          strokeWidth: strokeWidth,
          isFilled: isFilled,
          fillColor: fillColor,
        ),
      ),
    );
  }

  Widget _buildFlowchart(DeckElement elem) {
    final isKiosk = elem.props['isKioskCarousel'] == true;
    if (isKiosk) {
      final stages = (elem.props['stages'] as List? ?? []);
      return Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: stages.map<Widget>((st) {
          final sMap = Map<String, dynamic>.from(st);
          return Expanded(
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 8),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFFE2E8F0)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: const Color(0xFFEFF6FF),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          sMap['step'] ?? '',
                          style: const TextStyle(
                            color: Color(0xFF0052FF),
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: const Color(0xFFF1F5F9),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          sMap['badge'] ?? '',
                          style: const TextStyle(
                            color: Color(0xFF334155),
                            fontSize: 9.5,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    sMap['title'] ?? '',
                    style: const TextStyle(
                      color: Color(0xFF0F172A),
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    sMap['sub'] ?? '',
                    style: const TextStyle(color: Color(0xFF64748B), fontSize: 10),
                  ),
                  const SizedBox(height: 12),
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFF0F172A),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.tablet_mac, color: Colors.white, size: 36),
                            const SizedBox(height: 8),
                            Text(
                              sMap['title'] ?? '',
                              style: const TextStyle(color: Colors.white70, fontSize: 11),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  ...((sMap['features'] as List? ?? []).map((f) => Padding(
                        padding: const EdgeInsets.only(bottom: 4),
                        child: Row(
                          children: [
                            const Icon(Icons.check_circle, color: Color(0xFF0052FF), size: 12),
                            const SizedBox(width: 6),
                            Expanded(
                              child: Text(
                                f.toString(),
                                style: const TextStyle(color: Color(0xFF334155), fontSize: 10),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ],
                        ),
                      ))),
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                    decoration: BoxDecoration(
                      color: const Color(0xFFEFF6FF),
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(color: const Color(0xFFBFDBFE)),
                    ),
                    child: Center(
                      child: Text(
                        sMap['interaction'] ?? '',
                        style: const TextStyle(
                          color: Color(0xFF0052FF),
                          fontSize: 9,
                          fontWeight: FontWeight.bold,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        }).toList(),
      );
    }

    final items = (elem.props['items'] as List? ?? []);
    return Column(
      children: items.map<Widget>((item) {
        final iMap = Map<String, dynamic>.from(item);
        return Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFE2E8F0)),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFF1F5F9),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  iMap['num'] ?? '01',
                  style: const TextStyle(
                    color: Color(0xFF0052FF),
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFEFF6FF),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  iMap['tag'] ?? '',
                  style: const TextStyle(
                    color: Color(0xFF0052FF),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      iMap['title'] ?? '',
                      style: const TextStyle(
                        color: Color(0xFF0F172A),
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      iMap['desc'] ?? '',
                      style: const TextStyle(
                        color: Color(0xFF475569),
                        fontSize: 11,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildMockupPlaceholder(DeckElement elem) {
    final title = elem.props['screenTitle'] ?? 'Mockup Screen';
    final showMascot = elem.props['showMascot'] == true;
    final imagePath = elem.props['imagePath'] as String?;

    if (imagePath != null && imagePath.isNotEmpty) {
      final file = File(imagePath);
      if (file.existsSync()) {
        return ClipRRect(
          borderRadius: BorderRadius.circular(elem.boxStyle.borderRadius),
          child: Image.file(
            file,
            fit: BoxFit.contain,
          ),
        );
      }
    }

    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFEFF6FF).withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFBFDBFE), width: 1.5),
      ),
      child: Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 220,
              height: 420,
              decoration: BoxDecoration(
                color: const Color(0xFF0F172A),
                borderRadius: BorderRadius.circular(32),
                border: Border.all(color: const Color(0xFF475569), width: 4),
              ),
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.phone_android, color: Colors.white, size: 48),
                    const SizedBox(height: 12),
                    Text(
                      title,
                      style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      '3D Perspective Rotated',
                      style: TextStyle(color: Color(0xFF06B6D4), fontSize: 10),
                    ),
                  ],
                ),
              ),
            ),
            if (showMascot) ...[
              const SizedBox(width: 40),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 140,
                    height: 140,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                      border: Border.all(color: const Color(0xFF0052FF), width: 3),
                    ),
                    child: const Center(
                      child: Icon(Icons.cruelty_free, color: Color(0xFF0052FF), size: 64),
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    'Passy (패시)',
                    style: TextStyle(color: Color(0xFF0F172A), fontSize: 13, fontWeight: FontWeight.bold),
                  ),
                  const Text(
                    '시그니처 바보털 3D 마스코트',
                    style: TextStyle(color: Color(0xFF64748B), fontSize: 10),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildKpiStrip(DeckElement elem) {
    final header = elem.props['header'];
    final items = (elem.props['items'] as List? ?? []);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
      decoration: BoxDecoration(
        color: const Color(0xFFF0F6FF),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFBFDBFE)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (header != null) ...[
            Text(
              header,
              style: const TextStyle(
                color: Color(0xFF0052FF),
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
          ],
          Expanded(
            child: Row(
              children: items.map<Widget>((item) {
                final iMap = Map<String, dynamic>.from(item);
                return Expanded(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10),
                    decoration: BoxDecoration(
                      border: Border(
                        right: items.last == item
                            ? BorderSide.none
                            : const BorderSide(color: Color(0xFFCBD5E1)),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          iMap['title'] ?? '',
                          style: const TextStyle(color: Color(0xFF64748B), fontSize: 10),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          iMap['val'] ?? '',
                          style: const TextStyle(
                            color: Color(0xFF0052FF),
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 2),
                        Text(
                          iMap['sub'] ?? '',
                          style: const TextStyle(color: Color(0xFF475569), fontSize: 9.5),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDesignTokens(DeckElement elem) {
    final colors = (elem.props['colors'] as List? ?? []);
    final typog = (elem.props['typography'] as List? ?? []);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Color Palette Tokens',
            style: TextStyle(color: Color(0xFF0F172A), fontSize: 13, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Row(
            children: colors.map<Widget>((c) {
              final cMap = Map<String, dynamic>.from(c);
              final hex = cMap['hex'] as String;
              final color = Color(int.parse(hex.replaceFirst('#', '0xFF')));
              return Expanded(
                child: Container(
                  margin: const EdgeInsets.only(right: 6),
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: color,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.black12),
                  ),
                  child: Column(
                    children: [
                      Text(
                        cMap['name'].toString().split(' ').last,
                        style: TextStyle(
                          color: color.computeLuminance() > 0.5 ? Colors.black87 : Colors.white,
                          fontSize: 9,
                          fontWeight: FontWeight.bold,
                        ),
                        maxLines: 1,
                      ),
                      Text(
                        hex,
                        style: TextStyle(
                          color: color.computeLuminance() > 0.5 ? Colors.black54 : Colors.white70,
                          fontSize: 8,
                        ),
                      ),
                    ],
                  ),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 16),
          const Text(
            'Typography Scale Tokens',
            style: TextStyle(color: Color(0xFF0F172A), fontSize: 13, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: ListView(
              children: typog.map<Widget>((t) {
                final tMap = Map<String, dynamic>.from(t);
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Row(
                    children: [
                      SizedBox(
                        width: 90,
                        child: Text(
                          tMap['level'] ?? '',
                          style: const TextStyle(color: Color(0xFF64748B), fontSize: 10),
                        ),
                      ),
                      SizedBox(
                        width: 90,
                        child: Text(
                          tMap['size'] ?? '',
                          style: const TextStyle(color: Color(0xFF0052FF), fontSize: 10, fontWeight: FontWeight.bold),
                        ),
                      ),
                      Expanded(
                        child: Text(
                          tMap['sample'] ?? '',
                          style: const TextStyle(color: Color(0xFF0F172A), fontSize: 11, fontWeight: FontWeight.w600),
                        ),
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDonutChart(DeckElement elem) {
    final title = elem.props['title'] ?? 'Metrics';
    final percentage = (elem.props['percentage'] as num? ?? 90).toDouble();

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        children: [
          Text(
            title,
            style: const TextStyle(color: Color(0xFF0F172A), fontSize: 14, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          Expanded(
            child: Center(
              child: Stack(
                alignment: Alignment.center,
                children: [
                  SizedBox(
                    width: 140,
                    height: 140,
                    child: CircularProgressIndicator(
                      value: percentage / 100,
                      strokeWidth: 16,
                      backgroundColor: const Color(0xFFEFF6FF),
                      valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF0052FF)),
                    ),
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        '$percentage%',
                        style: const TextStyle(
                          color: Color(0xFF0F172A),
                          fontSize: 26,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const Text(
                        'Compliant',
                        style: TextStyle(color: Color(0xFF64748B), fontSize: 10),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildShape(DeckElement elem) {
    final num = elem.props['num'] as String?;
    final tag = elem.props['tag'] as String?;
    final title = elem.props['title'] as String? ?? elem.name;
    final desc = elem.props['desc'] as String?;

    return Container(
      padding: EdgeInsets.all(elem.boxStyle.padding),
      decoration: elem.boxStyle.toDecoration(),
      child: num != null || tag != null
          ? Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (num != null && num.isNotEmpty) ...[
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF1F5F9),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      num,
                      style: const TextStyle(
                        color: Color(0xFF0052FF),
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                ],
                if (tag != null && tag.isNotEmpty) ...[
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: const Color(0xFFEFF6FF),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      tag,
                      style: const TextStyle(
                        color: Color(0xFF0052FF),
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                ],
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        title,
                        style: elem.textStyle.fontSize > 16 || elem.textStyle.letterSpacing != 0.0 || elem.textStyle.height != 1.4
                            ? elem.textStyle.toTextStyle()
                            : TextStyle(
                                fontFamily: elem.textStyle.fontFamily,
                                color: elem.textStyle.color,
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                              ),
                      ),
                      if (desc != null && desc.isNotEmpty) ...[
                        const SizedBox(height: 3),
                        Text(
                          desc,
                          style: const TextStyle(
                            color: Color(0xFF475569),
                            fontSize: 11,
                            height: 1.4,
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ],
            )
          : Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: elem.textStyle.toTextStyle(),
                ),
                if (desc != null && desc.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  Text(
                    desc,
                    style: const TextStyle(color: Color(0xFF64748B), fontSize: 13, height: 1.5),
                  ),
                ],
              ],
            ),
    );
  }

  Widget _buildStatCard(DeckElement elem) {
    final title = elem.props['title'] as String? ?? 'METRIC';
    final val = elem.props['val'] as String? ?? '-';
    final sub = elem.props['sub'] as String? ?? '';

    final isDark = elem.boxStyle.backgroundColor.computeLuminance() < 0.2;

    return Container(
      padding: EdgeInsets.all(elem.boxStyle.padding),
      decoration: elem.boxStyle.toDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            title,
            style: TextStyle(
              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
              fontSize: 10,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            val,
            style: TextStyle(
              color: isDark ? const Color(0xFF38BDF8) : const Color(0xFF0052FF),
              fontSize: 16,
              fontWeight: FontWeight.w900,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 2),
          Text(
            sub,
            style: TextStyle(
              color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF475569),
              fontSize: 9.5,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

    // Drag-and-drop helpers for Figma-style nesting & reordering
  DeckElement? _findParentOf(List<DeckElement> elements, DeckElement target) {
    for (final elem in elements) {
      if (elem.children.any((c) => c.id == target.id)) return elem;
      final found = _findParentOf(elem.children, target);
      if (found != null) return found;
    }
    return null;
  }

  void _reorderOrMoveChild(DeckElement container, DeckElement draggedItem, int targetIndex) {
    if (container.id == draggedItem.id) return;
    setState(() {
      final oldParent = _findParentOf(widget.slide.elements, draggedItem);
      if (oldParent != null) {
        oldParent.children.removeWhere((c) => c.id == draggedItem.id);
        oldParent.applyAutoLayout();
      } else {
        widget.slide.elements.removeWhere((e) => e.id == draggedItem.id);
      }

      final insertIdx = targetIndex.clamp(0, container.children.length);
      container.children.insert(insertIdx, draggedItem);
      container.applyAutoLayout();
      widget.onElementSelected(draggedItem);
    });
    widget.onSlideModified();
  }

    Widget _buildGroup(DeckElement elem) {
    if (elem.children.isEmpty) {
      return DragTarget<DeckElement>(
        onWillAcceptWithDetails: (details) => details.data.id != elem.id,
        onAcceptWithDetails: (details) {
          _reorderOrMoveChild(elem, details.data, 0);
        },
        builder: (context, candidateData, rejectedData) {
          final isHovered = candidateData.isNotEmpty;
          return Container(
            decoration: BoxDecoration(
              color: isHovered ? const Color(0xFF0052FF).withOpacity(0.08) : Colors.transparent,
              border: Border.all(
                color: isHovered ? const Color(0xFF0052FF) : const Color(0xFF38BDF8).withOpacity(0.4),
                width: isHovered ? 2 : 1,
              ),
              borderRadius: BorderRadius.circular(elem.boxStyle.borderRadius),
            ),
            child: Center(
              child: Text(
                isHovered ? '여기에 드롭하여 요소 추가' : elem.name,
                style: const TextStyle(color: Color(0xFF0284C7), fontSize: 11, fontWeight: FontWeight.bold),
              ),
            ),
          );
        },
      );
    }

    if (elem.autoLayoutDirection == AutoLayoutDirection.horizontal) {
      final childrenList = <Widget>[];
      // 1. Drop target before the first item (Index 0)
      childrenList.add(_buildBetweenGapDropZone(elem, 0, isHorizontal: true));

      for (int idx = 0; idx < elem.children.length; idx++) {
        // Child item wrapper
        childrenList.add(_buildAutoLayoutChildWrapper(elem, elem.children[idx], idx));
        // Drop target between item idx and idx+1 (Index idx + 1)
        childrenList.add(_buildBetweenGapDropZone(elem, idx + 1, isHorizontal: true));
      }

      return Padding(
        padding: EdgeInsets.all(elem.autoLayoutPadding),
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          physics: const NeverScrollableScrollPhysics(),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: childrenList,
          ),
        ),
      );
    } else if (elem.autoLayoutDirection == AutoLayoutDirection.vertical) {
      final childrenList = <Widget>[];
      // 1. Drop target before the first item (Index 0)
      childrenList.add(_buildBetweenGapDropZone(elem, 0, isHorizontal: false));

      for (int idx = 0; idx < elem.children.length; idx++) {
        // Child item wrapper
        childrenList.add(_buildAutoLayoutChildWrapper(elem, elem.children[idx], idx));
        // Drop target between item idx and idx+1 (Index idx + 1)
        childrenList.add(_buildBetweenGapDropZone(elem, idx + 1, isHorizontal: false));
      }

      return Padding(
        padding: EdgeInsets.all(elem.autoLayoutPadding),
        child: SingleChildScrollView(
          physics: const NeverScrollableScrollPhysics(),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: childrenList,
          ),
        ),
      );
    }

    // Freeform absolute children
    return Stack(
      children: elem.children.map((child) {
        final isChildSelected = widget.selectedElement?.id == child.id;
        return Positioned(
          left: child.x,
          top: child.y,
          width: child.width,
          height: child.height,
          child: GestureDetector(
            onTap: () => widget.onElementSelected(child),
            onPanUpdate: child.isLocked
                ? null
                : (details) {
                    setState(() {
                      child.x += details.delta.dx;
                      child.y += details.delta.dy;
                    });
                    widget.onSlideModified();
                  },
            child: Container(
              decoration: BoxDecoration(
                border: isChildSelected
                    ? Border.all(color: const Color(0xFF0052FF), width: 2)
                    : null,
              ),
              child: _buildInnerElement(child),
            ),
          ),
        );
      }).toList(),
    );
  }

  /// Gap Drop Zone between elements for Figma-style precision insertion
  Widget _buildBetweenGapDropZone(DeckElement parent, int insertIndex, {required bool isHorizontal}) {
    final gapSize = (parent.autoLayoutSpacing > 8.0 ? parent.autoLayoutSpacing : 12.0);

    return DragTarget<DeckElement>(
      onWillAcceptWithDetails: (details) => true,
      onAcceptWithDetails: (details) {
        _reorderOrMoveChild(parent, details.data, insertIndex);
      },
      builder: (context, candidateData, rejectedData) {
        final isHovered = candidateData.isNotEmpty;

        if (isHorizontal) {
          return AnimatedContainer(
            duration: const Duration(milliseconds: 150),
            width: isHovered ? (gapSize + 16.0) : gapSize,
            height: parent.height > 30 ? (parent.height * 0.8) : 32.0,
            alignment: Alignment.center,
            child: isHovered
                ? Container(
                    width: 4,
                    height: double.infinity,
                    decoration: BoxDecoration(
                      color: const Color(0xFF0052FF),
                      borderRadius: BorderRadius.circular(2),
                      boxShadow: const [
                        BoxShadow(
                          color: Color(0x660052FF),
                          blurRadius: 8,
                          spreadRadius: 2,
                        ),
                      ],
                    ),
                  )
                : const SizedBox.shrink(),
          );
        } else {
          return AnimatedContainer(
            duration: const Duration(milliseconds: 150),
            height: isHovered ? (gapSize + 16.0) : gapSize,
            width: parent.width > 50 ? (parent.width * 0.9) : 60.0,
            alignment: Alignment.center,
            child: isHovered
                ? Container(
                    height: 4,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: const Color(0xFF0052FF),
                      borderRadius: BorderRadius.circular(2),
                      boxShadow: const [
                        BoxShadow(
                          color: Color(0x660052FF),
                          blurRadius: 8,
                          spreadRadius: 2,
                        ),
                      ],
                    ),
                  )
                : const SizedBox.shrink(),
          );
        }
      },
    );
  }

  Widget _buildAutoLayoutChildWrapper(DeckElement parent, DeckElement child, int index) {
    final isChildSelected = widget.selectedElement?.id == child.id;

    return DragTarget<DeckElement>(
      onWillAcceptWithDetails: (details) => details.data.id != child.id,
      onAcceptWithDetails: (details) {
        _reorderOrMoveChild(parent, details.data, index);
      },
      builder: (context, candidateData, rejectedData) {
        final isTargetHovered = candidateData.isNotEmpty;

        Widget contentWidget = Container(
          decoration: BoxDecoration(
            border: isTargetHovered
                ? Border.all(color: const Color(0xFF3B82F6), width: 2)
                : (isChildSelected
                    ? Border.all(color: const Color(0xFF0052FF), width: 2)
                    : null),
          ),
          child: SizedBox(
            width: child.width,
            height: child.height,
            child: _buildInnerElement(child),
          ),
        );

        return Draggable<DeckElement>(
          data: child,
          feedback: Material(
            color: Colors.transparent,
            elevation: 8,
            child: Opacity(
              opacity: 0.9,
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(color: const Color(0xFF0052FF), width: 2),
                  borderRadius: BorderRadius.circular(6),
                  boxShadow: const [
                    BoxShadow(color: Color(0x33000000), blurRadius: 16, offset: Offset(0, 6)),
                  ],
                ),
                child: SizedBox(
                  width: child.width,
                  height: child.height,
                  child: _buildInnerElement(child),
                ),
              ),
            ),
          ),
          childWhenDragging: Opacity(
            opacity: 0.2,
            child: contentWidget,
          ),
          child: GestureDetector(
            onTap: () => widget.onElementSelected(child),
            onDoubleTap: () => _startEditing(child),
            behavior: HitTestBehavior.opaque,
            child: contentWidget,
          ),
        );
      },
    );
  }
}

class _FigmaLayoutGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    // 1. Figma 12-Column Grid (Electric Red/Pink Transparent Overlay)
    const columns = 12;
    const gutter = 20.0;
    const margin = 100.0;
    final totalWidth = size.width - (margin * 2);
    final colWidth = (totalWidth - (gutter * (columns - 1))) / columns;

    final colPaint = Paint()
      ..color = const Color(0xFFFF0055).withValues(alpha: 0.08)
      ..style = PaintingStyle.fill;

    for (int i = 0; i < columns; i++) {
      final left = margin + (i * (colWidth + gutter));
      canvas.drawRect(Rect.fromLTWH(left, 0, colWidth, size.height), colPaint);
    }

    // 2. Figma 8pt Baseline Grid Lines
    final linePaint = Paint()
      ..color = const Color(0xFFFF0055).withValues(alpha: 0.12)
      ..strokeWidth = 1.0;

    for (double y = 0; y < size.height; y += 40.0) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), linePaint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class _VectorIconElementPainter extends CustomPainter {
  final List rawStrokes;
  final Color strokeColor;
  final double strokeWidth;
  final bool isFilled;
  final Color fillColor;

  _VectorIconElementPainter({
    required this.rawStrokes,
    required this.strokeColor,
    required this.strokeWidth,
    required this.isFilled,
    required this.fillColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final scale = size.width / 24.0;
    final vectorPaint = Paint()
      ..color = strokeColor
      ..strokeWidth = strokeWidth * (scale / 16.0).clamp(1.0, 8.0)
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..style = isFilled ? PaintingStyle.fill : PaintingStyle.stroke;

    for (final stroke in rawStrokes) {
      if (stroke is! List || stroke.isEmpty) continue;
      final path = Path();
      final first = stroke.first as Map;
      path.moveTo((first['x'] as num).toDouble() * scale, (first['y'] as num).toDouble() * scale);
      for (int i = 1; i < stroke.length; i++) {
        final pt = stroke[i] as Map;
        path.lineTo((pt['x'] as num).toDouble() * scale, (pt['y'] as num).toDouble() * scale);
      }
      canvas.drawPath(path, vectorPaint);
    }
  }

  @override
  bool shouldRepaint(covariant _VectorIconElementPainter old) => true;
}

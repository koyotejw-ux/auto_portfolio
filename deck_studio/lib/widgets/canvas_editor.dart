import 'package:flutter/material.dart';
import '../models/deck_model.dart';

class CanvasEditor extends StatefulWidget {
  final DeckSlide slide;
  final DeckElement? selectedElement;
  final ValueChanged<DeckElement?> onElementSelected;
  final VoidCallback onSlideModified;

  const CanvasEditor({
    super.key,
    required this.slide,
    required this.selectedElement,
    required this.onElementSelected,
    required this.onSlideModified,
  });

  @override
  State<CanvasEditor> createState() => _CanvasEditorState();
}

class _CanvasEditorState extends State<CanvasEditor> {
  double _scale = 0.55;

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
                        // Slide Background Click to Deselect
                        Positioned.fill(
                          child: GestureDetector(
                            onTap: () => widget.onElementSelected(null),
                            behavior: HitTestBehavior.opaque,
                            child: const SizedBox.expand(),
                          ),
                        ),

                        // Interactive Elements
                        ...widget.slide.elements.map((elem) {
                          final isSelected = widget.selectedElement?.id == elem.id;
                          return Positioned(
                            left: elem.x,
                            top: elem.y,
                            width: elem.width,
                            height: elem.height,
                            child: GestureDetector(
                              onTap: () => widget.onElementSelected(elem),
                              onPanUpdate: (details) {
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
                                      : null,
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
                                            color: const Color(0xFF0052FF),
                                            borderRadius: BorderRadius.circular(4),
                                          ),
                                          child: Text(
                                            '${elem.name} (${elem.x.toInt()}, ${elem.y.toInt()}) [${elem.width.toInt()}×${elem.height.toInt()}]',
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontSize: 10,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          ),
                                        ),
                                      ),
                                    if (isSelected)
                                      Positioned(
                                        right: -8,
                                        bottom: -8,
                                        child: GestureDetector(
                                          onPanUpdate: (details) {
                                            setState(() {
                                              elem.width = (elem.width + details.delta.dx).clamp(50.0, 1920.0);
                                              elem.height = (elem.height + details.delta.dy).clamp(30.0, 1080.0);
                                            });
                                            widget.onSlideModified();
                                          },
                                          child: Container(
                                            width: 16,
                                            height: 16,
                                            decoration: BoxDecoration(
                                              color: const Color(0xFF0052FF),
                                              shape: BoxShape.circle,
                                              border: Border.all(color: Colors.white, width: 2),
                                            ),
                                          ),
                                        ),
                                      ),
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
      default:
        return Container(
          color: Colors.blue.withOpacity(0.05),
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
    final category = elem.props['category'];
    final titleBlack = elem.props['titleBlack'] ?? '';
    final titleBlue = elem.props['titleBlue'] ?? '';
    final subtitle = elem.props['subtitle'] ?? '';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (category != null) ...[
          Text(
            category,
            style: const TextStyle(
              color: Color(0xFF0052FF),
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
        ],
        RichText(
          text: TextSpan(
            children: [
              TextSpan(
                text: titleBlack,
                style: const TextStyle(
                  color: Color(0xFF0F172A),
                  fontSize: 32,
                  fontWeight: FontWeight.w900,
                  height: 1.2,
                ),
              ),
              TextSpan(
                text: titleBlue,
                style: const TextStyle(
                  color: Color(0xFF0052FF),
                  fontSize: 32,
                  fontWeight: FontWeight.w900,
                  height: 1.2,
                ),
              ),
            ],
          ),
        ),
        if (subtitle.isNotEmpty) ...[
          const SizedBox(height: 14),
          Text(
            subtitle,
            style: const TextStyle(
              color: Color(0xFF475569),
              fontSize: 13.5,
              height: 1.5,
            ),
          ),
        ],
      ],
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

    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFEFF6FF).withOpacity(0.5),
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
}


import 'package:flutter/material.dart';
import '../models/deck_model.dart';

class DeckElementRenderer extends StatelessWidget {
  final DeckElement element;
  final bool isSelected;
  final VoidCallback onSelect;

  const DeckElementRenderer({
    super.key,
    required this.element,
    required this.isSelected,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: element.x,
      top: element.y,
      width: element.width,
      height: element.height,
      child: GestureDetector(
        onTap: onSelect,
        behavior: HitTestBehavior.opaque,
        child: Container(
          decoration: BoxDecoration(
            border: isSelected
                ? Border.all(color: const Color(0xFF0052FF), width: 2)
                : null,
          ),
          child: Stack(
            clipBehavior: Clip.none,
            children: [
              _buildContent(context),
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
                      '${element.name} (${element.width.toInt()}×${element.height.toInt()})',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildContent(BuildContext context) {
    switch (element.type) {
      case ElementType.header:
        return _buildHeader();
      case ElementType.text:
        return _buildText();
      case ElementType.flowchart:
        return _buildFlowchart();
      case ElementType.kpiStrip:
        return _buildKpiStrip();
      case ElementType.mockupPlaceholder:
        return _buildMockupPlaceholder();
      case ElementType.designTokens:
        return _buildDesignTokens();
      case ElementType.donutChart:
        return _buildDonutChart();
      case ElementType.statCard:
        return _buildStatCard();
      default:
        return Container(
          color: Colors.grey.withOpacity(0.1),
          child: Center(
            child: Text(element.name),
          ),
        );
    }
  }

  Widget _buildHeader() {
    final badge = element.props['badge'] ?? '2026 CASE STUDY';
    final meta = element.props['meta'] ?? 'Header Meta';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          height: 1,
          color: const Color(0xFFE2E8F0),
        ),
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

  Widget _buildText() {
    final category = element.props['category'];
    final titleBlack = element.props['titleBlack'] ?? '';
    final titleBlue = element.props['titleBlue'] ?? '';
    final subtitle = element.props['subtitle'] ?? '';
    final plainTitle = (element.props['title'] ?? element.props['text']) as String?;

    final ts = element.textStyle;
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

  Widget _buildFlowchart() {
    final isKiosk = element.props['isKioskCarousel'] == true;
    if (isKiosk) {
      final stages = (element.props['stages'] as List? ?? []);
      return Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: stages.map<Widget>((st) {
          final sMap = Map<String, dynamic>.from(st);
          return Expanded(
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 10),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFFE2E8F0)),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.03),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
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
                    style: const TextStyle(
                      color: Color(0xFF64748B),
                      fontSize: 10,
                    ),
                  ),
                  const SizedBox(height: 12),
                  // Mockup Container Placeholder inside card
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFF0F172A),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.tablet_mac, color: Colors.white, size: 38),
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
                  const SizedBox(height: 12),
                  // Features list
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
                  const SizedBox(height: 8),
                  // Interaction banner
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

    // Default 4-step flowchart
    final items = (element.props['items'] as List? ?? []);
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

  Widget _buildMockupPlaceholder() {
    final title = element.props['screenTitle'] ?? 'Mockup Screen';
    final showMascot = element.props['showMascot'] == true;

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
            // Phone frame
            Container(
              width: 220,
              height: 420,
              decoration: BoxDecoration(
                color: const Color(0xFF0F172A),
                borderRadius: BorderRadius.circular(32),
                border: Border.all(color: const Color(0xFF475569), width: 4),
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFF0F172A).withOpacity(0.25),
                    blurRadius: 30,
                    offset: const Offset(15, 25),
                  ),
                ],
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
              // Mascot badge
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
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF0052FF).withOpacity(0.15),
                          blurRadius: 20,
                          offset: const Offset(0, 10),
                        ),
                      ],
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

  Widget _buildKpiStrip() {
    final header = element.props['header'];
    final items = (element.props['items'] as List? ?? []);

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

  Widget _buildDesignTokens() {
    final colors = (element.props['colors'] as List? ?? []);
    final typog = (element.props['typography'] as List? ?? []);

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

  Widget _buildDonutChart() {
    final title = element.props['title'] ?? 'Metrics';
    final percentage = (element.props['percentage'] as num? ?? 90).toDouble();

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
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildMetricPill(element.props['stat1'] ?? 'Metric 1'),
              _buildMetricPill(element.props['stat2'] ?? 'Metric 2'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMetricPill(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        text,
        style: const TextStyle(color: Color(0xFF334155), fontSize: 10, fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _buildStatCard() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Center(
        child: Text(element.name),
      ),
    );
  }
}


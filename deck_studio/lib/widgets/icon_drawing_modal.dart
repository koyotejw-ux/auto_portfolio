import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import '../models/deck_model.dart';

class VectorPathPoint {
  final double x; // 0.0 ~ 24.0 (Material 24dp coordinates)
  final double y;
  final bool isMoveTo;

  VectorPathPoint({required this.x, required this.y, this.isMoveTo = false});

  Map<String, dynamic> toJson() => {'x': x, 'y': y, 'isMoveTo': isMoveTo};

  factory VectorPathPoint.fromJson(Map<String, dynamic> json) => VectorPathPoint(
        x: (json['x'] as num).toDouble(),
        y: (json['y'] as num).toDouble(),
        isMoveTo: json['isMoveTo'] == true,
      );
}

class IconDrawingModal extends StatefulWidget {
  final ValueChanged<DeckElement> onSaveComponent;

  const IconDrawingModal({super.key, required this.onSaveComponent});

  @override
  State<IconDrawingModal> createState() => _IconDrawingModalState();
}

class _IconDrawingModalState extends State<IconDrawingModal> {
  String _iconName = 'Custom Material Icon';
  Color _strokeColor = const Color(0xFF0052FF);
  double _strokeWidth = 2.0;
  bool _snapToPixel = true;
  bool _showKeylines = true;
  bool _isFilled = false;
  Color _fillColor = Colors.transparent;

  final List<List<VectorPathPoint>> _strokes = [];
  List<VectorPathPoint>? _currentStroke;

  void _addPoint(Offset localPos, Size canvasSize, {bool isStart = false}) {
    // Canvas is square, normalize to 0.0 ~ 24.0 (Material Design 24dp)
    double normX = (localPos.dx / canvasSize.width) * 24.0;
    double normY = (localPos.dy / canvasSize.height) * 24.0;

    if (_snapToPixel) {
      normX = normX.roundToDouble().clamp(0.0, 24.0);
      normY = normY.roundToDouble().clamp(0.0, 24.0);
    } else {
      normX = normX.clamp(0.0, 24.0);
      normY = normY.clamp(0.0, 24.0);
    }

    setState(() {
      if (isStart) {
        _currentStroke = [VectorPathPoint(x: normX, y: normY, isMoveTo: true)];
        _strokes.add(_currentStroke!);
      } else {
        if (_currentStroke != null) {
          final last = _currentStroke!.last;
          if ((last.x - normX).abs() > 0.01 || (last.y - normY).abs() > 0.01) {
            _currentStroke!.add(VectorPathPoint(x: normX, y: normY));
          }
        }
      }
    });
  }

  void _createComponentAndInsert() {
    final rawStrokes = _strokes
        .map((stroke) => stroke.map((pt) => pt.toJson()).toList())
        .toList();

    final id = 'icon_${DateTime.now().millisecondsSinceEpoch}';
    final elem = DeckElement(
      id: id,
      type: ElementType.vectorIcon,
      name: _iconName.trim().isEmpty ? '벡터 아이콘' : _iconName.trim(),
      x: 300,
      y: 300,
      width: 64,
      height: 64,
      props: {
        'iconStrokes': rawStrokes,
        'strokeColor': _strokeColor.toARGB32(),
        'strokeWidth': _strokeWidth,
        'isFilled': _isFilled,
        'fillColor': _fillColor.toARGB32(),
      },
    );

    widget.onSaveComponent(elem);
    Navigator.pop(context);
  }

  // Pre-loaded Material Shapes
  void _loadPreset(String type) {
    setState(() {
      _strokes.clear();
      if (type == 'check') {
        _strokes.add([
          VectorPathPoint(x: 4.0, y: 12.0, isMoveTo: true),
          VectorPathPoint(x: 9.5, y: 17.5),
          VectorPathPoint(x: 20.0, y: 6.5),
        ]);
        _iconName = 'ic_check_24dp';
      } else if (type == 'bookmark') {
        _strokes.add([
          VectorPathPoint(x: 5.0, y: 3.0, isMoveTo: true),
          VectorPathPoint(x: 19.0, y: 3.0),
          VectorPathPoint(x: 19.0, y: 21.0),
          VectorPathPoint(x: 12.0, y: 17.5),
          VectorPathPoint(x: 5.0, y: 21.0),
          VectorPathPoint(x: 5.0, y: 3.0),
        ]);
        _iconName = 'ic_bookmark_24dp';
      } else if (type == 'arrow_forward') {
        _strokes.add([
          VectorPathPoint(x: 5.0, y: 12.0, isMoveTo: true),
          VectorPathPoint(x: 19.0, y: 12.0),
        ]);
        _strokes.add([
          VectorPathPoint(x: 12.0, y: 5.0, isMoveTo: true),
          VectorPathPoint(x: 19.0, y: 12.0),
          VectorPathPoint(x: 12.0, y: 19.0),
        ]);
        _iconName = 'ic_arrow_forward_24dp';
      } else if (type == 'plus') {
        _strokes.add([
          VectorPathPoint(x: 12.0, y: 5.0, isMoveTo: true),
          VectorPathPoint(x: 12.0, y: 19.0),
        ]);
        _strokes.add([
          VectorPathPoint(x: 5.0, y: 12.0, isMoveTo: true),
          VectorPathPoint(x: 19.0, y: 12.0),
        ]);
        _iconName = 'ic_add_24dp';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: const Color(0xFF1E1E1E),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: Color(0xFF333333)),
      ),
      child: Container(
        width: 820,
        height: 660,
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            // Header
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: const Color(0xFF2C2C2C),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.gesture, color: Color(0xFF38BDF8), size: 20),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '구글 매터리얼 가이드 벡터 아이콘 스튜디오 (Material 24dp Icon Studio)',
                        style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '구글 매터리얼 24dp 키라인 그리드(원/사각/사선/패딩 2dp) 기반 정밀 벡터 드로잉 및 컴포넌트화',
                        style: TextStyle(color: Colors.grey.shade400, fontSize: 11),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white70),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Main Editor & Settings
            Expanded(
              child: Row(
                children: [
                  // Left: 24dp Drawing Canvas Box
                  Expanded(
                    child: Center(
                      child: Container(
                        width: 440,
                        height: 440,
                        decoration: BoxDecoration(
                          color: const Color(0xFF141414),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: const Color(0xFF404040), width: 1.5),
                          boxShadow: const [
                            BoxShadow(color: Color(0x66000000), blurRadius: 20, offset: Offset(0, 8)),
                          ],
                        ),
                        child: LayoutBuilder(
                          builder: (context, constraints) {
                            final cSize = Size(constraints.maxWidth, constraints.maxHeight);
                            return GestureDetector(
                              onPanStart: (d) => _addPoint(d.localPosition, cSize, isStart: true),
                              onPanUpdate: (d) => _addPoint(d.localPosition, cSize),
                              onPanEnd: (_) => setState(() => _currentStroke = null),
                              child: CustomPaint(
                                size: cSize,
                                painter: _MaterialIconGridPainter(
                                  showKeylines: _showKeylines,
                                  strokes: _strokes,
                                  strokeColor: _strokeColor,
                                  strokeWidth: _strokeWidth,
                                  isFilled: _isFilled,
                                  fillColor: _fillColor,
                                ),
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                  ),

                  const SizedBox(width: 20),

                  // Right: Tooling Controls & Presets
                  SizedBox(
                    width: 280,
                    child: ListView(
                      children: [
                        // Icon Name
                        const Text('아이콘 컴포넌트 이름', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 6),
                        TextFormField(
                          initialValue: _iconName,
                          style: const TextStyle(color: Colors.white, fontSize: 12),
                          decoration: InputDecoration(
                            isDense: true,
                            filled: true,
                            fillColor: const Color(0xFF262626),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(6), borderSide: const BorderSide(color: Color(0xFF404040))),
                          ),
                          onChanged: (v) => _iconName = v,
                        ),
                        const SizedBox(height: 16),

                        // Stroke Color & Width
                        const Text('선 색상 & 굵기 (Stroke)', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            GestureDetector(
                              onTap: () {
                                showDialog(
                                  context: context,
                                  builder: (ctx) => AlertDialog(
                                    title: const Text('아이콘 컬러 선택'),
                                    content: SingleChildScrollView(
                                      child: ColorPicker(
                                        pickerColor: _strokeColor,
                                        onColorChanged: (c) => setState(() => _strokeColor = c),
                                      ),
                                    ),
                                    actions: [
                                      ElevatedButton(child: const Text('확인'), onPressed: () => Navigator.pop(ctx)),
                                    ],
                                  ),
                                );
                              },
                              child: Container(
                                width: 34,
                                height: 34,
                                decoration: BoxDecoration(
                                  color: _strokeColor,
                                  borderRadius: BorderRadius.circular(6),
                                  border: Border.all(color: Colors.white24),
                                ),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: DropdownButtonFormField<double>(
                                initialValue: _strokeWidth,
                                dropdownColor: const Color(0xFF262626),
                                style: const TextStyle(color: Colors.white, fontSize: 12),
                                decoration: InputDecoration(
                                  isDense: true,
                                  filled: true,
                                  fillColor: const Color(0xFF262626),
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
                                ),
                                items: const [
                                  DropdownMenuItem(value: 1.5, child: Text('1.5dp (Thin)')),
                                  DropdownMenuItem(value: 2.0, child: Text('2.0dp (Standard)')),
                                  DropdownMenuItem(value: 2.5, child: Text('2.5dp (Medium)')),
                                  DropdownMenuItem(value: 3.0, child: Text('3.0dp (Bold)')),
                                ],
                                onChanged: (v) {
                                  if (v != null) setState(() => _strokeWidth = v);
                                },
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),

                        // Grid Controls Switch
                        SwitchListTile(
                          contentPadding: EdgeInsets.zero,
                          title: const Text('Material 24dp 가이드라인 표시', style: TextStyle(color: Colors.white, fontSize: 12)),
                          value: _showKeylines,
                          activeThumbColor: const Color(0xFF0052FF),
                          onChanged: (v) => setState(() => _showKeylines = v),
                        ),
                        SwitchListTile(
                          contentPadding: EdgeInsets.zero,
                          title: const Text('1dp 픽셀 스냅 (Pixel Snapping)', style: TextStyle(color: Colors.white, fontSize: 12)),
                          value: _snapToPixel,
                          activeThumbColor: const Color(0xFF0052FF),
                          onChanged: (v) => setState(() => _snapToPixel = v),
                        ),
                        const SizedBox(height: 12),

                        // Action Buttons: Undo & Clear
                        Row(
                          children: [
                            Expanded(
                              child: OutlinedButton.icon(
                                icon: const Icon(Icons.undo, size: 14),
                                label: const Text('마지막 선 취소', style: TextStyle(fontSize: 11)),
                                style: OutlinedButton.styleFrom(foregroundColor: Colors.white70),
                                onPressed: _strokes.isEmpty
                                    ? null
                                    : () {
                                        setState(() => _strokes.removeLast());
                                      },
                              ),
                            ),
                            const SizedBox(width: 8),
                            OutlinedButton(
                              style: OutlinedButton.styleFrom(foregroundColor: Colors.redAccent),
                              onPressed: () => setState(() => _strokes.clear()),
                              child: const Text('전체 지우기', style: TextStyle(fontSize: 11)),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),

                        // Material Key Presets
                        const Text('구글 매터리얼 기본 프리셋 (Presets)', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 6,
                          runSpacing: 6,
                          children: [
                            ActionChip(
                              label: const Text('Check', style: TextStyle(fontSize: 11)),
                              backgroundColor: const Color(0xFF2C2C2C),
                              onPressed: () => _loadPreset('check'),
                            ),
                            ActionChip(
                              label: const Text('Bookmark', style: TextStyle(fontSize: 11)),
                              backgroundColor: const Color(0xFF2C2C2C),
                              onPressed: () => _loadPreset('bookmark'),
                            ),
                            ActionChip(
                              label: const Text('Arrow Forward', style: TextStyle(fontSize: 11)),
                              backgroundColor: const Color(0xFF2C2C2C),
                              onPressed: () => _loadPreset('arrow_forward'),
                            ),
                            ActionChip(
                              label: const Text('Plus Add', style: TextStyle(fontSize: 11)),
                              backgroundColor: const Color(0xFF2C2C2C),
                              onPressed: () => _loadPreset('plus'),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Bottom Actions: Cancel & Create Component
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('취소', style: TextStyle(color: Colors.white70)),
                ),
                const SizedBox(width: 12),
                ElevatedButton.icon(
                  icon: const Icon(Icons.check, size: 16),
                  label: const Text('컴포넌트화하여 캔버스에 배치', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0052FF),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  onPressed: _strokes.isEmpty ? null : _createComponentAndInsert,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _MaterialIconGridPainter extends CustomPainter {
  final bool showKeylines;
  final List<List<VectorPathPoint>> strokes;
  final Color strokeColor;
  final double strokeWidth;
  final bool isFilled;
  final Color fillColor;

  _MaterialIconGridPainter({
    required this.showKeylines,
    required this.strokes,
    required this.strokeColor,
    required this.strokeWidth,
    required this.isFilled,
    required this.fillColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final scale = size.width / 24.0;

    // 1. Google Material Icon 24dp Guidelines & Keylines
    if (showKeylines) {
      // Background 24x24 grid lines
      final gridPaint = Paint()
        ..color = const Color(0xFF262626)
        ..strokeWidth = 0.5;

      for (int i = 0; i <= 24; i++) {
        final pos = i * scale;
        canvas.drawLine(Offset(pos, 0), Offset(pos, size.height), gridPaint);
        canvas.drawLine(Offset(0, pos), Offset(size.width, pos), gridPaint);
      }

      final keylinePaint = Paint()
        ..color = const Color(0xFF0052FF).withValues(alpha: 0.3)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.0;

      // Material Outer Padding: 2dp padding boundary (20x20 live area)
      canvas.drawRect(Rect.fromLTWH(2 * scale, 2 * scale, 20 * scale, 20 * scale), keylinePaint);

      // Material Center Cross Lines (x=12, y=12)
      final centerPaint = Paint()
        ..color = const Color(0xFF38BDF8).withValues(alpha: 0.4)
        ..strokeWidth = 1.0;
      canvas.drawLine(Offset(12 * scale, 0), Offset(12 * scale, size.height), centerPaint);
      canvas.drawLine(Offset(0, 12 * scale), Offset(size.width, 12 * scale), centerPaint);

      // Keyline Circle: 20dp diameter circle
      canvas.drawCircle(Offset(12 * scale, 12 * scale), 10 * scale, keylinePaint);

      // Keyline Small Circle: 16dp diameter circle
      canvas.drawCircle(Offset(12 * scale, 12 * scale), 8 * scale, keylinePaint);

      // Keyline Horizontal Rectangle: 20 x 12 dp
      canvas.drawRect(Rect.fromLTWH(2 * scale, 6 * scale, 20 * scale, 12 * scale), keylinePaint);

      // Keyline Vertical Rectangle: 12 x 20 dp
      canvas.drawRect(Rect.fromLTWH(6 * scale, 2 * scale, 12 * scale, 20 * scale), keylinePaint);

      // Keyline Square: 16 x 16 dp
      canvas.drawRect(Rect.fromLTWH(4 * scale, 4 * scale, 16 * scale, 16 * scale), keylinePaint);

      // Diagonal 45-degree Guide
      final diagPaint = Paint()
        ..color = const Color(0xFFFF0055).withValues(alpha: 0.25)
        ..strokeWidth = 0.8;
      canvas.drawLine(Offset(2 * scale, 2 * scale), Offset(22 * scale, 22 * scale), diagPaint);
      canvas.drawLine(Offset(22 * scale, 2 * scale), Offset(2 * scale, 22 * scale), diagPaint);
    }

    // 2. Render Drawn Vector Strokes
    final vectorPaint = Paint()
      ..color = strokeColor
      ..strokeWidth = strokeWidth * (scale / 16.0)
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..style = isFilled ? PaintingStyle.fill : PaintingStyle.stroke;

    for (final stroke in strokes) {
      if (stroke.isEmpty) continue;
      final path = Path();
      path.moveTo(stroke.first.x * scale, stroke.first.y * scale);
      for (int i = 1; i < stroke.length; i++) {
        path.lineTo(stroke[i].x * scale, stroke[i].y * scale);
      }
      canvas.drawPath(path, vectorPaint);

      // Render control vertices
      final vertexPaint = Paint()
        ..color = Colors.white
        ..style = PaintingStyle.fill;
      for (final pt in stroke) {
        canvas.drawCircle(Offset(pt.x * scale, pt.y * scale), 2.5, vertexPaint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant _MaterialIconGridPainter old) => true;
}


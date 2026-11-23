import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/deck_model.dart';
import 'element_library_modal.dart';
import 'design_system_library_modal.dart';

enum FigmaToolMode {
  select, // V
  frame, // F
  rect, // R
  text, // T
  component, // Shift + I
  hand, // H
}

class FigmaToolbar extends StatelessWidget {
  final FigmaToolMode activeMode;
  final ValueChanged<FigmaToolMode> onModeChanged;
  final DeckElement? selectedElement;
  final VoidCallback onAddText;
  final VoidCallback onAddCard;
  final VoidCallback onAddFrame;
  final VoidCallback onOpenComponentLibrary;
  final VoidCallback onOpenDesignSystem;
  final VoidCallback onDuplicateSelected;
  final VoidCallback onCopySelected;
  final VoidCallback onPasteSelected;
  final bool canPaste;
  final VoidCallback onDeleteSelected;
  final VoidCallback onBringToFront;
  final VoidCallback onSendToBack;
  final VoidCallback onGroupSelected;
  final VoidCallback onUngroupSelected;
  final VoidCallback onToggleAutoLayout;
  final ValueChanged<String> onAlignSelected; // 'left', 'center_h', 'right', 'top', 'center_v', 'bottom'
  final VoidCallback onUndo;
  final VoidCallback onRedo;
  final bool canUndo;
  final bool canRedo;
  final double zoomScale;
  final VoidCallback onZoomIn;
  final VoidCallback onZoomOut;
  final VoidCallback onZoomFit;

  const FigmaToolbar({
    super.key,
    required this.activeMode,
    required this.onModeChanged,
    required this.selectedElement,
    required this.onAddText,
    required this.onAddCard,
    required this.onAddFrame,
    required this.onOpenComponentLibrary,
    required this.onOpenDesignSystem,
    required this.onDuplicateSelected,
    required this.onCopySelected,
    required this.onPasteSelected,
    required this.canPaste,
    required this.onDeleteSelected,
    required this.onBringToFront,
    required this.onSendToBack,
    required this.onGroupSelected,
    required this.onUngroupSelected,
    required this.onToggleAutoLayout,
    required this.onAlignSelected,
    required this.onUndo,
    required this.onRedo,
    required this.canUndo,
    required this.canRedo,
    required this.zoomScale,
    required this.onZoomIn,
    required this.onZoomOut,
    required this.onZoomFit,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 48,
      padding: const EdgeInsets.symmetric(horizontal: 12),
      decoration: const BoxDecoration(
        color: Color(0xFF1E293B), // Figma dark toolbar slate
        border: Border(bottom: BorderSide(color: Color(0xFF334155))),
        boxShadow: [
          BoxShadow(
            color: Color(0x33000000),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          // 1. Figma Logo / Menu Icon
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: const Color(0xFF0F172A),
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: const Color(0xFF334155)),
            ),
            child: const Icon(Icons.layers, color: Color(0xFF0052FF), size: 16),
          ),
          const SizedBox(width: 8),

          // 2. Undo / Redo
          _buildIconButton(
            icon: Icons.undo,
            tooltip: '실행 취소 (Ctrl+Z)',
            enabled: canUndo,
            onPressed: onUndo,
          ),
          _buildIconButton(
            icon: Icons.redo,
            tooltip: '다시 실행 (Ctrl+Y)',
            enabled: canRedo,
            onPressed: onRedo,
          ),

          _buildDivider(),

          // 3. Figma Core Tools (Select, Frame, Shape, Text, Component, Hand)
          _buildToolButton(
            mode: FigmaToolMode.select,
            icon: Icons.near_me_outlined,
            tooltip: '선택 및 이동 도구 (V)',
          ),
          _buildToolButton(
            mode: FigmaToolMode.frame,
            icon: Icons.crop_free,
            tooltip: '새 프레임/섹션 생성 (F)',
            onSpecialPress: onAddFrame,
          ),
          _buildToolButton(
            mode: FigmaToolMode.rect,
            icon: Icons.rectangle_outlined,
            tooltip: '카드 / 박스 추가 (R)',
            onSpecialPress: onAddCard,
          ),
          _buildToolButton(
            mode: FigmaToolMode.text,
            icon: Icons.text_fields,
            tooltip: '텍스트 추가 (T)',
            onSpecialPress: onAddText,
          ),
          _buildToolButton(
            mode: FigmaToolMode.component,
            icon: Icons.dashboard_customize_outlined,
            tooltip: '컴포넌트 삽입 라이브러리 (Shift+I)',
            onSpecialPress: onOpenComponentLibrary,
          ),
          _buildToolButton(
            mode: FigmaToolMode.hand,
            icon: Icons.pan_tool_outlined,
            tooltip: '캔버스 이동 핸드 툴 (H / Space)',
          ),

          _buildDivider(),

          // 4. Quick Actions for Selected Element (Copy/Paste Component, Duplicate, Delete, Layer Order)
          _buildIconButton(
            icon: Icons.copy,
            tooltip: '컴포넌트 복사 (Ctrl+C, 하위 요소 포함)',
            enabled: selectedElement != null,
            color: selectedElement != null ? const Color(0xFF38BDF8) : null,
            onPressed: onCopySelected,
          ),
          _buildIconButton(
            icon: Icons.paste,
            tooltip: '컴포넌트 붙여넣기 (Ctrl+V)',
            enabled: canPaste,
            color: canPaste ? const Color(0xFF0052FF) : null,
            onPressed: onPasteSelected,
          ),
          _buildIconButton(
            icon: Icons.control_point_duplicate,
            tooltip: '선택 요소 즉시 복제 (Ctrl+D)',
            enabled: selectedElement != null,
            onPressed: onDuplicateSelected,
          ),
          _buildIconButton(
            icon: Icons.flip_to_front,
            tooltip: '맨 앞으로 가져오기 (])',
            enabled: selectedElement != null,
            onPressed: onBringToFront,
          ),
          _buildIconButton(
            icon: Icons.flip_to_back,
            tooltip: '맨 뒤로 보내기 ([)',
            enabled: selectedElement != null,
            onPressed: onSendToBack,
          ),
          _buildIconButton(
            icon: Icons.folder_open,
            tooltip: '선택 요소 그룹화 (Ctrl+G)',
            enabled: selectedElement != null,
            color: selectedElement != null ? const Color(0xFFFBBF24) : null,
            onPressed: onGroupSelected,
          ),
          _buildIconButton(
            icon: Icons.auto_awesome_motion,
            tooltip: '오토레이아웃 토글 (Shift+A)',
            enabled: selectedElement != null,
            color: selectedElement != null && selectedElement!.autoLayoutDirection != AutoLayoutDirection.none
                ? const Color(0xFF0052FF)
                : (selectedElement != null ? const Color(0xFF38BDF8) : null),
            onPressed: onToggleAutoLayout,
          ),
          _buildIconButton(
            icon: Icons.call_split,
            tooltip: '그룹/리스트 분해 (Ctrl+Shift+G)',
            enabled: selectedElement != null &&
                (selectedElement!.props['items'] is List ||
                 selectedElement!.type == ElementType.group ||
                 selectedElement!.children.isNotEmpty),
            color: selectedElement != null ? const Color(0xFF38BDF8) : null,
            onPressed: onUngroupSelected,
          ),
          _buildIconButton(
            icon: Icons.delete_outline,
            tooltip: '삭제 (Delete)',
            enabled: selectedElement != null,
            color: selectedElement != null ? const Color(0xFFEF4444) : null,
            onPressed: onDeleteSelected,
          ),

          _buildDivider(),

          // 5. Figma Alignment Suite (When Element Selected)
          _buildIconButton(
            icon: Icons.align_horizontal_left,
            tooltip: '좌측 정렬',
            enabled: selectedElement != null,
            onPressed: () => onAlignSelected('left'),
          ),
          _buildIconButton(
            icon: Icons.align_horizontal_center,
            tooltip: '수평 중앙 정렬',
            enabled: selectedElement != null,
            onPressed: () => onAlignSelected('center_h'),
          ),
          _buildIconButton(
            icon: Icons.align_horizontal_right,
            tooltip: '우측 정렬',
            enabled: selectedElement != null,
            onPressed: () => onAlignSelected('right'),
          ),
          _buildIconButton(
            icon: Icons.align_vertical_top,
            tooltip: '상단 정렬',
            enabled: selectedElement != null,
            onPressed: () => onAlignSelected('top'),
          ),
          _buildIconButton(
            icon: Icons.align_vertical_center,
            tooltip: '수직 중앙 정렬',
            enabled: selectedElement != null,
            onPressed: () => onAlignSelected('center_v'),
          ),
          _buildIconButton(
            icon: Icons.align_vertical_bottom,
            tooltip: '하단 정렬',
            enabled: selectedElement != null,
            onPressed: () => onAlignSelected('bottom'),
          ),

          const Spacer(),

          // 6. Design System & Export Shortcuts
          ElevatedButton.icon(
            icon: const Icon(Icons.auto_awesome, size: 14, color: Color(0xFF38BDF8)),
            label: const Text('Design System', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0F172A),
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(6),
                side: const BorderSide(color: Color(0xFF334155)),
              ),
            ),
            onPressed: onOpenDesignSystem,
          ),

          const SizedBox(width: 10),
          _buildDivider(),

          // 7. Zoom & Canvas Controls (Zoom In/Out/Fit)
          IconButton(
            icon: const Icon(Icons.remove, size: 16, color: Color(0xFF94A3B8)),
            onPressed: onZoomOut,
            tooltip: '화면 축소',
            visualDensity: VisualDensity.compact,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: const Color(0xFF0F172A),
              borderRadius: BorderRadius.circular(4),
              border: Border.all(color: const Color(0xFF334155)),
            ),
            child: Text(
              '${(zoomScale * 100).toInt()}%',
              style: const TextStyle(color: Color(0xFFE2E8F0), fontSize: 11, fontWeight: FontWeight.bold),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.add, size: 16, color: Color(0xFF94A3B8)),
            onPressed: onZoomIn,
            tooltip: '화면 확대',
            visualDensity: VisualDensity.compact,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
          ),
          IconButton(
            icon: const Icon(Icons.fullscreen, size: 18, color: Color(0xFF94A3B8)),
            onPressed: onZoomFit,
            tooltip: '캔버스 크기 맞춤 (100% Fit)',
            visualDensity: VisualDensity.compact,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
          ),
        ],
      ),
    );
  }

  Widget _buildDivider() {
    return Container(
      width: 1,
      height: 20,
      margin: const EdgeInsets.symmetric(horizontal: 8),
      color: const Color(0xFF334155),
    );
  }

  Widget _buildToolButton({
    required FigmaToolMode mode,
    required IconData icon,
    required String tooltip,
    VoidCallback? onSpecialPress,
  }) {
    final isActive = activeMode == mode;
    return Tooltip(
      message: tooltip,
      child: InkWell(
        onTap: () {
          onModeChanged(mode);
          if (onSpecialPress != null) {
            onSpecialPress();
          }
        },
        borderRadius: BorderRadius.circular(6),
        child: Container(
          width: 32,
          height: 32,
          margin: const EdgeInsets.symmetric(horizontal: 2),
          decoration: BoxDecoration(
            color: isActive ? const Color(0xFF0052FF) : Colors.transparent,
            borderRadius: BorderRadius.circular(6),
          ),
          child: Icon(
            icon,
            size: 18,
            color: isActive ? Colors.white : const Color(0xFF94A3B8),
          ),
        ),
      ),
    );
  }

  Widget _buildIconButton({
    required IconData icon,
    required String tooltip,
    required bool enabled,
    required VoidCallback onPressed,
    Color? color,
  }) {
    return Tooltip(
      message: tooltip,
      child: InkWell(
        onTap: enabled ? onPressed : null,
        borderRadius: BorderRadius.circular(6),
        child: Container(
          width: 30,
          height: 30,
          margin: const EdgeInsets.symmetric(horizontal: 1),
          alignment: Alignment.center,
          child: Icon(
            icon,
            size: 17,
            color: enabled
                ? (color ?? const Color(0xFFCBD5E1))
                : const Color(0xFF475569),
          ),
        ),
      ),
    );
  }
}


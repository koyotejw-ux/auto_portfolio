import 'package:flutter/material.dart';
import '../models/deck_model.dart';

class ElementLibraryModal extends StatelessWidget {
  final ValueChanged<ElementType> onSelectType;

  const ElementLibraryModal({super.key, required this.onSelectType});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 680,
        height: 520,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '포트폴리오 섹션 & 모듈 라이브러리',
                      style: TextStyle(
                        color: Color(0xFF0F172A),
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      '원하는 도식, 차트, 플로우차트, 디자인 시스템, 목업 요소를 캔버스에 추가하세요.',
                      style: TextStyle(color: Color(0xFF64748B), fontSize: 12),
                    ),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 20),
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                childAspectRatio: 2.2,
                crossAxisSpacing: 14,
                mainAxisSpacing: 14,
                children: [
                  _buildCard(
                    context,
                    title: '헤더 인디케이터 (Header)',
                    desc: '케이스 스터디 뱃지 및 메타데이터 상단 바',
                    icon: Icons.title,
                    type: ElementType.header,
                    color: const Color(0xFF0052FF),
                  ),
                  _buildCard(
                    context,
                    title: '핵심 헤드라인 & 텍스트 (Text)',
                    desc: '2색 볼드 타이틀 및 UX 설명 카피',
                    icon: Icons.text_fields,
                    type: ElementType.text,
                    color: const Color(0xFF06B6D4),
                  ),
                  _buildCard(
                    context,
                    title: 'UX 플로우차트 / 프로세스 (Flowchart)',
                    desc: '단계별 다이어그램, 사용자 여정, 키오스크 캐러셀',
                    icon: Icons.account_tree_outlined,
                    type: ElementType.flowchart,
                    color: const Color(0xFF10B981),
                  ),
                  _buildCard(
                    context,
                    title: '디자인 시스템 토큰 (Design Tokens)',
                    desc: '컬러 팔레트 토큰 및 타이포그래피 스케일',
                    icon: Icons.palette_outlined,
                    type: ElementType.designTokens,
                    color: const Color(0xFF8B5CF6),
                  ),
                  _buildCard(
                    context,
                    title: '목업 & 3D 캐릭터 (Mockup Screen)',
                    desc: '스마트폰/태블릿 디바이스 프레임 및 마스코트',
                    icon: Icons.phone_android,
                    type: ElementType.mockupPlaceholder,
                    color: const Color(0xFFF59E0B),
                  ),
                  _buildCard(
                    context,
                    title: '도넛 차트 / 성과 지표 (Donut Chart)',
                    desc: '완성도 백분율 게이지 및 핵심 통계 칩',
                    icon: Icons.donut_large,
                    type: ElementType.donutChart,
                    color: const Color(0xFFEC4899),
                  ),
                  _buildCard(
                    context,
                    title: '규격 요약 스트립 (KPI Strip)',
                    desc: '하단 4열 성과 지표, 텔레메트리 데이터 바',
                    icon: Icons.view_column_outlined,
                    type: ElementType.kpiStrip,
                    color: const Color(0xFF0284C7),
                  ),
                  _buildCard(
                    context,
                    title: '통계 & 서머리 카드 (Stat Card)',
                    desc: '하이라이트 수치 및 아이콘 요약 박스',
                    icon: Icons.analytics_outlined,
                    type: ElementType.statCard,
                    color: const Color(0xFF6366F1),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCard(
    BuildContext context, {
    required String title,
    required String desc,
    required IconData icon,
    required ElementType type,
    required Color color,
  }) {
    return InkWell(
      onTap: () {
        Navigator.pop(context);
        onSelectType(type);
      },
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: const Color(0xFFE2E8F0)),
        ),
        child: Row(
          children: [
            Container(
              width: 44,
              height: 44,
              decoration: BoxDecoration(
                color: color.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: color, size: 22),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      color: Color(0xFF0F172A),
                      fontSize: 12.5,
                      fontWeight: FontWeight.bold,
                    ),
                    maxLines: 1,
                  ),
                  const SizedBox(height: 3),
                  Text(
                    desc,
                    style: const TextStyle(color: Color(0xFF64748B), fontSize: 10.5),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}


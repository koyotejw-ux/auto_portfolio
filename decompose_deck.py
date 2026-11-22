import re

def main():
    with open('deck_studio/lib/models/multagi_template.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Slide 1: s1_features -> s1_card_1..4, s1_kpi_strip -> s1_kpi_1..4
    s1_features_orig = """        DeckElement(
          id: 's1_features',
          type: ElementType.flowchart,
          name: '4대 핵심 강점',
          x: 100,
          y: 330,
          width: 820,
          height: 470,
          props: {
            'items': [
              {'num': '01', 'tag': '인지 부하 해소', 'title': '인지 부하 제로 설계 (Zero-Friction Voice Dock)', 'desc': '급변하는 매수 타이밍에서 복잡한 수치 입력을 제거하고, 음성과 탭 한 번으로 계산 완료'},
              {'num': '02', 'tag': '직관적 역산 UX', 'title': '직관적인 역산 인터랙션 (Goal-Seeking Interactive Flow)', 'desc': '목표 평단가를 지정하면 필요 매수 수량과 추가 필요 예수금을 즉시 역산출'},
              {'num': '03', 'tag': '행동경제학', 'title': '행동경제학적 안전 장치 (Safety Margin Alert UI)', 'desc': '손실 회피 편향으로 인한 뇌동매매를 방지하도록 비중 초과 경고와 분할 매수 가이드 제공'},
              {'num': '04', 'tag': '신뢰 & 안심', 'title': '금융 신뢰감과 안심 UX (Trust & Privacy Interface)', 'desc': '모든 자산 데이터를 외부 전송 없이 100% 로컬 온디바이스에서만 완결 처리'},
            ]
          },
        ),"""

    s1_features_new = """        DeckElement(
          id: 's1_card_1',
          type: ElementType.shape,
          name: '강점 01 · 인지 부하 해소',
          x: 100,
          y: 330,
          width: 820,
          height: 106,
          props: {
            'num': '01',
            'tag': '인지 부하 해소',
            'title': '인지 부하 제로 설계 (Zero-Friction Voice Dock)',
            'desc': '급변하는 매수 타이밍에서 복잡한 수치 입력을 제거하고, 음성과 탭 한 번으로 계산 완료',
          },
        ),
        DeckElement(
          id: 's1_card_2',
          type: ElementType.shape,
          name: '강점 02 · 직관적 역산 UX',
          x: 100,
          y: 450,
          width: 820,
          height: 106,
          props: {
            'num': '02',
            'tag': '직관적 역산 UX',
            'title': '직관적인 역산 인터랙션 (Goal-Seeking Interactive Flow)',
            'desc': '목표 평단가를 지정하면 필요 매수 수량과 추가 필요 예수금을 즉시 역산출',
          },
        ),
        DeckElement(
          id: 's1_card_3',
          type: ElementType.shape,
          name: '강점 03 · 행동경제학',
          x: 100,
          y: 570,
          width: 820,
          height: 106,
          props: {
            'num': '03',
            'tag': '행동경제학',
            'title': '행동경제학적 안전 장치 (Safety Margin Alert UI)',
            'desc': '손실 회피 편향으로 인한 뇌동매매를 방지하도록 비중 초과 경고와 분할 매수 가이드 제공',
          },
        ),
        DeckElement(
          id: 's1_card_4',
          type: ElementType.shape,
          name: '강점 04 · 신뢰 & 안심',
          x: 100,
          y: 690,
          width: 820,
          height: 106,
          props: {
            'num': '04',
            'tag': '신뢰 & 안심',
            'title': '금융 신뢰감과 안심 UX (Trust & Privacy Interface)',
            'desc': '모든 자산 데이터를 외부 전송 없이 100% 로컬 온디바이스에서만 완결 처리',
          },
        ),"""

    s1_kpi_orig = """        DeckElement(
          id: 's1_kpi_strip',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': 'PROJECT ROLE', 'val': '서비스 기획 100% · UI/UX 100%', 'sub': '사용자 리서치 · 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄'},
              {'title': 'PERIOD & TIMELINE', 'val': '2026.07 - 현재 (v2.0 라이브)', 'sub': '스토어 출시 후 실 사용자 피드백 반영 및 v2.0 지속 고도화'},
              {'title': 'DESIGN SYSTEM', 'val': 'FinTech Trust 토큰 & 규격', 'sub': '8pt 베이스라인 · 인디고/블루 신뢰 팔레트 · 라이트/다크 규격화'},
              {'title': 'DELIVERY & RELEASE', 'val': 'Google Play 상용 & 웹 프로토타입', 'sub': '실제 스토어 사용자 피드백 반영 · 60fps 인터랙티브 체험 구축'},
            ]
          },
        ),"""

    s1_kpi_new = """        DeckElement(
          id: 's1_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · PROJECT ROLE',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'PROJECT ROLE',
            'val': '서비스 기획 100% · UI/UX 100%',
            'sub': '사용자 리서치 · 문제 정의 · IA 정보 설계 · 와이어프레임 · UI 디자인 총괄',
          },
        ),
        DeckElement(
          id: 's1_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · PERIOD & TIMELINE',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'PERIOD & TIMELINE',
            'val': '2026.07 - 현재 (v2.0 라이브)',
            'sub': '스토어 출시 후 실 사용자 피드백 반영 및 v2.0 지속 고도화',
          },
        ),
        DeckElement(
          id: 's1_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · DESIGN SYSTEM',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'DESIGN SYSTEM',
            'val': 'FinTech Trust 토큰 & 규격',
            'sub': '8pt 베이스라인 · 인디고/블루 신뢰 팔레트 · 라이트/다크 규격화',
          },
        ),
        DeckElement(
          id: 's1_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · DELIVERY & RELEASE',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'DELIVERY & RELEASE',
            'val': 'Google Play 상용 & 웹 프로토타입',
            'sub': '실제 스토어 사용자 피드백 반영 · 60fps 인터랙티브 체험 구축',
          },
        ),"""

    # Check replacements
    if s1_features_orig in content:
        content = content.replace(s1_features_orig, s1_features_new)
        print("Replaced Slide 1 features!")
    else:
        print("ERROR: s1_features_orig not found!")

    if s1_kpi_orig in content:
        content = content.replace(s1_kpi_orig, s1_kpi_new)
        print("Replaced Slide 1 KPI!")
    else:
        print("ERROR: s1_kpi_orig not found!")

    # 2. Slide 2: s2_research_cards -> s2_card_1..3, s2_kpi -> s2_kpi_1..4
    s2_research_orig = """        DeckElement(
          id: 's2_research_cards',
          type: ElementType.flowchart,
          name: '3대 핵심 문제점 및 기회 영역',
          x: 100,
          y: 310,
          width: 820,
          height: 480,
          props: {
            'items': [
              {'num': '01', 'tag': '공포 기반 매수', 'title': '감정적 물타기로 인한 추가 손실 73.4%', 'desc': '충분한 계산과 근거 없이 손실 만회를 위해 무리하게 진입하여 비중 왜곡 심화'},
              {'num': '02', 'tag': 'Fat-Finger 오타', 'title': '변동성 장세 속 긴급 입력 실수', 'desc': '모바일 키패드로 긴 단가와 수량을 입력하다가 호가 창 놓침 및 오입력 빈발'},
              {'num': '03', 'tag': '목표 없는 물타기', 'title': '단순 평단 계산기의 한계', 'desc': '현재 주가에서 몇 주를 더 사야 탈출할 수 있는지에 대한 역산 솔루션의 부재'},
            ]
          },
        ),"""

    s2_research_new = """        DeckElement(
          id: 's2_card_1',
          type: ElementType.shape,
          name: '문제점 01 · 공포 기반 매수',
          x: 100,
          y: 310,
          width: 820,
          height: 140,
          props: {
            'num': '01',
            'tag': '공포 기반 매수',
            'title': '감정적 물타기로 인한 추가 손실 73.4%',
            'desc': '충분한 계산과 근거 없이 손실 만회를 위해 무리하게 진입하여 비중 왜곡 심화',
          },
        ),
        DeckElement(
          id: 's2_card_2',
          type: ElementType.shape,
          name: '문제점 02 · Fat-Finger 오타',
          x: 100,
          y: 470,
          width: 820,
          height: 140,
          props: {
            'num': '02',
            'tag': 'Fat-Finger 오타',
            'title': '변동성 장세 속 긴급 입력 실수',
            'desc': '모바일 키패드로 긴 단가와 수량을 입력하다가 호가 창 놓침 및 오입력 빈발',
          },
        ),
        DeckElement(
          id: 's2_card_3',
          type: ElementType.shape,
          name: '문제점 03 · 목표 없는 물타기',
          x: 100,
          y: 630,
          width: 820,
          height: 140,
          props: {
            'num': '03',
            'tag': '목표 없는 물타기',
            'title': '단순 평단 계산기의 한계',
            'desc': '현재 주가에서 몇 주를 더 사야 탈출할 수 있는지에 대한 역산 솔루션의 부재',
          },
        ),"""

    s2_kpi_orig = """        DeckElement(
          id: 's2_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '표본 크기', 'val': 'N = 428명', 'sub': '자본시장연구원 패널 조사'},
              {'title': '감정 매매율', 'val': '73.4%', 'sub': '손실 구간 무계획 물타기'},
              {'title': '해결 목표', 'val': '0.2s 음성 도크', 'sub': '인지 마찰 100% 해소'},
              {'title': '리스크 제어', 'val': '100% 온디바이스', 'sub': '금융 프라이버시 안심 보호'},
            ]
          },
        ),"""

    s2_kpi_new = """        DeckElement(
          id: 's2_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 표본 크기',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '표본 크기',
            'val': 'N = 428명',
            'sub': '자본시장연구원 패널 조사',
          },
        ),
        DeckElement(
          id: 's2_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 감정 매매율',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '감정 매매율',
            'val': '73.4%',
            'sub': '손실 구간 무계획 물타기',
          },
        ),
        DeckElement(
          id: 's2_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 해결 목표',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '해결 목표',
            'val': '0.2s 음성 도크',
            'sub': '인지 마찰 100% 해소',
          },
        ),
        DeckElement(
          id: 's2_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 리스크 제어',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '리스크 제어',
            'val': '100% 온디바이스',
            'sub': '금융 프라이버시 안심 보호',
          },
        ),"""

    if s2_research_orig in content:
        content = content.replace(s2_research_orig, s2_research_new)
        print("Replaced Slide 2 research cards!")
    else:
        print("ERROR: s2_research_orig not found!")

    if s2_kpi_orig in content:
        content = content.replace(s2_kpi_orig, s2_kpi_new)
        print("Replaced Slide 2 KPI!")
    else:
        print("ERROR: s2_kpi_orig not found!")

    # 3. Slide 3: s3_kpi -> s3_kpi_1..4
    s3_kpi_orig = """        DeckElement(
          id: 's3_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '메인 타깃', 'val': '스마트 리테일 투자자', 'sub': '25-45세 직장인 및 개인 투자자'},
              {'title': '핵심 니즈', 'val': '손익분기점 즉시 산출', 'sub': '목표가 도달 필요 수량/금액'},
              {'title': '경쟁 우위', 'val': '음성 AI 도크 & 역산', 'sub': '기존 단순 계산기 압도'},
              {'title': '사용성 완성도', 'val': '98.5% 태스크 성공률', 'sub': '시니어 UT 검증 완료'},
            ]
          },
        ),"""

    s3_kpi_new = """        DeckElement(
          id: 's3_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 메인 타깃',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '메인 타깃',
            'val': '스마트 리테일 투자자',
            'sub': '25-45세 직장인 및 개인 투자자',
          },
        ),
        DeckElement(
          id: 's3_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 핵심 니즈',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '핵심 니즈',
            'val': '손익분기점 즉시 산출',
            'sub': '목표가 도달 필요 수량/금액',
          },
        ),
        DeckElement(
          id: 's3_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 경쟁 우위',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '경쟁 우위',
            'val': '음성 AI 도크 & 역산',
            'sub': '기존 단순 계산기 압도',
          },
        ),
        DeckElement(
          id: 's3_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 사용성 완성도',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '사용성 완성도',
            'val': '98.5% 태스크 성공률',
            'sub': '시니어 UT 검증 완료',
          },
        ),"""

    if s3_kpi_orig in content:
        content = content.replace(s3_kpi_orig, s3_kpi_new)
        print("Replaced Slide 3 KPI!")
    else:
        print("ERROR: s3_kpi_orig not found!")

    # 4. Slide 4: s4_kpi -> s4_kpi_1..4
    s4_kpi_orig = """        DeckElement(
          id: 's4_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '트리 깊이', 'val': 'Depth 2 Level', 'sub': '최대 2단 탭으로 전 기능 도달'},
              {'title': '화면 이동 경로', 'val': '최소 1-Tap 직결', 'sub': '진입 장벽 제로 아키텍처'},
              {'title': '온디바이스 DB', 'val': 'SQLite & Hive 로컬', 'sub': '네트워크 단절 시에도 100% 작동'},
              {'title': '정보 구조 안전성', 'val': 'ISO/IEC 25010 준수', 'sub': '소프트웨어 품질 모델 적합'},
            ]
          },
        ),"""

    s4_kpi_new = """        DeckElement(
          id: 's4_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 트리 깊이',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '트리 깊이',
            'val': 'Depth 2 Level',
            'sub': '최대 2단 탭으로 전 기능 도달',
          },
        ),
        DeckElement(
          id: 's4_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 화면 이동 경로',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '화면 이동 경로',
            'val': '최소 1-Tap 직결',
            'sub': '진입 장벽 제로 아키텍처',
          },
        ),
        DeckElement(
          id: 's4_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 온디바이스 DB',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '온디바이스 DB',
            'val': 'SQLite & Hive 로컬',
            'sub': '네트워크 단절 시에도 100% 작동',
          },
        ),
        DeckElement(
          id: 's4_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 정보 구조 안전성',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '정보 구조 안전성',
            'val': 'ISO/IEC 25010 준수',
            'sub': '소프트웨어 품질 모델 적합',
          },
        ),"""

    if s4_kpi_orig in content:
        content = content.replace(s4_kpi_orig, s4_kpi_new)
        print("Replaced Slide 4 KPI!")
    else:
        print("ERROR: s4_kpi_orig not found!")

    # 5. Slide 5: s5_kpi -> s5_kpi_1..4
    s5_kpi_orig = """        DeckElement(
          id: 's5_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '평균 완료 시간', 'val': '12.4초 → 2.1초', 'sub': '83% 시간 단축 혁신'},
              {'title': '플로우 단계', 'val': '단 3-Step 완결', 'sub': '불필요한 중간 모달 제거'},
              {'title': '에러 복구율', 'val': '100% 인라인 가이드', 'sub': '오입력 즉시 수정 피드백'},
              {'title': '조작 자유도', 'val': '음성 · 키패드 동시 지원', 'sub': '멀티모달 유연성 극대화'},
            ]
          },
        ),"""

    s5_kpi_new = """        DeckElement(
          id: 's5_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 평균 완료 시간',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '평균 완료 시간',
            'val': '12.4초 → 2.1초',
            'sub': '83% 시간 단축 혁신',
          },
        ),
        DeckElement(
          id: 's5_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 플로우 단계',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '플로우 단계',
            'val': '단 3-Step 완결',
            'sub': '불필요한 중간 모달 제거',
          },
        ),
        DeckElement(
          id: 's5_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 에러 복구율',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '에러 복구율',
            'val': '100% 인라인 가이드',
            'sub': '오입력 즉시 수정 피드백',
          },
        ),
        DeckElement(
          id: 's5_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 조작 자유도',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '조작 자유도',
            'val': '음성 · 키패드 동시 지원',
            'sub': '멀티모달 유연성 극대화',
          },
        ),"""

    if s5_kpi_orig in content:
        content = content.replace(s5_kpi_orig, s5_kpi_new)
        print("Replaced Slide 5 KPI!")
    else:
        print("ERROR: s5_kpi_orig not found!")

    # 6. Slide 6: s6_kpi -> s6_kpi_1..4
    s6_kpi_orig = """        DeckElement(
          id: 's6_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '엄지 조작 영역', 'val': '하단 48% Safe Zone', 'sub': '한 손 파지 최적화'},
              {'title': '터치 타깃 규격', 'val': '최소 48x48 dp', 'sub': 'WCAG 2.1 AAA 준수'},
              {'title': '음성 도크 위치', 'val': 'Bottom Docked UI', 'sub': '엄지 원터치 마이크 진입'},
              {'title': '정보 위계', 'val': '3단계 시각적 계층', 'sub': '인지 피로도 최소화'},
            ]
          },
        ),"""

    s6_kpi_new = """        DeckElement(
          id: 's6_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 엄지 조작 영역',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '엄지 조작 영역',
            'val': '하단 48% Safe Zone',
            'sub': '한 손 파지 최적화',
          },
        ),
        DeckElement(
          id: 's6_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 터치 타깃 규격',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '터치 타깃 규격',
            'val': '최소 48x48 dp',
            'sub': 'WCAG 2.1 AAA 준수',
          },
        ),
        DeckElement(
          id: 's6_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 음성 도크 위치',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '음성 도크 위치',
            'val': 'Bottom Docked UI',
            'sub': '엄지 원터치 마이크 진입',
          },
        ),
        DeckElement(
          id: 's6_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 정보 위계',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '정보 위계',
            'val': '3단계 시각적 계층',
            'sub': '인지 피로도 최소화',
          },
        ),"""

    if s6_kpi_orig in content:
        content = content.replace(s6_kpi_orig, s6_kpi_new)
        print("Replaced Slide 6 KPI!")
    else:
        print("ERROR: s6_kpi_orig not found!")

    # 7. Slide 7: s7_kpi -> s7_kpi_1..4
    s7_kpi_orig = """        DeckElement(
          id: 's7_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': 'Primary Color', 'val': '#0052FF (Electric Blue)', 'sub': '신뢰와 명확성의 상징'},
              {'title': 'Secondary Color', 'val': '#06B6D4 (Cyan Mint)', 'sub': '성공 지표 및 상승 하이라이트'},
              {'title': '베이스라인 그리드', 'val': '8pt Spatial Grid', 'sub': '규칙적 시각 리듬 유지'},
              {'title': '컴포넌트 준수율', 'val': '100% Token Reusability', 'sub': 'Figma & Flutter 1:1 매핑'},
            ]
          },
        ),"""

    s7_kpi_new = """        DeckElement(
          id: 's7_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · Primary Color',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'Primary Color',
            'val': '#0052FF (Electric Blue)',
            'sub': '신뢰와 명확성의 상징',
          },
        ),
        DeckElement(
          id: 's7_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · Secondary Color',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'Secondary Color',
            'val': '#06B6D4 (Cyan Mint)',
            'sub': '성공 지표 및 상승 하이라이트',
          },
        ),
        DeckElement(
          id: 's7_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 베이스라인 그리드',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '베이스라인 그리드',
            'val': '8pt Spatial Grid',
            'sub': '규칙적 시각 리듬 유지',
          },
        ),
        DeckElement(
          id: 's7_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 컴포넌트 준수율',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '컴포넌트 준수율',
            'val': '100% Token Reusability',
            'sub': 'Figma & Flutter 1:1 매핑',
          },
        ),"""

    if s7_kpi_orig in content:
        content = content.replace(s7_kpi_orig, s7_kpi_new)
        print("Replaced Slide 7 KPI!")
    else:
        print("ERROR: s7_kpi_orig not found!")

    # 8. Slide 8: s8_comparison_list -> s8_comp_1..3, s8_kpi -> s8_kpi_1..4
    s8_comp_orig = """        DeckElement(
          id: 's8_comparison_list',
          type: ElementType.flowchart,
          name: '수동 입력 vs 음성 도크 패러다임 비교',
          x: 100,
          y: 330,
          width: 820,
          height: 470,
          props: {
            'items': [
              {'num': '01', 'tag': '입력 시간', 'title': '기존 수동 8.4초 → 음성 0.2초 완결', 'desc': '자연어 발화 즉시 NLU 온디바이스 분리 파싱'},
              {'num': '02', 'tag': '오타율 제로', 'title': 'Fat-finger 긴급 입력 실수 0%', 'desc': '하락장 급변 호가 속 숫자 오타 원천 방지'},
              {'num': '03', 'tag': '즉시 계산', 'title': '평단가 및 손익분기점 자동 채우기', 'desc': '입력 확인 터치 없이 화면 실시간 동기화'},
            ]
          },
        ),"""

    s8_comp_new = """        DeckElement(
          id: 's8_comp_1',
          type: ElementType.shape,
          name: '비교 01 · 입력 시간',
          x: 100,
          y: 330,
          width: 820,
          height: 140,
          props: {
            'num': '01',
            'tag': '입력 시간',
            'title': '기존 수동 8.4초 → 음성 0.2초 완결',
            'desc': '자연어 발화 즉시 NLU 온디바이스 분리 파싱',
          },
        ),
        DeckElement(
          id: 's8_comp_2',
          type: ElementType.shape,
          name: '비교 02 · 오타율 제로',
          x: 100,
          y: 490,
          width: 820,
          height: 140,
          props: {
            'num': '02',
            'tag': '오타율 제로',
            'title': 'Fat-finger 긴급 입력 실수 0%',
            'desc': '하락장 급변 호가 속 숫자 오타 원천 방지',
          },
        ),
        DeckElement(
          id: 's8_comp_3',
          type: ElementType.shape,
          name: '비교 03 · 즉시 계산',
          x: 100,
          y: 650,
          width: 820,
          height: 140,
          props: {
            'num': '03',
            'tag': '즉시 계산',
            'title': '평단가 및 손익분기점 자동 채우기',
            'desc': '입력 확인 터치 없이 화면 실시간 동기화',
          },
        ),"""

    s8_kpi_orig = """        DeckElement(
          id: 's8_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '처리 속도', 'val': '0.2초 온디바이스', 'sub': '지연 없는 실시간 파싱'},
              {'title': '오류 방지율', 'val': 'Fat-finger 100% 차단', 'sub': '급변 호가 완벽 대응'},
              {'title': '자연어 지원', 'val': '한국어 단가/수량 완벽 인식', 'sub': '음성 텍스트 동시 피드백'},
              {'title': '보안 규격', 'val': '외부 음성 전송 제로', 'sub': '로컬 NLU 안전 보관'},
            ]
          },
        ),"""

    s8_kpi_new = """        DeckElement(
          id: 's8_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 처리 속도',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '처리 속도',
            'val': '0.2초 온디바이스',
            'sub': '지연 없는 실시간 파싱',
          },
        ),
        DeckElement(
          id: 's8_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 오류 방지율',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '오류 방지율',
            'val': 'Fat-finger 100% 차단',
            'sub': '급변 호가 완벽 대응',
          },
        ),
        DeckElement(
          id: 's8_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 자연어 지원',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '자연어 지원',
            'val': '한국어 단가/수량 완벽 인식',
            'sub': '음성 텍스트 동시 피드백',
          },
        ),
        DeckElement(
          id: 's8_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 보안 규격',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '보안 규격',
            'val': '외부 음성 전송 제로',
            'sub': '로컬 NLU 안전 보관',
          },
        ),"""

    if s8_comp_orig in content:
        content = content.replace(s8_comp_orig, s8_comp_new)
        print("Replaced Slide 8 comparison list!")
    else:
        print("ERROR: s8_comp_orig not found!")

    if s8_kpi_orig in content:
        content = content.replace(s8_kpi_orig, s8_kpi_new)
        print("Replaced Slide 8 KPI!")
    else:
        print("ERROR: s8_kpi_orig not found!")

    # 9. Slide 9: s9_formula_card -> s9_formula_1..3, s9_kpi -> s9_kpi_1..4
    s9_form_orig = """        DeckElement(
          id: 's9_formula_card',
          type: ElementType.flowchart,
          name: '수학적 폐쇄형 역산 알고리즘 설명',
          x: 100,
          y: 330,
          width: 820,
          height: 470,
          props: {
            'items': [
              {'num': '01', 'tag': '수학적 공식', 'title': 'Q_add = Q_0 × (P_0 - P_target) / (P_target - P_add)', 'desc': '복잡한 반복문 없이 O(1) 시간 복잡도로 즉각 도출'},
              {'num': '02', 'tag': '안전 여유율', 'title': '자금 가용 한도 실시간 비교', 'desc': '보유 예수금 초과 시 비중 경고 및 분할 매수 수량 자동 제안'},
              {'num': '03', 'tag': '직관적 슬라이더', 'title': '인터랙티브 평단-필요자금 그래프 연동', 'desc': '슬라이더를 미세 조정하며 위험도 시뮬레이션'},
            ]
          },
        ),"""

    s9_form_new = """        DeckElement(
          id: 's9_form_1',
          type: ElementType.shape,
          name: '알고리즘 01 · 수학적 폐쇄형 공식',
          x: 100,
          y: 330,
          width: 820,
          height: 140,
          props: {
            'num': '01',
            'tag': '수학적 공식',
            'title': 'Q_add = Q_0 × (P_0 - P_target) / (P_target - P_add)',
            'desc': '복잡한 반복문 없이 O(1) 시간 복잡도로 즉각 도출',
          },
        ),
        DeckElement(
          id: 's9_form_2',
          type: ElementType.shape,
          name: '알고리즘 02 · 안전 여유율',
          x: 100,
          y: 490,
          width: 820,
          height: 140,
          props: {
            'num': '02',
            'tag': '안전 여유율',
            'title': '자금 가용 한도 실시간 비교',
            'desc': '보유 예수금 초과 시 비중 경고 및 분할 매수 수량 자동 제안',
          },
        ),
        DeckElement(
          id: 's9_form_3',
          type: ElementType.shape,
          name: '알고리즘 03 · 직관적 슬라이더',
          x: 100,
          y: 650,
          width: 820,
          height: 140,
          props: {
            'num': '03',
            'tag': '직관적 슬라이더',
            'title': '인터랙티브 평단-필요자금 그래프 연동',
            'desc': '슬라이더를 미세 조정하며 위험도 시뮬레이션',
          },
        ),"""

    s9_kpi_orig = """        DeckElement(
          id: 's9_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '알고리즘 복잡도', 'val': 'O(1) 폐쇄형 해', 'sub': '연산 지연 0ms'},
              {'title': '계산 정밀도', 'val': '소수점 6자리 무손실', 'sub': '부동소수점 오차 보정'},
              {'title': '안전 가드', 'val': '3단계 경고 시스템', 'sub': '비중 초과/리스크 알림'},
              {'title': '시각화 피드백', 'val': '실시간 역산 차트', 'sub': '직관적 슬라이더 UI'},
            ]
          },
        ),"""

    s9_kpi_new = """        DeckElement(
          id: 's9_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 알고리즘 복잡도',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '알고리즘 복잡도',
            'val': 'O(1) 폐쇄형 해',
            'sub': '연산 지연 0ms',
          },
        ),
        DeckElement(
          id: 's9_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 계산 정밀도',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '계산 정밀도',
            'val': '소수점 6자리 무손실',
            'sub': '부동소수점 오차 보정',
          },
        ),
        DeckElement(
          id: 's9_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 안전 가드',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '안전 가드',
            'val': '3단계 경고 시스템',
            'sub': '비중 초과/리스크 알림',
          },
        ),
        DeckElement(
          id: 's9_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 시각화 피드백',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '시각화 피드백',
            'val': '실시간 역산 차트',
            'sub': '직관적 슬라이더 UI',
          },
        ),"""

    if s9_form_orig in content:
        content = content.replace(s9_form_orig, s9_form_new)
        print("Replaced Slide 9 formula card!")
    else:
        print("ERROR: s9_form_orig not found!")

    if s9_kpi_orig in content:
        content = content.replace(s9_kpi_orig, s9_kpi_new)
        print("Replaced Slide 9 KPI!")
    else:
        print("ERROR: s9_kpi_orig not found!")

    # 10. Slide 10: s10_kpi -> s10_kpi_1..4
    s10_kpi_orig = """        DeckElement(
          id: 's10_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '화면 완성도', 'val': '6개 핵심 뷰 100%', 'sub': '전체 투자 플로우 커버리지'},
              {'title': '디자인 일관성', 'val': 'Material 3 규격', 'sub': '시스템 컬러·타이포 100% 매핑'},
              {'title': '에셋 규격화', 'val': 'SVG 벡터 아이콘', 'sub': '모든 해상도 무손실 렌더링'},
              {'title': '마이크로 인터랙션', 'val': '60 fps 햅틱 피드백', 'sub': '버튼·슬라이더 터치 감성'},
            ]
          },
        ),"""

    s10_kpi_new = """        DeckElement(
          id: 's10_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 화면 완성도',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '화면 완성도',
            'val': '6개 핵심 뷰 100%',
            'sub': '전체 투자 플로우 커버리지',
          },
        ),
        DeckElement(
          id: 's10_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 디자인 일관성',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '디자인 일관성',
            'val': 'Material 3 규격',
            'sub': '시스템 컬러·타이포 100% 매핑',
          },
        ),
        DeckElement(
          id: 's10_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 에셋 규격화',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '에셋 규격화',
            'val': 'SVG 벡터 아이콘',
            'sub': '모든 해상도 무손실 렌더링',
          },
        ),
        DeckElement(
          id: 's10_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 마이크로 인터랙션',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '마이크로 인터랙션',
            'val': '60 fps 햅틱 피드백',
            'sub': '버튼·슬라이더 터치 감성',
          },
        ),"""

    if s10_kpi_orig in content:
        content = content.replace(s10_kpi_orig, s10_kpi_new)
        print("Replaced Slide 10 KPI!")
    else:
        print("ERROR: s10_kpi_orig not found!")

    # 11. Slide 11: s11_kpi -> s11_kpi_1..4
    s11_kpi_orig = """        DeckElement(
          id: 's11_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '평균 입력 소요 시간', 'val': '8.4초 → 0.2초', 'sub': '97.6% 단축 혁신'},
              {'title': '추가 뇌동매매 손실률', 'val': '73.4% → 14.2%', 'sub': '59.2%p 리스크 방어'},
              {'title': '단기 리텐션 (D+7)', 'val': '28.5% → 64.2%', 'sub': '2.25배 참여 증대'},
              {'title': '스토어 사용자 평점', 'val': '4.92 / 5.00', 'sub': '금융 유틸리티 최상위권'},
            ]
          },
        ),"""

    s11_kpi_new = """        DeckElement(
          id: 's11_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 평균 입력 소요 시간',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '평균 입력 소요 시간',
            'val': '8.4초 → 0.2초',
            'sub': '97.6% 단축 혁신',
          },
        ),
        DeckElement(
          id: 's11_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 추가 뇌동매매 손실률',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '추가 뇌동매매 손실률',
            'val': '73.4% → 14.2%',
            'sub': '59.2%p 리스크 방어',
          },
        ),
        DeckElement(
          id: 's11_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 단기 리텐션 (D+7)',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '단기 리텐션 (D+7)',
            'val': '28.5% → 64.2%',
            'sub': '2.25배 참여 증대',
          },
        ),
        DeckElement(
          id: 's11_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 스토어 사용자 평점',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '스토어 사용자 평점',
            'val': '4.92 / 5.00',
            'sub': '금융 유틸리티 최상위권',
          },
        ),"""

    if s11_kpi_orig in content:
        content = content.replace(s11_kpi_orig, s11_kpi_new)
        print("Replaced Slide 11 KPI!")
    else:
        print("ERROR: s11_kpi_orig not found!")

    # 12. Slide 12: s12_kpi -> s12_kpi_1..4
    s12_kpi_orig = """        DeckElement(
          id: 's12_kpi',
          type: ElementType.kpiStrip,
          name: '하단 다크 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          boxStyle: DeckBoxStyle(
            backgroundColor: const Color(0xFF1E293B),
            borderColor: const Color(0xFF334155),
          ),
          props: {
            'items': [
              {'title': '플랫폼', 'val': 'Flutter 3.x Web', 'sub': 'CanvasKit 고성능 렌더러'},
              {'title': '반응 속도', 'val': '60 fps 무지연', 'sub': '네이티브급 터치 인터랙션'},
              {'title': '호환성', 'val': '크롬·사파리 완벽 대응', 'sub': '모바일 뷰포트 자동 최적화'},
              {'title': '실행 모드', 'val': 'Live On-Device Simulator', 'sub': '즉시 터치 조작 가능'},
            ]
          },
        ),"""

    s12_kpi_new = """        DeckElement(
          id: 's12_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 플랫폼',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          boxStyle: DeckBoxStyle(
            backgroundColor: const Color(0xFF1E293B),
            borderColor: const Color(0xFF334155),
          ),
          props: {
            'title': '플랫폼',
            'val': 'Flutter 3.x Web',
            'sub': 'CanvasKit 고성능 렌더러',
          },
        ),
        DeckElement(
          id: 's12_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 반응 속도',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          boxStyle: DeckBoxStyle(
            backgroundColor: const Color(0xFF1E293B),
            borderColor: const Color(0xFF334155),
          ),
          props: {
            'title': '반응 속도',
            'val': '60 fps 무지연',
            'sub': '네이티브급 터치 인터랙션',
          },
        ),
        DeckElement(
          id: 's12_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 호환성',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          boxStyle: DeckBoxStyle(
            backgroundColor: const Color(0xFF1E293B),
            borderColor: const Color(0xFF334155),
          ),
          props: {
            'title': '호환성',
            'val': '크롬·사파리 완벽 대응',
            'sub': '모바일 뷰포트 자동 최적화',
          },
        ),
        DeckElement(
          id: 's12_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 실행 모드',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          boxStyle: DeckBoxStyle(
            backgroundColor: const Color(0xFF1E293B),
            borderColor: const Color(0xFF334155),
          ),
          props: {
            'title': '실행 모드',
            'val': 'Live On-Device Simulator',
            'sub': '즉시 터치 조작 가능',
          },
        ),"""

    if s12_kpi_orig in content:
        content = content.replace(s12_kpi_orig, s12_kpi_new)
        print("Replaced Slide 12 KPI!")
    else:
        print("ERROR: s12_kpi_orig not found!")

    with open('deck_studio/lib/models/multagi_template.dart', 'w', encoding='utf-8') as f:
        f.write(content)

    print("SUCCESS: multagi_template.dart updated with individual decomposed items!")

if __name__ == '__main__':
    main()


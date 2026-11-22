import re

def main():
    with open('deck_studio/lib/models/multagi_template.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # s4_kpi
    s4_orig = """        DeckElement(
          id: 's4_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '1. 홈 대시보드', 'val': '보유 자산 실시간 현황', 'sub': '평균단가·수익률 직관 요약'},
              {'title': '2. 퀀트 계산기', 'val': '0.2s 음성 도크 결합', 'sub': '자연어 발화 즉시 연동'},
              {'title': '3. 목표가 역산', 'val': 'Closed-form 방정식', 'sub': '필요 자금 무지연 계산'},
              {'title': '4. 안심 금고', 'val': '100% 로컬 암호화', 'sub': '완전 무결 데이터 보관'},
            ]
          },
        ),"""

    s4_new = """        DeckElement(
          id: 's4_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 1. 홈 대시보드',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '1. 홈 대시보드',
            'val': '보유 자산 실시간 현황',
            'sub': '평균단가·수익률 직관 요약',
          },
        ),
        DeckElement(
          id: 's4_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 2. 퀀트 계산기',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '2. 퀀트 계산기',
            'val': '0.2s 음성 도크 결합',
            'sub': '자연어 발화 즉시 연동',
          },
        ),
        DeckElement(
          id: 's4_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 3. 목표가 역산',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '3. 목표가 역산',
            'val': 'Closed-form 방정식',
            'sub': '필요 자금 무지연 계산',
          },
        ),
        DeckElement(
          id: 's4_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 4. 안심 금고',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '4. 안심 금고',
            'val': '100% 로컬 암호화',
            'sub': '완전 무결 데이터 보관',
          },
        ),"""

    # s5_kpi
    s5_orig = """        DeckElement(
          id: 's5_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': 'Step 1: 진입', 'val': '홈 대시보드 온보딩', 'sub': '직관적 상태 인지'},
              {'title': 'Step 2: 입력', 'val': '음성 탭 or 수치 입력', 'sub': 'Fat-finger 방지 0.2s'},
              {'title': 'Step 3: 역산', 'val': '목표 평단가 산출', 'sub': '실시간 필요 예수금 도출'},
              {'title': 'Step 4: 저장', 'val': '로컬 포트폴리오 동기화', 'sub': '외부 유출 제로 안심 저장'},
            ]
          },
        ),"""

    s5_new = """        DeckElement(
          id: 's5_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · Step 1: 진입',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'Step 1: 진입',
            'val': '홈 대시보드 온보딩',
            'sub': '직관적 상태 인지',
          },
        ),
        DeckElement(
          id: 's5_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · Step 2: 입력',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'Step 2: 입력',
            'val': '음성 탭 or 수치 입력',
            'sub': 'Fat-finger 방지 0.2s',
          },
        ),
        DeckElement(
          id: 's5_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · Step 3: 역산',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'Step 3: 역산',
            'val': '목표 평단가 산출',
            'sub': '실시간 필요 예수금 도출',
          },
        ),
        DeckElement(
          id: 's5_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · Step 4: 저장',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': 'Step 4: 저장',
            'val': '로컬 포트폴리오 동기화',
            'sub': '외부 유출 제로 안심 저장',
          },
        ),"""

    # s10_kpi
    s10_orig = """        DeckElement(
          id: 's10_kpi',
          type: ElementType.kpiStrip,
          name: '하단 메트릭',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '1. 홈 대시보드', 'val': '라이브 포트폴리오', 'sub': '평단/손익 직관 진단'},
              {'title': '2. 0.2s 음성 도크', 'val': '온디바이스 NLU', 'sub': '무지연 파라미터 파싱'},
              {'title': '3. 목표가 역산기', 'val': 'Closed-form 엔진', 'sub': '필요 수량/자금 역산출'},
              {'title': '4. 텔레메트리 리포트', 'val': '투자 심리 가드', 'sub': '감정 뇌동매매 방어'},
            ]
          },
        ),"""

    s10_new = """        DeckElement(
          id: 's10_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 1. 홈 대시보드',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '1. 홈 대시보드',
            'val': '라이브 포트폴리오',
            'sub': '평단/손익 직관 진단',
          },
        ),
        DeckElement(
          id: 's10_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 2. 0.2s 음성 도크',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '2. 0.2s 음성 도크',
            'val': '온디바이스 NLU',
            'sub': '무지연 파라미터 파싱',
          },
        ),
        DeckElement(
          id: 's10_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 3. 목표가 역산기',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '3. 목표가 역산기',
            'val': 'Closed-form 엔진',
            'sub': '필요 수량/자금 역산출',
          },
        ),
        DeckElement(
          id: 's10_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 4. 텔레메트리 리포트',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '4. 텔레메트리 리포트',
            'val': '투자 심리 가드',
            'sub': '감정 뇌동매매 방어',
          },
        ),"""

    # s11_kpi
    s11_orig = """        DeckElement(
          id: 's11_kpi',
          type: ElementType.kpiStrip,
          name: '하단 규격 바',
          x: 100,
          y: 840,
          width: 1720,
          height: 120,
          props: {
            'items': [
              {'title': '패닉셀 방어율', 'val': '64.2% 방어 성공', 'sub': '손실 구간 충동 매도 억제'},
              {'title': '유동성 보존율', 'val': '65.0% 예수금 유지', 'sub': '올인 방지 분할 매수'},
              {'title': '태스크 완료율', 'val': '98.5% 도달', 'sub': '목표 평단가 계산 성공률'},
              {'title': '앱스토어 평점', 'val': '4.9 / 5.0 ★', 'sub': '상용 실사용자 만족도'},
            ]
          },
        ),"""

    s11_new = """        DeckElement(
          id: 's11_kpi_1',
          type: ElementType.statCard,
          name: '메트릭 1 · 패닉셀 방어율',
          x: 100,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '패닉셀 방어율',
            'val': '64.2% 방어 성공',
            'sub': '손실 구간 충동 매도 억제',
          },
        ),
        DeckElement(
          id: 's11_kpi_2',
          type: ElementType.statCard,
          name: '메트릭 2 · 유동성 보존율',
          x: 534,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '유동성 보존율',
            'val': '65.0% 예수금 유지',
            'sub': '올인 방지 분할 매수',
          },
        ),
        DeckElement(
          id: 's11_kpi_3',
          type: ElementType.statCard,
          name: '메트릭 3 · 태스크 완료율',
          x: 968,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '태스크 완료율',
            'val': '98.5% 도달',
            'sub': '목표 평단가 계산 성공률',
          },
        ),
        DeckElement(
          id: 's11_kpi_4',
          type: ElementType.statCard,
          name: '메트릭 4 · 앱스토어 평점',
          x: 1402,
          y: 840,
          width: 418,
          height: 120,
          props: {
            'title': '앱스토어 평점',
            'val': '4.9 / 5.0 ★',
            'sub': '상용 실사용자 만족도',
          },
        ),"""

    for name, orig, repl in [('s4', s4_orig, s4_new), ('s5', s5_orig, s5_new), ('s10', s10_orig, s10_new), ('s11', s11_orig, s11_new)]:
        if orig in content:
            content = content.replace(orig, repl)
            print(f"Replaced {name} successfully!")
        else:
            print(f"ERROR: {name} not found!")

    with open('deck_studio/lib/models/multagi_template.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done decompose part 2!")

if __name__ == '__main__':
    main()


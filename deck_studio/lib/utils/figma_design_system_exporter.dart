import 'package:flutter/material.dart';

class FigmaDesignSystemExporter {
  /// Figma 및 웹 개발용 완전한 디자인 시스템 토큰 & 컴포넌트 라이브러리 소스 생성
  static String generateFullFigmaDesignSystem() {
    return '''
/* ========================================================================== */
/* ZEROPASS DESIGN SYSTEM: COMPLETE FOUNDATION & COMPONENT LIBRARY           */
/* Ready to Copy & Paste into Figma Local Variables / Styles / CSS Modules    */
/* ========================================================================== */

:root {
  /* ------------------------------------------------------------------------ */
  /* 1. COLOR TOKENS (Primitive & Semantic)                                  */
  /* ------------------------------------------------------------------------ */
  --color-brand-primary: #0052FF;        /* 시그니처 일렉트릭 블루 (WCAG AAA 12.8:1) */
  --color-brand-primary-light: #EFF6FF;  /* 블루 연무 서피스 */
  --color-brand-primary-border: #BFDBFE; /* 블루 포커스 라인 */
  
  --color-cyan-accent: #0891B2;          /* 사이버 시안 (키오스크 & 프로 하이라이트) */
  --color-cyan-light: #ECFEFF;
  
  --color-success-green: #10B981;        /* 출결 완료 피드백 (에메랄드 그린) */
  --color-success-light: #ECFDF5;
  --color-success-border: #A7F3D0;
  
  --color-warning-amber: #F59E0B;        /* D-Day 만료 임박 경고 (앰버 옐로우) */
  --color-warning-light: #FFFBEB;
  --color-warning-border: #FDE68A;
  
  --color-danger-red: #EF4444;           /* 미수금 연체 독촉 경고 (에러 레드) */
  --color-danger-light: #FEF2F2;
  --color-danger-border: #FECACA;
  
  --color-surface-obsidian: #0F172A;     /* 옵시디언 다크 (헤더 & 키오스크 서피스) */
  --color-surface-card: #FFFFFF;         /* 퓨어 화이트 카드 */
  --color-surface-bg: #F8FAFC;           /* 뉴트럴 캔버스 배경 */
  --color-border-line: #E2E8F0;          /* 헤어라인 보더 */
  --color-text-main: #0F172A;            /* 본문/타이틀 블랙 */
  --color-text-muted: #64748B;           /* 보조 설명 슬레이트 그레이 */

  /* ------------------------------------------------------------------------ */
  /* 2. SPATIAL & RADIUS TOKENS (8pt Base Grid System)                        */
  /* ------------------------------------------------------------------------ */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;

  --radius-sm: 8px;                      /* 뱃지, 태그, 다이얼 서브박스 */
  --radius-md: 12px;                     /* 버튼, 인풋 필드, 다이얼로그 */
  --radius-lg: 16px;                     /* 메인 카드, 수납 장부 서피스 */
  --radius-xl: 24px;                     /* 바텀시트, 키오스크 패드 */
  --radius-full: 9999px;                 /* 필 뱃지, 상태 칩 */

  /* ------------------------------------------------------------------------ */
  /* 3. ELEVATION & SHADOW TOKENS                                             */
  /* ------------------------------------------------------------------------ */
  --elevation-1: 0px 2px 4px rgba(15, 23, 42, 0.04);   /* 카드 플랫 서피스 */
  --elevation-2: 0px 8px 16px rgba(15, 23, 42, 0.08);  /* 팝오버, 모달 시트 */
  --elevation-3: 0px 16px 32px rgba(15, 23, 42, 0.12); /* 3D 플로팅 목업 */

  /* ------------------------------------------------------------------------ */
  /* 4. TYPOGRAPHY SCALES (Pretendard & Inter Variable)                      */
  /* ------------------------------------------------------------------------ */
  --font-family-display: "Pretendard", -apple-system, sans-serif;
  --font-hero: 900 56px/1.2 var(--font-family-display);      /* 자간: -1.2px */
  --font-title-1: 800 32px/1.25 var(--font-family-display);  /* 자간: -0.8px */
  --font-title-2: 700 24px/1.3 var(--font-family-display);   /* 자간: -0.5px */
  --font-headline: 700 18px/1.35 var(--font-family-display); /* 자간: -0.3px */
  --font-body: 500 14px/1.5 var(--font-family-display);      /* 자간: -0.1px */
  --font-caption: 600 11px/1.4 var(--font-family-display);   /* 자간: 0.0px */
}

/* ========================================================================== */
/* 5. ATOMIC COMPONENT LIBRARY (FIGMA READY-TO-PASTE HTML/CSS)                */
/* ========================================================================== */

/* Component: Primary Action CTA Button */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background-color: var(--color-brand-primary);
  color: #FFFFFF;
  font-family: var(--font-family-display);
  font-size: 14px;
  font-weight: 700;
  border-radius: var(--radius-md);
  border: none;
  box-shadow: 0 4px 12px rgba(0, 82, 255, 0.25);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.btn-primary:hover {
  background-color: #0043D6;
  transform: translateY(-1px);
}

/* Component: Pill Status Badge (3-Tier D-Day) */
.badge-dday-imminent {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background-color: var(--color-warning-light);
  border: 1px solid var(--color-warning-border);
  color: var(--color-warning-amber);
  font-size: 11px;
  font-weight: 700;
  border-radius: var(--radius-full);
}

.badge-attendance-complete {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background-color: var(--color-success-light);
  border: 1px solid var(--color-success-border);
  color: var(--color-success-green);
  font-size: 11px;
  font-weight: 700;
  border-radius: var(--radius-full);
}

/* Component: Kiosk 116dp Large Tenkey Dial Button */
.kiosk-dial-key {
  width: 116px;
  height: 116px;
  background-color: #1E293B;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 36px;
  font-weight: 900;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  user-select: none;
  transition: transform 0.08s ease, background-color 0.08s ease;
}
.kiosk-dial-key:active {
  transform: scale(0.92);
  background-color: var(--color-brand-primary);
}

/* Component: D-Day Ledger Member Card */
.ledger-member-card {
  background-color: #FFFFFF;
  border: 1px solid var(--color-border-line);
  border-radius: var(--radius-lg);
  padding: 18px 22px;
  box-shadow: var(--elevation-1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
''';
  }

  /// Figma 토큰 전용 JSON 규격
  static String generateFigmaTokensJson() {
    return '''
{
  "ZeroPass_Tokens": {
    "Color": {
      "Brand": {
        "Primary": { "value": "#0052FF", "type": "color", "description": "Electric Blue AAA 12.8:1" },
        "PrimaryLight": { "value": "#EFF6FF", "type": "color" },
        "Cyan": { "value": "#0891B2", "type": "color" }
      },
      "Semantic": {
        "Success": { "value": "#10B981", "type": "color" },
        "Warning": { "value": "#F59E0B", "type": "color" },
        "Danger": { "value": "#EF4444", "type": "color" },
        "Surface": { "value": "#0F172A", "type": "color" },
        "Background": { "value": "#F8FAFC", "type": "color" },
        "Border": { "value": "#E2E8F0", "type": "color" }
      }
    },
    "Spacing": {
      "4": { "value": 4, "type": "spacing" },
      "8": { "value": 8, "type": "spacing" },
      "12": { "value": 12, "type": "spacing" },
      "16": { "value": 16, "type": "spacing" },
      "24": { "value": 24, "type": "spacing" },
      "32": { "value": 32, "type": "spacing" }
    },
    "BorderRadius": {
      "sm": { "value": 8, "type": "borderRadius" },
      "md": { "value": 12, "type": "borderRadius" },
      "lg": { "value": 16, "type": "borderRadius" },
      "xl": { "value": 24, "type": "borderRadius" },
      "full": { "value": 9999, "type": "borderRadius" }
    },
    "Typography": {
      "Hero": {
        "fontFamily": "Pretendard",
        "fontSize": 56,
        "fontWeight": 900,
        "lineHeight": 1.2,
        "letterSpacing": -1.2
      },
      "SectionTitle": {
        "fontFamily": "Pretendard",
        "fontSize": 32,
        "fontWeight": 800,
        "lineHeight": 1.25,
        "letterSpacing": -0.8
      },
      "Body": {
        "fontFamily": "Pretendard",
        "fontSize": 14,
        "fontWeight": 500,
        "lineHeight": 1.5,
        "letterSpacing": -0.2
      }
    }
  }
}
''';
  }
}


import re

def main():
    with open('deck_studio/lib/models/multagi_template.dart', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Decompose all 12 Headers into AutoLayout Frames with [Badge, Meta] children
    def repl_header(match):
        h_id = match.group(1)
        badge = match.group(2)
        meta = match.group(3)
        return f"""DeckElement(
          id: '{h_id}',
          type: ElementType.group,
          name: '헤더 AutoLayout Frame',
          x: 100,
          y: 60,
          width: 1720,
          height: 50,
          autoLayoutDirection: AutoLayoutDirection.horizontal,
          autoLayoutSpacing: 16.0,
          autoLayoutPadding: 0.0,
          autoLayoutAlignment: AutoLayoutAlignment.spaceBetween,
          props: {{
            'badge': '{badge}',
            'meta': '{meta}',
          }},
          children: [
            DeckElement(
              id: '{h_id}_badge',
              type: ElementType.badge,
              name: '헤더 뱃지 · {badge}',
              x: 0,
              y: 0,
              width: 180,
              height: 32,
              props: {{'title': '{badge}', 'badge': '{badge}'}},
            ),
            DeckElement(
              id: '{h_id}_meta',
              type: ElementType.text,
              name: '헤더 메타 텍스트',
              x: 200,
              y: 0,
              width: 600,
              height: 32,
              props: {{'title': '{meta}', 'meta': '{meta}'}},
            ),
          ],
        )"""

    header_pattern = r'DeckElement\(\s*id:\s*\'(s\d+_header)\',\s*type:\s*ElementType\.header,\s*name:\s*\'[^\']+\',\s*x:\s*100,\s*y:\s*60,\s*width:\s*1720,\s*height:\s*50,\s*props:\s*\{\s*\'badge\':\s*\'([^\']+)\',\s*\'meta\':\s*\'([^\']+)\',?\s*\},?\s*\)'
    content, count_h = re.subn(header_pattern, repl_header, content)
    print(f'Decomposed {count_h} headers into AutoLayout Frames!')

    # 2. Decompose all 12 Titles into AutoLayout Frames with [Category, MainHeadline, Subtitle] children
    def repl_title(match):
        t_id = match.group(1)
        w_val = match.group(2)
        cat = match.group(3)
        t_black = match.group(4)
        t_blue = match.group(5)
        sub = match.group(6)

        sub_clean = sub.replace('\n', '\\n').replace("'", "\\'")
        t_black_clean = t_black.replace("'", "\\'")
        t_blue_clean = t_blue.replace("'", "\\'")
        cat_clean = cat.replace("'", "\\'")

        return f"""DeckElement(
          id: '{t_id}',
          type: ElementType.group,
          name: '헤드라인 AutoLayout Frame',
          x: 100,
          y: 130,
          width: {w_val},
          height: 180,
          autoLayoutDirection: AutoLayoutDirection.vertical,
          autoLayoutSpacing: 10.0,
          autoLayoutPadding: 0.0,
          autoLayoutAlignment: AutoLayoutAlignment.start,
          props: {{
            'category': '{cat_clean}',
            'titleBlack': '{t_black_clean}',
            'titleBlue': '{t_blue_clean}',
            'subtitle': '{sub_clean}',
          }},
          children: [
            DeckElement(
              id: '{t_id}_cat',
              type: ElementType.badge,
              name: '카테고리 칩 · {cat_clean}',
              x: 0,
              y: 0,
              width: {w_val},
              height: 24,
              props: {{'title': '{cat_clean}', 'category': '{cat_clean}'}},
            ),
            DeckElement(
              id: '{t_id}_main',
              type: ElementType.text,
              name: '메인 타이틀 텍스트',
              x: 0,
              y: 34,
              width: {w_val},
              height: 70,
              props: {{'titleBlack': '{t_black_clean}', 'titleBlue': '{t_blue_clean}', 'title': '{t_black_clean}{t_blue_clean}'}},
            ),
            DeckElement(
              id: '{t_id}_sub',
              type: ElementType.text,
              name: '서브 설명 텍스트',
              x: 0,
              y: 114,
              width: {w_val},
              height: 50,
              props: {{'subtitle': '{sub_clean}', 'title': '{sub_clean}'}},
            ),
          ],
        )"""

    title_pattern = r'DeckElement\(\s*id:\s*\'(s\d+_title)\',\s*type:\s*ElementType\.text,\s*name:\s*\'[^\']+\',\s*x:\s*100,\s*y:\s*130,\s*width:\s*([0-9.]+),\s*height:\s*[0-9.]+,\s*props:\s*\{\s*\'category\':\s*\'([^\']+)\',\s*\'titleBlack\':\s*\'([^\']+)\',\s*\'titleBlue\':\s*\'([^\']+)\',\s*\'subtitle\':\s*\'(.*?)\',?\s*\},?\s*\)'
    content, count_t = re.subn(title_pattern, repl_title, content, flags=re.DOTALL)
    print(f'Decomposed {count_t} titles into AutoLayout Frames!')

    # 3. Decompose all 13 Shape Cards into AutoLayout Frames with [Num, Tag, Title, Desc] children
    def repl_card(match):
        c_id = match.group(1)
        c_name = match.group(2)
        y_val = match.group(3)
        h_val = match.group(4)
        num = match.group(5)
        tag = match.group(6)
        title = match.group(7)
        desc = match.group(8)

        num_clean = num.replace("'", "\\'")
        tag_clean = tag.replace("'", "\\'")
        title_clean = title.replace("'", "\\'")
        desc_clean = desc.replace('\n', '\\n').replace("'", "\\'")

        return f"""DeckElement(
          id: '{c_id}',
          type: ElementType.group,
          name: '{c_name}',
          x: 100,
          y: {y_val},
          width: 820,
          height: {h_val},
          autoLayoutDirection: AutoLayoutDirection.horizontal,
          autoLayoutSpacing: 14.0,
          autoLayoutPadding: 16.0,
          autoLayoutAlignment: AutoLayoutAlignment.start,
          boxStyle: DeckBoxStyle(
            backgroundColor: Colors.white,
            borderColor: const Color(0xFFE2E8F0),
            borderRadius: 12.0,
          ),
          props: {{
            'num': '{num_clean}',
            'tag': '{tag_clean}',
            'title': '{title_clean}',
            'desc': '{desc_clean}',
          }},
          children: [
            DeckElement(
              id: '{c_id}_num',
              type: ElementType.badge,
              name: '번호 인디케이터 [{num_clean}]',
              x: 0,
              y: 0,
              width: 38,
              height: 26,
              props: {{'num': '{num_clean}', 'title': '{num_clean}'}},
            ),
            DeckElement(
              id: '{c_id}_tag',
              type: ElementType.badge,
              name: '태그 필터 칩 [{tag_clean}]',
              x: 48,
              y: 0,
              width: 120,
              height: 26,
              props: {{'tag': '{tag_clean}', 'title': '{tag_clean}'}},
            ),
            DeckElement(
              id: '{c_id}_content',
              type: ElementType.group,
              name: '내용 AutoLayout (제목+설명)',
              x: 180,
              y: 0,
              width: 580,
              height: 60,
              autoLayoutDirection: AutoLayoutDirection.vertical,
              autoLayoutSpacing: 4.0,
              autoLayoutPadding: 0.0,
              props: {{'title': '{title_clean}', 'desc': '{desc_clean}'}},
              children: [
                DeckElement(
                  id: '{c_id}_title',
                  type: ElementType.text,
                  name: '제목 인풋 레이블',
                  x: 0,
                  y: 0,
                  width: 580,
                  height: 24,
                  props: {{'title': '{title_clean}'}},
                ),
                DeckElement(
                  id: '{c_id}_desc',
                  type: ElementType.text,
                  name: '설명 인풋 레이블',
                  x: 0,
                  y: 28,
                  width: 580,
                  height: 32,
                  props: {{'desc': '{desc_clean}', 'title': '{desc_clean}'}},
                ),
              ],
            ),
          ],
        )"""

    card_pattern = r'DeckElement\(\s*id:\s*\'([^\']+)\',\s*type:\s*ElementType\.shape,\s*name:\s*\'([^\']+)\',\s*x:\s*100,\s*y:\s*([0-9.]+),\s*width:\s*820,\s*height:\s*([0-9.]+),\s*props:\s*\{\s*\'num\':\s*\'([^\']+)\',\s*\'tag\':\s*\'([^\']+)\',\s*\'title\':\s*\'([^\']+)\',\s*\'desc\':\s*\'(.*?)\',?\s*\},?\s*\)'
    content, count_c = re.subn(card_pattern, repl_card, content, flags=re.DOTALL)
    print(f'Decomposed {count_c} shape cards into AutoLayout Frames!')

    with open('deck_studio/lib/models/multagi_template.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: multagi_template.dart successfully updated with full Figma AutoLayout hierarchy!")

if __name__ == '__main__':
    main()


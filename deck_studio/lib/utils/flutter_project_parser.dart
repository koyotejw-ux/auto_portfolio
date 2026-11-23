import 'dart:io';
import 'package:flutter/material.dart';
import '../models/deck_model.dart';

/// Represents a parsed Flutter Screen/Widget file from a project
class ParsedFlutterScreen {
  final String filePath;
  final String fileName;
  final String screenName;
  final List<DeckElement> elements;
  final Color backgroundColor;

  ParsedFlutterScreen({
    required this.filePath,
    required this.fileName,
    required this.screenName,
    required this.elements,
    this.backgroundColor = const Color(0xFFFFFFFF),
  });

  /// Convert parsed Flutter screen into a visual DeckSlide for DeckStudio canvas
  DeckSlide toDeckSlide(int pageNumber) {
    return DeckSlide(
      id: 'flutter_screen_${DateTime.now().millisecondsSinceEpoch}_$pageNumber',
      title: screenName,
      pageNumber: pageNumber,
      backgroundColor: backgroundColor,
      elements: elements,
    );
  }
}

/// Robust Parser for reading real Flutter Widget source files and extracting UI elements
class FlutterProjectParser {
  /// Scan a Flutter project directory for screen & widget Dart files
  static Future<List<File>> findScreenFiles(String projectRoot) async {
    final dir = Directory(projectRoot);
    if (!await dir.exists()) return [];

    final libDir = Directory('$projectRoot/lib');
    final targetDir = await libDir.exists() ? libDir : dir;

    final files = <File>[];
    await for (final entity in targetDir.list(recursive: true, followLinks: false)) {
      if (entity is File && entity.path.endsWith('.dart')) {
        // Exclude generated files or pure tests
        final p = entity.path.replaceAll(r'\', '/');
        if (p.contains('.g.dart') || p.contains('.freezed.dart') || p.contains('/test/')) {
          continue;
        }
        files.add(entity);
      }
    }
    return files;
  }

  /// Parse a Flutter Dart file into visual DeckElements arranged in standard mobile frame (390x844 or canvas)
  static ParsedFlutterScreen parseDartFile(File file) {
    final content = file.readAsStringSync();
    final fileName = file.uri.pathSegments.last;
    String screenName = fileName.replaceAll('.dart', '');
    
    // Extract class name if available (e.g. class HomeScreen extends ...)
    final classMatch = RegExp(r'class\s+([A-Za-z0-9_]+)\s+extends\s+(StatefulWidget|StatelessWidget|ConsumerWidget|ConsumerStatefulWidget)').firstMatch(content);
    if (classMatch != null) {
      screenName = classMatch.group(1)!;
    }

    final elements = <DeckElement>[];
    double curY = 60.0;
    const double frameX = 140.0;
    const double frameWidth = 390.0;
    const double contentWidth = 350.0;
    Color screenBg = const Color(0xFFFFFFFF);

    // Detect dark or custom Scaffold background
    if (content.contains('Colors.black') || content.contains('0xFF0F172A') || content.contains('0xFF1E1E1E') || content.contains('0xFF121212')) {
      screenBg = const Color(0xFF0F172A);
    } else if (content.contains('Color(0xFFF8FAFC)') || content.contains('Color(0xFFF1F5F9)')) {
      screenBg = const Color(0xFFF8FAFC);
    }

    // 1. Mobile Phone Frame Container (Main Mockup Canvas Frame)
    elements.add(
      DeckElement(
        id: 'frame_${DateTime.now().microsecondsSinceEpoch}',
        type: ElementType.shape,
        name: '$screenName Frame (390×844)',
        x: frameX,
        y: 40,
        width: frameWidth,
        height: 844,
        boxStyle: DeckBoxStyle(
          backgroundColor: screenBg,
          borderColor: const Color(0xFFCBD5E1),
          borderWidth: 2.0,
          borderRadius: 44.0,
          padding: 20.0,
          hasShadow: true,
        ),
        props: {'isPhoneFrame': true},
        isComponent: true,
      ),
    );

    // 2. Status Bar Mockup (Top)
    elements.add(
      DeckElement(
        id: 'status_bar_${DateTime.now().microsecondsSinceEpoch}',
        type: ElementType.text,
        name: 'Status Bar (9:41)',
        x: frameX + 24,
        y: 56,
        width: contentWidth,
        height: 24,
        textStyle: DeckTextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: screenBg == const Color(0xFF0F172A) ? Colors.white70 : const Color(0xFF0F172A),
        ),
        props: {
          'title': '9:41',
          'subtitle': '5G 100%',
        },
      ),
    );
    curY = 96.0;

    // 3. Extract AppBar if present
    final appBarTitleRegex = RegExp(r"AppBar\s*\([^)]*title:\s*(?:const\s*)?Text\(\s*[']([^'\n\r]+)[']");
    final appBarMatch = appBarTitleRegex.firstMatch(content);
    if (appBarMatch != null || content.contains('AppBar(')) {
      final titleText = appBarMatch != null ? appBarMatch.group(1)! : screenName;
      elements.add(
        DeckElement(
          id: 'appbar_${DateTime.now().microsecondsSinceEpoch}',
          type: ElementType.header,
          name: 'App Bar [$titleText]',
          x: frameX + 20,
          y: curY,
          width: contentWidth,
          height: 48,
          textStyle: DeckTextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: screenBg == const Color(0xFF0F172A) ? Colors.white : const Color(0xFF0F172A),
          ),
          props: {
            'badge': 'APP BAR',
            'meta': titleText,
          },
        ),
      );
      curY += 56.0;
    }

    // 4. Extract Text(...) widgets
    final textWidgetRegex = RegExp(r"Text\(\s*[']([^'\n\r]{2,80})[']");
    final textMatches = textWidgetRegex.allMatches(content).toList();
    final seenTexts = <String>{};

    for (final tm in textMatches) {
      final t = tm.group(1)!.trim();
      if (t.isEmpty || seenTexts.contains(t) || t == screenName) continue;
      seenTexts.add(t);
      if (seenTexts.length > 8) break; // Limit to key visual elements

      final isLargeTitle = t.length < 24 && (content.contains('fontSize: 2') || content.contains('w800') || content.contains('bold'));
      final double h = isLargeTitle ? 36.0 : 28.0;

      elements.add(
        DeckElement(
          id: 'text_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
          type: ElementType.text,
          name: '텍스트: $t',
          x: frameX + 24,
          y: curY,
          width: contentWidth,
          height: h,
          textStyle: DeckTextStyle(
            fontSize: isLargeTitle ? 20 : 14,
            fontWeight: isLargeTitle ? FontWeight.w800 : FontWeight.w500,
            color: screenBg == const Color(0xFF0F172A) ? Colors.white : const Color(0xFF0F172A),
          ),
          props: {'title': t},
        ),
      );
      curY += h + 10.0;
      if (curY > 740) break;
    }

    // 5. Extract Buttons (ElevatedButton, OutlinedButton, TextButton)
    final buttonRegex = RegExp(r"(ElevatedButton|OutlinedButton|TextButton|FilledButton)(?:\.icon)?\s*\([^)]*child:\s*(?:const\s*)?Text\(\s*[']([^'\n\r]+)[']");
    for (final bm in buttonRegex.allMatches(content)) {
      final btnType = bm.group(1)!;
      final btnLabel = bm.group(2)!.trim();
      if (curY > 720) break;

      elements.add(
        DeckElement(
          id: 'btn_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
          type: ElementType.shape,
          name: '버튼: $btnLabel ($btnType)',
          x: frameX + 24,
          y: curY,
          width: contentWidth,
          height: 48,
          boxStyle: DeckBoxStyle(
            backgroundColor: btnType.contains('Outlined') || btnType.contains('Text')
                ? Colors.transparent
                : const Color(0xFF0052FF),
            borderColor: const Color(0xFF0052FF),
            borderWidth: btnType.contains('Outlined') ? 1.5 : 0,
            borderRadius: 12.0,
            padding: 12.0,
          ),
          textStyle: DeckTextStyle(
            color: btnType.contains('Outlined') || btnType.contains('Text')
                ? const Color(0xFF0052FF)
                : Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 14,
          ),
          props: {'title': btnLabel, 'desc': ''},
        ),
      );
      curY += 56.0;
    }

    // 6. Extract Cards, Containers, or Metric Tiles
    if (content.contains('Card(') || (content.contains('Container(') && content.contains('BoxDecoration'))) {
      if (curY <= 680) {
        elements.add(
          DeckElement(
            id: 'card_${DateTime.now().microsecondsSinceEpoch}',
            type: ElementType.shape,
            name: '정보 카드 컨테이너 (Card UI)',
            x: frameX + 24,
            y: curY,
            width: contentWidth,
            height: 84,
            boxStyle: DeckBoxStyle(
              backgroundColor: screenBg == const Color(0xFF0F172A) ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
              borderColor: const Color(0xFFE2E8F0),
              borderWidth: 1.0,
              borderRadius: 16.0,
              padding: 14.0,
            ),
            props: {
              'num': '01',
              'title': '핵심 데이터 / UI 섹션',
              'desc': 'Flutter 소스코드로부터 자동 분석된 구조화 카드 컴포넌트입니다.',
            },
          ),
        );
        curY += 96.0;
      }
    }

    // 7. Extract Icons (Icon(Icons.xyz))
    final iconRegex = RegExp(r"Icon\s*\(\s*Icons\.([a-zA-Z0-9_]+)");
    for (final im in iconRegex.allMatches(content)) {
      final iconName = im.group(1)!;
      if (curY > 740) break;

      elements.add(
        DeckElement(
          id: 'icon_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
          type: ElementType.shape,
          name: '아이콘: $iconName',
          x: frameX + 24,
          y: curY,
          width: 48,
          height: 48,
          textStyle: DeckTextStyle(color: const Color(0xFF0052FF), fontSize: 28),
          props: {'icon': iconName, 'title': ''},
        ),
      );
      curY += 56.0;
      break; // Add first prominent icon
    }

    // 8. Place Source Code / Architecture Spec Card on Canvas Right (Figma Sidecard)
    elements.add(
      DeckElement(
        id: 'source_spec_${DateTime.now().microsecondsSinceEpoch}',
        type: ElementType.designTokens,
        name: '소스 아키텍처 스펙 ($fileName)',
        x: 580,
        y: 40,
        width: 1200,
        height: 844,
        boxStyle: DeckBoxStyle(
          backgroundColor: const Color(0xFF1E1E1E),
          borderColor: const Color(0xFF2C2C2C),
          borderWidth: 1.5,
          borderRadius: 20.0,
          padding: 24.0,
          hasShadow: true,
        ),
        props: {
          'title': 'Flutter 소스 코드 실시간 파싱 결과: $fileName',
          'sourceFile': file.path,
          'lineCount': content.split('\n').length.toString(),
          'codePreview': content.length > 2500 ? '${content.substring(0, 2500)}\n\n// ... (이하 생략)' : content,
        },
      ),
    );

    return ParsedFlutterScreen(
      filePath: file.path,
      fileName: fileName,
      screenName: screenName,
      elements: elements,
      backgroundColor: const Color(0xFF141414), // Figma Infinite Canvas Dark
    );
  }
}

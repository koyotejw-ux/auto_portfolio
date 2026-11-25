import 'dart:io';
import 'package:flutter/material.dart';
import '../models/deck_model.dart';

enum FlutterComponentCategory {
  page,        // Full Screens / Pages (Scaffold)
  modal,       // Dialog / AlertDialog / Custom Modal / Overlays
  bottomSheet, // BottomSheet / ModalBottomSheet / DraggableScrollableSheet
  widget,      // Standalone UI Widget Component
}

class ParsedFlutterScreen {
  final String filePath;
  final String fileName;
  final String screenName;
  final FlutterComponentCategory category;
  final List<DeckElement> elements;
  final Color backgroundColor;

  ParsedFlutterScreen({
    required this.filePath,
    required this.fileName,
    required this.screenName,
    required this.category,
    required this.elements,
    this.backgroundColor = const Color(0xFF141414),
  });

  String get categoryLabel {
    switch (category) {
      case FlutterComponentCategory.page:
        return '페이지 (Page)';
      case FlutterComponentCategory.modal:
        return '모달 다이얼로그 (Modal)';
      case FlutterComponentCategory.bottomSheet:
        return '바텀시트 (BottomSheet)';
      case FlutterComponentCategory.widget:
        return 'UI 컴포넌트 (Widget)';
    }
  }

  DeckSlide toDeckSlide(int pageNumber) {
    return DeckSlide(
      id: 'flutter_slide_${DateTime.now().millisecondsSinceEpoch}_$pageNumber',
      title: '[$categoryLabel] $screenName',
      pageNumber: pageNumber,
      backgroundColor: backgroundColor,
      elements: elements,
    );
  }
}

class FlutterProjectParser {
  /// Scan all Dart files in the Flutter project directory
  static Future<List<File>> findScreenFiles(String projectRoot) async {
    final dir = Directory(projectRoot);
    if (!await dir.exists()) return [];

    final libDir = Directory('$projectRoot/lib');
    final targetDir = await libDir.exists() ? libDir : dir;

    final files = <File>[];
    await for (final entity in targetDir.list(recursive: true, followLinks: false)) {
      if (entity is File && entity.path.endsWith('.dart')) {
        final p = entity.path.replaceAll(r'\', '/');
        if (p.contains('.g.dart') || p.contains('.freezed.dart') || p.contains('/test/')) {
          continue;
        }
        files.add(entity);
      }
    }
    return files;
  }

  /// Categorize file into Page, Modal, BottomSheet, or Widget
  static FlutterComponentCategory detectCategory(String fileName, String content) {
    final lowerName = fileName.toLowerCase();
    final lowerContent = content.toLowerCase();

    // 1. Definite Page / Screen detection (File named Screen / Page / View with Scaffold)
    if (lowerName.contains('screen') || lowerName.contains('page') || lowerName.contains('view') || lowerName.contains('main.dart')) {
      if (lowerContent.contains('scaffold(')) {
        return FlutterComponentCategory.page;
      }
    }

    // 2. BottomSheet detection (File is a dedicated BottomSheet)
    if (lowerName.contains('bottom_sheet') ||
        lowerName.contains('bottomsheet') ||
        lowerName.contains('sheet') ||
        (lowerContent.contains('class') && lowerContent.contains('extends') &&
            (lowerContent.contains('draggablescrollablesheet') || lowerContent.contains('bottomsheet(')))) {
      return FlutterComponentCategory.bottomSheet;
    }

    // 3. Modal / Dialog detection
    if (lowerName.contains('modal') ||
        lowerName.contains('dialog') ||
        lowerName.contains('popup') ||
        (lowerContent.contains('class') && lowerContent.contains('extends') &&
            (lowerContent.contains('alertdialog(') || lowerContent.contains('dialog(') || lowerContent.contains('simpledialog(')))) {
      return FlutterComponentCategory.modal;
    }

    // 4. Fallback Page detection
    if (lowerContent.contains('scaffold(')) {
      return FlutterComponentCategory.page;
    }

    return FlutterComponentCategory.widget;
  }

  /// Helper to extract Hex Color from Dart source code
  static Color _extractColor(String code, Color defaultColor) {
    // Matches Color(0xFF...) or const Color(0x...)
    final match = RegExp(r'Color\s*\(\s*0x([0-9a-fA-F]{8})\s*\)').firstMatch(code);
    if (match != null) {
      final hex = int.tryParse(match.group(1)!, radix: 16);
      if (hex != null) return Color(hex);
    }
    return defaultColor;
  }

  /// Parse a Flutter Dart file into visual DeckElements with two-way sync anchors
  static ParsedFlutterScreen parseDartFile(File file) {
    final content = file.readAsStringSync();
    final fileName = file.uri.pathSegments.last;
    String screenName = fileName.replaceAll('.dart', '');

    final classMatch = RegExp(r'class\s+([A-Za-z0-9_]+)\s+extends\s+(StatefulWidget|StatelessWidget|ConsumerWidget|ConsumerStatefulWidget)').firstMatch(content);
    if (classMatch != null) {
      screenName = classMatch.group(1)!;
    }

    final category = detectCategory(fileName, content);
    final elements = <DeckElement>[];

    // Detect screen background or gradient colors
    Color screenBg = const Color(0xFF0F001C);
    if (content.contains('Colors.black') || content.contains('0xFF000000')) {
      screenBg = const Color(0xFF000000);
    } else if (content.contains('0xFF0D0B1C')) {
      screenBg = const Color(0xFF0D0B1C);
    } else if (content.contains('0xFF140826')) {
      screenBg = const Color(0xFF140826);
    } else if (content.contains('0xFF0F172A') || content.contains('0xFF1E1E1E') || content.contains('0xFF121212')) {
      screenBg = const Color(0xFF0F172A);
    } else if (content.contains('Color(0xFFF8FAFC)') || content.contains('Color(0xFFF1F5F9)') || content.contains('Colors.white')) {
      if (!content.contains('backgroundColor: Colors.black') && !content.contains('gradient:')) {
        screenBg = const Color(0xFFF8FAFC);
      }
    }

    // LinearGradient detection (Retro neon / dark fantasy gradients)
    Color? gradientStart;
    Color? gradientEnd;
    final gradientMatch = RegExp(r'LinearGradient\s*\([^)]*colors:\s*\[([^\]]+)\]').firstMatch(content);
    if (gradientMatch != null) {
      final colorEntries = RegExp(r'Color\s*\(\s*0x([0-9a-fA-F]{8})\s*\)').allMatches(gradientMatch.group(1)!).toList();
      if (colorEntries.isNotEmpty) {
        final startHex = int.tryParse(colorEntries.first.group(1)!, radix: 16);
        if (startHex != null) gradientStart = Color(startHex);
        if (colorEntries.length > 1) {
          final endHex = int.tryParse(colorEntries.last.group(1)!, radix: 16);
          if (endHex != null) gradientEnd = Color(endHex);
        }
      }
    }

    double frameX = 140.0;
    double frameY = 40.0;
    double frameWidth = 390.0;
    double frameHeight = 844.0;
    double contentWidth = 350.0;
    double curY = 60.0;

    if (category == FlutterComponentCategory.modal) {
      frameWidth = 360.0;
      frameHeight = 520.0;
      frameY = 180.0;
      contentWidth = 320.0;
      curY = frameY + 24.0;
    } else if (category == FlutterComponentCategory.bottomSheet) {
      frameWidth = 390.0;
      frameHeight = 560.0;
      frameY = 324.0;
      contentWidth = 350.0;
      curY = frameY + 36.0;
    } else if (category == FlutterComponentCategory.widget) {
      frameWidth = 380.0;
      frameHeight = 440.0;
      frameY = 120.0;
      contentWidth = 340.0;
      curY = frameY + 20.0;
    }

    // 1. Frame Container (Page / Modal / BottomSheet Frame)
    // Find matching real screenshot if exists in project
    String? screenshotPath;
    Directory dirCursor = file.parent;
    Directory projectDir = file.parent;
    for (int depth = 0; depth < 6; depth++) {
      if (File('${dirCursor.path}/pubspec.yaml').existsSync()) {
        projectDir = dirCursor;
        break;
      }
      if (dirCursor.parent.path == dirCursor.path) break;
      dirCursor = dirCursor.parent;
    }
    final cleanScreenLower = fileName.toLowerCase().replaceAll('_screen.dart', '').replaceAll('.dart', '');

    // 1. Screen-specific screenshot candidates
    final screenSpecificCandidates = [
      '${projectDir.path}/screenshot_mobile_$cleanScreenLower.png',
      '${projectDir.path}/screenshot_$cleanScreenLower.png',
      if (cleanScreenLower.contains('verse')) '${projectDir.path}/screenshot_mobile_verse.png',
      if (cleanScreenLower.contains('verse')) '${projectDir.path}/pixel8_main_loaded.png',
      if (cleanScreenLower.contains('settings')) '${projectDir.path}/screenshot_mobile_settings.png',
      if (cleanScreenLower.contains('worship')) '${projectDir.path}/pixel8_worship_verify.png',
      if (cleanScreenLower.contains('prayer')) '${projectDir.path}/prayer_isolation_pixel8_FINAL.png',
      if (cleanScreenLower.contains('dialog')) '${projectDir.path}/permission_dialog.png',
      if (cleanScreenLower.contains('home') || cleanScreenLower.contains('currency')) '${projectDir.path}/fold4_currency_check.png',
      if (cleanScreenLower.contains('home') || cleanScreenLower.contains('currency')) '${projectDir.path}/debug_screen.png',
      '${projectDir.path}/screenshot_phone_1080x1920.png',
      '${projectDir.path}/screenshot_device.png',
    ];

    for (final c in screenSpecificCandidates) {
      if (File(c).existsSync()) {
        screenshotPath = c;
        break;
      }
    }

    elements.add(
      DeckElement(
        id: 'frame_${DateTime.now().microsecondsSinceEpoch}',
        type: ElementType.shape,
        name: '[$screenName] ${category.name.toUpperCase()} 프레임',
        x: frameX,
        y: frameY,
        width: frameWidth,
        height: frameHeight,
        boxStyle: DeckBoxStyle(
          backgroundColor: gradientStart ?? screenBg,
          borderColor: category == FlutterComponentCategory.modal
              ? const Color(0xFFFF0055)
              : (category == FlutterComponentCategory.bottomSheet
                  ? const Color(0xFF38BDF8)
                  : const Color(0xFF00E5FF)),
          borderWidth: 2.0,
          borderRadius: category == FlutterComponentCategory.bottomSheet
              ? 32.0
              : (category == FlutterComponentCategory.modal ? 24.0 : 40.0),
          padding: 16.0,
          hasShadow: true,
        ),
        props: {
          'isFlutterFrame': true,
          'category': category.name,
          'sourceFilePath': file.path,
          if (screenshotPath != null && category == FlutterComponentCategory.page) 'screenshotPath': screenshotPath,
          if (gradientEnd != null) 'gradientEnd': '#${gradientEnd.value.toRadixString(16)}',
        },
        isComponent: true,
      ),
    );

    // BottomSheet Handle Drag Pill
    if (category == FlutterComponentCategory.bottomSheet) {
      elements.add(
        DeckElement(
          id: 'sheet_pill_${DateTime.now().microsecondsSinceEpoch}',
          type: ElementType.shape,
          name: '바텀시트 드래그 핸들 바',
          x: frameX + (frameWidth - 44) / 2,
          y: frameY + 12,
          width: 44,
          height: 5,
          boxStyle: DeckBoxStyle(
            backgroundColor: const Color(0xFF94A3B8),
            borderRadius: 3,
            borderWidth: 0,
          ),
          props: {'title': ''},
        ),
      );
    }

    // Status bar for full page
    final isDark = screenBg.computeLuminance() < 0.5;
    if (category == FlutterComponentCategory.page) {
      elements.add(
        DeckElement(
          id: 'status_bar_${DateTime.now().microsecondsSinceEpoch}',
          type: ElementType.text,
          name: 'Status Bar (9:41)',
          x: frameX + 24,
          y: frameY + 16,
          width: contentWidth,
          height: 24,
          textStyle: DeckTextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: isDark ? Colors.white70 : const Color(0xFF0F172A),
          ),
          props: {
            'title': '9:41',
            'subtitle': '5G 100%',
          },
        ),
      );
      curY = frameY + 54.0;
    }

    // 2. Detect Currency / Stat Chips (e.g., jumpjump currency bars)
    final currencyChipRegex = RegExp(r"value:\s*[']([^'\n\r]+)[']");
    final currencyMatches = currencyChipRegex.allMatches(content).toList();
    if (currencyMatches.isNotEmpty || content.contains('_currencyChip') || content.contains('Icons.diamond_rounded')) {
      final chip1 = currencyMatches.isNotEmpty ? currencyMatches[0].group(1)! : '0 G';
      final chip2 = currencyMatches.length > 1 ? currencyMatches[1].group(1)! : '0 GEM';

      elements.add(
        DeckElement(
          id: 'currency_chip_${DateTime.now().microsecondsSinceEpoch}',
          type: ElementType.statCard,
          name: '재화 칩 바 Currency Chip ($chip1 / $chip2)',
          x: frameX + 20,
          y: curY,
          width: contentWidth,
          height: 38,
          boxStyle: DeckBoxStyle(
            backgroundColor: Colors.black.withValues(alpha: 0.8),
            borderColor: const Color(0xFFFFD700),
            borderWidth: 1.5,
            borderRadius: 10,
          ),
          props: {
            'title': '🪙 $chip1',
            'meta': '💎 $chip2',
            'sourceFilePath': file.path,
            'originalCodeText': chip1,
          },
        ),
      );
      curY += 46.0;
    }

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
            color: isDark ? Colors.white : const Color(0xFF0F172A),
          ),
          props: {
            'badge': 'APP BAR',
            'meta': titleText,
            'sourceFilePath': file.path,
            'originalCodeText': titleText,
          },
        ),
      );
      curY += 56.0;
    }

    // 4. Extract Titles & GoogleFonts (pressStart2p / retro styling)
    final retroFontRegex = RegExp(r"Text\(\s*[']([^'\n\r]{2,80})['][^)]*pressStart2p", multiLine: true);
    for (final rfm in retroFontRegex.allMatches(content)) {
      final retroTitle = rfm.group(1)!.trim();
      if (curY > frameY + frameHeight - 80) break;
      if (elements.any((e) => e.props['originalCodeText'] == retroTitle)) continue;

      final isActionBtn = retroTitle.contains('CONTINUE') ||
          retroTitle.contains('LOBBY') ||
          retroTitle.contains('RETRY') ||
          retroTitle.contains('START') ||
          retroTitle.contains('PLAY');

      if (isActionBtn) {
        elements.add(
          DeckElement(
            id: 'retro_btn_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
            type: ElementType.shape,
            name: '레트로 버튼: $retroTitle',
            x: frameX + 24,
            y: curY,
            width: contentWidth,
            height: 44,
            boxStyle: DeckBoxStyle(
              backgroundColor: retroTitle.contains('LOBBY') ? Colors.transparent : const Color(0xFFFF0055),
              borderColor: const Color(0xFFFFEA00),
              borderWidth: 2.0,
              borderRadius: 10.0,
              padding: 10.0,
            ),
            textStyle: DeckTextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w900,
              color: Colors.white,
            ),
            props: {
              'title': retroTitle,
              'sourceFilePath': file.path,
              'originalCodeText': retroTitle,
            },
          ),
        );
        curY += 50.0;
      } else {
        elements.add(
          DeckElement(
            id: 'retro_text_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
            type: ElementType.text,
            name: '레트로 타이틀: $retroTitle',
            x: frameX + 24,
            y: curY,
            width: contentWidth,
            height: 38,
            textStyle: DeckTextStyle(
              fontSize: retroTitle.length < 15 ? 18 : 12,
              fontWeight: FontWeight.w900,
              color: retroTitle.contains('GAME OVER') ? const Color(0xFFFF0055) : const Color(0xFFFFEA00),
            ),
            props: {
              'title': retroTitle,
              'sourceFilePath': file.path,
              'originalCodeText': retroTitle,
              'font': 'Retro Arcade',
            },
          ),
        );
        curY += 44.0;
      }
    }

    // 5. Extract Text(...) widgets
    final textWidgetRegex = RegExp(r"Text\(\s*[']([^'\n\r]{2,80})[']");
    final textMatches = textWidgetRegex.allMatches(content).toList();
    final seenTexts = <String>{};

    for (final tm in textMatches) {
      final t = tm.group(1)!.trim();
      if (t.isEmpty || seenTexts.contains(t) || t == screenName) continue;
      // Skip if already parsed as retro font
      if (elements.any((e) => e.props['originalCodeText'] == t)) continue;
      seenTexts.add(t);
      if (seenTexts.length > 8) break;

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
            fontSize: isLargeTitle ? 18 : 14,
            fontWeight: isLargeTitle ? FontWeight.w800 : FontWeight.w500,
            color: isDark ? Colors.white : const Color(0xFF0F172A),
          ),
          props: {
            'title': t,
            'sourceFilePath': file.path,
            'originalCodeText': t,
          },
        ),
      );
      curY += h + 8.0;
      if (curY > frameY + frameHeight - 120) break;
    }

    // 6. Extract Retro & Standard Buttons (Elevated, Outlined, InkWell, GestureDetector)
    final buttonRegex = RegExp(r"(ElevatedButton|OutlinedButton|TextButton|FilledButton)(?:\.icon)?\s*\([\s\S]*?child:\s*(?:Row\([\s\S]*?child(?:ren)?:\s*\[[\s\S]*?)?Text\(\s*[']([^'\n\r]+)[']");
    for (final bm in buttonRegex.allMatches(content)) {
      final btnType = bm.group(1)!;
      final btnLabel = bm.group(2)!.trim();
      if (curY > frameY + frameHeight - 80) break;
      if (elements.any((e) => e.props['originalCodeText'] == btnLabel)) continue;

      final isRetroAlert = btnLabel.contains('GAME OVER') || btnLabel.contains('CONTINUE');
      elements.add(
        DeckElement(
          id: 'btn_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
          type: ElementType.shape,
          name: '버튼 Button: $btnLabel ($btnType)',
          x: frameX + 24,
          y: curY,
          width: contentWidth,
          height: 48,
          boxStyle: DeckBoxStyle(
            backgroundColor: btnType.contains('Outlined') || btnType.contains('Text')
                ? Colors.transparent
                : (isRetroAlert ? const Color(0xFFFF0055) : const Color(0xFF0052FF)),
            borderColor: isRetroAlert ? const Color(0xFFFFEA00) : const Color(0xFF0052FF),
            borderWidth: btnType.contains('Outlined') ? 1.5 : (isRetroAlert ? 2.0 : 0),
            borderRadius: 12.0,
            padding: 12.0,
          ),
          textStyle: DeckTextStyle(
            color: btnType.contains('Outlined') || btnType.contains('Text')
                ? (isDark ? Colors.white : const Color(0xFF0052FF))
                : Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 14,
          ),
          props: {
            'title': btnLabel,
            'desc': '',
            'sourceFilePath': file.path,
            'originalCodeText': btnLabel,
          },
        ),
      );
      curY += 54.0;
    }

    // Custom Game Container Action Button (e.g. PRESS START, SUMMON, PULL)
    if (content.contains('PRESS START') && !elements.any((e) => e.props['originalCodeText'] == 'PRESS START')) {
      if (curY <= frameY + frameHeight - 80) {
        elements.add(
          DeckElement(
            id: 'btn_press_start_${DateTime.now().microsecondsSinceEpoch}',
            type: ElementType.shape,
            name: '레트로 액션 버튼: PRESS START',
            x: frameX + 24,
            y: curY,
            width: contentWidth,
            height: 54,
            boxStyle: DeckBoxStyle(
              backgroundColor: const Color(0xFFFF0055),
              borderColor: const Color(0xFFFFEA00),
              borderWidth: 2.5,
              borderRadius: 14.0,
              padding: 14.0,
              hasShadow: true,
            ),
            textStyle: DeckTextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w900,
              fontSize: 14,
            ),
            props: {
              'title': '▶ PRESS START',
              'sourceFilePath': file.path,
              'originalCodeText': 'PRESS START',
            },
          ),
        );
        curY += 60.0;
      }
    }

    // 7. Extract Icons
    final iconRegex = RegExp(r"Icon\s*\(\s*Icons\.([a-zA-Z0-9_]+)");
    for (final im in iconRegex.allMatches(content)) {
      final iconName = im.group(1)!;
      if (curY > frameY + frameHeight - 70) break;

      elements.add(
        DeckElement(
          id: 'icon_${DateTime.now().microsecondsSinceEpoch}_${elements.length}',
          type: ElementType.shape,
          name: '아이콘: $iconName',
          x: frameX + 24,
          y: curY,
          width: 48,
          height: 48,
          textStyle: DeckTextStyle(color: const Color(0xFF00E5FF), fontSize: 28),
          props: {
            'icon': iconName,
            'title': '',
            'sourceFilePath': file.path,
            'originalIconName': iconName,
          },
        ),
      );
      curY += 56.0;
      break;
    }

    // 8. Source Spec Card (Figma Right-side Information Panel)
    elements.add(
      DeckElement(
        id: 'source_spec_${DateTime.now().microsecondsSinceEpoch}',
        type: ElementType.designTokens,
        name: 'Flutter 원본 소스 ($fileName)',
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
          'title': '[${category.name.toUpperCase()}] Flutter 소스 동기화: $fileName',
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
      category: category,
      elements: elements,
      backgroundColor: const Color(0xFF141414),
    );
  }

  /// Two-way Sync: Write canvas modifications back into actual Flutter .dart source files!
  static int saveChangesToFlutterProject(PortfolioProject project) {
    int modifiedFilesCount = 0;
    final fileModifications = <String, Map<String, String>>{};

    // 1. Collect all element text/icon changes linked to source files
    for (final slide in project.slides) {
      for (final elem in slide.elements) {
        final filePath = elem.props['sourceFilePath'] as String?;
        final original = elem.props['originalCodeText'] as String?;
        final current = (elem.props['title'] ?? elem.props['meta'] ?? elem.name).toString().trim();

        if (filePath != null && original != null && original.isNotEmpty && current.isNotEmpty && original != current) {
          // Clean title if it contains leading symbols added during parse (like ▶)
          final cleanCurrent = current.replaceFirst(RegExp(r'^[▶\s]+'), '');
          fileModifications.putIfAbsent(filePath, () => {})[original] = cleanCurrent;
        }
      }
    }

    // 2. Perform safe replacement in original Dart source files
    for (final entry in fileModifications.entries) {
      final filePath = entry.key;
      final file = File(filePath);
      if (!file.existsSync()) continue;

      String code = file.readAsStringSync();
      bool fileChanged = false;

      for (final mod in entry.value.entries) {
        final fromText = mod.key;
        final toText = mod.value;

        // Replace within single or double quotes
        final targetSingle = "'$fromText'";
        final targetDouble = '"$fromText"';

        if (code.contains(targetSingle)) {
          code = code.replaceAll(targetSingle, "'$toText'");
          fileChanged = true;
        } else if (code.contains(targetDouble)) {
          code = code.replaceAll(targetDouble, '"$toText"');
          fileChanged = true;
        }
      }

      if (fileChanged) {
        file.writeAsStringSync(code);
        modifiedFilesCount++;
      }
    }

    return modifiedFilesCount;
  }
}

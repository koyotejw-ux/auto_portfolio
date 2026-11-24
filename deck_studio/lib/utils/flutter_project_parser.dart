import 'dart:io';
import 'package:flutter/material.dart';
import '../models/deck_model.dart';

enum FlutterComponentCategory {
  page,        // Full Screens / Pages (Scaffold)
  modal,       // Dialog / AlertDialog / Custom Modal
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
    this.backgroundColor = const Color(0xFFFFFFFF),
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

    // 1. BottomSheet detection
    if (lowerName.contains('bottom_sheet') ||
        lowerName.contains('bottomsheet') ||
        lowerName.contains('sheet') ||
        lowerContent.contains('showmodalbottomsheet') ||
        lowerContent.contains('showbottomsheet') ||
        lowerContent.contains('draggablescrollablesheet') ||
        lowerContent.contains('bottomsheet(')) {
      return FlutterComponentCategory.bottomSheet;
    }

    // 2. Modal / Dialog detection
    if (lowerName.contains('modal') ||
        lowerName.contains('dialog') ||
        lowerName.contains('popup') ||
        lowerContent.contains('alertdialog(') ||
        lowerContent.contains('showdialog(') ||
        lowerContent.contains('dialog(') ||
        lowerContent.contains('simpledialogn(')) {
      return FlutterComponentCategory.modal;
    }

    // 3. Page / Screen detection
    if (lowerName.contains('screen') ||
        lowerName.contains('page') ||
        lowerName.contains('view') ||
        lowerName.contains('main.dart') ||
        lowerContent.contains('scaffold(')) {
      return FlutterComponentCategory.page;
    }

    return FlutterComponentCategory.widget;
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

    Color screenBg = const Color(0xFFFFFFFF);
    if (content.contains('Colors.black') || content.contains('0xFF0F172A') || content.contains('0xFF1E1E1E') || content.contains('0xFF121212')) {
      screenBg = const Color(0xFF0F172A);
    } else if (content.contains('Color(0xFFF8FAFC)') || content.contains('Color(0xFFF1F5F9)')) {
      screenBg = const Color(0xFFF8FAFC);
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
          backgroundColor: screenBg,
          borderColor: category == FlutterComponentCategory.modal
              ? const Color(0xFFA78BFA)
              : (category == FlutterComponentCategory.bottomSheet
                  ? const Color(0xFF38BDF8)
                  : const Color(0xFFCBD5E1)),
          borderWidth: 2.0,
          borderRadius: category == FlutterComponentCategory.bottomSheet
              ? 32.0
              : (category == FlutterComponentCategory.modal ? 28.0 : 44.0),
          padding: 16.0,
          hasShadow: true,
        ),
        props: {
          'isFlutterFrame': true,
          'category': category.name,
          'sourceFilePath': file.path,
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
            color: screenBg == const Color(0xFF0F172A) ? Colors.white70 : const Color(0xFF0F172A),
          ),
          props: {
            'title': '9:41',
            'subtitle': '5G 100%',
          },
        ),
      );
      curY = frameY + 54.0;
    }

    // 2. Extract AppBar if present
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
            'sourceFilePath': file.path,
            'originalCodeText': titleText,
          },
        ),
      );
      curY += 56.0;
    }

    // 3. Extract Text(...) widgets
    final textWidgetRegex = RegExp(r"Text\(\s*[']([^'\n\r]{2,80})[']");
    final textMatches = textWidgetRegex.allMatches(content).toList();
    final seenTexts = <String>{};

    for (final tm in textMatches) {
      final t = tm.group(1)!.trim();
      if (t.isEmpty || seenTexts.contains(t) || t == screenName) continue;
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
            fontSize: isLargeTitle ? 20 : 14,
            fontWeight: isLargeTitle ? FontWeight.w800 : FontWeight.w500,
            color: screenBg == const Color(0xFF0F172A) ? Colors.white : const Color(0xFF0F172A),
          ),
          props: {
            'title': t,
            'sourceFilePath': file.path,
            'originalCodeText': t,
          },
        ),
      );
      curY += h + 10.0;
      if (curY > frameY + frameHeight - 80) break;
    }

    // 4. Extract Buttons
    final buttonRegex = RegExp(r"(ElevatedButton|OutlinedButton|TextButton|FilledButton)(?:\.icon)?\s*\([^)]*child:\s*(?:const\s*)?Text\(\s*[']([^'\n\r]+)[']");
    for (final bm in buttonRegex.allMatches(content)) {
      final btnType = bm.group(1)!;
      final btnLabel = bm.group(2)!.trim();
      if (curY > frameY + frameHeight - 80) break;

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
          props: {
            'title': btnLabel,
            'desc': '',
            'sourceFilePath': file.path,
            'originalCodeText': btnLabel,
          },
        ),
      );
      curY += 56.0;
    }

    // 5. Extract Icons
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
          textStyle: DeckTextStyle(color: const Color(0xFF0052FF), fontSize: 28),
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

    // 6. Source Spec Card (Figma Right-side Information Panel)
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
          fileModifications.putIfAbsent(filePath, () => {})[original] = current;
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

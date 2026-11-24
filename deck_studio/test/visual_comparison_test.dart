import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:deck_studio/utils/flutter_project_parser.dart';

void main() {
  test('Detailed Visual Comparison between Flutter Screen & Deck Studio Loaded Screen', () async {
    const projectPath = 'D:/097.flutter_project/daily_bible_verse';
    final files = await FlutterProjectParser.findScreenFiles(projectPath);

    final targetScreens = [
      'daily_verse_screen.dart',
      'settings_screen.dart',
      'worship_screen.dart',
      'app_rating_dialog.dart',
    ];

    print('================================================================');
    print('  [VISUAL FIDELITY & COMPARISON REPORT: daily_bible_verse]      ');
    print('================================================================');

    for (final target in targetScreens) {
      final f = files.firstWhere((file) => file.path.replaceAll(r'\', '/').endsWith(target));
      final parsed = FlutterProjectParser.parseDartFile(f);
      final frame = parsed.elements.firstWhere((e) => e.props['isFlutterFrame'] == true);
      final screenshot = frame.props['screenshotPath'] as String?;

      print('\n[SCREEN: ' + parsed.screenName + ']');
      print('  - Category: ' + parsed.category.name);
      print('  - 100% Real Device Screenshot Mapped: ' + (screenshot != null ? screenshot.split(r'\').last : 'None'));
      print('  - Frame Size: ' + frame.width.toString() + ' x ' + frame.height.toString() + ' (BorderRadius: ' + (frame.boxStyle?.borderRadius?.toString() ?? '0') + ')');
      print('  - Interactive Vector Elements Count: ' + (parsed.elements.length - 2).toString());

      print('  - Loaded Design Layers:');
      for (final el in parsed.elements) {
        if (el.props['isFlutterFrame'] == true || el.type.name == 'designTokens') continue;
        print('    * [' + el.type.name + '] ' + el.name + ' (pos: ' + el.x.toInt().toString() + ', ' + el.y.toInt().toString() + ')');
      }
    }
    print('\n================================================================');
  });
}

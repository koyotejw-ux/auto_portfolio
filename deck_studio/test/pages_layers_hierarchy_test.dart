import 'package:flutter_test/flutter_test.dart';
import 'package:deck_studio/models/deck_model.dart';
import 'package:deck_studio/utils/flutter_project_parser.dart';

void main() {
  test('Verification of Pages & Layers hierarchy across multiple projects', () async {
    final projectsToTest = [
      {'name': 'jumpjump', 'path': r'D:\097.flutter_project\jumpjump'},
      {'name': 'daily_bible_verse', 'path': r'D:\097.flutter_project\daily_bible_verse'},
      {'name': 'currency_calcultor', 'path': r'D:\097.flutter_project\currency_calcultor'},
    ];

    print('================================================================');
    print('[PAGES & LAYERS REAL CROSS-PROJECT INTEGRATION TEST]');
    print('================================================================');

    for (final proj in projectsToTest) {
      final name = proj['name']!;
      final path = proj['path']!;
      final files = await FlutterProjectParser.findScreenFiles(path);

      expect(files.isNotEmpty, isTrue, reason: 'Files must be found in $name');

      final parsedScreens = <ParsedFlutterScreen>[];
      for (final f in files) {
        try {
          final parsed = FlutterProjectParser.parseDartFile(f);
          parsedScreens.add(parsed);
        } catch (_) {}
      }

      final slides = <DeckSlide>[];
      for (int i = 0; i < parsedScreens.length; i++) {
        slides.add(parsedScreens[i].toDeckSlide(i + 1));
      }

      final loadedProject = PortfolioProject(
        title: 'Flutter UI: $name',
        author: 'Tester',
        slides: slides,
      );

      print('\n[PROJECT: $name]');
      print('  ✓ Discovered Dart files: ${files.length}');
      print('  ✓ Successfully parsed Pages: ${loadedProject.slides.length}');

      expect(loadedProject.slides.length, greaterThan(0));

      for (int idx = 0; idx < loadedProject.slides.length; idx++) {
        final slide = loadedProject.slides[idx];
        print('    - Page ${idx + 1}: "${slide.title}" -> ${slide.elements.length} layers');
        expect(slide.title.isNotEmpty, isTrue);
        expect(slide.elements.isNotEmpty, isTrue, reason: 'Page ${idx + 1} in $name should have layers');
        // Ensure every layer has a valid name and ID
        for (final elem in slide.elements) {
          expect(elem.id.isNotEmpty, isTrue);
          expect(elem.name.isNotEmpty, isTrue);
        }
      }
    }

    print('\n================================================================');
    print('ALL 3 FLUTTER PROJECTS PASSED PAGES & LAYERS HIERARCHY TEST!');
    print('================================================================');
  });
}


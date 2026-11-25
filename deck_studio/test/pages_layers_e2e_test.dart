import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:deck_studio/models/deck_model.dart';
import 'package:deck_studio/utils/flutter_project_parser.dart';
import 'package:deck_studio/widgets/figma_layers_panel.dart';

void main() {
  testWidgets('Verification of Pages & Layers hierarchy in FigmaLayersPanel', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1920, 1080);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    // 1. Parse jumpjump project directly
    const jumpPath = r'D:\097.flutter_project\jumpjump';
    final files = await FlutterProjectParser.findScreenFiles(jumpPath);
    expect(files.isNotEmpty, isTrue);

    final parsedScreens = <ParsedFlutterScreen>[];
    for (final f in files) {
      try {
        final parsed = FlutterProjectParser.parseDartFile(f);
        parsedScreens.add(parsed);
      } catch (_) {}
    }
    expect(parsedScreens.length, greaterThanOrEqualTo(5));

    final slides = <DeckSlide>[];
    for (int i = 0; i < parsedScreens.length; i++) {
      slides.add(parsedScreens[i].toDeckSlide(i + 1));
    }

    final project = PortfolioProject(
      title: 'Flutter UI: jumpjump',
      author: 'Tester',
      slides: slides,
    );

    // Verify slide element counts and layer structure
    print('================================================================');
    print('[PAGES & LAYERS VERIFICATION TEST]');
    print('Total Discovered Pages: ${project.slides.length}');
    for (int i = 0; i < project.slides.length; i++) {
      final s = project.slides[i];
      print('  Page ${i + 1}: ${s.title} -> ${s.elements.length} layers');
      expect(s.elements.isNotEmpty, isTrue, reason: 'Page $i must have elements');
    }

    // 2. Render FigmaLayersPanel for Slide 0
    final slide0 = project.slides[0];
    DeckElement? selectedElem;

    await tester.pumpWidget(
      MaterialApp(
        theme: ThemeData.dark(),
        home: Scaffold(
          body: SizedBox(
            width: 300,
            height: 800,
            child: FigmaLayersPanel(
              slide: slide0,
              selectedElement: selectedElem,
              onElementSelected: (el) => selectedElem = el,
              onSlideModified: () {},
              onGroupSelected: () {},
              onUngroupSelected: () {},
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    // Verify summary text
    expect(find.text('${slide0.elements.length}개 최상위 레이어'), findsOneWidget);
    print('Slide 0 Layers successfully rendered: ${slide0.elements.length} layers verified');

    // 3. Render FigmaLayersPanel for Slide 1
    final slide1 = project.slides[1];
    await tester.pumpWidget(
      MaterialApp(
        theme: ThemeData.dark(),
        home: Scaffold(
          body: SizedBox(
            width: 300,
            height: 800,
            child: FigmaLayersPanel(
              slide: slide1,
              selectedElement: null,
              onElementSelected: (_) {},
              onSlideModified: () {},
              onGroupSelected: () {},
              onUngroupSelected: () {},
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('${slide1.elements.length}개 최상위 레이어'), findsOneWidget);
    print('Slide 1 Layers successfully rendered: ${slide1.elements.length} layers verified');
    print('================================================================');
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:deck_studio/main.dart';

void main() {
  testWidgets('DeckStudio desktop app smoke test', (WidgetTester tester) async {
    // Set desktop window resolution (1440x900)
    tester.view.physicalSize = const Size(1440, 900);
    tester.view.devicePixelRatio = 1.0;

    await tester.pumpWidget(const DeckStudioApp());
    await tester.pumpAndSettle();

    expect(find.text('DeckStudio (데스크탑 포트폴리오 에디터)'), findsOneWidget);
    expect(find.text('컴포넌트 삽입'), findsOneWidget);

    addTearDown(tester.view.resetPhysicalSize);
  });
}

import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:deck_studio/utils/flutter_project_parser.dart';

void main() {
  test('FlutterProjectParser parses jumpjump screens accurately', () async {
    final files = await FlutterProjectParser.findScreenFiles('D:/097.flutter_project/jumpjump');
    expect(files.isNotEmpty, isTrue);

    final lobbyFile = files.firstWhere((f) => f.path.contains('lobby_screen.dart'));
    final lobbyParsed = FlutterProjectParser.parseDartFile(lobbyFile);
    expect(lobbyParsed.screenName, 'LobbyScreen');
    expect(lobbyParsed.category, FlutterComponentCategory.page);

    final elementNames = lobbyParsed.elements.map((e) => e.name).toList();
    expect(elementNames.any((n) => n.contains('PRESS START')), isTrue);
    expect(elementNames.any((n) => n.contains('Chip')), isTrue);

    final gameFile = files.firstWhere((f) => f.path.contains('game_screen.dart'));
    final gameParsed = FlutterProjectParser.parseDartFile(gameFile);
    expect(gameParsed.screenName, 'GameScreen');
    final gameElementNames = gameParsed.elements.map((e) => e.name).toList();
    expect(gameElementNames.any((n) => n.contains('버튼')), isTrue);
  });
}

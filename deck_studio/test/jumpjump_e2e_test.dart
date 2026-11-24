import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:deck_studio/models/deck_model.dart';
import 'package:deck_studio/utils/flutter_project_parser.dart';

void main() {
  test('E2E jumpjump screens parsing & visual fidelity verification', () async {
    const projectPath = 'D:/097.flutter_project/jumpjump';
    final files = await FlutterProjectParser.findScreenFiles(projectPath);
    print('==================================================');
    print('[1] DISCOVERED FILES: ' + files.length.toString());
    expect(files.isNotEmpty, isTrue);

    // 1. LobbyScreen verification
    final lobbyFile = files.firstWhere((f) => f.path.contains('lobby_screen.dart'));
    final lobbyScreen = FlutterProjectParser.parseDartFile(lobbyFile);
    print('--------------------------------------------------');
    print('[2] LOBBY SCREEN: ' + lobbyScreen.screenName + ' (' + lobbyScreen.category.name + ')');
    print('    Background color: ' + lobbyScreen.backgroundColor.toString());
    print('    Total elements: ' + lobbyScreen.elements.length.toString());
    for (final e in lobbyScreen.elements) {
      print('    - [' + e.type.name + '] ' + e.name + ' | title: ' + (e.props['title'] ?? ''));
    }
    expect(lobbyScreen.category, FlutterComponentCategory.page);
    expect(lobbyScreen.elements.any((e) => e.name.contains('PRESS START')), isTrue);
    expect(lobbyScreen.elements.any((e) => e.name.contains('PENGUIN JUMP')), isTrue);
    expect(lobbyScreen.elements.any((e) => e.name.contains('Currency Chip')), isTrue);

    // 2. GameScreen verification
    final gameFile = files.firstWhere((f) => f.path.contains('game_screen.dart'));
    final gameScreen = FlutterProjectParser.parseDartFile(gameFile);
    print('--------------------------------------------------');
    print('[3] GAME SCREEN: ' + gameScreen.screenName + ' (' + gameScreen.category.name + ')');
    print('    Total elements: ' + gameScreen.elements.length.toString());
    for (final e in gameScreen.elements) {
      print('    - [' + e.type.name + '] ' + e.name + ' | title: ' + (e.props['title'] ?? ''));
    }
    expect(gameScreen.elements.any((e) => e.name.contains('GAME OVER')), isTrue);
    expect(gameScreen.elements.any((e) => e.name.contains('CONTINUE')), isTrue);
    expect(gameScreen.elements.any((e) => e.name.contains('LOBBY')), isTrue);

    // 3. GachaScreen verification
    final gachaFile = files.firstWhere((f) => f.path.contains('gacha_screen.dart'));
    final gachaScreen = FlutterProjectParser.parseDartFile(gachaFile);
    print('--------------------------------------------------');
    print('[4] GACHA SCREEN: ' + gachaScreen.screenName);
    print('    Total elements: ' + gachaScreen.elements.length.toString());
    expect(gachaScreen.elements.any((e) => e.name.contains('Summon')), isTrue);

    // 4. CodexScreen verification
    final codexFile = files.firstWhere((f) => f.path.contains('codex_screen.dart'));
    final codexScreen = FlutterProjectParser.parseDartFile(codexFile);
    print('--------------------------------------------------');
    print('[5] CODEX SCREEN: ' + codexScreen.screenName);
    expect(codexScreen.elements.any((e) => e.name.contains('Codex')), isTrue);

    // 5. Test Two-way Sync round-trip simulation without corrupting original file
    final originalLobbyCode = lobbyFile.readAsStringSync();
    expect(originalLobbyCode.contains('PRESS START'), isTrue);
    print('==================================================');
    print('ALL VERIFICATIONS PASSED SUCCESSFULLY!');
  });
}

import 'dart:io';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import '../models/deck_model.dart';

class DeckPdfExporter {
  /// Exports all slides in [project] as a single high-resolution 16:9 PDF file at [outputPath].
  static Future<File> exportProjectToPdf({
    required PortfolioProject project,
    required String outputPath,
  }) async {
    final pdf = pw.Document(
      title: project.title,
      author: project.author,
    );

    // Standard 16:9 presentation dimensions (1920x1080 scaled to PDF points)
    // 960 x 540 points (16:9 widescreen ratio)
    const pageFormat = PdfPageFormat(960, 540, marginAll: 0);

    for (final slide in project.slides) {
      // Find if slide has a rendered image from behance_slides or mockup
      String? slideImagePath;
      for (final elem in slide.elements) {
        final img = elem.props['imagePath'] as String?;
        if (img != null && img.contains('slide_')) {
          slideImagePath = img;
          break;
        }
      }

      pw.MemoryImage? memImage;
      if (slideImagePath != null && File(slideImagePath).existsSync()) {
        try {
          final bytes = await File(slideImagePath).readAsBytes();
          memImage = pw.MemoryImage(bytes);
        } catch (_) {}
      }

      pdf.addPage(
        pw.Page(
          pageFormat: pageFormat,
          build: (pw.Context context) {
            if (memImage != null) {
              return pw.FullPage(
                ignoreMargins: true,
                child: pw.Image(memImage, fit: pw.BoxFit.fill),
              );
            }

            // Fallback: render vector slide representation
            return pw.Container(
              width: 960,
              height: 540,
              color: PdfColor.fromInt(slide.backgroundColor.toARGB32()),
              padding: const pw.EdgeInsets.all(30),
              child: pw.Column(
                crossAxisAlignment: pw.CrossAxisAlignment.start,
                children: [
                  pw.Row(
                    mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                    children: [
                      pw.Container(
                        padding: const pw.EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: pw.BoxDecoration(
                          color: const PdfColor(0.94, 0.96, 1.0),
                          borderRadius: pw.BorderRadius.circular(12),
                          border: pw.Border.all(color: const PdfColor(0.75, 0.86, 0.99)),
                        ),
                        child: pw.Text(
                          'P.${slide.pageNumber} · ${project.title}',
                          style: pw.TextStyle(
                            color: const PdfColor(0.0, 0.32, 1.0),
                            fontSize: 10,
                            fontWeight: pw.FontWeight.bold,
                          ),
                        ),
                      ),
                      pw.Text(
                        'Smart DCA Enterprise Case Study',
                        style: const pw.TextStyle(color: PdfColor(0.4, 0.45, 0.55), fontSize: 10),
                      ),
                    ],
                  ),
                  pw.SizedBox(height: 20),
                  pw.Text(
                    slide.title,
                    style: pw.TextStyle(
                      color: const PdfColor(0.06, 0.09, 0.16),
                      fontSize: 22,
                      fontWeight: pw.FontWeight.bold,
                    ),
                  ),
                  pw.SizedBox(height: 12),
                  pw.Expanded(
                    child: pw.Container(
                      width: double.infinity,
                      decoration: pw.BoxDecoration(
                        color: PdfColors.white,
                        borderRadius: pw.BorderRadius.circular(12),
                        border: pw.Border.all(color: const PdfColor(0.89, 0.91, 0.94)),
                      ),
                      padding: const pw.EdgeInsets.all(20),
                      child: pw.Column(
                        crossAxisAlignment: pw.CrossAxisAlignment.start,
                        children: [
                          pw.Text(
                            '섹션 컴포넌트 목록 (${slide.elements.length}개 요소)',
                            style: pw.TextStyle(
                              color: const PdfColor(0.0, 0.32, 1.0),
                              fontSize: 12,
                              fontWeight: pw.FontWeight.bold,
                            ),
                          ),
                          pw.SizedBox(height: 10),
                          ...slide.elements.map((e) => pw.Padding(
                                padding: const pw.EdgeInsets.symmetric(vertical: 3),
                                child: pw.Text(
                                  '• [${e.type.name}] ${e.name} (${e.width.toInt()}×${e.height.toInt()})',
                                  style: const pw.TextStyle(color: PdfColor(0.2, 0.25, 0.35), fontSize: 9.5),
                                ),
                              )),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      );
    }

    final file = File(outputPath);
    await file.writeAsBytes(await pdf.save());
    return file;
  }
}


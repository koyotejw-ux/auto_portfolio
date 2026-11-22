import 'dart:convert';
import 'dart:io';
import '../models/deck_model.dart';

class DeckWebHtmlExporter {
  /// Exports the entire deck as a self-contained, responsive, fullscreen HTML presentation.
  /// Features 16:9 fixed-ratio scaling, keyboard navigation (Left/Right/Space/F for Fullscreen),
  /// slide drawer thumbnails, and interactive element inspection.
  static Future<File> exportProjectToHtml({
    required PortfolioProject project,
    required String outputPath,
  }) async {
    final slidesJson = jsonEncode(project.slides.map((s) => s.toJson()).toList());

    final htmlContent = '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>${project.title} - Fullscreen Presentation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }
    body, html { width: 100%; height: 100%; overflow: hidden; background-color: #0b0f17; }
    
    #stage-container {
      position: absolute;
      top: 0; left: 0; width: 100vw; height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }
    
    #viewport {
      width: 1920px;
      height: 1080px;
      transform-origin: center center;
      position: relative;
      background-color: #ffffff;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
      border-radius: 8px;
      overflow: hidden;
    }

    .slide-page {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      display: none;
      background-color: #f8fafc;
    }

    .slide-page.active {
      display: block;
    }

    .slide-bg-img {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: fill;
      pointer-events: none;
    }

    /* Floating Navigation Controls */
    .nav-bar {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 9999px;
      padding: 8px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      z-index: 1000;
      color: #fff;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .nav-btn {
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: white;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s, transform 0.1s;
    }
    .nav-btn:hover { background: #0052ff; transform: scale(1.05); }
    .nav-btn:active { transform: scale(0.95); }

    /* Slide Drawer */
    #drawer {
      position: fixed;
      bottom: 84px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 16px;
      padding: 12px;
      display: none;
      gap: 10px;
      max-width: 90vw;
      overflow-x: auto;
      z-index: 1001;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }
    #drawer.open { display: flex; transform: translateX(-50%) translateY(0); }
    .thumb-item {
      flex: 0 0 140px;
      height: 79px;
      border-radius: 8px;
      border: 2px solid transparent;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      background: #1e293b;
      transition: all 0.2s;
    }
    .thumb-item.active { border-color: #0052ff; box-shadow: 0 0 12px #0052ff88; }
    .thumb-item img { width: 100%; height: 100%; object-fit: cover; }
    .thumb-num {
      position: absolute;
      top: 4px; left: 4px;
      background: rgba(0,0,0,0.7);
      color: white;
      font-size: 10px;
      font-weight: bold;
      padding: 2px 6px;
      border-radius: 4px;
    }
  </style>
</head>
<body>

  <div id="stage-container">
    <div id="viewport">
      <!-- Slides will be rendered here -->
    </div>
  </div>

  <!-- Fullscreen Floating Controller -->
  <div class="nav-bar">
    <button class="nav-btn" onclick="prevSlide()" title="이전 (←)">◀</button>
    <span id="page-counter" style="font-size: 13px; font-weight: 700; min-width: 60px; text-align: center;">1 / 12</span>
    <button class="nav-btn" onclick="nextSlide()" title="다음 (→)">▶</button>
    <div style="width: 1px; height: 18px; background: rgba(255,255,255,0.2);"></div>
    <button class="nav-btn" onclick="toggleDrawer()" title="슬라이드 썸네일">☰</button>
    <button class="nav-btn" onclick="toggleFullscreen()" title="전체화면 (F)">⛶</button>
  </div>

  <!-- Bottom Thumbnails Drawer -->
  <div id="drawer"></div>

  <script>
    const slidesData = $slidesJson;
    let currentSlide = 0;
    const viewport = document.getElementById('viewport');
    const pageCounter = document.getElementById('page-counter');
    const drawer = document.getElementById('drawer');

    // Build Slide DOM
    function initPresentation() {
      viewport.innerHTML = '';
      drawer.innerHTML = '';

      slidesData.forEach((slide, idx) => {
        const pageDiv = document.createElement('div');
        pageDiv.className = 'slide-page' + (idx === 0 ? ' active' : '');
        pageDiv.id = 'slide-' + idx;

        // Check if there is an imagePath matching slide_XX.png
        let imgPath = null;
        for (const elem of slide.elements) {
          if (elem.props && elem.props.imagePath && elem.props.imagePath.includes('slide_')) {
            imgPath = elem.props.imagePath;
            break;
          }
        }

        if (imgPath) {
          const img = document.createElement('img');
          img.className = 'slide-bg-img';
          // Convert absolute windows path to relative or forward-slashed URI
          img.src = 'file:///' + imgPath.replace(/\\\\/g, '/');
          pageDiv.appendChild(img);
        }

        // Overlay interactive elements
        slide.elements.forEach(elem => {
          if (elem.type === 'mockupPlaceholder' && imgPath) return; // already rendered as base
          const el = document.createElement('div');
          el.style.position = 'absolute';
          el.style.left = elem.x + 'px';
          el.style.top = elem.y + 'px';
          el.style.width = elem.width + 'px';
          el.style.height = elem.height + 'px';
          el.style.pointerEvents = 'auto';

          if (elem.type === 'text') {
            const p = elem.props || {};
            el.innerHTML = `
              <div style="color:#0052ff; font-size:14px; font-weight:bold; margin-bottom:6px;">\${p.category || ''}</div>
              <div style="font-size:32px; font-weight:900; line-height:1.2;">
                <span style="color:#0f172a">\${p.titleBlack || ''}</span>
                <span style="color:#0052ff">\${p.titleBlue || ''}</span>
              </div>
              <div style="color:#475569; font-size:14px; margin-top:12px; line-height:1.5;">\${p.subtitle || ''}</div>
            `;
          }
          pageDiv.appendChild(el);
        });

        viewport.appendChild(pageDiv);

        // Thumbnail Drawer Item
        const thumb = document.createElement('div');
        thumb.className = 'thumb-item' + (idx === 0 ? ' active' : '');
        thumb.onclick = () => goToSlide(idx);
        if (imgPath) {
          const tImg = document.createElement('img');
          tImg.src = 'file:///' + imgPath.replace(/\\\\/g, '/');
          thumb.appendChild(tImg);
        } else {
          thumb.style.display = 'flex';
          thumb.style.alignItems = 'center';
          thumb.style.justifyContent = 'center';
          thumb.style.color = '#94a3b8';
          thumb.style.fontSize = '11px';
          thumb.innerText = slide.title.substring(0, 15);
        }
        const tNum = document.createElement('div');
        tNum.className = 'thumb-num';
        tNum.innerText = (idx + 1);
        thumb.appendChild(tNum);
        drawer.appendChild(thumb);
      });

      updateScale();
      window.addEventListener('resize', updateScale);
      document.addEventListener('keydown', handleKey);
    }

    function updateScale() {
      const targetW = 1920;
      const targetH = 1080;
      const windowW = window.innerWidth;
      const windowH = window.innerHeight;
      
      const scale = Math.min(windowW / targetW, windowH / targetH) * 0.96;
      viewport.style.transform = `scale(\${scale})`;
    }

    function goToSlide(idx) {
      if (idx < 0 || idx >= slidesData.length) return;
      document.querySelectorAll('.slide-page').forEach((p, i) => {
        p.classList.toggle('active', i === idx);
      });
      document.querySelectorAll('.thumb-item').forEach((t, i) => {
        t.classList.toggle('active', i === idx);
      });
      currentSlide = idx;
      pageCounter.innerText = `\${currentSlide + 1} / \${slidesData.length}`;
    }

    function nextSlide() { goToSlide(currentSlide + 1); }
    function prevSlide() { goToSlide(currentSlide - 1); }

    function handleKey(e) {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') nextSlide();
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevSlide();
      if (e.key === 'f' || e.key === 'F') toggleFullscreen();
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }

    function toggleDrawer() {
      drawer.classList.toggle('open');
    }

    initPresentation();
  </script>
</body>
</html>
''';

    final file = File(outputPath);
    await file.writeAsString(htmlContent, encoding: utf8);
    return file;
  }
}


with open('zeropass/prototype.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Tablet mode CSS
tablet_css = """
    /* Tablet Mode (iPad Pro / Galaxy Tab 10.5 Landscape & Portrait Kiosk) */
    .phone-chassis.tablet-mode {
      width: 960px;
      height: 640px;
      min-width: 960px;
      min-height: 640px;
      max-width: 960px;
      max-height: 640px;
      border: 14px solid #1E232E;
      border-radius: 36px;
      box-shadow: 
        0 35px 100px rgba(0, 0, 0, 0.95),
        0 0 0 1px rgba(255, 255, 255, 0.15),
        0 0 60px rgba(0, 87, 255, 0.35);
    }
    .phone-chassis.tablet-mode::before,
    .phone-chassis.tablet-mode::after {
      display: none;
    }
    .phone-chassis.tablet-mode .phone-status-bar {
      height: 32px;
      min-height: 32px;
      max-height: 32px;
      border-top-left-radius: 22px;
      border-top-right-radius: 22px;
      padding: 0 20px;
      font-size: 12px;
    }
    .phone-chassis.tablet-mode .dynamic-island {
      display: none;
    }
    .phone-chassis.tablet-mode .flutter-app-iframe {
      height: 608px;
      border-bottom-left-radius: 22px;
      border-bottom-right-radius: 22px;
    }
    .device-mode-toggle {
      display: inline-flex;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 9999px;
      padding: 2px;
      gap: 2px;
    }
    .device-mode-btn {
      background: transparent;
      border: none;
      color: #94A3B8;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 9999px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }
    .device-mode-btn:hover {
      color: #FFFFFF;
    }
    .device-mode-btn.active {
      background: #0052FF;
      color: #FFFFFF;
      box-shadow: 0 0 10px rgba(0, 82, 255, 0.4);
    }
"""

target_css = '    /* Live Interactive Prototype Frame */'
assert target_css in text
text = text.replace(target_css, tablet_css + '\n' + target_css, 1)

# 2. Add device toggle buttons in nav-right
target_nav = '<div class="proto-nav-right">'
device_buttons = '''<div class="proto-nav-right">
      <div class="device-mode-toggle" title="디바이스 뷰포트 전환">
        <button class="device-mode-btn active" id="btn-mode-tablet" data-device="tablet">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="12" cy="16" r="1"/></svg>
          <span>태블릿 키오스크</span>
        </button>
        <button class="device-mode-btn" id="btn-mode-phone" data-device="phone">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="5" y="2" width="14" height="20" rx="3"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
          <span>모바일 폰</span>
        </button>
      </div>'''

assert target_nav in text
text = text.replace(target_nav, device_buttons, 1)

# 3. Add JS device mode handling and auto tablet scaling
js_target = '        const chassisH = 866; // 844px screen + 22px border\n        const chassisW = 412; // 390px screen + 22px border'

js_replacement = '''        const isTablet = chassis.classList.contains('tablet-mode');
        const chassisH = isTablet ? 640 : 866;
        const chassisW = isTablet ? 960 : 412;'''

assert js_target in text
text = text.replace(js_target, js_replacement, 1)

# 4. Bind device toggle events in JS
js_events_target = '      // Check URL search parameters on initial load'

js_events_code = '''      // Device Chassis Mode Switcher (Tablet Kiosk vs Phone)
      const chassis = document.getElementById('phone-chassis');
      const btnModeTablet = document.getElementById('btn-mode-tablet');
      const btnModePhone = document.getElementById('btn-mode-phone');

      function setDeviceMode(mode) {
        if (mode === 'tablet') {
          chassis.classList.add('tablet-mode');
          btnModeTablet.classList.add('active');
          btnModePhone.classList.remove('active');
        } else {
          chassis.classList.remove('tablet-mode');
          btnModePhone.classList.add('active');
          btnModeTablet.classList.remove('active');
        }
        updateDeviceScale();
      }

      if (btnModeTablet && btnModePhone) {
        btnModeTablet.addEventListener('click', () => setDeviceMode('tablet'));
        btnModePhone.addEventListener('click', () => setDeviceMode('phone'));
      }

      // Check URL search parameters on initial load'''

assert js_events_target in text
text = text.replace(js_events_target, js_events_code, 1)

# 5. Automatically set tablet mode when kiosk flow is active
js_flow_target = '''        pills.forEach(pill => {
          pill.classList.toggle('active', pill.getAttribute('data-flow') === flow);
        });'''

js_flow_replacement = '''        pills.forEach(pill => {
          pill.classList.toggle('active', pill.getAttribute('data-flow') === flow);
        });

        // Automatically switch chassis to Tablet for Kiosk flow
        if (flow === 'kiosk') {
          setDeviceMode('tablet');
        } else {
          setDeviceMode('phone');
        }'''

assert js_flow_target in text
text = text.replace(js_flow_target, js_flow_replacement, 1)

with open('zeropass/prototype.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated zeropass/prototype.html successfully!')

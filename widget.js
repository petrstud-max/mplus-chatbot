/**
 * Mplus Czechia AI Chatbot Widget
 *
 * Vložte tento kód na libovolnou stránku před </body>:
 *
 * <script src="https://mplus-chatbot.onrender.com/widget.js"></script>
 *
 * Nebo zkopírujte celý obsah tohoto souboru do <script> tagu.
 */
(function() {
    var CHATBOT_URL = 'https://mplus-chatbot.onrender.com';

    // Vytvořit tlačítko
    var btn = document.createElement('div');
    btn.id = 'mplus-chat-btn';
    btn.innerHTML = '💬';
    btn.style.cssText = 'position:fixed;bottom:24px;right:24px;width:60px;height:60px;background:#002856;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;box-shadow:0 4px 16px rgba(0,0,0,0.3);z-index:99999;transition:transform 0.2s;border:2px solid #FFC600;';
    btn.onmouseenter = function() { btn.style.transform = 'scale(1.1)'; };
    btn.onmouseleave = function() { btn.style.transform = 'scale(1)'; };

    // Vytvořit iframe kontejner
    var wrap = document.createElement('div');
    wrap.id = 'mplus-chat-wrap';
    wrap.style.cssText = 'position:fixed;bottom:96px;right:24px;width:400px;height:580px;border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.4);z-index:99999;display:none;border:2px solid #FFC600;';

    var iframe = document.createElement('iframe');
    iframe.src = CHATBOT_URL;
    iframe.style.cssText = 'width:100%;height:100%;border:none;';
    wrap.appendChild(iframe);

    // Přidat na stránku
    document.body.appendChild(btn);
    document.body.appendChild(wrap);

    // Toggle
    var open = false;
    btn.onclick = function() {
        open = !open;
        wrap.style.display = open ? 'block' : 'none';
        btn.innerHTML = open ? '✕' : '💬';
        btn.style.background = open ? '#FF4438' : '#002856';
    };

    // Responzivní na mobilu
    if (window.innerWidth < 500) {
        wrap.style.width = 'calc(100vw - 24px)';
        wrap.style.height = 'calc(100vh - 120px)';
        wrap.style.right = '12px';
        wrap.style.bottom = '84px';
    }
})();

import os
import base64
import io
from PIL import Image
import random
import glob

# Paths
BASE_DIR = "A pics"
BG_DIR = os.path.join(BASE_DIR, "Backgrounds")
CHAR_DIR = os.path.join(BASE_DIR, "Characters")
ITEM_DIR = os.path.join(BASE_DIR, "Items")

# Configuration
BG_MAX_SIZE = (1920, 1080)
CHAR_MAX_SIZE = (150, 150)
ITEM_MAX_SIZE = (150, 150)

def image_to_base64(image_path, max_size):
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'LA') and image_path.lower().endswith(('.jpg', '.jpeg')):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            buffered = io.BytesIO()
            fmt = 'PNG'
            if image_path.lower().endswith(('.jpg', '.jpeg')):
                fmt = 'JPEG'
            elif image_path.lower().endswith('.webp'):
                fmt = 'WEBP'
            
            img.save(buffered, format=fmt)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            mime_type = f"image/{fmt.lower()}"
            return f"data:{mime_type};base64,{img_str}"
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def find_files(directory):
    files = []
    extensions = ['*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.webp', '*.WEBP']
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
    return sorted(list(set(files)))

def find_file_by_name(all_files, partial_name):
    for f in all_files:
        if partial_name in os.path.basename(f):
            return f
    return None

def main():
    print("Scanning files...")
    all_files = find_files(BASE_DIR) + find_files(BG_DIR) + find_files(CHAR_DIR) + find_files(ITEM_DIR)
    
    # Identify specific files
    bg_4210 = find_file_by_name(all_files, "IMG_4210")
    bg_4214 = find_file_by_name(all_files, "IMG_4214")
    bg_4211 = find_file_by_name(all_files, "IMG_4211")
    bg_4209 = find_file_by_name(all_files, "IMG_4209")
    bg_4212 = find_file_by_name(all_files, "IMG_4212")
    bg_image = find_file_by_name(all_files, "Image.png")
    bg_leopard = find_file_by_name(all_files, "leopard")
    
    if not all([bg_4210, bg_4214, bg_4211, bg_4209, bg_4212]):
        print("WARNING: Some required backgrounds were not found!")
    
    # Convert specific backgrounds
    b64_4210 = image_to_base64(bg_4210, BG_MAX_SIZE) if bg_4210 else ""
    b64_4214 = image_to_base64(bg_4214, BG_MAX_SIZE) if bg_4214 else ""
    b64_4211 = image_to_base64(bg_4211, BG_MAX_SIZE) if bg_4211 else ""
    b64_4209 = image_to_base64(bg_4209, BG_MAX_SIZE) if bg_4209 else ""
    b64_4212 = image_to_base64(bg_4212, BG_MAX_SIZE) if bg_4212 else ""
    b64_image = image_to_base64(bg_image, BG_MAX_SIZE) if bg_image else ""
    b64_leopard = image_to_base64(bg_leopard, BG_MAX_SIZE) if bg_leopard else ""
    
    # Process Characters & Items for scattering
    char_files = find_files(CHAR_DIR)
    item_files = find_files(ITEM_DIR)
    
    # Remove bg_4214 from scatterable items if present
    if bg_4214 and bg_4214 in item_files:
        item_files.remove(bg_4214)
        
    scatter_assets = []
    for f in char_files + item_files:
        b64 = image_to_base64(f, CHAR_MAX_SIZE)
        if b64: scatter_assets.append(b64)
    
    print("Generating HTML...")
    
    # JS variables
    js_scatter = str(scatter_assets)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>To Allysa</title>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="To Allysa">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap');
        
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #000;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        }}
        #scene {{
            position: relative;
            width: 100%;
            height: 100%;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            transition: opacity 0.5s ease-in-out;
        }}
        .scatter-obj {{
            position: absolute;
            transition: transform 0.3s ease;
            cursor: pointer;
            filter: drop-shadow(2px 2px 5px rgba(0,0,0,0.3));
            max-width: 15vh; /* Responsive size */
            max-height: 15vh;
            z-index: 10;
        }}
        .scatter-obj:hover {{
            transform: scale(1.1) rotate(5deg);
            z-index: 20;
        }}
        #text-layer {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60%;
            text-align: center;
            z-index: 50;
            background: rgba(255, 255, 255, 0.85);
            padding: 40px;
            border-radius: 8px; /* Slightly curved, more rectangular */
            box-shadow: 0 0 30px rgba(255, 105, 180, 0.6);
        }}
        #main-text {{
            color: #ff4d4d;
            font-size: 2.2em;
            line-height: 1.5;
            margin: 0 0 20px 0;
        }}
        .modern-font {{
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700;
        }}
        .sub-note {{
            font-size: 1.2em;
            color: #555;
            margin-top: 20px;
            font-family: 'Montserrat', sans-serif;
        }}
        #ui-layer {{
            position: absolute;
            bottom: 30px;
            width: 100%;
            text-align: center;
            z-index: 100;
        }}
        .btn {{
            background-color: #ff4d4d;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 24px;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(255, 77, 77, 0.4);
            transition: all 0.3s ease;
            margin: 0 15px;
            font-family: inherit;
        }}
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 77, 77, 0.6);
        }}
        #proposal-buttons {{
            display: none;
            margin-top: 30px;
        }}
        /* Page 2 Specifics */
        .page2-bg {{
            background-color: black !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }}
    </style>
</head>
<body>

<div id="scene">
    <!-- Scattered items will be injected here -->
        <div id="text-layer">
            <div id="text-content">
                <p id="main-text"></p>
                <p id="choice-note" class="sub-note" style="display:none; font-size: 0.95em;"></p>
            </div>
            <div id="proposal-buttons">
                <button class="btn" onclick="acceptProposal()">YES!</button>
                <button class="btn" id="no-btn" onclick="rejectProposal()">No</button>
            </div>
    </div>
</div>

<div id="ui-layer">
    <button class="btn" id="next-btn" onclick="nextPage()">Next</button>
</div>

        <script>
            const scatterAssets = {js_scatter};
            const decisionWebhook = '';
            const isiOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
            const inStandalone = window.navigator.standalone === true;
            const inSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
            
            // Page Configuration
            const pages = [
        {{
            bg: '{b64_4209}',
            text: "To Allysa:",
            type: 'normal',
            scatter: true
        }},
        {{
            bg: '{b64_4210}',
            text: "Everything you do like idk, creates another spark inside of me like sorta kinda.",
            type: 'normal',
            scatter: true
        }},
        {{
            bg: '{b64_4214}',
            text: "",
            type: 'special', // Black BG, Contain, No text
            scatter: false
        }},
        {{
            bg: '{b64_4211}',
            text: "No matter how big or small, I really do appreciate your actions. They haven't gone unnoticed at all. I'd never want to put too much pressure on you (eventhough it's kinda hard to hide the lovergirl inside of me soz).<br><br>Genuinely, I want you to be comfortable, yourself and take whatever time you need for anything. I just wanted to make this gesture to you because I feel that I can show my appreciation to you a bit more.<br><br>I guess what I want to ask you is:",
            type: 'normal',
            scatter: true
        }},
        {{
            bg: '{b64_leopard}',
            text: "Ally, Will You Be My Valentine?",
            type: 'proposal',
            scatter: true
        }}
                ];
            
                let currentPage = 0;
            
            function sendDecision(decision) {{
                if (!decisionWebhook) return;
                const payload = {{
                    decision,
                    timestamp: new Date().toISOString(),
                    title: document.title,
                    ua: navigator.userAgent
                }};
                try {{
                    const blob = new Blob([JSON.stringify(payload)], {{ type: 'application/json' }});
                    const ok = navigator.sendBeacon(decisionWebhook, blob);
                    if (!ok) {{
                        fetch(decisionWebhook, {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(payload)
                        }}).catch(() => {{}});
                    }}
                }} catch (e) {{
                    fetch(decisionWebhook, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }}).catch(() => {{}});
                }}
            }}
            
                function init() {{
                    if (isiOS && !inSafari && !inStandalone) {{
                        const note = document.createElement('div');
                        note.style.position = 'fixed';
                        note.style.top = '10px';
                        note.style.right = '10px';
                        note.style.background = 'rgba(255,255,255,0.9)';
                        note.style.color = '#333';
                        note.style.padding = '8px 12px';
                        note.style.borderRadius = '8px';
                        note.style.boxShadow = '0 2px 12px rgba(0,0,0,0.15)';
                        note.style.zIndex = '9999';
                        note.style.fontFamily = 'Montserrat, sans-serif';
                        note.style.fontSize = '12px';
                        note.textContent = 'If opened in Files, tap Share → Open in Safari for best experience.';
                        document.body.appendChild(note);
                        setTimeout(() => note.remove(), 6000);
                    }}
                    renderPage();
                }}

    function renderPage() {{
        const scene = document.getElementById('scene');
        const textLayer = document.getElementById('text-layer');
        const mainText = document.getElementById('main-text');
        const nextBtn = document.getElementById('next-btn');
        const propBtns = document.getElementById('proposal-buttons');
        
        // Clear previous scattered items
        document.querySelectorAll('.scatter-obj').forEach(el => el.remove());
        
        const page = pages[currentPage];
        
        // Background Logic
        scene.style.backgroundImage = `url('${{page.bg}}')`;
        if (page.type === 'special') {{
            scene.className = 'page2-bg';
            textLayer.style.display = 'none'; // No text box on page 2
        }} else {{
            scene.className = ''; // Reset
            scene.style.backgroundSize = 'cover';
            textLayer.style.display = 'block';
        }}
        
        // Text Logic
        mainText.innerHTML = page.text;
        
        // Proposal Logic & Modern Font
        if (page.type === 'proposal') {{
            nextBtn.style.display = 'none';
            propBtns.style.display = 'block';
            mainText.classList.add('modern-font');
            const choiceNote = document.getElementById('choice-note');
            if (choiceNote) {{
                choiceNote.style.display = 'block';
                choiceNote.innerText = "Whatever you choose, I'm really glad I met you.";
            }}
        }} else {{
            nextBtn.style.display = 'inline-block';
            propBtns.style.display = 'none';
            mainText.classList.remove('modern-font');
            const choiceNote = document.getElementById('choice-note');
            if (choiceNote) {{
                choiceNote.style.display = 'none';
                choiceNote.innerText = '';
            }}
        }}
        
        // Scatter Logic
        if (page.scatter) {{
            scatterItems(scene);
        }}
    }}

    function scatterItems(container) {{
        // Scatter logic: pushed to edges, no overlapping, further out
        const count = 12; 
        const shuffled = scatterAssets.sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, Math.min(count, shuffled.length));
        
        const zones = [
            // Top Edge (Left, Center, Right)
            {{l: 5, t: 5}}, {{l: 30, t: 5}}, {{l: 60, t: 5}}, {{l: 85, t: 5}},
            // Bottom Edge
            {{l: 5, t: 80}}, {{l: 30, t: 80}}, {{l: 60, t: 80}}, {{l: 85, t: 80}},
            // Left Edge (Middle)
            {{l: 2, t: 30}}, {{l: 2, t: 55}},
            // Right Edge (Middle)
            {{l: 88, t: 30}}, {{l: 88, t: 55}}
        ];
        
        zones.sort(() => 0.5 - Math.random());
        
        selected.forEach((src, i) => {{
            if (i >= zones.length) return;
            
            const img = document.createElement('img');
            img.src = src;
            img.className = 'scatter-obj';
            
            const zone = zones[i];
            
            const jitterX = (Math.random() - 0.5) * 5; 
            const jitterY = (Math.random() - 0.5) * 5; 
            
            img.style.left = (zone.l + jitterX) + '%';
            img.style.top = (zone.t + jitterY) + '%';
            
            const rot = (Math.random() - 0.5) * 60;
            img.style.transform = `rotate(${{rot}}deg)`;
            
            container.appendChild(img);
        }});
    }}

    function nextPage() {{
        currentPage++;
        if (currentPage < pages.length) {{
            renderPage();
        }}
    }}
    
                function acceptProposal() {{
                    const choiceNote = document.getElementById('choice-note');
                    if (choiceNote) choiceNote.style.display = 'none';
                    sendDecision('yes');
                    const textLayer = document.getElementById('text-layer');
                    textLayer.innerHTML = `
                        <h1 style="color: #ff4d4d; font-size: 3em; margin-bottom: 20px;" class="modern-font">YESSSS!! 🫶🏾</h1>
                        <p class="sub-note" style="font-size: 0.9em;">Can you please take a pic of this page and send it to me please, so that I know you'll let me be your Valentine? Ty xx</p>
                    `;
                    document.getElementById('next-btn').style.display = 'none';
                }}
                
                function rejectProposal() {{
                    const choiceNote = document.getElementById('choice-note');
                    if (choiceNote) choiceNote.style.display = 'none';
                    sendDecision('no');
                    alert("No worries at all, I still really appreciate you.");
                }}

    init();
</script>

</body>
</html>
    """
    
    output_path = "Ally.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Done! Created {output_path}")

if __name__ == "__main__":
    main()

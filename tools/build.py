"""Build a self-contained HTML game; no network or third-party Python packages."""
from pathlib import Path
import base64,json
root=Path(__file__).resolve().parents[1]
s=(root/'template.html').read_text()
assets='const ATLAS_URL='+json.dumps('data:image/png;base64,'+base64.b64encode((root/'assets/atlas.png').read_bytes()).decode())+';\nconst ATLAS_META='+(root/'assets/atlas.json').read_text()+';'
s=s.replace('/*__ASSETS__*/',assets).replace('/*__ANIMATIONS__*/',(root/'src/animations.js').read_text()).replace('/*__TURNS__*/',(root/'src/turns.js').read_text()).replace('/*__TACTICS__*/',(root/'src/tactics.js').read_text()).replace('/*__TOOLTIPS__*/',(root/'src/tooltips.js').read_text()).replace('/*__RELATIONS__*/',(root/'src/relations.js').read_text()).replace('/*__BESTIARY__*/',(root/'src/bestiary.js').read_text()).replace('/*__GAME__*/',(root/'src/game.js').read_text()).replace('/*__DEVELOPMENT__*/',(root/'src/development.js').read_text()).replace('/*__PAINTER__*/',(root/'src/painter.js').read_text())
lab=(root/'src/battle-lab.html').read_text().replace('/*__PIXEL_SPRITES__*/',(root/'src/pixel_sprites.js').read_text())
# srcdoc is embedded as a JS string; escape script terminators in the outer HTML.
lab_json=json.dumps(lab,ensure_ascii=False).replace('</','<\\/')
lab_module="""(()=>{let overlay=null;document.getElementById('openBattleLab').onclick=()=>{if(overlay)return;overlay=document.createElement('div');overlay.id='battleLabOverlay';overlay.style.cssText='position:fixed;inset:0;z-index:100;background:#14251f;padding-top:46px';const close=document.createElement('button');close.textContent='← Вернуться к игре';close.style.cssText='position:absolute;top:5px;left:12px';close.onclick=()=>{overlay.remove();overlay=null};const frame=document.createElement('iframe');frame.title='Пробный бой 4 на 4';frame.style.cssText='width:100%;height:100%;border:0';frame.srcdoc=__LAB__;overlay.append(close,frame);document.body.append(overlay)}})();""".replace('__LAB__',lab_json)
s=s.replace('/*__BATTLE_LAB__*/',lab_module)
(root/'battle-lab.html').write_text(lab)
(root/'index.html').write_text(s)
print('Built index.html:',len(s.encode()),'bytes')

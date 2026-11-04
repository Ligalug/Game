"""Create a self-contained browser download/folder-save page from a ZIP."""
from pathlib import Path
import argparse,base64,hashlib,html,json
p=argparse.ArgumentParser()
p.add_argument('archive',type=Path)
p.add_argument('output',type=Path)
p.add_argument('--version',default='0.7')
a=p.parse_args()
data=a.archive.read_bytes()
digest=hashlib.sha256(data).hexdigest()
s=(Path(__file__).with_name('backup_page_template.html')).read_text(encoding='utf-8')
name='Game-backup-'+a.version+'-'+digest[:8]+'.zip'
values={'__FILENAME__':json.dumps(name).replace('<','\\u003c')[1:-1],'__VERSION__':html.escape(a.version),'__ARCHIVE64__':base64.b64encode(data).decode(),'__HASH__':digest,'__SIZE__':str(round(len(data)/1024/1024,2))}
for key,value in values.items():s=s.replace(key,value)
a.output.write_text(s,encoding='utf-8')
print('Backup page:',a.output,'ZIP SHA-256:',digest)

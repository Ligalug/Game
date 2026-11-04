"""Verify the repository snapshot without dependencies or network access."""
from pathlib import Path
import hashlib
import sys
root=Path(__file__).resolve().parents[1]
manifest=root/'BACKUP_SHA256SUMS.txt'
if not manifest.is_file():
    sys.exit('Missing BACKUP_SHA256SUMS.txt')
failed=[]
count=0
for line in manifest.read_text().splitlines():
    expected,name=line.split('  ',1)
    path=(root/name).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        failed.append(name+': missing or invalid path')
        continue
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    count+=1
    if actual!=expected:
        failed.append(name+': SHA-256 mismatch')
for error in failed:
    print(error)
print(f'Checked {count} files; failures: {len(failed)}')
sys.exit(1 if failed else 0)

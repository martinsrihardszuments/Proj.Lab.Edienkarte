"""
Izveido projekta struktūras kopsavilkumu
"""
import os
from pathlib import Path
from datetime import datetime

def get_file_info(file_path):
    """Iegūst faila informāciju"""
    try:
        stat = file_path.stat()
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime)
        }
    except:
        return None

def should_skip(path):
    """Pārbauda, vai vajag izlaist"""
    skip = [
        '__pycache__', '.pyc', '.pyo', '.pyd',
        '.db', '.sqlite3', '.env', 'node_modules',
        '.git', '.venv', 'venv', '*.log', '*.tmp',
        'PROJEKTA_VISI_FAILI_', 'export_', 'check_'
    ]
    path_str = str(path).lower()
    return any(pattern in path_str for pattern in skip)

def export_structure():
    """Eksportē projekta struktūru"""
    project_root = Path(__file__).parent
    output_file = project_root / f"PROJEKTA_STRUKTURA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    files_list = []
    total_size = 0
    
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not should_skip(Path(root) / d)]
        
        for file in files:
            file_path = Path(root) / file
            if should_skip(file_path):
                continue
            
            info = get_file_info(file_path)
            if info:
                rel_path = file_path.relative_to(project_root)
                files_list.append({
                    'path': rel_path,
                    'size': info['size'],
                    'modified': info['modified']
                })
                total_size += info['size']
    
    # Kārto pēc ceļa
    files_list.sort(key=lambda x: str(x['path']))
    
    # Raksta failā
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("=" * 80 + "\n")
        out.write("PROJEKTA STRUKTURA UN FAILU SARAKSTS\n")
        out.write("=" * 80 + "\n")
        out.write(f"Izveidots: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"Projekta mape: {project_root}\n")
        out.write(f"Kopa failu: {len(files_list)}\n")
        out.write(f"Kopejais izmers: {total_size/1024:.2f} KB\n")
        out.write("=" * 80 + "\n\n")
        
        # Grupē pēc mapēm
        current_dir = None
        for file_info in files_list:
            path = file_info['path']
            dir_path = path.parent
            
            if dir_path != current_dir:
                current_dir = dir_path
                out.write(f"\n[{current_dir if current_dir != Path('.') else 'ROOT'}]\n")
                out.write("-" * 80 + "\n")
            
            size_kb = file_info['size'] / 1024
            out.write(f"  {path.name:<50} {size_kb:>8.2f} KB  {file_info['modified'].strftime('%Y-%m-%d %H:%M')}\n")
        
        out.write("\n" + "=" * 80 + "\n")
        out.write("STRUKTURA PABEIGTA\n")
        out.write("=" * 80 + "\n")
    
    print(f"[OK] Struktura eksporteta")
    print(f"Fails: {output_file}")
    print(f"Failu skaits: {len(files_list)}")
    print(f"Kopejais izmers: {total_size/1024:.2f} KB")
    
    return output_file

if __name__ == "__main__":
    export_structure()

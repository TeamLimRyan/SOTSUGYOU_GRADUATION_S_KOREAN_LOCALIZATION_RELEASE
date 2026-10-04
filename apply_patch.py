"""Graduation S Korean v1.0 installer. Source CHD is read-only."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(4*1024*1024):h.update(b)
    return h.hexdigest()
def tool(value):
    p=Path(value)
    if p.is_file():return str(p.resolve())
    result=shutil.which(value)
    if not result:raise ValueError('Required tool not found: '+value)
    return result
def install(args):
    package=Path(__file__).resolve().parent;m=json.loads((package/'manifest.json').read_text(encoding='utf8'));source=Path(args.source).resolve();dest=Path(args.output).resolve()
    if dest.exists():raise ValueError('Output already exists. Choose a new folder; no existing files are overwritten.')
    if not source.is_file() or source.stat().st_size!=m['source']['bytes'] or sha(source)!=m['source']['sha256']:raise ValueError('Wrong source CHD. Required T-20103G V1.001 and the exact SHA-256 in README.')
    chdman=tool(args.chdman);xd=tool(args.xdelta or str(package/'xdelta3.exe') if os.name=='nt' else args.xdelta or 'xdelta3')
    patch=package/m['patch']['path']
    if sha(patch)!=m['patch']['sha256']:raise ValueError('Patch checksum mismatch')
    dest.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix='.grad-ko-v1-',dir=dest.parent));diagnostic=dict(version='1.0',source_sha256=m['source']['sha256'],steps=[])
    try:
        def run(argv):
            p=subprocess.run(argv,capture_output=True,text=True,errors='replace');diagnostic['steps'].append(dict(command=argv,exit_code=p.returncode))
            if p.returncode:raise RuntimeError(p.stderr[-2000:] or p.stdout[-2000:])
        print('1/3 Extracting original CHD...',flush=True)
        run([chdman,'extractcd','-i',str(source),'-o',str(tmp/'original.cue'),'-ob',str(tmp/'original (Track %t).bin'),'-sb'])
        tracks=sorted(tmp.glob('original (Track *).bin'),key=lambda p:int(p.stem.split('Track ')[1].rstrip(')')))
        if len(tracks)!=9:raise RuntimeError('Expected 9 split tracks from chdman')
        for p,row in zip(tracks,m['tracks']):
            if p.stat().st_size!=row['bytes'] or sha(p)!=row['source_sha256']:raise RuntimeError('Extracted source track mismatch: '+p.name)
        print('2/3 Applying xdelta...',flush=True)
        out=tmp/'output';out.mkdir();run([xd,'-d','-s',str(tracks[0]),str(patch),str(out/'track01.bin')])
        for i,p in enumerate(tracks[1:],2):shutil.move(str(p),out/f'track{i:02}.bin')
        print('3/3 Verifying all 9 output tracks...',flush=True)
        for i,row in enumerate(m['tracks'],1):
            if sha(out/f'track{i:02}.bin')!=row['target_sha256']:raise RuntimeError('Output checksum mismatch')
        (out/'Graduation_S_Korean_v1.0.cue').write_text(m['cue'],encoding='ascii',newline='\n')
        diagnostic['status']='PASS';(out/'installation.json').write_text(json.dumps(diagnostic,indent=2),encoding='utf8');out.rename(dest)
        print('Complete: '+str(dest/'Graduation_S_Korean_v1.0.cue'))
    finally:shutil.rmtree(tmp)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('source',help='Original CHD');ap.add_argument('output',help='New output directory');ap.add_argument('--chdman',default='chdman');ap.add_argument('--xdelta');a=ap.parse_args()
    try:install(a)
    except Exception as e:print('ERROR: '+str(e),file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())

import http.client
import http.server
import json
import sys
import threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from iter_sync import LiveBoardHandler


def serve(directory):
    handler=type('BoundHandler',(LiveBoardHandler,),{'iter_dir':directory})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    return server,thread


def request(server,path,headers=None):
    c=http.client.HTTPConnection('127.0.0.1',server.server_address[1]);c.request('GET',path,headers=headers or {})
    r=c.getresponse();result=(r.status,dict(r.getheaders()),r.read());c.close();return result


def test_board_api_no_cors_or_project_writes(tmp_path):
    (tmp_path/'01.md').write_text('---\nstatus: DONE\n---\n',encoding='utf-8')
    before={p.name:p.read_bytes() for p in tmp_path.iterdir()}
    server,thread=serve(tmp_path)
    try:
        status,headers,body=request(server,'/api/board')
        assert status==200 and json.loads(body)['done']==1
        assert 'Access-Control-Allow-Origin' not in headers
        assert before=={p.name:p.read_bytes() for p in tmp_path.iterdir()}
        assert request(server,'/api/board',{'Host':'evil.example'})[0]==403
        assert request(server,'/api/board',{'Origin':'https://evil.example'})[0]==403
    finally:
        server.shutdown();server.server_close();thread.join()


def test_listed_evidence_can_be_read_but_not_arbitrary_files(tmp_path):
    (tmp_path/'receipt.json').write_text(json.dumps({'review_report':'report.txt','checks':[]}),encoding='utf-8')
    (tmp_path/'report.txt').write_text('independent findings',encoding='utf-8')
    (tmp_path/'private.txt').write_text('not listed',encoding='utf-8')
    (tmp_path/'01.md').write_text('---\nstatus: DONE\nreview_receipt: receipt.json\n---\n',encoding='utf-8')
    server,thread=serve(tmp_path)
    try:
        status,_,body=request(server,'/api/evidence?task=01.md&source=1')
        assert status==200 and body==b'independent findings'
        assert request(server,'/api/evidence?task=../private.txt&source=0')[0]==404
        assert request(server,'/api/evidence?task=01.md&source=999')[0]==404
    finally:
        server.shutdown();server.server_close();thread.join()


def test_http_symlink_escape_and_unlisted_routes_are_rejected(tmp_path):
    outside=tmp_path.parent/(tmp_path.name+'-private.txt')
    outside.write_text('secret outside project',encoding='utf-8')
    link=tmp_path/'escape.txt'
    # Creation failure is an explicit unverified gate, not a passing skip.
    link.symlink_to(outside)
    (tmp_path/'receipt.json').write_text(json.dumps({'review_report':'escape.txt','checks':[]}),encoding='utf-8')
    (tmp_path/'01.md').write_text('---\nstatus: TODO\nreview_receipt: receipt.json\n---\n',encoding='utf-8')
    server,thread=serve(tmp_path)
    try:
        status,_,body=request(server,'/api/board')
        assert status==200 and b'secret outside project' not in body
        assert all(s['path']!='escape.txt' for s in json.loads(body)['cards'][0]['sources'])
        for route in ('/escape.txt','/receipt.json','/api/evidence?task=01.md&source=1',
                      '/api/evidence?path=escape.txt','/api/evidence?task=01.md&source=-1'):
            status,_,body=request(server,route)
            assert status==404 and b'secret outside project' not in body
    finally:
        server.shutdown();server.server_close();thread.join()

import os
from flask import Flask, redirect, request, session, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY','change-me-before-production')
CLIENT_FILE = os.environ.get('GOOGLE_CLIENT_SECRET','client_secret.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

@app.get('/health')
def health(): return {'ok': True, 'mode': 'protected-readonly'}

@app.get('/auth/google')
def auth_google():
    flow = Flow.from_client_secrets_file(CLIENT_FILE, scopes=SCOPES, redirect_uri=request.url_root.rstrip('/') + '/oauth2/callback')
    url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='consent')
    session['state'] = state
    return redirect(url)

@app.get('/oauth2/callback')
def callback():
    flow = Flow.from_client_secrets_file(CLIENT_FILE, scopes=SCOPES, state=session.get('state'), redirect_uri=request.url_root.rstrip('/') + '/oauth2/callback')
    flow.fetch_token(authorization_response=request.url)
    c = flow.credentials
    session['credentials'] = {'token':c.token,'refresh_token':c.refresh_token,'token_uri':c.token_uri,'client_id':c.client_id,'client_secret':c.client_secret,'scopes':c.scopes}
    return redirect('/api/messages')

def gmail():
    d=session.get('credentials')
    if not d: return None
    return build('gmail','v1',credentials=Credentials(**d),cache_discovery=False)

@app.get('/api/messages')
def messages():
    svc=gmail()
    if not svc: return jsonify({'connected':False,'login':'/auth/google'}),401
    rows=svc.users().messages().list(userId='me',maxResults=20).execute().get('messages',[])
    out=[]
    for row in rows:
        m=svc.users().messages().get(userId='me',id=row['id'],format='metadata',metadataHeaders=['From','Subject','Date']).execute()
        h={x['name'].lower():x['value'] for x in m.get('payload',{}).get('headers',[])}
        out.append({'id':m['id'],'from':h.get('from',''),'subject':h.get('subject','(senza oggetto)'),'date':h.get('date',''),'snippet':m.get('snippet','')})
    return {'connected':True,'messages':out,'mode':'readonly'}

@app.post('/logout')
def logout(): session.clear(); return {'ok':True}

if __name__ == '__main__': app.run(host='127.0.0.1',port=8080,debug=False)

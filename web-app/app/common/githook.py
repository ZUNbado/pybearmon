from git import Repo
import os.path

def update_repo(path = None, remote = 'origin', restart = True, reload_file = None):
    if not path: path = os.path.dirname(os.path.abspath(os.path.join(__file__,'../../')))
    if not reload_file: reload_file = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__,'../../'))), 'UWSGI_RELOAD') 
    repo = Repo(path)
    try:
        repo.remote(remote).pull()
        updated = True
    except:
        updated = False

    restarted = False
    if updated and restart:
        try:
            open(reload_file, 'w').close()
            restarted = True
        except:
            pass

    return dict( updated = updated, restarted = restarted )

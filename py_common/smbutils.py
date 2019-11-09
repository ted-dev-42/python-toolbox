from __future__ import print_function
import shutil
import urllib2
from smb.SMBHandler import SMBHandler


class SmbFile(object):

    def __init__(self, smb_file_url):
        self._smb_file_url = smb_file_url
        self._user = ""
        self._pwd = ""
        self._domain = None
        self._server = None
        self._remote_dir = None
        self._remote_file = None
        self._parse_url(smb_file_url)
        pass

    """
        smb://domain;username:password@server_ip/share/path/subplan.xml
    """
    def _parse_url(self, smb_url):
        """
        :type smb_url: string
        """
        pass

    def get(self, lpath):
        fh = None
        try:
            director = urllib2.build_opener(SMBHandler)
            fh = director.open(self._smb_file_url)
            with open(lpath, 'w+') as fdest:
                shutil.copyfileobj(fh, fdest)
        except Exception as e:
            print("exception when get file from smb: " + str(e))
            import traceback
            traceback.print_exc()
        finally:
            if fh is not None:
                fh.close()

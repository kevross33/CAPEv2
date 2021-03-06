# CAPE - Config And Payload Extraction
# Copyright(C) 2015-2017 Context Information Security. (kevin.oreilly@contextis.com)
# See the file 'docs/LICENSE' for copying permission.

from __future__ import absolute_import
import os
import shutil

from lib.common.abstracts import Package

class Ursnif(Package):
    """Ursnif config extraction package."""
    PATHS = [
        ("SystemRoot", "system32", "rundll32.exe"),
    ]

    def __init__(self, options={}, config=None):
        """@param options: options dict."""
        self.config = config
        self.options = options
        self.options["dll"] = "Ursnif.dll"
        self.options["dll_64"] = "Ursnif_x64.dll"
        self.options["exclude-apis"] = "NtCreateFile:NtWriteFile:NtDeleteFile:NtQueryInformationFile"
        
    def start(self, path):
        args = self.options.get("arguments")
        appdata = self.options.get("appdata")
        runasx86 = self.options.get("runasx86")
        
        # If the file doesn't have an extension, add .exe
        # See CWinApp::SetCurrentHandles(), it will throw
        # an exception that will crash the app if it does
        # not find an extension on the main exe's filename
        if "." not in os.path.basename(path):
            new_path = path + ".exe"
            os.rename(path, new_path)
            path = new_path

        if appdata:
            # run the executable from the APPDATA directory, required for some malware
            basepath = os.getenv('APPDATA')
            newpath = os.path.join(basepath, os.path.basename(path))
            shutil.copy(path, newpath)
            path = newpath
        if runasx86:
            # ignore the return value, user must have CorFlags.exe installed in the guest VM
            call(["CorFlags.exe", path, "/32bit+"])
        return self.execute(path, args, path)    

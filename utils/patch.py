def patch_selenium():
    try:
        from StringIO import StringIO as IOStream
    except ImportError:  # 3+
        from io import BytesIO as IOStream
    from selenium.webdriver.remote.command import Command
    import base64
    import os
    import zipfile

    from selenium.common.exceptions import WebDriverException

    import selenium

    def _upload(self, filename):
        fp = IOStream()
        zipped = zipfile.ZipFile(fp, "w", zipfile.ZIP_DEFLATED)
        zipped.write(filename, os.path.split(filename)[1])
        zipped.close()
        content = base64.encodebytes(fp.getvalue())
        if not isinstance(content, str):
            content = content.decode("utf-8")
        try:
            return self._execute(Command.UPLOAD_FILE, {"file": content})["value"]
        except WebDriverException as e:
            if "Unrecognized command: POST" in e.__str__():
                return filename
            elif "Command not found: POST " in e.__str__():
                return filename
            elif '{"status":405,"value":["GET","HEAD","DELETE"]}' in e.__str__():
                return filename
            else:
                raise e

    selenium.webdriver.remote.webelement.WebElement._upload = _upload

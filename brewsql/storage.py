from qiniustorage.backends import QiniuStorage


class ImageStorage(QiniuStorage):

    def _clean_name(self, name):
        import os
        import time
        import random
        import re

        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        clean_name = name.replace(d, '').replace(ext, '').replace('/', '')
        if len(clean_name) == 16:
            match_obj = re.match(r'^20[0-9]{2}[0-1][0-9][0-3][0-9][0-2][0-9][0-6][0-9][0-6][0-9]{3}', clean_name)
            if match_obj:
                return name
            else:
                return os.path.join(d, '{0}{1}{2}'.format(time.strftime('%Y%m%d%H%M%S'), random.randint(0, 100), ext))
        else:
            return os.path.join(d, '{0}{1}{2}'.format(time.strftime('%Y%m%d%H%M%S'), random.randint(0, 100), ext))

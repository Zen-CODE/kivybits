"""
A helper class for providing Operating specific functionality.
"""

from kivy.utils import platform


class OS(object):
    """
    A convenience class for handling OS specific sunctionality.
    """

    @staticmethod
    def get_user_path():
        """
        Return a path that is writable by the current process and can
        be used to store app data.
        """

        if platform == "android":
            from jnius import autoclass, cast
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Environment = autoclass('android.os.Environment')
            context = cast('android.content.Context', PythonActivity.mActivity)
            ret = context.getExternalFilesDir(
                Environment.getDataDirectory().getAbsolutePath()
            ).getAbsolutePath()
        else:
            from os import path

            root = path.expanduser("~")
            if platform == "ios":
                # iOS does not seems to allow for sub-folder creation?
                # Documents seems to the the place to put it
                # https://groups.google.com/forum/#!topic/kivy-users/sQXAOecthmE
                ret = path.join(root, "Documents")
            else:
                ret = path.join(root, ".KivyServices")
        return ret


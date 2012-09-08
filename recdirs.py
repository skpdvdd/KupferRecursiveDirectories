
import os
from kupfer.objects import Source
from kupfer.obj.objects import ConstructFileLeaf
from kupfer import plugin_support

__kupfer_name__ = _("Recursive Directories")
__kupfer_sources__ = ("RecursiveDirectorySource", )
__kupfer_text_sources__ = ()
__kupfer_actions__ = ()
__description__ = _("Provides recursive directory access")
__version__ = "0.1"
__author__ = "Christopher Pramerdorfer"

__kupfer_settings__ = plugin_support.PluginSettings(
    {
        'key': 'dirs',
        'label': _("Directories (;-separated):"),
        'type': str,
        'value': "~/Documents/",
    },
    {
        'key': 'blacklist',
        'label': _("Blacklist (;-separated):"),
        'type': str,
        'value': ".git",
    }
)

class RecursiveDirectorySource (Source):
    def __init__(self):
        Source.__init__(self, _("Recursive Directories"))

    def initialized(self):
        __kupfer_settings__.connect("plugin-setting-changed", self._changed)

    def get_items(self):
        return (ConstructFileLeaf(d) for d in self._get_dirs())

    def get_icon_name(self):
        return "folder"

    def get_description(self):
        return _("Recursive subdirectory access")

    def _get_dirs(self):
        rootdirs = self._get_root_dirs()
        blacklist = self._get_blacklist()
        directories = set()

        for rootdir in rootdirs:
            for root, dirs, files in os.walk(rootdir):
                directories.add(root)
                for d in dirs:
                    if os.path.basename(d) in blacklist:
                        dirs.remove(d)
        return directories

    def _get_root_dirs(self):
        if not __kupfer_settings__['dirs']:
            return []
        return filter(os.path.isdir, (os.path.expanduser(path)
            for path
            in __kupfer_settings__['dirs'].split(';')))

    def _get_blacklist(self):
        if not __kupfer_settings__['blacklist']:
            return []
        return __kupfer_settings__['blacklist'].split(';')

    def _changed(self, settings, key, value):
        if key in ('dirs', 'blacklist'):
            self.mark_for_update()
import chemfiles


class RemoveChemfilesWarnings(object):
    def __enter__(self):
        chemfiles.set_warnings_callback(lambda u: None)

    def __exit__(self, *args):
        chemfiles.misc._set_default_warning_callback()


remove_warnings = RemoveChemfilesWarnings()

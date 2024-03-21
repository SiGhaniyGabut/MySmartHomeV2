class Updater:
    """
    A class to update your MicroController with the latest version from a GitHub tagged release,
    optimized for low power usage.
    """

    def __init__(self, github_repo, github_src_dir='', module='', main_dir='main', new_version_dir='next', secrets_file=None): ...

    def check_for_update_to_install_during_next_reboot(self) -> bool:
        """Function which will check the GitHub repo if there is a newer version available.
        
        This method expects an active internet connection and will compare the current 
        version with the latest version available on GitHub.
        If a newer version is available, the file 'next/.version' will be created 
        and you need to call machine.reset(). A reset is needed as the installation process 
        takes up a lot of memory (mostly due to the http stack)
        """
        ...

    def install_update_if_available_after_boot(self) -> bool:
        """This method will install the latest version if out-of-date after boot.
        
        This method, which should be called first thing after booting, will check if the 
        next/.version' file exists. 
        """
        ...

    def install_update_if_available(self) -> bool:
        """This method will immediately install the latest version if out-of-date.
        
        This method expects an active internet connection and allows you to decide yourself
        if you want to install the latest version. It is necessary to run it directly after boot 
        (for memory reasons) and you need to restart the microcontroller if a new version is found.
        """
        ...

    def _check_for_new_version(self) -> tuple:
        """Check for new version available on GitHub.
        
        Returns
        -------
            tuple: (current_version, latest_version)
        """
        ...

    def _create_new_version_file(self, latest_version): ...

    def get_version(self, directory, version_file_name='.version') -> str:
        """Get version from directory. If not found, return '0.0'."""
        ...

    def get_latest_version(self) -> str:
        """Get latest version from GitHub."""
        ...
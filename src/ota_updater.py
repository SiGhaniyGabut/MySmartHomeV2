import os, gc
from http_client import HttpClient

GITHUB_API_URL = 'https://api.github.com'
GITHUB_RAW_URL = 'https://raw.githubusercontent.com'

class Github:
    def __init__(self, github_repo, github_src_dir='', module='', main_dir='main', new_version_dir='next', secrets_file=None):
        self.request = HttpClient()
        self.repo = github_repo.rstrip('/').replace('https://github.com/', '').replace('.git', '')
        self.src_dir = '' if len(github_src_dir) < 1 else github_src_dir.rstrip('/') + '/'
        self.module = module.rstrip('/')
        self.main_dir = main_dir
        self.new_version_dir = new_version_dir
        self.secrets_file = secrets_file

    def check_for_update_to_install_during_next_reboot(self) -> bool:
        (current_version, latest_version) = self.__check_for_new_version()
        if latest_version > current_version:
            print('New version available, will download and install on next reboot')
            self.__create_new_version_file(latest_version)
            return True

        return False

    def install_update_if_available_after_boot(self) -> bool:
        if self.new_version_dir in os.listdir(self.module):
            if '.version' in os.listdir(self._modulepath(self.new_version_dir)):
                latest_version = self.get_version(self._modulepath(self.new_version_dir), '.version')
                print('New update found: ', latest_version)
                self.install_update_if_available()

                return True
            
        print('No new updates found...')
        return False

    def install_update_if_available(self) -> bool:
        (current_version, latest_version) = self.__check_for_new_version()
        if latest_version > current_version:
            print('Updating to version {}...'.format(latest_version))
            self.__create_new_version_file(latest_version)
            self.__download_new_version(latest_version)
            self.__copy_secrets_file()
            self.__delete_old_version()
            self.__install_new_version()
            return True

        return False

    def get_version(self, directory, version_file_name='.version'):
        if version_file_name in os.listdir(directory):
            with open(directory + '/' + version_file_name) as f:
                version = f.read()
                return version
        return '0.0'

    def get_latest_version(self):
        url = f'{GITHUB_API_URL}/repos/{self.repo}/releases/latest'
        response = self.request.get(url)
        gh_json = response.json()

        if 'tag_name' not in gh_json:
            raise ValueError(
                "Release not found: \n"
                "Please ensure release as marked as 'latest', rather than pre-release \n"
                f"github api message: \n {gh_json} \n "
            )

        return gh_json['tag_name']

    # different micropython versions act differently when directory already exists
    def _mkdir(self, path:str):
        try:
            os.mkdir(path)
        except OSError as exc:
            if exc.args[0] == 17: 
                pass

    def _modulepath(self, path):
        return self.module + '/' + path if self.module else path
    
    def __check_for_new_version(self):
        current_version = self.get_version(self._modulepath(self.main_dir))
        latest_version = self.get_latest_version()

        print('Checking version... ')
        print('\tCurrent version: ', current_version)
        print('\tLatest version: ', latest_version)
        return (current_version, latest_version)

    def __create_new_version_file(self, latest_version):
        self._mkdir(self._modulepath(self.new_version_dir))
        with open(self._modulepath(self.new_version_dir + '/.version'), 'w') as version_file:
            version_file.write(latest_version)
            version_file.close()

    def __download_new_version(self, version):
        print(f'Downloading version {version}')
        self.__download_all_files(version)
        print(f'Version {version} downloaded to {self._modulepath(self.new_version_dir)}')

    def __download_all_files(self, version, sub_dir=''):
        url = f'{GITHUB_API_URL}/repos/{self.repo}/contents{self.src_dir}{self.main_dir}{sub_dir}?ref=refs/tags/{version}'
        gc.collect() 
        file_list_json = self.request.get(url).json()
        for file in file_list_json:
            path = self._modulepath(f'{self.new_version_dir}/{file["path"].replace(self.main_dir + "/", "").replace(self.src_dir, "")}')
            if file['type'] == 'file':
                git_path = file['path']
                print(f'\tDownloading: {git_path} to {path}')
                self.__download_file(version, git_path, path)
            elif file['type'] == 'dir':
                print(f'Creating dir {path}')
                self._mkdir(path)
                self.__download_all_files(version, f'{sub_dir}/{file["name"]}')
            gc.collect()

    def __download_file(self, version, git_path, path):
        url = f'{GITHUB_RAW_URL}/{self.repo}/{version}/{git_path}'
        self.request.get(url, stream=True, save_to=path)

    def __copy_secrets_file(self):
        if self.secrets_file:
            from_path = self._modulepath(f'{self.main_dir}/{self.secrets_file}')
            to_path = self._modulepath(f'{self.new_version_dir}/{self.secrets_file}')
            print(f'Copying secrets file from {from_path} to {to_path}')
            self.__copy_file(from_path, to_path)
            print(f'Copied secrets file from {from_path} to {to_path}')

    def __delete_old_version(self):
        old_version_path = self._modulepath(self.main_dir)
        print(f'Deleting old version at {old_version_path} ...')
        self.__rmtree(old_version_path)
        print(f'Deleted old version at {old_version_path} ...')

    def __install_new_version(self):
        new_version_path = self._modulepath(self.new_version_dir)
        main_dir_path = self._modulepath(self.main_dir)
        print(f'Installing new version at {main_dir_path} ...')
        if self.__os_supports_rename():
            os.rename(new_version_path, main_dir_path)
        else:
            self.__copy_directory(new_version_path, main_dir_path)
            self.__rmtree(new_version_path)
        print('Update installed, please reboot now')

    def __rmtree(self, directory):
        for entry in os.ilistdir(directory):
            is_dir = entry[1] == 0x4000  # 0x4000 is the flag for directories
            full_path = directory + '/' + entry[0]
            if is_dir:
                self.__rmtree(full_path)
            else:
                os.remove(full_path)
        os.rmdir(directory)

    def __os_supports_rename(self) -> bool:
        self.__mk_dirs('otaUpdater/osRenameTest')
        os.rename('otaUpdater', 'otaUpdated')
        result = len(os.listdir('otaUpdated')) > 0
        self.__rmtree('otaUpdated')
        return result

    def __copy_directory(self, from_path, to_path):
        if not self.__exists_dir(to_path):
            self.__mk_dirs(to_path)

        for entry in os.listdir(from_path):
            source_path = from_path + '/' + entry
            destination_path = to_path + '/' + entry

            if self.__is_dir(source_path):
                self.__copy_directory(source_path, destination_path)
            else:
                self.__copy_file(source_path, destination_path)

    def __is_dir(self, path):
        try:
            return os.stat(path)[0] == 0o040000  # 0o040000 is the flag for directories
        except OSError:
            return False


    def __copy_file(self, from_path, to_path, chunk_size=512):
        with open(from_path, 'rb') as from_file, open(to_path, 'wb') as to_file:
            while True:
                chunk = from_file.read(chunk_size)
                if chunk:
                    to_file.write(chunk)
                else:
                    break

    def __exists_dir(self, path) -> bool:
        try:
            os.listdir(path)
            return True
        except:
            return False

    def __mk_dirs(self, path: str):
        paths = path.split('/')
        path_to_create = ''
        for directory in paths:
            path_to_create += '/' + directory
            self._mkdir(path_to_create)

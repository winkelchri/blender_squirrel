import click

from utils.settings import AddonInstallerSettings
from utils.installers import ZipPluginInstaller
from utils.plugin_finders import ZipPluginFinder


@click.command()
def install():
    settings = AddonInstallerSettings()
    downloaded_addons = settings.find_downloaded_plugins()

if __name__ == "__main__":
    pass

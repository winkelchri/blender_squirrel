import click

from loguru import logger

from utils.settings import AddonInstallerSettings
from utils.plugins import ZipPlugin
from utils.plugins.validators import InvalidBlenderPlugin
# from utils.installers import ZipPluginInstaller
# from utils.plugin_finders import ZipPluginFinder


@click.group()
def cli():
    pass


@cli.command()
def install():
    settings = AddonInstallerSettings()
    plugins_paths = settings.find_downloaded_plugins()

    for plugin_path in plugins_paths:
        plugin = ZipPlugin(
            settings=settings,
            plugin_filename=plugin_path
        )
        try:
            plugin.install()
        except InvalidBlenderPlugin as e:
            click.echo(f"Skipping {plugin_path} - invalid blender plugin")


if __name__ == "__main__":
    cli()

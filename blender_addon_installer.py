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
@click.option('--cleanup', is_flag=True, help="Removes the installed file from the source directory")
def install(cleanup):
    settings = AddonInstallerSettings()
    plugins_paths = settings.find_downloaded_plugins()
    skipped_files = []
    cleaned_files = []

    for plugin_path in plugins_paths:
        plugin = ZipPlugin(
            settings=settings,
            plugin_filename=plugin_path
        )
        try:
            plugin.install()
            if cleanup is True:
                cleaned_files.append(plugin_path)
                plugin_path.unlink()
        except InvalidBlenderPlugin:
            skipped_files.append(plugin_path)

    click.echo(f"Skipped: ")
    for file in skipped_files:
        click.echo(f"- {file}")

    if cleanup is True:
        click.echo(f"Cleaned: ")
        for file in cleaned_files:
            click.echo(f"- {file}")


if __name__ == "__main__":
    cli()

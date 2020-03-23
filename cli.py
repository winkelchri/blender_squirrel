import click

from loguru import logger

from squirrel.settings import AddonInstallerSettings
from squirrel.addons import ZipAddon
from squirrel.validators import InvalidBlenderAddon


SETTINGS = AddonInstallerSettings()
ADDON_PATHS = SETTINGS.find_downloaded_addons()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--cleanup', is_flag=True, help="Removes the installed file from the source directory")
@click.option('-v', '--verbose', count=True)
def install(cleanup, verbose):
    ''' Installs manually downloaded addons. '''

    skipped_files = []
    cleaned_files = []

    if verbose:
        logger.level('DEBUG')
    else:
        logger.level('WARNING')

    for addon_path in ADDON_PATHS:
        addon = ZipAddon(
            settings=SETTINGS,
            addon_filename=addon_path
        )

        try:
            addon.install()
            if cleanup is True:
                cleaned_files.append(addon_path)
                addon_path.unlink()
        except InvalidBlenderAddon:
            skipped_files.append(addon_path)
        except NotImplementedError:
            click.echo(
                f"Currently unsupported blender addon format: {addon_path}")
            skipped_files.append(addon_path)

    click.echo(f"Skipped: ")
    for file in skipped_files:
        click.echo(f"- {file}")

    if cleanup is True:
        click.echo(f"Cleaned: ")
        for file in cleaned_files:
            click.echo(f"- {file}")


@cli.command()
@click.option('-v', '--verbose', count=True)
def index(verbose):
    ''' Creates/Updates local blender addon database. '''

    click.echo("Indexing current blender addons ...")


if __name__ == "__main__":
    cli()

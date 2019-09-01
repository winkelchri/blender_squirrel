import click

from loguru import logger

from utils.settings import AddonInstallerSettings
from utils.addons import ZipAddon
from utils.addons.validators import InvalidBlenderAddon


@click.group()
def cli():
    pass


@cli.command()
@click.option('--cleanup', is_flag=True, help="Removes the installed file from the source directory")
def install(cleanup):
    settings = AddonInstallerSettings()
    addons_paths = settings.find_downloaded_addons()
    skipped_files = []
    cleaned_files = []

    for addon_path in addons_paths:
        addon = ZipA(
            settings=settings,
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


if __name__ == "__main__":
    cli()

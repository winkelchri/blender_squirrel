# Blender Addon Installer

## Mockup

```Python
from lib.settings import BlenderAddonSettings

downloaded_addons = BlenderAddonSettings.find_downloaded_addons()

for downloaded_addon in downloaded_addons:
    downloaded_addon.install()

```

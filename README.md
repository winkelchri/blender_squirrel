# Blender Squirrel - A blender addons manager

## Mockup

```Python
from squirrel.settings import BlenderAddonSettings

downloaded_addons = BlenderAddonSettings.find_downloaded_addons()

for downloaded_addon in downloaded_addons:
    downloaded_addon.install()

```

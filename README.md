# Blender Addon Installer

## Mockup

```Python
from utils.settings import BlenderAddonSettings

downloaded_plugins = BlenderAddonSettings.find_downloaded_plugins()

for downloaded_plugin in downloaded_plugins:
    downloaded_plugin.install()

```

# Blender Squirrel - A blender addons manager

## Mockup

```Python
from squirrel.settings import BlenderAddonSettings

downloaded_addons = BlenderAddonSettings.find_downloaded_addons()

for downloaded_addon in downloaded_addons:
    downloaded_addon.install()

```

## GUMROAD

It seems to be possible to authenticate towards Gumroad using a BEARER TOKEN.

1. Go to https://gumroad.com/settings/advanced
2. Create a new application
   Name: Blender-Squirrel
   redirect-url: http://example.com/blender-squirrel
3. Create a new **Access Token**
4. You can now authenticate using *BEARER TOKEN* instead of a hacky login.

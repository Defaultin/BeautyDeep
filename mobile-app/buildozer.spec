[app]

# (str) Title of your application
title = Beauty Deep

# (str) Package name
package.name = BeautyDeep

# (str) Package domain (needed for android/ios packaging)
package.domain = org.beauty_deep

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,kv

# (list) List of inclusions using pattern matching
source.include_patterns = images/*

# (str) Application versioning (method 1)
version = 2.9.0

# (list) Application requirements
requirements = python3==3.7.6,hostpython3==3.7.6,kivy==1.11.1,plyer,https://github.com/kivymd/KivyMD/archive/master.zip,akivymd,sdl2_ttf==2.0.15,numpy,socket,requests,urllib3,chardet,certifi,idna,simplejson,openssl,opencv

# (str) Presplash of the application
presplash.filename = %(source.dir)s/images/logo-bg.png

# (str) Icon of the application
icon.filename = %(source.dir)s/images/logo.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# change the major version of python used by the app
osx.python_version = 3.7.6

# Kivy version to use
osx.kivy_version = 1.9.1

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
android.presplash_color = #E91E63

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = %(source.dir)s/android-sdk/

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
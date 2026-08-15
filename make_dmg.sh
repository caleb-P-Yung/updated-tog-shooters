#!/bin/bash
set -e

APP_NAME="EggShooter"
DMG_NAME="${APP_NAME}-Installer.dmg"
APP_PATH="dist/${APP_NAME}.app"

rm -f "${DMG_NAME}"

create-dmg \
  --volname "${APP_NAME} Installer" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 150 190 \
  --hide-extension "${APP_NAME}.app" \
  --app-drop-link 450 190 \
  "${DMG_NAME}" \
  "${APP_PATH}"
emulator -avd Some_Android_Device

yes | poetry run buildozer android debug deploy run

poetry run python main.py

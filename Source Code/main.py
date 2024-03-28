import os.path, sys
import zipfile
from pathlib import Path
import tarfile
import wget
import asyncio
import shortcut
import ssl


PROTONURL = 'https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton9-2/GE-Proton9-2.tar.gz'
AREA_51_URL = 'https://github.com/ProjectDreamland/game/releases/download/1.1/Game.zip'
PROTONZIP = 'GE-Proton9-2.tar.gz'
PROTONDIR = 'GE-Proton9-2'
AREA_51_ZIP = 'Game.zip'
STEAMCOMPATTOOLSPATH = str(Path.home()) + '/.steam/root/compatibilitytools.d'

#create this bar_progress method which is invoked automatically from wget
def bar_progress(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  # Don't use print() as it will print in new line every time.
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()


def checkforprotonzip():
    # First check and see if Proton is installed in compat tools first thing
    if (os.path.isdir(STEAMCOMPATTOOLSPATH + '/' + PROTONDIR)):
        print('Proton already installed correctly!')
        return True
    if not os.path.isfile(PROTONZIP):
        print("Correct Proton version not found. Downloading now... ")
        return False
    else:
        print("Found Proton zip! Checking if Steam compat folder exists... ")
        return  True

async def DownloadProton():
    # Download the Proton tar
    try:
        wget.download(PROTONURL, bar=bar_progress)
    except Exception as e:
        print(e)

async def checkforsteamcompattooldir():
    print('Checking for compat tools path in Steam... ')
    if not os.path.isdir(STEAMCOMPATTOOLSPATH):
        print('Not found! Creating folder... ')
        os.makedirs(STEAMCOMPATTOOLSPATH, exist_ok=False)
        if os.path.isdir(STEAMCOMPATTOOLSPATH):
            print('Done! Extracting Proton version to directory... ')
            await ExtractProton()
        else:
            print('Could not create Steam compat tools directory!')
    else:
        print('Found compat tools folder! Extracting Proton version to directory... ')
        await ExtractProton()

async def ExtractProton():
    if not (os.path.isdir(STEAMCOMPATTOOLSPATH + '/' + PROTONDIR)):
        file = tarfile.open(PROTONZIP)
        # extracting file to compat tools
        file.extractall(STEAMCOMPATTOOLSPATH)
        # Close the file
        file.close()
        print('Extraction complete!')
        print('Removing zip file...')
        os.remove(PROTONZIP)
        print('Done!')
    else:
        print('Proton already extracted properly!')

def checkprotoninstall():
    if (os.path.isdir(STEAMCOMPATTOOLSPATH + '/' + PROTONDIR)):
        return True
    return False

def checkarea51extracted():
    if os.path.isdir(str(Path.home()) + '/project_dreamland/'):
        return True
    return False

async def getarea51files():
    print('Checking for Area51 zip file... ')
    if checkarea51extracted() is True:
        print('Area 51 already extracted!')
    elif not os.path.isfile(AREA_51_ZIP):
        print('Not found! Downloading now... ')
        output = AREA_51_ZIP
        try:
            url = AREA_51_URL
            wget.download(url=url, bar=bar_progress)
            await getarea51files()
        except Exception as e:
            print(e)
    else:
        print('Found!')
        await checkifarea51extracted()

async def checkifarea51extracted():
    if os.path.isdir(str(Path.home()) + '/project_dreamland/'):
        print('Area 51 already extracted properly!')
    else:
        print('Zip not extracted! Extracting now... ')
        await extractarea51files()

async def extractarea51files():
    zip_path = AREA_51_ZIP
    extract_to_path = Path.home() / 'project_dreamland'

    # Ensure the target directory exists
    extract_to_path.mkdir(parents=True, exist_ok=True)

    # Open and extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)

    print('Extraction complete!')
    print('Removing zip file...')
    os.remove(AREA_51_ZIP)
    print('Done!')

async def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    if checkforprotonzip() is False and checkprotoninstall() is False:
        try:
            await DownloadProton()
        except Exception as e:
            print(e)


    await checkforsteamcompattooldir()

    try:
        if (checkprotoninstall() is True):
            await getarea51files()
            if (shortcut.shortcut_exists() is True):
                print('Shortcut already added to Steam.')
            else:
                print('Adding shortcut to Steam... ')
                shortcut.create_shortcut()
                print('Done!')
    except Exception as e:
        print(e)

asyncio.run(main())

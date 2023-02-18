import zipfile


def unzip(location, file_name):
    zip_file_path = location + file_name + ".zip"
    print(f"Zip File Path: {zip_file_path}")

    try:
        with zipfile.ZipFile(zip_file_path) as z:
            z.extractall(location)
    except zipfile.BadZipFile as e:
        raise ValueError(
            'Bad zip file, please report on '
            'www.github.com/kaggle/kaggle-api', e)
    except FileNotFoundError as e:
        print(f"File not zipped!", e)
        return
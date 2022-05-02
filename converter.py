import ffmpeg
import glob
import os
import sys
from pyicloud import PyiCloudService


input_path = sys.path[0]

output_path = os.path.join(input_path, "output")


def collect_files(file_types):
    file_paths = []
    for file_type in file_types:
        file_paths.extend([f for f in glob.glob(input_path + f'/**/*.{file_type}', recursive=True)])

    file_zip = zip(map(os.path.basename, file_paths), file_paths)
    return file_zip


def convert_files(file_zip, api):
    for file_name, file_path in file_zip:
        if output_path not in file_path:
            print(f'Started processing: {file_name}\n{file_path}')
            new_dir = create_dir(file_path, file_name)
            extension = os.path.splitext(file_path)[1]
            new_file_name = str(file_name).replace(extension, '.mp4')

            if not os.path.isfile(new_dir + new_file_name):
                probe = ffmpeg.probe(file_path)

                try:
                    creation_time = str(probe['streams'][0]['tags']['creation_time'])

                except KeyError as err:
                    creation_time = ''

                source = ffmpeg.input(file_path)
                out = ffmpeg.output(source, new_dir + new_file_name, metadata='creation_time=' + creation_time)
                ffmpeg.run(out, overwrite_output=True)
                print(new_dir + new_file_name)

                with open(new_dir + new_file_name, 'rb') as file_in:
                    api.drive['Script Out'].upload(file_in)

            else:
                print('File already exists')

            print(f'Finished processing: {new_file_name}\n{new_dir + new_file_name}')


def create_dir(file_path, file_name):
    new_dir = (str(file_path).replace(input_path, output_path)).replace(file_name, '')
    try:
        os.makedirs(new_dir)
    except FileExistsError:
        pass

    return new_dir


def connect_to_cloud():
    user_name = input('User name: ')
    password = input('Password: ')
    api = PyiCloudService(user_name, password)

    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
    elif api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print("  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber'))))

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)
    
    return api            


if __name__ == '__main__':
    user_api=connect_to_cloud()
    file_types = [
         '3gp', '3GP', 'MKV', 'mkv', 'WMV', 'wmv','MP4', 'mp4', 'AVI', 'avi']
    files_to_convert = collect_files(file_types)
    convert_files(files_to_convert, user_api)
    

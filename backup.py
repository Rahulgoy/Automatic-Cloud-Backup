import os
import shutil
import sys
import time
import schedule
from datetime import datetime
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


def create_zip(path, file_name):
    try:
        shutil.make_archive(f"archive/{file_name}", 'zip', path)
        return True
    except FileNotFoundError as e:
        return False


def google_auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return gauth, drive


def upload_backup(drive, path, file_name):
    f = drive.CreateFile({'title': file_name})
    print(f)
    try:
        f.SetContentFile(os.path.join(path, file_name))
    except:
        print("Success")

    f.Upload()
    f = None


def create_log(path, status):
    with open("log.txt", "a") as file_object:
        now = datetime.now()
        date = now.strftime(r"%d/%m/%Y %H:%M:%S").replace('/', '-')
        status = "backup_"+status
        print(date+" "+status+" "+path)
        file_object.write(date+" "+status+" "+path+"\n")


def controller():
    path = r"/home/rahul/Projects/CC"
    print(path)
    now = datetime.now()
    file_name = "requirements"
    # file_name = "backup " + \
    #     now.strftime(r"%d/%m/%Y %H:%M:%S").replace('/', '-')
    # print(file_name)
    # if not create_zip(path, file_name):
    #     sys.exit(0)
    try:
        auth, drive = google_auth()
    except:
        path_ = "Authentication error"

    try:
        upload_backup(
            drive, r"/home/rahul/Projects/CC/archive", file_name+'.txt')
        print("done")
        status = "success"
        path_ = path
    except:
        status = "failure"
        if(path_ != "Authentication error"):
            path_ = "Upload Failure"
    create_log(path_, status)


if __name__ == "__main__":
    schedule.every(1).minutes.do(controller)  # for testing
    # schedule.every().day.at("00:00").do(controller)       #Backup after 1-day
    while True:
        schedule.run_pending()
        time.sleep(1)

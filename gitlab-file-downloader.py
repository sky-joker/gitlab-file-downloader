#!/usr/bin/env python
import os.path
import urllib.parse
import configparser
import base64
import json
import requests
import argparse
import sys


def options():
    parser = argparse.ArgumentParser(prog="gitlab-file-downloader.py",
                                     add_help=True,
                                     description="GitLabのリポジトリから指定したファイルをダウンロー"
                                                 "ドするツール")

    parser.add_argument("--server", "-s",
                        type=str, required=True,
                        help="GitLabのIPまたはホスト名を指定する")
    parser.add_argument("--project", "-p",
                        type=str, required=True,
                        help="プロジェクト名を指定する")
    parser.add_argument("--file", "-f",
                        type=str, required=True,
                        help="ダウンロードするファイルパスを指定する")
    parser.add_argument("--token", "-t",
                        type=str,
                        help="GitLabで生成したTokenを指定する")
    parser.add_argument("--ssl",
                        action="store_true",
                        help="SSL接続する場合は指定する")
    parser.add_argument("--branch", "-b",
                        type=str, default="master",
                        help="対象のブランチ名を指定する(default: master)")
    parser.add_argument("--output", "-o",
                        type=str,
                        help="ダウンロードしたファイルの保存先パスを指定する")

    args = parser.parse_args()
    return args


def status_code_err(obj):
    print("Error Code: %s" % obj.status_code)
    print(obj.text)
    sys.exit(1)


def main():
    args = options()

    # Create of request base url.
    if(args.ssl):
        base_url = "https://%s/api/v4" % args.server
    else:
        base_url = "http://%s/api/v4" % args.server

    # Encode file path to base64.
    file_path = urllib.parse.quote(args.file, safe="")

    # Set the save path.
    if(args.output):
        save_path = args.output
    else:
        save_path = args.file.split("/").pop()

    # Set the private token.
    if(args.token):
        headers = {"Private-Token": args.token}
    else:
        home_dir = os.path.expanduser("~")
        if(os.path.isfile(home_dir + "/.gitlab")):
            config = configparser.ConfigParser()
            config.read(home_dir + "/.gitlab")
            headers = {"Private-Token": config.get("settings", "token")}
        else:
            print("Error: Tokenを設定してください")
            sys.exit(1)

    # Get Project id.
    url = base_url + "/projects"
    r = requests.get(url,
                     headers=headers,
                     verify=False)

    if(r.status_code == 200):
        projects = json.loads(r.text)
        for project in projects:
            if(project["name"] == args.project):
                pid = project["id"]
                break
    else:
        status_code_err(r)

    # Download target file.
    url = base_url + "/projects/%s/repository/files/%s?ref=%s" \
                     % (pid, file_path, args.branch)
    r = requests.get(url,
                     headers=headers,
                     verify=False)

    if(r.status_code == 200):
        file_info = json.loads(r.text)
        content = base64.b64decode(file_info["content"]).decode('utf-8')
        with open(save_path, "w") as f:
            f.write(content)
    else:
        status_code_err(r)


if __name__ == "__main__":
    main()

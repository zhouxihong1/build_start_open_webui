#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        : build_start_open_webui.py    
@Contact     : https://github.com/zhouxihong1
@Version     : 1.0
@Modify Time : 2024/9/5 12:00
@Author      : zhouxihong
@Desciption  : None
@License     : (C)Copyright 2024-
"""
import os
import shutil


class BuildStartOpenWebui:
    
    def __init__(self) -> None:
        self.build_path = "start_open_webui"
        self.main_file = self.build_path+".py"
        # FIND PYTHON PATH
        python_path_list = os.popen("where pip").read().split("\n")  # windows
        while "" in python_path_list:
            python_path_list.remove("")
        self.python_path = os.path.dirname(os.path.dirname(python_path_list[0]))

    def copy_main_file(self):
        name = "open_webui"
        shutil.copyfile(self.python_path + rf"\Lib\site-packages\{name}\__init__.py", self.main_file)


    def copy_package(self, package_name):
        """copy venv package content

        :param package_name: package_name
        """
        shutil.copytree(self.python_path + rf"\Lib\site-packages\{package_name}", os.getcwd() + rf"\dist\{self.build_path}\_internal\{package_name}",
                        dirs_exist_ok=True)
    
    def copy_package_single_file(self, package_name, end_suffix=".pyd"):
        file_list = os.listdir(self.python_path + rf"\Lib\site-packages")
        pyd_name = ""
        for item in file_list:
            if item.startswith(package_name) and item.endswith(end_suffix):
                pyd_name = item
                break
        else:
            print("file not exists")
            return False
        shutil.copyfile(self.python_path + rf"\Lib\site-packages\{pyd_name}", os.getcwd() + rf"\dist\{self.build_path}\_internal\{pyd_name}")
    
    def gen_start_bat(self):
        with open(os.getcwd() + rf"\dist\{self.build_path}\{self.build_path}.bat", "w", encoding="utf-8") as f:
            f.write(f"{self.build_path}.exe serve")
    
    def main_build_step(self):
        self.copy_main_file()
        os.system(f"pyinstaller {self.main_file}")
        self.gen_start_bat()
        self.copy_package("chromadb")
        self.copy_package("open_webui")
        self.copy_package("passlib")
        self.copy_package("posthog")
        self.copy_package("backoff")
        self.copy_package("pypika")
        self.copy_package_single_file("hnswlib")
        self.copy_package_single_file("30fcd23745efe32ce681__mypyc")
        self.copy_package("pathspec")
        self.copy_package_single_file("_black_version", end_suffix=".py")
        self.copy_package("black")
        self.copy_package("platformdirs")
        self.copy_package("blib2to3")
        



if __name__ == '__main__':
    bsow = BuildStartOpenWebui()
    bsow.main_build_step()

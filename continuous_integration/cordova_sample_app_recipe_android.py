#!/usr/bin/env python3
#
#  cordova_sample_app_recipe_android.py
#
#  Created by Daniel Guttenberg on 14/01/16.
#
#

import os
import shutil
import subprocess
import tempfile
import time

from builderutilities import BuilderUtilities
from pathmanager import PathManager

from iosbuilder import IosBuilder

from abstractrecipe import AbstractRecipe
from artifactentry import ArtifactEntry
from dependencyentry import DependencyEntry


class CordovaSampleAppRecipeAndroid(AbstractRecipe):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'cordova_sample_app'

    @property
    def platform(self):
        return 'android'

    @property
    def artifacts(self):
        return []

    def get_dependencies(self):
        return [DependencyEntry("architect_worlds")]

    def prepare(self):
        print("Preparing " + self.name + ".")
        return 0

    def build(self):
        print('Building ' + self.name + '.')
        repository_root_dir = PathManager.get_recipe_path_with_subpath(__file__, os.pardir)
        previous_working_directory = os.getcwd()
        try:
            samples_script_root = os.path.join(PathManager.get_dependency_root_path(self, DependencyEntry("architect_worlds")), "src")
            os.chdir(samples_script_root)
            subprocess.run(["python3", "prepareexamples.py", "--phonegap", repository_root_dir])
        finally:
            os.chdir(previous_working_directory)
        return 0

    def finish(self):
        print('Finishing ' + self.name + '.')
        repo_root_path = PathManager.get_recipe_path_with_subpath(__file__, os.pardir)
        products_path = os.path.join(repo_root_path, 'products', self.platform)
        zip_file_name = 'wikitude-cordova-sample_app-5.1.1-3.2.0_' + time.strftime("%Y_%m_%d_%H_%M_%S")
        temporary_path = os.path.join(tempfile.gettempdir(), self.name)
        ignore_blacklist = shutil.ignore_patterns("continuous_integration", "products", ".git", ".gitignore", ".DS_Store")
        BuilderUtilities.create_zip_file_from_repository_via_temp_path(repo_root_path, os.path.join(products_path, zip_file_name), temporary_path, ignore_blacklist)
        return 0

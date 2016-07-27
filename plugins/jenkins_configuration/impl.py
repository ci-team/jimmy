# -*- coding: utf-8 -*-

#  Copyright 2016 Mirantis, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import subprocess
from lib.api import BaseGroovyPlugin


class JenkinsConfiguration(BaseGroovyPlugin):
    source_tree_path = 'jenkins.configuration'

    def update_dest(self, source, jenkins_url, jenkins_cli_path, **kwargs):
        data = self._tree_read(source, self.source_tree_path)
        if "security_type" in data:
            if data["security_type"] == "password":
                for u in data["admin_user"]:
                    try:
                        subprocess.call(["java",
                                         "-jar", jenkins_cli_path,
                                         "-s", jenkins_url,
                                         "groovy",
                                         self.groovy_path,
                                         "set_security_password",
                                         u["username"],
                                         "'{0}'".format(u["email"]),
                                         u["password"],
                                         "'{0}'".format(u["name"]),
                                         "'{0}'".format(u["public_key"])
                                         ], shell=False)
                    except OSError:
                        self.logger.exception('Could not find java')
            elif data["security_type"] == "unsecured":
                try:
                    subprocess.call(["java",
                                     "-jar", jenkins_cli_path,
                                     "-s", jenkins_url,
                                     "groovy",
                                     self.groovy_path,
                                     "set_unsecured"
                                     ], shell=False)
                except OSError:
                    self.logger.exception('Could not find java')

        try:
            subprocess.call(["java",
                             "-jar", jenkins_cli_path,
                             "-s", jenkins_url,
                             "groovy",
                             self.groovy_path,
                             "set_main_configuration",
                             "'{0}'".format(data["admin_email"]),  # jenkins-cli bug workaround
                             data["markup_format"],
                             str(data["num_of_executors"]),
                             str(data["scm_checkout_retry_count"])
                             ], shell=False)
        except OSError:
            self.logger.exception('Could not find java')

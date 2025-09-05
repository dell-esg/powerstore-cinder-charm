#! /usr/bin/env python3

# Copyright 2021 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

from ops.main import main
from ops_openstack.plugins.classes import CinderStoragePluginCharm

logger = logging.getLogger(__name__)

VOLUME_DRIVER = 'cinder.volume.drivers.dell_emc.powerstore.driver.PowerStoreDriver'

class CinderPowerStoreCharm(CinderStoragePluginCharm):

    PACKAGES = ['cinder-common']
    # Overriden from the parent. May be set depending on the charm's properties
    stateless = False
    active_active = False

    mandatory_config = ['protocol', 'san-ip', 'san-login', 'san-password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stored.is_started = True

    def cinder_configuration(self, charm_config) -> 'list[tuple]':
        """Return the configuration to be set by the principal"""
        cget = charm_config.get

        volume_backend_name = (
            cget('volume-backend-name') or self.framework.model.app.name
        )

        raw_options = [
            ('volume_driver', VOLUME_DRIVER),
            ('volume_backend_name', volume_backend_name),
            ('san_ip', cget('san-ip')),
            ('san_login', cget('san-login')),
            ('san_password', cget('san-password')),
            ("storage_protocol", self.cget("protocol")),
            ("powerstore_nvme", self.cget('powerstore-nvme')),
        ]
        
        if self.cget("use-multipath"):
            raw_options.extend(
                [
                    ("use_multipath_for_image_xfer", True),
                    ("enforce_multipath_for_image_xfer", True),
                ]
            )
        
        if self.cget("powerstore-ports"):
            raw_options.extend(
                [("powerstore_ports", self._csv_to_array(cget("powerstore-ports")))]
            )
            
        options = [(x, y) for x, y in raw_options if y]
        return options

    def _csv_to_array(self, csv: str | None) -> str | None:
        """
        Converts a csv input into an array of strings.
            i.e. `item1, item2, item3` -> `['item1', 'item2', 'item3']`

        This is used to handle multi-item user inputs.
        """
        if csv is None:
            return None

        items = [item.strip(" \"'") for item in csv.split(",")]
        return "[{}]".format(",".join(items))


if __name__ == '__main__':
    main(CinderPowerStoreCharm)

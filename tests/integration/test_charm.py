#!/usr/bin/env python3

import logging
from pathlib import Path

import jubilant
from pytest_jubilant import pack

logger = logging.getLogger(__name__)

APP_NAME = "cinder-powerstore"
CINDER_CHARM = "cinder"


def test_deploy_powerstore(juju: jubilant.Juju) -> None:
    """Deploy PowerMax Charm."""
    charm_root = Path(__file__).resolve().parents[2]

    config = {
         "protocol": "ISCSI",
         "san-login": "admin",
         "san-password": "password",
         "san-ip": "10.20.30.40",
     }
    juju.deploy(CINDER_CHARM)
    juju.deploy(pack(charm_root).resolve(), app=APP_NAME, config=config)
    
def test_relate(juju: jubilant.Juju) -> None:
    """Set the required relation."""
    for relation in ['storage-backend']:
        juju.integrate(f"{APP_NAME}:{relation}", f"{CINDER_CHARM}:{relation}")

    juju.wait(lambda status: jubilant.all_active(status, APP_NAME))
    logger.info("PowerMax cinder backend ready for operations")
    

Dell PowerStore Storage Backend for Cinder
-----------------------------------------

## Overview

This charm provides a Dell PowerStore storage backend for use with the Cinder charm.

## Configuration

This section covers common and/or important configuration options. See file `config.yaml` for the full list of options, along with their descriptions and default values. See the [Juju documentation][juju-docs-config-apps] for details on configuring applications.

[juju-docs-config-apps]: https://juju.is/docs/juju/juju-config

### `protocol`

Protocol to use with the array. Can be either FC or iSCSI.

### `san-ip`

UniSphere IP used to access the array.

### `san-login`

Username used to log on UniSphere.

### `san-password`

Password used to authenticate in UniSphere.

### `powerstore-ports`

Allowed ports. Comma separated list of PowerStore iSCSI IPs or FC WWNs to be used. If the option is not set all ports are allowed.

### `powerstore-nvme`

Enables NVMe-OF PowerStore connection.

### `use-multipath-for-image-xfer`

Use multipath for image xfer.


## Deployment

This charm's primary use is as a backend for the cinder charm. To do so, add a relation between both charms:
   
    juju deploy --config cinder-powerstore-config.yaml cinder-powerstore
    juju integrate cinder-powerstore:storage-backend cinder:storage-backend


# Documentation

The OpenStack Charms project maintains two documentation guides:

* [OpenStack Charm Guide][cg]: for project information, including development
  and support notes
* [OpenStack Charms Deployment Guide][cdg]: for charm usage information

[cg]: https://docs.openstack.org/charm-guide
[cdg]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/charm-cinder-powermax/+filebug).

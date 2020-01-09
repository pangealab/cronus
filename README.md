![Intro](./docs/now-cli.png)

This project shows you how to set up the **NOW CLI** and use it to interact with a ServiceNow instance either locally from your workstation or from a CI/CD Pipeline like Jenkins

# Installation

* Clone Project

    ```
    git clone git@github.com:advlab/cronus.git
    cd cronus
    ```
* Install Package

    ```
    sudo python3 setup.py install
    ```

    > NOTE: Once the package is deployed to the [PyPI](https://pypi.org) repository you can install the latest package using the standard *pip3* command (e.g. `pip3 install nowcli`)

* Uninstall Package

    ```
    sudo pip3 uninstall -y nowcli
    ```

# Operation

* Create default profile in ~/.now/credentials

    ```
    $now configure
    ```

* Setup additional profiles (e.g. newyork) and use your instance specifics

    ```
    $ now -p newyork configure
    table_api [/api/now/table]:
    cmdb_api [/api/x_snc_labs_atlas/v1/register/services]: 
    em_api [/api/x_snc_labs_atlas/v1/create/event]: 
    server []: https://newyorkdemo01.service-now.com
    username []: admin
    password []: changeit
    ```

* Register Service (e.g. startreck.json)

    ```
    $ now -p newyork -d startreck.json cmdb register-service
    Called CMDB...
    {'result': {'code': '200', 'type': 'register_services', 'message': 'Services created in ServiceNow: 4'}}
    ```

* Create Event

* Resolve Incident
![Intro](https://raw.githubusercontent.com/advlab/artemis/master/docs/now-cli.png)

This project shows you how to set up the **NOW CLI** and use it to interact with a ServiceNow instance either locally from your workstation or from a CI/CD Pipeline like Jenkins

# Prerequisites

* Python3 Installed
* PiPy Account to deploy package

# Installation

* Clone Project

    ```
    git clone git@github.com:advlab/cronus.git nowcli
    cd nowcli
    ```
* Install Package from Source

    ```
    sudo python3 setup.py install
    ```

    > NOTE: Once the package is deployed to the [PyPI](https://pypi.org) repository you can install the latest package using the standard *pip3* command (e.g. `pip3 install nowcli`)

* Uninstall Package

    ```
    sudo pip3 uninstall -y nowcli
    ```

# Deploy Package to PiPi

* Install Twine

    ```
    pip3 install twine
    ```

* Create Source Distribution

    ```
    python3 setup.py sdist
    ```

* Deploy Package

    ```
    twine upload dist/*
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
    server []: YOURSERVERURL
    username []: YOURUSERID
    password []: YOURPASSWORD
    ```

* Register Service (e.g. startreck.json)

    ```
    $ now -p newyork -d startreck.json cmdb register-services
    Called CMDB...
    {'result': {'code': '200', 'type': 'register_services', 'message': 'Services created in ServiceNow: 4'}}
    ```

* Create Event

* Resolve Incident

# Example Payloads

* bookinfo.json

    ```
    {
    "name": "Bookworms",
    "comments": "Bookworms 2019 Reviews",
    "services": [{
            "name": "bookinfo",
            "uri": "http://bookinfo.com"
        },
        {
            "name": "productpage",
            "uri": "http://bookinfo.com/product"
        },
        {
            "name": "details",
            "uri": "http://bookinfo.com/details"
        },
        {
            "name": "reviews-v1",
            "uri": "http://bookinfo.com/reviews-v1"
        },
        {
            "name": "reviews-v2",
            "uri": "http://bookinfo.com/reviews-v2"
        },
        {
            "name": "reviews-v3",
            "uri": "http://bookinfo.com/reviews-v3"
        },
        {
            "name": "ratings",
            "uri": "http://bookinfo.com/ratings"
        }
    ],
    "relationships": [{
            "parent": null,
            "child": "bookinfo"
        },
        {
            "parent": "bookinfo",
            "child": "productpage"
        },
        {
            "parent": "productpage",
            "child": "reviews-v1"
        },
        {
            "parent": "productpage",
            "child": "reviews-v2"
        },
        {
            "parent": "productpage",
            "child": "reviews-v3"
        },
        {
            "parent": "productpage",
            "child": "details"
        },
        {
            "parent": "reviews-v2",
            "child": "ratings"
        },
        {
            "parent": "reviews-v3",
            "child": "ratings"
        }
    ]
    }
    ```

* startreck.json

    ```
    {
    "name": "USS Enteprise NCC-1701",
    "comments": "NCC-1701 Constitution Class Starship",
    "services": [{
            "name": "ncc1701",
            "uri": "http://ncc1701.net"
        },
        {
            "name": "weapons",
            "uri": "http://weapons.ncc1701.net"
        },
        {
            "name": "phasers",
            "uri": "http://phasers.ncc1701.net"
        },
        {
            "name": "lifesuppport",
            "uri": "http://lifesupport.ncc1701.net"
        }
    ],
    "relationships": [{
            "parent": null,
            "child": "ncc1701"
        },
        {
            "parent": "ncc1701",
            "child": "weapons"
        },
        {
            "parent": "weapons",
            "child": "phasers"
        },
        {
            "parent": "ncc1701",
            "child": "lifesuppport"
        }
    ]
    }
    ```

# Reference

## Python 3

This section describes how to install Python 3.7.2 in Ubuntu 18.04 / 18.10

* Install Python 3

    ```
    sudo add-apt-repository ppa:ubuntu-toolchain-r/ppa
    sudo apt install -y python3.7
    ```

* Install Pip

    ```
    sudo apt install -y python3-pip
    ```

* To check versions 

    ```
    apt list --installed | grep python
    ```

* Install Unit Tester

    ```
    pip3 install nose
    ```

* Install Nose Tester

    ```
    sudo apt install python-nose
    ```

* Run Unit Tester

    ```
    nosetests --with-xunit tests/test_project.py
    ```

* Freeze Requirements

    ```
    pip3 freeze > requirements.txt
    ```
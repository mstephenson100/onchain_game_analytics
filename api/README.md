# Steps to install BIOS Api
Follow these steps to install the bios json-rpc server. YMMV

# Warning
Following the steps in this document will result in an internet facing Nginx server. Hopefully you know what you're doing.

# Install pyenv

Pyenv is required for this to work. Follow a guide like this to get pyenv installed: https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004

## Prerequisites
This documentation assumes you already have an indexer running with a pre-loaded MySQL Database. If you don't have that then you're in the wrong place.

Configure api.conf:
~~~
[credentials]
db_user = <redacted>
db_password = <redacted>
db = bios
~~~

## Configure pyenv environment

From the current working directory:
~~~
$ python -m venv venv
$ source venv/bin/activate
(venv) $
~~~
Install packages required for flask and uwsgi
~~~
(venv) $ pip install wheel
(venv) $ pip install uwsgi flask
~~~
Install packages needed by server.py
~~~
(venv) $ pip install PyMySQL==0.9.3
(venv) $ pip install jsonrpcserver
~~~
The remaining configs should already be good enough to make this run.

## Test some stuff
 You should probably test to make sure your environment is working. Verify that server.py runs without error. The following command should not return an error:
 ~~~~
 (venv) $ python server.py
 * Serving Flask app 'server'
* Debug mode: off
**WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.**
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
~~~
  
 ### Try making an API call
 This will only work if you have a copy of the fully indexed MySQL data loaded on a locally hosted server with credentials correctly configured in api.conf. Run the following curl command from another shell instance on the server where server.py is currently running:
 ~~~~
 $ curl -X POST http://localhost:5000 -d '{"jsonrpc": "2.0", "method": "warehouse_inventory", "params": {"capable_id": "1"}, "id": 1}' | jq . 
{
    "jsonrpc": "2.0",
    "result": {
        "results_len": 1,
        "warehouse_inventory": [{
            "capable_id": 1,
            "capable_owner": "0x048242eca329a05af1909fa79cb1f9a4275ff89b987d405ec7de08f73b85588f",
            "asteroid_id": 16337,
            "lot_id": 151,
            "crew_id": 2,
            "wallet": "0x048242eca329a05af1909fa79cb1f9a4275ff89b987d405ec7de08f73b85588f",
            "txn_id": "0x05edb28a12891cc37446c8fbc3c297106a5eca6b2fa574bb00efaee8c154b578",
            "block_number": 646493,
            "resource_len": 1,
            "resources": [{
                "resource_id": 11,
                "quantity": 1753333,
                "volume": 1087066460,
                "mass": 1753333000
            }]
        }]
    },
    "id": 1
}
~~~
If the above output shows an error then you might need to install jq.
~~~
sudo apt install jq
~~~
If it still shows errors then ¯\\_(ツ)_/¯

## Continue configuring uwsgi
CTL-C out of server.py and try running with uwsgi
~~~
(env) $uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
*** Starting uWSGI 2.0.21 (64bit) on [Sat Jul 22 21:17:12 2023] ***
compiled with version: 9.4.0 on 22 July 2023 21:00:39
os: Linux-5.4.0-97-generic #110-Ubuntu SMP Thu Jan 13 18:22:13 UTC 2022
nodename: <redacted>
machine: x86_64
clock source: unix
detected number of CPU cores: 4
current working directory: /home/dorks/bios/api
detected binary path: /home/dorks/bios/api/venv/bin/uwsgi
!!! no internal routing support, rebuild with pcre support !!!
*** WARNING: you are running uWSGI without its master process manager ***
your processes number limit is 65536
your memory page size is 4096 bytes
detected max file descriptor number: 65536
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
uwsgi socket 0 bound to TCP address 0.0.0.0:5000 fd 3
Python version: 3.9.5 (default, Jun 16 2023, 20:33:44)  [GCC 9.4.0]
*** Python threads support is disabled. You can enable it with --enable-threads ***
Python main interpreter initialized at 0x5604d7784cd0
your server socket listen backlog is limited to 100 connections
your mercy for graceful operations on workers is 60 seconds
mapped 72920 bytes (71 KB) for 1 cores
*** Operational MODE: single process ***
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x5604d7784cd0 pid: 3520236 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI worker 1 (and the only) (pid: 3520236, cores: 1)
~~~

If uwsgi runs without an error then try running the previous curl command and verify that data returns. If so then you are ready to move to the next steps of enabling the json-rpc server as a service. If not then oh well.

## Enable uWSGI as a service
You can now stop both server.py and uWSGI and deactivate the pyenv environment:
~~~
(venv) $ deactivate
~~~
Make a new file called /etc/systemd/system/biosapi.service:
~~~
$ sudo vi /etc/systemd/system/myproject.service
[Unit]
Description=uWSGI instance to serve myproject
After=network.target

[Service]
User=dorks
Group=www-data
WorkingDirectory=/home/dorks/bios/api
Environment="PATH=/home/dorks/bios/api/venv/bin"
ExecStart=/home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini

[Install]
WantedBy=multi-user.target
~~~
This should point at the correct path for wherever you have the apiserver code installed.
### Set some permissions
Go back to wherever you have the api code installed and fix it's permissions to be accessible by the www-data group. This will make it accessible to nginx:
~~~
$ sudo  chgrp www-data /home/dorks/bios/api
~~~
### Enable uWSGI to run as a service
Start the biosapi service which you configured two steps earlier:
~~~
$ sudo systemctl start biosapi
~~~
Enable biosapi to start on boot:
~~~
$ sudo systemctl enable biosapi
$ sudo systemctl status biosapi
**●** biosapi.service - uWSGI instance to serve myproject
Loaded: loaded (/etc/systemd/system/biosapi.service; disabled; vendor preset: enabled)
Active: **active (running)** since Sat 2023-07-22 19:41:55 UTC; 2h 4min ago
Main PID: 3514335 (uwsgi)
Tasks: 6 (limit: 9508)
Memory: 34.7M
CGroup: /system.slice/biosapi.service
├─3514335 /home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini
├─3514348 /home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini
├─3514349 /home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini
├─3514350 /home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini
├─3514351 /home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini
└─3514352 /home/dorks/bios/api/venv/bin/uwsgi --ini biosapi.ini
~~~
You should now be able to run that curl command again and it should respond. For now you can also tail /var/log/syslog to watch the biosapi log.

## Configure Nginx to proxy requests

If you don't already have nginx installed then install it:
~~~
$ sudo apt install nginx
~~~
Make a new config called /etc/nginx/sites-available/biosapi.conf:
~~~
$ sudo vi /etc/nginx/sites-available/biosapi.conf:
server {
    listen 8180;
    server_name fully.qualified.domain.com;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/dorks/bios/api/biosapi.sock;
    }
}
~~~
Symlink config to sites-available:
~~~
$ sudo ln -s /etc/nginx/sites-available/biosapi.conf /etc/nginx/sites-enabled
~~~
Start Nginx:
~~~
$ sudo systemctl restart nginx
~~~
Run that curl command but this time run it from another location on the internet because you should now be serving the api service to the internet on port 8180. You should probably read about firewalls to make sure you're protected.
~~~
$ curl -X POST http://fully.qualified.domain.com:8180 -d '{"jsonrpc": "2.0", "method": "warehouse_inventory_all", "params": {"crew_id": "79"}, "id": 1}'
~~~

## json-rpc api calls

### owned_asteroids
***retrieve all asteroids owned by wallet***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet that holds asteroids  |True  |

### owned_crewmates
***retrieve all crewmates owned by wallet***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet that holds crewmates  |True  |

### owned_crew
***retrieve all crew owned by wallet***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet that holds composed crew  |True  |

### crew_composition
***retrieve composition for a crew_id***

|parameter  |summary  |required  |
|--|--|--|
|crew_id  |id of composed crew  |True  |

### crew_owner
***retrieve wallet of crew owner***

|parameter  |summary  |required  |
|--|--|--|
|crew_id  |id of composed crew  |True  |

### asteroid_owner
***retrieve wallet of asteroid owner***

|parameter  |summary  |required  |
|--|--|--|
|asteroid_id  |id of asteroid  |True  |

### crewmate_owner
***retrieve wallet of crewmate owner***

|parameter  |summary  |required  |
|--|--|--|
|crewmate_id  |id of crewmate  |True  |

### construction_planned
***retrieve all planned construction for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|construction_type  |construction type either warehouse or extractor  |True  |

### construction_started
***retrieve all started construction for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|construction_type  |construction type either warehouse or extractor  |True  |

### construction_finished
***retrieve all finished construction for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|construction_type  |construction type either warehouse or extractor  |True  |

### construction_unplanned
***retrieve all unplanned construction for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|construction_type  |construction type either warehouse or extractor  |True  |

### construction_deconstructed
***retrieve all deconstructed construction for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|construction_type  |construction type either warehouse or extractor  |True  |

### owned_buildings
***retrieve all buildings for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|building_type  |building_type either warehouse or extractor  |True  |

### owned_buildings_on_asteroid
***retrieve all buildings on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |
|building_type  |building_type either warehouse or extractor  |True  |
|asteroid_id  |asteroid_id to search for owned buildings  |True  |

### owned_coresamples
***retrieve all coresamples for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet |wallet must be specified when crew_id is not |False |
|crew_id |crew_id must be specified when wallet is not |False |

### coresamples_finished
***retrieve all finished coresamples for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### coresamples_started
***retrieve all started coresamples for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### coresamples_by_lot
***retrieve all coresamples on a lot for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid for lot  |True  |
|lot_id |lot on asteroid |True |

### coresamples_by_asteroid
***retrieve all coresamples on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid for lot  |True  |

### coresamples_depleted
***retrieve all depleted coresamples for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### extraction_started
***retrieve all extraction actions started for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### extraction_started_on_asteroid
***retrieve all extraction actions started on asteroid_id for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid to check for started extractions  |True  |

### extraction_started_on_lot
***retrieve all started extraction actions on lot_id for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid to check for started extractions  |True  |
|lot_id |lot on asteroid |True |

### extraction_finished
***retrieve all finished extraction actions for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### extraction_finished_on_asteroid
***retrieve all finished extraction actions on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid to check for finished extractions  |True  |
|lot_id |lot on asteroid |True |

### extraction_finished_on_lot
***retrieve all finished extraction actions on a lot for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid to check for finished extractions  |True  |
|lot_id |lot on asteroid |True |

### extractions_pending
***retrieve all pending extraction actions for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### extractions_pending_on_asteroid
***retrieve all pending extraction actions on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid to check for pending extractions  |True  |

### extractions_pending_on_lot
***retrieve all pending extraction actions on a lot for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid to check for pending extractions  |True  |
|lot_id |lot on asteroid |True |

### extracted_resources
***retrieve all extracted resources for a resource_id by either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|resource_id |id of resource |True |

### extracted_resources_all
***retrieve all extracted resources for by either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### warehouse_started_delivery
***retrieve all started warehouse deliveries for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### warehouse_started_delivery_on_asteroid
***retrieve all started warehouse deliveries on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id to check for started deliveries  |True  |

### warehouse_started_delivery_on_lot
***retrieve all started warehouse deliveries on a lot for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id for started deliveries  |True  |
|lot_id |lot on asteroid |True |

### warehouse_finished_delivery
***retrieve all finished warehouse deliveries for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### warehouse_finished_delivery_on_asteroid
***retrieve all finished warehouse deliveries on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id for finished deliveries  |True  |

### warehouse_finished_delivery_on_lot
***retrieve all finished warehouse deliveries on a lot for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id for finished deliveries  |True  |
|lot_id |lot on asteroid |True |

### warehouse_delivery_pending
***retrieve all pending warehouse deliveries for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |

### warehouse_delivery_pending_on_asteroid
***retrieve all pending warehouse deliveries on an asteroid for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id for pending deliveries  |True  |

### warehouse_delivery_pending_on_lot
***retrieve all pending warehouse deliveries on a lot for either wallet or crew_id***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id for pending deliveries  |True  |
|lot_id |lot on asteroid |True |

### warehouse_inventory
***retrieve current warehouse inventory for a capable_id***

|parameter  |summary  |required  |
|--|--|--|
|capable_id  |capable_id of warehouse  |True  |

### warehouse_inventory_on_asteroid
***retrieve current warehouse inventory on an asteroid for either wallet or crew_id ***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |
|asteroid_id  |asteroid_id to check warehouse inventory  |True  |

### warehouse_inventory_all
***retrieve all warehouse inventories for  either wallet or crew_id ***

|parameter  |summary  |required  |
|--|--|--|
|wallet  |wallet must be specified when crew_id is not  |False  |
|crew_id |crew_id must be specified when wallet is not |False |


# DataCollector (comp-b)

This component read messages **all** (topic: #) from the Broker and puts the messages into different storages like mysql or log file

## How to use

Just start the docker container with:

```sh
docker run --rm --name dataprovider ghcr.io/idevopsdemo/comp-b
```

Deploy via Helm

(Optional) In case of private registry usage, login to the registry first:

```sh
helm registry login -u myuser oci://ghcr.io/idevopsdemo/charts/comp-b
```

```sh
helm install -n my-namespace comp-b oci://ghcr.io/idevopsdemo/charts/comp-b
#in order to deploy pre-release version use
helm install -n my-namespace --devel comp-b oci://ghcr.io/idevopsdemo/charts/comp-b
```

### Optional Parameters

The following environment variables are available to adjust the behavior:

* **DATACOLLECTOR_STORAGE** the storage class to use. Currently available: dummy(default), mysql
* **QCLIENT_BROKER_HOST** ip address of the mqtt broker (default: 172.17.0.1)
* **QCLIENT_BROKER_PORT** port of mqtt broker (default: 1883)

Based on the selected storage class additional parameters are available:

* MYSQL
    * **STORAGE_MYSQL_HOST** ip address of the cockroach db (default: 172.17.0.1)
    * **STORAGE_MYSQL_PORT** port of the cockroach db (default: 3306)
    * **STORAGE_MYSQL_DB** database to use (default: srsng)
    * **STORAGE_MYSQL_USER** username (default: admin)
    * **STORAGE_MYSQL_PASS** password (default: mysecret)

```sh
docker run --rm --name datacollector -e DATACOLLECTOR_STORAGE=mysql ghcr.io/idevopsdemo/comp-b
```

## TODOs

* Only some testing

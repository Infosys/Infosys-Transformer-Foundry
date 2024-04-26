# Hardware Requirements

No. of environments are indicative. At minimum Dev and Prod environments are required.

1. Enterprise Kubernetes Cluster

2. Enterprise Object Store - 1 each
   | Configuration/Env | Dev | Pre Prod + | Prod |
   | ---------------------- | ----------------------------------------------- | --------------------------------------- | --------------------------------------- |
   | Provider | Nutanix S3 - Object Store |Nutanix S3 - Object Store |Nutanix S3 - Object Store |
   |HDD | 140GIB | 5TB | 5TB |

<br>

3. Jenkins Server Setup - 1 each
   | Configuration/Env | Dev | Pre Prod + | Prod |
   | ---------------------- | ----------------------------------------------- | --------------------------------------- | --------------------------------------- |
   | CPU | 2 Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz | 4 Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz | 4 Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz |
   | RAM | 16GIB | 48GIB | 48GIB |
   | OS | Ubuntu -22.04.3 LTS |Ubuntu -22.04.3 LTS |Ubuntu -22.04.3 LTS |
   | HDD | 100GIB | 250GB | 250GB |

<br>

4. Mongo DB – 1 each
   | Configuration/Env | Dev | Pre Prod + | Prod |
   | ---------------------- | ----------------------------------------------- | --------------------------------------- | --------------------------------------- |
   | CPU | 2-core, 2.4 GHZ | 4-core, 2.4 GHZ | 4-core, 2.4 GHZ |
   | RAM | 16GIB | 48GIB | 48GIB |
   | OS | Red Hat Enterprise Linux 7+ (64 bit) |Red Hat Enterprise Linux 7+ (64 bit) |Red Hat Enterprise Linux 7+ (64 bit) |
   | HDD | 100GIB | 200GIB | 200GIB |

<br>

5. Enterprise ELK Server
6. Enterprise Docker Repository
7. Enterprise GitHub
8. Enterprise Artifactory

# Software Requirements

| No. | Name                            | Track              | Developer Machine | Kubernetes Cluster | Jenkins Server | ELK Server |
| --- | ------------------------------- | ------------------ | ----------------- | ------------------ | -------------- | ---------- |
| 1   | Kubeflow                        | Kubernetes Cluster |                   | Y                  |                |            |
| 2   | Kubectl.exe                     | Kubernetes Cluster |                   | Y                  | Y              |            |
| 3   | Node JS - 20.9.0                |                    | Y                 |                    |                |            |
| 4   | Angular JS 12+                  |                    | Y                 |                    |                |            |
| 5   | Python 3.9                      |                    | Y                 |                    |                |            |
| 6   | Mongo Compass -1.32.2.0         | Mongo DB           | Y                 |                    |                |            |
| 7   | Java 1.8 +                      | Jenkins Server     |                   |                    | Y              |            |
| 8   | Jenkins -2.426.3 (2024-01-24)   | Jenkins Server     |                   |                    | Y              |            |
| 9   | Docker -                        |                    |                   | Y                  | Y              |            |
| 10  | NPM -10.1.0                     |                    | Y                 |                    |                |            |
| 11  | Git -2.41.0.2                   |                    | Y                 |                    |                |            |
| 12  | Elastic Search -7.16.3          | ELK Server         |                   |                    |                | Y          |
| 13  | Kibana-7.16.3                   | ELK Server         |                   |                    |                | Y          |

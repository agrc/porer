# conductor

a bot that checks on the existence of data and required fields

![conductor_sm](https://user-images.githubusercontent.com/325813/90076216-62563280-dcbc-11ea-8023-afa62e75b04b.png)

## prerequisites

1. enable

   - cloud pub sub subscription
     - `gcloud services enable pubsub.googleapis.com`
   - cloud run api\*
     - `gcloud services enable run.googleapis.com`
   - cloud container registry api\*
     - `gcloud services enable containerregistry.googleapis.com`
   - cloud scheduler api\*
     - `gcloud services enable cloudscheduler.googleapis.com`
   - cloud secrets api\*
     - `gcloud services enable secretmanager.googleapis.com`
   - cloud compute engine
     - `gcloud services enable compute.googleapis.com`
   - cloud build api\*
     - `gcloud services enable cloudbuild.googleapis.com`

1. give google cloud default compute service account view access to stewardship spreadsheet
1. Request DTS to attach the project to the DTS [dev, prod] Shared VPC

_\* requires billing_

## cloud configuration

1. Update project id in `src/conductor/server.py:43`
1. Create a `client-secret.json` file with sheet privileges and read access to the stewardship spreadsheet.

### cloud registry

1. build image
   - `docker build . -t conductor`
1. tag image in GCR
   - `docker tag conductor gcr.io/ut-dts-agrc-porter-prod/conductor`
1. push image to GCR
   - `docker push gcr.io/ut-dts-agrc-porter-prod/conductor`

```bash
docker build . -t conductor &&
docker tag conductor gcr.io/ut-dts-agrc-porter-prod/conductor &&
docker push gcr.io/ut-dts-agrc-porter-prod/conductor
```

### cloud run

1. create a service named `conductor`
1. authentication: `require authentication`
1. choose latest container image
   - `gcr.io/ut-dts-agrc-porter-prod/conductor@latest`
1. Request timeout: `300`
1. Maximum instances: `10`
1. enable shared VPC connector
   - `gcloud run services update conductor --vpc-connector projects/ut-dts-shared-vpc-dev/locations/us-central1/connectors/dts-shared-vpc-connector`
   - `gcloud alpha run services update conductor --vpc-connector=projects/ut-dts-shared-vpc-dev/locations/us-central1/connectors/dts-shared-vpc-connector --vpc-egress=all --platform managed --zone us-central1`
1. copy cloud run url for the subscription

### subscriptions

1. create topic with id: `conductor-topic`
1. create subscription with id: `conductor-subscription` pointed at the newly created topic

   - delivery type: `push`
   - expiration: `never expires`
   - push endpoint: `<cloud run service url>/gcp/schedule`
   - acknowledgement deadline: `300 seconds`
   - message retention: `30 minutes`
   - retry policy: `min: 10; max: 60`

### scheduler

1. create job named `conductor`

   - frequency: `0 9 * * 1`
   - time zone: `America/Denver (MDT)`
   - target: `Pub/Sub`
   - topic: `conductor-topic`
   - payload: `{ "now": true }`

### secrets

1. create secret as valid json with name: `conductor-connections`
1. give default compute service account `secret manager secret accessor` role
1. create a secret named `stewardship-sa` and upload the `client-secret.json` key created earlier

### CI/CD

1. create a service account with the following privileges and create a key:
   - Cloud Build Service Account
   - Cloud Build Editor
   - Service Account User
   - Cloud Run Admin
   - Viewer
1. create two secrets in [github](https://github.com/agrc/porter/settings/secrets)
   - RUN_PROJECT - the project id to deploy conductor to
   - RUN_SA_KEY - the service account key data

## Development

1. use `test_conductor` as the entry point
1. install the Microsoft ODBC driver for SQL Server for [Windows](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) or [macOS](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos)
1. create a copy of `src/conductor/connections_sample.py` as `src/conductor/connections.py`
   1. generate a [new GitHub personal access token](https://github.com/settings/tokens/new) with `public_repo` and store it in `github_token`
   1. set the `local.service_account_file` path to a service account file with access to the stewardship sheet

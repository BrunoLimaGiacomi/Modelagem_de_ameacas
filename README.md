# GenAI Threat Modelling - Guide

## Back-End Stack

Start with the back-end first. It will generate the results for deployment on the front-end.

## Requirements
- Be in US-EAST-1 (Northern Virginia)
- Create a role in IAM and grant the following permissions:
  - AmazonEC2ContainerRegistryFullAccess;
  - AmazonEC2FullAccess;
  - AmazonECS_FullAccess;
  - AmazonElasticContainerRegistryPublicFullAccess;
  - AmazonElasticContainerRegistryPublicPowerUser;
  - AmazonElasticContainerRegistryPublicReadOnly;
  - AWSCloudFormationFullAccess;
  - AmazonRDSFullAccess;
  - AmazonS3FullAccess;
  - IAMFullAccess.
- EC2 T2 Medium, with a 30GB EBS 
- Attach the role to the EC2
- Modify its Security Group to accept custom TCP traffic on port 5173 originating from your IP address (your personal computer's IP address, not the EC2 partition)
- Python 3.11 or higher - [instructions for installing](https://stackoverflow.com/questions/27669927/how-do-i-install-python-3-on-an-aws-ec2-instance)
- Git - [instructions for installing](https://medium.com/@dassandeep0001/how-to-install-git-in-ec2-instance-1bfeb1cc9dc9)
- Docker - [instructions for installing](https://docs.docker.com/engine/install/)
- AWS CLI - [instructions for installing](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- AWS CDK v2 - [instructions for installing](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

You will also need valid credentials to your AWS Account to be present in your terminal session.

---

* Note that the permissions granted are quite extensive and this should not be done in a corporate environment.

---

## Getting started

Pull the repository into your EC2:

```
git clone -b master https://github.com/BrunoLimaGiacomi/Threat-Modeling.git
cd Threat-Modeling
git branch
```

We recommend you create a virtualenv to manage project dependencies.

```
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies (inside the Back-End folder).

```
pip install -r requirements.txt
```

Before synthesizing the CloudFormation templates, you may need to login on AWS and Docker

```
aws ecr-public get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin public.ecr.aws
```



To confirm you are logged in, use the commands below:

```
docker info | grep -i ecr
```

Deploying to your AWS Account require that you first bootstrap your Account. This is a one-time only process, so if you
have previously bootstrapped your account, you may skip this step.

```
cdk bootstrap 
```

At this point you can now synthesize the CloudFormation template for this project.

```
cdk synth
```

## Deploy to your AWS Account

Confirm you have valid credentials to the correct AWS account by running the following CLI command:

```
aws sts get-caller-identity
```

Make sure the output shows the identity you expect for the Account that will get the deployment.

License the AIs that will be used in this project; they are:

- Anthropic Claude 4 – Sonnet
- Anthropic Claude 4.5 – Sonnet
- Anthropic Claude 4.5 – Haiku

This is done at BedRock, after using them on the playground once.

Once you are bootstrapped and summarized the project, you can deploy. Deploying is as simple as running the command below.

```
cdk deploy --all --require-approval=never
```

(OPTIONAL) If you need to access Amazon Bedrock cross-account, you can optionally provide the ARN to an IAM Role that our Lambda 
functions will assume before invoking Bedrock APIs:

```
cdk deploy --all --require-approval=never --context BEDROCK_XACCT_ROLE=arn:aws:iam::XXX:role/YOUR_XACCT_ROLE
```

After deployment is completed you should see some output values that are required by the Frontend. Make note of them
before you begin deploying the Frontend.

Example outputs:

```
BackendStack.ThreatModelGenerateAllThreatsDataBucketNameDBF1C04D = backendstack-threatmodeldatabucketdxxxx-yyy
BackendStack.ThreatModelGraphQLEndpointA93404B8 = https://abc123.appsync-api.us-east-1.amazonaws.com/graphql
BackendStack.ThreatModelUserPoolIdentityPoolId106951F9 = us-east-1:xxx-yyy-zzz-...
BackendStack.ThreatModelUserPoolUserPoolClientIdB9EE2A87 = 123abc...
BackendStack.ThreatModelUserPoolUserPoolId9919005E = us-east-xyz...
```

*ATTENTION:* Do not forget to enable model access before attempting to use the application.

## Configure Examples for Diagram Describer

Part of the process of extracting threats involves describing your architectural diagrams as a Data Flow Diagram (DFD).

In order to understand the way you create your diagrams, the `Diagram Describer` process uses the Few Shot prompting 
technique, which requires you to provide one or more examples.

As a sample, we offer the architectural diagram of this prototype along with its description as a DFD. Feel free to use
it or even better, to create your own examples.

Create folders named "genai_core_examples/diagram_describer/" inside the DataBucket to upload the samples.

You should upload the pairs of diagram + description to a specific location in the data bucket. It is paramount that each pair has the same name with only the extensions changing.

Good:

```
my_arch.png
my_arch.png.description
```

Bad:

```
myarch.png
my_arch_description.txt
```

**ATTENTION:** You must upload at least one pair of examples before running the application, otherwise the process will 
fail silently (no error message is displayed in the frontend).

## Developing (Optional)

If you wish to make changes to this project, you can perform any code alterations and re-deploy the Backend stack.

If you wish to run tests, you may execute unit tests by running the command below from the root folder of this project:

```
PYTHONPATH="backend/api/resolvers/main:backend/genai_core:backend/api/shared" pytest tests/unit
```

---

## Front-End Stack

This repository contains a base web application. It uses [Vite](https://vitejs.dev/) + [React](https://react.dev/). To deploy you will run a basic CDK stack using [Amazon S3](https://aws.amazon.com/s3/) and [Amazon Cloudfront](https://aws.amazon.com/cloudfront/) with [AWS WAF](https://aws.amazon.com/waf/) for security.

## Requirements

In order to run and deploy this project, you need to have installed:

- AWS CLI. Refer to [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- AWS Credentials configured in your environment. Refer to [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- Node >= 18.x.x [Installing Node and NPM](https://docs.aws.amazon.com/pt_br/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html)
- AWS CDK. Refer to [Getting started with the AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
- Exit the .venv mode

You also need to have the proper backend stack for your prototype deployed into your account, as well as a valid user configured in [Amazon Cognito](https://aws.amazon.com/cognito/).

Make sure to deploy the frontend using the same configuration option as your backend.

---

## Developing and running locally

### Configuring your environment

In a terminal, run:

```shell
cd webapp/
```

Inside the `webapp/` folder, create a file named `.env`. Copy the environment displayed below and replace the property values with the outputs from your deployed backend stack. (You can ask an AI for help to assemble this.)

```properties
VITE_APP_NAME="Threat Modeling Platform"
VITE_AWS_REGION="us-east-1"
VITE_AUTH_MODE="userPool"
VITE_COGNITO_USER_POOL_ID="<COGNITO_USER_POOL_ID>"
VITE_COGNITO_USER_POOL_CLIENT_ID="<COGNITO_USER_POOL_CLIENT_ID>"
VITE_COGNITO_IDENTITY_POOL_ID="<COGNITO_IDENTITY_POOL_ID>"
VITE_DATA_BUCKET_NAME="<S3_BUCKET_NAME>"
VITE_GRAPHQL_ENDPOINT="<APP_SYNC_ENDPOINT>"
```

### Developing with dev mode

From the `webapp/` folder, you can run the following command in a terminal to run the app in development mode:

```shell
npm i
npm run dev -- --host {YOUR_IP or 0.0.0.0}
```

Open [http://localhost:5173/](http://localhost:5173/) to view it in your browser.

The page will reload when you make changes. You may also see any lint errors in the console.

### Developing with watch and hot reloading (Optional)

In one terminal window, run:

```shell
npm run watch
```

In another window, run:

```shell
npm run preview
```

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules. It builds the app for production to the `dist` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

---

### Updating GraphQL statements and types

If you update the GraphQL schema in the backend, you will most likely need to update its
representation in the frontend app.

To do so simply run:

```
npx @aws-amplify/cli codegen statements --apiId <GRAPHQL_API_ID_FROM_BACKEND_DEPLOY> --region <REGION_YOU_DEPLOYED_BACKEND_TO>
npx @aws-amplify/cli codegen types --apiId <GRAPHQL_API_ID_FROM_BACKEND_DEPLOY> --region <REGION_YOU_DEPLOYED_BACKEND_TO>
```

For additional details on codegen, and how to use it with Amplify see
[Client code generation](https://docs.amplify.aws/gen1/react/tools/cli-legacy/client-codegen/#workflows) on Amplify
docs.

## Deploying the app

### Configure your environment

Make sure your webapp environment is configured by creating the `.env` file inside the `webapp/` folder.

The required properties are:

```properties
VITE_APP_NAME="Threat Modeling Platform"
VITE_AWS_REGION="<REGION_NAME>"
VITE_AUTH_MODE="userPool"
VITE_COGNITO_USER_POOL_ID="<COGNITO_USER_POOL_ID>"
VITE_COGNITO_USER_POOL_CLIENT_ID="<COGNITO_USER_POOL_CLIENT_ID>"
VITE_COGNITO_IDENTITY_POOL_ID="<COGNITO_IDENTITY_POOL_ID>"
VITE_DATA_BUCKET_NAME="<S3_BUCKET_NAME>"
VITE_GRAPHQL_ENDPOINT="<APP_SYNC_ENDPOINT>"
```

You can find the proper values for the environment in your backend stack deployment outputs on the CloudFormation console.

### Dependencies

Move to the root folder (`frontend/`).

Use either [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/getting-started/install) to install the required dependencies.

```
npm install
```

or

```
yarn
```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

This will simply generate and print to stout the CloudFormation Template describing the resources. If this succeeds you are ready to deploy.

### Deployment

You can deploy the application stack by running:

```shell
cdk deploy --require-approval=never
```

This command will build the Web Application under the `webapp/` folder and deploy it to an Amazon S3 bucket. The application is served via an Amazon Cloudfront distribution protected by a Amazon WAF WebAcl distribution. If you wish to change and redeploy your application, you can run multiple deployment commands.

The URL for your application will be printed to your terminal at the end of the process, but you can always check it again on the CloudFront's console.


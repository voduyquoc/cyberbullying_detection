## Initial AWS Setup

Create an [AWS account](https://aws.amazon.com/free) with your email.

Create an [IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) with `AdministratorAccess` permission. This user acts as the admin for the project and will be used to create the infrastructure. However when the infrastructure is created each service will have its own IAM role with the least required permissions.

Log in to AWS by using IAM user account above.

Create an [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for the user. This will give you the `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY` which you'll need to configure the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) later. Access keys are secret, just like a password. Don’t share them.
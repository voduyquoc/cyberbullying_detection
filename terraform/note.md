terraform fmt

terraform init

terraform plan -var-file=vars/prod.tfvars

terraform apply -var-file=vars/prod.tfvars

terraform destroy -var-file=vars/prod.tfvars
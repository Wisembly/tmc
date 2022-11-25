# Locust

### Install

```bash
terraform init
export SCW_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXX"
export SCW_SECRET_KEY="xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Launch

```bash
terraform apply -var="tasks_url=https://gist.githubusercontent.com/guillaumepotier/1cde30986851e7a915e0ddce57c997f5/raw/4fda21ad5d4d7b1d054b58bd8f7900d3de71d0ed/tasks.py" -var="locust_username=guillaume" -var="locust_password=wisembly" -var="workers_nb=3"
```


## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_scaleway"></a> [scaleway](#provider\_scaleway) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_master"></a> [master](#module\_master) | ./modules/master |  |
| <a name="module_worker"></a> [worker](#module\_worker) | ./modules/worker |  |

## Resources

| Name | Type |
|------|------|
| [scaleway_instance_image.locust](https://registry.terraform.io/providers/scaleway/scaleway/latest/docs/data-sources/instance_image) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_locust_password"></a> [locust\_password](#input\_locust\_password) | Locust Password | `string` | n/a | yes |
| <a name="input_locust_username"></a> [locust\_username](#input\_locust\_username) | Locust Username | `string` | n/a | yes |
| <a name="input_tasks_url"></a> [tasks\_url](#input\_tasks\_url) | Where to download the tasks | `string` | n/a | yes |
| <a name="input_workers_nb"></a> [workers\_nb](#input\_workers\_nb) | n/a | `number` | `5` | no |

## Outputs

No outputs.

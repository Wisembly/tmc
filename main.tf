terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  zone            = "fr-par-1"
  region          = "fr-par"
  project_id      = "bfb14d1d-3b06-40df-8467-f2569e3f3db7"
}

data "scaleway_instance_image" "locust" {
  image_id = "eb32085c-a9fa-4477-b717-11553fc79e99"
}

module "master" {
  source = "./modules/master"
  startup_script = templatefile(
    "./startup-master.sh",
    {
      "TASKS_URL" = var.tasks_url
      "LOCUST_TYPE" = "master"
      "LOCUST_USERNAME"               = var.locust_username
      "LOCUST_PASSWORD"               = var.locust_password
    }
    )
  image_id = data.scaleway_instance_image.locust.id
}

module "worker" {
  source = "./modules/worker"
  startup_script = templatefile(
    "./startup-worker.sh",
    {
      "TASKS_URL" = var.tasks_url
      "LOCUST_TYPE" = "worker"
      "LOCUST_MASTER_IP" = module.master.locust_master_ip
    }
    )
  image_id = data.scaleway_instance_image.locust.id
  workers_number = var.workers_nb
  depends_on = [
    module.master
  ]
}

terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "XPTO"

    workspaces {
      name = "devops-XPTO"
    }
  }
}

##############

locals {
    pyapi-hello_labels = {
        app = "pyapi-hello"
        container_port = 8181
    }
}

##############

resource "kubernetes_namespace" "pyapi-hello-ns" {
    metadata {
        name = "${local.pyapi-hello_labels["app"]}-ns"
    }
}

##############

resource "kubernetes_service" "pyapi-hello-srv" {
    depends_on = [kubernetes_namespace.pyapi-hello-ns]

    metadata {
        name = "${local.pyapi-hello_labels["app"]}-srv"
        namespace = "${kubernetes_namespace.pyapi-hello-ns.id}"
    }

    spec {
        selector = {
            app = local.pyapi-hello_labels["app"]
        }
        port {
            protocol    = "TCP"
            port        = local.pyapi-hello_labels["container_port"]
            target_port = local.pyapi-hello_labels["container_port"]
        }
        type = "ClusterIP"
    }
}

##############

variable "k8s_dpl_qty_replicas" {
  type = number
}

variable "k8s_dpl_docker_image" {
  type = string
}

resource "kubernetes_deployment" "pyapi-hello-dpl" {
    depends_on = [kubernetes_service.pyapi-hello-srv]

    metadata {
        namespace = "${kubernetes_namespace.pyapi-hello-ns.id}"
        name = "${local.pyapi-hello_labels["app"]}-dpl"
    }

    spec {
        replicas = var.k8s_dpl_qty_replicas

        selector {
            match_labels = local.pyapi-hello_labels
        }

        template {

            metadata {
                labels = local.pyapi-hello_labels
            }

            spec {
                container {
                    image = var.k8s_dpl_docker_image
                    name  = local.pyapi-hello_labels["app"]
                    port {
                        container_port = local.pyapi-hello_labels["container_port"]
                    }
                }
            }
        }
    }
}
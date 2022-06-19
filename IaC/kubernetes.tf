terraform {
    required_providers {
        kubernetes = {
            source = "hashicorp/kubernetes"
        }
    }
}

variable "k8s_host" {
    type = string
}

variable "client_certificate" {
    type = string
}

variable "client_key" {
    type = string
}

variable "cluster_ca_certificate" {
    type = string
}

provider "kubernetes" {
    host = var.k8s_host

    client_certificate     = "${file("${var.client_certificate}")}"
    client_key             = "${file("${var.client_key}")}"
    cluster_ca_certificate = "${file("${var.cluster_ca_certificate}")}"
}
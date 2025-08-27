terraform {
  cloud {
    organization = "fdelu"
    workspaces {
      name = "auto-reservation"
    }
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.41.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "azuread" {
}

resource "azurerm_resource_group" "rg" {
  name     = local.app_name
  location = "brazilsouth"
}

data "azuread_user" "admin" {
  mail = "felipedelu@outlook.com"
}

data "azurerm_client_config" "config" {}

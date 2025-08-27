resource "azurerm_static_web_app" "swa" {
  name                = local.app_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = "eastus2"
  sku_tier            = "Free"
  sku_size            = "Free"
}

resource "random_password" "db_password" {
  length = 32
}

resource "azurerm_mssql_server" "sql_server" {
  name                          = local.app_name
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = azurerm_static_web_app.swa.location
  version                       = "12.0"
  administrator_login           = local.app_name
  administrator_login_password  = random_password.db_password.result
  public_network_access_enabled = false

  azuread_administrator {
    login_username = data.azuread_user.admin.display_name
    object_id      = data.azuread_user.admin.object_id
  }
}

resource "azurerm_mssql_database" "sql_database" {
  name                 = local.app_name
  sku_name             = "Free"
  server_id            = azurerm_mssql_server.sql_server.id
  collation            = "Modern_Spanish_CI_AS"
  storage_account_type = "Local"
}


# resource "azurerm_mssql_firewall_rule" "allow_swa" {
#   name             = azurerm_static_web_app.swa.name
#   server_id        = azurerm_mssql_server.sql_server.id
#   start_ip_address = 
#   end_ip_address   = 
# }

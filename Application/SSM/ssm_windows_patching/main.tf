#This script contains the module
module "ssm_patching_maintenance_window" {
  source = "./modules/ssm_module"

  name                               = var.name
  schedule                           = var.schedule
  maintenance_window_duration        = var.maintenance_window_duration
  maintenance_window_cutoff          = var.maintenance_window_cutoff
  resource_type                      = var.resource_type
  task_type                          = var.task_type
  task_arn                           = var.task_arn
  reboot_option                      = var.reboot_option
  window_target                      = var.window_target
  task_install_priority              = 1
  service_role_arn                   = var.service_role_arn
  notification_arn                   = var.notification_arn
  notification_events                = var.notification_events
  notification_type                  = var.notification_type
  max_concurrency                    = var.max_concurrency
  max_errors                         = var.max_errors
  operation_type                     = var.operation_type
  s3_bucket_name                     = var.s3_bucket_name
  s3_bucket_prefix_install_logs      = var.s3_bucket_prefix_install_logs
}

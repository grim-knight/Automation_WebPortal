#Configuring the maintenance window
resource "aws_ssm_maintenance_window" "install_window" {
  name     = var.name                        #  maintenance window name
  schedule = var.schedule                    #specify cron job for execution
  duration = var.maintenance_window_duration # duration of maintenance window
  cutoff   = var.maintenance_window_cutoff   # specify at cut off parameter for stopping Systems manager to stop passing command
}

#Assigning the targets for the maintenance window
resource "aws_ssm_maintenance_window_target" "target_install" {
  window_id     = aws_ssm_maintenance_window.install_window.id
  resource_type = var.resource_type
  targets { # specify target patch group key value pair
    key    = var.window_target.key
    values = [var.window_target.values]
  }
}

#Assigning the RunCommandTask to the maintenance windoow -> AWS-InstallWindowsUpdates
resource "aws_ssm_maintenance_window_task" "task_install_patches" {
  name             = var.name
  window_id        = aws_ssm_maintenance_window.install_window.id
  task_type        = var.task_type
  task_arn         = var.task_arn # specify the patch command
  priority         = var.task_install_priority
  service_role_arn = var.service_role_arn
  max_concurrency  = var.max_concurrency
  max_errors       = var.max_errors

  targets {
    key    = "WindowTargetIds"
    values = aws_ssm_maintenance_window_target.target_install.*.id
  }

  task_invocation_parameters {
    run_command_parameters {
      parameter {
        name   = "Action"
        values = [var.operation_type]
      }

      output_s3_bucket     = var.s3_bucket_name # specify bucket for log output
      output_s3_key_prefix = var.s3_bucket_prefix_install_logs
      service_role_arn     = var.service_role_arn
      notification_config {
        notification_arn    = var.notification_arn # Specify your SNS topic ARN here
        notification_events = [var.notification_events]
        notification_type   = var.notification_type
      }
    }
  }
}
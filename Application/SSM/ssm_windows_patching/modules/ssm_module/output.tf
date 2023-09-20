output "maintenance_window" {
  value = aws_ssm_maintenance_window.install_window
}
output "targets" {
  value = aws_ssm_maintenance_window_target.target_install.*.id
}
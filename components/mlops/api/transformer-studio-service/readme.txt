
# Please put the config file accoring to the use in VM or in local. in case of local use put the config/local/config.ini to local/config.ini.


#### This is for deploying the service file
sudo systemctl status transformer_studio_service.service
# ● transformer_studio_service.service - transformer_studio_service (Dev)
#   Loaded: loaded (/etc/systemd/system/transformer_studio_service.service; enabled; vendor preset: disabled)
#   Active: active (running) since Tue 2023-05-09 09:05:44 IST; 2 days ago

sudo systemctl stop transformer_studio_service.service

sudo systemctl status transformer_studio_service.service
# ● transformer_studio_service.service - transformer_studio_service (Dev)
#   Loaded: loaded (/etc/systemd/system/transformer_studio_service.service; enabled; vendor preset: disabled)
#   Active: inactive (dead) since Thu 2023-05-11 14:51:26 IST; 4s ago

sudo systemctl disable transformer_studio_service.service
# Removed symlink /etc/systemd/system/multi-user.target.wants/transformer_studio_service.service.

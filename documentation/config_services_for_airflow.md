    sudo nano /etc/systemd/system/airflow-webserver.service

<br>

    [Unit]
    Description=Airflow webserver daemon
    After=network.target postgresql.service
    Wants=postgresql.service

    [Service]
    Environment="PATH=/home/wolfframio/miniforge3/envs/airflow_env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    Environment="AIRFLOW_HOME=/home/wolfframio/Coding/Airflow"
    User=wolfframio
    Group=wolfframio
    Type=simple
    ExecStart=/home/wolfframio/miniforge3/envs/airflow_env/bin/airflow webserver
    Restart=always
    RestartSec=5s

    [Install]
    WantedBy=multi-user.target

<br>

    sudo nano /etc/systemd/system/airflow-scheduler.service

<br>

    [Unit]
    Description=Airflow scheduler daemon
    After=network.target postgresql.service
    Wants=postgresql.service

    [Service]
    Environment="PATH=/home/wolfframio/miniforge3/envs/airflow_env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    Environment="AIRFLOW_HOME=/home/wolfframio/Coding/Airflow"
    User=wolfframio
    Group=wolfframio
    Type=simple
    ExecStart=/home/wolfframio/miniforge3/envs/airflow_env/bin/airflow scheduler
    Restart=always
    RestartSec=5s

    [Install]
    WantedBy=multi-user.target

### Recargamos la configuración de systemd
   
    sudo systemctl daemon-reload

### Habilitamos los servicios para que se inicien con el sistema

    sudo systemctl enable airflow-webserver
    sudo systemctl enable airflow-scheduler

### Iniciamos los servicios
    
    sudo systemctl start airflow-webserver
    sudo systemctl start airflow-scheduler  

### Verificar el estado del webserver

    sudo systemctl status airflow-webserver

### Verificar el estado del scheduler

    sudo systemctl status airflow-scheduler

### Ver logs del webserver

    sudo journalctl -u airflow-webserver

### Ver logs del scheduler

    sudo journalctl -u airflow-scheduler


### Si por alguna razón necesitas detenerlos:

    sudo systemctl stop airflow-webserver

    sudo systemctl stop airflow-scheduler

### Y si necesitas reiniciarlos:

    sudo systemctl restart airflow-webserver

    sudo systemctl restart airflow-scheduler
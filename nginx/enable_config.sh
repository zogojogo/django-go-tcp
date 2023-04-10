sudo rm /etc/nginx/sites-enabled/entry_task_nginx
sudo rm /etc/nginx/sites-available/entry_task_nginx
sudo cp ./entry_task_nginx /etc/nginx/sites-available/
sudo ln /etc/nginx/sites-available/entry_task_nginx /etc/nginx/sites-enabled/entry_task_nginx
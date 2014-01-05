sudo mysql < reset.sql
python local_manage.py syncdb;
python local_manage.py migrate truespeak;

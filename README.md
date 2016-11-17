# slack-safari

Prep:
create + activate venv
pip install -r requirements.txt 

Create a bot / Slack token:
http://my.slack.com/apps/manage/custom-integrations

Set token in env (shell or in dotfile like .bashrc)
export SLACK=xyz 

Put post.py in cronjob 
I typically call Safaribook's API every hour, caching already sent titles in a shelve file (books)

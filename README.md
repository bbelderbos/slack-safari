# slack-safari

This project uses Python 3

First create a Python virtual env: 

	virtualenv venv
	(might need -p python3)

	source venv/bin/activate

Install requirements:
	
	pip install -r requirements.txt 

Get a Slack token for the bot [here](http://my.slack.com/apps/manage/custom-integrations).

Set the token in an environment variable:

	export SLACK=xyz 

Put the safaribot.py in an hourly (or daily) cronjob.

On my server I installed py3 in my $HOME so I had to export the PYTHONPATH env variable too:

	export SLACK=xyz && export PYTHONPATH=<path-to>/python<version>/site-packages && 
		cd <path-to>/slack_safari && <path-to>/python3.5 safaribot.py

Enjoy!

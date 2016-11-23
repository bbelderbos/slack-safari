# slack-safari

## Intro

This script checks the [Safaribooksonline](http://safaribooksonline.com) API for new books and posts them to one or more channels:

- Create a bot user
- Add the bot to one or more channels: a channel with the string 'safaribooks' in it will receive all updates
- Channels named like 'string-string' will do a title text match on 'string string', so adding the bot to a channel called 'data-science' will receive all new books with "data science" in the lowercase'd title, e.g. "Data Science with Java"

Each book has links to safaribooksonline (book page, and to queue it) and Amazon (attempt)

## Deployment 

First create a Python virtual env (this project requires python3, it's time to move on, not?): 

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

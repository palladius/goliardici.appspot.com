deploy-to-appengine:
	@echo Deploying app to AppEngine: 
	appcfg.py --oauth2 update .

deploy-locale:
	@echo deploy locally to 8080..
	dev_appserver.py --port 3000 .

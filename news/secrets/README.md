# Secrets

Secrets are passed via environment variables.  These environment variables may
need to be declared in the following places:

- `news/Makefile`
- `.github/workflows/build-and-deploy.yaml`
- In GitHub at `https://github.com/donmccaughey/donm_cc/settings/secrets/actions`
- `news/aws/create-container-service-deployment.template.json`  (generated by the makefile)
- `news/tmp/.env` (generated by the makefile)
- PyCharm Run/Debug Configuration for the extractor


## `REDDIT_PRIVATE_RSS_FEED` - Reddit private RSS feed

Found on the [RSS Feeds](https://www.reddit.com/prefs/feeds/) preferences page.
Stored in `reddit-private-rss-feed.txt`.
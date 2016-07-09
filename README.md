# TCR 2016 border crossings

This repo holds the code for
[borders.transcontinental.cc](http://borders.transcontinental.cc), a web
site that provides a map of the
[Transcontinental Race](http://www.transcontinental.cc/) (TCR) 2016 border
crossings, with information on each, and allowing people to comment on
them.

## TODO

### High priority

* Add comment display per crossing.
* Add backend comment addition.
* Wire up Submit button.
* Following commenting, add the new comment to the list.
* Add minimal / textual UI for crossings.
* Some notes on crossings have URLs in them. Turn them into links.
* Work on the admin interface to allow editing of comments. A downside here
  is that you currently need to know the id of the crossing you want to
  examine comments for. That's because the crossings are not in the db.

### Can wait a little

* <s>Deploy.</s>
* Get feedback from others, especially people with different browsers or OS.
* <s>Ask Shankie to point the subdomain at the deployed server.</s>
* Ensure the site restarts if the host VM is rebooted.
* Put a border around the panel that holds the Overview & Comments tabs.
* Show admin people how to access the admin UI & make them accounts.

### Low priority / questionable

* Add name tooltips to the crossing markers.
* Add an icon that when tapped zooms the map to show where you are.
* Get full list of crossings into app and store it into sqlite? This would
  then mean people would have to stop adding crossing details to the Google
  docs spreadsheet. Probably better to leave this alone.
* Add a refresh button on the comment list?
* Possibly add login (likely via Python social auth).
* Restrict the ability to add a comment to logged-in users?

## BUGS

* Does the Comments tab stay selected sometimes when it shouldn't?
* Disabling the comment submit button disables the comment `textarea`. This may be a FF thing.

## Resolved

* <s>Should this be deployed on Ivan's linode server?</s> No.
* <s>Should we use `borders.transcontinental.cc`,
  `crossings.transcontinental.cc`, or what?</s>

/*
** JavaScript for the user page.
**
** $Id$
*/

/*
dojo.io.bind({
    url: "http://foo.bar.com/processForm.cgi",

  load: function(type, evaldObj){ /* do something * },
    formNode:
  document.getElementById("formToSubmit")
});
*/

function hide_subscriptions() {
  /* the subscription list */
  dojo.lfx.html.fadeHide("my_subscriptions_wrapper", 1).play();

  /* the form for adding a new subscription */
  dojo.lfx.html.fadeHide("add_feed", 1).play();
}

function show_subscriptions () {
  /* the subscription list */
  dojo.lfx.html.fadeShow("my_subscriptions_wrapper", 1).play();

  /* the form for adding a new subscription */
  dojo.lfx.html.fadeShow("add_feed", 1).play();
}

function hide_feed_viewer() {
  dojo.lfx.html.fadeHide("feed_viewer", 1).play();
}

function show_feed_viewer() {
  /* show the feed viewer */
  var viewer_node = clear_feed_viewer();
  dojo.lfx.html.fadeShow(viewer_node, 1).play();

  return viewer_node;
}

/*
** CURRENT QUEUE
*/

/* returns a new node to be used as an icon to represent the mimetype */
function get_mimetype_icon(mimetype) {
	icon = document.createElement('img');

  if (mimetype.match("^audio/")) {
	icon.setAttribute('src', '/static/images/sound.png');
  } 
  else if (mimetype.match('^video/') || mimetype.match('shockwave') || mimetype.match('flash') )  {
	icon.setAttribute('src', '/static/images/film.png');
  } 
  else {
	icon = document.createTextNode(mimetype);
  }

  return icon;
}

/* tell the server to remove something from the queue */
function do_remove_from_queue(id) {

  show_status("Removing ...");

  dojo.io.bind({ 
	url: "queue/" + id + "/",
	handler: remove_from_queue_callback,
	method: "DELETE",
	});
  return false;
}

/* remove the item from the display */
function remove_item_from_queue(id) {
  dojo.debug('remove_item_from_queue ' + id);
  var queue_node = dojo.byId("queue");
  var node_id = "queue_item_" + id;
  var item_node = dojo.byId(node_id);

  if (item_node) {
	queue_node.removeChild(item_node);
	if (queue_node.childNodes.length == 0) {
	  set_queue_empty();
	}
  }
  else {
	dojo.debug('Could not find node ' + node_id);
  }
  return false;
}

/* called when the server responds after removing something from the queue */
function remove_from_queue_callback(type, data, evt) {
  if (type == "load") {
	
	payload = dojo.json.evalJson(data);

	if (payload["error"] != "") {
	  show_error("queue", payload["error"]);
	}

	to_remove = payload['remove_from_queue'];
	dojo.debug('remove_from_queue_callback');
	dojo.debugShallow(to_remove);
	for (var i=0; i < to_remove.length; i++) {
	  id = to_remove[i];
	  dojo.debug('Removing ' + id);
	  remove_item_from_queue(id);
	}

  } else if (type == "error") {
	dojo.debugShallow(data);
  }

  clear_status();

  return false;
}

/* update the queue */
function do_show_queue() {

  show_status("Updating queue ...");

  dojo.io.bind({ 
	url: "queue/",
	handler: show_queue_callback,
	method: "GET",
	});
  return false;
}

function show_queue() {
  if (initial_queue.length == 0) {
	set_queue_empty();
  }
  else {
	for (var i=0; i < initial_queue.length; i++) {
	  insert_entry_into_queue(initial_queue[i], 0);
	}
  }

  /* show the user feeds */
  for (i=0; i < initial_subscriptions.length; i++) {
	insert_feed_into_list(initial_subscriptions[i]);
  }
}

/* called when the server responds to a request for the queue contents */
function show_queue_callback(type, data, evt) {
  if (type == "load") {
	
	payload = dojo.json.evalJson(data);

	if (payload["error"] != "") {
	  show_error("queue", payload["error"]);
	}

	/* remember the response */
	initial_queue = payload['queue'];

	/* clear the current contents */
	var queue_node = dojo.byId("queue");
	queue_node.innerHTML = '';

	/* add the contents back */
	show_queue();

  } else if (type == "error") {
	dojo.debugShallow(data);
  }

  clear_status();

  return false;
}

function summarize_string(/*string*/s, /*number*/len) {
// summary:
//	Truncates 'str' after 'len' characters and appends periods as necessary so that it ends with "..."

	if(!len || s.length <= len){
		return s; // string
	}

	return s.substring(0, len).replace(/\.+$/, "") + "..."; // string
}

/* called to add a new entry to the display of the queue */
function insert_entry_into_queue(entry, atFront) {
  var queue_node = dojo.byId("queue");
  
  var new_item = document.createElement("div");
  new_item.setAttribute("class", "queue_item");
  new_item.setAttribute('id', 'queue_item_' + entry['id']);
  
  /* title */
  var item_title = document.createElement("div");
  item_title.setAttribute("class", "item_title");
  
  var item_link = document.createElement('a');
  item_link.setAttribute('href', entry['link']);
  item_link.setAttribute('target', '_blank');
  item_link.setAttribute('id', 'item_link_' + entry['id']);
  item_link.appendChild(document.createTextNode(entry['podcast_name']));
  item_link.appendChild(document.createTextNode(' - '));
  item_link.appendChild(document.createTextNode(entry['title']));
  item_title.appendChild(item_link);
  new_item.appendChild(item_title);

  var pubdate = document.createElement('div');
  pubdate.setAttribute('class', 'item_pubdate');
  pubdate.appendChild(document.createTextNode(entry['pubdate']));
  new_item.appendChild(pubdate);
  
  /* summary / body */

  var item_summary = document.createElement('div');
  item_summary.setAttribute('class', 'item_summary');
  short_summary = dojo.string.summary(entry['summary'], 100);
  item_summary.appendChild(document.createTextNode(short_summary));
  new_item.appendChild(item_summary);

  /* add action buttons to remove queue items */

  var delete_link = document.createElement('a');
  delete_link.setAttribute('href', '');
  delete_link.setAttribute('onclick', 'return do_remove_from_queue(' + entry['id'] + ')');
  delete_link.setAttribute('class', 'delete_link');
  delete_icon = document.createElement('img');
  delete_icon.setAttribute('src', '/static/images/cancel.png');
  delete_icon.setAttribute('alt', 'Remove from queue');
  delete_icon.setAttribute('title', 'Remove from queue');
  delete_link.appendChild(delete_icon);
  new_item.appendChild(delete_link);
  
  /* enclosure */
  var enclosure_link = document.createElement('a');
  enclosure_link.setAttribute('class', 'enclosure_link');
  enclosure_link.setAttribute('href', entry['enclosure_url']);
  
  play_icon = get_mimetype_icon(entry['enclosure_mimetype']);
  if (play_icon) {
    play_icon.setAttribute('alt', 'Play now');
    play_icon.setAttribute('title', 'Play now');
  }
  enclosure_link.appendChild(play_icon);
  new_item.appendChild(enclosure_link);
  
  /* put the item into the queue display */

  if (atFront) {
	first_child = queue_node.childNodes[0];
	queue_node.insertBefore(new_item, first_child);
  }
  else {
	queue_node.appendChild(new_item);
  }

  /* Construct a tooltip to show the full summary. */

  var tooltip = dojo.widget.createWidget('Tooltip',
										 {id:'tooltip_' + entry['id'],
											 connectId:'item_link_' + entry['id'],
											 caption:entry['summary'],
											 });
  new_item.appendChild(tooltip.domNode);
}

/* the user has nothing in their queue, so display a message to that effect */
function set_queue_empty() {
  var queue_node = dojo.byId("queue");
  queue_node.innerHTML = '<div id="empty_queue_item" class="queue_item">Your queue is empty.</div>';
}

/*
** Global variable that holds the entries retrieved as part of the
** feed the user has clicked on.  We use this because there are a
** bunch of attributes for each entry and it is easier to refer to the
** entry by id than pass all of those values around.
*/
var podcast_entries = {};

/* Tell the server we want to add something to the queue. */
function do_add_to_queue(podcast_id, entry_id) {
  var entry = podcast_entries[entry_id];

  show_status("Adding " + entry['title'] + " ...");

  enclosure = entry['enclosures'][0];
  author_detail = entry['author_detail'];
  if (author_detail) {
	author_name = author_detail['name'];
	author_email = author_detail['email'];
  } else {
	author_name = entry['author'];
	if (author_name) {
	  author_email = 'n/a';
	} else {
	  author_name = '';
	  author_email = '';
	}
  }

  if (entry['link']) {
	entry_link = entry['link'];
  } else {
	entry_link = enclosure['href'];
  }

  dojo.io.bind({ 
	url: "queue/",
	handler: add_to_queue_callback,
	method: "POST",
	content:{podcast:podcast_id,
             title:entry['title'],
		     summary:entry['summary'],
		     link:entry_link,
		     author_name:author_name,
		     author_email:author_email,
		     item_enclosure_url:enclosure['href'],
		     item_enclosure_mime_type:enclosure['type'],
		     item_enclosure_length:enclosure['length'],
		     },
	});

  return false;
}

/* called when we get the json response from the server when an item is added to the queue */
function add_to_queue_callback(type, data, evt) {
  if (type == "load") {
	
	payload = dojo.json.evalJson(data);

	/* errors *

	if (payload["error"] != "") {
	  show_error("queue", payload["error"]);
	}

	/* remove the empty queue message */
	var empty_queue = dojo.byId('empty_queue_item');
	if (empty_queue) {
	  var queue_node = dojo.byId("queue");
	  queue_node.removeChild(empty_queue);
	}

	/* add the response to the front of the queue */

	queue_contents = payload['add_to_queue'];
	for (var i=0; i < queue_contents.length; i++) {
	  item = queue_contents[i];
	  insert_entry_into_queue(item, 1);
	}

  } else if (type == "error") {
	dojo.debugShallow(data);
  }
  clear_status();

}

/* Insert a feed element into the list of feeds of the user. */
function insert_feed_into_list(feed_info) {
  var feed_node_id = 'feed_' + feed_info['id'];
  var feed_node = dojo.byId(feed_node_id);
  if (! feed_node) {
	var feed_id = feed_info['id'];
	var list_node = dojo.byId("my_subscriptions");
	var new_item = document.createElement("li");
	new_item.setAttribute('id', feed_node_id);
	var new_link = document.createElement("a");
	new_link.setAttribute("onclick", "return show_feed_by_id(" + feed_id + ", '" + escape(feed_info['name']) + "', '" + feed_info['home_url'] + "')");
	new_link.setAttribute("href", "");
	new_link.appendChild(document.createTextNode(feed_info["name"]));
	show_icon = document.createElement('img');
	show_icon.setAttribute('src', '/static/images/feed_magnify.png');
	show_icon.setAttribute('alt', 'Show feed contents');
	show_icon.setAttribute('title', 'Show feed contents');
	new_link.appendChild(show_icon);
	new_item.appendChild(new_link);

	monitor_icon = document.createElement('a');
	monitor_icon.setAttribute('href', feed_info['feed_url']);
	monitor_icon.setAttribute('target', '_blank');
	monitor_icon.setAttribute('alt', 'Original feed');
	monitor_icon.setAttribute('title', 'Original feed');
	monitor_icon.innerHTML = '<img src="/static/images/feed.png" />';
	new_item.appendChild(monitor_icon);

	home_icon = document.createElement('a');
	home_icon.setAttribute('href', feed_info['home_url']);
	home_icon.setAttribute('target', '_blank');
	home_icon.setAttribute('alt', 'Visit home page');
	home_icon.setAttribute('title', 'Visit home page');
	home_icon.innerHTML = '<img src="/static/images/house.png" />';
	new_item.appendChild(home_icon);

	/*
	feed_icon = document.createElement('a');
	feed_icon.setAttribute('href', feed_info['feed_url']);
	feed_icon.setAttribute('target', '_blank');
	feed_icon.setAttribute('alt', 'Direct link to feed');
	feed_icon.setAttribute('title', 'Direct link to feed');
	feed_icon.innerHTML = '<img src="/static/images/feed-14x14.png" />';
	new_item.appendChild(feed_icon);
	*/

	var delete_link = document.createElement('a');
	delete_link.setAttribute('href', '');
	delete_link.setAttribute('onclick', 'return do_remove_feed(' + feed_id + ')');
	delete_link.setAttribute('class', 'delete_link');
	delete_icon = document.createElement('img');
	delete_icon.setAttribute('src', '/static/images/cancel.png');
	delete_icon.setAttribute('alt', 'Remove this subscription');
	delete_icon.setAttribute('title', 'Remove this subscription');
	delete_link.appendChild(delete_icon);
	new_item.appendChild(delete_link);

	list_node.appendChild(new_item);
  }
  return false;
}

/*
** ADD FEED form
*/
function do_add_feed() {
  clear_error("add_feed_results");
  show_status("Loading feed...");

  dojo.io.bind({ 
	url: "subscriptions/",
		handler: add_feed_callback,
		formNode: document.getElementById("add_feed"),
		method:"POST",
		});

  return false;
}

/* called when we get the json response from the server when a feed is added */
function add_feed_callback(type, data, evt) {
  clear_status();

  if (type == "load") {
	
	payload = dojo.json.evalJson(data);
	
	if (payload["error"] != "") {
	  show_error("add_feed_results", payload["error"]);
	}
	else {
	  insert_feed_into_list(payload);
	  hide_subscriptions();
	  show_feed_viewer();
	  populate_feed_viewer(payload['name'], payload['id'], payload["entries"]);
	  clear_error("add_feed_results");
	}
	
  } else if (type == "error") {
	clear_error("add_feed_results");
	show_error("add_feed_results", data);
  }
}

/* tell the server we want to remove a feed from the subscription list */
function do_remove_feed(id) {
  show_status("Removing feed...");
  clear_feed_viewer();
  
  dojo.io.bind({ 
	url: "subscriptions/" + id + "/",
		handler: remove_feed_callback,
		method:"DELETE",
		});

  return false;
}

/* called when we get the json response from the server when a feed is removed */
function remove_feed_callback(type, data, evt) {
  clear_status();

  if (type == "load") {
	
	payload = dojo.json.evalJson(data);
	
	if (payload["error"] != "") {
	  show_error("add_feed_results", payload["error"]);
	}
	else {
	  clear_error("add_feed_results");

	  /* Update the list of feeds */
	  var feed_node_id = 'feed_' + payload['removed'];
	  var feed_node = dojo.byId(feed_node_id);
	  var list_node = dojo.byId("my_subscriptions");
	  list_node.removeChild(feed_node);

	  /* Update the queue, in case one or more items were removed. */
	  do_show_queue();
	}
	
  } else if (type == "error") {
	clear_error("add_feed_results");
	show_error("add_feed_results", data);
  }
}

/*
** SHOW FEEDS form
*/
function show_feed_by_id(id, name, url) {
  dojo.debug('show_feed_by_id ' + id + ' ' + name);

  hide_subscriptions();
  viewer_node = show_feed_viewer();

  /* indicate which podcast we are displaying */
  legend_node = document.createElement('legend');

  home_icon = document.createElement('a');
  home_icon.setAttribute('href', url);
  home_icon.setAttribute('target', '_blank');
  home_icon.setAttribute('alt', 'Visit home page');
  home_icon.setAttribute('title', 'Visit home page');
  home_icon.innerHTML = '<img src="/static/images/house.png" />';
  legend_node.appendChild(home_icon);

  legend_node.appendChild(document.createTextNode(' ' + unescape(name)));

  viewer_node.appendChild(legend_node);

  show_status("Loading feed...");
  dojo.io.bind({ 
	url: "/cast/external/" + id + "/",
		handler: show_feed_by_id_callback,
		method: "GET",
		});
  return false;
}

/* called when server responds to show_feed_by_id */
function show_feed_by_id_callback(type, data, evt) {
  clear_status();

  if (type == "load") {
	payload = dojo.json.evalJson(data);
	if (payload["error"] != "") {
	  show_error("feed_viewer", payload["error"]);
	}
	else {
	  populate_feed_viewer(payload['name'], payload['id'], payload["entries"]);
	}
  }
  else if (type == "error") {
	show_error("feed_viewer", data);
  }
}

/* emtpy and hide the feed_viewer */
function clear_feed_viewer() {
  var node = dojo.byId("feed_viewer");
  /*  dojo.lfx.html.wipeOut(node, 1).play();*/
  node.innerHTML = "";
  return node;
}

/* given a list of entries from the parsed feed, show them */
function populate_feed_viewer(podcast_name, podcast_id, entries) {
  var viewer_node = dojo.byId("feed_viewer");

  /* Add a link to indicate that we are done with this feed */
  done_node = document.createElement('a');
  done_node.setAttribute('href', '');
  done_node.setAttribute('alt', 'Back to subscriptions');
  done_node.setAttribute('title', 'Back to subscriptions');
  done_node.setAttribute('onclick', "return switch_to_subscriptions()");
  done_node.setAttribute('class', 'done');
  done_arrow = document.createElement('img');
  done_arrow.setAttribute('src', '/static/images/text_list_bullets.png');
  done_node.appendChild(done_arrow);
  done_node.appendChild(document.createTextNode(' Subscriptions'));
  viewer_node.appendChild(done_node);
  viewer_node.appendChild(document.createElement('br'));

  if (entries.length == 0) {
	message_node = document.createElement('div');
	message_node.setAttribute('class', 'message');
	message_node.appendChild(document.createTextNode('No entries'));
	viewer_node.appendChild(message_node);
  }
  else {
	/* update our global variable so the code to add to the queue can find the entries */
	podcast_entries = entries;

	for (i=0; i < entries.length; i++) {
	  var entry = entries[i];
	  var entry_node = document.createElement('div');
	  var div_id = 'add_item_' + i;
	  entry_node.setAttribute('class', 'podcast_entry');
	  entry_node.setAttribute('id', div_id);

	  title_node = document.createElement('div');
	  title_node.setAttribute('class', 'podcast_entry_title');

	  add_link = document.createElement('a');
	  add_link.setAttribute('class', 'add_link');
	  add_link.setAttribute('href', '');
	  add_link.setAttribute('onclick', "return do_add_to_queue(" + podcast_id + ", " + i + ")");
	  add_link.setAttribute('alt', 'Add to my queue');
	  add_link.setAttribute('title', 'Add to my queue');
	  add_link.innerHTML = '<img src="/static/images/add.png"/>' + entry['title'] + '</a>';
	  title_node.appendChild(add_link);

	  enclosure = entry['enclosures'][0];
	  enclosure_mime_type = enclosure['type'];
	  enclosure_url = enclosure['href'];
	  var enclosure_link = document.createElement('a');
	  enclosure_link.setAttribute('href', enclosure_url);
	  play_icon = get_mimetype_icon(enclosure_mime_type);
	  play_icon.setAttribute('alt', 'Play now');
	  play_icon.setAttribute('title', 'Play now');
	  enclosure_link.appendChild(play_icon);
	  title_node.appendChild(enclosure_link);

	  /* We only link to the entry if we have a valid link. */
	  if (entry['link']) {
		open_link = document.createElement('a');
		open_link.setAttribute('href', entry['link']);
		open_link.setAttribute('target', '_blank');
		open_link.setAttribute('alt', 'Open');
		open_link.setAttribute('title', 'Open');
		open_link.innerHTML = '<img src="/static/images/link_go.png"/></a>';
		title_node.appendChild(open_link);
	  }

	  entry_node.appendChild(title_node);

	  var pubdate = document.createElement('div');
	  pubdate.setAttribute('class', 'podcast_entry_pubdate');
	  pubdate.appendChild(document.createTextNode(entry['updated']));
	  entry_node.appendChild(pubdate);

	  summary_node = document.createElement('div');
	  summary_node.setAttribute('class', 'podcast_entry_summary');
	  summary_node.appendChild(document.createTextNode(entry['summary']));
	  entry_node.appendChild(summary_node);

	  viewer_node.appendChild(entry_node);
	}
	  
	/* duplicate the "Done" link */
	viewer_node.appendChild(done_node.cloneNode(true));
  }

  dojo.lfx.html.wipeIn(viewer_node, 200).play();
  return false;
}


/*
** ONLOAD
*/
function user_onload() {
  /* show the queue contents */
  var queue_node = dojo.byId("queue");
  queue_node.innerHTML = "";

  show_queue();

  hide_feed_viewer();
  clear_feed_viewer();

  if (document.add_feed.url.value) {
	/* we have a URL, so add it and start showing the contents */
    onload_counter = onload_counter + 1;
	do_add_feed();
  }

  /* give the url field focus */
  /* document.add_feed.url.focus(); */
}


/*
** Hide the feed_viewer and show the subscriptions
*/
function switch_to_subscriptions() {
  hide_feed_viewer();
  show_subscriptions();
  return false;
}

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

/*
** CURRENT QUEUE
*/
function show_queue() {
  dojo.io.bind({ 
	url: "queue/",
		handler: show_queue_callback,
		method:"GET",
		});
    return false;
}

/* returns a new node to be used as an icon to represent the mimetype */
function get_mimetype_icon(mimetype) {
	icon = document.createElement('img');

  if (mimetype.match("^audio/")) {
	icon.setAttribute('src', '/static/images/sound.png');
  } 
  else if (mimetype.match('^video/')) {
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
  item_link.appendChild(document.createTextNode(entry['podcast_name']));
  item_link.appendChild(document.createTextNode(' - '));
  item_link.appendChild(document.createTextNode(entry['title']));
  item_title.appendChild(item_link);
  new_item.appendChild(item_title);
  
  /* summary / body */
  var item_summary = document.createElement('div');
  item_summary.setAttribute('class', 'item_summary');
  item_summary.appendChild(document.createTextNode(entry['summary']));
  new_item.appendChild(item_summary);

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
  play_icon.setAttribute('alt', 'Play now');
  play_icon.setAttribute('title', 'Play now');
  enclosure_link.appendChild(play_icon);
  new_item.appendChild(enclosure_link);
  
  /* add action buttons to remove queue items */
  
  if (atFront) {
	first_child = queue_node.childNodes[0];
	queue_node.insertBefore(new_item, first_child);
  }
  else {
	queue_node.appendChild(new_item);
  }
}

/* called when we get the json response from the server with the queue contents */
function show_queue_callback(type, data, evt) {
  if (type == "load") {
	
	payload = dojo.json.evalJson(data);

	if (payload["error"] != "") {
	  show_error("queue", payload["error"]);
	}
	else {
	  /* find the node where we should show the queue */
	  var queue_node = dojo.byId("queue");
	  queue_node.innerHTML = "";
	  
	  /* process the queue contents */
	  queue_contents = payload['queue'];

	  if (queue_contents.length == 0) {
		queue_node.innerHTML = '<div class="queue_item">Your queue is empty.</div>';
	  }
	  else {
		for (var i=0; i < queue_contents.length; i++) {
		  item = queue_contents[i];
		  insert_entry_into_queue(item, 0);
		}
	  }
	}
	
  } else if (type == "error") {
	dojo.debugShallow(data);
	clear_feed_viewer();
  }
}


var podcast_entries = {};
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
	author_email = 'n/a';
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

	if (payload["error"] != "") {
	  show_error("queue", payload["error"]);
	}

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
	new_link.setAttribute("onclick", "return show_feed_by_id(" + feed_id + ")");
	new_link.setAttribute("href", "");
	new_link.appendChild(document.createTextNode(feed_info["name"]));
	show_icon = document.createElement('img');
	show_icon.setAttribute('src', '/static/images/arrow_down.png');
	show_icon.setAttribute('alt', 'Show feed below');
	show_icon.setAttribute('title', 'Show feed below');
	new_link.appendChild(show_icon);
	new_item.appendChild(new_link);

	home_icon = document.createElement('a');
	home_icon.setAttribute('href', feed_info['home_url']);
	home_icon.setAttribute('target', '_blank');
	home_icon.setAttribute('alt', 'Visit home page');
	home_icon.setAttribute('title', 'Visit home page');
	home_icon.innerHTML = '<img src="/static/images/house.png" />';
	new_item.appendChild(home_icon);

	feed_icon = document.createElement('a');
	feed_icon.setAttribute('href', feed_info['feed_url']);
	feed_icon.setAttribute('target', '_blank');
	feed_icon.setAttribute('alt', 'Visit podcast feed');
	feed_icon.setAttribute('title', 'Visit podcast feed');
	feed_icon.innerHTML = '<img src="/static/images/feed-icon-14x14.png" />';
	new_item.appendChild(feed_icon);

	var delete_link = document.createElement('a');
	delete_link.setAttribute('href', '');
	delete_link.setAttribute('onclick', 'return do_remove_feed(' + feed_id + ')');
	delete_link.setAttribute('class', 'delete_link');
	delete_icon = document.createElement('img');
	delete_icon.setAttribute('src', '/static/images/cancel.png');
	delete_icon.setAttribute('alt', 'Remove this feed');
	delete_icon.setAttribute('title', 'Remove this feed');
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
  show_status("Loading feed...");
  clear_feed_viewer();
  
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
	  populate_feed_viewer(payload['id'], payload["entries"]);
	  clear_error("add_feed_results");
	}
	
  } else if (type == "error") {
	clear_error("add_feed_results");
	show_error("add_feed_results", data);
  }
}

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
	  show_queue();
	}
	
  } else if (type == "error") {
	clear_error("add_feed_results");
	show_error("add_feed_results", data);
  }
}

/* Ask the server what feeds this user has. */
function show_user_feeds() {
  dojo.io.bind({ 
	url: "feed_list/",
		handler: show_user_feeds_callback,
		method: "GET",
		});
  return false;
}

/* called when we get the json response from the server with the list of feeds */
function show_user_feeds_callback(type, data, evt) {
  if (type == "load") {

	payload = dojo.json.evalJson(data);

	if (payload["error"] != "") {
	  show_error("add_feed_results", payload["error"]);
	}
	else {
	  feed_list = payload['list'];
	  for (i=0; i < feed_list.length; i++) {
		insert_feed_into_list(feed_list[i]);
	  }
	}
  }
  else if (type == "error") {
	show_error("add_feed_results", data);
  }
}

/*
** SHOW FEEDS form
*/
function show_feed_by_id(id) {
  show_status("Loading feed...");
  clear_feed_viewer();
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
	  populate_feed_viewer(payload['id'], payload["entries"]);
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
function populate_feed_viewer(podcast_id, entries) {
  var viewer_node = clear_feed_viewer();

  if (entries.length == 0) {
	viewer_node.innerHTML = '<div class="message">No entries</div>';
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

	  summary_node = document.createElement('div');
	  summary_node.setAttribute('class', 'podcast_entry_summary');
	  summary_node.appendChild(document.createTextNode(entry['summary']));
	  entry_node.appendChild(summary_node);

	  viewer_node.appendChild(entry_node);
	}
  }

  dojo.lfx.html.wipeIn(viewer_node, 200).play();
  return false;
}


/*
** ONLOAD
*/
function user_onload() {
  show_queue();
  show_user_feeds();
  clear_feed_viewer();

  if (document.add_feed.url.value) {
	/* we have a URL, so add it and start showing the contents */
	do_add_feed();
  }
}

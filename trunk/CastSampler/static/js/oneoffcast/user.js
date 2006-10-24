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
		});
    return false;
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
		  
		  var new_item = document.createElement("div");
		  new_item.setAttribute("class", "queue_item");
		  
		  /* title */
		  var item_title = document.createElement("div");
		  item_title.setAttribute("class", "item_title");
		  
		  var podcast_link = document.createElement('a');
		  podcast_link.setAttribute('href', item['podcast_home']);
		  podcast_link.appendChild(document.createTextNode(item['podcast_name']));
		  item_title.appendChild(podcast_link);
		  item_title.appendChild(document.createTextNode(' - '));
		  var item_link = document.createElement('a');
		  item_link.setAttribute('href', item['link']);
		  item_link.appendChild(document.createTextNode(item['title']));
		  item_title.appendChild(item_link);
		  new_item.appendChild(item_title);
		  
		  /* description / body */
		  var item_description = document.createElement('div');
		  item_description.setAttribute('class', 'item_description');
		  item_description.appendChild(document.createTextNode(item['description']));
		  new_item.appendChild(item_description);
		  
		  /* enclosure */
		  var enclosure_link = document.createElement('a');
		  enclosure_link.setAttribute('class', 'enclosure_link');
		  enclosure_link.setAttribute('href', item['enclosure_url']);
		  enclosure_link.appendChild(document.createTextNode(item['enclosure_mimetype']));
		  new_item.appendChild(enclosure_link);
		  
		  /* add action buttons to remove queue items */
		  
		  queue_node.appendChild(new_item);
		}
	  }
	}
	
  } else if (type == "error") {
	dojo.debugShallow(data);
	clear_feed_viewer();
  }
}

function do_add_to_queue(form_node_name) {
  show_status("Adding ...");
  
  dojo.io.bind({ 
	url: "add_to_queue/",
		handler: add_to_queue_callback,
		formNode: document.getElementById(form_node_name),
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
	var list_node = dojo.byId("my_podcasts");
	var new_item = document.createElement("li");
	new_item.setAttribute('id', feed_node_id);
	var new_link = document.createElement("a");
	new_link.setAttribute("onclick", "return show_feed_by_id(" + feed_info["id"] + ")");
	new_link.setAttribute("href", "");
	new_link.appendChild(document.createTextNode(feed_info["name"]));
	show_icon = document.createElement('img');
	show_icon.setAttribute('src', '/static/images/arrow_down.png');
	show_icon.setAttribute('alt', 'Show Feed Below');
	show_icon.setAttribute('title', 'Show Feed Below');
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
	url: "add_feed/",
		handler: add_feed_callback,
		formNode: document.getElementById("add_feed")
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

/* Ask the server what feeds this user has. */
function show_user_feeds() {
  dojo.io.bind({ 
	url: "feed_list/",
		handler: show_user_feeds_callback,
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
	for (i=0; i < entries.length; i++) {
	  var entry = entries[i];
	  var entry_node = document.createElement('div');
	  entry_node.setAttribute('class', 'podcast_entry');

	  /* an icon to add the item to the queue */
	  form = document.createElement('form');
	  var form_id = 'add_item_' + i;
	  form.setAttribute('id', form_id);
	  form.setAttribute('method', 'post');
	  form.innerHTML = '<input type="hidden" name="title" value="' + entry['title'] + '"/>' +
		'<input type="hidden" name="podcast" value="' + podcast_id + '"\>' +
		'<input type="hidden" name="description" value="' + entry['summary'] + '"/>' +
		'<div class="podcast_entry_title">' + 
		'<a href="" onclick="return do_add_to_queue(\'' + form_id + '\');" alt="Add to my queue" title="Add to my queue">' +
		'<img src="/static/images/add.png"/>' + entry['title'] + '</a>' +
		'<a href="' + entry['link'] + '" target="_blank" title="Open link">' + 
		'<img src="/static/images/link_go.png"/></a>' +
		'</a></div>' +
		'<div class="podcast_entry_summary">' + entry['summary'] + '</div>';

	  entry_node.appendChild(form);

	  /* a link to see the original item */
	  /*
	  title_link = document.createElement('a');
	  title_link.setAttribute('href', entry['link']);
	  title_link.setAttribute('target', '_blank');
	  title_link.appendChild(document.createTextNode(entry['title']));
	  title_node.appendChild(title_link);
	  entry_node.appendChild(title_node);

	  summary_node = document.createElement('div');
	  summary_node.setAttribute('class', 'podcast_entry_summary');
	  summary_node.appendChild(document.createTextNode(entry['summary']));
	  entry_node.appendChild(summary_node);
	  */

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
}

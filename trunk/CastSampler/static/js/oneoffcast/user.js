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

/* Insert a feed element into the list of feeds of the user. */
function insert_feed_into_list(feed_info) {
  var list_node = dojo.byId("my_podcasts");
  var new_item = document.createElement("li");
  var new_link = document.createElement("a");
  new_link.setAttribute("onclick", "return show_feed_by_id(" + feed_info["id"] + ")");
  new_link.setAttribute("href", "");
  new_link.appendChild(document.createTextNode(feed_info["name"]));
  new_item.appendChild(new_link);
  list_node.appendChild(new_item);
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
  clear_feed_viewer();
  clear_error("add_feed_results");
  
  dojo.debug(data);
  
  if (type == "load") {
	
	payload = dojo.json.evalJson(data);
	
	if (payload["error"] != "") {
	  show_error("add_feed_results", payload["error"]);
	}
	else {
	  insert_feed_into_list(payload);
	}
	
  } else if (type == "error") {
	clear_feed_viewer();
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

	/*dojo.debug(payload);*/

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
}

/*
** SHOW FEEDS form
*/
function do_show_feeds() {
  return false;
}

function show_feed_by_id(id) {
  dojo.debug("show feed " + id);
  return false;
}

function clear_feed_viewer() {
  var node = dojo.byId("feed_viewer");
  dojo.lfx.html.wipeOut(node, 1).play();
  node.innerHTML = "";
  return false;
}

/*
** ONLOAD
*/
function user_onload() {
  show_queue();
  show_user_feeds();
}

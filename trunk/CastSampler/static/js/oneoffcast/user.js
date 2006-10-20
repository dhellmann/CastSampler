/*
** JavaScript for the user page.
**
** $Id$
*/

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
	  /* TODO: need to add the feed to the list */
	  /* TODO: need to show the feed contents here */
	}
	
  } else if (type == "error") {
	dojo.debugShallow(data);
	clear_feed_viewer();
  }
}

/*
** SHOW FEEDS form
*/
function do_show_feeds() {
  return false;
}

function show_feed_by_id(id) {
  alert("Show " + id);
  return false;
}

function clear_feed_viewer() {
  var node = dojo.byId("feed_viewer");
  dojo.lfx.html.wipeOut(node, 1).play();
  node.innerHTML = "";
  return false;
}

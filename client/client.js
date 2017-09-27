// gsearch client with keyword ranker
// 2017-09-27

var argv = process.argv;
var keyword = argv.slice(2).join(' ');
var ranker = '';

if (argv.length > 3) {
  if (argv[2] == "rank") {
    ranker = argv[3];
    keyword = argv.slice(3).join(' ');
  }
}

var redis = require("redis")
  , subscriber = redis.createClient()
  , publisher  = redis.createClient();

var rank = 0;

subscriber.on("message", function(channel, message) {
  console.log("Message '" + message + "' on channel '" + channel + "' arrived!")

  if (ranker != '' && rank > 0) {
    console.log("=> Keyword Ranker: Rank " + rank + " test.");

    if (message.indexOf(ranker) < 0) {
      console.log("=> Keyword Ranker: Rank " + rank + " is not. message: " + message);
    } else {
      console.log("=> Keyword Ranker: Rank " + rank + " matched! message: " + message);
    }
  }

  // third, quit sub/pub when finish(FIN)
  if (message == "FIN") {
    console.log("Detected command: " + message);
    subscriber.unsubscribe();
    subscriber.quit();
    publisher.quit();
  }

  rank++; // set rank up
});

// first, request result by keyword
console.log("Keyword is: " + keyword);
publisher.publish("gsearch", keyword);

// second, get results
subscriber.subscribe("gsearch");

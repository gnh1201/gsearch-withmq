// gsearch client with keyword ranker
// 2017-09-27

var argv = process.argv;
var keyword = argv.slice(2).join(' ');
var ranker = '';

if (argv.length > 3) {
  if (argv[2] == "rank") {
    ranker = argv[3];
    keyword = argv.slice(4).join(' ');
  }
}

var redis = require("redis")
  , subscriber = redis.createClient()
  , publisher  = redis.createClient();

var fs = require('fs');

var rank = 0;
var rankMatched = [];

var getDateYmd = function() {
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth() + 1;
  var yyyy = today.getFullYear();

  return [('0000'+yyyy).slice(-4), ('00'+mm).slice(-2), ('00'+dd).slice(-2)].join('');
}

subscriber.on("message", function(channel, message) {
  console.log("Message '" + message + "' on channel '" + channel + "' arrived!")

  var foundUrl = '';
  var operator = '';
  var commands = [];

  commands = message.split(' ');
  if (commands.length > 1) {
    operator = commands[0];
  } else {
    operator = message;
  }

  if (operator == 'FOUND') {
    foundUrl = commands.slice(1).join('');
  }

  if (ranker != '' && rank > 0) {
    console.log("=> Keyword Ranker: Rank " + rank + " test.");

    if (foundUrl.indexOf(ranker) < 0) {
      console.log("=> Keyword Ranker: Rank " + rank + " is not. url: " + foundUrl);
    } else {
      rankMatched.push(rank);
      console.log("=> Keyword Ranker: Rank " + rank + " matched! message: " + foundUrl);
    }
  }

  // third, quit sub/pub when finish(FIN)
  if (message == 'FIN') {
    console.log("Detected command: " + message);
    subscriber.unsubscribe();
    subscriber.quit();
    publisher.quit();

    // write result to file
    appendDate = getDateYmd();
    appendData = {
       "keyword": keyword,
       "ranker": ranker,
       "matched": rankMatched.join(','),
       "date": appendDate
    };
    appendDataLine = "\n" + JSON.stringify(appendData);
    appendFilename = "./data/" + appendDate + ".txt";

    fs.appendFile(appendFilename, appendDataLine, function(err) {
      if(err) {
        return console.log(appendFilename + ": " + err);
      }

      console.log(appendFilename + ": " + "The file was saved!");
    });
  }

  rank++; // set rank up
});

// first, request result by keyword
console.log("Keyword is: " + keyword);

publisher.publish("gsearch", "SEARCH " + keyword);

// second, get results
subscriber.subscribe("gsearch");

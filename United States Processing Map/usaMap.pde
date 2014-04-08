PShape USA;
PShape State;

String [] Neutral = {};
String [] Positive  = {};
String [] Negative = {};

void setup() {
  // We create our image space
  size(950, 600);
  // We load a map of the USA (as seen on the Wikipedia Processing example)
  USA = loadShape("http://upload.wikimedia.org/wikipedia/commons/3/32/Blank_US_Map.svg");
  // We smooth the image so it looks better
  smooth(); 
}
 
void draw() {
  String [] Neutral = {};
  String [] Positive  = {};
  String [] Negative = {};
  // We open our file of tweets
  String tweets[] = loadStrings("ourTweets.txt"); 
  for (int i=0; i < tweets.length; i++) {
    String[] line = split(tweets[i], " ");
    String ourState = line[0];
    String ourSentiment = line[1];
    if (ourSentiment.equals("Negative")){
        Negative = append(Negative, ourState);
    }
    else if (ourSentiment.equals("Positive")){
       Positive = append(Positive, ourState); 
    }
    else{
      Neutral = append(Neutral, ourState);
    }
  }
  // We make the background white
  background(255);
  // We create a shape using the United States
  // TO DO: for some reason, some states are messed up, this needs to be fixed
  shape(USA, 0, 0);
  // We color our states based on neutral, positive, or negative sentiments
  statesColoring(Neutral , color(0, 255, 0));
  statesColoring(Positive , color(0, 0, 255));
  statesColoring(Negative, color(255, 0, 0));
}
 
void statesColoring(String[] TweetLocation, int c){
  // For every location, we create a state and update our color
  // This loop is the same as the Wikipedia Processing example
  for (int i = 0; i < TweetLocation.length; i++) {
    PShape State = USA.getChild(TweetLocation[i]);
    // Disable the colors found in the SVG file
    State.disableStyle();
    // Set our own coloring
    fill(c);
    noStroke();
    // Draw a single state
    shape(State, 0, 0);
  }
}

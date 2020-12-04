PFont font;
float bspeed=2.5, playerSpeed=3;
float playerx, playery, goalx, goaly;
int numBoxes, scoreV,scoreH, lives=5;
float[] xs, ys;
int[] lastChangedDir;
int[] changeDirInterval;
String[] currDir;
boolean Up, Down, Left, Right, start, lose;
 
void setup() {
  font = loadFont("IMPACT.vlw"); //loading impact font
  textFont(font);  
  
  size(1000, 800);
  numBoxes = 100;   //number of boxes
  
  xs = new float[numBoxes]; //declaring arrays
  ys = new float[numBoxes];
  lastChangedDir = new int[numBoxes];
  changeDirInterval = new int[numBoxes];
  currDir = new String[numBoxes];
  
  goalx = random(100,980); 
  goaly = random(0,780);
  
  for (int i=0;i<numBoxes;i++) {  //initial randomising location of boxes
    xs[i] = random(100, 1000);
    ys[i] = random(0, 780);
    lastChangedDir[i] = millis();
    changeDirInterval[i] = (int)random(1000,2000);
    
    int temp = (int)round(random(0, 3)); //initial random direction of boxes
    if (temp == 0) currDir[i] = "left";
    else if (temp == 1) currDir[i] = "right";
    else if (temp == 2) currDir[i] = "up";
    else if (temp == 3) currDir[i] = "down";
  }

}

 
 
void draw() {
  if (start==false&&lose==false){        //Starting screen
    background(0);
    textSize(80);
    stroke(0);
    textAlign(CENTER);
    text("PRESS MOUSE TO START",500,300);
    textSize(60);
    text("USE ARROWS KEYS TO MOVE",500,400);
    textSize(40);
    text("By Nikhil Mistry",500,500);
  }
    
  if(start){
  background(0);
  fill(255, 17, 0);       //Red player box
  rect(playerx,playery,20,20); 
  
  fill(#1C0DFF);               //Blue goal box
  rect(goalx,goaly,20,20);
  
  fill(255);
  font = loadFont("IMPACT.vlw");      //Score and Lives
  textFont(font);
  textAlign(CENTER);
  text("Score " + scoreV + " | " + "Lives "+lives ,500,27);
  textSize(40);
  
  fill(255);     //boundary
  rect(99,0,4,800);
   
  Boxes(); 
  Player();
  
  if (scoreH==0)  {numBoxes=5;}        //increasing difficulty as you play
  if (scoreH==3)  {numBoxes=10;}       //increase amount of boxes up to 35, then increase speed of player and boxes
  if (scoreH==6)  {numBoxes=15;}
  if (scoreH==9)  {numBoxes=20;}
  if (scoreH==12) {numBoxes=30;}
  if (scoreH==15) {numBoxes=35;}
  if (scoreH==18) {bspeed=bspeed+1; playerSpeed=playerSpeed+1; scoreH=0; numBoxes=0;}
  
  if (lives==0){    //If game is lost
    start = false;
    lose = true;
    scoreH=0;
    scoreV=0;
    lives=5;
  }
  if (lose){
    textAlign(CENTER);
    textSize(80);
    text("YOU LOSE TRY AGAIN",500,300);
    text("PRESS MOUSE TO RESTART",500,400);
    
     
  }
 
  

  }
 }

void keyPressed(){            // Player controls
  if (key==CODED){
  if (keyCode == UP) {Up = true; Down = false; Right = false; Left = false;}
  if (keyCode == DOWN) {Down = true; Up = false; Right = false; Left = false;}
  if (keyCode == LEFT) {Left = true; Right = false; Up = false; Down = false;}
  if (keyCode == RIGHT) {Right = true; Left = false; Up = false; Down = false;}
  }
}

void Player(){
  if (Up){playery = playery-playerSpeed;}      //Constant movement of player
  if (Down) {playery = playery+playerSpeed;}
  if (Left) {playerx = playerx-playerSpeed;}
  if (Right) {playerx = playerx+playerSpeed;}
  
  //Collision with blue box
  if(playerx>= goalx && playerx<=goalx+20 && playery>=goaly && playery<=goaly+20 || playerx+20>= goalx && playerx+20<=goalx+20 && playery+20>=goaly && playery+20<=goaly+20){
     playerx = 0;
     playery = 0;
     scoreV= scoreV+1;
     scoreH = scoreH+1;
     Up = false; Down = false; Right = false; Left = false;
     goalx = random(100,980);   //randomise blue box again
     goaly = random(0,780);   
  }
  if(playerx<=-1)  {Left=false; Right=true;}     //player rebounds off wall
  if(playerx>=981) {Right=false; Left=true;}
  if(playery<=-1)  {Up=false; Down=true;}
  if(playery>=780) {Down=false; Up=true;}

}

void Boxes(){    
  for (int i=0;i<numBoxes;i++) {   //Creating the boxes
    fill(255);           
    rect(xs[i], ys[i], 20, 20);   
                                  //resetting player if collision with boxes
   if (playerx>= xs[i] && playerx<=xs[i]+20 && playery>=ys[i] && playery<=ys[i]+20 || playerx+20>= xs[i] && playerx+20<=xs[i]+20 && playery+20>=ys[i] && playery+20<=ys[i]+20){
     playerx = 0;
     playery = 0;
     Up = false; Down = false; Right = false; Left = false;
     lives = lives-1;

   }
      
    if (currDir[i].equals("left"))       {xs[i] -= bspeed;}       //Movement of boxes
    else if (currDir[i].equals("right")) {xs[i] += bspeed;}
    else if (currDir[i].equals("up"))    {ys[i] -= bspeed;}
    else if (currDir[i].equals("down"))  {ys[i] += bspeed;}
    
    if (millis() - lastChangedDir[i] >= changeDirInterval[i]) {  //changing direction of boxes
      lastChangedDir[i] = millis();
      int temp = (int)round(random(0, 3));
      if (temp == 0) currDir[i] = "left";
      else if (temp == 1) currDir[i] = "right";
      else if (temp == 2) currDir[i] = "up";
      else if (temp == 3) currDir[i] = "down";      
    }
    
   if(xs[i] <= 100) {currDir[i]="right";}  //Boxes rebound off wall
   if(xs[i] >= 980) {currDir[i]="left";}
   if(ys[i] <= 100) {currDir[i]="down";}
   if(ys[i] >= 780) {currDir[i]="up";}
     
  }
}

void mousePressed() {start = true; lose=false;}

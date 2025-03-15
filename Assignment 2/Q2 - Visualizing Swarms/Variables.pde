// Slider Variables
int numBees = 30;
int numFood = 50;
int spawnIntervalBees = 20; // Frames between spawns
int spawnIntervalFood = 20; // Frames between spawns
float beeMaxSpeed = 2.0;

// Game Timer Variables
int gameDuration = 100; // 100 seconds (2 minutes)
int startTime;
boolean gameOver = false;
boolean gameWon = false;

// Array Variables
color[] col_leaves = new int[]{#79C832, #00FF10, #5BE928, #26e331};
ArrayList<Bee> bees;
ArrayList<Food> foodSources;
ArrayList<PVector> hiveLocations;
ArrayList<WindParticle> windParticles;
Cloud[] clouds;

// Other Variables
ControlP5 cp5;
float theta;
int spawnCounterFood = 0;
int spawnCounterBees = 0;
PVector prevMousePos;
boolean canDrag = true;
int dragStartTime = 0;
int numClouds = 8;

// Confetti Project
color[] rainbowColors = new int[]{#9A56FF, #527AF2, #F2B807, #F28907, #F2220F};
Confetti[] confetti = new Confetti[100];
boolean partyTime = false;

import java.util.*;
import controlP5.*;

void setup() {

  size(1500, 800);

  startTime = millis(); // Start the timer
  prevMousePos = new PVector(mouseX, mouseY);
  
  bees = new ArrayList<Bee>();
  foodSources = new ArrayList<Food>();
  hiveLocations = new ArrayList<PVector>();
  windParticles = new ArrayList<WindParticle>();
  
  // so that we don't lose at the start
  foodSources.add(new Food(913, 387));

  hiveLocations.add(new PVector(295, 460));
  hiveLocations.add(new PVector(630, 470));
  hiveLocations.add(new PVector(850, 410));
  hiveLocations.add(new PVector(1260, 460));
    
  clouds = new Cloud[numClouds];
  for (int i = 0; i < numClouds; i++) 
    clouds[i] = new Cloud(random(width), random(50, height / 2));
   
  // Add sliders with increased size and larger text
  cp5 = new ControlP5(this);
  
  cp5.addSlider("spawnIntervalBees")
    .setPosition(20, 30)
    .setSize(250, 25)
    .setRange(1, 100)
    .setValue(spawnIntervalBees)
    .setLabel("Bees Spawn Interval")
    .getCaptionLabel().setFont(createFont("Times New Roman", 20)).setColor(color(0, 0, 0));

  cp5.addSlider("numBees")
    .setPosition(20, 60)
    .setSize(250, 25)
    .setRange(10, 200)
    .setValue(numBees)
    .setLabel("Maximum Bees")
    .getCaptionLabel().setFont(createFont("Times New Roman", 20)).setColor(color(0, 0, 0));

  cp5.addSlider("spawnIntervalFood")
    .setPosition(20, 120)
    .setSize(250, 25)
    .setRange(1, 100)
    .setValue(spawnIntervalFood)
    .setLabel("Food Spawn Interval")
    .getCaptionLabel().setFont(createFont("Times New Roman", 20)).setColor(color(0, 0, 0));
  ;

  cp5.addSlider("numFood")
    .setPosition(20, 150)
    .setSize(250, 25)
    .setRange(10, 100)
    .setValue(numFood)
    .setLabel("Max Food")
    .getCaptionLabel().setFont(createFont("Times New Roman", 20)).setColor(color(0, 0, 0));
  ;

  cp5.addSlider("beeMaxSpeed")
    .setPosition(20, 90)
    .setSize(250, 25)
    .setRange(0.5, 10.0)
    .setValue(beeMaxSpeed)
    .setLabel("Bee Max Speed")
    .getCaptionLabel().setFont(createFont("Times New Roman", 20)).setColor(color(0, 0, 0));
  
  // Confetti :)
  for (int i = 0; i < confetti.length; i++) {
    confetti[i] = new Confetti();
  }
}

void draw() {

  //println("Mouse X: " + mouseX + ", Mouse Y: " + mouseY);
  background(125, 163, 239);
  frameRate(60);

  int elapsedTime = (millis() - startTime) / 1000;
  int remainingTime = gameDuration - elapsedTime;
 
  float sizeOfTree = height / 8;
  int numberOfTrees = 4;
  int numberOfHives = 4;
  float thetas[] = {35, 75, 45, 60};
  int ground_size = height / 6;
  
  //Clouds
  for (Cloud c : clouds) {
    c.update();
    c.display();
  }
  
  //fill(247,201,11);
  //#AD4836 : URDU DASKTARI
//#EB5D49: PINK CHUNKY
//#FAAE36: YELOWISH ON CHUNKY
  fill(#ff8300); // #f79621
  fill(#f79621);
  //fill(#8ad0ce);
  textSize(20);
  text(frameRate, 20, 20);

  // Display Game Title
  textSize(40);
  PFont font = createFont("Arial Bold", 50);
  textFont(font);
  text("Swarm Survival", 620, 90);

  // Display Timer and Food Count
  textSize(25);    
  fill(0);
  text("Time Left: " + remainingTime + "s", width - 220, 50);
  text("Current Food: " + foodSources.size(), width - 220, 90);

  // Check Game Conditions
  if (!gameOver) {
    if (remainingTime <= 0) {
      gameWon = true;
      gameOver = true;
      partyTime = true;
    } else if (foodSources.size() <= 0) {
      gameOver = true;
    }
  }

  if (gameOver) {
    if (gameWon) {
      text("YOU WIN!", 750, 260);
    } else {
      text("YOU LOSE!", 750, 260);
      return;
    }
  }
  
  // When Won the Game !!!
  if (partyTime) {
    for (Confetti c : confetti) {
      c.show();
      c.update();
    }
  }

  // Ensure sliders update values in real-time
  spawnIntervalBees = (int) cp5.getController("spawnIntervalBees").getValue();
  numBees = (int) cp5.getController("numBees").getValue();
  spawnIntervalFood = (int) cp5.getController("spawnIntervalFood").getValue();
  numFood = (int) cp5.getController("numFood").getValue();
  beeMaxSpeed = cp5.getController("beeMaxSpeed").getValue();
  
  // Ground
  strokeWeight(1);
  fill(149, 72, 11);
  stroke(0);
  rectMode(CORNER);
  rect(0, height - ground_size, width, ground_size);

  // Trees
  pushMatrix();
  translate(0, -ground_size);

  for (int i = 0; i < numberOfTrees; i++)
  {
    theta = radians(thetas[i]);
    float sizeOfStem = - (sizeOfTree + 50);

    pushMatrix();

    translate(i*350 + width/7, height);
    strokeWeight(10);
    stroke(103, 48, 11);
    line(0, 0, 0, sizeOfStem);

    translate(0, sizeOfStem);
    strokeWeight(3);
    stroke(col_leaves[i]);
    branch(sizeOfTree);

    popMatrix();
  }

  popMatrix();

  // Bee Hives
  fill(249, 185, 49);
  stroke(0);
  strokeWeight(2);

  for (int i = 0; i < numberOfHives; i++)
  {
    PVector current = hiveLocations.get(i);
    for (int j = 0; j < 3; j++)
      rect(current.x, current.y + j*10, 30, 10);
  }

  // Wind Particles
  for (int i = windParticles.size() - 1; i >= 0; i--) {
    WindParticle p = windParticles.get(i);
    p.update();
    p.display();
    if (p.isDead()) {
      windParticles.remove(i);
    }
  }

  // Spawn Bees
  if (bees.size() < numBees && spawnCounterBees % spawnIntervalBees == 0) {
    int bee_hive_number = int(random(0, 4));
    PVector current = hiveLocations.get(bee_hive_number);
    bees.add(new Bee(current.x + random(-10, 10), current.y + random(-10, 10)));
  }
  spawnCounterBees++;

  // Food
  if (spawnCounterFood % spawnIntervalFood == 0)
    generateFoodNearTrees();
  spawnCounterFood++;

  for (int i = foodSources.size() - 1; i >= 0; i--) {
    Food f = foodSources.get(i);
    f.display();
    if (f.isEaten())
      foodSources.remove(i);
  }

  // Update Bees
  for (Bee b : bees) {
    if (!foodSources.isEmpty()) {
      b.updatePSO(foodSources);
    } else {
      b.randomMovement();
    }
    b.applyWindEffect(windParticles);
    b.flock(bees);
    b.update();
    b.edges();
    b.display();
  }

  // Check if dragging time exceeded 3 seconds
  if (millis() - dragStartTime > 3000 && dragStartTime != 0)
    canDrag = false;

  // Update previous mouse position for next frame
  prevMousePos.set(mouseX, mouseY);
}

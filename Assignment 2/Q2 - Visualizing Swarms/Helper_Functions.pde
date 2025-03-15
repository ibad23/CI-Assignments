void generateFoodNearTrees() {

  int attempts = 0;

  while (foodSources.size() < numFood && attempts < 1000) { // Limit attempts to avoid infinite loops
    int x_cood = int(random(width));
    int y_cood = int(random(height));

    color c = get(x_cood, y_cood);

    // Check if the pixel is green (tree area)
    if (c == col_leaves[0] || c == col_leaves[1] || c == col_leaves[2] || c == col_leaves[3]) {

      boolean tooClose = false;

      for (Food food : foodSources) {
        if (dist(x_cood, y_cood, food.position.x, food.position.y) < 20) { // Adjust spacing
          tooClose = true;
          break;
        }
      }

      if (!tooClose) {
        foodSources.add(new Food(x_cood, y_cood));
        return;
      }
    }
    attempts++;
  }
}

void branch(float h) {
  // Each branch will be 2/3rds the size of the previous one
  h *= 0.66;

  // All recursive functions must have an exit condition!!!!
  // Here, ours is when the length of the branch is 2 pixels or less
  if (h > 2) {
    pushMatrix();    // Save the current state of transformation (i.e. where are we now)
    rotate(theta);   // Rotate by theta
    line(0, 0, 0, -h);  // Draw the branch
    translate(0, -h); // Move to the end of the branch
    branch(h);       // Ok, now call myself to draw two new branches!!
    popMatrix();     // Whenever we get back here, we "pop" in order to restore the previous matrix state

    // Repeat the same thing, only branch off to the "left" this time!
    pushMatrix();
    rotate(-theta);
    line(0, 0, 0, -h);
    translate(0, -h);
    branch(h);
    popMatrix();
  }
}

void controlEvent(ControlEvent event) {
  if (event.isFrom("spawnIntervalBees")) {
    spawnIntervalBees = (int) event.getValue();
  } else if (event.isFrom("numBees")) {
    numBees = (int) event.getValue();
  } else if (event.isFrom("spawnIntervalFood")) {
    spawnIntervalFood = (int) event.getValue();
  } else if (event.isFrom("numFood")) {
    numFood = (int) event.getValue();
  } else if (event.isFrom("beeMaxSpeed")) {
    beeMaxSpeed = event.getValue();
  }
}

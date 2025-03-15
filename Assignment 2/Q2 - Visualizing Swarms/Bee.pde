class Bee {
  PVector position, velocity, acceleration;
  //float maxSpeed = 1.5;
  float safeDistance = 25; // Safe space between bees

  Bee(float x, float y) {
    position = new PVector(x, y);
    velocity = PVector.random2D();
    acceleration = new PVector();
  }
  
  // Particle Swarm Optimization being used here
  void updatePSO(ArrayList<Food> foodSources) {
    Food targetFood = null;
    float minDist = Float.MAX_VALUE;

    for (Food f : foodSources) {
      float d = PVector.dist(position, f.position);
      if (d < minDist) {
        minDist = d;
        targetFood = f;
      }
    }

    if (targetFood != null) {
      ArrayList<Bee> closestBees = getClosestBees(targetFood);
      for (Bee b : closestBees) {
        if (b == this) {
          PVector force = PVector.sub(targetFood.position, position);
          force.setMag(0.05); // Slow attraction
          applyForce(force);
        }
      }

      // **Check if bee is close enough to "eat"**
      if (PVector.dist(position, targetFood.position) < 5) {
        targetFood.eatenBy++; // Increment eat counter
      }
    }
  }

  ArrayList<Bee> getClosestBees(Food food) {
    ArrayList<Bee> sortedBees = new ArrayList<>(bees);
    sortedBees.sort((b1, b2) -> Float.compare(PVector.dist(b1.position, food.position), PVector.dist(b2.position, food.position)));
    return new ArrayList<>(sortedBees.subList(0, Math.min(20, sortedBees.size())));
  }

  void flock(ArrayList<Bee> allBees) {
    PVector sep = separate(allBees);
    applyForce(sep);
  }

  PVector separate(ArrayList<Bee> allBees) {
    PVector steer = new PVector();
    int count = 0;
    for (Bee other : allBees) {
      float d = PVector.dist(position, other.position);
      if (d > 0 && d < safeDistance) {
        PVector diff = PVector.sub(position, other.position);
        diff.normalize();
        diff.div(d);
        steer.add(diff);
        count++;
      }
    }
    if (count > 0) {
      steer.div(count);
      //steer.setMag(maxSpeed);
      steer.setMag(beeMaxSpeed);
      steer.sub(velocity);
      steer.limit(0.05);
    }
    return steer;
  }

  void randomMovement() {
    PVector randMove = PVector.random2D();
    randMove.setMag(0.05);
    applyForce(randMove);
  }

  void applyForce(PVector force) {
    acceleration.add(force);
  }

  void update() {
    velocity.add(acceleration);
    velocity.limit(beeMaxSpeed);
    //veloctiy.limit(maxSpeed);
    position.add(velocity);
    acceleration.mult(0);
  }

  void edges() {
    if (position.x > width) position.x = 0;
    if (position.x < 0) position.x = width;

    if (position.y < 130) {
      position.y = 130;
      velocity.y *= -1; // Bounce back
    }
    if (position.y > 670) {
      position.y = 670;
      velocity.y *= -1; // Bounce back
    }
  }

  void applyWindEffect(ArrayList<WindParticle> windParticles) {
    for (WindParticle wind : windParticles) {
      float d = PVector.dist(position, wind.position);
      if (d < 100) { // Apply wind force if within range
        PVector windEffect = wind.velocity.copy().mult(0.05 / (d + 1)); // Scale effect by distance
        velocity.add(windEffect);
        //velocity.limit(maxSpeed * 2); // Prevent excessive acceleration
        velocity.limit(beeMaxSpeed * 2); // Prevent excessive acceleration
      }
    }
  }

  void display() {
    fill(255, 200, 0);
    stroke(0);
    strokeWeight(1);
    ellipse(position.x, position.y, 9, 9);
  }
}

class WindParticle {
  
  PVector position, velocity;
  float alpha = 200;
  float lifespan = 100;
  float length;
  float angle; // Rotation angle

  WindParticle(float x, float y, PVector mouseVel) {
    position = new PVector(x, y);
    velocity = mouseVel.copy().mult(random(0.5, 1.2)); // Scale velocity randomly for variation
    length = random(10, 25);
    angle = atan2(velocity.y, velocity.x); // Compute angle based on direction
  }

  void update() {
    position.add(velocity);
    alpha -= 20;
    lifespan -= 1;
  }

  boolean isDead() {
    return lifespan <= 0;
  }

  void display() {
    stroke(255, 255, 255, alpha);
    strokeWeight(5);

    // Calculate end point using rotation
    float x2 = position.x + length * cos(angle);
    float y2 = position.y + length * sin(angle);

    line(position.x, position.y, x2, y2);
  }
}

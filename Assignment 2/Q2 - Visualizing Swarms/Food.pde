class Food {
  PVector position;
  int eatenBy = 0;
  int maxEaters = 10; // Disappear after 1 bees eat (for now) ; technically this is a variable as well.
  float size = 10 + random(-2, 10);
  color col = color(255 + random(-50, 0), 50 + random(-20, 20), 50 + random(-20, 20));

  Food(float x, float y) {
    position = new PVector(x, y);
  }

  boolean isEaten() {
    return eatenBy >= maxEaters;
  }

  void display() {
    fill(col);
    noStroke();
    ellipse(position.x, position.y, size, size);
  }
}

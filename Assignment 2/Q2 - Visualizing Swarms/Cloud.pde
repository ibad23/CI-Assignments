class Cloud {
  float x, y;
  float speed;
  float size;
  float noiseOffset;

  Cloud(float startX, float startY) {
    x = startX;
    y = startY;
    speed = random(0.5, 1.2);
    size = random(50, 120); // Larger clouds
    noiseOffset = random(1000);
  }

  void update() {
    x += speed;
    
    // Wrap around when out of bounds
    if (x > width + size) {
      x = -size;
    }
  }

  void display() {
    noStroke();
    fill(255, 220);
    
    // More ellipses for fluffiness
    for (int i = 0; i < 8; i++) {
      float xOffset = noise(noiseOffset + i * 0.2) * size * 1.2;
      float yOffset = noise(noiseOffset + i * 0.3) * size * 0.6;
      float radius = size * (0.6 + noise(noiseOffset + i * 0.1) * 0.8);
      fill(255, 180 + noise(noiseOffset + i * 0.2) * 60); // Vary opacity
      ellipse(x + xOffset, y + yOffset, radius, radius * 0.8);
    }
  }
}

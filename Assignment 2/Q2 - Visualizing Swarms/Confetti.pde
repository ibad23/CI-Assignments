class Confetti {
  float x, y, w, h;
  float xspeed, yspeed;
  float rotationSpeed, angle; //rotation variables
  color col; //color
  
  Confetti() {
    x = -1000;
    y = -1000;
    w = 8; //confetti width
    h = random(4, 12); //confetti height
    xspeed = 0;
    yspeed = 0;
    angle = 0; 
    rotationSpeed = 3; //try adjusting this!
    col = rainbowColors[int(random(rainbowColors.length))]; 
  }

  void burst(float mx, float my) {
    x = mx;
    y = my;
    xspeed = random(-5, 5);
    yspeed = random(-5, 5);
  }

  void update() {
    x = x + xspeed;
    y = y + yspeed;
    angle = angle + radians(rotationSpeed); //update the angle

    yspeed = yspeed + 0.1;
  }

  void show() {
    push();
    fill(col);
    noStroke();
    rectMode(CENTER);
    translate(x, y);
    rotate(angle);
    rect(0, 0, w, h);
    pop();
  }
}

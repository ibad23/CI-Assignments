void mousePressed() {
  //  foodSources.add(new Food(mouseX, mouseY));
  if (partyTime) {
    for (Confetti c : confetti) {
      c.burst(mouseX, mouseY);
    }
  }
}

void mouseDragged() {
  if (!partyTime) {
    if (canDrag) {
      if (dragStartTime == 0) {
        dragStartTime = millis();
      }
      PVector mouseVel = new PVector(mouseX - prevMousePos.x, mouseY - prevMousePos.y);
      for (int i = 0; i < 5; i++) {
        windParticles.add(new WindParticle(mouseX, mouseY, mouseVel));
      }
    }
  }
}

void mouseReleased() {
  canDrag = true;
  dragStartTime = 0;
}

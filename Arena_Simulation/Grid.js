class Grid {
  constructor(w, h) {
    this.w = w;
    this.h = h;
  }
  
  draw() {
    for (let x=this.w; x<=displayWidth; x+=this.w){
      stroke("#fff");
      if(x%5 == 0){
        stroke("#ccc");
      }
      line(x, 0, x, displayHeight);
    }
    
    for (let y=this.h; y<=displayHeight; y+=this.h){
      stroke("#fff");
      if(y%5 == 0){
        stroke("#ccc");
      }
      line(0, y, displayWidth, y);
    }
  }
}
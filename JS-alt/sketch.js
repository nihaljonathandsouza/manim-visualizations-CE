// --- CONFIGURATION ---
const cols = 4;
const rows = 6;
const pWidth = 80;
const pHeight = 70;
const chocolateColor = '#7B3F00';

let lowerHalf = [], mainUpper = [], leftColumn = [], extraPiece = [];
let startX, startY;

// --- STATE MACHINE (TIMELINE) ---
let currentStep = 0;

// Target & Current coordinates for smooth animations
let tMainX = 0, tMainY = 0, cMainX = 0, cMainY = 0;
let tLeftX = 0, tLeftY = 0, cLeftX = 0, cLeftY = 0;
let tExtraX = 0, tExtraY = 0, cExtraX = 0, cExtraY = 0;

function setup() {
  createCanvas(800, 600);
  
  startX = (width - (cols * pWidth)) / 2;
  startY = (height - (rows * pHeight)) / 2 + 30; 

  let cutStartY = startY + 4 * pHeight; 
  let cutEndY = startY + 3 * pHeight;   

  // --- BUILD THE PIECES ---
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      let x = startX + (c * pWidth);
      let y = startY + (r * pHeight);
      
      if (r < 3) {
        let block = createRect(x, y, pWidth, pHeight);
        if (c === 0) {
            if (r === 0) extraPiece.push(block); 
            else leftColumn.push(block);         
        } else mainUpper.push(block);               
      } 
      else if (r > 3) lowerHalf.push(createRect(x, y, pWidth, pHeight)); 
      else if (r === 3) {
        let yLeft = map(c, 0, cols, cutStartY, cutEndY);
        let yRight = map(c + 1, 0, cols, cutStartY, cutEndY);

        let upPoly = [
          {x: x, y: y}, {x: x + pWidth, y: y},
          {x: x + pWidth, y: yRight}, {x: x, y: yLeft}
        ];
        let downPoly = [
          {x: x, y: yLeft}, {x: x + pWidth, y: yRight},
          {x: x + pWidth, y: y + pHeight}, {x: x, y: y + pHeight}
        ];

        lowerHalf.push(downPoly);
        if (c === 0) leftColumn.push(upPoly);
        else mainUpper.push(upPoly);
      }
    }
  }
}

function createRect(x, y, w, h) {
  return [ {x: x, y: y}, {x: x + w, y: y}, {x: x + w, y: y + h}, {x: x, y: y + h} ];
}

// --- MOUSE CLICK ADVANCES THE TIMELINE ---
function mousePressed() {
  currentStep++;
  if (currentStep > 5) currentStep = 0; 

  if (currentStep === 0) {
    tMainX = 0; tMainY = 0;
    tLeftX = 0; tLeftY = 0;
    tExtraX = 0; tExtraY = 0;
  } 
  else if (currentStep === 1) { /* White dotted lines appear */ } 
  else if (currentStep === 2) {
    tExtraX = -100; tExtraY = -100;
  } 
  else if (currentStep === 3) {
    tMainX = -pWidth; 
    tMainY = pHeight / 4;
  } 
  else if (currentStep === 4) {
    tLeftX = pWidth * 3; 
    tLeftY = -(pHeight * 3) / 4;
  }
}

function draw() {
  background(40);
  
  // Physics engine for smooth sliding
  cMainX = lerp(cMainX, tMainX, 0.08); cMainY = lerp(cMainY, tMainY, 0.08);
  cLeftX = lerp(cLeftX, tLeftX, 0.08); cLeftY = lerp(cLeftY, tLeftY, 0.08);
  cExtraX = lerp(cExtraX, tExtraX, 0.08); cExtraY = lerp(cExtraY, tExtraY, 0.08);

  // --- DRAW CHOCOLATE PIECES ---
  drawShapes(lowerHalf, 0, 0); 
  drawShapes(mainUpper, cMainX, cMainY); 
  drawShapes(leftColumn, cLeftX, cLeftY);
  drawShapes(extraPiece, cExtraX, cExtraY);
  
  // --- DRAW WHITE DOTTED CUT LINES (ONLY IN STEP 1) ---
  if (currentStep === 1) {
    stroke(255); 
    strokeWeight(4); 
    strokeCap(ROUND); 
    drawingContext.setLineDash([1, 10]); 
    
    line(startX, startY + 4 * pHeight, startX + 4 * pWidth, startY + 3 * pHeight);
    line(startX + pWidth, startY, startX + pWidth, startY + 3.75 * pHeight); 
    line(startX, startY + pHeight, startX + pWidth, startY + pHeight);
    
    drawingContext.setLineDash([]); 
    strokeCap(SQUARE);
  }

  // --- NARRATIVE TEXT ---
  fill(255); noStroke(); textAlign(CENTER);
  
  textSize(24);
  text("The Infinite Chocolate Trick", width/2, 40);
  
  textSize(18);
  fill('#AAAAAA');
  text("(Click anywhere to advance to the next step)", width/2, 70);

  fill(255);
  textSize(20);
  let narrative = "";
  
  switch(currentStep) {
    case 0: narrative = "Consider a standard chocolate bar having 6 rows and 4 columns."; break;
    case 1: narrative = "We map out our cuts to isolate the top-left block."; break;
    case 2: narrative = "First, we remove the extra piece from the top left corner."; break;
    case 3: narrative = "Next, the large upper piece slides down the diagonal slope."; break;
    case 4: narrative = "Then, the remaining column slides up to fill the gap."; break;
    case 5: narrative = "Voila! We have a full bar again, plus an extra piece! (Click to reset)"; break;
  }
  
  text(narrative, width/2, height - 40);
}

// --- THE UPGRADED DRAWING FUNCTION ---
function drawShapes(shapeArray, offsetX, offsetY) {
  for (let i = 0; i < shapeArray.length; i++) {
    let poly = shapeArray[i];

    // 1. Fill the polygon with a chocolate-colored border to hide the background seamlessly
    stroke(chocolateColor);
    strokeWeight(2);
    fill(chocolateColor);
    
    // Override color for the extra piece when it separates!
    if (currentStep >= 2 && shapeArray === extraPiece) {
      fill('#D4AF37');
      stroke('#B5952F');
    }

    beginShape();
    for (let j = 0; j < poly.length; j++) {
      vertex(poly[j].x + offsetX, poly[j].y + offsetY);
    }
    endShape(CLOSE);

    // 2. ONLY draw black borders on the Horizontal and Vertical edges (the true grid lines)
    stroke(0);
    strokeWeight(2);
    for (let j = 0; j < poly.length; j++) {
      let p1 = poly[j];
      let p2 = poly[(j + 1) % poly.length];

      // Math Check: Is the edge horizontal or vertical?
      let isHorizontal = abs(p1.y - p2.y) < 0.1;
      let isVertical = abs(p1.x - p2.x) < 0.1;

      // If it's a sloped line (our diagonal cut), it skips this entirely!
      if (isHorizontal || isVertical) {
        line(p1.x + offsetX, p1.y + offsetY, p2.x + offsetX, p2.y + offsetY);
      }
    }
  }
}
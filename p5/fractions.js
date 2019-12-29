setup = () => {
    createCanvas(500, 500);
    background(0);
    stroke(255);
    colorMode(HSB);
    translate(height / 2, width / 2);
    scale(4, -4);
    noFill();
    circle(0, 0, 100);
    for (den = 10; den > 0; den--) {
        for (num = 1; num <= den; num++) {
            console.log(num, den);
            stroke(Math.floor(den * 360 / 10), 255, 255);
            let a = num * TWO_PI / den;
            line(0, 0, 50 * cos(a), 50 * sin(a));
        }
    }
}
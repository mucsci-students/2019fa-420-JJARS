// ScrUML
// diagram.js
// Team JJARS

class Diagram {

    constructor(canvasID) {
        if (!canvasID)
            console.error("No canvas ID provided in Diagram constructor.");
        this.canvasID = canvasID;
    }

    update() {

        var draw = new SVG(this.canvasID).size(500, 500);
        var rect = draw.rect(100, 50);
        rect.draggable();

    }

}

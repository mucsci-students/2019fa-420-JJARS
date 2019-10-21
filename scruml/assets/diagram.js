// ScrUML
// diagram.js
// Team JJARS

class Diagram {

    constructor(canvasID) {
        if (!canvasID)
            console.error("No canvas ID provided in Diagram constructor.");
        this.canvas = new SVG(canvasID).size(1000, 1000);
    }

    buildClassElement(className, classAttr) {

        const W = 150; // Rectangle width
        const H = 50;  // Rectangle height

        // Build element on the canvas
        var element = this.canvas.nested().id(className).addClass("uml-class");

        // Add body and text
        element.rect(W,H).fill("#ffffff");
        element.text(className).fill("#1C140D");

        // Place element at the appropriate coordinates, if in the attributes
        if (classAttr["[x]"] && classAttr["[y]"])
        {
            element.move(classAttr["[x]"] - (W/2), classAttr["[y]"] - (H/2));
        }

        // Make element draggable
        element.draggable();

        // Hook element in to click event handler
        element.click(function() {
            elementClicked(this);
        });

    }

    update() {

        // "this" is shadowed by a reference to the promise in the callback
        var me = this;

        // Get the diagram and get to work
        pywebview.api.getDiagram().then(function(response) {

            // Remove classes that are no longer in the diagram
            me.canvas.each(function(i, children) {
                if (this.hasClass("uml-class"))
                {
                    if (!(this.id in response.classes))
                    {
                        this.remove();
                    }
                }
            });

            // Check for new classes in the diagram
            for (let [key, value] of Object.entries(response.classes))
            {

                // If the class isn't on the diagram yet, add it
                if (!SVG.get(key))
                {
                    me.buildClassElement(key, value);

                }

            }
        });

    }

}

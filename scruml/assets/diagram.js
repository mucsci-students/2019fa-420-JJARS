// ScrUML
// diagram.js
// Team JJARS

class Diagram {

    // ----------
    // Constructor

    constructor(canvasID) {
        if (!canvasID)
            console.error("No canvas ID provided in Diagram constructor.");
        this.canvas = new SVG(canvasID).size(1000, 1000);
    }

    // ----------
    // buildClassElement

    buildClassElement(className, classAttr) {

        const W = 150; // Rectangle width
        const H = 50;  // Rectangle height

        // Build element on the canvas
        var element = this.canvas.nested().id(className).addClass("uml-class");

        // Add body and text
        element.rect(W,H);
        element.text(className).move(10, 10);

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

    // ----------
    // buildRelationshipElement

    buildRelationshipElement(relationshipID, relationshipAttr) {

    }

    // ----------
    // update

    update() {

        // "this" is shadowed by a reference to the promise in the callback
        var me = this;

        // Get the diagram object and get to work
        pywebview.api.getDiagram().then(function(response) {

            // Remove classes from the canvas that are no longer in the diagram
            me.canvas.each(function(i, children) {
                if (this.hasClass("uml-class"))
                {
                    if (!(this.id() in response.classes))
                    {
                        this.remove();
                    }
                }
            });

            // Add new classes in the diagram that are not yet on the canvas
            for (let [key, value] of Object.entries(response.classes))
            {
                if (!SVG.get(key))
                {
                    me.buildClassElement(key, value);

                }
            }

            // Remove relationships from the canvas that are no longer in the diagram

            // Add new relationships in the diagram that are not yet on the canvas

        });

    }

}

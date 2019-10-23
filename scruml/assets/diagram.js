// ScrUML
// diagram.js
// Team JJARS

const CLASS_WIDTH = 150;
const CLASS_HEIGHT = 50;

class Diagram {

    // ----------
    // Constructor

    constructor(canvasID) {
        if (!canvasID)
            console.error("No canvas ID provided in Diagram constructor.");
        this.canvas = new SVG(canvasID).size(500, 500);
        this.canvas.click(function(event) {
            tryAddClass(event);
        })
    }

    // ----------
    // buildClassElement

    buildClassElement(className, classAttr) {

        // Build element on the canvas
        var element = this.canvas.nested().id(className).addClass("uml-class");

        // Add body and text
        element.rect(CLASS_WIDTH, CLASS_HEIGHT);
        element.text(className).move(10, 10);

        // Place element at the appropriate coordinates, if in the attributes
        if (classAttr["[x]"] && classAttr["[y]"])
        {
            element.move(classAttr["[x]"] - (CLASS_WIDTH/2), classAttr["[y]"] - (CLASS_HEIGHT/2));
        }

        // Make element draggable
        element.draggy({
            minX: 0,
            minY: 0,
            maxX: this.canvas.width() - CLASS_WIDTH,
            maxY: this.canvas.height() - CLASS_HEIGHT
        });

        console.log(this.canvas.width());

        // Hook element in to click event handler
        element.click(function() {
            classElementClicked(this);
        });

        // Hook drag stop event to handler
        var me = this;
        element.on("dragend", function(event) {
            // TODO: Fix relationships on drag
            // me.update();
        });

    }

    // ----------
    // buildRelationshipElement

    buildRelationshipElement(relationshipID, relationshipAttr) {

        // Remove starting and ending brackets from relationship ID
        var relationshipID = relationshipID.slice(1, -1);

        // Get class names from relationship ID
        var names = relationshipID.split(",");
        var classNameA = names[0];
        var classNameB = names[1];

        // Build element on the canvas
        var element = this.canvas.nested().id(relationshipID).addClass("uml-relationship");

        // Draw line on the canvas
        var classAElem = SVG.get(classNameA);
        var classBElem = SVG.get(classNameB);
        classAElem.connectable({"sourceAttach": "perifery",
                                "targetAttach": "perifery",
                                "type": "curved"},
                               classBElem);
        // element.line(classAElem.x() + (CLASS_WIDTH/2), classAElem.y() + (CLASS_HEIGHT/2),
        //              classBElem.x() + (CLASS_WIDTH/2), classBElem.y() + (CLASS_HEIGHT/2));

        // Hook element in to click event handler
        element.click(function() {
            relationshipElementClicked(this);
        });

    }

    // ----------
    // update

    update() {

        // "this" is shadowed by a reference to the promise in the callbacks
        var me = this;

        // Get the classes in the diagram
        pywebview.api.getAllClasses().then(function(response) {

            console.log(response);
            var classes = response;

            // Get the relationships in the diagram
            pywebview.api.getAllRelationships().then(function(response) {

                console.log(response);
                var relationships = response;

                console.log(classes);
                console.log(relationships);

                // Remove elements from the canvas that are no longer in the diagram
                me.canvas.each(function(i, children) {
                    if (!(this.id() in classes) || !(this.id() in relationships))
                    {
                        this.remove();
                    }
                });

                for (let [key, value] of Object.entries(classes))
                {
                    if (!SVG.get(key))
                    {
                        me.buildClassElement(key, value);

                    }
                }

                for (let [key, value] of Object.entries(relationships))
                {
                    if (!SVG.get(key))
                    {
                        me.buildRelationshipElement(key, value);
                    }
                }

            });

        });

    }

}

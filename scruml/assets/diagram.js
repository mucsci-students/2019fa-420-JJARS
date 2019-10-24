// ScrUML
// diagram.js
// Team JJARS

const CLASS_WIDTH = 150;
const CLASS_HEIGHT = 50;

class Diagram {

    // ----------
    // Constructor

    constructor(canvasID) {

        // Capture canvas element
        if (!canvasID)
            console.error("No canvas ID provided in Diagram constructor.");
        this.canvas = new SVG(canvasID).size(500, 500);
        this.canvas.mousedown(function(event) {
            tryAddClass(event);
        })

        // Set environment variables
        this.draggingEnabled = false;

    }

    // ----------
    // buildClassElement

    buildClassElement(className, classAttr) {

        // Build element on the canvas with appropriate ID and classification
        var element = this.canvas.nested().id(className).addClass("uml-class");

        // Add body and text
        element.rect(CLASS_WIDTH, CLASS_HEIGHT);
        element.text(className).move(10, 10);

        // Place element at the appropriate coordinates, if in the attributes
        if (classAttr["[x]"] && classAttr["[y]"])
        {
            element.move(classAttr["[x]"], classAttr["[y]"]);
        }

        // Hook element in to click event handler
        element.mousedown(function() {
            classElementClicked(this);
        });

        // Hook drag stop event to handler
        element.on("dragend", function(event) {
            classElementDragged(this);
        });

    }

    // ----------
    // buildRelationshipElement

    buildRelationshipElement(relationshipID, relationshipAttr) {

        // Get class names from relationship ID
        var names = relationshipID.slice(1, -1).split(",");
        var classNameA = names[0];
        var classNameB = names[1];

        // Draw connector to the canvas
        var classAElem = SVG.get(classNameA);
        var classBElem = SVG.get(classNameB);
        var connector = classAElem.connectable({"sourceAttach": "perifery",
                                                "targetAttach": "perifery",
                                                "type": "curved"},
                                               classBElem).connector;

        // Give the connector an ID and classify it properly
        connector.id(relationshipID).addClass("uml-relationship");

        // Hook element in to click event handler
        connector.click(function() {
            relationshipElementClicked(this);
        });

    }

    // ----------
    // setDragging

    setDragging(enable) {

        // Set global dragging flag
        this.draggingEnabled = enable;

        // "this" is shadowed by a reference to the element in the "each" loop
        var me = this;

        // Set dragging behavior of every UML class
        this.canvas.each(function(i, children) {
            if (this.hasClass("uml-class")) {

                // Enable dragging
                if (enable && typeof this.fixed !== "function")
                {
                    this.draggy({
                        minX: 0,
                        minY: 0,
                        maxX: me.canvas.width() - CLASS_WIDTH,
                        maxY: me.canvas.height() - CLASS_HEIGHT
                    });
                }
                else if (!enable && typeof this.fixed === "function")
                {
                    this.fixed();
                }
            }
        });

    }

    // ----------
    // update

    update() {

        // "this" is shadowed by a reference to the promise in the callbacks
        var me = this;

        // Get the classes in the diagram
        pywebview.api.getAllClasses().then(function(response) {

            var classes = response;

            // Get the relationships in the diagram
            pywebview.api.getAllRelationships().then(function(response) {

                var relationships = response;

                // Remove elements from the canvas that are no longer in the diagram
                me.canvas.each(function(i, children) {
                    if (!(this.id() in classes) || !(this.id() in relationships))
                    {
                        this.remove();
                    }
                });

                // Add any new classes to the canvas
                for (let [key, value] of Object.entries(classes))
                {
                    if (!SVG.get(key))
                    {
                        me.buildClassElement(key, value);

                    }
                }

                // Add any new relationships to the diagram
                for (let [key, value] of Object.entries(relationships))
                {
                    if (!SVG.get(key))
                    {
                        me.buildRelationshipElement(key, value);
                    }
                }

                // Make sure that newly-created diagram elements are appropriately draggable/fixed
                me.setDragging(me.draggingEnabled);

            });

        });

    }

}

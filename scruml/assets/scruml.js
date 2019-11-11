// ScrUML
// scruml.js
// Team JJARS


// ----------
// Constants

const UI_STATES = {
    SELECT: "select",
    ADD: "add",
    CONNECT: "connect",
    REMOVE: "remove"
}


// ----------
// Global variables

var currentUIState = UI_STATES.SELECT;
var selectedElement = null;
var diagram = null;


// ---------
// Keyboard accelerator handling function

function handleKeys(keyEvent)
{

    // Menubar accelerators (Ctrl)
    if (keyEvent.ctrlKey)
    {
        switch (keyEvent.key)
        {
            case "n":
            menubarNewButtonClicked();
            break;

            case "o":
            menubarLoadButtonClicked();
            break;

            case "s":
            menubarSaveButtonClicked();
            break;
        }
    }

    // Toolbar accelerators (Alt)
    if (keyEvent.altKey)
    {
        switch (keyEvent.key)
        {
            case "s":
//            document.getElementById("toolbar-select").click();
            break;

            case "a":
//            document.getElementById("toolbar-add").click();
            break;

            case "c":
//            document.getElementById("toolbar-connect").click();
            break;

            case "r":
//            document.getElementById("toolbar-remove").click();
            break;
        }
    }

}

document.addEventListener("keyup", handleKeys);


// ---------
// Menubar button click event functions

function menubarNewButtonClicked(element)
{
    if (confirm("Create a new diagram? (Unsaved work will be lost!)"))
    {
        pywebview.api.newDiagramFile().then(function newFileUpdate(){diagram.update();});
    }
}

function menubarLoadButtonClicked(element)
{
    pywebview.api.loadDiagramFile().then(function loadFileUpdate(){diagram.update();});
}

function menubarSaveButtonClicked(element)
{
    pywebview.api.saveDiagramFile().then(function saveFileUpdate(){diagram.update();});
}


// ---------
// UML class element click event functions

function classElementClicked(element)
{
    switch (currentUIState)
    {
        case UI_STATES.SELECT:
        classElementSelect(element);
        break;

        case UI_STATES.ADD:
        break;

        case UI_STATES.CONNECT:
        classElementConnect(element);
        break;

        case UI_STATES.REMOVE:
        classElementRemove(element);
        break;
    }
}

function classElementSelect(element)
{

    changeSelection(element);

    // TODO: Loop through dictionary. For each key-value pair, append 2 input elements to propertiesList

}

function classElementConnect(element)
{

    if (selectedElement == null)
    {
        changeSelection(element);
        document.querySelector("#info-panel-content").innerHTML = "<i>Select another class to create a relationship.</i>"
        return;
    }

    var classAName = selectedElement.id();
    var classBName = element.id();
    clearSelection();

    var relationshipName = prompt("Enter the relationship name (leave blank for no name):");

    // If the user hit "cancel", return
    if (relationshipName == null) return;

    pywebview.api.addRelationship({"class_name_a": classAName,
                                   "class_name_b": classBName,
                                   "relationship_name": relationshipName}).then(function addRelationshipUpdate(response) {
                                       if (response !== "")
                                       {
                                           alert(response);
                                       }
                                       diagram.update();
                                       document.getElementById("toolbar-connect").click();
                                   });

}

function classElementRemove(element)
{
    if (element == selectedElement)
    {
        clearSelection();
    }
    pywebview.api.removeClass(element.id()).then(function removeClassUpdate() { diagram.update(); });
}

function classElementDragged(element)
{

    // Get element information
    var class_name = element.id();
    var new_x = element.node.attributes.x.nodeValue; // Only reliable way to get coordinates here. Why???
    var new_y = element.node.attributes.y.nodeValue;

    // Update class X, then class Y attributes in the backend model
    pywebview.api.setClassAttribute({"class_name": class_name,
                                     "attribute_name": "[x]",
                                     "attribute_value": new_x,
                                     "ignore_naming_rules": "true"
                                    }).then(function classXUpdateThen() {
                                        pywebview.api.setClassAttribute({"class_name": class_name,
                                                                         "attribute_name": "[y]",
                                                                         "attribute_value": new_y,
                                                                         "ignore_naming_rules": "true"
                                                                        });
                                    });

}


// ---------
// UML relationship element click event functions

function relationshipElementClicked(element)
{
    switch (currentUIState)
    {
        case UI_STATES.SELECT:
        relationshipElementSelect(element);
        break;

        case UI_STATES.ADD:
        break;

        case UI_STATES.CONNECT:
        break;

        case UI_STATES.REMOVE:
        relationshipElementRemove(element);
        break;
    }
}

function relationshipElementSelect(element)
{

    changeSelection(element);

    // TODO: Loop through dictionary. For each key-value pair, append 2 input elements to propertiesList

}

function relationshipElementRemove(element)
{
    if (element == selectedElement)
    {
        clearSelection();
    }
    pywebview.api.removeRelationship(element.id()).then(function removeRelationshipUpdate() { diagram.update(); });
}


// ----------
// Diagram canvas class add event function

function tryAddClass(event)
{

    if (currentUIState != UI_STATES.ADD)
    {
        return;
    }

    var rect = event.target.getBoundingClientRect();
    var x = event.clientX - rect.left - (CLASS_WIDTH/2);
    var y = event.clientY - rect.top - (CLASS_HEIGHT/2);

    var newClassName = prompt("Enter the name of the new class:");

    // If the user hit "cancel", return
    if (newClassName == null) return;

    pywebview.api.addClass({"class_name": newClassName,
                            "x": x,
                            "y": y}).then(function addClassUpdate(response) {
                                if (response !== "")
                                {
                                    alert(response);
                                }
                                diagram.update();
                            });

}


// ----------
// Toolbar button click event function

function toolbarButtonClicked(element)
{
    diagram.canvas.removeClass("select").removeClass("add").removeClass("connect").removeClass("remove");
    diagram.setDragging(false);
    switch (element.id)
    {
        case "toolbar-select":
        diagram.canvas.addClass("select");
        document.querySelector("#info-panel-header").innerHTML = "Select"
        document.querySelector("#info-panel-content").innerHTML = "<i>Select an element to view its properties.</i>"
        diagram.setDragging(true);
        currentUIState = UI_STATES.SELECT;
        break;

        case "toolbar-add":
        diagram.canvas.addClass("add");
        document.querySelector("#info-panel-header").innerHTML = "Add"
        document.querySelector("#info-panel-content").innerHTML = "<i>Click anywhere on the canvas to add a new class.</i>"
        currentUIState = UI_STATES.ADD;
        break;

        case "toolbar-connect":
        clearSelection();
        diagram.canvas.addClass("connect");
        document.querySelector("#info-panel-header").innerHTML = "Connect"
        document.querySelector("#info-panel-content").innerHTML = "<i>Select a class to begin creating a relationship.</i>"
        currentUIState = UI_STATES.CONNECT;
        break;

        case "toolbar-remove":
        diagram.canvas.addClass("remove");
        document.querySelector("#info-panel-header").innerHTML = "Remove"
        document.querySelector("#info-panel-content").innerHTML = "<i>Select a class or relationship to remove it.</i>"
        currentUIState = UI_STATES.REMOVE;
        break;
    }
    if (document.querySelector("#toolbar a.selected"))
        document.querySelector("#toolbar a.selected").classList.remove("selected");
    element.classList.add("selected");
}


// ----------
// Selection functions

function clearSelection()
{
    if (selectedElement != null && document.querySelector("#diagram-canvas .selected"))
        document.querySelector("#diagram-canvas .selected").classList.remove("selected");
    selectedElement = null;
}

function changeSelection(element)
{
    clearSelection();
    element.addClass("selected");
    selectedElement = element;
}


// ----------
// Page initialization

document.addEventListener("DOMContentLoaded", function contentLoadedInit() {
    setTimeout(function() {

        diagram = new Diagram("diagram-canvas");
        diagram.update();

        document.getElementById("toolbar-select").click();

    }, 50);
});

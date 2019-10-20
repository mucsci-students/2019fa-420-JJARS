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

            case "l":
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
            document.getElementById("toolbar-select").click();
            break;

            case "a":
            document.getElementById("toolbar-add").click();
            break;

            case "c":
            document.getElementById("toolbar-connect").click();
            break;

            case "r":
            document.getElementById("toolbar-remove").click();
            break;
        }
    }

}

document.addEventListener("keyup", handleKeys);


// ---------
// Menubar button click event functions

function menubarNewButtonClicked(element)
{
    pywebview.api.newDiagramFile();
    // TODO: Update/redraw diagram
}

function menubarLoadButtonClicked(element)
{
    pywebview.api.loadDiagramFile();
    // TODO: Update/redraw diagram
}

function menubarSaveButtonClicked(element)
{
    pywebview.api.saveDiagramFile();
    // TODO: Update/redraw diagram
}


// ---------
// UML element click event functions

function elementClicked(element)
{
    switch (currentUIState)
    {
        case UI_STATES.SELECT:
        elementSelect(element);
        break;

        case UI_STATES.ADD:
        break;

        case UI_STATES.CONNECT:
        elementConnect(element);
        break;

        case UI_STATES.REMOVE:
        elementRemove(element);
        break;
    }
}

function elementSelect(element)
{
    if (element.className != "class")
    {
        return;
    }

    selectedElement = element;
    highlightElement(element);
    var className = element.textContent; // TODO: Get the actual class name from element
    var attrDict = pywebview.api.getClassAttributes(className);
    var propertiesList = document.getElementById("properties-list");

    // TODO: Display class name
    // TODO: Loop through dictionary. For each key-value pair, append 2 input elements to propertiesList

}

function elementConnect(element)
{
    if (element.className != "class")
    {
        return;
    }

    if (selectedElement == null)
    {
        selectedElement = element;
        highlightElement(element, "#FF00FF");
        return;
    }

    var classAName = selectedElement.textContent; // TODO: Get the actual class name from element
    var classBName = element.textContent; // TODO: Get the actual class name from element
    var relationshipName = prompt("Enter the relationship name (leave blank for no name):");
    pywebview.api.addRelationship(classAName, classBName, relationshipName);
    clearSelection();
    // TODO: Update/redraw diagram
}

function elementRemove(element)
{
    if (element.className == "class")
    {
        var className = element.textContent; // TODO: Get the actual class name from element
        pywebview.api.completelyRemoveClass(classname); // TODO: Remove class and its relationships
        // TODO: Update/redraw diagram
    }
    else if (element.className == "relationship")
    {
        var relationshipID = element.title; // TODO: Get the actual relationship ID name from element
        // RelationshipID is a string in the form "[ClassA,ClassB,RelationshipName]". Split it into individual arguments
        var relArgs = relationshipID.split(",");
        // Remove leading '[' from first arg
        relArgs[0] = relArgs[0].slice(1);
        // Remove trailing ']' from final arg
        relArgs[2] = relArgs[2].slice(0,-1);

        pywebview.api.removeRelationship(relArgs[0],relArgs[1],relArgs[2]);
        // TODO: Update/redraw diagram
    }
}

// ----------
// Toolbar button click event function

function toolbarButtonClicked(element)
{
    var prevUIState = currentUIState;

    switch (element.id)
    {
        case "toolbar-select":
        currentUIState = UI_STATES.SELECT;
        break;

        case "toolbar-add":
        currentUIState = UI_STATES.ADD;
        break;

        case "toolbar-connect":
        currentUIState = UI_STATES.CONNECT;
        break;

        case "toolbar-remove":
        currentUIState = UI_STATES.REMOVE;
        break;
    }
    // Clear selected element upon state change
    if (prevUIState != currentUIState)
    {
        clearSelection();
    }
    document.querySelectorAll("#toolbar a.selected")[0].classList.remove("selected");
    element.classList.add("selected");
}

function highlightElement(element, hexVal = "#00FFFF")
{
    if (element)
    {
        element.style.border = "2px solid " + hexVal;
        element.style.borderRadius = "6px";
    }
}

function clearSelection()
{
    if (selectedElement)
    {
        selectedElement.style.border = "none";
    }
    selectedElement = null;
}

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
var diagram = Diagram();


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
}

function menubarLoadButtonClicked(element)
{
    pywebview.api.loadDiagramFile();
}

function menubarSaveButtonClicked(element)
{
    pywebview.api.saveDiagramFile();
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
{}

function elementConnect(element)
{}

function elementRemove(element)
{}


// ----------
// Toolbar button click event function

function toolbarButtonClicked(element)
{
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
    document.querySelectorAll("#toolbar a.selected")[0].classList.remove("selected");
    element.classList.add("selected");
}

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


// ----------
// Modal functions

function modalPrompt(message, placeholder)
{
    document.querySelector("#prompt-modal-message").innerHTML = message;
    document.querySelector("#prompt-modal-input").placeholder = placeholder;
    document.querySelector("#prompt-modal").style.display = "inherit";
}

function acceptModalPrompt()
{
    // TODO
}

function cancelModalPrompt()
{
    // TODO
}

function modalAlert(message)
{
    document.querySelector("#alert-modal-message").innerHTML = message;
    document.querySelector("#alert-modal").style.display = "inherit";
}

function dismissModalAlert()
{
    document.querySelector("#alert-modal").style.display = "none";
}


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
    diagram.changeSelection(element);
}

function classElementConnect(element)
{

    if (diagram.selectedElement == null)
    {
        diagram.changeSelection(element);
        document.querySelector("#info-panel-content").innerHTML = "<i>Select another class to create a relationship.</i>"
        return;
    }

    var classAName = diagram.selectedElement.id();
    var classBName = element.id();
    diagram.clearSelection();

    pywebview.api.addRelationship({"class_name_a": classAName, "class_name_b": classBName}).then(function addRelationshipUpdate(response) {
                                       if (response !== "")
                                       {
                                           modalAlert(response);
                                       }
                                       diagram.update();
                                       document.getElementById("toolbar-connect").click();
                                   });

}

function classElementRemove(element)
{
    if (element == diagram.selectedElement)
    {
        diagram.clearSelection();
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
    diagram.changeSelection(element);
}

function relationshipElementRemove(element)
{
    if (element == diagram.selectedElement)
    {
        diagram.clearSelection();
    }
    pywebview.api.removeRelationship(element.id()).then(function removeRelationshipUpdate() { diagram.update(); });
}


// ----------
// Rename UML class function

function renameClass()
{

    //    var newClassName = prompt("Enter a new class name:");
    var newClassName = prompt("New class name:", diagram.selectedElement.id());

    // If the user hit "cancel", return
    if (newClassName == null) return;

    pywebview.api.renameClass({"old_class_name": diagram.selectedElement.id(),
                               "new_class_name": newClassName}).then(function renameClassUpdate(response) {
                                   if (response !== "")
                                   {
                                       modalAlert(response);
                                   }
                                   diagram.update(newClassName);
                               });
}


// ----------
// Add input elements for a member function in the properties panel

function addMemberFunction(visibility = "private", type = "int", name = "func", params = "int x, float y")
{
    // TODO: name will need to be a unique function name

    var funcDiv = document.createElement("div");
    funcDiv.setAttribute('class', 'member-function');
    funcDiv.setAttribute('id', name);

    var deleteButton = document.createElement("input");
    deleteButton.setAttribute('type', 'button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('value', 'x');

    var visibilityField = document.createElement("input");
    visibilityField.setAttribute('type', 'text');
    visibilityField.setAttribute('class', 'func-visibility');
    visibilityField.setAttribute('placeholder', 'visibility');
    visibilityField.setAttribute('value', visibility);

    var retTypeField = document.createElement("input");
    retTypeField.setAttribute('type', 'text');
    retTypeField.setAttribute('class', 'func-ret-type');
    retTypeField.setAttribute('placeholder', 'type');
    retTypeField.setAttribute('value', type);

    var nameField = document.createElement("input");
    nameField.setAttribute('type', 'text');
    nameField.setAttribute('class', 'func-name');
    nameField.setAttribute('placeholder', 'funcName');
    nameField.setAttribute('value', name);

    var paramsField = document.createElement("input");
    paramsField.setAttribute('type', 'text');
    paramsField.setAttribute('class', 'func-params');
    paramsField.setAttribute('placeholder', 'int x, float y');
    paramsField.setAttribute('value', params);

    funcDiv.appendChild(deleteButton);
    funcDiv.appendChild(visibilityField);
    funcDiv.appendChild(retTypeField);
    funcDiv.appendChild(nameField);
    funcDiv.appendChild(paramsField);

    var funcList = document.getElementById("function-list");
    funcList.appendChild(funcDiv);
}


// ----------
// Add input elements for a member variable in the properties panel

function addMemberVariable(visibility = "private", type = "int", name = "var")
{
    // TODO: name will need to be unique variable name

    var varDiv = document.createElement("div");
    varDiv.setAttribute('class', 'member-variable');
    varDiv.setAttribute('id', name);

    var deleteButton = document.createElement("input");
    deleteButton.setAttribute('type', 'button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('value', 'x');

    var visibilityField = document.createElement("input");
    visibilityField.setAttribute('type', 'text');
    visibilityField.setAttribute('class', 'var-visibility');
    visibilityField.setAttribute('placeholder', 'visibility');
    visibilityField.setAttribute('value', visibility);

    var typeField = document.createElement("input");
    typeField.setAttribute('class', 'var-type');
    typeField.setAttribute('placeholder', 'type');
    typeField.setAttribute('value', type);

    var nameField = document.createElement("input");
    nameField.setAttribute('type', 'text');
    nameField.setAttribute('class', 'var-name');
    nameField.setAttribute('placeholder', 'varName');
    nameField.setAttribute('value', name);

    varDiv.appendChild(deleteButton);
    varDiv.appendChild(visibilityField);
    varDiv.appendChild(typeField);
    varDiv.appendChild(nameField);

    var varList = document.getElementById("variable-list");
    varList.appendChild(varDiv);
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
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;

    var newClassName = prompt("Enter the name of the new class:");

    // If the user hit "cancel", return
    if (newClassName == null) return;

    pywebview.api.addClass({"class_name": newClassName,
                            "x": x,
                            "y": y}).then(function addClassUpdate(response) {
                                if (response !== "")
                                {
                                    modalAlert(response);
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
        diagram.setDragging(true);
        currentUIState = UI_STATES.SELECT;
        break;

        case "toolbar-add":
        diagram.clearSelection();
        diagram.canvas.addClass("add");
        currentUIState = UI_STATES.ADD;
        break;

        case "toolbar-connect":
        diagram.clearSelection();
        diagram.canvas.addClass("connect");
        currentUIState = UI_STATES.CONNECT;
        break;

        case "toolbar-remove":
        diagram.clearSelection();
        diagram.canvas.addClass("remove");
        currentUIState = UI_STATES.REMOVE;
        break;
    }
    if (document.querySelector("#toolbar a.selected"))
        document.querySelector("#toolbar a.selected").classList.remove("selected");
    element.classList.add("selected");
}


// ----------
// Page initialization

document.addEventListener("DOMContentLoaded", function contentLoadedInit() {

    var checkLoaded = setInterval(function() {
        if (typeof(pywebview) !== 'undefined') {

            clearInterval(checkLoaded);

            diagram = new Diagram("diagram-canvas");
            diagram.update();

            document.getElementById("toolbar-select").click();
            document.getElementById("loading-modal").style.display = "none";

        }
    }, 500);
});

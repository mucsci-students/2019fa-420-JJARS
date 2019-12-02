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
                                           alert(response);
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
                                     "attribute_category": "metadata",
                                     "attribute_name": "[x]",
                                     "attribute_value": new_x,
                                     "ignore_naming_rules": "true"
                                    }).then(function classXUpdateThen() {
                                        pywebview.api.setClassAttribute({"class_name": class_name,
                                                                         "attribute_category": "metadata",
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

    var newClassName = prompt("Enter a new class name:");

    // If the user hit "cancel", return
    if (newClassName == null) return;

    pywebview.api.renameClass({"old_class_name": diagram.selectedElement.id(),
                               "new_class_name": newClassName}).then(function renameClassUpdate(response) {
                                   if (response !== "")
                                   {
                                       alert(response);
                                   }
                                   diagram.update(newClassName);
                               });
}


// ----------
// Adds/updates the member function for the selected class

function submitMemberFunction()
{
    var parentDiv = this.parentElement;

    var visibility = parentDiv.getElementsByClassName("func-visibility")[0].value;
    var returnType = parentDiv.getElementsByClassName("func-ret-type")[0].value;
    var name = parentDiv.getElementsByClassName("func-name")[0].value;
    var parameters = parentDiv.getElementsByClassName("func-params")[0].value;

    var attrData = {"class_name": diagram.selectedElement.id(),
                            "attribute_category": "function",
                            "func_visibility": visibility,
                            "func_return_type": returnType,
                            "func_name": name,
                            "func_params": parameters};

    pywebview.api.setClassAttribute(attrData).then(function alertMemberFunc(response) {
        if (response !== "")
        {
            alert(response);
            return;
        }

        // Check if function is being added or updated
        if (parentDiv.id == "[new]")
            alert("Function " + name + " has been added.");
        else
            alert("Function " + name + " has been updated.");
        parentDiv.id = name;
    });
}


// ----------
// Adds/updates the member variable for the selected class

function submitMemberVariable()
{
    var parentDiv = this.parentElement;

    var visibility = parentDiv.getElementsByClassName("var-visibility")[0].value;
    var returnType = parentDiv.getElementsByClassName("var-type")[0].value;
    var name = parentDiv.getElementsByClassName("var-name")[0].value;

    var attrData = {"class_name": diagram.selectedElement.id(),
                            "attribute_category": "variable",
                            "var_visibility": visibility,
                            "var_type": returnType,
                            "var_name": name};

    pywebview.api.setClassAttribute(attrData).then(function alertMemberVar(response) {
        if (response !== "")
        {
            alert(response);
            return;
        }

        // Check if variable is being added or updated
        if (parentDiv.id == "[new]")
            alert("Variable " + name + " has been added.");
        else
            alert("Variable " + name + " has been updated.");

        parentDiv.id = name;
    });
}

// ----------
// Add input elements for a member function in the properties panel

function addMemberFunction(visibility = "", type = "", name = "", params = "")
{
    var funcDiv = document.createElement("div");
    funcDiv.setAttribute('class', 'member-function');
    // Set the id of the div to indicate if the function is new and unsubmitted
    var divID = ((name === "") ? "[new]" : name);
    funcDiv.setAttribute('id', divID);

    var deleteButton = document.createElement("input");
    deleteButton.setAttribute('type', 'button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('value', 'x');

    var submitButton = document.createElement("input");
    submitButton.setAttribute('type', 'button');
    submitButton.setAttribute('class', 'submit-button');
    submitButton.setAttribute('value', '✓');
    submitButton.onclick = submitMemberFunction;

    var visibilityField = document.createElement("input");
    visibilityField.setAttribute('type', 'text');
    visibilityField.setAttribute('class', 'func-visibility');
    visibilityField.setAttribute('placeholder', 'visibility');
    visibilityField.setAttribute('value', visibility);

    var retTypeField = document.createElement("input");
    retTypeField.setAttribute('type', 'text');
    retTypeField.setAttribute('class', 'func-ret-type');
    retTypeField.setAttribute('placeholder', 'return type');
    retTypeField.setAttribute('value', type);

    var nameField = document.createElement("input");
    nameField.setAttribute('type', 'text');
    nameField.setAttribute('class', 'func-name');
    nameField.setAttribute('placeholder', 'func name');
    nameField.setAttribute('value', name);

    var paramsField = document.createElement("input");
    paramsField.setAttribute('type', 'text');
    paramsField.setAttribute('class', 'func-params');
    paramsField.setAttribute('placeholder', 'int x, float y, ...');
    paramsField.setAttribute('value', params);

    funcDiv.appendChild(deleteButton);
    funcDiv.appendChild(submitButton);
    funcDiv.appendChild(visibilityField);
    funcDiv.appendChild(retTypeField);
    funcDiv.appendChild(nameField);
    funcDiv.appendChild(paramsField);

    var funcList = document.getElementById("function-list");
    funcList.appendChild(funcDiv);
}


// ----------
// Add input elements for a member variable in the properties panel

function addMemberVariable(visibility = "", type = "", name = "")
{
    var varDiv = document.createElement("div");
    varDiv.setAttribute('class', 'member-variable');
    // Set the id of the div to indicate if the variable is new and unsubmitted
    var divID = ((name === "") ? "[new]" : name);
    varDiv.setAttribute('id', divID);

    var deleteButton = document.createElement("input");
    deleteButton.setAttribute('type', 'button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('value', 'x');

    var submitButton = document.createElement("input");
    submitButton.setAttribute('type', 'button');
    submitButton.setAttribute('class', 'submit-button');
    submitButton.setAttribute('value', '✓');
    submitButton.onclick = submitMemberVariable;

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
    nameField.setAttribute('placeholder', 'variable name');
    nameField.setAttribute('value', name);

    varDiv.appendChild(deleteButton);
    varDiv.appendChild(submitButton);
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
    setTimeout(function() {

        diagram = new Diagram("diagram-canvas");
        diagram.update();

        document.getElementById("toolbar-select").click();

    }, 200);
});

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

var modalPromptCallback = null;

function modalPrompt(message, placeholder, callback)
{
    document.querySelector("#prompt-modal-message").innerHTML = message;
    document.querySelector("#prompt-modal-input").placeholder = placeholder;
    document.querySelector("#prompt-modal").style.display = "inherit";
    setTimeout(function focusPromptModalInput() {
        document.querySelector("#prompt-modal-input").focus();
    }, 0);
    modalPromptCallback = callback;
}

function acceptModalPrompt()
{
    if (typeof(modalPromptCallback) === "function")
    {
        var modalPromptValue = document.querySelector("#prompt-modal-input").value;
        modalPromptCallback(modalPromptValue);
    }
    closeModalPrompt();
}

function closeModalPrompt()
{
    modalPromptCallback = null;
    document.querySelector("#prompt-modal").style.display = "none";
    document.querySelector("#prompt-modal-input").value = "";
}

function handleModalPromptKeys(keyEvent)
{
    switch (keyEvent.key)
    {
        case "Enter":
        document.querySelector("#prompt-modal-ok").click();
        break;

        case "Escape":
        document.querySelector("#prompt-modal-cancel").click();
        break;
    }
}

function modalAlert(message)
{
    document.querySelector("#alert-modal-message").innerHTML = message;
    document.querySelector("#alert-modal").style.display = "inherit";
    setTimeout(function focusAlertModalOk() {
      document.querySelector("#alert-modal-ok").focus();
    }, 0);
}

function dismissModalAlert()
{
    document.querySelector("#alert-modal").style.display = "none";
}

function handleModalAlertKeys(keyEvent)
{
    switch (keyEvent.key)
    {
        case "Enter":
        case "Escape":
        document.querySelector("#alert-modal-ok").click();
        break;
    }
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
    modalPrompt("New class name:",
                diagram.selectedElement.id(),
                function renamePromptAccepted(newClassName) {
                    pywebview.api.renameClass({
                        "old_class_name": diagram.selectedElement.id(),
                        "new_class_name": newClassName}).then(function renameClassUpdate(response) {
                            if (response !== "")
                            {
                                modalAlert(response);
                            }
                            diagram.update(newClassName);
                        });
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
                    "attribute_name": parentDiv.id,
                    "func_visibility": visibility,
                    "func_return_type": returnType,
                    "func_name": name,
                    "func_params": parameters};

    pywebview.api.removeClassAttribute(attrData).then(function () {
    pywebview.api.setClassAttribute(attrData).then(function alertMemberFunc(response) {

        if (response !== "")
        {
            modalAlert(response);
            return;
        }

        // Check if function is being added or updated
        // if (parentDiv.id == "[new]")
        //     modalAlert("Function " + name + " has been added.");
        // else
        //     modalAlert("Function " + name + " has been updated.");

        parentDiv.id = "[F:" + name + "]";
        diagram.update(diagram.selectedElement.id());

    });

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
                    "attribute_name": parentDiv.id,
                    "attribute_category": "variable",
                    "var_visibility": visibility,
                    "var_type": returnType,
                    "var_name": name};

    pywebview.api.removeClassAttribute(attrData).then(function () {
    pywebview.api.setClassAttribute(attrData).then(function alertMemberVar(response) {
        if (response !== "")
        {
            modalAlert(response);
            return;
        }

        // Check if variable is being added or updated
        // if (parentDiv.id == "[new]")
        //     modalAlert("Variable " + name + " has been added.");
        // else
        //     modalAlert("Variable " + name + " has been updated.");

        parentDiv.id = "[V:" + name + "]";
        diagram.update(diagram.selectedElement.id());
    });

    });

}

// ----------
// Removes the member for the selected class

function removeMember()
{
    var parentDiv = this.parentElement;
    var divName = parentDiv.id;

    // Delete the div tht contains the member's buttons and input fields
    parentDiv.remove();

    // Only remove the member from the model if had been submitted
    if (divName == "[new]")
    {
        return;
    }

    // Remove the member from the model
    var attrData = {"class_name": diagram.selectedElement.id(),
                            "attribute_name": divName};

    pywebview.api.removeClassAttribute(attrData).then(function alertMemberDelete(response) {
        if (response !== "")
        {
            modalAlert(response);
            return;
        }

        divName = divName.substring(3, divName.length - 1);
        // modalAlert("Member " + divName + " has been removed.");

        diagram.update(diagram.selectedElement.id());
    });
}

// ----------
// Generate random name

function stringGen(len)
{

    var text = "";

    var charset = "abcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < len; i++ )
        text += charset.charAt(Math.floor(Math.random() * charset.length));

    return text;

}

// ----------
// Add input elements for a member function in the properties panel

function addMemberFunction(visibility = "", type = "", name = "", params = "")
{

    var funcDiv = document.createElement("div");
    funcDiv.setAttribute('class', 'member-function');

    // Set the id of the div to indicate if the function is new and unsubmitted
    var divID = ((name === "") ? "[new]" : "[F:" + name + "]");
    funcDiv.setAttribute('id', divID);

    var deleteButton = document.createElement("input");
    deleteButton.setAttribute('type', 'button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('value', 'x');
    deleteButton.onclick = removeMember;

    var visibilityField = document.createElement("input");
    visibilityField.setAttribute('type', 'text');
    visibilityField.setAttribute('class', 'func-visibility');
    visibilityField.setAttribute('placeholder', 'visibility');
    visibilityField.setAttribute('value', visibility);
    visibilityField.onchange = submitMemberFunction;

    var retTypeField = document.createElement("input");
    retTypeField.setAttribute('type', 'text');
    retTypeField.setAttribute('class', 'func-ret-type');
    retTypeField.setAttribute('placeholder', 'return type');
    retTypeField.setAttribute('value', type);
    retTypeField.onchange = submitMemberFunction;

    // Generate random name if one is not provided
    if (name === "")
    {
        name = "fn_" + stringGen(4);
    }

    var nameField = document.createElement("input");
    nameField.setAttribute('type', 'text');
    nameField.setAttribute('class', 'func-name');
    nameField.setAttribute('placeholder', 'func name');
    nameField.setAttribute('value', name);
    nameField.onchange = submitMemberFunction;

    var paramsField = document.createElement("input");
    paramsField.setAttribute('type', 'text');
    paramsField.setAttribute('class', 'func-params');
    paramsField.setAttribute('placeholder', 'int x, float y');
    paramsField.setAttribute('value', params);
    paramsField.onchange = submitMemberFunction;

    funcDiv.appendChild(deleteButton);
    funcDiv.appendChild(visibilityField);
    funcDiv.appendChild(retTypeField);
    funcDiv.appendChild(nameField);
    funcDiv.appendChild(paramsField);

    var funcList = document.getElementById("function-list");
    funcList.appendChild(funcDiv);

    // Force update function
    if (diagram.selectedElement !== null)
    {
        nameField.onchange();
    }

}


// ----------
// Add input elements for a member variable in the properties panel

function addMemberVariable(visibility = "", type = "", name = "")
{

    var varDiv = document.createElement("div");
    varDiv.setAttribute('class', 'member-variable');

    // Set the id of the div to indicate if the variable is new and unsubmitted
    var divID = ((name === "") ? "[new]" : "[V:" + name + "]");
    varDiv.setAttribute('id', divID);

    var deleteButton = document.createElement("input");
    deleteButton.setAttribute('type', 'button');
    deleteButton.setAttribute('class', 'delete-button');
    deleteButton.setAttribute('value', 'x');
    deleteButton.onclick = removeMember;

    var visibilityField = document.createElement("input");
    visibilityField.setAttribute('type', 'text');
    visibilityField.setAttribute('class', 'var-visibility');
    visibilityField.setAttribute('placeholder', 'visibility');
    visibilityField.setAttribute('value', visibility);
    visibilityField.onchange = submitMemberVariable;

    var typeField = document.createElement("input");
    typeField.setAttribute('class', 'var-type');
    typeField.setAttribute('placeholder', 'type');
    typeField.setAttribute('value', type);
    typeField.onchange = submitMemberVariable;

    // Generate random name if one is not provided
    if (name === "")
    {
        name = "var_" + stringGen(4);
    }

    var nameField = document.createElement("input");
    nameField.setAttribute('type', 'text');
    nameField.setAttribute('class', 'var-name');
    nameField.setAttribute('placeholder', 'variable name');
    nameField.setAttribute('value', name);
    nameField.onchange = submitMemberVariable;

    varDiv.appendChild(deleteButton);
    varDiv.appendChild(visibilityField);
    varDiv.appendChild(typeField);
    varDiv.appendChild(nameField);

    var varList = document.getElementById("variable-list");
    varList.appendChild(varDiv);

    // Force update function
    if (diagram.selectedElement !== null)
    {
        nameField.onchange();
    }

}

// ----------
// relabelRelationship

function setRelationshipAttrValue(key, value)
{
    var attrData = {
        "attr_key": "label",
        "attr_value": this.value,
        "relationship_id": diagram.selectedElement.id()
    };
    pywebview.api.setRelationshipAttribute(attrData).then(function alertRelabelRelationship() {
        if (response !== "")
        {
            modalAlert(response);
            return;
        }
        diagram.update(diagram.selectedElement.id());
    });
}
function changeRelationshipType()
{
    var attrData = {
        "attr_key": "type",
        "attr_value": this.value,
        "relationship_id": diagram.selectedElement.id()
    };
    pywebview.api.setRelationshipAttribute(attrData).then(function alertChangeRelationshipType() {
        if (response !== "")
        {
            modalAlert(response);
            return;
        }
        diagram.update(diagram.selectedElement.id());
    });
}
function changeRelationshipMultiplicity()
{
    var attrData = {
        "attr_key": "multiplicity",
        "attr_value": this.value,
        "relationship_id": diagram.selectedElement.id()
    };
    pywebview.api.setRelationshipAttribute(attrData).then(function alertChangeRelationshipType() {
        if (response !== "")
        {
            modalAlert(response);
            return;
        }
        diagram.update(diagram.selectedElement.id());
    });
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

    modalPrompt("New class name:",
                "className",
                function addClassPromptAccepted(newClassName) {
                    pywebview.api.addClass({
                        "class_name": newClassName,
                        "x": x,
                        "y": y}).then(function addClassUpdate(response) {
                            if (response !== "")
                            {
                                modalAlert(response);
                            }
                            diagram.update();
                        });
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

    // Check every 500ms to see if pywebview has loaded
    var checkLoaded = setInterval(function() {
        if (typeof(pywebview) !== 'undefined') {

            // Clear the check interval timer
            clearInterval(checkLoaded);

            // Initialize and draw the canvas
            diagram = new Diagram("diagram-canvas");
            diagram.update();

            // Default the current UI state to selection mode
            document.getElementById("toolbar-select").click();

            // Add hotkey handling to modal dialogs
            document.querySelector("#prompt-modal-input").addEventListener("keyup", handleModalPromptKeys);
            document.querySelector("#alert-modal-ok").addEventListener("keyup", handleModalAlertKeys);

            // Hide the loading screen to allow user interaction
            document.getElementById("loading-modal").style.display = "none";

        }
    }, 500);
});

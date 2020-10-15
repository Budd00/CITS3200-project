
//Used for finding the direct parent of the currently selected tag
function find_parent(input_id) {
    //This whole string of parentNodes gives the tag id of the direct parent
    let parent_tag = input_id.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute("value")
    console.log(parent_tag)
    let parent_tag_input = input_id
    //For loop is used to find the input field of the parent tag
    for(let i = 0; i < parent_tag_input.children.length; i++) {
        if(parent_tag_input.children[i].name =='parent_tag') {
            parent_tag_input = parent_tag_input.children[i]
        }
    }
    //Value of the parent tag input field is initialised so the Django back-end can read the data when the form is submitted
    parent_tag_input.value = parent_tag
    return true;
}

$(document).ready(function() {
    $('.js-example-basic-single').select2();
    
});

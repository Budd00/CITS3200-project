//Quick search
function search_tag(input) {
    const keyword = input.value.toLowerCase()
    root_tag_list = document.getElementsByClassName("root_tag")

    for(let i = 0; i < root_tag_list.length; i++) {
        if( root_tag_list[i].innerText.toLowerCase().includes(keyword)) {
            root_tag_list[i].style.display = 'block'
        }
        else {
            root_tag_list[i].style.display = 'none'
        }
    }
}

//function finds all tags which are the same as the selected tag
function find_same_tags(input) {
    tag_list = document.getElementsByClassName(input.classList[0])
    for( let i = 0; i < tag_list.length; i++) {
        if( tag_list[i] != input) {
            tag_list[i].checked = !tag_list[i].checked
        }
    }
}
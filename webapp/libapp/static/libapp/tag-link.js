
function search_tag(input) {
    //console.log(input.value)
    const keyword = input.value.toLowerCase()
    root_tag_list = document.getElementsByClassName("root_tag")
    //console.log(root_tag_list)

    for(let i = 0; i < root_tag_list.length; i++) {
        root_tag_list[i].style.display = 'none'
    }
    
    for(let i = 0; i < root_tag_list.length; i++) {
        if( root_tag_list[i].children[0].children[0].children[0].children[0].innerText.toLowerCase().includes(keyword)) {
            root_tag_list[i].style.display = 'block'
        }

        if(root_tag_list[i].children.length > 2) { //Has child tags
            //console.log(root_tag_list[i])
            let current_tag = root_tag_list[i].children[2]
            if( recursive_search(current_tag, keyword) == true) {
                root_tag_list[i].style.display = 'block';
            }
        }
            
            
        
            /*
            while( current_tag != undefined) {
                for(let j = 0; j < current_tag.children.length; j++) {
                    if( current_tag.children[j].outerHTML == "<p></p>") {
                        continue
                    }
                    //console.log(root_tag_list[i].children[2].children[j])
                    //console.log(root_tag_list[i].children[2].children[j].children[0])
                    if(current_tag.children[j].children[0].children[0].children[0].innerText.toLowerCase().includes(keyword)) {
                        root_tag_list[i].style.display = 'block';
                    }
                }
            }
            */


    }
}

function recursive_search(current_tag, keyword) {
    for (let i = 0; i < current_tag.children.length; i++) {
        if( current_tag.children[i].outerHTML == "<p></p>") {
            continue
        }
        else if (current_tag.children[i].children[0].children[0].children[0].innerText.toLowerCase().includes(keyword)) {
            return true
        }
        else if (current_tag.children[i].children.length > 2) { //Has child tags
            if( recursive_search(current_tag.children[i].children[2], keyword) == true) {
                return true
            }
        }
    }
    return false
}
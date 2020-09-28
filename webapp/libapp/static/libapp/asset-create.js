console.log("Lets do this");

//console.log(document.getElementById('tag-list').children)


let number = 2
/*
for(let i = 0; i < number; i++) {
    let current_id = document.getElementById('id_parent_' + i)
    if(current_id.parentNode.innerText.includes('---')) {
        console.log("Is a child")
    }
}
*/
console.log(document.getElementById('id_parent_0'))
$(document).ready(function(){
        $(".tag-selection").click(function() {
            let str = this.id
            let matches = str.match(/(\d+)/)
            console.log(matches[0])
            for(let i = matches[0] + 1; i < number; i++) {
                let current_id = document.getElementById('id_parent_' + i)
                if(current_id.parentNode.innerText.includes('---')) {
                    console.log("Is a child")
                    //continues
                }
            }
        })
})
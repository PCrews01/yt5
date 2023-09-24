
function checkLink(){
    let linkfield = document.querySelector('#yt-link')
    let sub = document.querySelector('#sub_btn');
    // console.log("Err", linkfield.value)

    if(linkfield.value.length >= 1){
        sub.removeAttribute('disabled')
    } else {
        if(!sub.hasAttribute('disabled')){
            sub.setAttribute('disabled', true)
        }
    }
    
}
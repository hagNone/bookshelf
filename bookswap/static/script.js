function toggleform(){
    let Element_ID = document.getElementById("toggleContent");
    if(Element_ID.style.display === 'none')
    {
        Element_ID.style.display = "block"
    }
    else{
        Element_ID.style.display = "none"
    }
}

function searchbook(){
    let query = document.getElementById("searchBox").value.toLowerCase();
    let books = document.querySelectorAll("#booklist li");

    console.log("Search triggered: ", query);

    books.forEach(book => {
        if(book.textContent.toLowerCase().includes(query)){
            book.style.display = "block";
        }
        else{
            book.style.display = "none";
        }
    });
}

// window.onload(document.getElementById("toggleBtn").addEventListener("click",
//     function (){
//         console.log("button clicked")
//         let Element_ID = document.getElementById("toggleContent");
//         if(Element_ID.style.display === 'none' || Element_ID.style.display === "")
//         {
//             Element_ID.style.display = "block"
//         }
//         else{
//             Element_ID.style.display = "none"
//         }
//     }
// ))
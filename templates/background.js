// ! get rekt lol
// var loadFile = function(event) {
    

//     // send it as a get request to the server
//     var xhr = new XMLHttpRequest();

//     xhr.onreadystatechange = function() {
//       if (this.readyState === XMLHttpRequest.DONE) {
//         // Request finished. Do processing here.
//         console.log(this.responseText);
//     }
//     }

//     var selectedfile = document.getElementById("myinput").files;
//     var caption=document.getElementById("caption").value;
//     var result="";
//     var srcData;
//     if (selectedfile.length > 0) {
//       var imageFile = selectedfile[0];
//       var fileReader = new FileReader();
//       fileReader.onload = function(fileLoadedEvent) {
//         srcData = fileLoadedEvent.target.result;
//         // console.log(caption)
//         // console.log(srcData)
//         // console.log(data)
//         requestUrl = "http://localhost:5000/gen"
     
//         xhr.open("POST", requestUrl, true);
//         // xhr.onreadystatechange = callback;
//         xhr.setRequestHeader("Content-Type", "application/json");

//         xhr.send(JSON.stringify(
//             {
//                 "caption": caption,
//                 "img_base64": srcData
//             }
//         ));
//       }
//       fileReader.readAsDataURL(imageFile);
//     }

    
//     // fetch(requestUrl).then(function(response) {
//     //     return response.json();
//     //     }).then(function(data) {
//     //         console.log(data);
//     // });

    
// }
// document.getElementById('button').addEventListener('click', loadFile);
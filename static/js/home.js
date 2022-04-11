let imageInput = document.getElementById("image_input");
let videoInput = document.getElementById("video_input");
let imageContainer = document.getElementById("imageContainer");
let videoContainer = document.getElementById("videoContainer");

let ImageList = imageInput.value;
let VideoList = imageInput.value; 
console.log(imageInput.value)
console.log(VideoList)
let id = 0;

function previewImage(){
    imageContainer.style.visibility = "visible";
    ImageList.push.apply(ImageList, imageInput.files);
    imageContainer.innerHTML = "";
    for(i of ImageList){
        let reader = new FileReader();
        let figuer = document.createElement("figuer");
        let figCap = document.createElement("figcaption");

        let del = document.createElement("input");
        del.setAttribute("type","button");

        figCap.innerHTML = id;

        figuer.setAttribute("id", id);
        del.id = id;
        del.name = i.name;
        id += 1;

        del.value = "×";


        del.onclick = () => {
            console.log(ImageList);
            document.getElementById(`${del.id}`).remove();
            ImageList = ImageList.filter( image => image.name !== del.name);
            console.log(ImageList);
            imageInput.setAttribute("value", ImageList);
        };

        figuer.appendChild(del);
        figuer.appendChild(figCap);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src", reader.result);
            figuer.insertBefore(img,figCap);
        }
        imageContainer.appendChild(figuer);
        reader.readAsDataURL(i);
    }
    imageInput.setAttribute("value", ImageList);
};

function previewVideo(){
    videoContainer.style.visibility = "visible";
    VideoList.push.apply(VideoList, videoInput.files);
    videoContainer.innerHTML = "";
    for(i of VideoList){
        let reader = new FileReader();
        let figuer = document.createElement("figuer");
        let figCap = document.createElement("figcaption");
        let del = document.createElement("input");
        del.setAttribute("type","button");

        figCap.innerHTML = id;

        figuer.setAttribute("id", id);
        del.name = i.name;
        del.id = id
        id += 1;
        del.value = "×";


        del.onclick = () => {
            console.log(VideoList);
            document.getElementById(`${del.id}`).remove();
            VideoList = VideoList.filter( video => video.name !== del.name);
            console.log(VideoList);
            videoInput.setAttribute("value", VideoList);
        };

        figuer.appendChild(del);
        figuer.appendChild(figCap);
        reader.onload=()=>{
            let vid = document.createElement("video");
            vid.setAttribute("src", reader.result);
            figuer.insertBefore(vid,figCap);
            vid.autoplay = false;
            vid.controls = true;
            vid.style.width = "100%"
        };
        videoContainer.appendChild(figuer);
        reader.readAsDataURL(i);
    }
    videoInput.setAttribute("value", VideoList);
    console.log(videoInput)
    console.log(VideoList)
}
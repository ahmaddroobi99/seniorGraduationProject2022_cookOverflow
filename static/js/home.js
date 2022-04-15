let imageInput = document.getElementById("image_input");
let videoInput = document.getElementById("video_input");
let imageContainer = document.getElementById("imageContainer");
let videoContainer = document.getElementById("videoContainer");

var ImageList = [];
let VideoList = [];
let id = 1000;

function previewImage() {
    imageContainer.style.visibility = "visible";
    ImageList.push.apply(ImageList, imageInput.files);
    imageContainer.innerHTML = "";

    for (i in ImageList) {
        let reader = new FileReader();
        let figuer = document.createElement("figuer");
        let figCap = document.createElement("figcaption");

        let del = document.createElement("input");
        del.setAttribute("type", "button");

        figCap.innerHTML = id;

        figuer.setAttribute("id", id);
        del.id = id;
        console.log(del.id);
        del.name = ImageList[i].name;
        console.log(del.name);
        id += 1;

        del.value = "×";


        del.onclick = () => {
            console.log(ImageList);
            document.getElementById(`${del.id}`).remove();
            ImageList = ImageList.filter(image => image.name !== del.name);
            console.log(ImageList);
        };

        figuer.appendChild(del);
        figuer.appendChild(figCap);
        reader.onload = () => {
            let img = document.createElement("img");
            img.setAttribute("src", reader.result);
            figuer.insertBefore(img, figCap);
        }
        imageContainer.appendChild(figuer);
        reader.readAsDataURL(ImageList[i]);
    }
};



function previewVideo() {
    videoContainer.style.visibility = "visible";
    VideoList.push.apply(VideoList, videoInput.files);
    videoContainer.innerHTML = "";
    for (i of VideoList) {
        let reader = new FileReader();
        let figuer = document.createElement("figuer");
        let figCap = document.createElement("figcaption");
        let del = document.createElement("input");
        del.setAttribute("type", "button");

        figCap.innerHTML = id;

        figuer.setAttribute("id", id);
        del.name = i.name;
        del.id = id
        id += 1;
        del.value = "×";


        del.onclick = () => {
            console.log(VideoList);
            document.getElementById(`${del.id}`).remove();
            VideoList = VideoList.filter(video => video.name !== del.name);
            console.log(VideoList);
            videoInput.setAttribute("value", VideoList);
        };

        figuer.appendChild(del);
        figuer.appendChild(figCap);
        reader.onload = () => {
            let vid = document.createElement("video");
            vid.setAttribute("src", reader.result);
            figuer.insertBefore(vid, figCap);
            vid.autoplay = false;
            vid.controls = true;
            vid.style.width = "100%"
        };
        videoContainer.appendChild(figuer);
        reader.readAsDataURL(i);
    }
}

function submitFiles() {
    // var dataForm = $('#create_post').serialize();
    // dataForm.append("images", ImageList);
    // dataForm.append("csrfmiddlewaretoken", "{{ csrf_token }}");
    $.ajax({
        type: 'post',
        data: {
            "images": ImageList
        },
        error: function() {
            alert("no");
        },
        success: function() {
            alert("OK");
        }
    });
}


function removeItem(id, name) {
    console.log(ImageList);
    document.getElementById(`${id}`).remove();
    ImageList = ImageList.filter(image => image.name !== name);
    console.log(ImageList);
}
document.getElementById("imageupload").addEventListener("change", function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const imgPreview = document.getElementById("imagepreview");
    imgPreview.style.backgroundImage = "url('" + e.target.result + "')";
    document.querySelector(".image-section").style.display = "block";
  };

  reader.readAsDataURL(file);
});

document.getElementById("btn-predict").addEventListener("click", function() {
  document.querySelector(".loader").style.display = "block";
  const formData = new FormData(document.getElementById("upload-file"));
  
  fetch("/predict", {
    method: "POST",
    body: formData
  })
  .then(response => response.text())
  .then(result => {
    document.querySelector(".loader").style.display = "none";
    document.getElementById("result").innerHTML = "<span>" + result + "</span>";
  })
  .catch(error => {
    document.querySelector(".loader").style.display = "none";
    console.error("Error:", error);
  });
});

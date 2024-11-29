const webcamElement = document.getElementById('webcam');
const webcam = new Webcam(webcamElement, 'user');
const modelPath = 'models';
let faceDetected = false;
let currentStream;
let displaySize;
let canvas;
let faceDetection;

$("#webcam-switch").change(function () {
  if (this.checked) {
    webcam.start()
      .then(result => {
        cameraStarted();
        webcamElement.style.transform = "";
        console.log("webcam started");
      })
      .catch(err => {
        displayError();
      });
  }
  else {
    cameraStopped();
    webcam.stop();
    console.log("webcam stopped");
  }
});

$('#cameraFlip').click(function () {
  webcam.flip();
  webcam.start()
    .then(result => {
      webcamElement.style.transform = "";
    });
});

$("#webcam").bind("loadedmetadata", function () {
  displaySize = { width: this.scrollWidth, height: this.scrollHeight }
});

$("#detection-switch").change(function () {
  if (this.checked) {
    toggleContrl("box-switch", true);
    toggleContrl("landmarks-switch", true);
    toggleContrl("expression-switch", true);
    toggleContrl("age-gender-switch", true);
    $("#box-switch").prop('checked', true);
    $(".loading").removeClass('d-none');
    Promise.all([
      faceapi.nets.tinyFaceDetector.load(modelPath),
      faceapi.nets.faceLandmark68TinyNet.load(modelPath),
      faceapi.nets.faceExpressionNet.load(modelPath),
      faceapi.nets.ageGenderNet.load(modelPath)
    ]).then(function () {
      createCanvas();
      startDetection();
    })
  }
  else {
    clearInterval(faceDetection);
    toggleContrl("box-switch", false);
    toggleContrl("landmarks-switch", false);
    toggleContrl("expression-switch", false);
    toggleContrl("age-gender-switch", false);
    if (typeof canvas !== "undefined") {
      setTimeout(function () {
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
      }, 1000);
    }
  }
});

function createCanvas() {
  if (document.getElementsByTagName("canvas").length == 0) {
    canvas = faceapi.createCanvasFromMedia(webcamElement)
    document.getElementById('webcam-container').append(canvas)
    faceapi.matchDimensions(canvas, displaySize)
  }
}

function toggleContrl(id, show) {
  if (show) {
    $("#" + id).prop('disabled', false);
    $("#" + id).parent().removeClass('disabled');
  } else {
    $("#" + id).prop('checked', false).change();
    $("#" + id).prop('disabled', true);
    $("#" + id).parent().addClass('disabled');
  }
}

function startDetection() {
  faceDetection = setInterval(async () => {
    const detections = await faceapi.detectAllFaces(webcamElement, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks(true).withFaceExpressions().withAgeAndGender()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    if ($("#box-switch").is(":checked")) {
      faceapi.draw.drawDetections(canvas, resizedDetections)
    }
    if ($("#landmarks-switch").is(":checked")) {
      faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)

    }
    if ($("#expression-switch").is(":checked")) {
      faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
    }
    if ($("#age-gender-switch").is(":checked")) {
      resizedDetections.forEach(result => {
        const { age, gender, genderProbability } = result
        new faceapi.draw.DrawTextField(
          [
            `${faceapi.round(age, 0)} years`,
            `${gender} (${faceapi.round(genderProbability)})`
          ],
          result.detection.box.bottomRight
        ).draw(canvas)
      })
    }
    if (detections.length > 0 && !faceDetected) {
      faceDetected = true;
      getSnap();
    } else if (detections.length === 0) {
      faceDetected = false;
    }

    if (!$(".loading").hasClass('d-none')) {
      $(".loading").addClass('d-none')
    }
  }, 300)
}

function getSnap() {
  const ctx = canvas.getContext('2d');
  ctx.drawImage(webcamElement, 0, 0, canvas.width, canvas.height);

  const image = canvas.toDataURL();

  // document.getElementById('snap').innerHTML = '<img src="' + image + '"/>';

  sendImageToBackend(image);
}

function sendImageToBackend(imageBase64) {
  fetch('http://localhost:5000/faceTrain/detect-face', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      image: imageBase64,
    }),
  })
  .then(response => response.json())
  .then(data => {
    if(data.distance){
      document.getElementById('response').innerHTML = 'Nama: ' + data.nim + ', nilai distance =' + data.distance;
    }
    else{
      document.getElementById('response').innerHTML = 'Wajah tidak ditemukan';
    }
  })
  .catch((error) => {
    document.getElementById('response').innerHTML = 'Error: ' + error;
  });
}

function cameraStarted() {
  toggleContrl("detection-switch", true);
  $("#errorMsg").addClass("d-none");
  if (webcam.webcamList.length > 1) {
    $("#cameraFlip").removeClass('d-none');
  }
}

function cameraStopped() {
  toggleContrl("detection-switch", false);
  $("#errorMsg").addClass("d-none");
  $("#cameraFlip").addClass('d-none');
}

function displayError(err = '') {
  if (err != '') {
    $("#errorMsg").html(err);
  }
  $("#errorMsg").removeClass("d-none");
}

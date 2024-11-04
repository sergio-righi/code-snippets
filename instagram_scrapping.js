var result = [];
var currentIndex = 0;
var main = document.body?.querySelector("main");
var postsContainer = main?.firstElementChild?.lastElementChild;
var posts = [...postsContainer?.querySelectorAll("img")];

function getContent(contentType) {
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        img { width: 100%; display: block; cursor: pointer; }
        button { width: 100px; }
        button { display: block; margin-top: 8px; }
        #image-container { column-count: 2; column-gap: 0; }
        #toolbar-container { z-index: 9; position: fixed; top: 8px; right: 8px; }
        .selected { opacity: 0.7 }
        @media(min-width: 768px) { #image-container { column-count: 4; }
        @media(min-width: 1024px) { #image-container { column-count: 6; }
      </style>
    </head>
    <body>
      ${
        contentType === "grid"
          ? `<div id="toolbar-container">
        <button id="close-button">Close</button>
        <button id="copy-button">Copy</button>
        <button id="download-button">Download</button>
      </div>`
          : ""
      }
      <div id="image-container">
        ${unique()
          .map((item, index) => `<img id="image-${index}" src="${item}" />`)
          .join("")}
      </div>
    </body>
    </html>
  `;
}

function openNewWindow(contentType) {
  // Open a new tab or window and load the Blob URL
  const newWindow = window.open();
  newWindow.document.write(getContent(contentType));
  newWindow.document.close();
}

function openWindow(contentType) {
  if (result.length === 0) return;

  // Create a new iframe
  const iframe = document.createElement("iframe");
  iframe.style.top = "0px";
  iframe.style.left = "0px";
  iframe.style.width = "100%";
  iframe.style.height = "40vh";
  iframe.style.border = "none";
  iframe.style.position = "fixed";
  document.body.appendChild(iframe);

  // Write the HTML into the iframe
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  iframeDoc.open();
  iframeDoc.write(getContent(contentType));
  iframeDoc.close();

  // Once the iframe is ready, add the interactivity
  iframe.onload = function () {
    let selectedImages = [];
    const iframeWindow = iframe.contentWindow;

    function toggleImage(src, imgElement) {
      const index = selectedImages.indexOf(src);
      if (index > -1) {
        selectedImages.splice(index, 1); // Remove if already selected
        imgElement.classList.remove("selected"); // Remove visual indicator
      } else {
        selectedImages.push(src); // Add if not selected
        imgElement.classList.add("selected"); // Add visual indicator
      }
    }

    function getInstagramProfileName() {
      const title = document.title; // Get the title of the document
      const match = title.match(/@([a-zA-Z0-9_.]+)/); // Check if the title is in the expected format
      // If there is a match, return the profile name; otherwise, return null or an error message
      return match ? match[1] : null;
    }

    function clearSelection() {
      selectedImages = [];
      iframeWindow.document.querySelectorAll("img").forEach((img) => {
        img.classList.remove("selected");
      });
    }

    // Attach click event listeners to each image
    unique().forEach((src, index) => {
      const imgElement = iframeWindow.document.getElementById(`image-${index}`);
      imgElement.addEventListener("click", () => {
        toggleImage(src, imgElement);
      });
    });

    // Function to copy selected images to clipboard
    iframeWindow.document
      .getElementById("copy-button")
      .addEventListener("click", function () {
        const content = selectedImages.join("\n");
        const tempTextArea = iframeWindow.document.createElement("textarea");
        tempTextArea.value = content;
        iframeWindow.document.body.appendChild(tempTextArea);
        tempTextArea.select();
        iframeWindow.document.execCommand("copy");
        iframeWindow.document.body.removeChild(tempTextArea);
        clearSelection(); // Clear selection after downloading
      });

    // Add event listener to the close button
    iframeWindow.document
      .getElementById("close-button")
      .addEventListener("click", () => {
        iframe.remove(); // Remove the iframe from the DOM
      });

    // Function to download the list of selected images as a .txt file
    iframeWindow.document
      .getElementById("download-button")
      .addEventListener("click", () => {
        // Create a Blob with the selected images content
        const content = selectedImages.join("\n");
        const blob = new Blob([content], { type: "text/plain" });
        const url = URL.createObjectURL(blob);

        // Create a temporary anchor element and trigger the download
        const a = document.createElement("a");
        a.href = url;
        a.download = `${getInstagramProfileName()}.txt`;
        a.click();

        // Clean up
        URL.revokeObjectURL(url);

        clearSelection(); // Clear selection after downloading
      });
  };
}

function unique() {
  const list = [];
  result.forEach((item) => (!list.includes(item) ? list.push(item) : null));
  return list;
}

async function imageBitmapToSrc(imageBitmap) {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  // Set canvas dimensions to match the video frame
  canvas.width = imageBitmap.width;
  canvas.height = imageBitmap.height;

  // Draw the ImageBitmap onto the canvas
  ctx.drawImage(imageBitmap, 0, 0);

  // Convert the canvas to a Blob, then to a URL
  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      resolve(url);
    });
  });
}

async function getVideoElement(src) {
  const videos = document.getElementsByTagName("video");
  const video = [...videos].find((item) => item.src === src);
  await video.play();
  return video;
}

async function processVideo(src) {
  result = [];
  if (HTMLVideoElement.prototype.requestVideoFrameCallback) {
    const video = await getVideoElement(src);
    const duration = Math.floor(video?.duration) * 5;
    const frames = [];

    const drawingLoop = async (timestamp, frame) => {
      const mediaTime = frame.mediaTime;

      if (!frames.includes(mediaTime)) {
        frames.push(mediaTime);
        const imageBitmap = await createImageBitmap(video);
        const img = await imageBitmapToSrc(imageBitmap); // Convert the ImageBitmap to src
        result.push(img);
      }

      if (frames.length === duration) {
        await video.pause();
        openNewWindow("video");
      } else {
        video.requestVideoFrameCallback(drawingLoop);
      }
    };

    video.requestVideoFrameCallback(drawingLoop);
  } else {
    console.error("your browser doesn't support this API yet");
  }
}

function processSimple() {
  result = grid.map((item) => item.src);
  openWindow("grid");
}

function run() {
  posts[currentIndex++].click();

  setTimeout(() => {
    const article = document.getElementsByTagName("article")[0];
    const dialog = document.querySelector("div[role=dialog]");
    const parentContainer =
      dialog.parentElement?.parentElement?.parentElement?.parentElement;
    const closeButton = parentContainer?.childNodes[1].firstElementChild;
    const postContainer = article.firstElementChild?.firstElementChild;
    const video = postContainer?.querySelector("video");
    const ul = postContainer.querySelector("ul");

    function processImage(isLast) {
      let img = null;
      if (ul) {
        const length = ul.childNodes.length;
        const li = ul.childNodes[isLast ? length - 1 : length - 2];
        img = li.querySelector("img");
      } else {
        img = postContainer.querySelector("img");
      }
      if (img) {
        result.push(img.src);
      }
    }

    function moveToNext() {
      let button = postContainer?.querySelector("button[aria-label=Next]");
      if (button) {
        processImage(false);
        button.click();
        setTimeout(moveToNext, 150);
      } else {
        if (video) {
          console.log(video.src);
        } else {
          processImage(true);
        }
        closeButton.click();
        setTimeout(function () {
          if (posts.length > currentIndex) {
            run();
          } else {
            openWindow("grid");
          }
        }, 200);
      }
    }

    moveToNext();
  }, 300);
}

run();

var result = [];

const main = document.body?.querySelector("main");
const grid = [...main?.querySelectorAll("img")];

function generate() {
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

  // Custom HTML content for the iframe
  const htmlContent = `
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
      <div id="toolbar-container">
        <button id="close-button">Close</button>
        <button id="copy-button">Copy</button>
        <button id="download-button">Download</button>
      </div>
      <div id="image-container">
        ${unique()
          .map((item, index) => `<img id="image-${index}" src="${item}" />`)
          .join("")}
      </div>
    </body>
    </html>
  `;

  // Write the HTML into the iframe
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  iframeDoc.open();
  iframeDoc.write(htmlContent);
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

function start() {
  result = grid.map((item) => item.src);
  generate();
}

start();

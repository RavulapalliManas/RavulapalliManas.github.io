// FILE: main.js
function setupLightbox() {
  const dialog = document.getElementById("lightbox-dialog");
  const triggers = Array.from(document.querySelectorAll("[data-lightbox-index]"));
  if (!dialog || !triggers.length) {
    return;
  }

  const image = dialog.querySelector(".lightbox-dialog__image");
  const closeButton = dialog.querySelector(".lightbox-dialog__close");
  const prevButton = dialog.querySelector(".lightbox-dialog__nav--prev");
  const nextButton = dialog.querySelector(".lightbox-dialog__nav--next");
  let activeIndex = 0;

  const items = triggers.map((trigger) => ({
    src: trigger.getAttribute("data-lightbox-src"),
    alt: trigger.getAttribute("data-lightbox-alt")
  }));

  function render(index) {
    const item = items[index];
    if (!item) {
      return;
    }
    activeIndex = index;
    image.src = item.src;
    image.alt = item.alt;
  }

  function open(index) {
    render(index);
    if (!dialog.open) {
      dialog.showModal();
    }
  }

  function close() {
    if (dialog.open) {
      dialog.close();
    }
  }

  function step(delta) {
    const nextIndex = (activeIndex + delta + items.length) % items.length;
    render(nextIndex);
  }

  triggers.forEach((trigger, index) => {
    trigger.addEventListener("click", () => open(index));
  });

  closeButton.addEventListener("click", close);
  prevButton.addEventListener("click", () => step(-1));
  nextButton.addEventListener("click", () => step(1));

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      close();
    }
  });

  dialog.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      close();
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      step(-1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      step(1);
    }
  });
}

setupLightbox();

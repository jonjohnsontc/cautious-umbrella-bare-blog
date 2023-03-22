/**
 * Script to show dropdown menu when clicked
 * */
const palette = document.getElementById("palette");
function dropDown() {
  document.getElementById("dropdown-content").classList.toggle("open");
}
palette.addEventListener("click", () => {
  dropDown();
});
window.onclick = function (event) {
  if (
    !event.target.matches("#dropdown-content") &&
    !event.target.matches("#palette")
  ) {
    const dropDown = document.getElementById("dropdown-content");
    if (dropDown.classList.contains("open")) {
      dropDown.classList.remove("open");
    }
  }
};

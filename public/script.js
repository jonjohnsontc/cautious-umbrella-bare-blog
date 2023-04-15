/**
 * Script to show dropdown menu when clicked
 * */
const dropdownBtn = document.getElementById("dropdown-button");
const content = document.getElementById("dropdown-content");
function toggleDropdown() {
	content.classList.toggle("open");
}
dropdownBtn.addEventListener("click", (e) => {
	e.stopPropagation();
	toggleDropdown();
});
document.documentElement.addEventListener("click", () => {
	if (content.classList.contains("open")) {
		toggleDropdown();
	}
});

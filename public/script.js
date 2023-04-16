// *Script to show dropdown menu when clicked*
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

// *Change theme when button is clicked*
// If I already have a class on the root element, I would like
// to remove that class, and replace it with the new one
const gruvbox = document.getElementById("gruvbox");
const booberry = document.getElementById("booberry");
const dark = document.getElementById("dark");
function toggleTheme(name) {
	let classList = document.body.classList;
	while (classList.length > 0) {
		classList.remove(classList.item(0));
	}
	window.localStorage.setItem("theme", name);
	classList.add(name);
}
gruvbox.addEventListener("click", () => {
	toggleTheme("gruvbox");
});
booberry.addEventListener("click", () => {
	toggleTheme("booberry");
});
dark.addEventListener("click", () => {
	toggleTheme("dark");
});
if (window.localStorage.getItem("theme")) {
	toggleTheme(window.localStorage.getItem("theme"));
}

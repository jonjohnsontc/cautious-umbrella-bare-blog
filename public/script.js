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
	// toggle the theme in the body
	let classList = document.body.classList;
	while (classList.length > 0) {
		classList.remove(classList.item(0));
	}
	window.localStorage.setItem("theme", name);
	classList.add(name);

	// untoggle any active theme btn
	const prevActiveBtns = document.getElementsByClassName(
		"theme-button--active"
	);
	if (prevActiveBtns) {
		for (let i; i < prevActiveBtns.length; i++) {
			const prevActive = prevActiveBtns[i].classList;
			if (prevActive) {
				prevActive.remove("theme-button--active");
			}
		}
	}

	// add the active class for the new btn
	let activeBtn = document.getElementById(name);
	let activeBtnClasses = activeBtn.classList;
	activeBtnClasses.add("theme-button--active");
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

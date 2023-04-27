// *Script to add popover footnotes*
const footnotes = document.getElementsByClassName("footnote");
/**
 * Checks the document for footnotes, and if any exist, copies them from the bottom
 * of the document as popover asides
 * @param {HTMLCollection} el The footnote element to check
 * @returns {void}
 */
function addFootnotes(el) {
	// if there are any footnotes we'll add some
	if (el.length > 0) {
		// Get copies of ref and backref pairs (a-tags)
		const refs = Array.from(document.getElementsByClassName("footnote-ref"));
		const backrefs = Array.from(
			document.getElementsByClassName("footnote-backref")
		);
		// if they have the same length, we'll generate the footnotes
		if (refs.length === backrefs.length) {
			for (let i = 0; i < refs.length; i++) {
				// create a footnote and insert text content
				const fn = document.createElement("aside");
				fn.className = "footnote-content swing-in-top-fwd";
				const fnEl = backrefs[i].parentElement.parentElement.cloneNode(true);
				const fnContent = fnEl.children;
				// iterate through and remove any backref links from the footnote
				for (let child of fnContent) {
					if (child.querySelector(".footnote-backref")) {
						const backrefToRemove = child.querySelector(".footnote-backref");
						child.removeChild(backrefToRemove);
					}
				}
				fn.append(...fnContent);
				// the superscript text
				const sup = refs[i].parentElement;
				// remove the a link from the superscipt
				const aEl = sup.querySelector("a.footnote-ref");
				aEl.removeAttribute("href");
				// create a new button element for the superscipt
				// and copy over the a elements children
				const buttonEl = document.createElement("button");
				buttonEl.className = "footnote-btn";
				while (aEl.firstChild) {
					buttonEl.appendChild(aEl.firstChild);
				}
				aEl.replaceWith(buttonEl);
				// Add footnote as child of button element
				buttonEl.appendChild(fn);
				// add an event listener to open the aside
				sup.addEventListener("click", (e) => {
					e.stopPropagation();
					fn.classList.toggle("open");
				});
				// add document event listener to remove footnote "off-click"
				document.documentElement.addEventListener("click", () => {
					if (fn.classList.contains("open")) {
						fn.classList.toggle("open");
					}
				});
			}
		}
	}
}

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

	const themeMap = new Map([
		["gruvbox", "#b16286"],
		["booberry", "#7139bf"],
		["dark", "#1b1436"],
	]);
	// replace meta theme element
	const metaTheme = document.querySelector("meta[name=theme-color]");
	metaTheme.setAttribute("content", themeMap.get(name));

	// untoggle any active theme btn
	const prevActiveBtns = document.getElementsByClassName(
		"theme-button--active"
	);
	for (let i = 0; i < prevActiveBtns.length; i++) {
		const prevActive = prevActiveBtns[i].classList;
		if (prevActive) {
			prevActive.remove("theme-button--active");
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
addFootnotes(footnotes);

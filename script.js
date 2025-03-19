const nav = document.querySelector(".nav"),
  searchIcon = document.querySelector("#searchIcon"),
  navOpenBtn = document.querySelector(".navOpenBtn"),
  navCloseBtn = document.querySelector(".navCloseBtn"),
  mainSearchBox = document.querySelector(".main-search-box input"),
  mainSearchBtn = document.querySelector(".main-search-box button");

// Navbar search icon functionality
searchIcon.addEventListener("click", () => {
  nav.classList.toggle("openSearch");
  nav.classList.remove("openNav");
  if (nav.classList.contains("openSearch")) {
    return searchIcon.classList.replace("uil-search", "uil-times");
  }
  searchIcon.classList.replace("uil-times", "uil-search");
});

navOpenBtn.addEventListener("click", () => {
  nav.classList.add("openNav");
  nav.classList.remove("openSearch");
  searchIcon.classList.replace("uil-times", "uil-search");
});

navCloseBtn.addEventListener("click", () => {
  nav.classList.remove("openNav");
});

// Main search functionality
function performSearch() {
  const query = mainSearchBox.value.trim(); // Get search input
  if (query !== "") {
    alert(`Searching for: ${query}`);
    // Redirect or handle search results (modify as needed)
    // window.location.href = `search.html?q=${query}`;
  }
}

// Search when button is clicked
mainSearchBtn.addEventListener("click", performSearch);

// Search when "Enter" key is pressed
mainSearchBox.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    performSearch();
  }
});
